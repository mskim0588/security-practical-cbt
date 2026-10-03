import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cbt-dev-secret-key-2026")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EXAM_TITLE = "정보보안기사 실기시험 모의고사 CBT"
    PASSING_SCORE = 60.0
    TOTAL_SCORE = 100.0
    EXAM_DURATION_MINUTES = 180  # 실제 실기 시험 3시간

    # Database
    PROJECT_ROOT = os.path.dirname(BASE_DIR)
    INSTANCE_DIR = os.path.join(PROJECT_ROOT, "instance")
    DEFAULT_DB_PATH = os.path.join(INSTANCE_DIR, "learning.db")
    
    _raw_db_url = os.environ.get("DATABASE_URL")
    if _raw_db_url and _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = _raw_db_url or f"sqlite:///{DEFAULT_DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
