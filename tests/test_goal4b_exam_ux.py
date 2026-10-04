import os
import re
import unittest
from app import create_app

class TestGoal4BExamUX(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.css_path = os.path.join(self.app.root_path, "static", "css", "style.css")
        with open(self.css_path, "r", encoding="utf-8") as f:
            self.css_content = f.read()

    def test_exam_form_fields_integrity(self):
        """1 & 2 & 3: Ensure submission_token, selected_practical_id, and 2 practical candidates exist."""
        resp = self.client.get("/exam")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # 1. submission_token hidden input
        token_match = re.search(r'name="submission_token"\s+value="([^"]+)"', html)
        self.assertIsNotNone(token_match, "submission_token hidden input must exist on /exam")
        self.assertTrue(len(token_match.group(1).strip()) > 0)

        # 2. practical radio buttons
        radios = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"', html)
        self.assertEqual(len(radios), 2, "Exactly 2 practical options must be present")

        # 3. Practical question cards
        practical_cards = re.findall(r'class="question-card practical-card"\s+id="q-([^"]+)"', html)
        self.assertEqual(len(practical_cards), 2, "2 practical cards must be rendered")
        self.assertEqual(radios, practical_cards, "Radio values must match practical card IDs")

    def test_exam_navigation_and_sheet_markup(self):
        """4 & 5 & 6: Ensure desktop sidebar, mobile action bar, and question sheet drawer exist."""
        resp = self.client.get("/exam")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # 4. Global Mobile Bottom Nav should NOT be rendered in exam session
        self.assertNotIn('class="nav-mobile-bottom"', html, "Global mobile nav must be hidden on /exam")
        self.assertIn("is-exam-session", html)

        # 5. Mobile dedicated bottom action bar markup
        self.assertIn('class="mobile-exam-action-bar"', html)
        self.assertIn('id="btn-mobile-sheet-open"', html)
        self.assertIn('id="mobile-progress-count"', html)

        # 6. Question Navigator markup (desktop sidebar and mobile sheet)
        self.assertIn('class="exam-sidebar"', html)
        self.assertIn('id="mobile-question-sheet"', html)
        self.assertIn('role="dialog"', html)
        self.assertIn('id="btn-mobile-sheet-close"', html)

        # Desktop nav buttons (18 buttons)
        nav_targets = re.findall(r'class="nav-btn[^"]*"\s+data-target="([^"]+)"', html)
        self.assertEqual(len(nav_targets), 18, "Desktop sidebar must have 18 question buttons")

        # Sheet drawer buttons (18 buttons)
        sheet_targets = re.findall(r'class="sheet-btn[^"]*"\s+data-target="([^"]+)"', html)
        self.assertEqual(len(sheet_targets), 18, "Mobile sheet must have 18 question buttons")

    def test_input_and_textarea_label_associations(self):
        """7. Ensure every input, textarea, and practical radio has an associated label."""
        resp = self.client.get("/exam")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Check inputs have id and label for
        inputs = re.findall(r'<input\s+type="text"\s+id="([^"]+)"', html)
        self.assertTrue(len(inputs) >= 12, "Must have text inputs for short questions")
        for inp_id in inputs:
            self.assertIn(f'for="{inp_id}"', html, f"Input id '{inp_id}' must have a matching label for")

        # Check textareas have id and label for
        textareas = re.findall(r'<textarea\s+id="([^"]+)"', html)
        self.assertTrue(len(textareas) >= 4, "Must have textareas for descriptive/practical questions")
        for txt_id in textareas:
            self.assertIn(f'for="{txt_id}"', html, f"Textarea id '{txt_id}' must have a matching label for")

        # Check practical radios have id and label for
        prac_radios = re.findall(r'<input\s+type="radio"\s+id="([^"]+)"', html)
        self.assertEqual(len(prac_radios), 2)
        for r_id in prac_radios:
            self.assertIn(f'for="{r_id}"', html, f"Radio id '{r_id}' must have a matching label for")

    def test_review_flow_and_kpis(self):
        """9. Ensure review POST returns 200, summary KPIs, and retains submission_token."""
        review_payload = {
            "question_ids": "Q-SHORT-001,Q-SHORT-002,Q-DESC-001,Q-PRAC-001,Q-PRAC-002",
            "exam_mode": "standard",
            "submission_token": "token_test_4b",
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001": "test_answer"
        }
        resp = self.client.post("/review", data=review_payload)
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Verification of Review content
        self.assertIn("답안 최종 검토", html)
        self.assertIn("17문항", html)
        self.assertIn("작성 완료", html)
        self.assertIn("미완료 문항", html)
        self.assertIn("실무형 선택", html)
        self.assertIn("17번 (IPTables) 선택됨", html)

        # Ensure submission_token is preserved in hidden inputs
        self.assertIn('name="submission_token" value="token_test_4b"', html)

        # Ensure Global Bottom Nav is hidden in review session
        self.assertNotIn('class="nav-mobile-bottom"', html)

    def test_result_page_hierarchy_and_filters(self):
        """8. Ensure result page GET returns 200, displays total score first, and has filter tabs."""
        with self.client.session_transaction() as sess:
            sess["csrf_token"] = "test-token-4b"

        submit_payload = {
            "csrf_token": "test-token-4b",
            "selected_practical_id": "Q-PRAC-001",
            "submission_token": "token_result_test",
            "exam_mode": "standard",
            "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_B": "법적 준거성",
            "ans_Q-SHORT-001_C": "2"
        }
        resp = self.client.post("/submit", data=submit_payload, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        # Score & pass status
        self.assertIn("정보보안기사 실기 모의고사 채점 결과", html)
        self.assertIn("/ 100점", html)
        self.assertIn("단답형 (12문항)", html)
        self.assertIn("서술형 (4문항)", html)
        self.assertIn("실무형 (선택 1문항)", html)

        # Filter bar
        self.assertIn('class="result-filter-bar"', html)
        self.assertIn('data-filter="all"', html)
        self.assertIn('data-filter="short"', html)
        self.assertIn('data-filter="descriptive"', html)
        self.assertIn('data-filter="practical"', html)
        self.assertIn('data-filter="incorrect"', html)

        # Source badge
        self.assertIn("출처:", html)
        self.assertIn("Page", html)

        # Action CTAs
        self.assertIn("/history", html)
        self.assertIn("/wrong-notes", html)
        self.assertIn("/dashboard", html)
        self.assertIn("/exam", html)

    def test_code_and_log_classes_presence(self):
        """10. Ensure .code-terminal, .code-block, and .log-block exist with horizontal scroll rules."""
        self.assertIn(".code-terminal", self.css_content)
        self.assertIn(".code-block", self.css_content)
        self.assertIn(".log-block", self.css_content)
        self.assertIn("font-family: var(--font-mono);", self.css_content)
        self.assertIn("overflow-x: auto;", self.css_content)
        self.assertIn("white-space: pre;", self.css_content)

if __name__ == "__main__":
    unittest.main()
