import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.data_loader import DataLoader

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestGoal4DHistoryWrong(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(self.loader)
            self.wrong_service = WrongAnswerService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_01_history_empty_state(self):
        """1. /history shows friendly empty state when no attempts exist."""
        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("아직 저장된 응시 이력이 없습니다", html)
        self.assertIn("/exam", html)

    def test_02_history_list_rendering_and_mode_badges(self):
        """2. /history renders friendly mode badges, status pills, scores, and links."""
        with self.app.app_context():
            modes = [
                ("standard", "📘 표준 모의고사"),
                ("random", "🎲 랜덤 모의고사"),
                ("wrong_review", "🔥 오답 집중 모의고사"),
                ("adaptive", "🎯 취약점 맞춤 모의고사"),
            ]
            for mode, _ in modes:
                mock_res = {
                    "total_score": 65.0,
                    "is_passed": True,
                    "summary": {
                        "short": {"earned": 24.0},
                        "descriptive": {"earned": 25.0},
                        "practical": {"earned": 16.0}
                    },
                    "details": [
                        {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0, "is_correct": True},
                        {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0, "is_correct": False},
                        {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0}
                    ]
                }
                self.history_service.save_exam_attempt(
                    exam_mode=mode,
                    seed=42,
                    selected_practical_id=None,
                    grading_result=mock_res,
                    answers={"Q-SHORT-001": "ans1", "Q-SHORT-002": "ans2"}
                )

        resp = self.client.get("/history")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("회 응시 기록", html)
        self.assertIn(">4</span>", html)
        self.assertIn("📘 표준 모의고사", html)
        self.assertIn("🎲 랜덤 모의고사", html)
        self.assertIn("🔥 오답 집중 모의고사", html)
        self.assertIn("🎯 취약점 맞춤 모의고사", html)
        self.assertIn("✓ 합격", html)
        self.assertIn("상세 복기 &rarr;", html)

    def test_03_history_detail_rendering(self):
        """3. /history/<id> renders detailed review with concept link, explanation, and AI modal."""
        with self.app.app_context():
            mock_res = {
                "total_score": 50.0,
                "is_passed": False,
                "summary": {"short": {"earned": 10.0}, "descriptive": {"earned": 20.0}, "practical": {"earned": 20.0}},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0, "sub_results": [
                        {"sub_id": 1, "score": 3.0, "max_score": 6.0, "matched_keywords": ["CIA"], "missing_keywords": ["기밀성"]}
                    ]}
                ]
            }
            att = self.history_service.save_exam_attempt(
                exam_mode="standard",
                seed=1,
                selected_practical_id=None,
                grading_result=mock_res,
                answers={"Q-SHORT-001": "wrong text", "Q-DESC-001": "partial text"}
            )
            att_id = att.id

        resp = self.client.get(f"/history/{att_id}")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("제" + str(att_id) + "회차 모의고사 복기 리포트", html)
        self.assertIn("📘 표준 모의고사", html)
        self.assertIn("/ 100점", html)
        self.assertIn("기준 미달", html)
        self.assertIn("/concepts/", html)  # Concept link rendered
        self.assertIn("ai-prompt-modal", html)  # AI modal included
        self.assertIn("심층 해설", html)  # Deep explanation accordion
        self.assertIn("/exam?mode=wrong_review", html)  # Re-exam CTA

    def test_04_history_detail_404(self):
        """4. /history/<id> returns 404 for non-existent attempt."""
        resp = self.client.get("/history/999999")
        self.assertEqual(resp.status_code, 404)

    def test_05_history_delete(self):
        """5. POST /history/<id>/delete removes attempt and redirects to /history."""
        with self.app.app_context():
            att = self.history_service.save_exam_attempt(
                exam_mode="standard", seed=1, selected_practical_id=None,
                grading_result={"total_score": 0.0, "summary": {}, "details": []},
                answers={}
            )
            att_id = att.id

        with self.client.session_transaction() as sess:
            sess["csrf_token"] = "del-csrf-4d"

        del_resp = self.client.post(f"/history/{att_id}/delete", data={"csrf_token": "del-csrf-4d"}, follow_redirects=True)
        self.assertEqual(del_resp.status_code, 200)
        with self.app.app_context():
            self.assertIsNone(self.history_service.get_attempt_by_id(att_id))

    def test_06_wrong_notes_empty_state(self):
        """6. /wrong-notes displays celebration empty state when no wrong questions exist."""
        resp = self.client.get("/wrong-notes")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("현재 미해결된 오답 문항이 없습니다", html)
        self.assertIn("/exam", html)

    def test_07_wrong_notes_summary_cards_and_primary_cta(self):
        """7. /wrong-notes displays 3 stat cards (미해결 오답, 부분 감점, 반복 오답) and primary CTA."""
        with self.app.app_context():
            # Attempt 1: Q-SHORT-001 (incorrect), Q-DESC-001 (partial)
            res1 = {
                "total_score": 6.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res1, {"Q-SHORT-001": "fail1"})

            # Attempt 2: Q-SHORT-001 failed again (fail_count becomes 2 -> repeat fail!)
            res2 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("random", None, None, res2, {"Q-SHORT-001": "fail2"})

        resp = self.client.get("/wrong-notes")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("미해결 완전 오답 (0점)", html)
        self.assertIn("부분 감점 문항", html)
        self.assertIn("2회 이상 반복 오답", html)
        self.assertIn("🔥 오답 집중 모의고사 시작", html)
        self.assertIn("/exam?mode=wrong_review", html)
        self.assertIn("🔥 반복 오답 2회", html)  # Repeat badge

    def test_08_wrong_notes_filtering_and_reset(self):
        """8. /wrong-notes horizontal filter handles type, status, category, sorting and reset."""
        with self.app.app_context():
            res = {
                "total_score": 4.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-001", "type": "descriptive", "earned_score": 4.0, "max_score": 12.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        # Type filter
        resp_short = self.client.get("/wrong-notes?type=short")
        self.assertEqual(resp_short.status_code, 200)
        self.assertIn("Q-SHORT-001", resp_short.get_data(as_text=True))
        self.assertNotIn("Q-DESC-001", resp_short.get_data(as_text=True))

        # Reset button visible when filtered
        self.assertIn("🔄 초기화", resp_short.get_data(as_text=True))

        # Status filter
        resp_partial = self.client.get("/wrong-notes?status=partial")
        self.assertEqual(resp_partial.status_code, 200)
        self.assertIn("Q-DESC-001", resp_partial.get_data(as_text=True))
        self.assertNotIn("Q-SHORT-001", resp_partial.get_data(as_text=True))

        # Sort filter
        resp_sort = self.client.get("/wrong-notes?sort=frequency")
        self.assertEqual(resp_sort.status_code, 200)

    def test_09_wrong_detail_rendering(self):
        """9. /wrong-notes/<question_id> renders connected concept, timeline, explanation, and AI modal."""
        with self.app.app_context():
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {"Q-SHORT-001": "my wrong answer"})

        resp = self.client.get("/wrong-notes/Q-SHORT-001")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        self.assertIn("문항 심층 복기 리포트", html)
        self.assertIn("Q-SHORT-001", html)
        self.assertIn("연계 보안 개념", html)
        self.assertIn("/concepts/", html)  # Concept link
        self.assertIn("나의 응시 이력 타임라인", html)
        self.assertIn("timeline-container", html)
        self.assertIn("my wrong answer", html)
        self.assertIn("ai-prompt-modal", html)  # AI modal included
        self.assertIn("/exam?mode=wrong_review", html)  # Re-exam CTA

    def test_10_wrong_detail_404(self):
        """10. /wrong-notes/<question_id> returns 404 for invalid question ID."""
        resp = self.client.get("/wrong-notes/INVALID-999")
        self.assertEqual(resp.status_code, 404)

    def test_11_ai_prompt_modal_included_across_views(self):
        """11. AI prompt modal component is properly present in history detail, wrong notes, and wrong detail."""
        with self.app.app_context():
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            att = self.history_service.save_exam_attempt("standard", None, None, res, {"Q-SHORT-001": "wrong"})
            att_id = att.id

        # 1. /history/<id>
        r1 = self.client.get(f"/history/{att_id}")
        self.assertIn('id="ai-prompt-modal"', r1.get_data(as_text=True))
        self.assertIn('학습 프롬프트 생성기', r1.get_data(as_text=True))

        # 2. /wrong-notes
        r2 = self.client.get("/wrong-notes")
        self.assertIn('id="ai-prompt-modal"', r2.get_data(as_text=True))

        # 3. /wrong-notes/Q-SHORT-001
        r3 = self.client.get("/wrong-notes/Q-SHORT-001")
        self.assertIn('id="ai-prompt-modal"', r3.get_data(as_text=True))

    def test_12_learning_loop_completion(self):
        """12. Complete learning loop: failure -> wrong notes -> wrong detail -> re-exam resolution."""
        with self.app.app_context():
            # Step 1: User fails Q-SHORT-002
            res1 = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res1, {"Q-SHORT-002": "incorrect"})

            # Step 2: Appears in wrong notes
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 1)

            # Step 3: User accesses wrong detail and follows link to concept
            detail = self.wrong_service.get_wrong_question_detail("Q-SHORT-002")
            self.assertIsNotNone(detail)
            self.assertEqual(detail["latest_status"], "incorrect")
            self.assertIsNotNone(detail["deep_explanation"])
            self.assertGreater(detail["related_questions_count"], 0)

            # Step 4: User retakes via wrong_review mode and gets it right!
            res2 = {
                "total_score": 3.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("wrong_review", None, None, res2, {"Q-SHORT-002": "correct answer"})

            # Step 5: Resolved! Active wrong count is now 0
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 0)

            # Step 6: Detailed timeline preserves both attempts
            updated_detail = self.wrong_service.get_wrong_question_detail("Q-SHORT-002")
            self.assertEqual(updated_detail["total_attempts"], 2)
            self.assertEqual(updated_detail["latest_status"], "sufficient")
            self.assertEqual(updated_detail["sufficient_count"], 1)
            self.assertEqual(updated_detail["incorrect_count"], 1)

if __name__ == "__main__":
    unittest.main()
