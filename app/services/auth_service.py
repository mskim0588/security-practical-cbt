from functools import wraps
from flask import session, redirect, url_for, request, current_app

def is_admin_authenticated() -> bool:
    """
    관리자 인증 상태를 확인합니다.
    ADMIN_ACCESS_KEY가 비어있으면 (로컬/테스트 환경) 항상 True를 반환합니다.
    """
    admin_key = current_app.config.get("ADMIN_ACCESS_KEY", "")
    if not admin_key:
        return True
    return session.get("is_admin") is True

def admin_required(f):
    """
    관리자/개인 데이터 영역(/history, /wrong-notes, /dashboard) 보호 데코레이터.
    ADMIN_ACCESS_KEY가 설정된 환경에서 비인증 사용자의 접근 시 로그인 페이지로 안내합니다.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            return redirect(url_for("auth.admin_login", next=request.full_path if request.query_string else request.path))
        return f(*args, **kwargs)
    return decorated_function
