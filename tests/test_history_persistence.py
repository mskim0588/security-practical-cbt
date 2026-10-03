import unittest
import json
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db, db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.history_service import HistoryService
from app.services.data_loader import DataLoader

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestHistoryPersistence(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.service = HistoryService(DataLoader(self.app.config["DATA_DIR"]))

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_save_exam_attempt_integrity(self):
        with self.app.app_context():
            # Mock grading result matching Grader.grade_full_exam format
            mock_grading_result = {
                "total_score": 75.5,
                "max_total_score": 100.0,
                "is_passed": True,
                "summary": {
                    "short": {"earned": 30.0, "max": 36.0, "percentage": 83.3},
                    "descriptive": {"earned": 33.5, "max": 48.0, "percentage": 69.8},
                    "practical": {"earned": 12.0, "max": 16.0, "percentage": 75.0, "selected_id": "Q-PRAC-001"}
                },
                "graded_count": 17,
                "details": [
                    {
                        "question_id": "Q-SHORT-001",
                        "type": "short",
                        "earned_score": 3.0,
                        "max_score": 3.0,
                        "is_correct": True
                    },
                    {
                        "question_id": "Q-SHORT-002",
                        "type": "short",
                        "earned_score": 0.0,
                        "max_score": 3.0,
                        "is_correct": False
                    },
                    {
                        "question_id": "Q-DESC-001",
                        "type": "descriptive",
                        "earned_score": 8.0,
                        "max_score": 12.0,
                        "sub_results": [{"sub_id": "1", "prompt": "p1", "earned_score": 8.0, "max_score": 12.0}]
                    },
                    {
                        "question_id": "Q-PRAC-001",
                        "type": "practical",
                        "is_selected": True,
                        "earned_score": 12.0,
                        "max_score": 16.0,
                        "sub_results": [{"sub_id": "1", "prompt": "p1", "earned_score": 12.0, "max_score": 16.0}]
                    },
                    {
                        "question_id": "Q-PRAC-002",
                        "type": "practical",
                        "is_selected": False,
                        "earned_score": 0.0,
                        "max_score": 16.0,
                        "sub_results": []
                    }
                ]
            }

            user_answers = {
                "Q-SHORT-001": "access.log",
                "Q-SHORT-002": "wrong answer",
                "Q-DESC-001": {"1": "설명 내용"},
                "Q-PRAC-001": {"1": "iptables -A INPUT"},
                "Q-PRAC-002": {}
            }

            attempt = self.service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id="Q-PRAC-001",
                grading_result=mock_grading_result,
                answers=user_answers
            )

            self.assertIsNotNone(attempt.id)
            self.assertEqual(attempt.total_score, 75.5)
            self.assertTrue(attempt.is_passed)
            self.assertEqual(len(attempt.answers), 5)

            # Check individual answer records
            ans_map = {a.question_id: a for a in attempt.answers}
            self.assertEqual(ans_map["Q-SHORT-001"].achievement_status, "sufficient")
            self.assertTrue(ans_map["Q-SHORT-001"].is_correct)

            self.assertEqual(ans_map["Q-SHORT-002"].achievement_status, "incorrect")
            self.assertFalse(ans_map["Q-SHORT-002"].is_correct)

            self.assertEqual(ans_map["Q-DESC-001"].achievement_status, "partial")
            self.assertFalse(ans_map["Q-DESC-001"].is_correct)

            self.assertEqual(ans_map["Q-PRAC-001"].achievement_status, "partial")
            self.assertEqual(ans_map["Q-PRAC-002"].achievement_status, "unselected")

    def test_get_attempt_detail_enrichment(self):
        with self.app.app_context():
            mock_grading_result = {
                "total_score": 3.0,
                "summary": {"short": {"earned": 3.0}, "descriptive": {"earned": 0.0}, "practical": {"earned": 0.0}},
                "is_passed": False,
                "details": [
                    {
                        "question_id": "Q-SHORT-001",
                        "type": "short",
                        "earned_score": 3.0,
                        "max_score": 3.0
                    }
                ]
            }
            attempt = self.service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id=None,
                grading_result=mock_grading_result,
                answers={"Q-SHORT-001": "Apache access.log"}
            )

            detail = self.service.get_attempt_detail(attempt.id)
            self.assertIsNotNone(detail)
            self.assertEqual(detail["id"], attempt.id)
            self.assertEqual(len(detail["answers"]), 1)
            
            first_ans = detail["answers"][0]
            self.assertEqual(first_ans["question_id"], "Q-SHORT-001")
            # Enriched metadata from DataLoader
            self.assertTrue(len(first_ans["question_text"]) > 0)
            self.assertIsNotNone(first_ans["source_info"])
            self.assertIsNotNone(first_ans["category"])

    def test_history_routes(self):
        # 1. Empty history
        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("모의고사 응시 이력", resp.get_data(as_text=True))
        self.assertIn("아직 저장된 응시 이력이 없습니다", resp.get_data(as_text=True))

        # 2. Submit exam via POST /submit
        form_data = {
            "exam_mode": "standard",
            "question_ids": "Q-SHORT-001,Q-SHORT-002,Q-SHORT-003,Q-SHORT-004,Q-SHORT-005,Q-SHORT-006,Q-SHORT-007,Q-SHORT-008,Q-SHORT-009,Q-SHORT-010,Q-SHORT-011,Q-SHORT-012,Q-DESC-001,Q-DESC-002,Q-DESC-003,Q-DESC-004,Q-PRAC-001,Q-PRAC-002",
            "selected_practical_id": "Q-PRAC-001",
            "q_Q-SHORT-001": "access.log"
        }
        submit_resp = self.client.post("/submit", data=form_data, follow_redirects=True)
        self.assertEqual(submit_resp.status_code, 200)
        html = submit_resp.get_data(as_text=True)
        self.assertIn("성공적으로 저장되었습니다", html)
        self.assertIn("/history/1", html)

        # 3. Check history list has 1 item
        resp2 = self.client.get("/history")
        self.assertEqual(resp2.status_code, 200)
        self.assertIn("#1", resp2.get_data(as_text=True))

        # 4. View history detail
        detail_resp = self.client.get("/history/1")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn("제1회차 모의고사 복기 리포트", detail_resp.get_data(as_text=True))
        self.assertIn("Q-SHORT-001", detail_resp.get_data(as_text=True))

        # 5. Non-existent attempt returns 404
        resp404 = self.client.get("/history/9999")
        self.assertEqual(resp404.status_code, 404)

        # 6. Delete attempt
        del_resp = self.client.post("/history/1/delete", follow_redirects=True)
        self.assertEqual(del_resp.status_code, 200)
        self.assertIn("아직 저장된 응시 이력이 없습니다", del_resp.get_data(as_text=True))

    def test_multiple_attempts_pagination(self):
        with self.app.app_context():
            mock_res = {
                "total_score": 50.0,
                "summary": {"short": {"earned": 20.0}, "descriptive": {"earned": 20.0}, "practical": {"earned": 10.0}},
                "is_passed": False,
                "details": []
            }
            # Create 20 attempts
            for i in range(20):
                self.service.save_exam_attempt(
                    exam_mode="random",
                    seed=i,
                    selected_practical_id=None,
                    grading_result=mock_res,
                    answers={}
                )

            self.assertEqual(self.service.get_attempt_count(), 20)
            p1_attempts = self.service.get_attempts(limit=15, offset=0)
            self.assertEqual(len(p1_attempts), 15)

            p2_attempts = self.service.get_attempts(limit=15, offset=15)
            self.assertEqual(len(p2_attempts), 5)

        # Test web route pagination
        page1_resp = self.client.get("/history?page=1")
        self.assertEqual(page1_resp.status_code, 200)
        page2_resp = self.client.get("/history?page=2")
        self.assertEqual(page2_resp.status_code, 200)

    def test_cascade_delete_integrity(self):
        with self.app.app_context():
            mock_res = {
                "total_score": 60.0,
                "summary": {"short": {"earned": 30.0}, "descriptive": {"earned": 20.0}, "practical": {"earned": 10.0}},
                "is_passed": True,
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 12.0, "max_score": 12.0}
                ]
            }
            att = self.service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id=None,
                grading_result=mock_res,
                answers={}
            )
            att_id = att.id

            # Verify AnswerRecords exist
            records = db_session.query(AnswerRecord).filter_by(attempt_id=att_id).all()
            self.assertEqual(len(records), 2)

            # Delete attempt
            success = self.service.delete_attempt(att_id)
            self.assertTrue(success)

            # Verify AnswerRecords are cascade deleted
            records_after = db_session.query(AnswerRecord).filter_by(attempt_id=att_id).all()
            self.assertEqual(len(records_after), 0)
