import hmac
import time
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.services.csrf_service import csrf_protect

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/admin-login", methods=["GET", "POST"])
@csrf_protect
def admin_login():
    admin_key = current_app.config.get("ADMIN_ACCESS_KEY", "")
    next_url = request.args.get("next") or request.form.get("next") or url_for("dashboard.view_dashboard")

    # ADMIN_ACCESS_KEY가 미설정 상태라면 바로 대시보드로 이동
    if not admin_key:
        session["is_admin"] = True
        return redirect(next_url)

    error = None
    if request.method == "POST":
        input_key = request.form.get("access_key", "").strip()
        # 타이밍 공격 방지 비교 (constant-time)
        if hmac.compare_digest(input_key, admin_key):
            # Session Fixation 방어: 기존 세션 데이터를 정리하되 CSRF 토큰과 응시 소유권은 안전하게 보존
            csrf_tok = session.get("csrf_token")
            submitted = session.get("submitted_attempts", [])
            session.clear()
            session["is_admin"] = True
            if csrf_tok:
                session["csrf_token"] = csrf_tok
            if submitted:
                session["submitted_attempts"] = submitted
            return redirect(next_url)
        else:
            current_app.logger.warning(f"Failed admin login attempt from remote: {request.remote_addr or 'unknown'}")
            time.sleep(0.3)  # Brute-force 지연
            error = "입력하신 관리자 패스프레이즈가 일치하지 않습니다."

    return render_template("auth/admin_login.html", error=error, next_url=next_url)

@auth_bp.route("/admin-logout", methods=["POST"])
@csrf_protect
def admin_logout():
    session.clear()
    return redirect(url_for("main.index"))
