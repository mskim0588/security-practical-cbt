# -*- coding: utf-8 -*-
"""
Concept Routes
Provides routes for the Concept Library (/concepts) and individual Concept Detail view (/concepts/<concept_id>).
"""
from flask import Blueprint, render_template, request, abort, current_app
from app.services.data_loader import DataLoader
from app.services.learning_service import LearningService

concept_bp = Blueprint("concepts", __name__)

def get_learning_service():
    loader = DataLoader(current_app.config.get("DATA_DIR"))
    return LearningService(data_loader=loader)

@concept_bp.route("/concepts")
def list_concepts():
    service = get_learning_service()
    concepts = service.get_concept_overview_list()

    category_filter = request.args.get("category", "").strip()
    search_query = request.args.get("q", "").strip().lower()

    categories = [
        "시스템 보안",
        "네트워크 보안",
        "애플리케이션 보안",
        "정보보안 일반 및 암호학",
        "정보보호 관리 및 법규"
    ]

    # Category counts
    category_counts = {cat: 0 for cat in categories}
    for c in concepts:
        cat = c.get("category")
        if cat in category_counts:
            category_counts[cat] += 1

    filtered_concepts = concepts
    if category_filter:
        filtered_concepts = [c for c in filtered_concepts if c.get("category") == category_filter]

    if search_query:
        filtered_concepts = [
            c for c in filtered_concepts
            if search_query in c.get("concept_id", "").lower()
            or search_query in c.get("name", "").lower()
            or search_query in c.get("summary", "").lower()
            or any(search_query in p.lower() for p in c.get("core_points", []))
        ]

    return render_template(
        "concepts/index.html",
        concepts=filtered_concepts,
        total_concepts_count=len(concepts),
        selected_category=category_filter,
        search_query=search_query,
        categories=categories,
        category_counts=category_counts
    )

@concept_bp.route("/concepts/<concept_id>")
def view_concept_detail(concept_id: str):
    service = get_learning_service()
    detail = service.get_concept_detail(concept_id)
    if not detail:
        abort(404, description=f"개념 ID '{concept_id}'를 찾을 수 없습니다.")

    return render_template(
        "concepts/detail.html",
        concept=detail
    )
