from flask import Blueprint, abort, current_app, render_template, request

from app.services.auth_service import admin_required
from app.services.data_loader import DataLoader
from app.services.law_freshness_service import LawFreshnessService


law_freshness_bp = Blueprint("law_freshness", __name__)


def get_law_freshness_service() -> LawFreshnessService:
    return LawFreshnessService(DataLoader(current_app.config["DATA_DIR"]))


@law_freshness_bp.route("/law-freshness")
@admin_required
def review_queue():
    service = get_law_freshness_service()
    selected_status = request.args.get("status", "ALL").strip().upper()
    if selected_status not in ("ALL", *service.STATUSES):
        abort(400, description="지원하지 않는 법규 최신성 상태입니다.")
    records = service.get_records(
        None if selected_status == "ALL" else selected_status
    )
    return render_template(
        "law_freshness/index.html",
        records=records,
        inventory=service.get_inventory(),
        selected_status=selected_status,
    )
