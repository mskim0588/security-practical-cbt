"""Read-only presentation fields shared by stored Result and History views.

The caller must authorize the attempt before mapping it. No answer, rubric, or
grading data is loaded here, and stored scores are copied without recalculation.
"""

from collections.abc import Mapping
from datetime import datetime

from flask import url_for

from app.config import Config
from app.models.history import LEARNING_ONLY_EXAM_MODES


_MODE_LABELS = {
    "standard": ("📘 표준 모의고사", "📘 표준"),
    "random": ("🎲 랜덤 모의고사", "🎲 랜덤"),
    "wrong_review": ("🔥 오답 집중 모의고사", "🔥 오답집중"),
    "adaptive": ("🎯 취약점 맞춤 모의고사", "🎯 취약점"),
}


def _field(source, name):
    return source.get(name) if isinstance(source, Mapping) else getattr(source, name, None)


def _display_time(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, str):
        return value[:16].replace("T", " ")
    return "-"


def map_attempt_summary(source):
    """Copy canonical attempt fields from a model or its existing detail dict."""
    attempt_id = _field(source, "id")
    mode = _field(source, "exam_mode")
    total_score = _field(source, "total_score")
    submitted_at = _field(source, "submitted_at")
    is_finalized = mode not in LEARNING_ONLY_EXAM_MODES and submitted_at is not None
    is_scored = is_finalized and total_score is not None
    mode_label, mode_short_label = _MODE_LABELS.get(mode, (mode or "-", mode or "-"))
    is_owner = bool(_field(source, "is_owner"))

    return {
        "id": attempt_id,
        "exam_mode": mode,
        "mode_label": mode_label,
        "mode_short_label": mode_short_label,
        "mode_class": mode if mode in _MODE_LABELS else None,
        "is_finalized": is_finalized,
        "is_scored": is_scored,
        "status_label": ("합격" if _field(source, "is_passed") else "불합격") if is_scored else ("진행 중" if not is_finalized else "채점 전"),
        "created_at_text": _display_time(_field(source, "created_at")),
        "submitted_at_text": _display_time(submitted_at),
        "total_score": total_score if is_scored else None,
        "max_score": Config.TOTAL_SCORE if is_scored else None,
        "short_score": _field(source, "short_score") if is_scored else None,
        "descriptive_score": _field(source, "descriptive_score") if is_scored else None,
        "practical_score": _field(source, "practical_score") if is_scored else None,
        "selected_practical_id": _field(source, "selected_practical_id"),
        "is_passed": _field(source, "is_passed") if is_scored else None,
        "result_url": url_for("exam.view_result", attempt_id=attempt_id) if attempt_id and is_scored else None,
        "history_url": url_for("history.view_history_detail", attempt_id=attempt_id) if attempt_id and is_owner else None,
    }
