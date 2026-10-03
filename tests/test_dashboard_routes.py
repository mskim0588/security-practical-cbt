import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestDashboardRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.history_service = HistoryService(DataLoader(self.app.config["DATA_DIR"]))

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_dashboard_empty_state(self):
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("개인 학습현황", html)
        self.assertIn("총 모의고사 응시", html)
        self.assertIn("0", html)
        self.assertIn("5대 영역별 가중 성취도", html)

    def test_dashboard_with_attempts_data(self):
        with self.app.app_context():
            # Add an attempt
            mock_res = {
                "total_score": 75.0,
                "is_passed": True,
                "summary": {"short": {"earned": 30.0}, "descriptive": {"earned": 30.0}, "practical": {"earned": 15.0}},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id=None,
                grading_result=mock_res,
                answers={}
            )

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("75", html)
        self.assertIn("100.0%", html)  # 1 out of 1 passed
        self.assertIn("CON-APP-03", html)  # Q-SHORT-002 failed -> top vulnerable concept!
