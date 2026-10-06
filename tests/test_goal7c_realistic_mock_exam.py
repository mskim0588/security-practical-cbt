import json
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from sqlalchemy import inspect, select

from app import create_app
from app.config import Config
from app.models import database
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.csrf_service import CSRF_SESSION_KEY
from app.services.data_loader import DataLoader
from app.services.grader import Grader
from app.services.history_service import HistoryService
from app.services.mock_exam_service import MockExamService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class TestGoal7CRealisticMockExam(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.client.get("/mock-exam")
        with self.client.session_transaction() as sess:
            sess["is_admin"] = True
            self.csrf_token = sess[CSRF_SESSION_KEY]

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def _start(self, client=None, token=None):
        client = client or self.client
        token = token or self.csrf_token
        response = client.post(
            "/mock-exam/start",
            data={"csrf_token": token},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        location = response.headers["Location"]
        attempt_id = int(location.split("/mock-exam/", 1)[1].split("?", 1)[0])
        return attempt_id, location

    def _question(self, index):
        return self.loader.get_question_by_id(MockExamService(self.loader).exam_service.get_exam_questions()[index]["id"])

    @staticmethod
    def _answer_data(question, value="persisted answer"):
        data = {}
        if question["type"] == "short":
            subs = question.get("sub_questions") or []
            if subs:
                for sub in subs:
                    data[f"ans_{question['id']}_{sub['label']}"] = value
            else:
                data[f"ans_{question['id']}"] = value
        else:
            for sub in question.get("sub_questions", []):
                data[f"ans_{question['id']}_{sub['sub_id']}"] = value
        return data

    def _save(self, attempt_id, question, index=0, destination="save", extra=None, client=None, token=None):
        data = {
            "csrf_token": token or self.csrf_token,
            "question_id": question["id"],
            "current_index": str(index),
            "destination": destination,
            **self._answer_data(question),
        }
        if extra:
            data.update(extra)
        return (client or self.client).post(
            f"/mock-exam/{attempt_id}/save",
            data=data,
            follow_redirects=False,
        )

    def test_01_entry_and_canonical_composition(self):
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn('href="/mock-exam"', home)
        response = self.client.get("/mock-exam")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("실전 모의고사", html)
        self.assertIn("180분", html)
        with self.app.app_context():
            questions = MockExamService(self.loader).exam_service.get_exam_questions()
            self.assertEqual([q["type"] for q in questions].count("short"), 12)
            self.assertEqual([q["type"] for q in questions].count("descriptive"), 4)
            self.assertEqual([q["type"] for q in questions].count("practical"), 2)
            self.assertEqual(sum(q["score"] for q in questions[:-1]), 100)

    def test_02_duration_refresh_and_schema_reuse(self):
        fixed = datetime(2026, 10, 6, 3, 0, 0)
        with patch.object(MockExamService, "_now", return_value=fixed):
            attempt_id, _ = self._start()
        with self.app.app_context():
            service = MockExamService(self.loader)
            attempt = service.get_attempt(attempt_id)
            started_at = attempt.started_at
            self.assertEqual((service.expiry_at(attempt) - started_at).total_seconds(), 10800)
            columns = {column["name"] for column in inspect(database.engine).get_columns("exam_attempts")}
            self.assertEqual(columns, {
                "id", "submission_token", "exam_mode", "seed", "started_at", "submitted_at",
                "duration_seconds", "total_score", "short_score", "descriptive_score",
                "practical_score", "selected_practical_id", "is_passed", "is_owner", "created_at",
            })
        later = fixed + timedelta(minutes=17)
        with patch.object(MockExamService, "_now", return_value=later):
            first = self.client.get(f"/mock-exam/{attempt_id}?question=0")
            second = self.client.get(f"/mock-exam/{attempt_id}?question=0")
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        with self.app.app_context():
            self.assertEqual(MockExamService(self.loader).get_attempt(attempt_id).started_at, started_at)

    def test_03_answer_navigation_and_refresh_persistence(self):
        attempt_id, _ = self._start()
        question = self._question(0)
        response = self._save(attempt_id, question, destination="next")
        self.assertEqual(response.status_code, 302)
        self.assertIn("question=1", response.headers["Location"])
        refreshed = self.client.get(f"/mock-exam/{attempt_id}?question=0").get_data(as_text=True)
        self.assertIn("persisted answer", refreshed)
        with self.app.app_context():
            state = MockExamService(self.loader).get_state(attempt_id)
            self.assertEqual(state["answered_count"], 1)
            self.assertEqual(state["items"][0]["state_text"], "답변 완료")

    def test_04_review_flag_toggle_persistence_and_isolation(self):
        first_id, _ = self._start()
        second_id, _ = self._start()
        question = self._question(0)
        flagged = self._save(first_id, question, extra={"review_flag": "1"})
        self.assertEqual(flagged.status_code, 302)
        with self.app.app_context():
            service = MockExamService(self.loader)
            self.assertTrue(service.get_state(first_id)["items"][0]["is_flagged"])
            self.assertFalse(service.get_state(second_id)["items"][0]["is_flagged"])
        unflag = self.client.post(
            f"/mock-exam/{first_id}/flag",
            data={"csrf_token": self.csrf_token, "question_id": question["id"], "current_index": "0"},
        )
        self.assertEqual(unflag.status_code, 302)
        with self.app.app_context():
            self.assertFalse(MockExamService(self.loader).get_state(first_id)["items"][0]["is_flagged"])

    def test_05_navigator_combined_and_practical_states(self):
        attempt_id, _ = self._start()
        question = self._question(0)
        self._save(attempt_id, question, extra={"review_flag": "1"})
        with self.app.app_context():
            service = MockExamService(self.loader)
            state = service.get_state(attempt_id)
            self.assertEqual(state["items"][0]["state_text"], "답변 완료 + 다시 보기")
            practical = state["practical_items"]
            self.assertEqual(len(practical), 2)
            self.assertTrue(practical[0]["is_selected_practical"])
            self.assertTrue(practical[1]["is_unselected_practical"])
            self.assertFalse(practical[1]["is_required"])
            self.assertEqual(state["unanswered_count"], 16)

    def test_06_practical_selection_persists_and_does_not_score_flag(self):
        attempt_id, _ = self._start()
        with self.app.app_context():
            state = MockExamService(self.loader).get_state(attempt_id, 17)
            selected = state["practical_items"][1]
            question = self.loader.get_question_by_id(selected["id"])
        response = self._save(
            attempt_id,
            question,
            index=17,
            extra={"selected_practical_id": selected["id"], "review_flag": "1"},
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            service = MockExamService(self.loader)
            state = service.get_state(attempt_id)
            self.assertEqual(state["selected_practical_id"], selected["id"])
            self.assertTrue(state["items"][17]["is_answered"])
        self.client.post(
            f"/mock-exam/{attempt_id}/submit",
            data={"csrf_token": self.csrf_token},
        )
        with self.app.app_context():
            attempt = MockExamService(self.loader).get_attempt(attempt_id)
            answers = {record.question_id: record for record in attempt.answers}
            self.assertEqual(answers[selected["id"]].achievement_status in {"sufficient", "partial", "incorrect"}, True)
            other = state["practical_items"][0]["id"]
            self.assertEqual(answers[other].achievement_status, "unselected")

    def test_07_review_summary_and_active_anti_cheat(self):
        attempt_id, _ = self._start()
        question = self._question(0)
        self._save(attempt_id, question, destination="review", extra={"review_flag": "1"})
        response = self.client.get(f"/mock-exam/{attempt_id}/review")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("답변 완료", html)
        self.assertIn("미응답", html)
        self.assertIn("다시 보기", html)
        self.assertIn("선택 실무형", html)
        for forbidden in ("모범답안", "채점 루브릭", "AI Helper", "누락 키워드", "구조 평가"):
            self.assertNotIn(forbidden, html)
        with self.app.app_context():
            public = MockExamService._learner_question(question)
            for key in ("answer", "accepted_answers", "model_answer", "rubric", "explanation", "concept_id"):
                self.assertNotIn(key, public)

    def test_08_manual_submit_is_idempotent_and_reuses_grader(self):
        attempt_id, _ = self._start()
        question = self._question(0)
        self._save(attempt_id, question)
        with patch.object(Grader, "grade_full_exam", wraps=Grader.grade_full_exam) as canonical:
            first = self.client.post(
                f"/mock-exam/{attempt_id}/submit",
                data={"csrf_token": self.csrf_token},
                follow_redirects=False,
            )
            second = self.client.post(
                f"/mock-exam/{attempt_id}/submit",
                data={"csrf_token": self.csrf_token},
                follow_redirects=False,
            )
        self.assertEqual(first.status_code, 302)
        self.assertEqual(second.status_code, 302)
        self.assertEqual(canonical.call_count, 1)
        with self.app.app_context():
            attempts = list(db_session.scalars(select(ExamAttempt).where(ExamAttempt.id == attempt_id)).all())
            records = list(db_session.scalars(select(AnswerRecord).where(AnswerRecord.attempt_id == attempt_id)).all())
            self.assertEqual(len(attempts), 1)
            self.assertEqual(len(records), 18)
            self.assertEqual(attempts[0].exam_mode, MockExamService.FINAL_MODE)
            self.assertEqual(len(HistoryService(self.loader).get_attempt_detail(attempt_id)["answers"]), 18)

    def test_09_server_expiry_finalizes_once_and_rejects_mutation(self):
        attempt_id, _ = self._start()
        question = self._question(0)
        expired_now = datetime.now(timezone.utc).replace(tzinfo=None)
        with self.app.app_context():
            attempt = MockExamService(self.loader).get_attempt(attempt_id)
            attempt.started_at = expired_now - timedelta(seconds=MockExamService.DURATION_SECONDS + 1)
            db_session.commit()
        with patch.object(MockExamService, "_now", return_value=expired_now), patch.object(
            Grader, "grade_full_exam", wraps=Grader.grade_full_exam
        ) as canonical:
            response = self._save(attempt_id, question)
            repeated = self.client.post(
                f"/mock-exam/{attempt_id}/submit",
                data={"csrf_token": self.csrf_token},
            )
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"/result/{attempt_id}", response.headers["Location"])
        self.assertEqual(repeated.status_code, 302)
        self.assertEqual(canonical.call_count, 1)
        with self.app.app_context():
            attempt = MockExamService(self.loader).get_attempt(attempt_id)
            record = next(record for record in attempt.answers if record.question_id == question["id"])
            self.assertNotIn("persisted answer", record.user_answer)
            self.assertEqual(attempt.duration_seconds, MockExamService.DURATION_SECONDS)

    def test_10_manual_submit_near_expiry_has_one_terminal_result(self):
        attempt_id, _ = self._start()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        with self.app.app_context():
            attempt = MockExamService(self.loader).get_attempt(attempt_id)
            attempt.started_at = now - timedelta(seconds=MockExamService.DURATION_SECONDS - 1)
            db_session.commit()
        with patch.object(MockExamService, "_now", return_value=now):
            manual = self.client.post(
                f"/mock-exam/{attempt_id}/submit",
                data={"csrf_token": self.csrf_token},
            )
        with patch.object(MockExamService, "_now", return_value=now + timedelta(seconds=2)):
            expiry = self.client.post(
                f"/mock-exam/{attempt_id}/submit",
                data={"csrf_token": self.csrf_token},
            )
        self.assertEqual(manual.status_code, 302)
        self.assertEqual(expiry.status_code, 302)
        with self.app.app_context():
            self.assertEqual(db_session.query(ExamAttempt).filter_by(id=attempt_id).count(), 1)
            self.assertEqual(db_session.query(AnswerRecord).filter_by(attempt_id=attempt_id).count(), 18)

    def test_11_guest_owner_and_result_isolation(self):
        guest_one = self.app.test_client()
        guest_two = self.app.test_client()
        guest_one.get("/mock-exam")
        guest_two.get("/mock-exam")
        with guest_one.session_transaction() as sess:
            token_one = sess[CSRF_SESSION_KEY]
        with guest_two.session_transaction() as sess:
            token_two = sess[CSRF_SESSION_KEY]
        guest_id, _ = self._start(guest_one, token_one)
        self.assertEqual(guest_one.get(f"/mock-exam/{guest_id}").status_code, 200)
        self.assertEqual(guest_two.get(f"/mock-exam/{guest_id}").status_code, 403)
        submit = guest_one.post(
            f"/mock-exam/{guest_id}/submit",
            data={"csrf_token": token_one},
        )
        self.assertEqual(submit.status_code, 302)
        self.assertEqual(guest_one.get(f"/result/{guest_id}").status_code, 200)
        self.assertEqual(guest_two.get(f"/result/{guest_id}").status_code, 403)

        owner_id, _ = self._start()
        self.assertEqual(guest_one.get(f"/mock-exam/{owner_id}").status_code, 403)
        with self.app.app_context():
            self.assertTrue(MockExamService(self.loader).get_attempt(owner_id).is_owner)

    def test_12_csrf_protects_all_state_changes(self):
        other = self.app.test_client()
        other.get("/mock-exam")
        self.assertEqual(other.post("/mock-exam/start", data={}).status_code, 403)
        attempt_id, _ = self._start()
        question = self._question(0)
        base = {"question_id": question["id"], "current_index": "0"}
        self.assertEqual(self.client.post(f"/mock-exam/{attempt_id}/save", data=base).status_code, 403)
        self.assertEqual(self.client.post(f"/mock-exam/{attempt_id}/flag", data=base).status_code, 403)
        self.assertEqual(self.client.post(f"/mock-exam/{attempt_id}/submit", data={}).status_code, 403)

    def test_13_timer_script_recalculates_on_browser_lifecycle(self):
        response = self.client.get("/static/js/mock_exam.js")
        script = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("expiryMs - Date.now()", script)
        self.assertIn('document.addEventListener("visibilitychange", refreshTimer)', script)
        self.assertIn('window.addEventListener("focus", refreshTimer)', script)
        self.assertIn('window.addEventListener("pageshow", refreshTimer)', script)
        self.assertNotIn("remaining--", script)

    def test_14_accessible_timer_flag_and_text_states(self):
        attempt_id, location = self._start()
        html = self.client.get(location).get_data(as_text=True)
        self.assertIn('aria-label="남은 시간"', html)
        self.assertIn('aria-live="off"', html)
        self.assertIn('for="review-flag"', html)
        self.assertIn("상태는 색상뿐 아니라 텍스트와 ★ 기호", html)
        self.assertIn("미응답", html)
        self.assertIn("미선택 · 채점 제외", html)

    def test_15_existing_mode_route_regression(self):
        for path in (
            "/exam", "/practice", "/descriptive-training", "/history",
            "/wrong-notes", "/concepts", "/dashboard",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_16_review_flag_does_not_affect_scoring(self):
        flagged_id, _ = self._start()
        plain_id, _ = self._start()
        question = self._question(0)
        answer = self._answer_data(question, value="same answer")
        self._save(flagged_id, question, extra={**answer, "review_flag": "1"})
        self._save(plain_id, question, extra=answer)
        self.client.post(f"/mock-exam/{flagged_id}/submit", data={"csrf_token": self.csrf_token})
        self.client.post(f"/mock-exam/{plain_id}/submit", data={"csrf_token": self.csrf_token})
        with self.app.app_context():
            service = MockExamService(self.loader)
            self.assertEqual(service.get_attempt(flagged_id).total_score, service.get_attempt(plain_id).total_score)

    def test_17_active_attempt_is_hidden_then_final_result_uses_existing_flow(self):
        attempt_id, _ = self._start()
        with self.app.app_context():
            history = HistoryService(self.loader)
            self.assertNotIn(attempt_id, [attempt.id for attempt in history.get_attempts()])
            self.assertIsNone(history.get_attempt_detail(attempt_id))
        submit = self.client.post(
            f"/mock-exam/{attempt_id}/submit",
            data={"csrf_token": self.csrf_token},
            follow_redirects=False,
        )
        self.assertEqual(submit.status_code, 302)
        result = self.client.get(submit.headers["Location"])
        self.assertEqual(result.status_code, 200)
        self.assertIn("채점 결과", result.get_data(as_text=True))
        with self.app.app_context():
            history = HistoryService(self.loader)
            self.assertIn(attempt_id, [attempt.id for attempt in history.get_attempts()])
            self.assertEqual(len(history.get_attempt_detail(attempt_id)["answers"]), 18)


if __name__ == "__main__":
    unittest.main()
