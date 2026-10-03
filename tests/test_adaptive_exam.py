import unittest
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.data_loader import DataLoader
from app.services.exam_generator import ExamGenerator
from app.services.exam_service import ExamService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestAdaptiveExam(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.all_questions = self.loader.get_enriched_questions()
            self.exam_service = ExamService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_wrong_review_exam_structure_and_priority(self):
        # Specific known questions from question bank
        target_wrongs = ["Q-SHORT-001", "Q-SHORT-002", "Q-DESC-001", "Q-PRAC-001"]
        exam = ExamGenerator.generate_wrong_review_exam(
            self.all_questions,
            wrong_question_ids=target_wrongs,
            seed=42
        )

        # 1. Total questions count = 18
        self.assertEqual(len(exam), 18)

        short_qs = [q for q in exam if q["type"] == "short"]
        desc_qs = [q for q in exam if q["type"] == "descriptive"]
        prac_qs = [q for q in exam if q["type"] == "practical"]

        # 2. Type breakdown
        self.assertEqual(len(short_qs), 12)
        self.assertEqual(len(desc_qs), 4)
        self.assertEqual(len(prac_qs), 2)

        # 3. 100-point structure
        self.assertEqual(sum(q["score"] for q in short_qs), 36)
        self.assertEqual(sum(q["score"] for q in desc_qs), 48)
        self.assertTrue(all(q["score"] == 16 for q in prac_qs))

        # 4. Target wrong questions must be included!
        exam_ids = [q["id"] for q in exam]
        for w_id in target_wrongs:
            self.assertIn(w_id, exam_ids, f"Wrong question {w_id} should be included in wrong review exam")

    def test_adaptive_exam_structure_and_vulnerability_weight(self):
        # Target vulnerable concepts
        target_vuln_concepts = ["CON-APP-03", "CON-NET-01"]
        exam = ExamGenerator.generate_adaptive_exam(
            self.all_questions,
            vulnerable_concept_ids=target_vuln_concepts,
            seed=123
        )

        # 1. Total questions count = 18
        self.assertEqual(len(exam), 18)

        short_qs = [q for q in exam if q["type"] == "short"]
        desc_qs = [q for q in exam if q["type"] == "descriptive"]
        prac_qs = [q for q in exam if q["type"] == "practical"]

        # 2. Type breakdown & score integrity
        self.assertEqual(len(short_qs), 12)
        self.assertEqual(len(desc_qs), 4)
        self.assertEqual(len(prac_qs), 2)
        self.assertEqual(sum(q["score"] for q in short_qs), 36)
        self.assertEqual(sum(q["score"] for q in desc_qs), 48)
        self.assertTrue(all(q["score"] == 16 for q in prac_qs))

        # 3. Vulnerable concepts must be represented
        vuln_qs = [q for q in exam if q.get("concept_id") in target_vuln_concepts]
        self.assertGreaterEqual(len(vuln_qs), 3, "Adaptive exam should include multiple questions from vulnerable concepts")

    def test_wrong_review_fallback_empty_wrong_notes(self):
        # When user has 0 wrong questions
        exam = ExamGenerator.generate_wrong_review_exam(
            self.all_questions,
            wrong_question_ids=[],
            seed=999
        )
        self.assertEqual(len(exam), 18)
        self.assertEqual(len(set(q["id"] for q in exam)), 18)

    def test_web_routes_for_adaptive_and_wrong_review(self):
        # 1. GET /exam?mode=adaptive
        resp_adap = self.client.get("/exam?mode=adaptive")
        self.assertEqual(resp_adap.status_code, 200)
        self.assertIn("취약 Concept 집중 모의고사", resp_adap.get_data(as_text=True))

        # 2. GET /exam?mode=wrong_review
        resp_wrong = self.client.get("/exam?mode=wrong_review")
        self.assertEqual(resp_wrong.status_code, 200)
        self.assertIn("오답 다시 풀기 모의고사", resp_wrong.get_data(as_text=True))
