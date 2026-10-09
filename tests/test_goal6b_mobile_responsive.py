"""
Goal 6B: Automated Mobile Responsive & Layout Integrity Regression Tests
Verifies the presence and correctness of mobile UI polish fixes (MOB-001 ~ MOB-008)
without brittle dependency on volatile CSS properties.
"""

import os
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_FILE = BASE_DIR / "app" / "static" / "css" / "style.css"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"


class TestGoal6BMobileResponsive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            cls.css_content = f.read()

    def test_mob_001_exam_grid_min_width_safety(self):
        """MOB-001: .exam-container and .exam-main prevent unconstrained grid track expansion."""
        self.assertIn("minmax(0, 1fr)", self.css_content, "CSS should contain minmax(0, 1fr) for grid safety")
        self.assertIn(".exam-main", self.css_content)
        self.assertIn("min-width: 0", self.css_content, ".exam-main should declare min-width: 0")

    def test_mob_002_bottom_nav_compact_grid(self):
        """MOB-002: Goal 9A uses four Guest and five Owner mobile destinations."""
        self.assertIn("repeat(4, minmax(0, 1fr))", self.css_content)
        self.assertIn("repeat(5, minmax(0, 1fr))", self.css_content)
        self.assertIn(".nav-mobile-label", self.css_content)

    def test_mob_003_dashboard_responsive_class(self):
        """MOB-003: dashboard.html uses .dashboard-analysis-grid instead of fixed inline minmax(460px, 1fr)."""
        dashboard_tpl = (TEMPLATES_DIR / "dashboard.html").read_text(encoding="utf-8")
        self.assertIn("dashboard-analysis-grid", dashboard_tpl, "dashboard.html must use dashboard-analysis-grid")
        self.assertNotIn("minmax(460px, 1fr)", dashboard_tpl, "dashboard.html must not contain inline minmax(460px, 1fr)")
        self.assertIn(".dashboard-analysis-grid", self.css_content)

    def test_mob_004_ios_input_font_size(self):
        """MOB-004: Inputs and textareas enforce minimum 16px font-size below 768px to prevent iOS auto-zoom."""
        self.assertIn("font-size: 16px !important", self.css_content, "Mobile inputs must enforce 16px font-size")

    def test_mob_005_history_and_review_mobile_cards(self):
        """MOB-005: /history and /review provide mobile card alternatives while preserving desktop tables."""
        history_tpl = (TEMPLATES_DIR / "history_list.html").read_text(encoding="utf-8")
        self.assertIn("history-table-wrapper", history_tpl, "history_list.html must retain desktop table wrapper")
        self.assertIn("history-cards-list", history_tpl, "history_list.html must provide mobile cards list")

        review_tpl = (TEMPLATES_DIR / "review.html").read_text(encoding="utf-8")
        self.assertIn("review-table-wrapper", review_tpl, "review.html must retain desktop table wrapper")
        self.assertIn("review-cards-list", review_tpl, "review.html must provide mobile cards list")

        self.assertIn(".history-table-wrapper", self.css_content)
        self.assertIn(".history-cards-list", self.css_content)
        self.assertIn(".review-table-wrapper", self.css_content)
        self.assertIn(".review-cards-list", self.css_content)

    def test_mob_006_header_actions_compact_presentation(self):
        """MOB-006: Header action buttons support wrapping and compact text on small viewports."""
        wrong_detail_tpl = (TEMPLATES_DIR / "wrong_detail.html").read_text(encoding="utf-8")
        self.assertIn("header-action-btn", wrong_detail_tpl)
        self.assertIn("header-btn-full", wrong_detail_tpl)
        self.assertIn(".header-actions", self.css_content)

    def test_mob_007_mobile_touch_targets(self):
        """MOB-007: Touch targets ensure >= 44px tap areas on mobile viewports."""
        self.assertIn("min-height: 44px", self.css_content)
        self.assertIn(".practical-radio-label", self.css_content)

    def test_mob_008_ai_modal_responsive_constraints(self):
        """MOB-008: AI modal enforces max-width calc(100vw - 32px) and safe margins."""
        self.assertIn("calc(100vw - 32px)", self.css_content, "AI modal must constrain max-width with 16px gutters")


if __name__ == "__main__":
    unittest.main()
