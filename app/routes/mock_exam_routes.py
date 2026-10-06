from flask import Blueprint, abort, current_app, redirect, render_template, request, session, url_for

from app.services.auth_service import is_admin_authenticated
from app.services.csrf_service import csrf_protect
from app.services.data_loader import DataLoader
from app.services.mock_exam_service import MockExamService, MockExamStateError


mock_exam_bp = Blueprint("mock_exam", __name__)


def get_mock_exam_service() -> MockExamService:
    return MockExamService(DataLoader(current_app.config["DATA_DIR"]))


def _remember_attempt(attempt_id: int) -> None:
    attempt_ids = session.get("mock_exam_attempts", [])
    if attempt_id not in attempt_ids:
        attempt_ids.append(attempt_id)
    session["mock_exam_attempts"] = attempt_ids[-20:]
    session["active_mock_exam_id"] = attempt_id
    session.modified = True


def _remember_result(attempt_id: int) -> None:
    submitted = session.get("submitted_attempts", [])
    if attempt_id not in submitted:
        submitted.append(attempt_id)
    session["submitted_attempts"] = submitted[-100:]
    if session.get("active_mock_exam_id") == attempt_id:
        session.pop("active_mock_exam_id", None)
    session.modified = True


def _authorize(attempt_id: int):
    service = get_mock_exam_service()
    attempt = service.get_attempt(attempt_id)
    if not attempt:
        abort(404, description="실전 모의고사 응시 기록을 찾을 수 없습니다.")
    session_owned = attempt_id in session.get("mock_exam_attempts", [])
    owner_access = is_admin_authenticated() and attempt.is_owner
    if not session_owned and not owner_access:
        abort(403, description="본인의 실전 모의고사만 열 수 있습니다.")
    if not is_admin_authenticated() and attempt.is_owner:
        abort(403, description="본인의 실전 모의고사만 열 수 있습니다.")
    return service, attempt


def _question_index(raw_value, default: int = 0) -> int:
    try:
        return max(0, min(int(raw_value), MockExamService.CANDIDATE_COUNT - 1))
    except (TypeError, ValueError):
        return default


@mock_exam_bp.route("/mock-exam")
def setup_mock_exam():
    service = get_mock_exam_service()
    active_session = None
    active_id = session.get("active_mock_exam_id")
    if isinstance(active_id, int):
        attempt = service.get_attempt(active_id)
        authorized = attempt and (
            active_id in session.get("mock_exam_attempts", [])
            or (is_admin_authenticated() and attempt.is_owner)
        )
        if authorized and attempt.exam_mode == service.ACTIVE_MODE:
            try:
                if service.finalize_if_expired(active_id):
                    _remember_result(active_id)
                else:
                    active_session = service.get_state(active_id)
            except MockExamStateError:
                active_session = None
    recent_sessions = service.get_recent_owner_attempts() if is_admin_authenticated() else []
    return render_template(
        "mock_exam/setup.html",
        active_session=active_session,
        recent_sessions=recent_sessions,
    )


@mock_exam_bp.route("/mock-exam/start", methods=["POST"])
@csrf_protect
def start_mock_exam():
    service = get_mock_exam_service()
    try:
        attempt = service.create_attempt(is_owner=is_admin_authenticated())
    except MockExamStateError as error:
        abort(409, description=str(error))
    _remember_attempt(attempt.id)
    return redirect(url_for("mock_exam.view_mock_exam", attempt_id=attempt.id, question=0))


@mock_exam_bp.route("/mock-exam/<int:attempt_id>")
def view_mock_exam(attempt_id: int):
    service, attempt = _authorize(attempt_id)
    if attempt.exam_mode == service.FINAL_MODE or service.finalize_if_expired(attempt_id):
        _remember_result(attempt_id)
        return redirect(url_for("exam.view_result", attempt_id=attempt_id))
    index = _question_index(request.args.get("question"), 0)
    try:
        state = service.get_state(attempt_id, current_index=index)
    except MockExamStateError as error:
        abort(409, description=str(error))
    _remember_attempt(attempt_id)
    return render_template("mock_exam/session.html", mock=state)


@mock_exam_bp.route("/mock-exam/<int:attempt_id>/save", methods=["POST"])
@csrf_protect
def save_mock_exam(attempt_id: int):
    service, _ = _authorize(attempt_id)
    current_index = _question_index(request.form.get("current_index"), 0)
    question_id = str(request.form.get("question_id", "")).strip()
    try:
        finalized = service.save_answer(attempt_id, question_id, request.form)
    except MockExamStateError as error:
        abort(409, description=str(error))
    if finalized:
        _remember_result(attempt_id)
        return redirect(url_for("exam.view_result", attempt_id=attempt_id))

    destination = str(request.form.get("destination", "save")).strip().lower()
    if destination == "review":
        return redirect(url_for("mock_exam.review_mock_exam", attempt_id=attempt_id))
    if destination == "previous":
        target = max(0, current_index - 1)
    elif destination == "next":
        target = min(MockExamService.CANDIDATE_COUNT - 1, current_index + 1)
    elif destination.startswith("question:"):
        target = _question_index(destination.split(":", 1)[1], current_index)
    else:
        target = current_index
    return redirect(url_for("mock_exam.view_mock_exam", attempt_id=attempt_id, question=target))


@mock_exam_bp.route("/mock-exam/<int:attempt_id>/flag", methods=["POST"])
@csrf_protect
def flag_mock_exam(attempt_id: int):
    service, _ = _authorize(attempt_id)
    current_index = _question_index(request.form.get("current_index"), 0)
    question_id = str(request.form.get("question_id", "")).strip()
    try:
        finalized = service.toggle_flag(attempt_id, question_id)
    except MockExamStateError as error:
        abort(409, description=str(error))
    if finalized:
        _remember_result(attempt_id)
        return redirect(url_for("exam.view_result", attempt_id=attempt_id))
    return redirect(url_for("mock_exam.view_mock_exam", attempt_id=attempt_id, question=current_index))


@mock_exam_bp.route("/mock-exam/<int:attempt_id>/review")
def review_mock_exam(attempt_id: int):
    service, attempt = _authorize(attempt_id)
    if attempt.exam_mode == service.FINAL_MODE or service.finalize_if_expired(attempt_id):
        _remember_result(attempt_id)
        return redirect(url_for("exam.view_result", attempt_id=attempt_id))
    try:
        state = service.get_state(attempt_id)
    except MockExamStateError as error:
        abort(409, description=str(error))
    return render_template("mock_exam/review.html", mock=state)


@mock_exam_bp.route("/mock-exam/<int:attempt_id>/submit", methods=["POST"])
@csrf_protect
def submit_mock_exam(attempt_id: int):
    service, _ = _authorize(attempt_id)
    try:
        attempt = service.finalize(attempt_id, reason="manual")
    except MockExamStateError as error:
        abort(409, description=str(error))
    _remember_result(attempt.id)
    return redirect(url_for("exam.view_result", attempt_id=attempt.id))
