from datetime import datetime
from typing import Optional, List, Dict, Any
import json
from sqlalchemy import Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.database import Base

LEARNING_ONLY_EXAM_MODES = ("practice", "descriptive_training")

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    submission_token: Mapped[Optional[str]] = mapped_column(String(64), unique=True, index=True, nullable=True)
    exam_mode: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    seed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    total_score: Mapped[float] = mapped_column(Float, default=0.0)
    short_score: Mapped[float] = mapped_column(Float, default=0.0)
    descriptive_score: Mapped[float] = mapped_column(Float, default=0.0)
    practical_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    selected_practical_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_owner: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    # 관계 정의 (Attempt 삭제 시 종속 AnswerRecord 연쇄 삭제)
    answers: Mapped[List["AnswerRecord"]] = relationship(
        "AnswerRecord",
        back_populates="attempt",
        cascade="all, delete-orphan",
        order_by="AnswerRecord.id"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "submission_token": self.submission_token,
            "exam_mode": self.exam_mode,
            "seed": self.seed,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "submitted_at": self.submitted_at.isoformat() if self.submitted_at else None,
            "duration_seconds": self.duration_seconds,
            "total_score": self.total_score,
            "short_score": self.short_score,
            "descriptive_score": self.descriptive_score,
            "practical_score": self.practical_score,
            "selected_practical_id": self.selected_practical_id,
            "is_passed": self.is_passed,
            "is_owner": self.is_owner,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "answers_count": len(self.answers) if self.answers else 0
        }


class AnswerRecord(Base):
    __tablename__ = "answer_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    question_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # 사용자 답안 저장 (단답형 텍스트 / 서술형·실무형 답안 딕셔너리의 JSON 직렬화 문자열)
    user_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    earned_score: Mapped[float] = mapped_column(Float, default=0.0)
    max_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # 성취 상태: 'sufficient'(정답) | 'partial'(부분정답) | 'incorrect'(오답) | 'unselected'(미선택 실무형)
    achievement_status: Mapped[str] = mapped_column(String(20), index=True, default="incorrect")
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 서술형/실무형 세부 자가채점/루브릭 평가 내역 (JSON)
    self_eval_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)

    # 관계 정의
    attempt: Mapped["ExamAttempt"] = relationship("ExamAttempt", back_populates="answers")

    # 복합 인덱스 (통계 및 문항별 이력 검색 최적화)
    __table_args__ = (
        Index("idx_answer_attempt_question", "attempt_id", "question_id"),
        Index("idx_answer_question_status", "question_id", "achievement_status"),
    )

    def get_parsed_answer(self) -> Any:
        if not self.user_answer:
            return ""
        try:
            return json.loads(self.user_answer)
        except Exception:
            return self.user_answer

    def get_parsed_self_eval(self) -> Any:
        if not self.self_eval_data:
            return None
        try:
            return json.loads(self.self_eval_data)
        except Exception:
            return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attempt_id": self.attempt_id,
            "question_id": self.question_id,
            "question_type": self.question_type,
            "user_answer": self.get_parsed_answer(),
            "earned_score": self.earned_score,
            "max_score": self.max_score,
            "achievement_status": self.achievement_status,
            "is_correct": self.is_correct,
            "self_eval_data": self.get_parsed_self_eval(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
