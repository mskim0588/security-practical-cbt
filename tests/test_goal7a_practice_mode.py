import json
import re
import unittest
from unittest.mock import patch

from sqlalchemy import select

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.analytics_service import AnalyticsService
from app.services.csrf_service import CSRF_SESSION_KEY
from app.services.data_loader import DataLoader
from app.services.grader import Grader
from app.services.history_service import HistoryService
from app.services.practice_service import PracticeService
from app.services.wrong_answer_service import WrongAnswerService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class TestGoal7APracticeMode(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.client.get("/practice")
        with self.client.session_transaction() as sess:
            sess["is_admin"] = True
            self.csrf_token = sess[CSRF_SESSION_KEY]

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def _start(self, rounds="1", scope_kind="all", category="", question_type=""):
        response = self.client.post(
            "/practice/start",
            data={
                "csrf_token": self.csrf_token,
                "rounds": rounds,
                "scope_kind": scope_kind,
                "category": category,
                "question_type": question_type,
            },
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        location = response.headers["Location"]
        attempt_id = int(location.rstrip("/").split("/")[-1])
        return attempt_id, location

    def _force_question_set(self, attempt_id, question_ids):
        with self.app.app_context():
            meta = db_session.scalar(
                select(AnswerRecord).where(
                    AnswerRecord.attempt_id == attempt_id,
                    AnswerRecord.question_type == PracticeService.META_QUESTION_TYPE,
                )
            )
            config = meta.get_parsed_self_eval()
            config["question_ids"] = question_ids
            config["current_round"] = 1
            config["current_index"] = 0
            config["phase"] = "question"
            config["latest_record_id"] = None
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()

    def _short_answer_data(self, question, mode="correct"):
        data = {"csrf_token": self.csrf_token}
        sub_questions = question.get("sub_questions") or []
        if sub_questions:
            for index, sub in enumerate(sub_questions):
                value = sub.get("answer", "") if mode == "correct" or (mode == "partial" and index == 0) else "wrong"
                data[f"ans_{question['id']}_{sub['label']}"] = value
        else:
            data[f"ans_{question['id']}"] = question.get("answer", "") if mode == "correct" else "wrong"
        return data

    def _multi_short_question(self):
        return next(
            q for q in self.loader.get_enriched_questions()
            if q["type"] == "short" and len(q.get("sub_questions") or []) >= 2
        )

    def _single_short_question(self):
        return next(
            q for q in self.loader.get_enriched_questions()
            if q["type"] == "short" and not q.get("sub_questions")
        )

    def test_01_setup_supports_rounds_and_existing_scopes(self):
        response = self.client.get("/practice")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for rounds in ("1", "2", "3"):
            self.assertIn(f'name="rounds" value="{rounds}"', html)
        for scope in ("all", "category", "type"):
            self.assertIn(f'name="scope_kind" value="{scope}"', html)
        for category in sorted({q["category"] for q in self.loader.load_questions()}):
            self.assertIn(category, html)
        for question_type in ("short", "descriptive", "practical"):
            self.assertIn(f'value="{question_type}"', html)

    def test_02_scope_retains_selected_question_set_across_rounds(self):
        category = self.loader.load_questions()[0]["category"]
        attempt_id, _ = self._start(rounds="2", scope_kind="category", category=category)
        with self.app.app_context():
            service = PracticeService(self.loader)
            state = service.get_state(attempt_id)
            meta = service._get_meta_record(attempt_id)
            config = meta.get_parsed_self_eval()
            expected_ids = {q["id"] for q in self.loader.load_questions() if q["category"] == category}
            self.assertEqual(set(config["question_ids"]), expected_ids)
            self.assertEqual(state["rounds"], 2)
            self.assertEqual(state["scope_label"], f"카테고리 · {category}")

    def test_03_pre_submit_hides_answers_explanation_and_ai(self):
        question = self._single_short_question()
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        response = self.client.get(location)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("accepted-answer-list", html)
        self.assertNotIn("explanation-accordion", html)
        self.assertNotIn("btn-ai-helper", html)
        self.assertNotIn("ai-prompt-modal", html)
        self.assertNotIn(question.get("answer", ""), html)

    def test_04_submission_uses_canonical_grader_and_reveals_learning_content(self):
        question = self._single_short_question()
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        with patch.object(Grader, "grade_short_question", wraps=Grader.grade_short_question) as canonical:
            response = self.client.post(
                f"{location}/answer",
                data=self._short_answer_data(question, "correct"),
                follow_redirects=True,
            )
        html = response.get_data(as_text=True)
        self.assertEqual(canonical.call_count, 1)
        self.assertIn("practice-result-correct", html)
        self.assertIn("accepted-answer-list", html)
        self.assertIn("explanation-accordion", html)
        self.assertIn("btn-ai-helper", html)
        self.assertIn("https://chatgpt.com/", html)
        self.assertIn("https://gemini.google.com/app", html)
        self.assertNotIn("?prompt=", html)

    def test_05_immediate_results_cover_correct_partial_and_wrong(self):
        question = self._multi_short_question()
        observed = []
        for mode in ("correct", "partial", "wrong"):
            attempt_id, location = self._start()
            self._force_question_set(attempt_id, [question["id"]])
            response = self.client.post(
                f"{location}/answer",
                data=self._short_answer_data(question, mode),
                follow_redirects=True,
            )
            html = response.get_data(as_text=True)
            expected = {"correct": "correct", "partial": "partial", "wrong": "wrong"}[mode]
            self.assertIn(f"practice-result-{expected}", html)
            with self.app.app_context():
                state = PracticeService(self.loader).get_state(attempt_id)
                observed.append(state["result"]["status"])
        self.assertEqual(observed, ["correct", "partial", "wrong"])

    def test_06_attempts_latest_result_and_round_progress_update(self):
        question = self._single_short_question()
        attempt_id, location = self._start(rounds="2")
        self._force_question_set(attempt_id, [question["id"]])
        self.client.post(f"{location}/answer", data=self._short_answer_data(question, "wrong"))
        with self.app.app_context():
            state = PracticeService(self.loader).get_state(attempt_id)
            self.assertEqual(state["question_attempts"], 1)
            self.assertEqual(state["latest_result"], "wrong")
            self.assertEqual(state["status_counts"], {"correct": 0, "partial": 0, "wrong": 1})
        self.client.post(f"{location}/next", data={"csrf_token": self.csrf_token})
        self.client.post(f"{location}/answer", data=self._short_answer_data(question, "correct"))
        with self.app.app_context():
            state = PracticeService(self.loader).get_state(attempt_id)
            self.assertEqual(state["current_round"], 2)
            self.assertEqual(state["question_attempts"], 2)
            self.assertEqual(state["latest_result"], "correct")

    def test_07_round_transitions_and_final_completion(self):
        question = self._single_short_question()
        attempt_id, location = self._start(rounds="3")
        self._force_question_set(attempt_id, [question["id"]])
        for expected_round in (1, 2, 3):
            response = self.client.post(
                f"{location}/answer",
                data=self._short_answer_data(question, "correct"),
                follow_redirects=True,
            )
            with self.app.app_context():
                state = PracticeService(self.loader).get_state(attempt_id)
                self.assertEqual(state["current_round"], expected_round)
                self.assertEqual(state["round_summary"]["correct"], 1)
            if expected_round < 3:
                self.assertIn("practice-round-summary", response.get_data(as_text=True))
                self.client.post(f"{location}/next", data={"csrf_token": self.csrf_token})
        with self.app.app_context():
            state = PracticeService(self.loader).get_state(attempt_id)
            self.assertEqual(state["phase"], "complete")
            self.assertTrue(state["is_final_complete"])
            self.assertEqual(state["question_attempts"], 3)

    def test_08_refresh_and_duplicate_posts_do_not_double_count(self):
        question = self._single_short_question()
        attempt_id, location = self._start(rounds="2")
        self._force_question_set(attempt_id, [question["id"]])
        data = self._short_answer_data(question, "wrong")
        self.client.post(f"{location}/answer", data=data)
        self.client.post(f"{location}/answer", data=data)
        self.client.get(location)
        self.client.get(location)
        with self.app.app_context():
            records = list(db_session.scalars(select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_type != PracticeService.META_QUESTION_TYPE,
            )).all())
            state = PracticeService(self.loader).get_state(attempt_id)
            self.assertEqual(len(records), 1)
            self.assertEqual(state["question_attempts"], 1)
            self.assertEqual(state["phase"], "round_complete")

    def test_09_no_raw_source_metadata_and_ai_policy_regression(self):
        question = self._single_short_question()
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        response = self.client.post(
            f"{location}/answer",
            data=self._short_answer_data(question, "wrong"),
            follow_redirects=True,
        )
        html = response.get_data(as_text=True)
        for forbidden in ("source_type", "total_pages", "private path", "'filename':", '"filename":'):
            self.assertNotIn(forbidden, html)
        self.assertIn("data-ai-context", html)
        self.assertIn("프롬프트는 이 사이트에서만 생성되며 외부 AI에 자동 전송되지 않습니다.", html)
        self.assertNotRegex(html, r"https://(?:chatgpt\.com|gemini\.google\.com)[^\"']*[?&](?:prompt|q|text)=")
        self.assertNotIn("btn-ai-helper", self.client.get("/exam").get_data(as_text=True))

    def test_10_practice_records_do_not_pollute_normal_learning_analytics(self):
        question = self._single_short_question()
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        self.client.post(f"{location}/answer", data=self._short_answer_data(question, "wrong"))
        with self.app.app_context():
            self.assertEqual(HistoryService(self.loader).get_attempt_count(), 0)
            self.assertEqual(AnalyticsService(self.loader).get_summary_stats()["total_attempts"], 0)
            self.assertEqual(WrongAnswerService(self.loader).get_wrong_question_count(), 0)
            attempt = db_session.get(ExamAttempt, attempt_id)
            self.assertEqual(attempt.exam_mode, "practice")
            self.assertTrue(attempt.is_owner)

    def test_11_guest_and_owner_practice_isolation(self):
        guest = self.app.test_client()
        stranger = self.app.test_client()

        guest.get("/practice")
        with guest.session_transaction() as sess:
            guest_token = sess[CSRF_SESSION_KEY]
        response = guest.post(
            "/practice/start",
            data={"csrf_token": guest_token, "rounds": "1", "scope_kind": "type", "question_type": "short"},
        )
        guest_location = response.headers["Location"]
        self.assertEqual(guest.get(guest_location).status_code, 200)
        self.assertEqual(stranger.get(guest_location).status_code, 403)

        response = self.client.post(
            "/practice/start",
            data={"csrf_token": self.csrf_token, "rounds": "1", "scope_kind": "type", "question_type": "short"},
        )
        owner_location = response.headers["Location"]
        self.assertEqual(self.client.get(owner_location).status_code, 200)
        self.assertEqual(guest.get(owner_location).status_code, 403)

    def test_12_entry_and_normal_routes_remain_available(self):
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn('href="/practice"', home)
        self.assertIn("회독 학습", home)
        for route in ("/exam", "/result/999999", "/history", "/wrong-notes", "/concepts", "/dashboard"):
            response = self.client.get(route)
            self.assertIn(response.status_code, (200, 403, 404), route)

    def test_13_all_existing_question_types_render_and_grade(self):
        questions = self.loader.get_enriched_questions()
        for question_type in ("short", "descriptive", "practical"):
            question = next(q for q in questions if q["type"] == question_type)
            attempt_id, location = self._start()
            self._force_question_set(attempt_id, [question["id"]])
            before = self.client.get(location).get_data(as_text=True)
            self.assertIn(f'data-practice-phase="question"', before)
            if question_type == "short":
                answer_data = self._short_answer_data(question, "wrong")
            else:
                answer_data = {"csrf_token": self.csrf_token}
                for sub in question.get("sub_questions", []):
                    field = f"ans_{question['id']}_{sub['sub_id']}"
                    self.assertIn(f'name="{field}"', before)
                    answer_data[field] = ""
            after = self.client.post(f"{location}/answer", data=answer_data, follow_redirects=True)
            self.assertEqual(after.status_code, 200)
            self.assertIn("practice-result-", after.get_data(as_text=True))

    def test_14_practice_state_changes_require_valid_csrf(self):
        response = self.client.post(
            "/practice/start",
            data={"rounds": "1", "scope_kind": "all"},
        )
        self.assertEqual(response.status_code, 403)
        attempt_id, location = self._start()
        question = self._single_short_question()
        self._force_question_set(attempt_id, [question["id"]])
        response = self.client.post(
            f"{location}/answer",
            data={f"ans_{question['id']}": "wrong"},
        )
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
