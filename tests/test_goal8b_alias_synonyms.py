import hashlib
import os
import unittest
from collections import Counter

from app import create_app
from app.config import Config
from app.models.database import close_db, init_db
from app.services.alias_service import AliasService, normalize_alias
from app.services.data_loader import DataLoader
from app.services.learning_service import LearningService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class Goal8BAliasTests(unittest.TestCase):
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
        self.aliases = AliasService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_inventory_schema_and_valid_targets(self):
        records = self.loader.load_aliases()
        self.assertEqual(len(records), 39)
        self.assertEqual(len({a["alias_id"] for a in records}), len(records))
        self.assertEqual(self.aliases.audit["invalid_records"], [])
        self.assertEqual(self.aliases.audit["duplicate_ids"], [])
        self.assertEqual(self.aliases.audit["exact_duplicates"], [])
        self.assertEqual(self.aliases.audit["normalized_duplicates"], [])
        self.assertEqual(self.aliases.audit["canonical_name_collisions"], [])
        self.assertEqual(self.aliases.audit["cross_target_collisions"], [])
        self.assertEqual(set(Counter(a["alias_type"] for a in records)),
                         {"ko_alt", "en_full", "acronym", "synonym"})

    def test_normalization_and_unique_resolution(self):
        self.assertEqual(normalize_alias("  SQLi\t  "), "sqli")
        self.assertEqual(normalize_alias("A  B"), normalize_alias("A\tB"))
        self.assertEqual(normalize_alias("e\u0301"), normalize_alias("é"))
        self.assertEqual(normalize_alias("SQL-Injection"), "sql-injection")
        self.assertEqual(self.aliases.resolve("  sQlI  ")[0]["target_id"], "TOP-APP-01-02")
        self.assertEqual(self.aliases.resolve(" SQL   Injection ")[0]["target_id"], "TOP-APP-01-02")
        self.assertEqual(self.aliases.resolve("SQL 인젝션")[0]["target_id"], "TOP-APP-01-02")
        self.assertEqual(self.aliases.resolve("unlisted alias"), [])
        synthetic = dict(self.loader.load_aliases()[0], alias_id="SYNTH-U", alias="Café")
        self.assertEqual(
            AliasService(self.loader, aliases=[synthetic]).resolve("Cafe\u0301")[0]["target_id"],
            "CON-NET-02",
        )

    def test_ambiguity_is_not_first_match_wins(self):
        extra = dict(self.loader.load_aliases()[0])
        extra.update(alias_id="SYNTH-1", target_id="CON-NET-03", alias="shared term")
        other = dict(extra, alias_id="SYNTH-2", target_id="CON-NET-02")
        service = AliasService(self.loader, aliases=[extra, other])
        self.assertEqual(len(service.resolve("SHARED  TERM")), 2)
        self.assertEqual(service.audit["cross_target_collisions"][0]["classification"],
                         "SAFE_DISAMBIGUATION_REQUIRED")

    def test_invalid_records_duplicates_and_canonical_collision_rejected(self):
        valid = dict(self.loader.load_aliases()[0])
        bad_target = dict(valid, alias_id="BAD-1", target_id="CON-NOT-REAL")
        with self.assertRaises(ValueError):
            AliasService(self.loader, aliases=[bad_target])
        bad_language = dict(valid, alias_id="BAD-2", language="xx")
        with self.assertRaises(ValueError):
            AliasService(self.loader, aliases=[bad_language])
        for change in ({"alias_type": "related"}, {"alias": "  "}, {"target_type": "question"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                AliasService(self.loader, aliases=[dict(valid, alias_id="BAD-X", **change)])
        with self.assertRaises(ValueError):
            AliasService(self.loader, aliases=[valid, dict(valid)])
        duplicate = dict(valid, alias_id="BAD-3", alias="  무선 LAN 보안 및 네트워크 인증  ")
        audit = AliasService.audit_inventory([valid, duplicate], self.aliases.targets)
        self.assertEqual(len(audit["normalized_duplicates"]), 1)
        with self.assertRaises(ValueError):
            AliasService(self.loader, aliases=[valid, duplicate])
        exact = dict(valid, alias_id="BAD-4")
        self.assertEqual(len(AliasService.audit_inventory([valid, exact], self.aliases.targets)["exact_duplicates"]), 1)
        other_name = self.aliases.targets[("concept", "CON-APP-01")]
        misleading = dict(valid, alias_id="BAD-5", alias=other_name)
        audit = AliasService.audit_inventory([misleading], self.aliases.targets)
        self.assertEqual(len(audit["canonical_name_collisions"]), 1)
        with self.assertRaises(ValueError):
            AliasService(self.loader, aliases=[misleading])

    def test_related_terms_remain_distinct(self):
        # The actual Topic IDs cover distinct detection and prevention, and
        # authentication versus access control, without claiming equivalence.
        self.assertEqual(self.aliases.resolve("IDS"), [])
        self.assertEqual(self.aliases.resolve("IPS"), [])
        self.assertEqual(self.aliases.resolve("IDS Rules and Detection Methods")[0]["target_id"],
                         "TOP-NET-01-06")
        self.assertEqual(self.aliases.group_for_target("topic", "TOP-NET-04-03")["en_full"], [])
        self.assertEqual(self.aliases.resolve("authentication"), [])
        self.assertEqual(self.aliases.resolve("authorization"), [])
        self.assertEqual(self.aliases.resolve("Windows Authentication and SID")[0]["target_id"],
                         "TOP-SYS-02-01")
        self.assertEqual(self.aliases.resolve("접근 제어 모델과 특수 권한")[0]["target_id"],
                         "TOP-SYS-01-05")

    def test_detail_ui_and_active_assessment_boundary(self):
        concept = self.client.get("/concepts/CON-MGT-04")
        topic = self.client.get("/topics/TOP-APP-01-02")
        self.assertEqual(concept.status_code, 200)
        self.assertEqual(topic.status_code, 200)
        concept_html = concept.get_data(as_text=True)
        topic_html = topic.get_data(as_text=True)
        self.assertIn("Business Continuity Management and Disaster Recovery", concept_html)
        self.assertIn("사업 연속성 관리 및 재해복구", concept_html)
        self.assertIn("SQL Injection", topic_html)
        self.assertIn("SQLi", topic_html)
        self.assertIn("learning-aliases", topic_html)
        self.assertIn("영문", topic_html)
        self.assertIn("약어", topic_html)
        self.assertIn("다른 이름", topic_html)
        self.assertNotIn("alias_id", topic_html)
        self.assertNotIn("target_id", topic_html)
        self.assertEqual(self.client.get("/topics/TOP-NOT-REAL").status_code, 404)
        for path in ("/exam", "/mock-exam", "/descriptive-training"):
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                self.assertNotIn("learning-aliases", html)

    def test_invalid_alias_target_does_not_crash_learning_detail(self):
        loader = DataLoader(self.app.config["DATA_DIR"])
        loader._aliases = [dict(self.loader.load_aliases()[0], target_id="CON-NOT-REAL")]
        with self.assertLogs("app.services.learning_service", level="ERROR"):
            detail = LearningService(loader).get_topic_detail("TOP-APP-01-02")
        self.assertEqual(detail["aliases"], {
            "ko_alt": [], "en_full": [], "acronym": [], "synonym": [],
        })

    def test_goal8a_and_core_preservation(self):
        concepts = {c["id"] for c in self.loader.load_concepts()}
        topics = {t["topic_id"]: t for t in self.loader.load_topics()}
        questions = {q["id"]: q for q in self.loader.load_questions()}
        mappings = self.loader.load_question_topics()
        self.assertEqual((len(concepts), len(topics), len(questions), len(mappings)),
                         (20, 67, 180, 180))
        self.assertEqual({m["question_id"] for m in mappings}, set(questions))
        counts = Counter(m["topic_id"] for m in mappings)
        self.assertEqual(set(counts), set(topics))
        for m in mappings:
            self.assertIn(m["topic_id"], topics)
            self.assertEqual(topics[m["topic_id"]]["parent_concept_id"],
                             questions[m["question_id"]]["concept_id"])
        for name, digest in self.EXPECTED_HASHES.items():
            with open(os.path.join(self.loader.data_dir, name), "rb") as handle:
                self.assertEqual(hashlib.sha256(handle.read()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
