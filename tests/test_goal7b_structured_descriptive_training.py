import json
import html as html_module
import re
import unittest

from sqlalchemy import inspect, select

from app import create_app
from app.config import Config
from app.models import database
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.analytics_service import AnalyticsService
from app.services.csrf_service import CSRF_SESSION_KEY
from app.services.data_loader import DataLoader
from app.services.descriptive_training_evaluator import DescriptiveTrainingEvaluator
from app.services.descriptive_training_service import DescriptiveTrainingService
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class TestGoal7BStructuredDescriptiveTraining(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.client.get("/descriptive-training")
        with self.client.session_transaction() as sess:
            sess["is_admin"] = True
            self.csrf_token = sess[CSRF_SESSION_KEY]

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def _start(self, scope_kind="all", category="", count="5", client=None, token=None):
        client = client or self.client
        token = token or self.csrf_token
        response = client.post(
            "/descriptive-training/start",
            data={
                "csrf_token": token,
                "scope_kind": scope_kind,
                "category": category,
                "count": count,
            },
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        location = response.headers["Location"]
        return int(location.rstrip("/").split("/")[-1]), location

    def _force_question_set(self, attempt_id, question_ids):
        with self.app.app_context():
            meta = db_session.scalar(select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_type == DescriptiveTrainingService.META_QUESTION_TYPE,
            ))
            config = meta.get_parsed_self_eval()
            config.update({
                "question_ids": question_ids,
                "current_index": 0,
                "phase": "question",
                "latest_record_id": None,
            })
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()

    def _answer_data(self, question, complete=True):
        data = {"csrf_token": self.csrf_token}
        for index, sub in enumerate(question.get("sub_questions", [])):
            field = f"ans_{question['id']}_{sub['sub_id']}"
            data[field] = sub.get("model_answer", "") if complete or index == 0 else ""
        return data

    def test_01_entry_setup_scopes_and_counts(self):
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn('href="/descriptive-training"', home)
        response = self.client.get("/descriptive-training")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("서술형 구조 훈련", html)
        self.assertIn('name="scope_kind" value="all"', html)
        self.assertIn('name="scope_kind" value="category"', html)
        for count in ("5", "10", "all"):
            self.assertIn(f'value="{count}"', html)
        for category in {q["category"] for q in self.loader.load_questions() if q["type"] == "descriptive"}:
            self.assertIn(category, html)

    def test_02_question_appropriate_fields_hide_feedback_before_submit(self):
        question = next(q for q in self.loader.get_enriched_questions() if q["type"] == "descriptive")
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        html = self.client.get(location).get_data(as_text=True)
        rendered_text = html_module.unescape(html)
        for sub in question["sub_questions"]:
            self.assertIn(f'name="ans_{question["id"]}_{sub["sub_id"]}"', html)
            self.assertIn(sub["prompt"], rendered_text)
            self.assertNotIn(sub["model_answer"], rendered_text)
        self.assertIn("문제 맞춤 답안 구조", html)
        self.assertNotIn("핵심 / 누락 키워드 분석", html)
        self.assertNotIn("ai-prompt-modal", html)

    def test_03_structure_evaluation_covers_all_three_states(self):
        question = {
            "id": "Q-TEST",
            "score": 4,
            "sub_questions": [
                {"sub_id": 1, "score": 2, "prompt": "설정", "model_answer": "alpha", "rubric": {"keywords": [["alpha"]], "all_match_points": 2}},
                {"sub_id": 2, "score": 2, "prompt": "효과", "model_answer": "beta", "rubric": {"keywords": [["beta"]], "all_match_points": 2}},
            ],
        }
        full = DescriptiveTrainingEvaluator.evaluate(question, {"1": "alpha", "2": "beta"})
        partial = DescriptiveTrainingEvaluator.evaluate(question, {"1": "alpha", "2": ""})
        empty = DescriptiveTrainingEvaluator.evaluate(question, {"1": "", "2": ""})
        self.assertEqual(full["structure_evaluation"]["label"], "충족")
        self.assertEqual(partial["structure_evaluation"]["label"], "부분 충족")
        self.assertEqual(empty["structure_evaluation"]["label"], "미충족")

    def test_04_keyword_analysis_uses_boundaries_to_control_false_positives(self):
        question = {
            "id": "Q-BOUNDARY",
            "score": 3,
            "sub_questions": [{
                "sub_id": 1,
                "score": 3,
                "prompt": "경계 검사",
                "model_answer": "no v3 +",
                "rubric": {"keywords": [["no"], ["v3"], ["+"], ["인증"]], "all_match_points": 3, "partial_match_points": 1.5},
            }],
        }
        rejected = DescriptiveTrainingEvaluator.evaluate(question, {"1": "snow v30 C++ 미인증"})
        accepted = DescriptiveTrainingEvaluator.evaluate(question, {"1": "no=101, v3 사용, '+' 설정 제거, 인증 적용"})
        self.assertEqual(rejected["keyword_analysis"]["matched_group_count"], 0)
        self.assertEqual(accepted["keyword_analysis"]["matched_group_count"], 4)
        self.assertIn("부정 표현", accepted["keyword_analysis"]["false_positive_control"])

    def test_05_submission_reveals_rubric_explanation_concept_and_local_ai_helper(self):
        question = next(q for q in self.loader.get_enriched_questions() if q["type"] == "descriptive")
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        response = self.client.post(f"{location}/answer", data=self._answer_data(question), follow_redirects=True)
        html = response.get_data(as_text=True)
        rendered_text = html_module.unescape(html)
        self.assertEqual(response.status_code, 200)
        self.assertIn("구조 평가", html)
        self.assertIn("핵심 / 누락 키워드 분석", html)
        self.assertIn(question["model_answer"], rendered_text)
        self.assertIn(question["explanation"], rendered_text)
        self.assertIn("explanation-accordion", html)
        self.assertIn("btn-ai-helper", html)
        self.assertIn("https://chatgpt.com/", html)
        self.assertIn("https://gemini.google.com/app", html)
        self.assertNotRegex(html, r"https://(?:chatgpt\.com|gemini\.google\.com)[^\"']*[?&](?:prompt|q|text)=")

    def test_06_refresh_and_duplicate_post_are_idempotent_and_csrf_protected(self):
        question = next(q for q in self.loader.get_enriched_questions() if q["type"] == "descriptive")
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        invalid = self.client.post(f"{location}/answer", data={})
        self.assertEqual(invalid.status_code, 403)
        data = self._answer_data(question)
        self.client.post(f"{location}/answer", data=data)
        self.client.post(f"{location}/answer", data=data)
        self.client.get(location)
        with self.app.app_context():
            records = list(db_session.scalars(select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_type != DescriptiveTrainingService.META_QUESTION_TYPE,
            )).all())
            self.assertEqual(len(records), 1)
            self.assertEqual(DescriptiveTrainingService(self.loader).get_state(attempt_id)["phase"], "complete")

    def test_07_guest_and_owner_sessions_are_isolated(self):
        guest = self.app.test_client()
        stranger = self.app.test_client()
        guest.get("/descriptive-training")
        with guest.session_transaction() as sess:
            guest_token = sess[CSRF_SESSION_KEY]
        _, guest_location = self._start(client=guest, token=guest_token)
        self.assertEqual(guest.get(guest_location).status_code, 200)
        self.assertEqual(stranger.get(guest_location).status_code, 403)
        _, owner_location = self._start()
        self.assertEqual(self.client.get(owner_location).status_code, 200)
        self.assertEqual(guest.get(owner_location).status_code, 403)

    def test_08_training_records_do_not_pollute_normal_exam_features(self):
        question = next(q for q in self.loader.get_enriched_questions() if q["type"] == "descriptive")
        attempt_id, location = self._start()
        self._force_question_set(attempt_id, [question["id"]])
        self.client.post(f"{location}/answer", data=self._answer_data(question, complete=False))
        with self.app.app_context():
            attempt = db_session.get(ExamAttempt, attempt_id)
            self.assertEqual(attempt.exam_mode, DescriptiveTrainingService.MODE)
            self.assertTrue(attempt.is_owner)
            self.assertEqual(HistoryService(self.loader).get_attempt_count(), 0)
            self.assertEqual(AnalyticsService(self.loader).get_summary_stats()["total_attempts"], 0)
            self.assertEqual(WrongAnswerService(self.loader).get_wrong_question_count(), 0)

    def test_09_progression_and_session_count_are_persisted(self):
        questions = [q for q in self.loader.get_enriched_questions() if q["type"] == "descriptive"][:2]
        attempt_id, location = self._start(count="10")
        self._force_question_set(attempt_id, [q["id"] for q in questions])
        self.client.post(f"{location}/answer", data=self._answer_data(questions[0]))
        with self.app.app_context():
            state = DescriptiveTrainingService(self.loader).get_state(attempt_id)
            self.assertEqual(state["phase"], "graded")
            self.assertEqual(state["answered_count"], 1)
        self.client.post(f"{location}/next", data={"csrf_token": self.csrf_token})
        with self.app.app_context():
            state = DescriptiveTrainingService(self.loader).get_state(attempt_id)
            self.assertEqual(state["phase"], "question")
            self.assertEqual(state["question_number"], 2)

    def test_10_existing_schema_is_reused_without_new_tables_or_columns(self):
        with self.app.app_context():
            inspector = inspect(database.engine)
            self.assertEqual(set(inspector.get_table_names()), {"answer_records", "exam_attempts"})
            self.assertEqual(
                {column["name"] for column in inspector.get_columns("exam_attempts")},
                {
                    "id", "submission_token", "exam_mode", "seed", "started_at", "submitted_at",
                    "duration_seconds", "total_score", "short_score", "descriptive_score",
                    "practical_score", "selected_practical_id", "is_passed", "is_owner", "created_at",
                },
            )

    def test_11_invalid_scope_and_count_fail_closed(self):
        bad_scope = self.client.post(
            "/descriptive-training/start",
            data={"csrf_token": self.csrf_token, "scope_kind": "search", "count": "5"},
        )
        bad_count = self.client.post(
            "/descriptive-training/start",
            data={"csrf_token": self.csrf_token, "scope_kind": "all", "count": "180"},
        )
        self.assertEqual(bad_scope.status_code, 400)
        self.assertEqual(bad_count.status_code, 400)
        self.assertNotIn("/search", bad_scope.get_data(as_text=True))

    def test_12_responsive_styles_and_no_disallowed_goal_scope(self):
        css = (self.app.root_path + "/static/css/style.css")
        with open(css, "r", encoding="utf-8") as handle:
            stylesheet = handle.read()
        self.assertIn(".desc-evaluation-grid", stylesheet)
        self.assertRegex(stylesheet, r"@media\s*\(max-width:\s*767px\)")
        setup = self.client.get("/descriptive-training").get_data(as_text=True)
        for forbidden in ("180-minute", "Review Flag", "RAG", "bookmark", "/search"):
            self.assertNotIn(forbidden, setup)


if __name__ == "__main__":
    unittest.main()
