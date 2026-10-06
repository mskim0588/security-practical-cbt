import json
import random
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, select

from app.models.database import db_session
from app.models.history import AnswerRecord, ExamAttempt
from app.services.data_loader import DataLoader
from app.services.descriptive_training_evaluator import DescriptiveTrainingEvaluator
from app.services.exam_service import ExamService


class DescriptiveTrainingStateError(RuntimeError):
    """Raised when persisted descriptive-training state cannot be restored safely."""


class DescriptiveTrainingService:
    MODE = "descriptive_training"
    META_QUESTION_ID = "__descriptive_training_config__"
    META_QUESTION_TYPE = "desc_train_meta"
    VALID_SCOPE_KINDS = ("all", "category")
    VALID_COUNTS = (5, 10, 0)

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.exam_service = ExamService(self.loader)

    def get_setup_options(self) -> Dict[str, Any]:
        questions = [q for q in self.loader.get_enriched_questions() if q.get("type") == "descriptive"]
        categories = sorted({q.get("category", "") for q in questions if q.get("category")})
        return {
            "categories": [
                {
                    "value": category,
                    "label": category,
                    "count": sum(1 for q in questions if q.get("category") == category),
                }
                for category in categories
            ],
            "total_questions": len(questions),
        }

    def _select_questions(self, scope_kind: str, scope_value: str, count: int) -> List[Dict[str, Any]]:
        if scope_kind not in self.VALID_SCOPE_KINDS:
            raise ValueError("지원하지 않는 문제 범위입니다.")
        if count not in self.VALID_COUNTS:
            raise ValueError("학습 문항 수는 5문항, 10문항 또는 전체 중에서 선택해 주세요.")

        questions = [q for q in self.loader.get_enriched_questions() if q.get("type") == "descriptive"]
        if scope_kind == "category":
            valid_categories = {q.get("category") for q in questions}
            if scope_value not in valid_categories:
                raise ValueError("유효한 카테고리를 선택해 주세요.")
            questions = [q for q in questions if q.get("category") == scope_value]
        if not questions:
            raise ValueError("선택한 범위에 학습할 서술형 문제가 없습니다.")
        return questions

    def create_session(
        self,
        scope_kind: str,
        scope_value: str = "",
        count: int = 5,
        is_owner: bool = True,
    ) -> ExamAttempt:
        candidates = self._select_questions(scope_kind, scope_value, count)
        seed = secrets.randbelow(2_147_483_647)
        question_ids = [q["id"] for q in candidates]
        random.Random(seed).shuffle(question_ids)
        if count:
            question_ids = question_ids[:count]
        now = datetime.now()
        attempt = ExamAttempt(
            submission_token=f"desc-training-{secrets.token_urlsafe(28)}",
            exam_mode=self.MODE,
            seed=seed,
            started_at=now,
            submitted_at=now,
            total_score=0.0,
            short_score=0.0,
            descriptive_score=0.0,
            practical_score=0.0,
            selected_practical_id=None,
            is_passed=False,
            is_owner=is_owner,
            created_at=now,
        )
        config = {
            "version": 1,
            "scope_kind": scope_kind,
            "scope_value": scope_value if scope_kind == "category" else "",
            "question_ids": question_ids,
            "current_index": 0,
            "phase": "question",
            "latest_record_id": None,
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
            db_session.commit()
            return attempt
        except Exception:
            db_session.rollback()
            raise

    def get_attempt(self, attempt_id: int, lock: bool = False) -> Optional[ExamAttempt]:
        stmt = select(ExamAttempt).where(
            ExamAttempt.id == attempt_id,
            ExamAttempt.exam_mode == self.MODE,
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
        required = {"scope_kind", "question_ids", "current_index", "phase", "latest_record_id"}
        if not isinstance(config, dict) or not required.issubset(config):
            raise DescriptiveTrainingStateError("서술형 훈련 진행 정보를 복구할 수 없습니다.")
        if not isinstance(config.get("question_ids"), list) or not config["question_ids"]:
            raise DescriptiveTrainingStateError("서술형 훈련 문제 구성을 복구할 수 없습니다.")
        return config

    def _get_answer_records(self, attempt_id: int) -> List[AnswerRecord]:
        return list(db_session.scalars(
            select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_type != self.META_QUESTION_TYPE,
            ).order_by(AnswerRecord.id)
        ).all())

    @staticmethod
    def _training_payload(record: AnswerRecord) -> Dict[str, Any]:
        payload = record.get_parsed_self_eval()
        if not isinstance(payload, dict) or not isinstance(payload.get("evaluation"), dict):
            raise DescriptiveTrainingStateError("저장된 서술형 평가 결과를 복구할 수 없습니다.")
        return payload["evaluation"]

    @staticmethod
    def _scope_label(config: Dict[str, Any]) -> str:
        if config.get("scope_kind") == "category":
            return f"카테고리 · {config.get('scope_value', '')}"
        return "전체 서술형"

    @staticmethod
    def _structure_hint(prompt: str) -> str:
        normalized = str(prompt or "")
        if any(word in normalized for word in ("절차", "순서", "단계", "명령")):
            return "대상 → 수행 절차 또는 명령 → 기대 결과 순서로 작성하세요."
        if any(word in normalized for word in ("의미", "설명", "정의")):
            return "대상이 무엇을 뜻하는지와 보안상 결과를 한 문장으로 연결하세요."
        if any(word in normalized for word in ("설정", "방안", "강화", "통제", "대응")):
            return "구체적인 설정·조치를 먼저 쓰고 목적 또는 효과를 덧붙이세요."
        return "요구 항목의 핵심 조치와 근거 또는 효과를 함께 작성하세요."

    @classmethod
    def _learner_question(cls, question: Dict[str, Any]) -> Dict[str, Any]:
        sub_questions = []
        for sub in question.get("sub_questions", []):
            sub_questions.append({
                "sub_id": str(sub.get("sub_id")),
                "score": sub.get("score", 0),
                "prompt": sub.get("prompt", ""),
                "structure_hint": cls._structure_hint(sub.get("prompt", "")),
            })
        return {
            "id": question.get("id"),
            "category": question.get("category", ""),
            "score": question.get("score", 0),
            "question": question.get("question", ""),
            "sub_questions": sub_questions,
            "concept_id": question.get("concept_id"),
            "concept_name": question.get("concept_name", ""),
        }

    @staticmethod
    def _answer_text(answer: Any) -> str:
        if isinstance(answer, dict):
            return "\n".join(f"[{key}] {value or '(미작성)'}" for key, value in answer.items())
        return str(answer or "(미작성)")

    def get_state(self, attempt_id: int) -> Optional[Dict[str, Any]]:
        attempt = self.get_attempt(attempt_id)
        if not attempt:
            return None
        meta = self._get_meta_record(attempt_id)
        if not meta:
            raise DescriptiveTrainingStateError("서술형 훈련 진행 정보가 없습니다.")
        config = self._decode_config(meta)
        questions = self.exam_service.get_questions_by_ids(config["question_ids"])
        if len(questions) != len(config["question_ids"]):
            raise DescriptiveTrainingStateError("문제은행 변경으로 기존 훈련을 안전하게 복구할 수 없습니다.")
        current_index = int(config["current_index"])
        if current_index < 0 or current_index >= len(questions):
            raise DescriptiveTrainingStateError("현재 문제 위치를 복구할 수 없습니다.")
        question = questions[current_index]
        records = self._get_answer_records(attempt_id)
        result = None
        if config["phase"] in ("graded", "complete") and config.get("latest_record_id"):
            record = next((item for item in records if item.id == config["latest_record_id"]), None)
            if not record:
                raise DescriptiveTrainingStateError("최근 평가 결과를 복구할 수 없습니다.")
            evaluation = self._training_payload(record)
            answer = record.get_parsed_answer()
            result = {
                **evaluation,
                "user_answer": answer,
                "user_answer_text": self._answer_text(answer),
                "deep_explanation": self.loader.get_explanation_for_question(question["id"]),
                "concept_id": question.get("concept_id"),
                "concept_name": question.get("concept_name", ""),
            }

        sufficient = sum(1 for item in records if item.achievement_status == "sufficient")
        partial = sum(1 for item in records if item.achievement_status == "partial")
        incorrect = sum(1 for item in records if item.achievement_status == "incorrect")
        return {
            "attempt_id": attempt.id,
            "is_owner": attempt.is_owner,
            "phase": config["phase"],
            "scope_label": self._scope_label(config),
            "current_index": current_index,
            "question_number": current_index + 1,
            "total_questions": len(questions),
            "answered_count": len(records),
            "status_counts": {"sufficient": sufficient, "partial": partial, "incorrect": incorrect},
            "question": self._learner_question(question),
            "result": result,
            "is_final_complete": config["phase"] == "complete",
        }

    def submit_answer(self, attempt_id: int, form_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            attempt = self.get_attempt(attempt_id, lock=True)
            if not attempt:
                raise DescriptiveTrainingStateError("서술형 훈련 세션을 찾을 수 없습니다.")
            meta = self._get_meta_record(attempt_id)
            if not meta:
                raise DescriptiveTrainingStateError("서술형 훈련 진행 정보가 없습니다.")
            config = self._decode_config(meta)
            if config["phase"] != "question":
                db_session.rollback()
                return self.get_state(attempt_id)

            questions = self.exam_service.get_questions_by_ids(config["question_ids"])
            current_index = int(config["current_index"])
            question = questions[current_index]
            parsed = self.exam_service.parse_submission(form_data, [question])
            answer = parsed["answers"].get(question["id"], {})
            evaluation = DescriptiveTrainingEvaluator.evaluate(question, answer)
            now = datetime.now()
            status = evaluation["achievement_status"]
            record = AnswerRecord(
                attempt_id=attempt.id,
                question_id=question["id"],
                question_type="descriptive",
                user_answer=json.dumps(answer, ensure_ascii=False),
                earned_score=float(evaluation["earned_score"]),
                max_score=float(evaluation["max_score"]),
                achievement_status=status,
                is_correct=status == "sufficient",
                self_eval_data=json.dumps({
                    "descriptive_training": {"index": current_index},
                    "evaluation": evaluation,
                }, ensure_ascii=False),
                created_at=now,
            )
            db_session.add(record)
            db_session.flush()
            config["latest_record_id"] = record.id
            config["phase"] = "complete" if current_index == len(questions) - 1 else "graded"
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)

            all_records = self._get_answer_records(attempt_id)
            earned_total = sum(item.earned_score for item in all_records)
            max_total = sum(item.max_score for item in all_records)
            attempt.descriptive_score = round(earned_total, 1)
            attempt.total_score = round((earned_total / max_total) * 100, 1) if max_total else 0.0
            attempt.submitted_at = now
            if config["phase"] == "complete" and attempt.started_at:
                attempt.duration_seconds = max(0, int((now - attempt.started_at).total_seconds()))
            db_session.commit()
            return self.get_state(attempt_id)
        except Exception:
            db_session.rollback()
            raise

    def advance(self, attempt_id: int) -> Dict[str, Any]:
        try:
            attempt = self.get_attempt(attempt_id, lock=True)
            if not attempt:
                raise DescriptiveTrainingStateError("서술형 훈련 세션을 찾을 수 없습니다.")
            meta = self._get_meta_record(attempt_id)
            if not meta:
                raise DescriptiveTrainingStateError("서술형 훈련 진행 정보가 없습니다.")
            config = self._decode_config(meta)
            if config["phase"] != "graded":
                db_session.rollback()
                return self.get_state(attempt_id)
            config["current_index"] = int(config["current_index"]) + 1
            config["phase"] = "question"
            config["latest_record_id"] = None
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()
            return self.get_state(attempt_id)
        except Exception:
            db_session.rollback()
            raise

    def get_recent_owner_sessions(self, limit: int = 5) -> List[Dict[str, Any]]:
        attempts = list(db_session.scalars(
            select(ExamAttempt).where(
                ExamAttempt.exam_mode == self.MODE,
                ExamAttempt.is_owner.is_(True),
            ).order_by(desc(ExamAttempt.created_at)).limit(limit)
        ).all())
        sessions = []
        for attempt in attempts:
            try:
                state = self.get_state(attempt.id)
            except DescriptiveTrainingStateError:
                continue
            if state:
                sessions.append({**state, "created_at": attempt.created_at})
        return sessions
