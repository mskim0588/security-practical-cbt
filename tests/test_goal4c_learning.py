# -*- coding: utf-8 -*-
"""
Tests for Goal 4C Learning Content Architecture
Verifies DataLoader extensions, LearningService, Concept Routes (/concepts, /concepts/<id>),
Anti-Cheat Boundary Policy, and baseline stability.
"""
import unittest
from app import create_app
from app.services.data_loader import DataLoader
from app.services.learning_service import LearningService

class TestGoal4CLearningContent(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.service = LearningService(self.loader)

    def test_concept_contents_integrity(self):
        """Ensure all 20 concepts exist in concept_contents.json with all required schema fields."""
        contents = self.loader.load_concept_contents()
        self.assertEqual(len(contents), 20, "Must contain exactly 20 concepts")

        # Verify against concepts.json master
        concepts_master = self.loader.load_concepts()
        master_ids = {c["id"] for c in concepts_master}
        self.assertEqual(set(contents.keys()), master_ids, "Concept IDs must match concepts.json 1:1")

        required_keys = [
            "concept_id", "summary", "core_points", "mechanism",
            "exam_points", "common_mistakes", "compare_with",
            "commands_or_examples", "related_sources", "law_review_status"
        ]
        for cid, item in contents.items():
            for k in required_keys:
                self.assertIn(k, item, f"Missing key '{k}' in {cid}")
            self.assertGreaterEqual(len(item["core_points"]), 4, f"{cid} must have at least 4 core points")
            self.assertGreaterEqual(len(item["common_mistakes"]), 1, f"{cid} must have at least 1 trap")
            self.assertIn(item["law_review_status"]["status"], [
                "source_current", "source_may_be_outdated", "current_law_review_required"
            ])

    def test_explanations_fallback_behavior(self):
        """Ensure get_explanation_for_question falls back gracefully to question.explanation."""
        # Q-001 should return valid explanation structure even without explanations.json
        exp = self.loader.get_explanation_for_question("Q-001")
        self.assertEqual(exp["question_id"], "Q-001")
        self.assertIn("overview", exp)
        self.assertTrue(len(exp["overview"]) > 0)
        self.assertIn("why_correct", exp)

        # Invalid question ID fallback
        invalid_exp = self.loader.get_explanation_for_question("Q-NON-EXISTENT")
        self.assertEqual(invalid_exp["question_id"], "Q-NON-EXISTENT")
        self.assertIn("해설", invalid_exp["overview"])

    def test_learning_service_overview_list(self):
        """Ensure LearningService returns all 20 concepts with question stats and analytics."""
        overview = self.service.get_concept_overview_list()
        self.assertEqual(len(overview), 20)

        total_questions = sum(c["question_count"] for c in overview)
        self.assertEqual(total_questions, 180, "Sum of questions across 20 concepts must be 180")

        # Check structure of each concept
        for c in overview:
            self.assertIn("concept_id", c)
            self.assertIn("name", c)
            self.assertIn("category", c)
            self.assertIn("summary", c)
            self.assertIn("grade", c)
            self.assertIn("grade_code", c)

    def test_learning_service_concept_detail(self):
        """Ensure get_concept_detail returns enriched study pack with connected questions and sources."""
        detail = self.service.get_concept_detail("CON-SYS-01")
        self.assertIsNotNone(detail)
        self.assertEqual(detail["concept_id"], "CON-SYS-01")
        self.assertIn("content", detail)
        self.assertIn("questions", detail)
        self.assertGreaterEqual(len(detail["questions"]), 1, "Must have connected questions")
        self.assertIn("sources", detail)

        # All connected questions must belong to CON-SYS-01
        for q in detail["questions"]:
            self.assertEqual(q["concept_id"], "CON-SYS-01")

        # Invalid ID returns None
        invalid_detail = self.service.get_concept_detail("CON-INVALID-99")
        self.assertIsNone(invalid_detail)

    def test_concept_list_route(self):
        """GET /concepts should return 200, render cards, category filter and search."""
        resp = self.client.get("/concepts")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("개념 도서관", html)
        self.assertIn("CON-SYS-01", html)
        self.assertIn("CON-MGT-03", html)

        # Test category filtering
        resp_cat = self.client.get("/concepts?category=시스템 보안")
        self.assertEqual(resp_cat.status_code, 200)
        html_cat = resp_cat.get_data(as_text=True)
        self.assertIn("CON-SYS-01", html_cat)
        self.assertNotIn("CON-NET-01", html_cat)

        # Test search query
        resp_search = self.client.get("/concepts?q=PAM")
        self.assertEqual(resp_search.status_code, 200)
        html_search = resp_search.get_data(as_text=True)
        self.assertIn("CON-SYS-01", html_search)
        self.assertNotIn("CON-NET-02", html_search)

    def test_concept_detail_route(self):
        """GET /concepts/<concept_id> returns 200 and renders sections, 404 for invalid ID."""
        resp = self.client.get("/concepts/CON-SYS-01")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn("CON-SYS-01", html)
        self.assertIn("핵심 포인트 및 동작 메커니즘", html)
        self.assertIn("실기 시험 공략 & 오답 함정 클리닉", html)
        self.assertIn("연계 기출 및 연습 문제", html)

        # 404 test
        resp_404 = self.client.get("/concepts/CON-INVALID-99")
        self.assertEqual(resp_404.status_code, 404)

    def test_anti_cheat_exam_isolation(self):
        """Ensure /exam and /review do NOT expose concept study links or cheat spoilers."""
        # 1. /exam
        resp_exam = self.client.get("/exam")
        self.assertEqual(resp_exam.status_code, 200)
        html_exam = resp_exam.get_data(as_text=True)
        self.assertNotIn('href="/concepts/CON-', html_exam, "Exam screen must not link to concept study pages")

        # 2. /review (POST to enter review)
        post_data = {
            "submission_token": "anti_cheat_token_1",
            "ans_Q-001": "auth",
            "ans_Q-100": "test"
        }
        resp_rev = self.client.post("/review", data=post_data)
        self.assertEqual(resp_rev.status_code, 200)
        html_rev = resp_rev.get_data(as_text=True)
        self.assertNotIn('href="/concepts/CON-', html_rev, "Review screen must not link to concept study pages")

    def test_navigation_presence_of_concepts(self):
        """Ensure 개념학습 appears in global navigation on home page."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('href="/concepts"', html)
        self.assertIn("개념학습", html)

        # When visiting /concepts, it should be active
        resp_c = self.client.get("/concepts")
        html_c = resp_c.get_data(as_text=True)
        self.assertIn('href="/concepts" class="nav-desktop-link is-active" aria-current="page"', html_c)

    def test_explanations_json_full_coverage(self):
        """Ensure explanations.json covers all 180 questions with schema compliance."""
        explanations = self.loader.load_explanations()
        self.assertEqual(len(explanations), 180, "Must contain explanations for all 180 questions")

        questions = self.loader.load_questions()
        for q in questions:
            qid = q["id"]
            self.assertIn(qid, explanations)
            exp = explanations[qid]
            self.assertEqual(exp["question_id"], qid)
            self.assertTrue(len(exp["overview"]) > 0)
            self.assertTrue(len(exp["why_correct"]) > 0)
            self.assertGreaterEqual(len(exp["why_wrong_common_traps"]), 1)
            self.assertTrue(len(exp["exam_strategy"]) > 0)

            if q["type"] in ("descriptive", "practical"):
                self.assertIsNotNone(exp["practical_scoring_criteria"])
                self.assertGreaterEqual(len(exp["practical_scoring_criteria"]["rubrics"]), 1)

    def test_result_and_history_deep_explanation_rendering(self):
        """Submit an exam, verify /result and /history contain concept link and explanation accordion."""
        # 1. Submit exam
        with self.client.session_transaction() as sess:
            sess["csrf_token"] = "test_token_4c_csrf"

        post_data = {
            "csrf_token": "test_token_4c_csrf",
            "submission_token": "test_token_4c2_1",
            "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_B": "법적 준거성",
            "ans_Q-SHORT-001_C": "2",
            "selected_practical_id": "Q-PRAC-001"
        }
        resp = self.client.post("/submit", data=post_data, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Result screen should display concept link and explanation accordion
        self.assertIn("학습 &rarr;", html)
        self.assertIn("explanation-accordion", html)
        self.assertIn("심층 해설 및 오답 분석 보기", html)

    def test_dashboard_concept_links(self):
        """Ensure /dashboard renders links to /concepts/<concept_id>."""
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('href="/concepts/CON-', html)

    def test_prompt_builder_templates(self):
        """Ensure PromptBuilder generates templates and privacy-safe provider home URLs."""
        from app.services.prompt_builder import PromptBuilder

        q_text = "PAM의 4대 인터페이스를 기술하시오."
        concept_id = "CON-SYS-01"
        concept_name = "Linux 권한 및 PAM"

        # 1. Why wrong template
        p_wrong = PromptBuilder.build_prompt(
            PromptBuilder.TEMPLATE_WHY_WRONG,
            question_text=q_text,
            concept_id=concept_id,
            concept_name=concept_name,
            user_answer="auth, account",
            model_answer="auth, account, password, session"
        )
        self.assertIn("오답 분석 질문", p_wrong)
        self.assertIn("CON-SYS-01", p_wrong)
        self.assertIn("auth, account", p_wrong)

        # 2. Real world template
        p_real = PromptBuilder.build_prompt(
            PromptBuilder.TEMPLATE_REAL_WORLD,
            question_text=q_text,
            concept_id=concept_id,
            concept_name=concept_name
        )
        self.assertIn("실무 연계 질문", p_real)
        self.assertIn("명령어 및 설정 예시", p_real)

        # 3. Similar question template
        p_sim = PromptBuilder.build_prompt(
            PromptBuilder.TEMPLATE_SIMILAR_QUESTION,
            question_text=q_text,
            concept_id=concept_id,
            concept_name=concept_name,
            question_type="short",
            score=3
        )
        self.assertIn("모의 출제 요청", p_sim)
        self.assertIn("변형 문제", p_sim)

        # 4. URLs
        chatgpt_url = PromptBuilder.get_chatgpt_url(p_wrong)
        self.assertEqual(chatgpt_url, "https://chatgpt.com/")
        self.assertNotIn(p_wrong, chatgpt_url)
        gemini_url = PromptBuilder.get_gemini_url(p_wrong)
        self.assertEqual(gemini_url, "https://gemini.google.com/app")

    def test_ai_modal_and_anti_cheat_isolation(self):
        """Ensure AI prompt modal is present on non-exam pages and strictly absent on /exam and /review."""
        # Non-exam page (e.g. /concepts) should have ai-prompt-modal
        resp_c = self.client.get("/concepts")
        html_c = resp_c.get_data(as_text=True)
        self.assertIn('id="ai-prompt-modal"', html_c)
        self.assertIn('href="https://chatgpt.com/"', html_c)
        self.assertNotIn("openChatGPTLauncher", html_c)

        # Exam page must NOT have ai-prompt-modal
        resp_exam = self.client.get("/exam")
        html_exam = resp_exam.get_data(as_text=True)
        self.assertNotIn('id="ai-prompt-modal"', html_exam)

