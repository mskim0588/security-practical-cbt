import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.analytics_service import AnalyticsService
from app.services.wrong_answer_service import WrongAnswerService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestGoal4EDashboard(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(self.loader)
            self.analytics_service = AnalyticsService(self.loader)
            self.wrong_service = WrongAnswerService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_01_dashboard_status_code_200(self):
        """1. GET /dashboard returns 200 OK."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)

    def test_02_empty_dashboard_cta_and_onboarding(self):
        """2. Empty dashboard renders friendly onboarding recommendation and CTAs."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("개인 학습현황", html)
        self.assertIn("총 모의고사 응시", html)
        self.assertIn("0", html)
        self.assertIn("첫 모의고사로 나의 보안 실력을 진단해보세요", html)  # Onboarding recommendation
        self.assertIn("/exam?mode=standard", html)  # Primary CTA
        self.assertIn("/concepts", html)  # Secondary CTA
        self.assertIn("아직 응시 기록이 없습니다", html)  # Empty trend message

    def test_03_kpi_4_cards_rendering(self):
        """3. All 4 core KPI metric cards are rendered with proper values and links."""
        with self.app.app_context():
            mock_res = {
                "total_score": 70.0,
                "is_passed": True,
                "summary": {"short": {"earned": 20.0}, "descriptive": {"earned": 30.0}, "practical": {"earned": 20.0}},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, mock_res, {"Q-SHORT-001": "ans", "Q-SHORT-002": "bad"})

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("총 모의고사 응시", html)
        self.assertIn("1", html)
        self.assertIn("평균 획득 점수", html)
        self.assertIn("70", html)
        self.assertIn("합격권 달성률", html)
        self.assertIn("100.0%", html)
        self.assertIn("미해결 오답 문항", html)
        self.assertIn("/wrong-notes", html)
        self.assertIn("/history", html)

    def test_04_five_categories_rendering(self):
        """4. Standard 5 categories are all rendered with weighted scores and counts."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        expected_cats = [
            "시스템 보안",
            "네트워크 보안",
            "애플리케이션 보안",
            "정보보안 일반 및 암호학",
            "정보보호 관리 및 법규"
        ]
        for cat in expected_cats:
            self.assertIn(cat, html)

    def test_05_achievement_status_text_and_symbols_not_color_alone(self):
        """5. Achievement status uses text + symbols, not color alone."""
        with self.app.app_context():
            # Add attempts: Q-SHORT-008 (시스템 보안 3/3 -> 100% -> 안전)
            res = {
                "total_score": 100.0,
                "is_passed": True,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-008", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Status text + symbols
        self.assertIn("✓ 안전", html)
        self.assertIn("- 미응시", html)
        # Accessible progressbar
        self.assertIn('role="progressbar"', html)
        self.assertIn('aria-valuenow=', html)

    def test_06_top_5_concept_clinic_rendering(self):
        """6. Top 5 vulnerable concepts are rendered in clinic section."""
        with self.app.app_context():
            # Failure on Q-SHORT-001 (CON-MGT-01)
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("취약 Concept 집중 클리닉 Top 5", html)
        self.assertIn("CON-MGT-01", html)
        self.assertIn("위험관리 및 위험평가 방법론", html)
        self.assertIn("VI", html)
        self.assertIn("개념 공부하기 &rarr;", html)

    def test_07_concept_detail_link_navigation(self):
        """7. Concept links point to /concepts/<concept_id> and resolve with 200 OK."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("/concepts/", html)
        # Test following a concept link from dashboard
        concept_resp = self.client.get("/concepts/CON-MGT-01")
        self.assertEqual(concept_resp.status_code, 200)

    def test_08_adaptive_exam_cta(self):
        """8. Adaptive exam CTA (/exam?mode=adaptive) is available and functional."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("/exam?mode=adaptive", html)
        adap_resp = self.client.get("/exam?mode=adaptive")
        self.assertEqual(adap_resp.status_code, 200)

    def test_09_wrong_review_cta(self):
        """9. Wrong review CTA is highlighted when unresolved wrong answers exist."""
        with self.app.app_context():
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {"Q-SHORT-001": "wrong"})

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("미해결 오답 문항 1개를 먼저 복습하세요", html)
        self.assertIn("/exam?mode=wrong_review", html)
        wrong_exam_resp = self.client.get("/exam?mode=wrong_review")
        self.assertEqual(wrong_exam_resp.status_code, 200)

    def test_10_recent_history_links_and_delta(self):
        """10. Recent attempts display history link and score delta between consecutive exams."""
        with self.app.app_context():
            # Attempt 1: 50 pts
            res1 = {"total_score": 50.0, "is_passed": False, "summary": {}, "details": []}
            att1 = self.history_service.save_exam_attempt("standard", None, None, res1, {})
            att1_id = att1.id

            # Attempt 2: 70 pts (+20 delta)
            res2 = {"total_score": 70.0, "is_passed": True, "summary": {}, "details": []}
            att2 = self.history_service.save_exam_attempt("random", None, None, res2, {})
            att2_id = att2.id

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Recent history link
        self.assertIn(f"/history/{att1_id}", html)
        self.assertIn(f"/history/{att2_id}", html)

        # Following history link returns 200
        hist_resp = self.client.get(f"/history/{att2_id}")
        self.assertEqual(hist_resp.status_code, 200)

        # Delta indicator: +20점
        self.assertIn("+20점", html)

    def test_11_learning_recommendation_states(self):
        """11. Learning recommendations trigger correctly across all 4 deterministic states."""
        with self.app.app_context():
            # State A: 0 attempts
            s_empty = self.analytics_service.get_summary_stats()
            rec_a = from_dashboard_route_recommendation(s_empty, 0, [])
            self.assertEqual(rec_a["type"], "onboarding")
            self.assertIn("/exam?mode=standard", rec_a["primary_btn_url"])

            # State B: wrong_count > 0
            rec_b = from_dashboard_route_recommendation({"total_attempts": 1}, 3, [])
            self.assertEqual(rec_b["type"], "wrong_review")
            self.assertIn("/exam?mode=wrong_review", rec_b["primary_btn_url"])

            # State C: wrong_count == 0, vulnerable concept VI > 0
            top_vuln = [{"name": "방화벽", "concept_id": "CON-NET-01", "vulnerability_index": 120.0}]
            rec_c = from_dashboard_route_recommendation({"total_attempts": 2, "pass_rate": 50.0}, 0, top_vuln)
            self.assertEqual(rec_c["type"], "concept_clinic")
            self.assertIn("/exam?mode=adaptive", rec_c["primary_btn_url"])

            # State D: wrong_count == 0, pass_rate >= 60, no high VI
            rec_d = from_dashboard_route_recommendation({"total_attempts": 5, "pass_rate": 80.0}, 0, [])
            self.assertEqual(rec_d["type"], "practice")
            self.assertIn("/exam?mode=random", rec_d["primary_btn_url"])

    def test_12_analytics_values_consistency(self):
        """12. Values rendered on /dashboard are mathematically consistent with AnalyticsService."""
        with self.app.app_context():
            res = {
                "total_score": 64.0,
                "is_passed": True,
                "summary": {"short": {"earned": 24.0}, "descriptive": {"earned": 24.0}, "practical": {"earned": 16.0}},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

            summary = self.analytics_service.get_summary_stats()
            self.assertEqual(summary["total_attempts"], 1)
            self.assertEqual(summary["average_score"], 64.0)
            self.assertEqual(summary["highest_score"], 64.0)

            cats = self.analytics_service.get_category_analytics()
            self.assertEqual(len(cats), 5)

        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("64", html)

def from_dashboard_route_recommendation(summary, wrong_count, top_vulnerable):
    from app.routes.dashboard_routes import get_learning_recommendation
    return get_learning_recommendation(summary, wrong_count, top_vulnerable)

if __name__ == "__main__":
    unittest.main()
