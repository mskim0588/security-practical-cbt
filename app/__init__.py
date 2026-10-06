from flask import Flask, render_template
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Production Secret Fail-Closed 검증
    if app.config.get("IS_PRODUCTION") and not app.config.get("TESTING"):
        secret = app.config.get("SECRET_KEY")
        if not secret or secret == "cbt-dev-secret-key-2026":
            raise RuntimeError("CRITICAL SECURITY ERROR: SECRET_KEY environment variable must be set in production mode. Fail closed.")

    # Reverse Proxy 지원 (Railway / Cloudflare / Nginx)
    if app.config.get("USE_PROXYFIX", False):
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

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
    from app.routes.auth_routes import auth_bp
    from app.routes.practice_routes import practice_bp
    from app.routes.descriptive_training_routes import descriptive_training_bp
    from app.routes.mock_exam_routes import mock_exam_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(wrong_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(concept_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(descriptive_training_bp)
    app.register_blueprint(mock_exam_bp)

    # CSRF & Auth Context Processor
    from app.services.csrf_service import generate_csrf_token
    from app.services.auth_service import is_admin_authenticated

    @app.context_processor
    def inject_global_context():
        return {
            "csrf_token": generate_csrf_token,
            "is_admin_authenticated": is_admin_authenticated,
            "admin_access_key_configured": bool(app.config.get("ADMIN_ACCESS_KEY"))
        }

    # Production HTTP Security Response Headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if "Content-Security-Policy" not in response.headers:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; "
                "font-src 'self';"
            )
        return response

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
