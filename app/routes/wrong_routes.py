from flask import Blueprint, render_template, request, abort, current_app
from app.services.data_loader import DataLoader
from app.services.wrong_answer_service import WrongAnswerService
from app.services.auth_service import admin_required

wrong_bp = Blueprint("wrong", __name__)

def get_wrong_service():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return WrongAnswerService(loader)

@wrong_bp.route("/wrong-notes")
@admin_required
def list_wrong_notes():
    service = get_wrong_service()
    
    type_filter = request.args.get("type", "all").strip().lower()
    status_filter = request.args.get("status", "all").strip().lower()
    category_filter = request.args.get("category", "all").strip()
    sort_by = request.args.get("sort", "latest").strip().lower()

    questions = service.get_wrong_questions(
        type_filter=type_filter,
        status_filter=status_filter,
        category_filter=category_filter,
        sort_by=sort_by
    )

    # 5대 카테고리 목록
    categories = [
        "시스템 보안",
        "네트워크 보안",
        "애플리케이션 보안",
        "정보보안 일반 및 암호학",
        "정보보호 관리 및 법규"
    ]

    # 유형별/상태별 통계 카운트 (필터링 전 원본 기준)
    all_wrong = service.get_wrong_questions()
    stats = {
        "total": len(all_wrong),
        "short": sum(1 for q in all_wrong if q["type"] == "short"),
        "descriptive": sum(1 for q in all_wrong if q["type"] == "descriptive"),
        "practical": sum(1 for q in all_wrong if q["type"] == "practical"),
        "incorrect": sum(1 for q in all_wrong if q["latest_status"] == "incorrect"),
        "partial": sum(1 for q in all_wrong if q["latest_status"] == "partial"),
        "repeat": sum(1 for q in all_wrong if q.get("fail_count", 0) >= 2),
    }

    return render_template(
        "wrong_notes.html",
        questions=questions,
        categories=categories,
        stats=stats,
        current_type=type_filter,
        current_status=status_filter,
        current_category=category_filter,
        current_sort=sort_by
    )

@wrong_bp.route("/wrong-notes/<question_id>")
@admin_required
def view_wrong_detail(question_id: str):
    service = get_wrong_service()
    detail = service.get_wrong_question_detail(question_id)
    if not detail:
        abort(404)

    return render_template(
        "wrong_detail.html",
        detail=detail
    )
