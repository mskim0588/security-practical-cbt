from flask import Blueprint, abort, current_app, redirect, render_template, request, session, url_for

from app.services.auth_service import is_admin_authenticated
from app.services.csrf_service import csrf_protect
from app.services.data_loader import DataLoader
from app.services.law_freshness_service import LawFreshnessService
from app.services.descriptive_training_service import (
    DescriptiveTrainingService,
    DescriptiveTrainingStateError,
)


descriptive_training_bp = Blueprint("descriptive_training", __name__)


def get_descriptive_training_service() -> DescriptiveTrainingService:
    return DescriptiveTrainingService(DataLoader(current_app.config["DATA_DIR"]))


def _remember_session(attempt_id: int) -> None:
    attempt_ids = session.get("descriptive_training_attempts", [])
    if attempt_id not in attempt_ids:
        attempt_ids.append(attempt_id)
    session["descriptive_training_attempts"] = attempt_ids[-20:]
    session["active_descriptive_training_id"] = attempt_id
    session.modified = True


def _authorize_training(attempt_id: int):
    service = get_descriptive_training_service()
    attempt = service.get_attempt(attempt_id)
    if not attempt:
        abort(404, description="서술형 훈련 세션을 찾을 수 없습니다.")
    session_owned = attempt_id in session.get("descriptive_training_attempts", [])
    owner_access = is_admin_authenticated() and attempt.is_owner
    if not session_owned and not owner_access:
        abort(403, description="본인의 서술형 훈련 세션만 열 수 있습니다.")
    if not is_admin_authenticated() and attempt.is_owner:
        abort(403, description="본인의 서술형 훈련 세션만 열 수 있습니다.")
    return service, attempt


@descriptive_training_bp.route("/descriptive-training")
def setup_training():
    service = get_descriptive_training_service()
    active_session = None
    active_id = session.get("active_descriptive_training_id")
    if isinstance(active_id, int):
        attempt = service.get_attempt(active_id)
        if attempt and (active_id in session.get("descriptive_training_attempts", []) or (is_admin_authenticated() and attempt.is_owner)):
            try:
                active_session = service.get_state(active_id)
            except DescriptiveTrainingStateError:
                active_session = None
    return render_template(
        "descriptive_training/setup.html",
        options=service.get_setup_options(),
        active_session=active_session,
        recent_sessions=service.get_recent_owner_sessions() if is_admin_authenticated() else [],
        form_error=None,
        form_values={"scope_kind": "all", "category": "", "count": "5"},
    )


@descriptive_training_bp.route("/descriptive-training/start", methods=["POST"])
@csrf_protect
def start_training():
    service = get_descriptive_training_service()
    form_values = {
        "scope_kind": request.form.get("scope_kind", "all").strip().lower(),
        "category": request.form.get("category", "").strip(),
        "count": request.form.get("count", "5").strip().lower(),
    }
    try:
        count = 0 if form_values["count"] == "all" else int(form_values["count"])
    except (TypeError, ValueError):
        count = -1
    scope_value = form_values["category"] if form_values["scope_kind"] == "category" else ""
    try:
        attempt = service.create_session(
            scope_kind=form_values["scope_kind"],
            scope_value=scope_value,
            count=count,
            is_owner=is_admin_authenticated(),
        )
    except ValueError as error:
        return render_template(
            "descriptive_training/setup.html",
            options=service.get_setup_options(),
            active_session=None,
            recent_sessions=service.get_recent_owner_sessions() if is_admin_authenticated() else [],
            form_error=str(error),
            form_values=form_values,
        ), 400
    _remember_session(attempt.id)
    return redirect(url_for("descriptive_training.view_training", attempt_id=attempt.id))


@descriptive_training_bp.route("/descriptive-training/<int:attempt_id>")
def view_training(attempt_id: int):
    service, _ = _authorize_training(attempt_id)
    try:
        state = service.get_state(attempt_id)
    except DescriptiveTrainingStateError as error:
        abort(409, description=str(error))
    if not state:
        abort(404, description="서술형 훈련 세션을 찾을 수 없습니다.")
    if state.get("result"):
        state["result"]["law_freshness"] = LawFreshnessService(
            DataLoader(current_app.config["DATA_DIR"])
        ).get_for_question(state["question"]["id"])
    _remember_session(attempt_id)
    return render_template(
        "descriptive_training/session.html",
        training=state,
        show_ai_helper_modal=bool(state.get("result")),
    )


@descriptive_training_bp.route("/descriptive-training/<int:attempt_id>/answer", methods=["POST"])
@csrf_protect
def answer_training(attempt_id: int):
    service, _ = _authorize_training(attempt_id)
    try:
        service.submit_answer(attempt_id, request.form)
    except DescriptiveTrainingStateError as error:
        abort(409, description=str(error))
    return redirect(url_for("descriptive_training.view_training", attempt_id=attempt_id))


@descriptive_training_bp.route("/descriptive-training/<int:attempt_id>/next", methods=["POST"])
@csrf_protect
def next_training(attempt_id: int):
    service, _ = _authorize_training(attempt_id)
    try:
        service.advance(attempt_id)
    except DescriptiveTrainingStateError as error:
        abort(409, description=str(error))
    return redirect(url_for("descriptive_training.view_training", attempt_id=attempt_id))
