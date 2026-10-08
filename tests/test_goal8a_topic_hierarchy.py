# -*- coding: utf-8 -*-
import hashlib
import os
import unittest
from collections import Counter

from app import create_app
from app.config import Config
from app.models.database import close_db, init_db
from app.services.analytics_service import AnalyticsService
from app.services.data_loader import DataLoader
from app.services.exam_generator import ExamGenerator
from app.services.learning_service import LearningService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class TestGoal8ATopicHierarchy(unittest.TestCase):
    EXPECTED_HASHES = {
        "questions.json": "661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9",
        "concepts.json": "d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943",
        "sources.json": "9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21",
        "concept_contents.json": "025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171",
        "explanations.json": "e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696",
    }

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.service = LearningService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_01_topic_schema_ids_names_parents_and_categories(self):
        concepts = self.loader.load_concepts()
        topics = self.loader.load_topics()
        concept_map = {item["id"]: item for item in concepts}
        topic_ids = [item["topic_id"] for item in topics]
        topic_names = [item["name"] for item in topics]

        self.assertEqual(len(concepts), 20)
        self.assertEqual(len(topics), 67)
        self.assertEqual(len(topic_ids), len(set(topic_ids)))
        self.assertEqual(len(topic_names), len(set(topic_names)))
        for topic in topics:
            self.assertTrue(topic["name"].strip())
            self.assertTrue(topic["summary"].strip())
            self.assertIn(topic["parent_concept_id"], concept_map)
            self.assertEqual(
                topic["category"],
                concept_map[topic["parent_concept_id"]]["category"],
            )
            self.assertGreaterEqual(topic["display_order"], 1)

    def test_02_question_topic_mapping_full_coverage_and_integrity(self):
        concepts = {item["id"]: item for item in self.loader.load_concepts()}
        questions = {item["id"]: item for item in self.loader.load_questions()}
        topics = {item["topic_id"]: item for item in self.loader.load_topics()}
        mappings = self.loader.load_question_topics()
        mapped_question_ids = [item["question_id"] for item in mappings]

        self.assertEqual(len(questions), 180)
        self.assertEqual(len(mappings), 180)
        self.assertEqual(len(mapped_question_ids), len(set(mapped_question_ids)))
        self.assertEqual(set(mapped_question_ids), set(questions))
        for mapping in mappings:
            self.assertIn(mapping["question_id"], questions)
            self.assertIn(mapping["topic_id"], topics)
            question = questions[mapping["question_id"]]
            topic = topics[mapping["topic_id"]]
            self.assertIn(topic["parent_concept_id"], concepts)
            self.assertEqual(question["concept_id"], topic["parent_concept_id"])

    def test_03_no_zero_question_topics_and_distribution_is_bounded(self):
        topics = self.loader.load_topics()
        mappings = self.loader.load_question_topics()
        counts = Counter(item["topic_id"] for item in mappings)

        self.assertFalse([item["topic_id"] for item in topics if counts[item["topic_id"]] == 0])
        self.assertLessEqual(max(counts.values()), 6)

    def test_04_concept_and_topic_service_views(self):
        overview = self.service.get_concept_overview_list()
        self.assertEqual(len(overview), 20)
        self.assertEqual(sum(item["topic_count"] for item in overview), 67)
        self.assertEqual(sum(item["question_count"] for item in overview), 180)

        concept = self.service.get_concept_detail("CON-SYS-01")
        self.assertEqual(len(concept["topics"]), 8)
        self.assertEqual(sum(item["question_count"] for item in concept["topics"]), 31)
        self.assertTrue(all(item.get("topic_id") for item in concept["questions"]))

        topic = self.service.get_topic_detail("TOP-APP-01-02")
        self.assertEqual(topic["parent_concept_id"], "CON-APP-01")
        self.assertEqual({item["id"] for item in topic["questions"]}, {"Q-DESC-004", "Q-PRAC-020"})
        self.assertIsNone(self.service.get_topic_detail("TOP-INVALID-99"))

    def test_05_concept_and_topic_routes_render_html(self):
        index = self.client.get("/concepts")
        concept = self.client.get("/concepts/CON-APP-01")
        topic = self.client.get("/topics/TOP-APP-01-02")

        self.assertEqual(index.status_code, 200)
        self.assertEqual(concept.status_code, 200)
        self.assertEqual(topic.status_code, 200)
        self.assertIn("Topic <strong>8</strong>개", index.get_data(as_text=True))
        concept_html = concept.get_data(as_text=True)
        self.assertIn("세부 Topic", concept_html)
        self.assertIn("/topics/TOP-APP-01-02", concept_html)
        topic_html = topic.get_data(as_text=True)
        self.assertIn("SQL 인젝션", topic_html)
        self.assertIn("CON-APP-01", topic_html)
        self.assertIn("Q-DESC-004", topic_html)
        self.assertIn("Q-PRAC-020", topic_html)
        self.assertIn("#question-Q-DESC-004", topic_html)
        self.assertNotIn("{'topic_id'", topic_html)
        self.assertNotIn('"parent_concept_id"', topic_html)

    def test_06_invalid_topic_id_uses_html_404(self):
        response = self.client.get("/topics/TOP-INVALID-99")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("404", html)
        self.assertNotIn("{'topic_id'", html)

    def test_07_analytics_and_adaptive_selection_remain_concept_based(self):
        with self.app.app_context():
            analytics = AnalyticsService(self.loader).get_concept_analytics()
        self.assertEqual(len(analytics), 20)
        self.assertEqual(
            {item["concept_id"] for item in analytics},
            {item["id"] for item in self.loader.load_concepts()},
        )

        adaptive = ExamGenerator.generate_exam_set(
            self.loader.load_questions(),
            mode="adaptive",
            vulnerable_concept_ids=["CON-APP-01"],
            seed=808,
        )
        self.assertEqual(len(adaptive), 18)
        self.assertGreaterEqual(sum(item["concept_id"] == "CON-APP-01" for item in adaptive), 3)
        self.assertTrue(all("topic_id" not in item for item in adaptive))

    def test_08_active_assessment_surfaces_do_not_expose_topic_help(self):
        for path in ("/exam", "/mock-exam", "/descriptive-training"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertNotIn('href="/topics/', html)
                self.assertNotIn("Topic 요약", html)

    def test_09_protected_core_hashes_and_question_concepts_are_unchanged(self):
        for filename, expected_digest in self.EXPECTED_HASHES.items():
            with open(os.path.join(self.loader.data_dir, filename), "rb") as handle:
                self.assertEqual(hashlib.sha256(handle.read()).hexdigest(), expected_digest)

        concepts = {item["id"] for item in self.loader.load_concepts()}
        self.assertEqual(len(concepts), 20)
        self.assertTrue(all(item["concept_id"] in concepts for item in self.loader.load_questions()))


if __name__ == "__main__":
    unittest.main()
