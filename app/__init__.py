from flask import Flask
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

    app.register_blueprint(main_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(wrong_bp)
    app.register_blueprint(dashboard_bp)

    return app
