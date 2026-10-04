import secrets
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService
from app.services.grader import Grader
from app.services.csrf_service import csrf_protect

exam_bp = Blueprint("exam", __name__)

def get_exam_service():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return ExamService(loader)

@exam_bp.route("/exam")
def take_exam():
    service = get_exam_service()
    mode = request.args.get("mode", "standard").strip().lower()
    if mode not in ("standard", "random", "wrong_review", "adaptive"):
        mode = "standard"

    seed_param = request.args.get("seed")
    seed_val = None
    if seed_param is not None and seed_param.strip() != "":
        try:
            seed_val = int(seed_param.strip())
        except (ValueError, TypeError):
            # 잘못된 seed 값 입력 시 서버 오류(500) 없이 안전하게 일반 랜덤으로 fallback
            seed_val = None

    questions = service.get_exam_questions(mode=mode, seed=seed_val)

    short_qs = [q for q in questions if q["type"] == "short"]
    desc_qs = [q for q in questions if q["type"] == "descriptive"]
    prac_qs = [q for q in questions if q["type"] == "practical"]
    question_ids_str = ",".join(q["id"] for q in questions)
    submission_token = secrets.token_urlsafe(32)

    return render_template(
        "exam.html",
        short_qs=short_qs,
        desc_qs=desc_qs,
        prac_qs=prac_qs,
        total_questions=len(questions),
        exam_mode=mode,
        exam_seed=seed_val,
        question_ids_str=question_ids_str,
        submission_token=submission_token
    )

@exam_bp.route("/review", methods=["POST"])
def review_exam():
    service = get_exam_service()
    questions = service.resolve_submitted_questions(request.form)
    parsed = service.parse_submission(request.form, questions)

    selected_prac_id = parsed["selected_practical_id"]
    answers = parsed["answers"]

    review_items = []
    answered_count = 0
    complete_count = 0

    for idx, q in enumerate(questions, start=1):
        q_id = q["id"]
        q_type = q["type"]
        q_ans = answers.get(q_id, {})
        is_sel_prac = (q_id == selected_prac_id)

        status_info = service.calculate_question_status(q, q_ans, is_sel_prac)

        if status_info["is_filled"] and (q_type != "practical" or is_sel_prac):
            answered_count += 1
        if status_info["is_complete"] and (q_type != "practical" or is_sel_prac):
            complete_count += 1

        review_items.append({
            "index": idx,
            "id": q_id,
            "type": q_type,
            "category": q.get("category"),
            "score": q.get("score"),
            "status_text": status_info["status_text"],
            "status_code": status_info["status_code"],
            "is_answered": status_info["is_filled"],
            "is_complete": status_info["is_complete"],
            "is_selected_practical": is_sel_prac
        })

    selected_prac_title = None
    for idx, q in enumerate(questions, start=1):
        if q["id"] == selected_prac_id:
            selected_prac_title = f"{idx}번 ({q.get('category', '실무')})"
            break

    return render_template(
        "review.html",
        review_items=review_items,
        answered_count=answered_count,
        complete_count=complete_count,
        selected_practical_id=selected_prac_id,
        selected_prac_title=selected_prac_title,
        raw_form_data=request.form
    )

