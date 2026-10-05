import html as html_module
import json
import re
import unittest
from pathlib import Path

from app import create_app
from app.config import Config
from app.models.database import close_db, init_db
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class TestGoal6DPreFinalAIHistory(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(self.loader)
            grading_result = {
                "total_score": 4.0,
                "is_passed": False,
                "summary": {
                    "short": {"earned": 1.0},
                    "descriptive": {"earned": 3.0},
                    "practical": {"earned": 0.0},
                },
                "details": [
                    {
                        "question_id": "Q-SHORT-001",
                        "type": "short",
                        "earned_score": 1.0,
                        "max_score": 3.0,
                    },
                    {
                        "question_id": "Q-DESC-001",
                        "type": "descriptive",
                        "earned_score": 3.0,
                        "max_score": 12.0,
                        "sub_results": [
                            {
                                "sub_id": 1,
                                "prompt": "요청 파라미터 의미",
                                "earned_score": 3.0,
                                "max_score": 4.0,
                                "matched_keywords": ["no", "101"],
                                "missing_keywords": ["item", "book"],
                            }
                        ],
                    },
                ],
            }
            attempt = self.history_service.save_exam_attempt(
                exam_mode="standard",
                seed=6,
                selected_practical_id=None,
                grading_result=grading_result,
                answers={
                    "Q-SHORT-001": {"A": "발생 가능성", "B": "", "C": "2"},
                    "Q-DESC-001": "no=101만 설명",
                },
            )
            self.attempt_id = attempt.id

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_ai_helper_is_local_private_and_accessible(self):
        modal = (TEMPLATES_DIR / "components" / "ai_prompt_modal.html").read_text(encoding="utf-8")
        self.assertIn("ChatGPT용 프롬프트", modal)
        self.assertIn("Gemini용 프롬프트", modal)
        self.assertIn("프롬프트 복사", modal)
        self.assertIn("프롬프트는 이 사이트에서만 생성되며 외부 AI에 자동 전송되지 않습니다.", modal)
        self.assertIn('href="https://chatgpt.com/"', modal)
        self.assertIn('href="https://gemini.google.com/app"', modal)
        self.assertGreaterEqual(modal.count('target="_blank"'), 2)
        self.assertGreaterEqual(modal.count('rel="noopener noreferrer"'), 2)
        self.assertIn('aria-label="생성된 학습 프롬프트"', modal)
        self.assertIn("navigator.clipboard.writeText(textarea.value)", modal)
        self.assertIn("document.execCommand('copy') === true", modal)
        self.assertIn("프롬프트를 복사했습니다.", modal)
        self.assertIn("자동 복사가 지원되지 않습니다. 프롬프트를 길게 눌러 직접 복사하세요.", modal)
        for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "chatgpt.com/?", "?q=", "?prompt=", "?text="):
            self.assertNotIn(forbidden, modal)
        for private_field in (
            "SECRET_KEY",
            "ADMIN_ACCESS_KEY",
            "DATABASE_URL",
            "csrf_token",
            "session cookie",
            "source_info",
            "source_type",
            "total_pages",
            "filename",
        ):
            self.assertNotIn(private_field, modal)

    def test_ai_helper_remains_absent_from_exam_and_review(self):
        exam_html = self.client.get("/exam").get_data(as_text=True)
        review_html = self.client.get("/review").get_data(as_text=True)
        self.assertNotIn('id="ai-prompt-modal"', exam_html)
        self.assertNotIn('id="ai-prompt-modal"', review_html)

    def test_history_renders_canonical_explanation_and_learning_flow(self):
        html = html_module.unescape(self.client.get(f"/history/{self.attempt_id}").get_data(as_text=True))
        explanation = self.loader.get_explanation_for_question("Q-DESC-001")
        question = self.loader.get_question_by_id("Q-DESC-001")
        self.assertIn(question["model_answer"], html)
        self.assertIn("채점 기준 및 부분 점수 루브릭", html)
        self.assertIn(explanation["overview"], html)
        self.assertIn(explanation["why_correct"], html)
        self.assertIn("개념 상세 학습서", html)
        self.assertIn("AI 질문 프롬프트 생성", html)
        self.assertIn('class="explanation-accordion"', html)
        self.assertIn(" open>", html)

    def test_ai_helper_trigger_contains_valid_local_context_json(self):
        html = self.client.get(f"/history/{self.attempt_id}").get_data(as_text=True)
        match = re.search(r"data-ai-context='([^']+)'", html)
        self.assertIsNotNone(match)
        context = json.loads(html_module.unescape(match.group(1)))
        self.assertEqual(context["qid"], "Q-SHORT-001")
        self.assertIn("question_text", context)
        self.assertIn("model_answer", context)
        self.assertIn("user_answer", context)
        self.assertNotIn("source_info", context)
        self.assertIn('onclick="openAIPromptModal(JSON.parse(this.dataset.aiContext))"', html)

    def test_history_hides_raw_source_registry_but_preserves_internal_data(self):
        html = self.client.get(f"/history/{self.attempt_id}").get_data(as_text=True)
        question = self.loader.get_question_by_id("Q-SHORT-001")
        source = question["source_info"]
        self.assertTrue(source["filename"])
        self.assertTrue(source["source_type"])
        self.assertNotIn(source["filename"], html)
        for registry_key in ("source_type", "priority", "total_pages", "'filename'", "&#39;filename&#39;"):
            self.assertNotIn(registry_key, html)
        history_template = (TEMPLATES_DIR / "history_detail.html").read_text(encoding="utf-8")
        self.assertNotIn("{{ ans.source_info }}", history_template)

    def test_multi_answer_values_are_compact_and_empty_values_do_not_allocate_rows(self):
        html = self.client.get(f"/history/{self.attempt_id}").get_data(as_text=True)
        for label, value in (("A", "침해요인 발생 가능성"), ("B", "법적 준거성"), ("C", "2")):
            self.assertIn(f"[{label}]", html)
            self.assertIn(value, html)
        history_template = (TEMPLATES_DIR / "history_detail.html").read_text(encoding="utf-8")
        self.assertIn("sub.answer or sub.expected or sub.model_answer", history_template)
        self.assertIn("accepted-answer-list", history_template)
        self.assertNotIn('white-space: pre-wrap; min-height: 40px;">\n          {% if ans.sub_questions %}', history_template)


if __name__ == "__main__":
    unittest.main()
