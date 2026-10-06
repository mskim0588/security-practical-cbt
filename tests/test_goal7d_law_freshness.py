import hashlib
import json
import os
import tempfile
import unittest
from datetime import date
from urllib.parse import urlparse

from sqlalchemy import select

from app import create_app
from app.config import Config
from app.models.database import close_db, db_session, init_db
from app.models.history import AnswerRecord
from app.services.csrf_service import CSRF_SESSION_KEY
from app.services.data_loader import DataLoader
from app.services.descriptive_training_service import DescriptiveTrainingService
from app.services.history_service import HistoryService
from app.services.law_freshness_service import (
    LawFreshnessService,
    LawFreshnessValidationError,
)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "owner-secret"


class TestGoal7DLawFreshness(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.service = LawFreshnessService(self.loader)
        self.client.get("/exam")
        with self.client.session_transaction() as sess:
            sess["is_admin"] = True
            self.csrf_token = sess[CSRF_SESSION_KEY]

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def _service_with_record(self, record):
        verified = 1 if record.get("status") == "VERIFIED" else 0
        payload = {
            "schema_version": 1,
            "inventory": {
                "inventory_date": "2026-10-07",
                "candidates_inspected": 1,
                "freshness_sensitive_mapped": 1,
                "non_sensitive_excluded": 0,
                "verified_count": verified,
                "review_required_count": 1 - verified,
                "scope_note": "test",
            },
            "records": [record],
        }
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", encoding="utf-8", delete=False
        )
        json.dump(payload, handle, ensure_ascii=False)
        handle.close()
        self.addCleanup(lambda: os.path.exists(handle.name) and os.unlink(handle.name))
        return LawFreshnessService(self.loader, metadata_path=handle.name)

    @staticmethod
    def _review_record(**overrides):
        record = {
            "record_id": "LAW-TEST-1",
            "target_type": "question",
            "target_id": "Q-SHORT-023",
            "status": "REVIEW_REQUIRED",
            "reference_date": None,
            "last_reviewed_at": None,
            "authority": "",
            "source_url": "",
            "legal_basis": "",
            "review_note": "공식 자료 재검토 필요",
        }
        record.update(overrides)
        return record

    def _start_descriptive(self):
        response = self.client.post(
            "/descriptive-training/start",
            data={
                "csrf_token": self.csrf_token,
                "scope_kind": "all",
                "category": "",
                "count": "5",
            },
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        return int(response.headers["Location"].rstrip("/").split("/")[-1])

    def _force_descriptive_question(self, attempt_id, question_id):
        with self.app.app_context():
            meta = db_session.scalar(
                select(AnswerRecord).where(
                    AnswerRecord.attempt_id == attempt_id,
                    AnswerRecord.question_type
                    == DescriptiveTrainingService.META_QUESTION_TYPE,
                )
            )
            config = meta.get_parsed_self_eval()
            config.update(
                {
                    "question_ids": [question_id],
                    "current_index": 0,
                    "phase": "question",
                    "latest_record_id": None,
                }
            )
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()

    def _create_law_attempt(self):
        question = self.loader.get_question_by_id("Q-SHORT-023")
        grading_result = {
            "total_score": 0,
            "is_passed": False,
            "summary": {
                "short": {"earned": 0},
                "descriptive": {"earned": 0},
                "practical": {"earned": 0},
            },
            "details": [
                {
                    "question_id": question["id"],
                    "type": "short",
                    "earned_score": 0,
                    "max_score": question["score"],
                    "is_selected": True,
                    "sub_results": [],
                }
            ],
        }
        with self.app.app_context():
            attempt = HistoryService(self.loader).save_exam_attempt(
                exam_mode="standard",
                seed=7,
                selected_practical_id=None,
                grading_result=grading_result,
                answers={question["id"]: "오답"},
                submission_token="goal7d-law-attempt",
                is_owner=True,
            )
            return attempt.id

    def test_01_inventory_statuses_and_targets_are_valid(self):
        records = self.service.get_records()
        inventory = self.service.get_inventory()
        self.assertEqual(len(records), 13)
        self.assertEqual(inventory["candidates_inspected"], 29)
        self.assertEqual(inventory["freshness_sensitive_mapped"], 13)
        self.assertEqual(inventory["non_sensitive_excluded"], 16)
        self.assertEqual(inventory["verified_count"], 4)
        self.assertEqual(inventory["review_required_count"], 9)
        self.assertEqual({item["status"] for item in records}, set(self.service.STATUSES))
        question_ids = {item["id"] for item in self.loader.load_questions()}
        self.assertTrue(all(item["target_id"] in question_ids for item in records))

    def test_02_verified_requires_real_evidence_and_dates(self):
        verified = self.service.get_records("VERIFIED")
        self.assertEqual(len(verified), 4)
        for record in verified:
            self.assertTrue(record["authority"])
            self.assertTrue(record["legal_basis"])
            self.assertEqual(urlparse(record["source_url"]).scheme, "https")
            self.assertIn(urlparse(record["source_url"]).hostname, self.service.ALLOWED_SOURCE_HOSTS)
            self.assertEqual(date.fromisoformat(record["reference_date"]).isoformat(), record["reference_date"])
            self.assertEqual(date.fromisoformat(record["last_reviewed_at"]).isoformat(), record["last_reviewed_at"])
        review = self.service.get_records("REVIEW_REQUIRED")
        self.assertEqual(len(review), 9)
        self.assertTrue(all(not item["source_url"] for item in review))

    def test_03_invalid_status_and_target_are_rejected(self):
        invalid_status = self._service_with_record(
            self._review_record(status="CURRENT")
        )
        with self.assertRaises(LawFreshnessValidationError):
            invalid_status.get_records()
        invalid_target = self._service_with_record(
            self._review_record(target_id="Q-NOT-REAL")
        )
        with self.assertRaises(LawFreshnessValidationError):
            invalid_target.get_records()

    def test_04_invalid_dates_and_untrusted_urls_are_rejected(self):
        bad_date = self._service_with_record(
            self._review_record(reference_date="2026-02-30")
        )
        with self.assertRaises(LawFreshnessValidationError):
            bad_date.get_records()
        bad_url = self._service_with_record(
            self._review_record(source_url="https://example.com/law")
        )
        with self.assertRaises(LawFreshnessValidationError):
            bad_url.get_records()

    def test_05_verified_missing_evidence_is_rejected_but_review_is_not(self):
        missing = self._service_with_record(
            self._review_record(status="VERIFIED")
        )
        with self.assertRaises(LawFreshnessValidationError):
            missing.get_records()
        review = self._service_with_record(self._review_record())
        self.assertEqual(review.get_records()[0]["status"], "REVIEW_REQUIRED")

    def test_06_owner_review_page_permissions_filters_and_safe_links(self):
        guest = self.app.test_client()
        denied = guest.get("/law-freshness", follow_redirects=False)
        self.assertEqual(denied.status_code, 302)
        self.assertIn("/admin-login", denied.headers["Location"])

        response = self.client.get("/law-freshness")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("검증됨", html)
        self.assertIn("검토 필요", html)
        self.assertIn("Q-SHORT-023", html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertNotIn("{'record_id':", html)
        self.assertEqual(self.client.post("/law-freshness").status_code, 405)

        verified = self.client.get("/law-freshness?status=VERIFIED").get_data(as_text=True)
        self.assertIn("Q-SHORT-023", verified)
        self.assertNotIn("Q-SHORT-001", verified)
        required = self.client.get("/law-freshness?status=REVIEW_REQUIRED").get_data(as_text=True)
        self.assertIn("Q-SHORT-001", required)
        self.assertNotIn("Q-SHORT-023", required)
        self.assertEqual(self.client.get("/law-freshness?status=INVALID").status_code, 400)

    def test_07_learner_concept_badges_are_scoped_to_sensitive_content(self):
        law_html = self.client.get("/concepts/CON-MGT-02").get_data(as_text=True)
        self.assertIn("법규 최신성", law_html)
        self.assertIn("검증됨", law_html)
        self.assertIn("검토 필요", law_html)
        self.assertIn("2026-10-07", law_html)
        self.assertIn("공식 출처 확인", law_html)

        stable_html = self.client.get("/concepts/CON-SYS-01").get_data(as_text=True)
        self.assertNotIn('class="law-freshness-badge', stable_html)
        self.assertNotIn('class="law-concept-summary', stable_html)

    def test_08_active_exam_surfaces_do_not_leak_freshness_details(self):
        exam_html = self.client.get("/exam").get_data(as_text=True)
        self.assertNotIn("law-freshness-card", exam_html)
        self.assertNotIn("개인정보 보호법 제34조제1항", exam_html)

        mock_response = self.client.post(
            "/mock-exam/start",
            data={"csrf_token": self.csrf_token},
            follow_redirects=True,
        )
        self.assertEqual(mock_response.status_code, 200)
        self.assertNotIn("law-freshness-card", mock_response.get_data(as_text=True))

        attempt_id = self._start_descriptive()
        self._force_descriptive_question(attempt_id, "Q-DESC-019")
        active_html = self.client.get(
            f"/descriptive-training/{attempt_id}"
        ).get_data(as_text=True)
        self.assertNotIn("law-freshness-card", active_html)
        self.assertNotIn("최신성 근거 보기", active_html)

    def test_09_descriptive_freshness_appears_only_after_submission(self):
        attempt_id = self._start_descriptive()
        question = self.loader.get_question_by_id("Q-DESC-019")
        self._force_descriptive_question(attempt_id, question["id"])
        data = {"csrf_token": self.csrf_token}
        for sub in question["sub_questions"]:
            data[f"ans_{question['id']}_{sub['sub_id']}"] = sub.get("model_answer", "")
        response = self.client.post(
            f"/descriptive-training/{attempt_id}/answer",
            data=data,
            follow_redirects=True,
        )
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("law-freshness-card", html)
        self.assertIn("검토 필요", html)
        self.assertIn("법규 내용은 개정될 수 있으므로", html)

    def test_10_result_history_and_wrong_note_show_verified_record(self):
        attempt_id = self._create_law_attempt()
        with self.client.session_transaction() as sess:
            sess["submitted_attempts"] = [attempt_id]
        for path in (
            f"/result/{attempt_id}",
            f"/history/{attempt_id}",
            "/wrong-notes/Q-SHORT-023",
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn("law-freshness-card", html)
                self.assertIn("검증됨", html)
                self.assertIn("2026-10-07", html)

    def test_11_existing_mode_route_regression(self):
        attempt_id = self._create_law_attempt()
        with self.client.session_transaction() as sess:
            sess["submitted_attempts"] = [attempt_id]
        for path in (
            "/exam",
            "/practice",
            "/descriptive-training",
            "/mock-exam",
            f"/result/{attempt_id}",
            "/history",
            "/wrong-notes",
            "/concepts",
            "/dashboard",
        ):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_12_protected_core_hashes_are_unchanged(self):
        expected = {
            "questions.json": "661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9",
            "concepts.json": "d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943",
            "sources.json": "9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21",
            "concept_contents.json": "025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171",
            "explanations.json": "e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696",
        }
        for filename, digest in expected.items():
            with open(os.path.join(self.loader.data_dir, filename), "rb") as handle:
                self.assertEqual(hashlib.sha256(handle.read()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
