"""Browser-local question bookmarks: canonical, answer-free catalog only."""

from flask import Blueprint, current_app, jsonify, render_template, url_for

from app.services.data_loader import DataLoader


bookmark_bp = Blueprint("bookmarks", __name__)

TYPE_LABELS = {"short": "단답형", "descriptive": "서술형", "practical": "실무형"}


@bookmark_bp.get("/bookmarks")
def list_bookmarks():
    return render_template("bookmarks/index.html")


@bookmark_bp.get("/bookmarks/catalog")
def question_catalog():
    """Return current canonical IDs and display summaries, never answer data."""
    loader = DataLoader(current_app.config["DATA_DIR"])
    concepts = {item["id"]: item for item in loader.load_concepts()}
    topics = {item["topic_id"]: item for item in loader.load_topics()}
    topic_by_question = {
        item["question_id"]: item["topic_id"]
        for item in loader.load_question_topics()
    }
    catalog = []
    for question in loader.load_questions():
        question_id = question["id"]
        topic_id = topic_by_question[question_id]
        preview = " ".join(question["question"].split())
        catalog.append({
            "id": question_id,
            "type": question["type"],
            "type_label": TYPE_LABELS[question["type"]],
            "category": question["category"],
            "concept": concepts[question["concept_id"]]["name"],
            "topic": topics[topic_id]["name"],
            "preview": preview[:180] + ("…" if len(preview) > 180 else ""),
            "url": url_for("concepts.view_topic_detail", topic_id=topic_id) + "#question-" + question_id,
        })
    response = jsonify(catalog)
    response.headers["Cache-Control"] = "no-store"
    return response
