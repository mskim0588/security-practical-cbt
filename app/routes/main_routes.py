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

@main_bp.route("/healthz")
def healthz():
    from sqlalchemy import text
    from app.models.database import engine
    db_status = "healthy"
    try:
        if engine is not None:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        else:
            db_status = "uninitialized"
    except Exception as e:
        current_app.logger.error(f"Health check database failure: {e}")
        return {
            "status": "error",
            "database": "unhealthy"
        }, 503

    return {
        "status": "ok",
        "database": db_status,
        "environment": current_app.config.get("FLASK_ENV", "development"),
        "version": "0.5.0"
    }, 200
