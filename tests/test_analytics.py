import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.history_service import HistoryService
from app.services.analytics_service import AnalyticsService
from app.services.data_loader import DataLoader

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestAnalyticsService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(loader)
            self.analytics_service = AnalyticsService(loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_summary_stats_empty_and_populated(self):
        with self.app.app_context():
            # 1. Empty DB
            empty_stats = self.analytics_service.get_summary_stats()
            self.assertEqual(empty_stats["total_attempts"], 0)
            self.assertEqual(empty_stats["pass_rate"], 0.0)
            self.assertEqual(empty_stats["average_score"], 0.0)

            # 2. Add two attempts (70: passed, 50: failed)
            res1 = {"total_score": 70.0, "is_passed": True, "summary": {}, "details": []}
            res2 = {"total_score": 50.0, "is_passed": False, "summary": {}, "details": []}
            self.history_service.save_exam_attempt("standard", None, None, res1, {})
            self.history_service.save_exam_attempt("random", 42, None, res2, {})

            stats = self.analytics_service.get_summary_stats()
            self.assertEqual(stats["total_attempts"], 2)
            self.assertEqual(stats["passed_count"], 1)
            self.assertEqual(stats["pass_rate"], 50.0)
            self.assertEqual(stats["average_score"], 60.0)
            self.assertEqual(stats["highest_score"], 70.0)
            self.assertEqual(stats["latest_score"], 50.0)

    def test_weighted_score_rate_and_categories(self):
        with self.app.app_context():
            # Q-SHORT-008 (시스템 보안, 3점 중 3점 획득)
            # Q-DESC-002 (시스템 보안, 12점 중 6점 획득)
            res = {
                "total_score": 9.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-008", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-002", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

            cat_analytics = self.analytics_service.get_category_analytics()
            self.assertEqual(len(cat_analytics), 5)

            sys_cat = next(c for c in cat_analytics if c["category"] == "시스템 보안")
            self.assertEqual(sys_cat["attempts_count"], 2)
            self.assertEqual(sys_cat["earned_score_sum"], 9.0)
            self.assertEqual(sys_cat["max_score_sum"], 15.0)
            # 9 / 15 * 100 = 60.0%
            self.assertAlmostEqual(sys_cat["score_rate"], 60.0, places=1)
            self.assertEqual(sys_cat["grade"], "주의")

    def test_concept_analytics_and_vulnerability_index(self):
        with self.app.app_context():
            # Q-SHORT-001 has concept_id CON-MGT-01
            # Attempt 1: 0점 (incorrect)
            res1 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}]
            }
            self.history_service.save_exam_attempt("standard", None, None, res1, {})

            concepts = self.analytics_service.get_concept_analytics()
            # Must return all 20 concepts
            self.assertEqual(len(concepts), 20)

            con1 = next(c for c in concepts if c["concept_id"] == "CON-MGT-01")
            self.assertEqual(con1["attempts_count"], 1)
            self.assertEqual(con1["score_rate"], 0.0)
            self.assertEqual(con1["incorrect_count"], 1)
            # VI should be (100 - 0) * (1/1) * log2(1+1) = 100.0
            self.assertAlmostEqual(con1["vulnerability_index"], 100.0, places=1)
            self.assertEqual(con1["grade"], "취약")

            # Other concepts with 0 attempts
            con2 = next(c for c in concepts if c["concept_id"] == "CON-SYS-01")
            self.assertEqual(con2["attempts_count"], 0)
            self.assertEqual(con2["vulnerability_index"], 0.0)
            self.assertEqual(con2["grade"], "미응시")

    def test_top_vulnerable_concepts_ranking(self):
        with self.app.app_context():
            # CON-MGT-01 (Q-SHORT-001) has 1 fail: VI = 100.0
            # CON-NET-01 (Q-SHORT-002) has 2 fails: VI = 100 * 1.0 * log2(3) = 158.5
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}, # CON-MGT-01
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}, # CON-NET-01
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

            # 2nd attempt with Q-SHORT-002 again
            res2 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res2, {})

            top_vuln = self.analytics_service.get_top_vulnerable_concepts(limit=5)
            self.assertEqual(len(top_vuln), 5)
            # CON-APP-03 has 2 failures, so higher VI than CON-MGT-01 (1 failure)
            self.assertEqual(top_vuln[0]["concept_id"], "CON-APP-03")
            self.assertEqual(top_vuln[1]["concept_id"], "CON-MGT-01")
            self.assertGreater(top_vuln[0]["vulnerability_index"], top_vuln[1]["vulnerability_index"])
