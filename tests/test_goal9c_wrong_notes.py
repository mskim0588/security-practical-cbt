import copy
import re
import unittest
from datetime import datetime
from unittest.mock import patch

from sqlalchemy import func, select

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService


class WrongNotesTestConfig(Config):
    TESTING = True
    ADMIN_ACCESS_KEY = "goal9c-test-owner-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class Goal9CWrongNotesTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(WrongNotesTestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            loader = DataLoader(self.app.config["DATA_DIR"])
            self.history = HistoryService(loader)
            self.wrong = WrongAnswerService(loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def owner(self):
        with self.client.session_transaction() as session:
            session["is_admin"] = True

    def save(self, details, answers=None, mode="standard", is_owner=True):
        with self.app.app_context():
            result = {"total_score": sum(item.get("earned_score", 0) for item in details),
                      "is_passed": False, "summary": {}, "details": details}
            return self.history.save_exam_attempt(
                mode, None, None, result, answers or {}, is_owner=is_owner
            ).id

    @staticmethod
    def card(html, question_id):
        match = re.search(
            rf'<article[^>]*data-wrong-question-id="{re.escape(question_id)}"[^>]*>.*?</article>',
            html, re.DOTALL,
        )
        assert match is not None
        return match.group()

    def test_owner_guest_empty_and_historyless_detail(self):
        for path in ("/wrong-notes", "/wrong-notes/Q-SHORT-001"):
            guest = self.client.get(path)
            self.assertEqual(guest.status_code, 302)
            self.assertIn("/admin-login", guest.location)

        self.owner()
        html = self.client.get("/wrong-notes").get_data(as_text=True)
        self.assertIn("현재 미해결된 오답 문항이 없습니다", html)
        self.assertIn('href="/exam"', html)
        self.assertNotIn('data-wrong-question-id="', html)
        detail = self.client.get("/wrong-notes/Q-SHORT-001").get_data(as_text=True)
        self.assertIn("아직 저장된 응시 이력이 없습니다", detail)
        self.assertIn('id="wrong-detail-history"', detail)

    def test_one_summary_card_and_complete_detail_timeline(self):
        first = self.save(
            [{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3}],
            {"Q-SHORT-001": "first submitted answer"},
        )
        latest = self.save(
            [
                {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 1, "max_score": 3,
                 "sub_results": [{"sub_id": "a", "missing_keywords": ["required term"]}]},
                {"question_id": "Q-PRAC-002", "type": "practical", "earned_score": 0,
                 "max_score": 16, "is_selected": False},
            ],
            {"Q-SHORT-001": "latest submitted answer"},
        )
        with self.app.app_context():
            rows = db_session.scalars(select(AnswerRecord).where(
                AnswerRecord.question_id == "Q-SHORT-001"
            )).all()
            for row in rows:
                row.created_at = datetime(2026, 10, 10, 12, 0)
            db_session.commit()

        self.owner()
        html = self.client.get("/wrong-notes").get_data(as_text=True)
        self.assertEqual(html.count('data-wrong-question-id="Q-SHORT-001"'), 1)
        self.assertNotIn('data-wrong-question-id="Q-PRAC-002"', html)
        card = self.card(html, "Q-SHORT-001")
        self.assertIn("오답·부분 감점 2회 / 총 응시 2회", card)
        self.assertIn("최근 부분 감점", card)
        self.assertIn("반복 오답 2회", card)
        self.assertIn("최근 응시 2026-10-10", card)
        self.assertIn("/wrong-notes/Q-SHORT-001", card)
        self.assertNotIn("first submitted answer", html)
        self.assertNotIn("latest submitted answer", html)
        self.assertNotIn("explanation-accordion", html)
        self.assertNotIn("모범 답안:", card)

        detail = self.client.get("/wrong-notes/Q-SHORT-001").get_data(as_text=True)
        self.assertIn("first submitted answer", detail)
        self.assertIn("latest submitted answer", detail)
        self.assertLess(detail.index(f'/history/{latest}'), detail.index(f'/history/{first}'))
        self.assertIn("required term", detail)
        self.assertIn("모범 정답 및 핵심 루브릭", detail)
        self.assertIn("explanation-accordion", detail)
        self.assertIn("btn-ai-helper", detail)
        self.assertIn('data-bookmark-id="Q-SHORT-001"', detail)
        self.assertIn('id="wrong-detail-answer"', detail)
        self.assertIn('id="wrong-detail-history"', detail)

    def test_existing_filters_sort_and_resolution(self):
        self.save([
            {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3},
            {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 4, "max_score": 12},
        ])
        self.save([{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3}])
        self.owner()

        frequent = self.client.get("/wrong-notes?sort=frequency").get_data(as_text=True)
        self.assertLess(frequent.index('data-wrong-question-id="Q-SHORT-001"'),
                        frequent.index('data-wrong-question-id="Q-DESC-001"'))
        self.assertIn('name="sort"', frequent)
        self.assertIn('name="category"', frequent)
        self.assertIn('name="status"', frequent)
        self.assertIn('aria-label="문항 유형 필터"', frequent)
        partial = self.client.get("/wrong-notes?status=partial").get_data(as_text=True)
        self.assertIn('data-wrong-question-id="Q-DESC-001"', partial)
        self.assertNotIn('data-wrong-question-id="Q-SHORT-001"', partial)

        self.save([{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3, "max_score": 3}])
        resolved = self.client.get("/wrong-notes").get_data(as_text=True)
        self.assertNotIn('data-wrong-question-id="Q-SHORT-001"', resolved)
        self.assertEqual(self.client.get("/wrong-notes/Q-SHORT-001").status_code, 200)

    def test_owner_scope_learning_modes_and_bookmark_independence(self):
        self.save([{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3}])
        self.save([{"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0, "max_score": 3}],
                  is_owner=False)
        self.save([{"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 0,
                    "max_score": 12}], mode="mock_exam_active")
        self.owner()
        with self.app.app_context():
            before = (db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                      db_session.scalar(select(func.count()).select_from(AnswerRecord)))
        html = self.client.get("/wrong-notes").get_data(as_text=True)
        detail = self.client.get("/wrong-notes/Q-SHORT-001").get_data(as_text=True)
        self.assertIn('data-wrong-question-id="Q-SHORT-001"', html)
        self.assertNotIn('data-wrong-question-id="Q-SHORT-002"', html)
        self.assertNotIn('data-wrong-question-id="Q-DESC-001"', html)
        self.assertIn('data-bookmark-id="Q-SHORT-001"', detail)
        self.assertNotIn("review_flags", html)
        with self.app.app_context():
            after = (db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                     db_session.scalar(select(func.count()).select_from(AnswerRecord)))
        self.assertEqual(before, after)

    def test_limited_metadata_and_private_source_are_not_exposed(self):
        self.save([{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3}])
        self.owner()
        with self.app.app_context():
            row = copy.deepcopy(self.wrong.get_wrong_questions()[0])
            detail = copy.deepcopy(self.wrong.get_wrong_question_detail("Q-SHORT-001"))
        row.update(question_text="", concept_id=None, concept_name=None,
                   latest_date=None, source_info=r"C:\private\exam.pdf")
        detail["question"]["source_info"] = r"C:\private\exam.pdf"
        with patch("app.routes.wrong_routes.get_wrong_service") as service_factory:
            service = service_factory.return_value
            service.get_wrong_questions.return_value = [row]
            service.get_wrong_question_detail.return_value = detail
            html = self.client.get("/wrong-notes").get_data(as_text=True)
            detail_html = self.client.get("/wrong-notes/Q-SHORT-001").get_data(as_text=True)
        card = self.card(html, "Q-SHORT-001")
        self.assertIn("문항 Q-SHORT-001", card)
        self.assertNotIn("최근 응시", card)
        self.assertNotIn("C:\\private\\exam.pdf", html)
        self.assertNotIn("C:\\private\\exam.pdf", detail_html)
        self.assertNotIn("{'", card)


if __name__ == "__main__":
    unittest.main()
