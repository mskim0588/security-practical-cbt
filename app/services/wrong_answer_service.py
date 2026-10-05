from typing import Dict, List, Any, Optional
from sqlalchemy import select, desc
from app.models.database import db_session
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader

class WrongAnswerService:
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()

    def get_wrong_questions(
        self,
        type_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        category_filter: Optional[str] = None,
        sort_by: str = "latest",
        is_owner: bool = True
    ) -> List[Dict[str, Any]]:
        """
        오답노트 대상 문항 목록을 동적으로 집계하여 반환합니다 (기본적으로 Owner 전용).
        - 실무형 미선택 문항('unselected')은 모수에서 제외
        - 최신 응시 상태가 'incorrect' 또는 'partial'인 문항만 추출
        """
        stmt = (
            select(AnswerRecord)
            .join(ExamAttempt, AnswerRecord.attempt_id == ExamAttempt.id)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode != "practice",
                AnswerRecord.achievement_status != "unselected"
            )
            .order_by(desc(AnswerRecord.created_at), desc(AnswerRecord.id))
        )
        all_records = list(db_session.scalars(stmt).all())

        # question_id 별로 그룹화 (이미 최신순 정렬되어 있으므로 첫 번째 레코드가 최신 상태)
        grouped: Dict[str, List[AnswerRecord]] = {}
        for rec in all_records:
            grouped.setdefault(rec.question_id, []).append(rec)

        results = []
        for q_id, records in grouped.items():
            latest = records[0]
            # 최신 상태가 오답(incorrect)이거나 부분감점(partial)인 경우만 오답노트에 포함
            if latest.achievement_status not in ("incorrect", "partial"):
                continue

            q_meta = self.loader.get_question_by_id(q_id) or {}
            q_type = q_meta.get("type", latest.question_type)
            category = q_meta.get("category", "")

            # 필터 적용
            if type_filter and type_filter != "all" and q_type != type_filter:
                continue
            if status_filter and status_filter != "all" and latest.achievement_status != status_filter:
                continue
            if category_filter and category_filter != "all" and category != category_filter:
                continue

            total_attempts = len(records)
            incorrect_count = sum(1 for r in records if r.achievement_status == "incorrect")
            partial_count = sum(1 for r in records if r.achievement_status == "partial")
            sufficient_count = sum(1 for r in records if r.achievement_status == "sufficient")

            fail_count = incorrect_count + partial_count
            fail_rate = round((fail_count / total_attempts) * 100, 1) if total_attempts > 0 else 0.0

            results.append({
                "question_id": q_id,
                "type": q_type,
                "category": category,
                "concept_id": q_meta.get("concept_id"),
                "concept_name": q_meta.get("concept_name"),
                "source_info": q_meta.get("source_info"),
                "source_page": q_meta.get("source_page"),
                "question_text": q_meta.get("question", ""),
                "model_answer": q_meta.get("model_answer", ""),
                "explanation": q_meta.get("explanation", ""),
                "deep_explanation": self.loader.get_explanation_for_question(q_id),
                "sub_questions": q_meta.get("sub_questions", []),
                "accepted_answers": q_meta.get("accepted_answers", []),
                "latest_status": latest.achievement_status,
                "latest_earned": latest.earned_score,
                "max_score": latest.max_score,
                "latest_user_answer": latest.get_parsed_answer(),
                "latest_date": latest.created_at,
                "total_attempts": total_attempts,
                "incorrect_count": incorrect_count,
                "partial_count": partial_count,
                "sufficient_count": sufficient_count,
                "fail_count": fail_count,
                "fail_rate": fail_rate
            })

        # 정렬
        if sort_by == "frequency":
            # 오답 횟수 많은 순 -> 최신순
            results.sort(key=lambda x: (x["fail_count"], x["latest_date"]), reverse=True)
        else:
            # 최신순 (기본값)
            results.sort(key=lambda x: x["latest_date"], reverse=True)

        return results

    def get_wrong_question_count(self, is_owner: bool = True) -> int:
        """현재 미해결 오답 문항 수 반환 (기본적으로 Owner 전용)"""
        wrong_list = self.get_wrong_questions(is_owner=is_owner)
        return len(wrong_list)

    def get_wrong_question_detail(self, question_id: str, is_owner: bool = True) -> Optional[Dict[str, Any]]:
        """
        특정 문항의 상세 정보와 과거 모든 응시 이력(타임라인)을 반환합니다 (기본적으로 Owner 전용).
        """
        q_meta = self.loader.get_question_by_id(question_id)
        if not q_meta:
            return None

        stmt = (
            select(AnswerRecord)
            .join(ExamAttempt, AnswerRecord.attempt_id == ExamAttempt.id)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode != "practice",
            )
            .where(AnswerRecord.question_id == question_id)
            .where(AnswerRecord.achievement_status != "unselected")
            .order_by(desc(AnswerRecord.created_at))
        )
        records = list(db_session.scalars(stmt).all())

        history_timeline = []
        for r in records:
            history_timeline.append({
                "attempt_id": r.attempt_id,
                "date": r.created_at,
                "status": r.achievement_status,
                "earned_score": r.earned_score,
                "max_score": r.max_score,
                "user_answer": r.get_parsed_answer(),
                "self_eval_data": r.get_parsed_self_eval()
            })

        total_attempts = len(records)
        incorrect_count = sum(1 for r in records if r.achievement_status == "incorrect")
        partial_count = sum(1 for r in records if r.achievement_status == "partial")
        sufficient_count = sum(1 for r in records if r.achievement_status == "sufficient")

        latest_status = records[0].achievement_status if records else "unattempted"
        deep_explanation = self.loader.get_explanation_for_question(question_id)
        
        # 소속 Concept의 전체 문항 수 계산 (학습 연계용)
        concept_id = q_meta.get("concept_id")
        related_questions_count = 0
        if concept_id:
            related_questions_count = sum(1 for q in self.loader.load_questions() if q.get("concept_id") == concept_id)

        return {
            "question": q_meta,
            "latest_status": latest_status,
            "total_attempts": total_attempts,
            "incorrect_count": incorrect_count,
            "partial_count": partial_count,
            "sufficient_count": sufficient_count,
            "history": history_timeline,
            "deep_explanation": deep_explanation,
            "related_questions_count": related_questions_count
        }
