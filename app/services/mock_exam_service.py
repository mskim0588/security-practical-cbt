import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, select

from app.models.database import db_session
from app.models.history import AnswerRecord, ExamAttempt
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService
from app.services.grader import Grader


class MockExamStateError(RuntimeError):
    """Raised when a persisted mock exam cannot be restored safely."""


class MockExamService:
    ACTIVE_MODE = "mock_exam_active"
    FINAL_MODE = "mock_exam"
    META_QUESTION_ID = "__mock_exam_config__"
    META_QUESTION_TYPE = "mock_exam_meta"
    DURATION_SECONDS = 180 * 60
    CANDIDATE_COUNT = 18
    SCORED_COUNT = 17

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.exam_service = ExamService(self.loader)

    @staticmethod
    def _now() -> datetime:
        """Return a naive UTC timestamp, matching the existing DateTime columns."""
        return datetime.now(timezone.utc).replace(tzinfo=None)

    @staticmethod
    def _type_label(question_type: str) -> str:
        return {
            "short": "단답형",
            "descriptive": "서술형",
            "practical": "실무형",
        }.get(question_type, question_type)

    @staticmethod
    def _empty_answer(question: Dict[str, Any]) -> Any:
        if question.get("type") == "short":
            subs = question.get("sub_questions") or []
            if subs:
                return {str(sub.get("label")): "" for sub in subs}
            return ""
        return {str(sub.get("sub_id")): "" for sub in question.get("sub_questions", [])}

    @staticmethod
    def _serialize_answer(answer: Any) -> str:
        if isinstance(answer, (dict, list)):
            return json.dumps(answer, ensure_ascii=False)
        return str(answer or "")

    @staticmethod
    def _learner_question(question: Dict[str, Any]) -> Dict[str, Any]:
        """Return prompt-only question data. Grading and learning fields stay server-side."""
        public = {
            "id": question.get("id"),
            "type": question.get("type"),
            "type_label": MockExamService._type_label(question.get("type", "")),
            "category": question.get("category", ""),
            "score": question.get("score", 0),
            "question": question.get("question", ""),
            "sub_questions": [],
        }
        if question.get("type") == "short":
            public["sub_questions"] = [
                {"label": sub.get("label"), "score": sub.get("score", 0)}
                for sub in question.get("sub_questions") or []
            ]
        else:
            public["sub_questions"] = [
                {
                    "sub_id": str(sub.get("sub_id")),
                    "prompt": sub.get("prompt", ""),
                    "score": sub.get("score", 0),
                }
                for sub in question.get("sub_questions", [])
            ]
        return public

    def create_attempt(self, is_owner: bool) -> ExamAttempt:
        questions = self.exam_service.get_exam_questions(mode="standard", is_owner=is_owner)
        if len(questions) != self.CANDIDATE_COUNT:
            raise MockExamStateError("실전 모의고사 18문항 구성을 생성할 수 없습니다.")

        practical_ids = [q["id"] for q in questions if q.get("type") == "practical"]
        if len(practical_ids) != 2:
            raise MockExamStateError("실무형 후보 2문항 구성을 생성할 수 없습니다.")

        now = self._now()
        attempt = ExamAttempt(
            submission_token=f"mock-{secrets.token_urlsafe(32)}",
            exam_mode=self.ACTIVE_MODE,
            seed=None,
            started_at=now,
            submitted_at=now,
            duration_seconds=None,
            total_score=0.0,
            short_score=0.0,
            descriptive_score=0.0,
            practical_score=0.0,
            selected_practical_id=practical_ids[0],
            is_passed=False,
            is_owner=is_owner,
            created_at=now,
        )
        config = {
            "version": 1,
            "phase": "active",
            "question_ids": [q["id"] for q in questions],
            "selected_practical_id": practical_ids[0],
            "review_flags": [],
            "finalized_reason": None,
            "finalized_at": None,
        }

        try:
            db_session.add(attempt)
            db_session.flush()
            db_session.add(AnswerRecord(
                attempt_id=attempt.id,
                question_id=self.META_QUESTION_ID,
                question_type=self.META_QUESTION_TYPE,
                user_answer="",
                earned_score=0.0,
                max_score=0.0,
                achievement_status="unselected",
                is_correct=False,
                self_eval_data=json.dumps(config, ensure_ascii=False),
                created_at=now,
            ))
            for question in questions:
                db_session.add(AnswerRecord(
                    attempt_id=attempt.id,
                    question_id=question["id"],
                    question_type=question["type"],
                    user_answer=self._serialize_answer(self._empty_answer(question)),
                    earned_score=0.0,
                    max_score=0.0,
                    achievement_status="ungraded",
                    is_correct=False,
                    self_eval_data=None,
                    created_at=now,
                ))
            db_session.commit()
            return attempt
        except Exception:
            db_session.rollback()
            raise

    def get_attempt(self, attempt_id: int, lock: bool = False) -> Optional[ExamAttempt]:
        stmt = select(ExamAttempt).where(
            ExamAttempt.id == attempt_id,
            ExamAttempt.exam_mode.in_((self.ACTIVE_MODE, self.FINAL_MODE)),
        )
        if lock:
            stmt = stmt.with_for_update()
        return db_session.scalar(stmt)

    def _get_meta_record(self, attempt_id: int) -> Optional[AnswerRecord]:
        return db_session.scalar(select(AnswerRecord).where(
            AnswerRecord.attempt_id == attempt_id,
            AnswerRecord.question_id == self.META_QUESTION_ID,
            AnswerRecord.question_type == self.META_QUESTION_TYPE,
        ))

    @staticmethod
    def _decode_config(meta: AnswerRecord) -> Dict[str, Any]:
        config = meta.get_parsed_self_eval()
        required = {"phase", "question_ids", "selected_practical_id", "review_flags"}
        if not isinstance(config, dict) or not required.issubset(config):
            raise MockExamStateError("실전 모의고사 진행 정보를 복구할 수 없습니다.")
        if not isinstance(config.get("question_ids"), list) or len(config["question_ids"]) != 18:
            raise MockExamStateError("실전 모의고사 문항 구성이 올바르지 않습니다.")
        if not isinstance(config.get("review_flags"), list):
            raise MockExamStateError("다시 보기 상태를 복구할 수 없습니다.")
        return config

    def _get_question_records(self, attempt_id: int) -> List[AnswerRecord]:
        return list(db_session.scalars(
            select(AnswerRecord)
            .where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_type != self.META_QUESTION_TYPE,
            )
            .order_by(AnswerRecord.id)
        ).all())

    @classmethod
    def expiry_at(cls, attempt: ExamAttempt) -> datetime:
        if not attempt.started_at:
            raise MockExamStateError("시험 시작 시각을 복구할 수 없습니다.")
        return attempt.started_at + timedelta(seconds=cls.DURATION_SECONDS)

    def is_expired(self, attempt: ExamAttempt, now: Optional[datetime] = None) -> bool:
        return (now or self._now()) >= self.expiry_at(attempt)

    def _resolve_questions(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        questions = self.exam_service.get_questions_by_ids(config["question_ids"])
        if len(questions) != self.CANDIDATE_COUNT:
            raise MockExamStateError("문제은행 변경으로 현재 모의고사를 안전하게 복구할 수 없습니다.")
        return questions

    def _build_state(
        self,
        attempt: ExamAttempt,
        config: Dict[str, Any],
        current_index: int = 0,
        now: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        questions = self._resolve_questions(config)
        records = {record.question_id: record for record in self._get_question_records(attempt.id)}
        if len(records) != self.CANDIDATE_COUNT:
            raise MockExamStateError("저장된 답안 구성이 올바르지 않습니다.")

        selected_id = config.get("selected_practical_id")
        flags = set(config.get("review_flags", []))
        items = []
        answered_count = 0
        for index, question in enumerate(questions):
            record = records[question["id"]]
            answer = record.get_parsed_answer()
            selected = question["type"] != "practical" or question["id"] == selected_id
            status = self.exam_service.calculate_question_status(question, answer, selected)
            required = question["type"] != "practical" or selected
            if required and status["is_filled"]:
                answered_count += 1
            flagged = question["id"] in flags
            if question["type"] == "practical" and not selected:
                state_text = "미선택 · 채점 제외"
            elif status["is_filled"]:
                state_text = "답변 완료"
            else:
                state_text = "미응답"
            if flagged:
                state_text += " + 다시 보기"
            items.append({
                "index": index,
                "number": index + 1,
                "id": question["id"],
                "type": question["type"],
                "type_label": self._type_label(question["type"]),
                "category": question.get("category", ""),
                "score": question.get("score", 0),
                "answer": answer,
                "is_answered": bool(status["is_filled"]),
                "is_complete": bool(status["is_complete"]),
                "is_flagged": flagged,
                "is_selected_practical": question["type"] == "practical" and selected,
                "is_unselected_practical": question["type"] == "practical" and not selected,
                "is_required": required,
                "state_text": state_text,
                "status_code": status["status_code"],
                "question": self._learner_question(question),
            })

        safe_index = max(0, min(int(current_index), self.CANDIDATE_COUNT - 1))
        expiry = self.expiry_at(attempt)
        current_now = now or self._now()
        remaining = max(0, int((expiry - current_now).total_seconds()))
        practical_items = [item for item in items if item["type"] == "practical"]
        selected_item = next((item for item in practical_items if item["is_selected_practical"]), None)
        return {
            "attempt_id": attempt.id,
            "phase": config.get("phase"),
            "items": items,
            "current_index": safe_index,
            "current": items[safe_index],
            "answered_count": answered_count,
            "unanswered_count": self.SCORED_COUNT - answered_count,
            "flagged_count": len(flags),
            "selected_practical_id": selected_id,
            "selected_practical_label": f"{selected_item['number']}번" if selected_item else "미선택",
            "practical_items": practical_items,
            "expiry_iso": expiry.isoformat(timespec="seconds") + "Z",
            "remaining_seconds": remaining,
            "duration_seconds": self.DURATION_SECONDS,
            "finalized_reason": config.get("finalized_reason"),
        }

    def get_state(self, attempt_id: int, current_index: int = 0) -> Optional[Dict[str, Any]]:
        attempt = self.get_attempt(attempt_id)
        if not attempt:
            return None
        meta = self._get_meta_record(attempt_id)
        if not meta:
            raise MockExamStateError("실전 모의고사 진행 정보가 없습니다.")
        config = self._decode_config(meta)
        return self._build_state(attempt, config, current_index=current_index)

    def finalize_if_expired(self, attempt_id: int, now: Optional[datetime] = None) -> bool:
        attempt = self.get_attempt(attempt_id)
        if not attempt or attempt.exam_mode == self.FINAL_MODE:
            return bool(attempt and attempt.exam_mode == self.FINAL_MODE)
        current_now = now or self._now()
        if not self.is_expired(attempt, current_now):
            return False
        self.finalize(attempt_id, reason="expired", now=current_now)
        return True

    def _active_locked(self, attempt_id: int, now: datetime):
        attempt = self.get_attempt(attempt_id, lock=True)
        if not attempt:
            raise MockExamStateError("실전 모의고사 응시 기록을 찾을 수 없습니다.")
        if attempt.exam_mode == self.FINAL_MODE:
            return attempt, None, {}, True
        meta = self._get_meta_record(attempt_id)
        if not meta:
            raise MockExamStateError("실전 모의고사 진행 정보가 없습니다.")
        config = self._decode_config(meta)
        if config.get("phase") == "submitted":
            return attempt, meta, config, True
        if self.is_expired(attempt, now):
            self._finalize_locked(attempt, meta, config, "expired", now)
            db_session.commit()
            return attempt, meta, config, True
        return attempt, meta, config, False

    def save_answer(self, attempt_id: int, question_id: str, form_data: Dict[str, Any]) -> bool:
        now = self._now()
        try:
            attempt, meta, config, finalized = self._active_locked(attempt_id, now)
            if finalized:
                return True
            questions = self._resolve_questions(config)
            question = next((q for q in questions if q["id"] == question_id), None)
            if not question:
                raise MockExamStateError("저장할 문항을 찾을 수 없습니다.")

            parsed = self.exam_service.parse_submission(form_data, [question])
            answer = parsed["answers"].get(question_id, self._empty_answer(question))
            record = db_session.scalar(select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_id == question_id,
                AnswerRecord.question_type != self.META_QUESTION_TYPE,
            ).with_for_update())
            if not record:
                raise MockExamStateError("저장할 답안 레코드를 찾을 수 없습니다.")
            record.user_answer = self._serialize_answer(answer)

            practical_ids = {q["id"] for q in questions if q["type"] == "practical"}
            selected_id = str(form_data.get("selected_practical_id", "")).strip()
            if selected_id in practical_ids:
                config["selected_practical_id"] = selected_id

            flags = set(config.get("review_flags", []))
            if str(form_data.get("review_flag", "")) == "1":
                flags.add(question_id)
            else:
                flags.discard(question_id)
            config["review_flags"] = [qid for qid in config["question_ids"] if qid in flags]
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()
            return False
        except Exception:
            db_session.rollback()
            raise

    def toggle_flag(self, attempt_id: int, question_id: str) -> bool:
        now = self._now()
        try:
            attempt, meta, config, finalized = self._active_locked(attempt_id, now)
            if finalized:
                return True
            if question_id not in config["question_ids"]:
                raise MockExamStateError("다시 보기 상태를 변경할 문항을 찾을 수 없습니다.")
            flags = set(config.get("review_flags", []))
            if question_id in flags:
                flags.remove(question_id)
            else:
                flags.add(question_id)
            config["review_flags"] = [qid for qid in config["question_ids"] if qid in flags]
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()
            return False
        except Exception:
            db_session.rollback()
            raise

    @staticmethod
    def _achievement(item: Dict[str, Any]) -> tuple[str, bool]:
        q_type = item.get("type", "short")
        earned = float(item.get("earned_score", 0.0))
        maximum = float(item.get("max_score", 0.0))
        if q_type == "practical" and not item.get("is_selected", True):
            return "unselected", False
        if maximum > 0 and earned >= maximum:
            return "sufficient", True
        if earned > 0:
            return "partial", False
        return "incorrect", False

    def _finalize_locked(
        self,
        attempt: ExamAttempt,
        meta: AnswerRecord,
        config: Dict[str, Any],
        reason: str,
        now: datetime,
    ) -> ExamAttempt:
        if attempt.exam_mode == self.FINAL_MODE or config.get("phase") == "submitted":
            return attempt

        questions = self._resolve_questions(config)
        records = {record.question_id: record for record in self._get_question_records(attempt.id)}
        if len(records) != self.CANDIDATE_COUNT:
            raise MockExamStateError("저장된 답안 구성이 올바르지 않습니다.")
        answers = {qid: record.get_parsed_answer() for qid, record in records.items()}
        submission = {
            "selected_practical_id": config.get("selected_practical_id"),
            "answers": answers,
        }
        result = Grader.grade_full_exam(questions, submission)
        details = {item.get("question_id"): item for item in result.get("details", [])}
        for question in questions:
            item = details.get(question["id"])
            if not item:
                raise MockExamStateError("채점 결과에서 문항 정보를 찾을 수 없습니다.")
            record = records[question["id"]]
            status, correct = self._achievement(item)
            record.earned_score = float(item.get("earned_score", 0.0))
            record.max_score = float(item.get("max_score", 0.0))
            record.achievement_status = status
            record.is_correct = correct
            sub_results = item.get("sub_results")
            record.self_eval_data = json.dumps(sub_results, ensure_ascii=False) if sub_results else None

        summary = result.get("summary", {})
        attempt.exam_mode = self.FINAL_MODE
        attempt.total_score = float(result.get("total_score", 0.0))
        attempt.short_score = float(summary.get("short", {}).get("earned", 0.0))
        attempt.descriptive_score = float(summary.get("descriptive", {}).get("earned", 0.0))
        attempt.practical_score = float(summary.get("practical", {}).get("earned", 0.0))
        attempt.selected_practical_id = config.get("selected_practical_id")
        attempt.is_passed = bool(result.get("is_passed", False))
        attempt.submitted_at = now
        elapsed = int((now - attempt.started_at).total_seconds()) if attempt.started_at else 0
        attempt.duration_seconds = max(0, min(elapsed, self.DURATION_SECONDS))
        # Active-only metadata must not enter History, Wrong Notes, or analytics.
        # The finalized ExamAttempt mode is the idempotent terminal marker.
        db_session.delete(meta)
        return attempt

    def finalize(self, attempt_id: int, reason: str = "manual", now: Optional[datetime] = None) -> ExamAttempt:
        current_now = now or self._now()
        try:
            attempt = self.get_attempt(attempt_id, lock=True)
            if not attempt:
                raise MockExamStateError("실전 모의고사 응시 기록을 찾을 수 없습니다.")
            if attempt.exam_mode == self.FINAL_MODE:
                return attempt
            meta = self._get_meta_record(attempt_id)
            if not meta:
                raise MockExamStateError("실전 모의고사 진행 정보가 없습니다.")
            config = self._decode_config(meta)
            final_reason = "expired" if self.is_expired(attempt, current_now) else reason
            self._finalize_locked(attempt, meta, config, final_reason, current_now)
            db_session.commit()
            return attempt
        except Exception:
            db_session.rollback()
            raise

    def get_recent_owner_attempts(self, limit: int = 5) -> List[Dict[str, Any]]:
        attempts = list(db_session.scalars(
            select(ExamAttempt)
            .where(ExamAttempt.exam_mode == self.ACTIVE_MODE, ExamAttempt.is_owner.is_(True))
            .order_by(desc(ExamAttempt.created_at))
            .limit(limit)
        ).all())
        recent = []
        for attempt in attempts:
            if self.finalize_if_expired(attempt.id):
                continue
            state = self.get_state(attempt.id)
            if state:
                recent.append(state)
        return recent
