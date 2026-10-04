from flask import Flask, render_template
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # DB 초기화
    from app.models.database import init_db
    init_db(app)

    # Blueprint 등록
    from app.routes.main_routes import main_bp
    from app.routes.exam_routes import exam_bp
    from app.routes.history_routes import history_bp
    from app.routes.wrong_routes import wrong_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.concept_routes import concept_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(wrong_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(concept_bp)

    # CSRF Token Context Processor
    from app.services.csrf_service import generate_csrf_token

    @app.context_processor
    def inject_csrf():
        return {"csrf_token": generate_csrf_token}

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html", error_message=getattr(e, "description", None)), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app
