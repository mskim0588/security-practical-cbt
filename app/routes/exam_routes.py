from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService

exam_bp = Blueprint("exam", __name__)

def get_exam_service():
    loader = DataLoader(current_app.config["DATA_DIR"])
    return ExamService(loader)

@exam_bp.route("/exam")
def take_exam():
    service = get_exam_service()
    mode = request.args.get("mode", "standard").strip().lower()
    if mode not in ("standard", "random"):
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

    return render_template(
        "exam.html",
        short_qs=short_qs,
        desc_qs=desc_qs,
        prac_qs=prac_qs,
        total_questions=len(questions),
        exam_mode=mode,
        exam_seed=seed_val,
        question_ids_str=question_ids_str
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
def submit_exam():
    service = get_exam_service()
    result = service.grade_exam(request.form)
    return render_template("result.html", result=result)
