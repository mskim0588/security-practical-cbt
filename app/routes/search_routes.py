"""Read-only integrated learning search route."""

from flask import Blueprint, current_app, render_template, request

from app.services.data_loader import DataLoader
from app.services.search_service import SearchService


search_bp = Blueprint("search", __name__)


@search_bp.get("/search")
def learning_search():
    loader = DataLoader(current_app.config["DATA_DIR"])
    result = SearchService(loader).search(
        request.args.get("q", ""), request.args.get("type", "all")
    )
    return render_template("search/index.html", **result)
