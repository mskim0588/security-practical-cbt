from flask import Blueprint, render_template, current_app
from app.services.data_loader import DataLoader
from app.services.analytics_service import AnalyticsService
from app.services.wrong_answer_service import WrongAnswerService

dashboard_bp = Blueprint("dashboard", __name__)

def get_services():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return AnalyticsService(loader), WrongAnswerService(loader)

@dashboard_bp.route("/dashboard")
def view_dashboard():
    analytics_service, wrong_service = get_services()

    summary = analytics_service.get_summary_stats()
    categories = analytics_service.get_category_analytics()
    top_vulnerable = analytics_service.get_top_vulnerable_concepts(limit=5)
    recent_trend = analytics_service.get_recent_performance_trend(limit=5)
    wrong_count = wrong_service.get_wrong_question_count()

    return render_template(
        "dashboard.html",
        summary=summary,
        categories=categories,
        top_vulnerable=top_vulnerable,
        recent_trend=recent_trend,
        wrong_count=wrong_count
    )
