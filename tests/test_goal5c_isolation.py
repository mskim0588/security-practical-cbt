import unittest
import json
import secrets
from unittest.mock import patch, MagicMock
from flask import session
from app import create_app
from app.config import Config
from app.models.database import db_session, close_db, init_db
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.analytics_service import AnalyticsService

class TestGoal5CDataIsolationAndSecurity(unittest.TestCase):
    """
    Goal 5C: Comprehensive Guest / Owner Data Isolation & Production Security Tests
    Verifies all 20 required isolation, authorization, session, CSRF, and hardening criteria.
    """

    def setUp(self):
        class TestConfig(Config):
            TESTING = True
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
            ADMIN_ACCESS_KEY = "test-owner-secret-key"

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.history_service = HistoryService(self.loader)
        self.wrong_service = WrongAnswerService(self.loader)
        self.analytics_service = AnalyticsService(self.loader)

    def tearDown(self):
        self.app_context.pop()
        close_db()

    def _login_as_owner(self, client):
        """Helper: authenticate client as owner"""
        with client.session_transaction() as sess:
            sess["is_admin"] = True
            sess["csrf_token"] = "valid-owner-csrf-token"

    def _create_mock_attempt(self, is_owner: bool, total_score: float = 70.0, answers_map: dict = None, token: str = None):
        if answers_map is None:
            answers_map = {"Q-SHORT-001": "ans"}
        grading_result = {
            "total_score": total_score,
            "is_passed": total_score >= 60.0,
            "summary": {
                "short": {"earned": 30.0},
                "descriptive": {"earned": 24.0},
                "practical": {"earned": 16.0}
            },
            "details": []
        }
        for qid, ans in answers_map.items():
            is_correct = (ans == "correct")
            earned = 3.0 if is_correct else 0.0
            grading_result["details"].append({
                "question_id": qid,
                "type": "short",
                "earned_score": earned,
                "max_score": 3.0,
                "is_selected": True
            })
        return self.history_service.save_exam_attempt(
            exam_mode="standard",
            seed=42,
            selected_practical_id=None,
            grading_result=grading_result,
            answers=answers_map,
            submission_token=token or secrets.token_hex(16),
            is_owner=is_owner
        )

    # -------------------------------------------------------------
    # 01. Guest Attempt가 Owner History에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_01_guest_attempt_excluded_from_owner_history(self):
        owner_att = self._create_mock_attempt(is_owner=True, total_score=85.0)
        guest_att = self._create_mock_attempt(is_owner=False, total_score=40.0)

        # Service level
        owner_attempts = self.history_service.get_attempts(is_owner=True)
        self.assertEqual(len(owner_attempts), 1)
        self.assertEqual(owner_attempts[0].id, owner_att.id)
        self.assertEqual(self.history_service.get_attempt_count(is_owner=True), 1)

        # Route level
        self._login_as_owner(self.client)
        res = self.client.get("/history")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn(f"/history/{owner_att.id}", body)
        self.assertNotIn(f"/history/{guest_att.id}", body)

        # Detail route level: guest attempt cannot be viewed in /history/<id>
        res_guest = self.client.get(f"/history/{guest_att.id}")
        self.assertEqual(res_guest.status_code, 404)

    # -------------------------------------------------------------
    # 02. Guest Attempt가 Owner Wrong Notes에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_02_guest_attempt_excluded_from_owner_wrong_notes(self):
        # Owner fails Q-SHORT-001
        self._create_mock_attempt(is_owner=True, answers_map={"Q-SHORT-001": "wrong"})
        # Guest fails Q-SHORT-002
        self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-002": "wrong"})

        wrong_qs = self.wrong_service.get_wrong_questions(is_owner=True)
        wrong_ids = [w["question_id"] for w in wrong_qs]

        self.assertIn("Q-SHORT-001", wrong_ids)
        self.assertNotIn("Q-SHORT-002", wrong_ids)

    # -------------------------------------------------------------
    # 03. Guest Correct가 Owner Wrong Note를 resolve하지 않는다.
    # -------------------------------------------------------------
    def test_03_guest_correct_does_not_resolve_owner_wrong_note(self):
        # Owner gets Q-SHORT-001 wrong
        self._create_mock_attempt(is_owner=True, answers_map={"Q-SHORT-001": "wrong"})
        self.assertEqual(self.wrong_service.get_wrong_question_count(is_owner=True), 1)

        # Guest gets Q-SHORT-001 correct later
        self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-001": "correct"})

        # Owner's wrong note MUST remain unresolved
        wrong_qs = self.wrong_service.get_wrong_questions(is_owner=True)
        wrong_ids = [w["question_id"] for w in wrong_qs]
        self.assertIn("Q-SHORT-001", wrong_ids)
        self.assertEqual(self.wrong_service.get_wrong_question_count(is_owner=True), 1)

    # -------------------------------------------------------------
    # 04. Guest Attempt가 Dashboard KPI에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_04_guest_attempt_excluded_from_dashboard_kpis(self):
        self._create_mock_attempt(is_owner=True, total_score=90.0)
        self._create_mock_attempt(is_owner=False, total_score=20.0)
        self._create_mock_attempt(is_owner=False, total_score=10.0)

        stats = self.analytics_service.get_summary_stats(is_owner=True)
        self.assertEqual(stats["total_attempts"], 1)
        self.assertEqual(stats["average_score"], 90.0)
        self.assertEqual(stats["highest_score"], 90.0)
        self.assertEqual(stats["latest_score"], 90.0)

    # -------------------------------------------------------------
    # 05. Guest Attempt가 Category Analytics에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_05_guest_attempt_excluded_from_category_analytics(self):
        # Q-SHORT-008 is "시스템 보안"
        self._create_mock_attempt(is_owner=True, answers_map={"Q-SHORT-008": "correct"})
        self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-008": "wrong"})

        cats = self.analytics_service.get_category_analytics(is_owner=True)
        sys_cat = next(c for c in cats if c["category"] == "시스템 보안")
        self.assertEqual(sys_cat["attempts_count"], 1)
        self.assertEqual(sys_cat["sufficient_count"], 1)
        self.assertEqual(sys_cat["incorrect_count"], 0)

    # -------------------------------------------------------------
    # 06. Guest Attempt가 Concept Analytics에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_06_guest_attempt_excluded_from_concept_analytics(self):
        # Q-SHORT-008 is mapped to concept CON-SYS-03
        self._create_mock_attempt(is_owner=True, answers_map={"Q-SHORT-008": "correct"})
        self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-008": "wrong"})

        concepts = self.analytics_service.get_concept_analytics(is_owner=True)
        c_stats = next(c for c in concepts if c["concept_id"] == "CON-SYS-03")
        self.assertEqual(c_stats["attempts_count"], 1)
        self.assertEqual(c_stats["sufficient_count"], 1)
        self.assertEqual(c_stats["incorrect_count"], 0)

    # -------------------------------------------------------------
    # 07. Guest Attempt가 VI에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_07_guest_attempt_excluded_from_vi(self):
        self._create_mock_attempt(is_owner=True, answers_map={"Q-SHORT-008": "correct"})
        vi_before = {c["concept_id"]: c["vulnerability_index"] for c in self.analytics_service.get_concept_analytics(is_owner=True)}

        # Add 5 guest failures for same question
        for _ in range(5):
            self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-008": "wrong"})

        vi_after = {c["concept_id"]: c["vulnerability_index"] for c in self.analytics_service.get_concept_analytics(is_owner=True)}
        self.assertEqual(vi_before, vi_after)

    # -------------------------------------------------------------
    # 08. Guest Attempt가 Adaptive source data에 포함되지 않는다.
    # -------------------------------------------------------------
    def test_08_guest_attempt_excluded_from_adaptive_source_data(self):
        top_before = self.analytics_service.get_top_vulnerable_concepts(limit=5, is_owner=True)
        for _ in range(5):
            self._create_mock_attempt(is_owner=False, answers_map={"Q-SHORT-008": "wrong"})
        top_after = self.analytics_service.get_top_vulnerable_concepts(limit=5, is_owner=True)

        self.assertEqual([c["concept_id"] for c in top_before], [c["concept_id"] for c in top_after])

    # -------------------------------------------------------------
    # 09. Browser A Result를 Browser B가 조회할 수 없다.
    # -------------------------------------------------------------
    def test_09_browser_a_result_inaccessible_by_browser_b(self):
        client_a = self.app.test_client()
        client_b = self.app.test_client()

        # Browser A submits exam
        att_a = self._create_mock_attempt(is_owner=False, total_score=75.0)
        with client_a.session_transaction() as sess:
            sess["submitted_attempts"] = [att_a.id]

        # Browser A can view its own result
        res_a = client_a.get(f"/result/{att_a.id}")
        self.assertEqual(res_a.status_code, 200)

        # Browser B attempts to view Browser A's result (IDOR attempt)
        res_b = client_b.get(f"/result/{att_a.id}")
        self.assertEqual(res_b.status_code, 403)

    # -------------------------------------------------------------
    # 10. Invalid Result Ownership → 403 또는 404
    # -------------------------------------------------------------
    def test_10_invalid_result_ownership_returns_403_or_404(self):
        # Guest accessing non-existent result
        res_guest = self.client.get("/result/999999")
        self.assertIn(res_guest.status_code, (403, 404))

        # Admin accessing non-existent result
        self._login_as_owner(self.client)
        res_admin = self.client.get("/result/999999")
        self.assertEqual(res_admin.status_code, 404)

    # -------------------------------------------------------------
    # 11. Owner Result 정상 접근
    # -------------------------------------------------------------
    def test_11_owner_result_access(self):
        owner_att = self._create_mock_attempt(is_owner=True, total_score=88.0)
        self._login_as_owner(self.client)
        res = self.client.get(f"/result/{owner_att.id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers.get("X-Robots-Tag"), "noindex, nofollow")

    # -------------------------------------------------------------
    # 12. Guest adaptive가 Owner Analytics를 사용하지 않는다.
    # -------------------------------------------------------------
    def test_12_guest_adaptive_fallback_to_random(self):
        # Unauthenticated guest requests adaptive mode
        res = self.client.get("/exam?mode=adaptive")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        # Should fallback to random mode for guest
        self.assertIn('name="exam_mode" value="random"', body)

    # -------------------------------------------------------------
    # 13. Guest wrong_review가 Owner Wrong Notes를 사용하지 않는다.
    # -------------------------------------------------------------
    def test_13_guest_wrong_review_fallback_to_standard(self):
        # Unauthenticated guest requests wrong_review mode
        res = self.client.get("/exam?mode=wrong_review")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        # Should fallback to standard mode for guest
        self.assertIn('name="exam_mode" value="standard"', body)

    # -------------------------------------------------------------
    # 14. Protected Route 직접 접근 차단
    # -------------------------------------------------------------
    def test_14_protected_routes_block_unauthorized_guest(self):
        routes = ["/dashboard", "/history", "/wrong-notes", "/wrong-notes/Q-SHORT-001"]
        for r in routes:
            res = self.client.get(r)
            self.assertEqual(res.status_code, 302, f"Route {r} should redirect unauthorized guests")
            self.assertIn("/admin-login", res.headers.get("Location"))

    # -------------------------------------------------------------
    # 15. Logout 후 Protected Route 접근 차단
    # -------------------------------------------------------------
    def test_15_logout_revokes_access_to_protected_routes(self):
        self._login_as_owner(self.client)
        res = self.client.get("/dashboard")
        self.assertEqual(res.status_code, 200)

        with self.client.session_transaction() as sess:
            csrf_tok = sess.get("csrf_token")

        logout_res = self.client.post("/admin-logout", data={"csrf_token": csrf_tok})
        self.assertEqual(logout_res.status_code, 302)

        after_res = self.client.get("/dashboard")
        self.assertEqual(after_res.status_code, 302)
        self.assertIn("/admin-login", after_res.headers.get("Location"))

    # -------------------------------------------------------------
    # 16. Missing/invalid CSRF 차단
    # -------------------------------------------------------------
    def test_16_missing_and_invalid_csrf_blocked(self):
        # Missing token
        res_missing = self.client.post("/admin-login", data={"access_key": "any"})
        self.assertEqual(res_missing.status_code, 403)

        # Invalid token
        res_invalid = self.client.post("/admin-login", data={"access_key": "any", "csrf_token": "bad-token"})
        self.assertEqual(res_invalid.status_code, 403)

    # -------------------------------------------------------------
    # 17. Production Secret missing → Fail Closed
    # -------------------------------------------------------------
    def test_17_production_secret_missing_fails_closed(self):
        class InsecureProdConfig(Config):
            FLASK_ENV = "production"
            IS_PRODUCTION = True
            TESTING = False
            SECRET_KEY = "cbt-dev-secret-key-2026"  # dev fallback

        with self.assertRaises(RuntimeError) as ctx:
            create_app(InsecureProdConfig)
        self.assertIn("CRITICAL SECURITY ERROR", str(ctx.exception))

    # -------------------------------------------------------------
    # 18. healthz DB 장애 시 민감정보 비노출
    # -------------------------------------------------------------
    def test_18_healthz_db_failure_does_not_leak_internals(self):
        with patch("app.models.database.engine.connect") as mock_conn:
            mock_conn.side_effect = Exception("postgres://admin:super_secret_pw@db.railway.internal:5432/main DB crashed")
            res = self.client.get("/healthz")
            self.assertEqual(res.status_code, 503)
            data = res.get_json()
            self.assertEqual(data.get("status"), "error")
            self.assertEqual(data.get("database"), "unhealthy")
            # Must not leak secret or connection string
            self.assertNotIn("super_secret_pw", str(data))
            self.assertNotIn("postgres://", str(data))

    # -------------------------------------------------------------
    # 19. Duplicate submission → Attempt 1개
    # -------------------------------------------------------------
    def test_19_duplicate_submission_creates_single_attempt(self):
        token = secrets.token_hex(16)
        att1 = self._create_mock_attempt(is_owner=True, total_score=70.0, token=token)
        att2 = self._create_mock_attempt(is_owner=True, total_score=70.0, token=token)

        self.assertEqual(att1.id, att2.id)
        count = self.history_service.get_attempt_count(is_owner=True)
        self.assertEqual(count, 1)

    # -------------------------------------------------------------
    # 20. Concurrent-like duplicate token path에서도 기존 Attempt 정상 반환
    # -------------------------------------------------------------
    def test_20_concurrent_duplicate_token_integrity_error_handled(self):
        token = secrets.token_hex(16)
        att1 = self._create_mock_attempt(is_owner=True, total_score=70.0, token=token)

        # Force bypass initial check and simulate concurrent INSERT race condition
        from sqlalchemy.exc import IntegrityError
        with patch("app.services.history_service.db_session.scalar") as mock_scalar:
            # First call (check) returns None, second call (in except) returns existing att1
            mock_scalar.side_effect = [None, att1]
            with patch("app.services.history_service.db_session.commit") as mock_commit:
                mock_commit.side_effect = IntegrityError("UNIQUE constraint failed", params=None, orig=None)
                att2 = self._create_mock_attempt(is_owner=True, total_score=70.0, token=token)
                self.assertEqual(att1.id, att2.id)

if __name__ == "__main__":
    unittest.main()
