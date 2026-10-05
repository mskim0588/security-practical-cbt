from flask import Blueprint, render_template, current_app
from typing import Dict, Any, List
from app.services.data_loader import DataLoader
from app.services.analytics_service import AnalyticsService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.auth_service import admin_required

dashboard_bp = Blueprint("dashboard", __name__)

def get_services():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return AnalyticsService(loader), WrongAnswerService(loader)

def get_learning_recommendation(summary: Dict[str, Any], wrong_count: int, top_vulnerable: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    학습자의 현재 성취도와 오답 현황에 기반한 결정론적 다음 학습 추천 Action 생성
    """
    total_attempts = summary.get("total_attempts", 0)

    # Rule A: 응시 기록 없음
    if total_attempts == 0:
        return {
            "type": "onboarding",
            "badge": "학습 진단 추천",
            "title": "첫 모의고사로 나의 보안 실력을 진단해보세요",
            "message": "아직 학습 기록이 없습니다. 표준 또는 랜덤 모의고사를 1회 응시하시면 5대 영역별 가중 성취도와 20개 보안 개념의 취약점을 정밀 진단해 드립니다.",
            "primary_btn_text": "📘 제1회 표준 모의고사 응시하기 →",
            "primary_btn_url": "/exam?mode=standard",
            "secondary_btn_text": "📖 20대 핵심 보안 개념 둘러보기",
            "secondary_btn_url": "/concepts"
        }

    # Rule B: 미해결 오답 문항 존재
    if wrong_count > 0:
        return {
            "type": "wrong_review",
            "badge": "오답 복습 시급",
            "title": f"미해결 오답 문항 {wrong_count}개를 먼저 복습하세요",
            "message": f"현재 모의고사에서 틀렸거나 부분 감점된 문항이 {wrong_count}개 남아있습니다. 오답 집중 모의고사로 취약점을 확실히 보완하세요.",
            "primary_btn_text": "🔥 오답 집중 모의고사 시작하기 →",
            "primary_btn_url": "/exam?mode=wrong_review",
            "secondary_btn_text": "📝 오답노트에서 확인하기",
            "secondary_btn_url": "/wrong-notes"
        }

    # Rule C: 취약 Concept 존재 (VI > 0)
    if top_vulnerable and top_vulnerable[0].get("vulnerability_index", 0) > 0:
        top_c = top_vulnerable[0]
        c_name = top_c.get("name", "")
        c_id = top_c.get("concept_id", "")
        return {
            "type": "concept_clinic",
            "badge": "취약 개념 보완",
            "title": f"최우선 취약 개념: {c_name}",
            "message": f"'{c_name}({c_id})'의 취약도 지수(VI)가 가장 높습니다. 개념 심층 학습서를 복습하고 맞춤형 모의고사로 실력을 점검하세요.",
            "primary_btn_text": "🎯 취약 Concept 맞춤 모의고사 시작 →",
            "primary_btn_url": "/exam?mode=adaptive",
            "secondary_btn_text": f"📖 {c_id} 개념 심층 학습서 보기",
            "secondary_btn_url": f"/concepts/{c_id}"
        }

    # Rule D: 전체적으로 안정된 상태
    pass_rate = summary.get("pass_rate", 0.0)
    return {
        "type": "practice",
        "badge": "실전 감각 유지",
        "title": f"우수한 성취도를 안정적으로 유지하고 있습니다! (합격률 {pass_rate}%)",
        "message": "모든 오답을 극복하고 안정적인 합격권에 도달했습니다. 랜덤 실전 모의고사로 다양한 실무 유형을 연습해보세요.",
        "primary_btn_text": "🎲 랜덤 실전 모의고사 응시하기 →",
        "primary_btn_url": "/exam?mode=random",
        "secondary_btn_text": "📜 과거 응시 이력 복기",
        "secondary_btn_url": "/history"
    }

@dashboard_bp.route("/dashboard")
@admin_required
def view_dashboard():
    analytics_service, wrong_service = get_services()

    summary = analytics_service.get_summary_stats()
    categories = analytics_service.get_category_analytics()
    top_vulnerable = analytics_service.get_top_vulnerable_concepts(limit=5)
    recent_trend = analytics_service.get_recent_performance_trend(limit=5)
    wrong_count = wrong_service.get_wrong_question_count()

    # 최근 성적 변동 (직전 시험 대비 delta)
    score_delta = None
    if len(recent_trend) >= 2:
        latest = recent_trend[-1]["total_score"]
        prev = recent_trend[-2]["total_score"]
        score_delta = round(latest - prev, 1)

    recommendation = get_learning_recommendation(summary, wrong_count, top_vulnerable)

    return render_template(
        "dashboard.html",
        summary=summary,
        categories=categories,
        top_vulnerable=top_vulnerable,
        recent_trend=recent_trend,
        wrong_count=wrong_count,
        score_delta=score_delta,
        recommendation=recommendation
    )
