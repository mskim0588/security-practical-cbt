import re
import unittest

from sqlalchemy import func, select

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.routes.dashboard_routes import build_dashboard_presentation, get_learning_recommendation
from app.services.analytics_service import AnalyticsService
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService


class DashboardTestConfig(Config):
    TESTING = True
    ADMIN_ACCESS_KEY = "goal9b-test-owner-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class Goal9BDashboardTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(DashboardTestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            loader = DataLoader(self.app.config["DATA_DIR"])
            self.history = HistoryService(loader)
            self.analytics = AnalyticsService(loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def owner(self):
        with self.client.session_transaction() as session:
            session["is_admin"] = True

    def save(self, score, mode="standard", details=None, is_owner=True):
        with self.app.app_context():
            return self.history.save_exam_attempt(
                mode, None, None,
                {"total_score": score, "is_passed": score >= 60,
                 "summary": {}, "details": details or []},
                {}, is_owner=is_owner,
            ).id

    @staticmethod
    def summary_section(html, section_id):
        match = re.search(
            rf'<section[^>]*aria-labelledby="{section_id}"[^>]*>(.*?)</section>',
            html, re.DOTALL,
        )
        assert match is not None
        return match.group(1)

    def test_owner_auth_and_empty_summary(self):
        guest = self.client.get("/dashboard")
        self.assertEqual(guest.status_code, 302)
        self.assertIn("/admin-login", guest.location)
        self.owner()
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("내 학습", html)
        self.assertIn("다음 추천 학습", html)
        self.assertIn("/exam?mode=standard", self.summary_section(html, "dashboard-next-title"))
        weak = self.summary_section(html, "dashboard-weak-title")
        self.assertIn("아직 풀이 기록에 기반한", weak)
        self.assertNotIn("<li>", weak)
        recent = self.summary_section(html, "dashboard-recent-title")
        self.assertIn("아직 완료한 시험 기록이 없습니다.", recent)
        self.assertNotIn("0점", recent)
        self.assertIn("/exam?mode=standard", recent)
        self.assertLess(html.index("다음 추천 학습"), html.index("상세 학습 분석"))
        self.assertLess(html.index("취약 개념 TOP 3"), html.index("상세 학습 분석"))
        for detail in ("총 모의고사 응시", "평균 획득 점수", "합격권 달성률",
                       "미해결 오답 문항", "5대 영역별 가중 성취도",
                       "취약 Concept 집중 클리닉 Top 5"):
            self.assertIn(detail, html)

    def test_recent_score_uses_owner_scored_exams_and_detail_link(self):
        first = self.save(55, details=[{"question_id": "Q-SHORT-001", "type": "short",
                                        "earned_score": 0, "max_score": 3}])
        latest = self.save(75, mode="random")
        self.save(98, mode="practice")
        self.save(97, mode="descriptive_training")
        self.save(96, mode="mock_exam_active")
        self.save(99, is_owner=False)
        self.owner()
        with self.app.app_context():
            before = (
                db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                db_session.scalar(select(func.count()).select_from(AnswerRecord)),
            )
        html = self.client.get("/dashboard").get_data(as_text=True)
        recent = self.summary_section(html, "dashboard-recent-title")
        self.assertIn("75", recent)
        self.assertIn("/ 100점", recent)
        self.assertIn(f'/history/{latest}', recent)
        self.assertNotIn("99", recent)
        self.assertNotIn("98", recent)
        self.assertNotIn("97", recent)
        self.assertNotIn("96", recent)
        self.assertEqual(self.client.get(f"/history/{latest}").status_code, 200)
        self.assertEqual(self.client.get(f"/history/{first}").status_code, 200)
        with self.app.app_context():
            after = (
                db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                db_session.scalar(select(func.count()).select_from(AnswerRecord)),
            )
        self.assertEqual(before, after)

    def test_weak_summary_uses_canonical_vi_and_excludes_unattempted(self):
        self.save(40, details=[
            {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0, "max_score": 3},
            {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0, "max_score": 3},
        ])
        self.owner()
        with self.app.app_context():
            canonical = self.analytics.get_top_vulnerable_concepts(limit=5)
        expected = [item for item in canonical if item["attempts_count"] > 0 and item["vulnerability_index"] > 0][:3]
        html = self.client.get("/dashboard").get_data(as_text=True)
        weak = self.summary_section(html, "dashboard-weak-title")
        self.assertEqual(weak.count("<li>"), len(expected))
        for item in expected:
            self.assertIn(f'/concepts/{item["concept_id"]}', weak)
            self.assertEqual(self.client.get(f'/concepts/{item["concept_id"]}').status_code, 200)
        self.assertIn("풀이 1건", weak)
        self.assertIn("VI", weak)
        self.assertIn("득점률", weak)

    def test_partial_data_ties_and_unselected_practical(self):
        sample = [
            {"concept_id": "CON-B", "name": "B", "attempts_count": 1,
             "vulnerability_index": 12, "score_rate": 0},
            {"concept_id": "CON-A", "name": "A", "attempts_count": 1,
             "vulnerability_index": 12, "score_rate": 0},
            {"concept_id": "CON-C", "name": "C", "attempts_count": 0,
             "vulnerability_index": 0, "score_rate": 0},
            {"concept_id": "CON-D", "name": "D", "attempts_count": None,
             "vulnerability_index": 20, "score_rate": 0},
            {"concept_id": "CON-E", "name": "E", "attempts_count": 2,
             "vulnerability_index": 5, "score_rate": 20},
            {"concept_id": "CON-F", "name": "F", "attempts_count": 1,
             "vulnerability_index": 2, "score_rate": 30},
        ]
        self.assertEqual(
            [item["concept_id"] for item in build_dashboard_presentation(sample, [])["weak_concepts"]],
            ["CON-A", "CON-B", "CON-E"],
        )
        self.assertIsNone(build_dashboard_presentation([], [])['recent_score'])
        self.assertIsNone(build_dashboard_presentation([], [{"exam_mode": "mock_exam_active",
             "attempt_id": 1, "total_score": 80, "is_passed": True, "date_str": "10/10"}])["recent_score"])
        self.save(55, details=[{"question_id": "Q-PRAC-001", "type": "practical",
                                "earned_score": 0, "max_score": 16, "is_selected": False}])
        with self.app.app_context():
            self.assertFalse(any(c["attempts_count"] for c in self.analytics.get_top_vulnerable_concepts(limit=5)))
        self.assertEqual(get_learning_recommendation({"total_attempts": 1}, 0, [])["primary_btn_url"],
                         "/exam?mode=random")


if __name__ == "__main__":
    unittest.main()
