from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Blueprint 등록
    from app.routes.main_routes import main_bp
    from app.routes.exam_routes import exam_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(exam_bp)

    return app
