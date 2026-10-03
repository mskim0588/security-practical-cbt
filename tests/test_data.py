import unittest
import os
import json
from app.services.data_loader import DataLoader

class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()

    def test_sources_loaded(self):
        sources = self.loader.load_sources()
        self.assertGreaterEqual(len(sources), 4)
        for s in sources:
            self.assertIn("id", s)
            self.assertIn("filename", s)
            self.assertIn("title", s)

    def test_questions_structure_and_scores(self):
        validation = self.loader.validate_dataset()
        self.assertTrue(validation["valid"], f"Validation failed: {validation}")
        self.assertEqual(validation["short_count"], 12)
        self.assertEqual(validation["short_score"], 36)
        self.assertEqual(validation["desc_count"], 4)
        self.assertEqual(validation["desc_score"], 48)
        self.assertEqual(validation["prac_count"], 2)
        self.assertEqual(validation["prac_scores"], [16, 16])
        self.assertEqual(validation["total_candidate_count"], 18)
        self.assertEqual(validation["target_graded_count"], 17)
        self.assertEqual(validation["target_total_score"], 100)

    def test_enriched_questions_have_valid_sources(self):
        enriched = self.loader.get_enriched_questions()
        self.assertGreaterEqual(len(enriched), 18)
        for q in enriched:
            self.assertIn("source_info", q)
            self.assertIn("source_page", q)
            self.assertIsInstance(q["source_page"], int)
            self.assertGreater(q["source_page"], 0)

if __name__ == "__main__":
    unittest.main()
