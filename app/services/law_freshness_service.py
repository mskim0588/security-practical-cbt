import json
import os
from datetime import date
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from app.services.data_loader import DataLoader


class LawFreshnessValidationError(ValueError):
    """Raised when additive law-freshness metadata is unsafe or inconsistent."""


class LawFreshnessService:
    STATUSES = ("VERIFIED", "REVIEW_REQUIRED")
    TARGET_TYPES = ("question", "concept")
    STATUS_LABELS = {
        "VERIFIED": "검증됨",
        "REVIEW_REQUIRED": "검토 필요",
    }
    ALLOWED_SOURCE_HOSTS = {
        "law.go.kr",
        "www.law.go.kr",
        "pipc.go.kr",
        "www.pipc.go.kr",
        "kisa.or.kr",
        "www.kisa.or.kr",
    }

    def __init__(
        self,
        data_loader: Optional[DataLoader] = None,
        metadata_path: Optional[str] = None,
    ):
        self.loader = data_loader or DataLoader()
        self.metadata_path = metadata_path or os.path.join(
            self.loader.data_dir, "law_freshness.json"
        )
        self._payload: Optional[Dict[str, Any]] = None
        self._records: Optional[List[Dict[str, Any]]] = None

    @staticmethod
    def _parse_date(value: Any, field_name: str, required: bool = False) -> Optional[str]:
        if value in (None, ""):
            if required:
                raise LawFreshnessValidationError(f"{field_name} is required")
            return None
        if not isinstance(value, str):
            raise LawFreshnessValidationError(f"{field_name} must use YYYY-MM-DD")
        try:
            parsed = date.fromisoformat(value)
        except ValueError as error:
            raise LawFreshnessValidationError(
                f"{field_name} must use YYYY-MM-DD"
            ) from error
        if parsed.isoformat() != value:
            raise LawFreshnessValidationError(f"{field_name} must use YYYY-MM-DD")
        return value

    @classmethod
    def _validate_source_url(cls, value: Any, required: bool = False) -> str:
        if value in (None, ""):
            if required:
                raise LawFreshnessValidationError("source_url is required")
            return ""
        if not isinstance(value, str):
            raise LawFreshnessValidationError("source_url must be a string")
        parsed = urlparse(value)
        if parsed.scheme != "https" or parsed.hostname not in cls.ALLOWED_SOURCE_HOSTS:
            raise LawFreshnessValidationError(
                "source_url must be HTTPS and use an approved authoritative host"
            )
        return value

    def _load_payload(self) -> Dict[str, Any]:
        if self._payload is None:
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
            except (OSError, json.JSONDecodeError) as error:
                raise LawFreshnessValidationError(
                    "law freshness metadata could not be loaded"
                ) from error
            if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
                raise LawFreshnessValidationError("metadata must contain a records list")
            self._payload = payload
        return self._payload

    def _target_maps(self):
        questions = {item["id"]: item for item in self.loader.load_questions()}
        concepts = {item["id"]: item for item in self.loader.load_concepts()}
        return questions, concepts

    def _validate_record(
        self,
        record: Dict[str, Any],
        questions: Dict[str, Dict[str, Any]],
        concepts: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        if not isinstance(record, dict):
            raise LawFreshnessValidationError("each freshness record must be an object")

        record_id = str(record.get("record_id", "")).strip()
        target_type = str(record.get("target_type", "")).strip()
        target_id = str(record.get("target_id", "")).strip()
        status = str(record.get("status", "")).strip()
        review_note = str(record.get("review_note", "")).strip()

        if not record_id or not target_id or not review_note:
            raise LawFreshnessValidationError(
                "record_id, target_id, and review_note are required"
            )
        if target_type not in self.TARGET_TYPES:
            raise LawFreshnessValidationError(f"invalid target_type: {target_type}")
        if status not in self.STATUSES:
            raise LawFreshnessValidationError(f"invalid status: {status}")

        target = questions.get(target_id) if target_type == "question" else concepts.get(target_id)
        if not target:
            raise LawFreshnessValidationError(
                f"unknown {target_type} target: {target_id}"
            )

        verified = status == "VERIFIED"
        authority = str(record.get("authority", "")).strip()
        legal_basis = str(record.get("legal_basis", "")).strip()
        reference_date = self._parse_date(
            record.get("reference_date"), "reference_date", required=verified
        )
        last_reviewed_at = self._parse_date(
            record.get("last_reviewed_at"), "last_reviewed_at", required=verified
        )
        source_url = self._validate_source_url(
            record.get("source_url"), required=verified
        )
        if verified and (not authority or not legal_basis):
            raise LawFreshnessValidationError(
                "VERIFIED records require authority and legal_basis"
            )

        normalized = {
            "record_id": record_id,
            "target_type": target_type,
            "target_id": target_id,
            "status": status,
            "status_label": self.STATUS_LABELS[status],
            "reference_date": reference_date,
            "last_reviewed_at": last_reviewed_at,
            "authority": authority,
            "source_url": source_url,
            "legal_basis": legal_basis,
            "review_note": review_note,
            "target_title": target.get("question") or target.get("name", target_id),
            "category": target.get("category", ""),
            "concept_id": target.get("concept_id") if target_type == "question" else target_id,
            "learner_note": (
                "기록된 공식 출처와 기준일을 기준으로 검증된 상태입니다."
                if verified
                else "법규 내용은 개정될 수 있으므로 최신 기준 확인이 필요합니다."
            ),
        }
        return normalized

    def get_records(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if self._records is None:
            questions, concepts = self._target_maps()
            records: List[Dict[str, Any]] = []
            record_ids = set()
            targets = set()
            for raw_record in self._load_payload()["records"]:
                record = self._validate_record(raw_record, questions, concepts)
                target_key = (record["target_type"], record["target_id"])
                if record["record_id"] in record_ids:
                    raise LawFreshnessValidationError("duplicate record_id")
                if target_key in targets:
                    raise LawFreshnessValidationError("duplicate freshness target")
                record_ids.add(record["record_id"])
                targets.add(target_key)
                records.append(record)
            self._records = sorted(records, key=lambda item: item["target_id"])
            self._validate_inventory()

        if status is None:
            return [dict(item) for item in self._records]
        if status not in self.STATUSES:
            raise LawFreshnessValidationError(f"invalid status filter: {status}")
        return [dict(item) for item in self._records if item["status"] == status]

    def _validate_inventory(self) -> None:
        inventory = self._load_payload().get("inventory")
        if not isinstance(inventory, dict):
            raise LawFreshnessValidationError("metadata must contain inventory")
        verified_count = sum(1 for item in self._records or [] if item["status"] == "VERIFIED")
        review_count = sum(
            1 for item in self._records or [] if item["status"] == "REVIEW_REQUIRED"
        )
        mapped = len(self._records or [])
        if (
            inventory.get("freshness_sensitive_mapped") != mapped
            or inventory.get("verified_count") != verified_count
            or inventory.get("review_required_count") != review_count
            or inventory.get("candidates_inspected", 0) < mapped
            or inventory.get("non_sensitive_excluded")
            != inventory.get("candidates_inspected", 0) - mapped
        ):
            raise LawFreshnessValidationError("inventory counts do not match records")

    def get_inventory(self) -> Dict[str, Any]:
        self.get_records()
        return dict(self._load_payload()["inventory"])

    def get_for_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        return next(
            (
                item
                for item in self.get_records()
                if item["target_type"] == "question" and item["target_id"] == question_id
            ),
            None,
        )

    def get_concept_summary(self, concept_id: str) -> Optional[Dict[str, Any]]:
        records = [
            item for item in self.get_records() if item.get("concept_id") == concept_id
        ]
        if not records:
            return None
        verified_count = sum(1 for item in records if item["status"] == "VERIFIED")
        review_count = len(records) - verified_count
        status = "REVIEW_REQUIRED" if review_count else "VERIFIED"
        return {
            "status": status,
            "status_label": self.STATUS_LABELS[status],
            "verified_count": verified_count,
            "review_required_count": review_count,
            "records": records,
            "by_target_id": {item["target_id"]: item for item in records},
        }
