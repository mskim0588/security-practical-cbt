"""Goal 8C search behavior and preservation gates."""

import hashlib
import os
import unittest

from app import create_app
from app.config import Config
from app.models.database import close_db, init_db
from app.services.alias_service import AliasService, normalize_alias
from app.services.data_loader import DataLoader
from app.services.search_service import MAX_QUERY_LENGTH, SearchService


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class Goal8CSearchTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
        self.loader = DataLoader(self.app.config["DATA_DIR"])
        self.aliases = AliasService(self.loader)
        self.search = SearchService(self.loader, self.aliases)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_taxonomy_aliases_and_protected_hashes(self):
        concepts = self.loader.load_concepts()
        topics = self.loader.load_topics()
        questions = self.loader.load_questions()
        mappings = self.loader.load_question_topics()
        self.assertEqual((len(concepts), len(topics), len(questions), len(mappings)), (20, 67, 180, 180))
        self.assertEqual(len({m["question_id"] for m in mappings}), 180)
        self.assertEqual(len({m["topic_id"] for m in mappings}), 67)
        self.assertEqual(len(self.aliases.aliases), 39)
        self.assertEqual(len({a["target_id"] for a in self.aliases.aliases if a["target_type"] == "concept"}), 9)
        self.assertEqual(len({a["target_id"] for a in self.aliases.aliases if a["target_type"] == "topic"}), 23)
        for finding in self.aliases.audit.values():
            self.assertFalse(finding)
        expected = {
            "questions.json": "661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9",
            "concepts.json": "d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943",
            "sources.json": "9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21",
            "concept_contents.json": "025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171",
            "explanations.json": "e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696",
        }
        for filename, digest in expected.items():
            with open(os.path.join(self.loader.data_dir, filename), "rb") as file:
                self.assertEqual(hashlib.sha256(file.read()).hexdigest(), digest)

    def test_exact_canonical_alias_types_and_normalization(self):
        concept = self.loader.load_concepts()[0]
        topic = self.loader.load_topics()[0]
        self.assertEqual(self.search.search(concept["name"])["results"][0]["id"], concept["id"])
        self.assertEqual(self.search.search(topic["name"])["results"][0]["id"], topic["topic_id"])
        samples = {
            "ko_alt": next(a["alias"] for a in self.aliases.aliases if a["alias_type"] == "ko_alt"),
            "en_full": "SQL Injection",
            "acronym": "SQLi",
            "synonym": "SQL 삽입 공격",
        }
        for alias in samples.values():
            target = self.aliases.resolve(alias)[0]
            results = self.search.search("  " + alias.swapcase() + "  ")["results"]
            self.assertEqual((results[0]["type"], results[0]["id"]),
                             (target["target_type"], target["target_id"]))
        self.assertEqual(normalize_alias("  SQL   Injection  "), normalize_alias("SQL\tInjection"))
        self.assertEqual(self.search.search("e\u0301")["results"], self.search.search("é")["results"])

    def test_ranking_dedup_and_determinism(self):
        for term, target in [("SQLi", "TOP-APP-01-02"), ("SQL Injection", "TOP-APP-01-02")]:
            result = self.search.search(term)
            self.assertEqual(result["results"][0]["id"], target)
            ids = [(r["type"], r["id"]) for r in result["results"]]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(result, self.search.search(term))
        topic = next(t for t in self.loader.load_topics() if t["topic_id"] == "TOP-APP-01-02")
        self.assertEqual(self.search.search(topic["name"])["results"][0]["id"], topic["topic_id"])
        self.assertEqual(self.search.search(topic["name"][:3])["results"][0]["id"], topic["topic_id"])

    def test_keyword_command_question_and_filters(self):
        for term in ("iptables", "lastb", "tcpdump"):
            result = self.search.search(term)
            self.assertGreater(result["total"], 0)
        self.assertTrue(any(r["type"] == "question" for r in self.search.search("lastb")["results"]))
        all_result = self.search.search("SQLi")
        for kind in ("concept", "topic", "question"):
            filtered = self.search.search("SQLi", kind)
            self.assertEqual(filtered["total"], all_result["type_counts"][kind])
            self.assertTrue(all(r["type"] == kind for r in filtered["results"]))
        self.assertEqual(self.search.search("SQLi", "bad")["results"], all_result["results"])

    def test_future_ambiguous_alias_returns_all_targets(self):
        base = dict(self.aliases.aliases[0])
        first = dict(base, alias_id="FUTURE-1", alias="shared future term", target_id="CON-NET-02")
        second = dict(base, alias_id="FUTURE-2", alias="shared future term", target_id="CON-NET-03")
        aliases = AliasService(self.loader, aliases=[first, second])
        ids = {(r["type"], r["id"]) for r in SearchService(self.loader, aliases).search("shared future term")["results"]}
        self.assertEqual(ids, {("concept", "CON-NET-02"), ("concept", "CON-NET-03")})

    def test_route_security_navigation_and_anti_cheat(self):
        self.assertEqual(self.client.get("/search").status_code, 200)
        page = self.client.get("/search?q=SQLi").get_data(as_text=True)
        self.assertIn("검색 결과", page)
        self.assertIn("/topics/TOP-APP-01-02", page)
        self.assertNotIn("normalized_title", page)
        self.assertNotIn("model_answer", page[page.index('<div class="learning-search-results">'):page.index("</main>")])
        self.assertIn("/search", self.client.get("/concepts").get_data(as_text=True))
        self.assertIn("검색어를 입력", self.client.get("/search").get_data(as_text=True))
        self.assertIn("일치하는 학습 항목", self.client.get("/search?q=unlisted-zzz-9888").get_data(as_text=True))
        unsafe = self.client.get("/search", query_string={"q": "<script>alert(1)</script>"}).get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", unsafe)
        self.assertIn("&lt;script&gt;", unsafe)
        self.assertIn("검색어는", self.client.get("/search", query_string={"q": "x" * (MAX_QUERY_LENGTH + 1)}).get_data(as_text=True))
        self.assertEqual(self.client.get("/search?q=%5B%28%2A%3F").status_code, 200)
        for path in ("/exam", "/mock-exam", "/descriptive-training"):
            self.assertNotIn("learning-search-form", self.client.get(path).get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
