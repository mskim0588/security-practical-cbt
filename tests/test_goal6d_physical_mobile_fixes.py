"""Stable regressions for confirmed physical mobile findings MDEV-001 through MDEV-005."""

import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CSS_FILE = BASE_DIR / "app" / "static" / "css" / "style.css"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
DASHBOARD_ROUTES = BASE_DIR / "app" / "routes" / "dashboard_routes.py"


class TestGoal6DPhysicalMobileFixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = CSS_FILE.read_text(encoding="utf-8")
        cls.ai_modal = (TEMPLATES_DIR / "components" / "ai_prompt_modal.html").read_text(encoding="utf-8")
        cls.concepts_index = (TEMPLATES_DIR / "concepts" / "index.html").read_text(encoding="utf-8")
        cls.dashboard = (TEMPLATES_DIR / "dashboard.html").read_text(encoding="utf-8")
        cls.dashboard_routes = DASHBOARD_ROUTES.read_text(encoding="utf-8")

    def test_mdev_001_clipboard_success_and_fallback_contract(self):
        self.assertIn("window.isSecureContext", self.ai_modal)
        self.assertIn("navigator.clipboard.writeText(textarea.value)", self.ai_modal)
        self.assertIn(".catch(completeFallbackCopy)", self.ai_modal)
        self.assertIn("document.execCommand('copy') === true", self.ai_modal)
        self.assertIn("자동 복사가 지원되지 않습니다. 프롬프트를 길게 눌러 직접 복사하세요.", self.ai_modal)
        self.assertIn("selectPromptForManualCopy(textarea)", self.ai_modal)
        base_template = (TEMPLATES_DIR / "base.html").read_text(encoding="utf-8")
        self.assertEqual(base_template.count('include "components/ai_prompt_modal.html"'), 1)
        for template_name in ("history_detail.html", "wrong_detail.html", "wrong_notes.html"):
            content = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
            self.assertNotIn('include "components/ai_prompt_modal.html"', content)

    def test_mdev_002_search_layout_can_shrink_without_wrapping_button(self):
        self.assertIn('class="concept-search-field"', self.concepts_index)
        self.assertIn("grid-template-columns: minmax(0, 1fr) auto", self.css)
        self.assertIn(".concept-search-input", self.css)
        self.assertIn(".search-submit-btn", self.css)
        self.assertIn("white-space: nowrap", self.css)

    def test_mdev_003_prose_wraps_while_code_scrolls(self):
        self.assertIn(".prose-wrap", self.css)
        self.assertIn("overflow-wrap: anywhere", self.css)
        self.assertIn("white-space: pre;", self.css)
        self.assertIn("overflow-x: auto", self.css)
        for template_name in ("result.html", "history_detail.html", "wrong_detail.html"):
            content = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
            self.assertIn("prose-wrap", content)

    def test_mdev_004_dashboard_heading_uses_mobile_safe_wrapping(self):
        self.assertIn('class="dashboard-page-title"', self.dashboard)
        self.assertIn(".dashboard-page-title", self.css)
        self.assertIn("font-size: clamp(", self.css)
        self.assertIn("word-break: keep-all", self.css)

    def test_mdev_005_dynamic_dashboard_ctas_use_unicode_arrow(self):
        self.assertNotIn("&rarr;", self.dashboard_routes)
        self.assertIn("오답 집중 모의고사 시작하기 →", self.dashboard_routes)


if __name__ == "__main__":
    unittest.main()
