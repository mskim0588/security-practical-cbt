import os
import re
import unittest
from app import create_app

class TestGoal4ALayoutNavigation(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.css_path = os.path.join(self.app.root_path, "static", "css", "style.css")
        with open(self.css_path, "r", encoding="utf-8") as f:
            self.css_content = f.read()

    def test_design_tokens_presence(self):
        """Ensure all Goal 4A required Design Tokens exist in style.css."""
        # Primary colors
        for i in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
            self.assertIn(f"--primary-{i}:", self.css_content)

        # Neutral colors
        for i in [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
            self.assertIn(f"--neutral-{i}:", self.css_content)

        # Semantic status colors
        self.assertIn("--success:", self.css_content)
        self.assertIn("--warning:", self.css_content)
        self.assertIn("--danger:", self.css_content)
        self.assertIn("--info:", self.css_content)

        # Spacing scale 1 ~ 10
        for i in range(1, 11):
            self.assertIn(f"--space-{i}:", self.css_content)

        # Radius scale
        self.assertIn("--radius-sm:", self.css_content)
        self.assertIn("--radius-md:", self.css_content)
        self.assertIn("--radius-lg:", self.css_content)
        self.assertIn("--radius-full:", self.css_content)

        # Shadows
        self.assertIn("--shadow-sm:", self.css_content)
        self.assertIn("--shadow-md:", self.css_content)
        self.assertIn("--shadow-lg:", self.css_content)

        # Typography
        self.assertIn("--font-sans:", self.css_content)
        self.assertIn("--font-mono:", self.css_content)
        self.assertIn("Consolas", self.css_content)
        for s in ["xs", "sm", "base", "lg", "xl", "2xl", "3xl"]:
            self.assertIn(f"--text-{s}:", self.css_content)

        # Layout dimensions
        self.assertIn("--container-max: 1280px;", self.css_content)
        self.assertIn("--header-height:", self.css_content)
        self.assertIn("--bottom-nav-height:", self.css_content)
        self.assertIn("--touch-target-min: 44px;", self.css_content)

        # Backward compatibility aliases
        self.assertIn("--primary-color:", self.css_content)
        self.assertIn("--gray-50:", self.css_content)
        self.assertIn("--gray-900:", self.css_content)

    def test_accessibility_foundation_css(self):
        """Ensure focus-visible, skip-link, and reduced-motion are in style.css."""
        self.assertIn(":focus-visible", self.css_content)
        self.assertIn(".skip-link", self.css_content)
        self.assertIn("prefers-reduced-motion: reduce", self.css_content)

    def test_touch_target_in_mobile_nav(self):
        """Ensure touch target for mobile nav items meets 44px requirement."""
        self.assertIn("min-height: var(--touch-target-min);", self.css_content)
        self.assertIn("min-width: var(--touch-target-min);", self.css_content)

    def test_global_navigation_links_on_home(self):
        """Ensure home page renders skip-link, landmark main, desktop & mobile navs."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)

        self.assertIn('class="skip-link"', html)
        self.assertIn('id="main-content"', html)
        self.assertIn('class="nav-desktop"', html)
        self.assertIn('class="nav-mobile-bottom"', html)

        # Check all 5 menu items in desktop and mobile nav
        for path, name in [
            ("/", "홈"),
            ("/dashboard", "대시보드"),
            ("/exam", "모의고사"),
            ("/history", "응시이력"),
            ("/wrong-notes", "오답노트"),
        ]:
            self.assertIn(f'href="{path}"', html)
            self.assertIn(name, html)

        # On home, '/' should have is-active and aria-current="page"
        self.assertIn('href="/" class="nav-desktop-link is-active" aria-current="page"', html)
        self.assertIn('href="/" class="nav-mobile-item is-active" aria-current="page"', html)

    def test_active_navigation_across_pages(self):
        """Test active state styling across different pages."""
        pages = [
            ("/dashboard", 'href="/dashboard" class="nav-desktop-link is-active" aria-current="page"'),
            ("/history", 'href="/history" class="nav-desktop-link is-active" aria-current="page"'),
            ("/wrong-notes", 'href="/wrong-notes" class="nav-desktop-link is-active" aria-current="page"'),
        ]
        for url, expected_active_snippet in pages:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200)
                html = resp.get_data(as_text=True)
                self.assertIn(expected_active_snippet, html)
                self.assertIn('class="nav-mobile-bottom"', html)
                self.assertIn('has-mobile-nav', html)

    def test_exam_and_review_collision_prevention(self):
        """Ensure /exam and /review hide mobile global nav and set is-exam-session body class."""
        # 1. /exam
        resp_exam = self.client.get("/exam")
        self.assertEqual(resp_exam.status_code, 200)
        html_exam = resp_exam.get_data(as_text=True)
        self.assertIn("is-exam-session", html_exam)
        self.assertNotIn("has-mobile-nav", html_exam)
        self.assertNotIn("nav-mobile-bottom", html_exam)

        # 2. /review (POST with minimal payload)
        review_data = {
            "question_ids": "Q-SHORT-001,Q-SHORT-002,Q-DESC-001,Q-PRAC-001,Q-PRAC-002",
            "exam_mode": "standard",
            "submission_token": "token123",
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001": "test"
        }
        resp_review = self.client.post("/review", data=review_data)
        self.assertEqual(resp_review.status_code, 200)
        html_review = resp_review.get_data(as_text=True)
        self.assertIn("is-exam-session", html_review)
        self.assertNotIn("has-mobile-nav", html_review)
        self.assertNotIn("nav-mobile-bottom", html_review)

if __name__ == "__main__":
    unittest.main()
