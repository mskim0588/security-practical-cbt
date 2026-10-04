from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService

history_bp = Blueprint("history", __name__)

def get_history_service():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return HistoryService(loader)

@history_bp.route("/history")
def list_history():
    service = get_history_service()
    
    page = request.args.get("page", 1, type=int)
    per_page = 15
    offset = (page - 1) * per_page
    
    total_count = service.get_attempt_count()
    attempts = service.get_attempts(limit=per_page, offset=offset)
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1

    return render_template(
        "history_list.html",
        attempts=attempts,
        total_count=total_count,
        current_page=page,
        total_pages=total_pages
    )

@history_bp.route("/history/<int:attempt_id>")
def view_history_detail(attempt_id: int):
    service = get_history_service()
    detail = service.get_attempt_detail(attempt_id)
    if not detail:
        abort(404)
        
    return render_template(
        "history_detail.html",
        attempt=detail
    )

from app.services.csrf_service import csrf_protect

@history_bp.route("/history/<int:attempt_id>/delete", methods=["POST"])
@csrf_protect
def delete_history_item(attempt_id: int):
    service = get_history_service()
    attempt = service.get_attempt_by_id(attempt_id)
    if not attempt:
        abort(404, description="삭제할 응시 기록을 찾을 수 없습니다.")
    service.delete_attempt(attempt_id)
    return redirect(url_for("history.list_history"))
