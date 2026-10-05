from flask import Blueprint, abort, current_app, redirect, render_template, request, session, url_for

from app.services.auth_service import is_admin_authenticated
from app.services.csrf_service import csrf_protect
from app.services.data_loader import DataLoader
from app.services.practice_service import PracticeService, PracticeStateError


practice_bp = Blueprint("practice", __name__)


def get_practice_service() -> PracticeService:
    return PracticeService(DataLoader(current_app.config["DATA_DIR"]))


def _remember_session(attempt_id: int) -> None:
    attempt_ids = session.get("practice_attempts", [])
    if attempt_id not in attempt_ids:
        attempt_ids.append(attempt_id)
    session["practice_attempts"] = attempt_ids[-20:]
    session["active_practice_id"] = attempt_id
    session.modified = True


def _authorize_practice(attempt_id: int):
    service = get_practice_service()
    attempt = service.get_attempt(attempt_id)
    if not attempt:
        abort(404, description="회독 학습 세션을 찾을 수 없습니다.")

    session_owned = attempt_id in session.get("practice_attempts", [])
    owner_access = is_admin_authenticated() and attempt.is_owner
    if not session_owned and not owner_access:
        abort(403, description="본인의 회독 학습 세션만 열 수 있습니다.")
    if not is_admin_authenticated() and attempt.is_owner:
        abort(403, description="본인의 회독 학습 세션만 열 수 있습니다.")
    return service, attempt


@practice_bp.route("/practice")
def setup_practice():
    service = get_practice_service()
    active_session = None
    active_id = session.get("active_practice_id")
    if isinstance(active_id, int):
        attempt = service.get_attempt(active_id)
        if attempt and (active_id in session.get("practice_attempts", []) or (is_admin_authenticated() and attempt.is_owner)):
            try:
                active_session = service.get_state(active_id)
            except PracticeStateError:
                active_session = None

    recent_sessions = service.get_recent_owner_sessions() if is_admin_authenticated() else []
    return render_template(
        "practice/setup.html",
        options=service.get_setup_options(),
        active_session=active_session,
        recent_sessions=recent_sessions,
        form_error=None,
        form_values={"rounds": "1", "scope_kind": "all", "category": "", "question_type": ""},
    )


@practice_bp.route("/practice/start", methods=["POST"])
@csrf_protect
def start_practice():
    service = get_practice_service()
    form_values = {
        "rounds": request.form.get("rounds", "1"),
        "scope_kind": request.form.get("scope_kind", "all"),
        "category": request.form.get("category", ""),
        "question_type": request.form.get("question_type", ""),
    }
    try:
        rounds = int(form_values["rounds"])
    except (TypeError, ValueError):
        rounds = 0

    scope_kind = form_values["scope_kind"].strip().lower()
    scope_value = ""
    if scope_kind == "category":
        scope_value = form_values["category"].strip()
    elif scope_kind == "type":
        scope_value = form_values["question_type"].strip().lower()

    try:
        attempt = service.create_session(
            rounds=rounds,
            scope_kind=scope_kind,
            scope_value=scope_value,
            is_owner=is_admin_authenticated(),
        )
    except ValueError as error:
        return render_template(
            "practice/setup.html",
            options=service.get_setup_options(),
            active_session=None,
            recent_sessions=service.get_recent_owner_sessions() if is_admin_authenticated() else [],
            form_error=str(error),
            form_values=form_values,
        ), 400

    _remember_session(attempt.id)
    return redirect(url_for("practice.view_practice", attempt_id=attempt.id))


@practice_bp.route("/practice/<int:attempt_id>")
def view_practice(attempt_id: int):
    service, _ = _authorize_practice(attempt_id)
    try:
        state = service.get_state(attempt_id)
    except PracticeStateError as error:
        abort(409, description=str(error))
    if not state:
        abort(404, description="회독 학습 세션을 찾을 수 없습니다.")
    _remember_session(attempt_id)
    return render_template("practice/session.html", practice=state)


@practice_bp.route("/practice/<int:attempt_id>/answer", methods=["POST"])
@csrf_protect
def answer_practice(attempt_id: int):
    service, _ = _authorize_practice(attempt_id)
    try:
        service.submit_answer(attempt_id, request.form)
    except PracticeStateError as error:
        abort(409, description=str(error))
    return redirect(url_for("practice.view_practice", attempt_id=attempt_id))


@practice_bp.route("/practice/<int:attempt_id>/next", methods=["POST"])
@csrf_protect
def next_practice(attempt_id: int):
    service, _ = _authorize_practice(attempt_id)
    try:
        service.advance(attempt_id)
    except PracticeStateError as error:
        abort(409, description=str(error))
    return redirect(url_for("practice.view_practice", attempt_id=attempt_id))
