import json
import random
import secrets
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, select

from app.models.database import db_session
from app.models.history import AnswerRecord, ExamAttempt
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService
from app.services.grader import Grader


class PracticeStateError(RuntimeError):
    """Raised when persisted practice state cannot be restored safely."""


class PracticeService:
    MODE = "practice"
    META_QUESTION_ID = "__practice_config__"
    META_QUESTION_TYPE = "practice_meta"
    VALID_ROUNDS = (1, 2, 3)
    VALID_SCOPE_KINDS = ("all", "category", "type")

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.exam_service = ExamService(self.loader)

    def get_setup_options(self) -> Dict[str, List[Dict[str, str]]]:
        questions = self.loader.get_enriched_questions()
        categories = sorted({q.get("category", "") for q in questions if q.get("category")})
        return {
            "categories": [{"value": value, "label": value} for value in categories],
            "question_types": [
                {"value": "short", "label": "단답형"},
                {"value": "descriptive", "label": "서술형"},
                {"value": "practical", "label": "실무형"},
            ],
        }

    def _select_questions(self, scope_kind: str, scope_value: str) -> List[Dict[str, Any]]:
        if scope_kind not in self.VALID_SCOPE_KINDS:
            raise ValueError("지원하지 않는 문제 범위입니다.")

        questions = self.loader.get_enriched_questions()
        if scope_kind == "category":
            valid = {q.get("category") for q in questions}
            if scope_value not in valid:
                raise ValueError("유효한 카테고리를 선택해 주세요.")
            questions = [q for q in questions if q.get("category") == scope_value]
        elif scope_kind == "type":
            valid = {q.get("type") for q in questions}
            if scope_value not in valid:
                raise ValueError("유효한 문제 유형을 선택해 주세요.")
            questions = [q for q in questions if q.get("type") == scope_value]

        if not questions:
            raise ValueError("선택한 범위에 학습할 문제가 없습니다.")
        return questions

    def create_session(
        self,
        rounds: int,
        scope_kind: str,
        scope_value: str = "",
        is_owner: bool = True,
    ) -> ExamAttempt:
        if rounds not in self.VALID_ROUNDS:
            raise ValueError("회독 수는 1, 2, 3 중에서 선택해 주세요.")

        questions = self._select_questions(scope_kind, scope_value)
        seed = secrets.randbelow(2_147_483_647)
        question_ids = [q["id"] for q in questions]
        random.Random(seed).shuffle(question_ids)

        now = datetime.now()
        attempt = ExamAttempt(
            submission_token=f"practice-{secrets.token_urlsafe(32)}",
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
            "rounds": rounds,
            "scope_kind": scope_kind,
            "scope_value": scope_value if scope_kind != "all" else "",
            "question_ids": question_ids,
            "current_round": 1,
            "current_index": 0,
            "phase": "question",
            "latest_record_id": None,
        }

        try:
            db_session.add(attempt)
            db_session.flush()
            db_session.add(
                AnswerRecord(
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
                )
            )
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
        return db_session.scalar(
            select(AnswerRecord).where(
                AnswerRecord.attempt_id == attempt_id,
                AnswerRecord.question_id == self.META_QUESTION_ID,
                AnswerRecord.question_type == self.META_QUESTION_TYPE,
            )
        )

    @staticmethod
    def _decode_config(meta: AnswerRecord) -> Dict[str, Any]:
        config = meta.get_parsed_self_eval()
        if not isinstance(config, dict):
            raise PracticeStateError("회독 학습 진행 정보를 복구할 수 없습니다.")
        required = {
            "rounds", "scope_kind", "question_ids", "current_round",
            "current_index", "phase", "latest_record_id",
        }
        if not required.issubset(config):
            raise PracticeStateError("회독 학습 진행 정보가 불완전합니다.")
        if not isinstance(config.get("question_ids"), list) or not config["question_ids"]:
            raise PracticeStateError("회독 학습 문제 구성을 복구할 수 없습니다.")
        return config

    def _get_answer_records(self, attempt_id: int) -> List[AnswerRecord]:
        return list(
            db_session.scalars(
                select(AnswerRecord)
                .where(
                    AnswerRecord.attempt_id == attempt_id,
                    AnswerRecord.question_type != self.META_QUESTION_TYPE,
                )
                .order_by(AnswerRecord.id)
            ).all()
        )

    @staticmethod
    def _practice_meta(record: AnswerRecord) -> Dict[str, Any]:
        payload = record.get_parsed_self_eval()
        if isinstance(payload, dict) and isinstance(payload.get("practice"), dict):
            return payload["practice"]
        return {}

    @staticmethod
    def _result_payload(record: AnswerRecord) -> Dict[str, Any]:
        payload = record.get_parsed_self_eval()
        if isinstance(payload, dict) and isinstance(payload.get("grading"), dict):
            return payload["grading"]
        raise PracticeStateError("저장된 문항 채점 결과를 복구할 수 없습니다.")

    @staticmethod
    def _status_for_result(result: Dict[str, Any]) -> str:
        earned = float(result.get("earned_score", 0.0))
        maximum = float(result.get("max_score", 0.0))
        if maximum > 0 and earned >= maximum:
            return "sufficient"
        if earned > 0:
            return "partial"
        return "incorrect"

    @staticmethod
    def _public_result(status: str) -> str:
        return {
            "sufficient": "correct",
            "partial": "partial",
            "incorrect": "wrong",
        }.get(status, "wrong")

    @staticmethod
    def _result_label(status: str) -> str:
        return {
            "sufficient": "정답",
            "partial": "부분정답",
            "incorrect": "오답",
        }.get(status, "오답")

    @staticmethod
    def _type_label(question_type: str) -> str:
        return {
            "short": "단답형",
            "descriptive": "서술형",
            "practical": "실무형",
        }.get(question_type, question_type)

    @staticmethod
    def _scope_label(config: Dict[str, Any]) -> str:
        if config.get("scope_kind") == "category":
            return f"카테고리 · {config.get('scope_value', '')}"
        if config.get("scope_kind") == "type":
            return f"문제 유형 · {PracticeService._type_label(config.get('scope_value', ''))}"
        return "전체 문제"

    @staticmethod
    def _learner_question(question: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": question.get("id"),
            "type": question.get("type"),
            "type_label": PracticeService._type_label(question.get("type", "")),
            "category": question.get("category", ""),
            "score": question.get("score", 0),
            "question": question.get("question", ""),
            "sub_questions": question.get("sub_questions", []),
            "answer": question.get("answer", ""),
            "accepted_answers": question.get("accepted_answers", []),
            "model_answer": question.get("model_answer", ""),
            "explanation": question.get("explanation", ""),
            "concept_id": question.get("concept_id"),
            "concept_name": question.get("concept_name", ""),
        }

    @staticmethod
    def _answer_text(answer: Any) -> str:
        if isinstance(answer, dict):
            return "\n".join(f"[{label}] {value or '(미작성)'}" for label, value in answer.items())
        if isinstance(answer, list):
            return "\n".join(str(value) for value in answer)
        return str(answer or "(미작성)")

    @staticmethod
    def _model_answer_text(question: Dict[str, Any], sub_results: List[Dict[str, Any]]) -> str:
        if question.get("model_answer"):
            return str(question["model_answer"])
        values = []
        for sub_result in sub_results:
            expected = sub_result.get("expected_answer")
            if expected:
                label = sub_result.get("label")
                values.append(f"[{label}] {expected}" if label and label != "단일답안" else str(expected))
        return "\n".join(values)

    def _round_summary(
        self,
        records: List[AnswerRecord],
        round_number: int,
        total_questions: int,
    ) -> Dict[str, Any]:
        round_records = [
            record for record in records
            if self._practice_meta(record).get("round") == round_number
        ]
        correct = sum(1 for record in round_records if record.achievement_status == "sufficient")
        partial = sum(1 for record in round_records if record.achievement_status == "partial")
        wrong = sum(1 for record in round_records if record.achievement_status == "incorrect")
        weighted_accuracy = round(
            ((correct + (0.5 * partial)) / len(round_records)) * 100, 1
        ) if round_records else 0.0
        needs_review = []
        for record in round_records:
            if record.achievement_status in ("partial", "incorrect"):
                question = self.loader.get_question_by_id(record.question_id) or {}
                needs_review.append({
                    "question_id": record.question_id,
                    "category": question.get("category", ""),
                    "result": self._public_result(record.achievement_status),
                    "result_label": self._result_label(record.achievement_status),
                })
        return {
            "round": round_number,
            "total": total_questions,
            "answered": len(round_records),
            "correct": correct,
            "partial": partial,
            "wrong": wrong,
            "weighted_accuracy": weighted_accuracy,
            "needs_review": needs_review,
        }

    def get_state(self, attempt_id: int) -> Optional[Dict[str, Any]]:
        attempt = self.get_attempt(attempt_id)
        if not attempt:
            return None
        meta = self._get_meta_record(attempt_id)
        if not meta:
            raise PracticeStateError("회독 학습 진행 정보가 없습니다.")
        config = self._decode_config(meta)
        question_ids = config["question_ids"]
        questions = self.exam_service.get_questions_by_ids(question_ids)
        if len(questions) != len(question_ids):
            raise PracticeStateError("문제은행 변경으로 기존 회독 학습을 안전하게 복구할 수 없습니다.")

        records = self._get_answer_records(attempt_id)
        current_round = int(config["current_round"])
        current_index = int(config["current_index"])
        if current_index < 0 or current_index >= len(questions):
            raise PracticeStateError("현재 문제 위치를 복구할 수 없습니다.")
        question = questions[current_index]

        current_round_records = [
            record for record in records
            if self._practice_meta(record).get("round") == current_round
        ]
        status_counts = {
            "correct": sum(1 for r in current_round_records if r.achievement_status == "sufficient"),
            "partial": sum(1 for r in current_round_records if r.achievement_status == "partial"),
            "wrong": sum(1 for r in current_round_records if r.achievement_status == "incorrect"),
        }
        question_records = [r for r in records if r.question_id == question["id"]]
        latest_for_question = question_records[-1] if question_records else None

        result = None
        latest_record_id = config.get("latest_record_id")
        if config["phase"] in ("graded", "round_complete", "complete") and latest_record_id:
            latest_record = next((r for r in records if r.id == latest_record_id), None)
            if not latest_record:
                raise PracticeStateError("최근 채점 결과를 복구할 수 없습니다.")
            grading = self._result_payload(latest_record)
            sub_results = grading.get("sub_results", [])
            missing_keywords = []
            for sub_result in sub_results:
                for keyword in sub_result.get("missing_keywords", []):
                    if keyword not in missing_keywords:
                        missing_keywords.append(keyword)
            result = {
                "record_id": latest_record.id,
                "status": self._public_result(latest_record.achievement_status),
                "status_label": self._result_label(latest_record.achievement_status),
                "earned_score": latest_record.earned_score,
                "max_score": latest_record.max_score,
                "user_answer": latest_record.get_parsed_answer(),
                "user_answer_text": self._answer_text(latest_record.get_parsed_answer()),
                "sub_results": sub_results,
                "model_answer": question.get("model_answer", ""),
                "model_answer_text": self._model_answer_text(question, sub_results),
                "accepted_answers": question.get("accepted_answers", []),
                "explanation": question.get("explanation", ""),
                "deep_explanation": self.loader.get_explanation_for_question(question["id"]),
                "missing_keywords": missing_keywords,
            }

        round_summary = None
        if config["phase"] in ("round_complete", "complete"):
            round_summary = self._round_summary(records, current_round, len(questions))

        return {
            "attempt_id": attempt.id,
            "is_owner": attempt.is_owner,
            "rounds": int(config["rounds"]),
            "current_round": current_round,
            "current_index": current_index,
            "question_number": current_index + 1,
            "total_questions": len(questions),
            "phase": config["phase"],
            "scope_label": self._scope_label(config),
            "question": self._learner_question(question),
            "result": result,
            "question_attempts": len(question_records),
            "latest_result": self._public_result(latest_for_question.achievement_status) if latest_for_question else None,
            "latest_result_label": self._result_label(latest_for_question.achievement_status) if latest_for_question else None,
            "round_answered": len(current_round_records),
            "status_counts": status_counts,
            "round_summary": round_summary,
            "is_final_complete": config["phase"] == "complete",
        }

    def _grade_question(self, question: Dict[str, Any], answer: Any) -> Dict[str, Any]:
        if question["type"] == "short":
            return Grader.grade_short_question(question, answer)
        if question["type"] == "descriptive":
            return Grader.grade_descriptive_question(question, answer)
        if question["type"] == "practical":
            return Grader.grade_practical_question(question, answer, True)
        raise PracticeStateError("지원하지 않는 문제 유형입니다.")

    def submit_answer(self, attempt_id: int, form_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            attempt = self.get_attempt(attempt_id, lock=True)
            if not attempt:
                raise PracticeStateError("회독 학습 세션을 찾을 수 없습니다.")
            meta = self._get_meta_record(attempt_id)
            if not meta:
                raise PracticeStateError("회독 학습 진행 정보가 없습니다.")
            config = self._decode_config(meta)

            # Phase is the idempotency boundary: refresh or repeated POST cannot add a second record.
            if config["phase"] != "question":
                db_session.rollback()
                return self.get_state(attempt_id)

            questions = self.exam_service.get_questions_by_ids(config["question_ids"])
            if len(questions) != len(config["question_ids"]):
                raise PracticeStateError("문제은행 변경으로 현재 답안을 안전하게 채점할 수 없습니다.")
            current_index = int(config["current_index"])
            question = questions[current_index]
            parsed = self.exam_service.parse_submission(form_data, [question])
            answer = parsed["answers"].get(question["id"], {})
            grading = self._grade_question(question, answer)
            status = self._status_for_result(grading)
            now = datetime.now()
            record = AnswerRecord(
                attempt_id=attempt.id,
                question_id=question["id"],
                question_type=question["type"],
                user_answer=json.dumps(answer, ensure_ascii=False) if isinstance(answer, (dict, list)) else str(answer or ""),
                earned_score=float(grading.get("earned_score", 0.0)),
                max_score=float(grading.get("max_score", 0.0)),
                achievement_status=status,
                is_correct=status == "sufficient",
                self_eval_data=json.dumps({
                    "practice": {
                        "round": int(config["current_round"]),
                        "index": current_index,
                    },
                    "grading": grading,
                }, ensure_ascii=False),
                created_at=now,
            )
            db_session.add(record)
            db_session.flush()

            config["latest_record_id"] = record.id
            is_last_question = current_index == len(questions) - 1
            if is_last_question:
                config["phase"] = "complete" if int(config["current_round"]) >= int(config["rounds"]) else "round_complete"
            else:
                config["phase"] = "graded"
            meta.self_eval_data = json.dumps(config, ensure_ascii=False)

            all_records = self._get_answer_records(attempt_id)
            correct = sum(1 for r in all_records if r.achievement_status == "sufficient")
            partial = sum(1 for r in all_records if r.achievement_status == "partial")
            attempt.total_score = round(((correct + 0.5 * partial) / len(all_records)) * 100, 1)
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
                raise PracticeStateError("회독 학습 세션을 찾을 수 없습니다.")
            meta = self._get_meta_record(attempt_id)
            if not meta:
                raise PracticeStateError("회독 학습 진행 정보가 없습니다.")
            config = self._decode_config(meta)

            if config["phase"] == "graded":
                config["current_index"] = int(config["current_index"]) + 1
                config["phase"] = "question"
                config["latest_record_id"] = None
            elif config["phase"] == "round_complete":
                config["current_round"] = int(config["current_round"]) + 1
                config["current_index"] = 0
                config["phase"] = "question"
                config["latest_record_id"] = None
            else:
                db_session.rollback()
                return self.get_state(attempt_id)

            meta.self_eval_data = json.dumps(config, ensure_ascii=False)
            db_session.commit()
            return self.get_state(attempt_id)
        except Exception:
            db_session.rollback()
            raise

    def get_recent_owner_sessions(self, limit: int = 5) -> List[Dict[str, Any]]:
        attempts = list(
            db_session.scalars(
                select(ExamAttempt)
                .where(ExamAttempt.exam_mode == self.MODE, ExamAttempt.is_owner.is_(True))
                .order_by(desc(ExamAttempt.created_at))
                .limit(limit)
            ).all()
        )
        sessions = []
        for attempt in attempts:
            try:
                state = self.get_state(attempt.id)
            except PracticeStateError:
                continue
            if state:
                sessions.append({
                    "attempt_id": state["attempt_id"],
                    "scope_label": state["scope_label"],
                    "rounds": state["rounds"],
                    "current_round": state["current_round"],
                    "question_number": state["question_number"],
                    "total_questions": state["total_questions"],
                    "phase": state["phase"],
                    "created_at": attempt.created_at,
                })
        return sessions
