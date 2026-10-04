# -*- coding: utf-8 -*-
"""
Goal 4F-Fix: CSRF Security Audit & Verification Test Suite
Verifies CSRF token generation, header/form validation, missing/invalid token rejection (403),
POST delete security with cascade removal, 404 on nonexistent records, and coexistence with idempotency.
"""
import unittest
import re
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db, db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.csrf_service import CSRF_SESSION_KEY, CSRF_FORM_FIELD, CSRF_HEADER_NAME


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class TestCSRFSecurity(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_db(self.app, uri="sqlite:///:memory:")
        self.client = self.app.test_client()
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.history_service = HistoryService(self.loader)

    def tearDown(self):
        db_session.remove()
        close_db()
        self.app_context.pop()

    def _sample_submit_data(self, csrf_token=None, submission_token="token_csrf_test_01"):
        data = {
            "submission_token": submission_token,
            "exam_mode": "standard",
            "exam_seed": "42",
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001_sub_1": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_sub_2": "법적 준거성",
            "ans_Q-SHORT-001_sub_3": "2"
        }
        if csrf_token is not None:
            data[CSRF_FORM_FIELD] = csrf_token
        return data

    def test_01_csrf_token_generated_in_session_and_template(self):
        """1. GET /exam initializes CSRF token in session and embeds it in form."""
        resp = self.client.get("/exam")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        m = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
        self.assertIsNotNone(m, "exam.html must contain hidden csrf_token field")
        token = m.group(1)
        self.assertEqual(len(token), 64, "CSRF token must be 32 bytes hex (64 chars)")

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get(CSRF_SESSION_KEY), token)

    def test_02_submit_success_with_valid_form_token(self):
        """2. POST /submit succeeds (302 PRG) when valid CSRF token is provided in form."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "valid_csrf_token_12345"

        post_data = self._sample_submit_data(csrf_token="valid_csrf_token_12345")
        resp = self.client.post("/submit", data=post_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertIn("/result/", resp.headers.get("Location", ""))

    def test_03_submit_success_with_valid_header_token(self):
        """3. POST /submit succeeds when valid CSRF token is passed in X-CSRF-Token header."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "header_token_secret_999"

        post_data = self._sample_submit_data(csrf_token=None)
        headers = {CSRF_HEADER_NAME: "header_token_secret_999"}
        resp = self.client.post("/submit", data=post_data, headers=headers, follow_redirects=False)

        self.assertEqual(resp.status_code, 302)
        self.assertIn("/result/", resp.headers.get("Location", ""))

    def test_04_submit_rejected_when_token_missing(self):
        """4. POST /submit returns 403 Forbidden when CSRF token is completely missing."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "active_session_token"

        post_data = self._sample_submit_data(csrf_token=None)
        resp = self.client.post("/submit", data=post_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 403)
        html = resp.get_data(as_text=True)
        self.assertIn("403 Forbidden", html)
        self.assertIn("CSRF", html)

    def test_05_submit_rejected_when_token_invalid(self):
        """5. POST /submit returns 403 Forbidden when CSRF token does not match session."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "genuine_session_token"

        post_data = self._sample_submit_data(csrf_token="forged_attacker_token")
        resp = self.client.post("/submit", data=post_data, follow_redirects=False)

        self.assertEqual(resp.status_code, 403)
        html = resp.get_data(as_text=True)
        self.assertIn("403 Forbidden", html)

    def test_06_delete_success_with_valid_csrf(self):
        """6. POST /history/<id>/delete succeeds and cascades when valid CSRF token is sent."""
        with self.app.app_context():
            mock_res = {
                "total_score": 50.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            att = self.history_service.save_exam_attempt("standard", None, None, mock_res, {})
            att_id = att.id

        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "delete_token_valid"

        resp = self.client.post(
            f"/history/{att_id}/delete",
            data={CSRF_FORM_FIELD: "delete_token_valid"},
            follow_redirects=True
        )
        self.assertEqual(resp.status_code, 200)

        with self.app.app_context():
            self.assertIsNone(self.history_service.get_attempt_by_id(att_id))
            ans_count = db_session.query(AnswerRecord).filter_by(attempt_id=att_id).count()
            self.assertEqual(ans_count, 0)

    def test_07_delete_rejected_when_token_missing(self):
        """7. POST /history/<id>/delete returns 403 Forbidden when CSRF token is missing."""
        with self.app.app_context():
            att = self.history_service.save_exam_attempt("standard", None, None, {"total_score": 0.0}, {})
            att_id = att.id

        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "delete_session_token"

        # Missing token
        resp = self.client.post(f"/history/{att_id}/delete", data={}, follow_redirects=False)
        self.assertEqual(resp.status_code, 403)

        # Attempt must NOT be deleted
        with self.app.app_context():
            self.assertIsNotNone(self.history_service.get_attempt_by_id(att_id))

    def test_08_delete_rejected_when_token_invalid(self):
        """8. POST /history/<id>/delete returns 403 Forbidden when CSRF token is forged."""
        with self.app.app_context():
            att = self.history_service.save_exam_attempt("standard", None, None, {"total_score": 0.0}, {})
            att_id = att.id

        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "genuine_delete_token"

        resp = self.client.post(
            f"/history/{att_id}/delete",
            data={CSRF_FORM_FIELD: "malicious_token"},
            follow_redirects=False
        )
        self.assertEqual(resp.status_code, 403)

        # Attempt must NOT be deleted
        with self.app.app_context():
            self.assertIsNotNone(self.history_service.get_attempt_by_id(att_id))

    def test_09_delete_nonexistent_attempt_returns_404_with_valid_csrf(self):
        """9. POST /history/<id>/delete returns 404 when valid CSRF is provided but record does not exist."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "valid_token_for_404"

        resp = self.client.post(
            "/history/999999/delete",
            data={CSRF_FORM_FIELD: "valid_token_for_404"},
            follow_redirects=False
        )
        self.assertEqual(resp.status_code, 404)

    def test_10_delete_get_method_returns_405(self):
        """10. GET /history/<id>/delete unconditionally returns 405 Method Not Allowed."""
        resp = self.client.get("/history/1/delete")
        self.assertEqual(resp.status_code, 405)

    def test_11_csrf_and_idempotency_coexistence(self):
        """11. Coexistence: Valid CSRF token with duplicate submission_token preserves idempotency (1 attempt)."""
        with self.client.session_transaction() as sess:
            sess[CSRF_SESSION_KEY] = "coexistence_csrf_token"

        shared_sub_token = "sub_token_idempotent_test_999"
        post_data = self._sample_submit_data(
            csrf_token="coexistence_csrf_token",
            submission_token=shared_sub_token
        )

        # Submit 1
        r1 = self.client.post("/submit", data=post_data, follow_redirects=False)
        self.assertEqual(r1.status_code, 302)
        loc1 = r1.headers.get("Location")

        # Submit 2 (same submission token)
        r2 = self.client.post("/submit", data=post_data, follow_redirects=False)
        self.assertEqual(r2.status_code, 302)
        loc2 = r2.headers.get("Location")

        # Both redirect to identical attempt result
        self.assertEqual(loc1, loc2)

        # DB has exactly 1 attempt
        attempts = self.history_service.get_attempts()
        matching = [a for a in attempts if a.submission_token == shared_sub_token]
        self.assertEqual(len(matching), 1)

    def test_12_csrf_rejection_never_produces_500_internal_server_error(self):
        """12. CSRF rejection strictly returns 403 and renders friendly error template, never 500."""
        post_data = self._sample_submit_data(csrf_token="invalid_random_token")
        resp = self.client.post("/submit", data=post_data, follow_redirects=False)
        self.assertNotEqual(resp.status_code, 500)
        self.assertEqual(resp.status_code, 403)


if __name__ == "__main__":
    unittest.main()
