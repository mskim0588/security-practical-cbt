import os
from typing import Optional
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

engine = None
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

def init_db(app: Optional[Flask] = None, uri: Optional[str] = None):
    """
    데이터베이스 엔진 및 세션을 초기화하고 테이블을 생성합니다.
    """
    global engine, db_session

    if uri is None:
        if app is not None and "SQLALCHEMY_DATABASE_URI" in app.config:
            uri = app.config["SQLALCHEMY_DATABASE_URI"]
        else:
            uri = "sqlite:///:memory:"

    # SQLite 파일 경로인 경우 부모 디렉터리 자동 생성
    if uri.startswith("sqlite:///") and not uri.startswith("sqlite:///:memory:"):
        db_path = uri.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    connect_args = {}
    engine_kwargs = {}
    if uri.startswith("sqlite:"):
        connect_args["check_same_thread"] = False
    else:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_recycle"] = 300

    engine = create_engine(uri, connect_args=connect_args, **engine_kwargs)
    db_session.configure(bind=engine)

    # 모델 클래스 임포트하여 Base.metadata에 등록
    from app.models import history  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # 기존 DB 스키마 안전 마이그레이션 (기존 레코드 완전 보존)
    _migrate_schema(engine)

    if app is not None:
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

def _migrate_schema(bind_engine):
    """
    기존 테이블에 누락된 컬럼 및 인덱스를 안전하게 점검하고 마이그레이션합니다.
    """
    from sqlalchemy import inspect, text
    try:
        with bind_engine.connect() as conn:
            inspector = inspect(conn)
            tables = inspector.get_table_names()
            if "exam_attempts" in tables:
                columns = [col["name"] for col in inspector.get_columns("exam_attempts")]
                if "submission_token" not in columns:
                    conn.execute(text("ALTER TABLE exam_attempts ADD COLUMN submission_token VARCHAR(64)"))
                    conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_exam_attempts_submission_token ON exam_attempts (submission_token)"))
                    conn.commit()
                if "is_owner" not in columns:
                    conn.execute(text("ALTER TABLE exam_attempts ADD COLUMN is_owner BOOLEAN DEFAULT 1 NOT NULL"))
                    conn.execute(text("CREATE INDEX IF NOT EXISTS ix_exam_attempts_is_owner ON exam_attempts (is_owner)"))
                    conn.commit()
    except Exception:
        # 인메모리 DB나 특수 환경에서 예외 발생 시 안전하게 통과
        pass

def close_db():
    """세션 제거 및 엔진 정리"""
    global db_session, engine
    db_session.remove()
    if engine is not None:
        engine.dispose()
