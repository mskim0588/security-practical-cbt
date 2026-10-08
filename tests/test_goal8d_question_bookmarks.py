"""Goal 8D question-only catalog, route boundaries, and taxonomy preservation."""

import hashlib
import os
import unittest

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord, ExamAttempt
from app.services.alias_service import AliasService
from app.services.csrf_service import CSRF_SESSION_KEY
from app.services.data_loader import DataLoader
from sqlalchemy import func, select


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class Goal8DBookmarkTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
        self.loader = DataLoader(self.app.config["DATA_DIR"])

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_catalog_has_only_canonical_questions_and_safe_display_fields(self):
        response = self.client.get("/bookmarks/catalog")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        items = response.get_json()
        canonical = self.loader.load_questions()
        self.assertEqual(len(items), 180)
        self.assertEqual([item["id"] for item in items], [question["id"] for question in canonical])
        self.assertEqual(len({item["id"] for item in items}), 180)
        self.assertEqual(set(items[0]), {"id", "type", "type_label", "category", "concept", "topic", "preview", "url"})
        for item in items:
            self.assertTrue(item["url"].startswith("/topics/"))
            self.assertTrue(item["url"].endswith("#question-" + item["id"]))
            self.assertLessEqual(len(item["preview"]), 181)

    def test_page_and_supported_learning_surfaces(self):
        page = self.client.get("/bookmarks")
        self.assertEqual(page.status_code, 200)
        html = page.get_data(as_text=True)
        self.assertIn("다시 볼 문제", html)
        self.assertIn("Bookmarks are stored on this browser/device.", html)
        self.assertIn("bookmark-empty", html)
        self.assertIn('data-bookmark-filter="practical"', html)
        self.assertIn("js/bookmarks.js", html)

        first = self.loader.load_questions()[0]
        mapping = next(m for m in self.loader.load_question_topics() if m["question_id"] == first["id"])
        topic = self.client.get("/topics/" + mapping["topic_id"]).get_data(as_text=True)
        self.assertIn('data-bookmark-id="' + first["id"] + '"', topic)
        concept = self.client.get("/concepts/" + first["concept_id"]).get_data(as_text=True)
        self.assertIn('data-bookmark-id="' + first["id"] + '"', concept)
        search = self.client.get("/search?q=lastb").get_data(as_text=True)
        self.assertIn("data-bookmark-id=", search)

    def test_active_exam_and_pre_submit_training_have_no_bookmark_controls(self):
        for path in ("/exam", "/mock-exam", "/descriptive-training"):
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("data-bookmark-id=", html)
        for path in ("/exam",):
            html = self.client.get(path).get_data(as_text=True)
            self.assertNotIn("js/bookmarks.js", html)
        self.client.get("/mock-exam")
        with self.client.session_transaction() as session:
            token = session[CSRF_SESSION_KEY]
        started = self.client.post("/mock-exam/start", data={"csrf_token": token})
        self.assertEqual(started.status_code, 302)
        active = self.client.get(started.headers["Location"]).get_data(as_text=True)
        self.assertIn("review_flag", active)
        self.assertNotIn("data-bookmark-id=", active)
        self.assertNotIn("js/bookmarks.js", active)
        self.assertNotIn('href="/bookmarks"', active)

    def test_bookmark_routes_cannot_change_attempts_answers_or_grades(self):
        with self.app.app_context():
            before = (
                db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                db_session.scalar(select(func.count()).select_from(AnswerRecord)),
            )
        self.assertEqual(self.client.get("/bookmarks").status_code, 200)
        self.assertEqual(self.client.get("/bookmarks/catalog").status_code, 200)
        self.assertEqual(self.client.post("/bookmarks", data={"question_id": "Q-SHORT-001"}).status_code, 405)
        self.assertEqual(self.client.post("/bookmarks/catalog", data={"review_flag": "1"}).status_code, 405)
        with self.app.app_context():
            after = (
                db_session.scalar(select(func.count()).select_from(ExamAttempt)),
                db_session.scalar(select(func.count()).select_from(AnswerRecord)),
            )
        self.assertEqual(before, after)

    def test_practice_and_descriptive_controls_only_after_feedback(self):
        self.client.get("/practice")
        with self.client.session_transaction() as session:
            token = session[CSRF_SESSION_KEY]
        started = self.client.post("/practice/start", data={
            "csrf_token": token, "rounds": "1", "scope_kind": "type", "question_type": "short",
        })
        self.assertEqual(started.status_code, 302)
        path = started.headers["Location"]
        before = self.client.get(path).get_data(as_text=True)
        self.assertNotIn("data-bookmark-id=", before)
        self.assertNotIn("js/bookmarks.js", before)
        answered = self.client.post(path + "/answer", data={"csrf_token": token})
        self.assertEqual(answered.status_code, 302)
        after = self.client.get(path).get_data(as_text=True)
        self.assertIn("data-bookmark-id=", after)

        self.client.get("/descriptive-training")
        started = self.client.post("/descriptive-training/start", data={
            "csrf_token": token, "scope_kind": "all", "count": "5",
        })
        self.assertEqual(started.status_code, 302)
        path = started.headers["Location"]
        before = self.client.get(path).get_data(as_text=True)
        self.assertNotIn("data-bookmark-id=", before)
        self.assertNotIn("js/bookmarks.js", before)
        answered = self.client.post(path + "/answer", data={"csrf_token": token})
        self.assertEqual(answered.status_code, 302)
        after = self.client.get(path).get_data(as_text=True)
        self.assertIn("data-bookmark-id=", after)

    def test_taxonomy_aliases_and_core_hashes_unchanged(self):
        concepts = self.loader.load_concepts()
        topics = self.loader.load_topics()
        questions = self.loader.load_questions()
        mappings = self.loader.load_question_topics()
        self.assertEqual((len(concepts), len(topics), len(questions), len(mappings)), (20, 67, 180, 180))
        concept_by_id = {concept["id"]: concept for concept in concepts}
        topic_by_id = {topic["topic_id"]: topic for topic in topics}
        question_by_id = {question["id"]: question for question in questions}
        self.assertEqual({m["question_id"] for m in mappings}, set(question_by_id))
        self.assertEqual({m["topic_id"] for m in mappings}, set(topic_by_id))
        self.assertTrue(all(topic_by_id[m["topic_id"]]["parent_concept_id"] == question_by_id[m["question_id"]]["concept_id"] for m in mappings))
        self.assertTrue(all(topic["parent_concept_id"] in concept_by_id for topic in topics))
        alias_service = AliasService(self.loader)
        self.assertEqual(len(alias_service.aliases), 39)
        self.assertTrue(all(not finding for finding in alias_service.audit.values()))
        expected = {
            "questions.json": "661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9",
            "concepts.json": "d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943",
            "sources.json": "9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21",
            "concept_contents.json": "025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171",
            "explanations.json": "e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696",
        }
        for name, digest in expected.items():
            with open(os.path.join(self.loader.data_dir, name), "rb") as file:
                self.assertEqual(hashlib.sha256(file.read()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
