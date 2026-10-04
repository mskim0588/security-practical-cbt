# -*- coding: utf-8 -*-
"""
CSRF Protection Service
Provides session-based CSRF token generation, validation, and request verification
for state-changing endpoints (/submit, /history/<id>/delete).

Distinction:
- CSRF Token: Protects against Cross-Site Request Forgery by ensuring requests originate
  from an authenticated/valid local user session.
- Submission Token (Idempotency): Prevents duplicate submissions and double-click record
  duplication at the database level.
"""
import secrets
import hmac
from functools import wraps
from flask import session, request, abort

CSRF_SESSION_KEY = "csrf_token"
CSRF_FORM_FIELD = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"


def generate_csrf_token() -> str:
    """
    Generate or return the existing cryptographically secure CSRF token stored in the session.
    """
    if CSRF_SESSION_KEY not in session:
        session[CSRF_SESSION_KEY] = secrets.token_hex(32)
    return session[CSRF_SESSION_KEY]


def validate_csrf_token(token: str | None) -> bool:
    """
    Validate provided CSRF token against session token using constant-time comparison.
    Returns False if session has no token, or token is None/mismatched.
    """
    expected = session.get(CSRF_SESSION_KEY)
    if not expected or not token:
        return False
    return hmac.compare_digest(str(token).strip(), str(expected).strip())


def verify_csrf():
    """
    Verifies CSRF token from request form data or HTTP header.
    Aborts with HTTP 403 Forbidden on missing or mismatched token.
    """
    token = request.form.get(CSRF_FORM_FIELD) or request.headers.get(CSRF_HEADER_NAME)
    if not validate_csrf_token(token):
        abort(403, description="보안 검증(CSRF) 실패: 유효한 CSRF 토큰이 누락되었거나 일치하지 않습니다.")


def csrf_protect(f):
    """
    Decorator to enforce CSRF validation on state-changing view functions.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_csrf()
        return f(*args, **kwargs)
    return decorated_function
