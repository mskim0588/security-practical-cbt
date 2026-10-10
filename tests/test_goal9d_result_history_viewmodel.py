import unittest
from datetime import datetime

from sqlalchemy import event, select

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.attempt_view_model import map_attempt_summary
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService


class Goal9DConfig(Config):
    TESTING = True
    ADMIN_ACCESS_KEY = "goal9d-local-owner-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class Goal9DResultHistoryTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Goal9DConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.history = HistoryService(DataLoader(self.app.config["DATA_DIR"]))

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def owner(self):
        with self.client.session_transaction() as session:
            session["is_admin"] = True

    def save(self, score, mode="standard", owner=True, partial=False):
        selected = "Q-PRAC-001"
        practical = 16.0 if score >= 16 else 0.0
        short = score - practical
        details = [
            {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 1 if partial else 0,
             "max_score": 3, "sub_results": [{"missing_keywords": ["review"]}] if partial else []},
            {"question_id": selected, "type": "practical", "earned_score": practical,
             "max_score": 16, "is_selected": True},
            {"question_id": "Q-PRAC-002", "type": "practical", "earned_score": 0,
             "max_score": 16, "is_selected": False},
        ]
        grading = {
            "total_score": score, "is_passed": score >= 60,
            "summary": {"short": {"earned": short}, "descriptive": {"earned": 0},
                        "practical": {"earned": practical}},
            "details": details,
        }
        with self.app.app_context():
            attempt = self.history.save_exam_attempt(
                mode, None, selected, grading,
                {"Q-SHORT-001": "long submitted answer " * 20}, is_owner=owner,
            )
            return attempt.id

    def test_mapper_copies_canonical_values_and_never_exposes_answers(self):
        attempt_id = self.save(64.5, partial=True)
        with self.app.app_context(), self.app.test_request_context():
            attempt = self.history.get_attempt_by_id(attempt_id)
            detail = self.history.get_attempt_detail(attempt_id)
            from_model = map_attempt_summary(attempt)
            from_detail = map_attempt_summary(detail)
            self.assertEqual(from_model, from_detail)
            self.assertEqual(from_model["total_score"], 64.5)
            self.assertEqual(from_model["max_score"], 100)
            self.assertEqual(from_model["practical_score"], 16)
            self.assertEqual(from_model["selected_practical_id"], "Q-PRAC-001")
            self.assertEqual(from_model["history_url"], f"/history/{attempt_id}")
            self.assertEqual(from_model["result_url"], f"/result/{attempt_id}")
            self.assertEqual(from_model["created_at_text"], attempt.created_at.strftime("%Y-%m-%d %H:%M"))
            self.assertFalse(set(from_model) & {"answers", "model_answer", "rubric", "source_info"})

    def test_missing_optional_and_ungraded_values_do_not_become_zero(self):
        with self.app.test_request_context():
            active = map_attempt_summary({"id": 11, "exam_mode": "mock_exam_active", "total_score": 0,
                                          "submitted_at": None, "is_owner": True})
            ungraded = map_attempt_summary({"id": 12, "exam_mode": "standard", "total_score": None,
                                            "submitted_at": "2026-10-10T09:00:00", "is_owner": True})
            self.assertEqual(active["status_label"], "진행 중")
            self.assertEqual(ungraded["status_label"], "채점 전")
            for view in (active, ungraded):
                self.assertIsNone(view["total_score"])
                self.assertIsNone(view["is_passed"])
                self.assertIsNone(view["result_url"])
                self.assertEqual(view["created_at_text"], "-")

    def test_finalized_pass_fail_partial_mock_and_history_consistency(self):
        passing = self.save(64.5, partial=True)
        failing = self.save(42)
        mock = self.save(72, mode="mock_exam")
        self.owner()
        listing = self.client.get("/history").get_data(as_text=True)
        self.assertLess(listing.index(f"/history/{mock}"), listing.index(f"/history/{failing}"))
        self.assertLess(listing.index(f"/history/{failing}"), listing.index(f"/history/{passing}"))
        for attempt_id, score, label in ((passing, "64.5", "합격"),
                                         (failing, "42", "불합격"),
                                         (mock, "72", "합격")):
            result = self.client.get(f"/result/{attempt_id}")
            history = self.client.get(f"/history/{attempt_id}")
            self.assertEqual((result.status_code, history.status_code), (200, 200))
            result_html = result.get_data(as_text=True)
            history_html = history.get_data(as_text=True)
            self.assertIn(score, result_html)
            self.assertIn(score, history_html)
            self.assertIn(label, result_html)
            self.assertIn(label, history_html)
            self.assertIn(f"/history/{attempt_id}", result_html)
            self.assertIn("/ 100점", result_html)
            self.assertIn("/ 100점", history_html)
            self.assertEqual(result.headers["X-Robots-Tag"], "noindex, nofollow")
        self.assertIn("mock_exam", listing)
        self.assertIn("선택: Q-PRAC-001", self.client.get(f"/history/{passing}").get_data(as_text=True))
        self.assertIn("미선택 (채점 제외)", self.client.get(f"/history/{passing}").get_data(as_text=True))

    def test_empty_and_active_history(self):
        self.owner()
        self.assertIn("아직 저장된 응시 이력이 없습니다", self.client.get("/history").get_data(as_text=True))
        with self.app.app_context():
            active = ExamAttempt(exam_mode="mock_exam_active", is_owner=True, created_at=datetime(2026, 10, 10, 8))
            db_session.add(active)
            db_session.commit()
            active_id = active.id
        listing = self.client.get("/history").get_data(as_text=True)
        self.assertNotIn(f"/history/{active_id}", listing)
        self.assertEqual(self.client.get(f"/result/{active_id}").status_code, 404)

    def test_guest_result_and_owner_idor_boundaries(self):
        guest_id = self.save(64, owner=False)
        owner_id = self.save(75, owner=True)
        self.assertEqual(self.client.get("/history").status_code, 302)
        self.assertIn("/admin-login", self.client.get("/history").location)
        self.assertEqual(self.client.get(f"/result/{guest_id}").status_code, 403)
        self.assertEqual(self.client.get(f"/result/{owner_id}").status_code, 403)
        with self.client.session_transaction() as session:
            session["submitted_attempts"] = [guest_id, owner_id]
        self.assertEqual(self.client.get(f"/result/{guest_id}").status_code, 200)
        self.assertEqual(self.client.get(f"/result/{owner_id}").status_code, 403)
        self.owner()
        self.assertEqual(self.client.get(f"/history/{guest_id}").status_code, 404)
        self.assertEqual(self.client.get(f"/history/{owner_id}").status_code, 200)
        self.assertEqual(self.client.get("/result/999999").status_code, 404)

    def test_rendering_read_only_private_source_and_query_count(self):
        first = self.save(64.5, partial=True)
        self.save(64.5, mode="mock_exam")
        self.owner()
        with self.app.app_context():
            before = [(a.id, a.total_score, a.is_passed) for a in db_session.scalars(select(ExamAttempt).order_by(ExamAttempt.id))]
            answer_count = len(db_session.scalars(select(AnswerRecord)).all())
            from app.models import database
            selects = []
            def count_select(_conn, _cursor, statement, _params, _ctx, _many):
                if statement.lstrip().upper().startswith("SELECT"):
                    selects.append(statement)
            event.listen(database.engine, "before_cursor_execute", count_select)
            try:
                listing = self.client.get("/history")
            finally:
                event.remove(database.engine, "before_cursor_execute", count_select)
            self.assertLessEqual(len(selects), 3)
            result = self.client.get(f"/result/{first}")
            detail = self.client.get(f"/history/{first}")
            after = [(a.id, a.total_score, a.is_passed) for a in db_session.scalars(select(ExamAttempt).order_by(ExamAttempt.id))]
            self.assertEqual(before, after)
            self.assertEqual(answer_count, len(db_session.scalars(select(AnswerRecord)).all()))
        for response in (listing, result, detail):
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("source_type", html)
            self.assertNotIn("{'id': 'SRC-", html)
        self.assertIn("long submitted answer", result.get_data(as_text=True))
        self.assertIn("long submitted answer", detail.get_data(as_text=True))
        self.assertIn("btn-ai-helper", result.get_data(as_text=True))
        self.assertIn("btn-ai-helper", detail.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
