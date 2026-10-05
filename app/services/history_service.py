import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy import select, func, desc
from app.models.database import db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader

class HistoryService:
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()

    def save_exam_attempt(
        self,
        exam_mode: str,
        seed: Optional[int],
        selected_practical_id: Optional[str],
        grading_result: Dict[str, Any],
        answers: Dict[str, Any],
        started_at: Optional[datetime] = None,
        duration_seconds: Optional[int] = None,
        submission_token: Optional[str] = None,
        is_owner: bool = True
    ) -> ExamAttempt:
        """
        시험 채점 결과와 수험자 답안을 원자적으로 DB에 저장합니다.
        동일 submission_token이 이미 저장된 경우 멱등성을 보장하여 기존 attempt를 반환합니다.
        """
        # 1. 멱등성 1차 검사: 동일 submission_token 존재 여부 확인
        clean_token = None
        if submission_token:
            cleaned = str(submission_token).strip()
            if cleaned:
                clean_token = cleaned
                existing = db_session.scalar(
                    select(ExamAttempt).where(ExamAttempt.submission_token == clean_token)
                )
                if existing:
                    return existing

        total_score = float(grading_result.get("total_score", 0.0))
        summary = grading_result.get("summary", {})
        short_score = float(summary.get("short", {}).get("earned", 0.0))
        desc_score = float(summary.get("descriptive", {}).get("earned", 0.0))
        prac_score = float(summary.get("practical", {}).get("earned", 0.0))
        is_passed = bool(grading_result.get("is_passed", False))

        attempt = ExamAttempt(
            submission_token=clean_token,
            exam_mode=exam_mode,
            seed=seed,
            started_at=started_at,
            submitted_at=datetime.now(),
            duration_seconds=duration_seconds,
            total_score=total_score,
            short_score=short_score,
            descriptive_score=desc_score,
            practical_score=prac_score,
            selected_practical_id=selected_practical_id,
            is_passed=is_passed,
            is_owner=is_owner,
            created_at=datetime.now()
        )

        try:
            db_session.add(attempt)
            db_session.flush()  # attempt.id 생성

            details = grading_result.get("details", [])
            for item in details:
                q_id = item.get("question_id")
                q_type = item.get("type", "short")
                earned = float(item.get("earned_score", 0.0))
                max_sc = float(item.get("max_score", 0.0))
                user_raw_ans = answers.get(q_id)

                # 성취 상태(achievement_status) 판정
                is_selected = item.get("is_selected", True)
                if q_type == "practical" and not is_selected:
                    status = "unselected"
                    is_correct = False
                elif max_sc > 0 and earned >= max_sc:
                    status = "sufficient"
                    is_correct = True
                elif earned > 0:
                    status = "partial"
                    is_correct = False
                else:
                    status = "incorrect"
                    is_correct = False

                # 사용자 답안 직렬화
                if isinstance(user_raw_ans, (dict, list)):
                    user_ans_str = json.dumps(user_raw_ans, ensure_ascii=False)
                elif user_raw_ans is not None:
                    user_ans_str = str(user_raw_ans)
                else:
                    user_ans_str = ""

                # 세부 루브릭 / 소문항 채점 내역
                sub_results = item.get("sub_results")
                self_eval_str = json.dumps(sub_results, ensure_ascii=False) if sub_results else None

                ans_record = AnswerRecord(
                    attempt_id=attempt.id,
                    question_id=q_id,
                    question_type=q_type,
                    user_answer=user_ans_str,
                    earned_score=earned,
                    max_score=max_sc,
                    achievement_status=status,
                    is_correct=is_correct,
                    self_eval_data=self_eval_str,
                    created_at=datetime.now()
                )
                db_session.add(ans_record)

            db_session.commit()
            return attempt
        except Exception as e:
            db_session.rollback()
            # 2. Race Condition 방어: 동시 제출로 인한 DB UNIQUE 제약조건 위반 시 기존 레코드 반환
            from sqlalchemy.exc import IntegrityError
            if clean_token and isinstance(e, IntegrityError):
                existing = db_session.scalar(
                    select(ExamAttempt).where(ExamAttempt.submission_token == clean_token)
                )
                if existing:
                    return existing
            raise

    def get_attempts(self, limit: int = 20, offset: int = 0, is_owner: bool = True) -> List[ExamAttempt]:
        """응시 이력 목록을 최신순으로 조회합니다 (기본적으로 Owner 전용)."""
        stmt = (
            select(ExamAttempt)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode != "practice",
            )
            .order_by(desc(ExamAttempt.created_at))
            .limit(limit)
            .offset(offset)
        )
        return list(db_session.scalars(stmt).all())

    def get_attempt_count(self, is_owner: bool = True) -> int:
        """총 응시 횟수 반환 (기본적으로 Owner 전용)"""
        stmt = select(func.count(ExamAttempt.id)).where(
            ExamAttempt.is_owner == is_owner,
            ExamAttempt.exam_mode != "practice",
        )
        return db_session.scalar(stmt) or 0

    def get_attempt_by_id(self, attempt_id: int) -> Optional[ExamAttempt]:
        """Attempt 단건 조회"""
        stmt = select(ExamAttempt).where(ExamAttempt.id == attempt_id)
        return db_session.scalar(stmt)

    def get_attempt_detail(self, attempt_id: int) -> Optional[Dict[str, Any]]:
        """
        특정 응시 회차의 상세 정보와 각 문항의 원본 메타데이터(출처, 루브릭 등)를 병합하여 반환합니다.
        DB에 본문을 중복 저장하지 않고 DataLoader의 최신 데이터와 동적 결합합니다.
        """
        attempt = self.get_attempt_by_id(attempt_id)
        if not attempt or attempt.exam_mode == "practice":
            return None

        enriched_answers = []
        for ans in attempt.answers:
            q_meta = self.loader.get_question_by_id(ans.question_id) or {}
            
            ans_info = ans.to_dict()
            ans_info["question_text"] = q_meta.get("question", "")
            ans_info["category"] = q_meta.get("category", "")
            ans_info["concept_id"] = q_meta.get("concept_id")
            ans_info["concept_name"] = q_meta.get("concept_name")
            ans_info["source_info"] = q_meta.get("source_info")
            ans_info["source_page"] = q_meta.get("source_page")
            ans_info["model_answer"] = q_meta.get("model_answer", "")
            ans_info["explanation"] = q_meta.get("explanation", "")
            ans_info["deep_explanation"] = self.loader.get_explanation_for_question(ans.question_id)
            ans_info["sub_questions"] = q_meta.get("sub_questions", [])
            ans_info["accepted_answers"] = q_meta.get("accepted_answers", [])
            
            enriched_answers.append(ans_info)

        data = attempt.to_dict()
        data["answers"] = enriched_answers
        return data

    def delete_attempt(self, attempt_id: int) -> bool:
        """특정 응시 기록 삭제"""
        attempt = self.get_attempt_by_id(attempt_id)
        if not attempt:
            return False
        try:
            db_session.delete(attempt)
            db_session.commit()
            return True
        except Exception:
            db_session.rollback()
            raise
