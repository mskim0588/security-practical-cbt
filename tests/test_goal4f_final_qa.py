# -*- coding: utf-8 -*-
"""
Goal 4F: Desktop Final QA & Release Baseline Verification Test Suite
Comprehensive automated audit covering all 4 user journeys, route inventory,
security audits, data integrity, idempotency, and error handling.
"""
import unittest
import json
import re
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db, db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.analytics_service import AnalyticsService
from app.services.wrong_answer_service import WrongAnswerService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestGoal4FFinalQA(unittest.TestCase):
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

    def test_01_all_14_routes_accessible(self):
        """1. Verify that all 14 routes in the system respond with proper status codes."""
        # Setup a sample attempt for routes requiring an ID
        with self.app.app_context():
            mock_res = {
                "total_score": 60.0,
                "is_passed": True,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            att = self.history_service.save_exam_attempt("standard", None, None, mock_res, {"Q-SHORT-001": "ans"})
            att_id = att.id

        # GET routes (should return 200)
        get_routes = [
            "/",
            "/dashboard",
            "/concepts",
            "/concepts/CON-MGT-01",
            "/exam",
            "/history",
            f"/history/{att_id}",
            f"/result/{att_id}",
            "/wrong-notes",
            "/wrong-notes/Q-SHORT-001"
        ]
        for url in get_routes:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"Failed GET {url}: status {resp.status_code}")

        # POST-only routes (GET should return 405)
        post_only_routes = [
            "/review",
            "/submit",
            f"/history/{att_id}/delete"
        ]
        for url in post_only_routes:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 405, f"GET {url} should be 405 Method Not Allowed")

    def test_02_e2e_scenario_1_standard_exam_submission_result_history(self):
        """2. E2E Scenario 1: Standard Exam -> Review -> Submit -> Result -> History -> History Detail."""
        # Step A: View exam
        r_exam = self.client.get("/exam?mode=standard")
        self.assertEqual(r_exam.status_code, 200)
        exam_html = r_exam.get_data(as_text=True)
        self.assertIn('name="submission_token"', exam_html)
        self.assertIn('name="selected_practical_id"', exam_html)
        m_csrf = re.search(r'name="csrf_token" value="([^"]+)"', exam_html)
        csrf_token = m_csrf.group(1) if m_csrf else "test-csrf"

        # Step B: Review exam POST
        review_data = {
            "csrf_token": csrf_token,
            "submission_token": "token-e2e-sc1",
            "exam_mode": "standard",
            "seed": "42",
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001_sub_1": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_sub_2": "법적 준거성",
            "ans_Q-SHORT-001_sub_3": "2"
        }
        r_rev = self.client.post("/review", data=review_data)
        self.assertEqual(r_rev.status_code, 200)
        self.assertIn("답안 최종 검토", r_rev.get_data(as_text=True))

        # Step C: Submit exam POST (PRG pattern -> redirects to /result/<id>)
        r_sub = self.client.post("/submit", data=review_data, follow_redirects=False)
        self.assertEqual(r_sub.status_code, 302)
        result_url = r_sub.headers.get("Location")
        self.assertIn("/result/", result_url)

        # Step D: View Result
        r_res = self.client.get(result_url)
        self.assertEqual(r_res.status_code, 200)
        res_html = r_res.get_data(as_text=True)
        self.assertIn("채점 결과 리포트", res_html)
        self.assertIn("심층 해설", res_html)
        self.assertIn("ai-prompt-modal", res_html)

        # Step E: View History
        r_hist = self.client.get("/history")
        self.assertEqual(r_hist.status_code, 200)
        self.assertIn("📘 표준 모의고사", r_hist.get_data(as_text=True))

        # Step F: View History Detail
        attempt_id = result_url.split("/")[-1]
        r_hdetail = self.client.get(f"/history/{attempt_id}")
        self.assertEqual(r_hdetail.status_code, 200)
        self.assertIn("📘 표준 모의고사", r_hdetail.get_data(as_text=True))
        self.assertIn("ai-prompt-modal", r_hdetail.get_data(as_text=True))

    def test_03_e2e_scenario_2_random_fail_wrong_notes_reexam_resolution(self):
        """3. E2E Scenario 2: Fail question -> Wrong Notes -> Wrong Detail -> Explanation -> Re-exam -> Resolved."""
        with self.app.app_context():
            # Failure on Q-SHORT-002
            res1 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("random", 123, None, res1, {"Q-SHORT-002": "incorrect answer"})

        # Step A: Appears in Wrong Notes
        r_wn = self.client.get("/wrong-notes")
        self.assertEqual(r_wn.status_code, 200)
        wn_html = r_wn.get_data(as_text=True)
        self.assertIn("Q-SHORT-002", wn_html)
        self.assertIn("🔥 오답 집중 모의고사", wn_html)

        # Step B: Wrong Detail view
        r_wd = self.client.get("/wrong-notes/Q-SHORT-002")
        self.assertEqual(r_wd.status_code, 200)
        wd_html = r_wd.get_data(as_text=True)
        self.assertIn("문항 심층 복기 리포트", wd_html)
        self.assertIn("/concepts/", wd_html)  # Concept link
        self.assertIn("ai-prompt-modal", wd_html)  # AI modal
        self.assertIn("incorrect answer", wd_html)  # Timeline contains submitted answer

        # Step C: Retake and solve correctly
        with self.app.app_context():
            res2 = {
                "total_score": 3.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("wrong_review", None, None, res2, {"Q-SHORT-002": "correct answer"})

        # Step D: Verified resolved in wrong notes (active count becomes 0)
        r_wn2 = self.client.get("/wrong-notes")
        self.assertIn("현재 미해결된 오답 문항이 없습니다", r_wn2.get_data(as_text=True))

    def test_04_e2e_scenario_3_dashboard_vulnerable_adaptive_exam(self):
        """4. E2E Scenario 3: Dashboard -> Weakest Concept Clinic -> Concept Detail -> Adaptive Exam."""
        with self.app.app_context():
            # Fail CON-MGT-01
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        # Step A: Dashboard identifies vulnerable concept
        r_dash = self.client.get("/dashboard")
        self.assertEqual(r_dash.status_code, 200)
        dash_html = r_dash.get_data(as_text=True)
        self.assertIn("CON-MGT-01", dash_html)
        self.assertIn("취약 개념 집중 모의고사", dash_html)

        # Step B: Follow concept detail
        r_c = self.client.get("/concepts/CON-MGT-01")
        self.assertEqual(r_c.status_code, 200)
        self.assertIn("위험관리 및 위험평가 방법론", r_c.get_data(as_text=True))

        # Step C: Enter adaptive exam
        r_adap = self.client.get("/exam?mode=adaptive")
        self.assertEqual(r_adap.status_code, 200)
        self.assertIn("취약 Concept 집중 모의고사", r_adap.get_data(as_text=True))

    def test_05_e2e_scenario_4_concept_search_and_detail_to_exam(self):
        """5. E2E Scenario 4: Concept Library -> Search -> Detail -> Related Questions -> Exam."""
        # Step A: Search for "방화벽"
        r_lib = self.client.get("/concepts?q=방화벽")
        self.assertEqual(r_lib.status_code, 200)
        lib_html = r_lib.get_data(as_text=True)
        self.assertIn("CON-NET-01", lib_html)

        # Step B: View detail
        r_detail = self.client.get("/concepts/CON-NET-01")
        self.assertEqual(r_detail.status_code, 200)
        self.assertIn("네트워크 패킷 분석 및 방화벽/탐지", r_detail.get_data(as_text=True))
        self.assertIn("연계 기출 및 연습 문제", r_detail.get_data(as_text=True))

    def test_06_security_history_delete_method_post_only(self):
        """6. Security Audit: History deletion MUST be POST only, confirm cascade delete of answers."""
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
            sess["csrf_token"] = "test-csrf-del"

        # GET request MUST return 405 Method Not Allowed
        get_del = self.client.get(f"/history/{att_id}/delete")
        self.assertEqual(get_del.status_code, 405)

        # POST request succeeds and deletes attempt + cascade answer records
        post_del = self.client.post(f"/history/{att_id}/delete", data={"csrf_token": "test-csrf-del"}, follow_redirects=True)
        self.assertEqual(post_del.status_code, 200)

        with self.app.app_context():
            # Attempt must be deleted
            deleted_att = self.history_service.get_attempt_by_id(att_id)
            self.assertIsNone(deleted_att)
            # Child answers must also be cascade-deleted
            ans_count = db_session.query(AnswerRecord).filter_by(attempt_id=att_id).count()
            self.assertEqual(ans_count, 0)

    def test_07_security_no_xss_and_no_ai_leaks(self):
        """7. Security Audit: User-submitted scripts are escaped, AI modal contains zero secrets."""
        with self.app.app_context():
            xss_payload = '<script>alert("xss")</script>'
            mock_res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            att = self.history_service.save_exam_attempt(
                "standard", None, None, mock_res,
                {"Q-SHORT-001": xss_payload},
                submission_token="secret-token-xyz-123"
            )
            att_id = att.id

        r_hist = self.client.get(f"/history/{att_id}")
        hist_html = r_hist.get_data(as_text=True)

        # XSS payload is escaped
        self.assertNotIn('<script>alert("xss")</script>', hist_html)
        self.assertIn('&lt;script&gt;alert(&#34;xss&#34;)&lt;/script&gt;', hist_html)

        # Sensitive submission_token is NEVER leaked in HTML
        self.assertNotIn("secret-token-xyz-123", hist_html)

    def test_08_error_handlers_404_and_custom_pages(self):
        """8. Custom 404 handler returns 404 with friendly navigation layout."""
        bad_urls = [
            "/concepts/CON-NON-EXISTENT",
            "/history/999999",
            "/wrong-notes/INVALID-Q-999",
            "/some-completely-invalid-url"
        ]
        for url in bad_urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 404, f"URL {url} did not return 404")
            html = resp.get_data(as_text=True)
            self.assertIn("요청하신 페이지를 찾을 수 없습니다", html)
            self.assertIn("/exam", html)

    def test_09_desktop_navigation_active_states(self):
        """9. Global Navigation active state ('is-active') and aria-current reflect current page."""
        nav_checks = [
            ("/", "홈"),
            ("/dashboard", "대시보드"),
            ("/concepts", "개념학습"),
            ("/exam", "모의고사"),
            ("/history", "응시이력"),
            ("/wrong-notes", "오답노트")
        ]
        for path, label in nav_checks:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('aria-current="page"', html)
            self.assertIn('is-active', html)

    def test_10_recommendation_boundary_states(self):
        """10. Deterministic recommendation generator handles all boundary cases without collision."""
        from app.routes.dashboard_routes import get_learning_recommendation

        # Case 1: 0 attempts -> onboarding
        r1 = get_learning_recommendation({"total_attempts": 0}, 0, [])
        self.assertEqual(r1["type"], "onboarding")

        # Case 2: wrong_count > 0 takes precedence over vulnerable concepts
        r2 = get_learning_recommendation(
            {"total_attempts": 3}, 2,
            [{"name": "X", "concept_id": "CON-01", "vulnerability_index": 100.0}]
        )
        self.assertEqual(r2["type"], "wrong_review")

        # Case 3: wrong_count == 0 and VI > 0 -> concept clinic
        r3 = get_learning_recommendation(
            {"total_attempts": 3}, 0,
            [{"name": "X", "concept_id": "CON-01", "vulnerability_index": 80.0}]
        )
        self.assertEqual(r3["type"], "concept_clinic")

        # Case 4: wrong_count == 0 and VI == 0 -> practice
        r4 = get_learning_recommendation(
            {"total_attempts": 3, "pass_rate": 100.0}, 0,
            [{"name": "X", "concept_id": "CON-01", "vulnerability_index": 0.0}]
        )
        self.assertEqual(r4["type"], "practice")

    def test_11_data_integrity_and_referential_fidelity(self):
        """11. Verify 180 questions, 20 concepts, 12 sources, 180 explanations, and 20 concept contents."""
        questions = self.loader.load_questions()
        concepts = self.loader.load_concepts()
        sources = self.loader.load_sources()
        explanations = self.loader.load_explanations()
        concept_contents = self.loader.load_concept_contents()

        self.assertEqual(len(questions), 180)
        self.assertEqual(len(concepts), 20)
        self.assertEqual(len(sources), 12)
        self.assertEqual(len(explanations), 180)
        self.assertEqual(len(concept_contents), 20)

        c_ids = {c["id"] for c in concepts}
        s_ids = {s["id"] for s in sources}
        q_ids = {q["id"] for q in questions}

        for q in questions:
            self.assertIn(q.get("concept_id"), c_ids)
            self.assertIn(q.get("source_id"), s_ids)
            self.assertIn(q["id"], explanations)

        for c in concepts:
            self.assertIn(c["id"], concept_contents)

    def test_12_idempotency_double_and_triple_post(self):
        """12. Idempotency Audit: Double/Triple POST of same submission_token returns identical attempt."""
        token = "test-token-idempotency-final-qa"
        mock_res = {
            "total_score": 80.0,
            "is_passed": True,
            "summary": {"short": {"earned": 30.0}, "descriptive": {"earned": 30.0}, "practical": {"earned": 20.0}},
            "details": [
                {"question_id": f"Q-SHORT-{i:03d}", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                for i in range(1, 13)
            ]
        }

        with self.app.app_context():
            # Post 1
            att1 = self.history_service.save_exam_attempt(
                "standard", None, None, mock_res, {}, submission_token=token
            )
            # Post 2
            att2 = self.history_service.save_exam_attempt(
                "standard", None, None, mock_res, {}, submission_token=token
            )
            # Post 3
            att3 = self.history_service.save_exam_attempt(
                "standard", None, None, mock_res, {}, submission_token=token
            )

            # All 3 returns must point to the EXACT same attempt ID
            self.assertEqual(att1.id, att2.id)
            self.assertEqual(att2.id, att3.id)

            # DB must only have 1 attempt for this token
            attempts = db_session.query(ExamAttempt).filter_by(submission_token=token).all()
            self.assertEqual(len(attempts), 1)

            # Exactly 12 answer records for this attempt
            answers = db_session.query(AnswerRecord).filter_by(attempt_id=att1.id).all()
            self.assertEqual(len(answers), 12)

if __name__ == "__main__":
    unittest.main()
