import os
import re
import unittest
from app import create_app
from app.config import Config
from app.models.database import db_session, init_db, close_db
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.analytics_service import AnalyticsService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestSubmissionIdempotency(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_db(self.app, uri="sqlite:///:memory:")
        self.client = self.app.test_client()
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.history_service = HistoryService(self.loader)
        self.analytics_service = AnalyticsService(self.loader)

    def tearDown(self):
        db_session.remove()
        close_db()
        self.app_context.pop()

    def _sample_post_data(self, token="test_token_123", mode="standard"):
        return {
            "submission_token": token,
            "exam_mode": mode,
            "exam_seed": "42",
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_B": "법적 준거성",
            "ans_Q-SHORT-001_C": "2",
            "ans_Q-SHORT-003": "WPA2",
            "ans_Q-SHORT-005": "robots.txt",
            "ans_Q-SHORT-007": "DLP",
            "ans_Q-SHORT-008": "/proc",
            "ans_Q-SHORT-010": "Log4j"
        }

    def test_prg_pattern_and_redirect(self):
        """PRG 패턴: POST /submit은 직접 HTML을 렌더링하지 않고 302 Redirect를 반환해야 한다."""
        post_data = self._sample_post_data("token_prg_001")
        response = self.client.post("/submit", data=post_data, follow_redirects=False)

        # 1. 302 Redirect 확인
        self.assertEqual(response.status_code, 302)
        location = response.headers.get("Location")
        self.assertTrue(location.startswith("/result/") or "/result/" in location)

        # 2. Redirect된 GET 라우트 확인
        get_resp = self.client.get(location)
        self.assertEqual(get_resp.status_code, 200)
        html = get_resp.get_data(as_text=True)
        self.assertIn("정보보안기사 실기 모의고사 채점 결과", html)
        self.assertIn("/ 100점", html)
        self.assertIn("성공적으로 저장되었습니다", html)

    def test_initial_submission_creates_one_attempt_and_18_answers(self):
        """A. 최초 제출: ExamAttempt 1건 및 AnswerRecord 정확히 18건 생성"""
        post_data = self._sample_post_data("token_single_001")
        response = self.client.post("/submit", data=post_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0].submission_token, "token_single_001")

        detail = self.history_service.get_attempt_detail(attempts[0].id)
        self.assertIsNotNone(detail)
        self.assertEqual(len(detail["answers"]), 18)

    def test_double_post_with_identical_token(self):
        """B. 동일 Token 2회 제출 (Double Click): Attempt 및 AnswerRecord 중복 증가 없음"""
        token = "token_double_click_999"
        post_data = self._sample_post_data(token)

        # First POST
        r1 = self.client.post("/submit", data=post_data, follow_redirects=False)
        self.assertEqual(r1.status_code, 302)
        loc1 = r1.headers.get("Location")

        # Second POST (Double Click / Replay)
        r2 = self.client.post("/submit", data=post_data, follow_redirects=False)
        self.assertEqual(r2.status_code, 302)
        loc2 = r2.headers.get("Location")

        # 동일한 결과 페이지로 리다이렉트
        self.assertEqual(loc1, loc2)

        # DB 레코드 수 확인: Attempt 1개, AnswerRecord 18개
        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 1)

        detail = self.history_service.get_attempt_detail(attempts[0].id)
        self.assertEqual(len(detail["answers"]), 18)

    def test_triple_post_with_identical_token(self):
        """C. 동일 Token 3회 제출: 항상 Attempt=1, AnswerRecord=18 유지"""
        token = "token_triple_post_777"
        post_data = self._sample_post_data(token)

        for _ in range(3):
            r = self.client.post("/submit", data=post_data, follow_redirects=False)
            self.assertEqual(r.status_code, 302)

        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 1)
        detail = self.history_service.get_attempt_detail(attempts[0].id)
        self.assertEqual(len(detail["answers"]), 18)

    def test_distinct_tokens_create_separate_attempts(self):
        """D. 서로 다른 Token 제출: 독립적인 Attempt 각각 생성"""
        p1 = self._sample_post_data("token_alpha_1")
        p2 = self._sample_post_data("token_beta_2")

        r1 = self.client.post("/submit", data=p1, follow_redirects=False)
        r2 = self.client.post("/submit", data=p2, follow_redirects=False)

        self.assertEqual(r1.status_code, 302)
        self.assertEqual(r2.status_code, 302)
        self.assertNotEqual(r1.headers.get("Location"), r2.headers.get("Location"))

        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 2)
        tokens = {a.submission_token for a in attempts}
        self.assertEqual(tokens, {"token_alpha_1", "token_beta_2"})

    def test_f5_refresh_on_result_page(self):
        """F5 새로고침 검증: 결과 화면을 여러 번 새로고침해도 레코드 증가 없음"""
        post_data = self._sample_post_data("token_f5_test")
        r = self.client.post("/submit", data=post_data, follow_redirects=False)
        loc = r.headers.get("Location")

        # F5 새로고침 5회 시뮬레이션 (GET /result/<id>)
        for _ in range(5):
            get_resp = self.client.get(loc)
            self.assertEqual(get_resp.status_code, 200)

        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 1)
        detail = self.history_service.get_attempt_detail(attempts[0].id)
        self.assertEqual(len(detail["answers"]), 18)

    def test_practical_selected_unselected_integrity(self):
        """G. Practical 문항 정합성: 1건 선택 + 1건 미선택 (총 2건), 전체 18건 유지"""
        post_data = self._sample_post_data("token_prac_test")
        self.client.post("/submit", data=post_data, follow_redirects=True)

        attempts = self.history_service.get_attempts()
        self.assertEqual(len(attempts), 1)
        detail = self.history_service.get_attempt_detail(attempts[0].id)

        prac_answers = [a for a in detail["answers"] if a["question_type"] == "practical"]
        self.assertEqual(len(prac_answers), 2)

        selected = [a for a in prac_answers if a["question_id"] == "Q-PRAC-001"]
        unselected = [a for a in prac_answers if a["question_id"] != "Q-PRAC-001"]

        self.assertEqual(len(selected), 1)
        self.assertEqual(len(unselected), 1)
        self.assertEqual(unselected[0]["achievement_status"], "unselected")

    def test_dashboard_stats_not_distorted_by_duplicate_submissions(self):
        """H. Dashboard 집계: 중복 POST 재요청 후에도 응시 횟수 및 통계가 1회만 반영됨"""
        token = "token_dashboard_idempotent"
        post_data = self._sample_post_data(token)

        # 3회 중복 제출
        self.client.post("/submit", data=post_data, follow_redirects=False)
        self.client.post("/submit", data=post_data, follow_redirects=False)
        self.client.post("/submit", data=post_data, follow_redirects=False)

        dash_resp = self.client.get("/dashboard")
        self.assertEqual(dash_resp.status_code, 200)
        html = dash_resp.get_data(as_text=True)

        # 총 응시 횟수 KPI 카드가 1회로 표시되어야 함
        self.assertIn("총 모의고사 응시", html)
        self.assertEqual(self.history_service.get_attempt_count(), 1)

    def test_all_exam_modes_supply_unique_submission_token(self):
        """모든 시험 모드(standard, random, wrong_review, adaptive)에서 고유 submission_token 제공 확인"""
        tokens = set()
        for mode in ("standard", "random", "wrong_review", "adaptive"):
            r = self.client.get(f"/exam?mode={mode}")
            self.assertEqual(r.status_code, 200)
            html = r.get_data(as_text=True)

            m = re.search(r'name="submission_token"\s+value="([^"]+)"', html)
            self.assertIsNotNone(m, f"Mode {mode} must supply submission_token hidden input")
            token = m.group(1)
            self.assertTrue(len(token) >= 32)
            self.assertNotIn(token, tokens, f"Token for mode {mode} must be uniquely generated")
            tokens.add(token)

    def test_service_level_race_condition_and_unique_constraint(self):
        """서비스 레벨 Race Condition 방어: 동일 토큰 재저장 시 기존 attempt 반환"""
        grading_result = {
            "total_score": 50.0,
            "summary": {"short": {"earned": 20.0}, "descriptive": {"earned": 30.0}, "practical": {"earned": 0.0}},
            "is_passed": False,
            "details": []
        }
        att1 = self.history_service.save_exam_attempt(
            exam_mode="standard",
            seed=None,
            selected_practical_id=None,
            grading_result=grading_result,
            answers={},
            submission_token="token_race_001"
        )
        self.assertIsNotNone(att1.id)

        # Second attempt with same token directly via service
        att2 = self.history_service.save_exam_attempt(
            exam_mode="standard",
            seed=None,
            selected_practical_id=None,
            grading_result=grading_result,
            answers={},
            submission_token="token_race_001"
        )
        self.assertEqual(att1.id, att2.id)
        self.assertEqual(self.history_service.get_attempt_count(), 1)

if __name__ == "__main__":
    unittest.main()
