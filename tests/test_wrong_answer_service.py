import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db, db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.data_loader import DataLoader

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestWrongAnswerService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(loader)
            self.wrong_service = WrongAnswerService(loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_detect_incorrect_and_partial_and_exclude_unselected(self):
        with self.app.app_context():
            mock_grading = {
                "total_score": 15.0,
                "is_passed": False,
                "summary": {"short": {"earned": 3.0}, "descriptive": {"earned": 6.0}, "practical": {"earned": 6.0}},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0, "is_correct": True},
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0, "is_correct": False},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0},
                    {"question_id": "Q-PRAC-001", "type": "practical", "is_selected": True, "earned_score": 6.0, "max_score": 16.0},
                    {"question_id": "Q-PRAC-002", "type": "practical", "is_selected": False, "earned_score": 0.0, "max_score": 16.0}
                ]
            }
            self.history_service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id="Q-PRAC-001",
                grading_result=mock_grading,
                answers={"Q-SHORT-001": "correct", "Q-SHORT-002": "wrong", "Q-DESC-001": "partial", "Q-PRAC-001": "partial"}
            )

            wrong_qs = self.wrong_service.get_wrong_questions()
            wrong_ids = [q["question_id"] for q in wrong_qs]

            # Q-SHORT-001 (정답) -> 제외
            self.assertNotIn("Q-SHORT-001", wrong_ids)
            # Q-PRAC-002 (미선택 실무형) -> 제외
            self.assertNotIn("Q-PRAC-002", wrong_ids)

            # Q-SHORT-002 (오답) -> 포함
            self.assertIn("Q-SHORT-002", wrong_ids)
            # Q-DESC-001 (부분점수) -> 포함
            self.assertIn("Q-DESC-001", wrong_ids)
            # Q-PRAC-001 (부분점수 실무형) -> 포함
            self.assertIn("Q-PRAC-001", wrong_ids)

            self.assertEqual(len(wrong_qs), 3)

    def test_state_transition_resolution(self):
        with self.app.app_context():
            # Attempt 1: Failed Q-SHORT-002
            res1 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res1, {"Q-SHORT-002": "bad"})

            self.assertEqual(self.wrong_service.get_wrong_question_count(), 1)
            wrong_list = self.wrong_service.get_wrong_questions()
            self.assertEqual(wrong_list[0]["question_id"], "Q-SHORT-002")

            # Attempt 2: Succeeded Q-SHORT-002 (earned 3.0)
            res2 = {
                "total_score": 3.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res2, {"Q-SHORT-002": "good"})

            # Now active wrong question count must become 0!
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 0)

            # But question detail history still records 2 attempts
            detail = self.wrong_service.get_wrong_question_detail("Q-SHORT-002")
            self.assertEqual(detail["total_attempts"], 2)
            self.assertEqual(detail["latest_status"], "sufficient")
            self.assertEqual(detail["sufficient_count"], 1)
            self.assertEqual(detail["incorrect_count"], 1)

    def test_filters_and_sorting(self):
        with self.app.app_context():
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 4.0, "max_score": 12.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

            # Filter by type: short
            short_only = self.wrong_service.get_wrong_questions(type_filter="short")
            self.assertEqual(len(short_only), 1)
            self.assertEqual(short_only[0]["question_id"], "Q-SHORT-001")

            # Filter by type: descriptive
            desc_only = self.wrong_service.get_wrong_questions(type_filter="descriptive")
            self.assertEqual(len(desc_only), 1)
            self.assertEqual(desc_only[0]["question_id"], "Q-DESC-001")

            # Filter by status: incorrect
            inc_only = self.wrong_service.get_wrong_questions(status_filter="incorrect")
            self.assertEqual(len(inc_only), 1)
            self.assertEqual(inc_only[0]["question_id"], "Q-SHORT-001")

            # Filter by status: partial
            part_only = self.wrong_service.get_wrong_questions(status_filter="partial")
            self.assertEqual(len(part_only), 1)
            self.assertEqual(part_only[0]["question_id"], "Q-DESC-001")

    def test_wrong_routes(self):
        with self.app.app_context():
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        # 1. GET /wrong-notes
        resp = self.client.get("/wrong-notes")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("오답노트 & 취약 문항 복습", resp.get_data(as_text=True))
        self.assertIn("Q-SHORT-001", resp.get_data(as_text=True))

        # 2. GET /wrong-notes/Q-SHORT-001
        detail_resp = self.client.get("/wrong-notes/Q-SHORT-001")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn("문항 심층 복기", detail_resp.get_data(as_text=True))
        self.assertIn("응시 이력 타임라인", detail_resp.get_data(as_text=True))

        # 3. GET /wrong-notes/NON-EXISTENT
        resp404 = self.client.get("/wrong-notes/NON-EXISTENT")
        self.assertEqual(resp404.status_code, 404)
