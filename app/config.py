import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cbt-dev-secret-key-2026")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    EXAM_TITLE = "정보보안기사 실기시험 모의고사 CBT"
    PASSING_SCORE = 60.0
    TOTAL_SCORE = 100.0
    EXAM_DURATION_MINUTES = 180  # 실제 실기 시험 3시간
