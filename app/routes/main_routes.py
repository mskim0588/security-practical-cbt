from flask import Blueprint, render_template, current_app
from app.services.data_loader import DataLoader

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    loader = DataLoader(current_app.config["DATA_DIR"])
    validation = loader.validate_dataset()
    sources = loader.load_sources()
    sources_summary = loader.get_sources_summary()
    total_bank_count = len(loader.load_questions())
    return render_template(
        "index.html",
        validation=validation,
        sources=sources,
        sources_summary=sources_summary,
        total_bank_count=total_bank_count
    )