@exam_bp.route("/submit", methods=["POST"])
@csrf_protect
def submit_exam():
    service = get_exam_service()
    form_data = request.form
    submission_token = form_data.get("submission_token")
    if submission_token:
        submission_token = str(submission_token).strip() or None
    else:
        submission_token = None

    questions = service.resolve_submitted_questions(form_data)
    submission = service.parse_submission(form_data, questions)
    result = Grader.grade_full_exam(questions, submission)

    # Goal 3A / 3F-Fix: 응시 기록 영속화 및 멱등성 토큰 저장
    attempt_id = None
    try:
        from app.services.history_service import HistoryService
        loader = DataLoader(current_app.config["DATA_DIR"])
        history_service = HistoryService(loader)

        exam_mode = form_data.get("exam_mode", "standard").strip().lower()
        seed_param = form_data.get("exam_seed")
        seed_val = None
        if seed_param is not None and str(seed_param).strip() != "":
            try:
                seed_val = int(str(seed_param).strip())
            except (ValueError, TypeError):
                seed_val = None

        attempt = history_service.save_exam_attempt(
            exam_mode=exam_mode,
            seed=seed_val,
            selected_practical_id=submission.get("selected_practical_id"),
            grading_result=result,
            answers=submission.get("answers", {}),
            submission_token=submission_token
        )
        attempt_id = attempt.id
    except Exception as e:
        current_app.logger.error(f"Failed to save exam attempt: {e}")

    # Goal 3F-Fix: PRG 패턴 (Post -> Redirect -> Get)
    if attempt_id:
        return redirect(url_for("exam.view_result", attempt_id=attempt_id))

    # DB 저장 실패 시 비상 fallback 렌더링
    for d in result.get("details", []):
        qid = d.get("question_id")
        q_meta = loader.get_question_by_id(qid) if qid else None
        if q_meta:
            d["concept_id"] = q_meta.get("concept_id")
            d["deep_explanation"] = loader.get_explanation_for_question(qid)
    return render_template("result.html", result=result, attempt_id=None)

@exam_bp.route("/result/<int:attempt_id>")
def view_result(attempt_id: int):
    """
    PRG 패턴에 따라 제출 완료 후 시험 채점 결과를 안전하게 조회하는 GET 라우트.
    새로고침(F5) 시 중복 제출이나 데이터 왜곡 없이 안전하게 채점 결과를 재표시합니다.
    """
    from app.services.history_service import HistoryService
    loader = DataLoader(current_app.config["DATA_DIR"])
    history_service = HistoryService(loader)
    detail = history_service.get_attempt_detail(attempt_id)
    if not detail:
        return redirect(url_for("history.list_history"))

    short_earned = detail.get("short_score", 0.0)
    desc_earned = detail.get("descriptive_score", 0.0)
    prac_earned = detail.get("practical_score", 0.0)
    total_score = detail.get("total_score", 0.0)
    is_passed = detail.get("is_passed", False)
    selected_prac_id = detail.get("selected_practical_id")

    details = []
    for ans in detail.get("answers", []):
        qid = ans.get("question_id")
        q_type = ans.get("question_type", "short")
        is_sel = (q_type != "practical") or (qid == selected_prac_id)
        q_meta = loader.get_question_by_id(qid) if qid else None
        concept_id = q_meta.get("concept_id") if q_meta else None
        deep_expl = loader.get_explanation_for_question(qid) if qid else None

        details.append({
            "question_id": qid,
            "type": q_type,
            "category": ans.get("category", ""),
            "concept_id": concept_id,
            "deep_explanation": deep_expl,
            "question_text": ans.get("question_text", ""),
            "earned_score": ans.get("earned_score", 0.0),
            "max_score": ans.get("max_score", 0.0),
            "is_selected": is_sel,
            "sub_results": ans.get("self_eval_data") or [],
            "model_answer": ans.get("model_answer", ""),
            "explanation": ans.get("explanation", ""),
            "source_info": ans.get("source_info") or {},
            "source_page": ans.get("source_page", 1)
        })

    result_dict = {
        "total_score": total_score,
        "is_passed": is_passed,
        "summary": {
            "short": {
                "earned": short_earned,
                "percentage": round((short_earned / 36.0) * 100, 1) if 36 > 0 else 0
            },
            "descriptive": {
                "earned": desc_earned,
                "percentage": round((desc_earned / 48.0) * 100, 1) if 48 > 0 else 0
            },
            "practical": {
                "earned": prac_earned,
                "percentage": round((prac_earned / 16.0) * 100, 1) if 16 > 0 else 0,
                "selected_id": selected_prac_id
            }
        },
        "details": details
    }

    return render_template("result.html", result=result_dict, attempt_id=attempt_id)

