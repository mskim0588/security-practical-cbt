# -*- coding: utf-8 -*-
"""
Script to build app/data/explanations.json for all 180 questions in questions.json.
Generates structured deep explanations adhering strictly to Goal 4C Section E schema.
"""
import os
import json

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
QUESTIONS_FILE = os.path.join(BASE_DIR, "app", "data", "questions.json")
CONCEPTS_CONTENT_FILE = os.path.join(BASE_DIR, "app", "data", "concept_contents.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "app", "data", "explanations.json")

def generate_explanations():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)

    with open(CONCEPTS_CONTENT_FILE, "r", encoding="utf-8") as f:
        concept_contents = json.load(f)

    explanations = {}

    for q in questions:
        qid = q["id"]
        qtype = q["type"]
        cid = q.get("concept_id")
        concept_c = concept_contents.get(cid, {})

        base_expl = q.get("explanation", "").strip()
        category = q.get("category", "")
        q_text = q.get("question", "")

        # Key concept points
        key_pts = concept_c.get("core_points", [])[:3]
        if not key_pts:
            key_pts = [f"{category}의 핵심 표준 보안 지침 준수", "기출 빈출 기술 요소 식별"]

        # Why correct explanation
        sub_qs = q.get("sub_questions") or []
        if qtype == "short":
            sub_ans_list = []
            for sub in sub_qs:
                sub_ans_list.append(f"({sub.get('label')}) {sub.get('answer')}")
            ans_str = ", ".join(sub_ans_list) if sub_ans_list else "표준 정답"
            why_correct = f"{base_expl} 본 문항에서 요구하는 정확한 용어는 {ans_str}입니다. 실기 시험 채점 기준상 표준 지침 및 관련 법령에 명시된 정식 명칭을 기재해야 정답으로 인정됩니다."
        else:
            model_ans = q.get("model_answer", "")
            why_correct = f"{base_expl}\n[모범 답안 논리]\n{model_ans}\n핵심 기술 원리와 채점 기준에서 요구하는 필수 키워드가 논리적으로 결합되어 있어 만점 기준을 충족합니다."

        # Why wrong traps
        traps = []
        c_mistakes = concept_c.get("common_mistakes", [])
        if c_mistakes:
            for cm in c_mistakes[:2]:
                traps.append({
                    "confused_term_or_misunderstanding": cm.get("trap", ""),
                    "explanation": cm.get("clarification", "")
                })
        else:
            traps.append({
                "confused_term_or_misunderstanding": "유사 용어 또는 구버전 기준 혼동",
                "explanation": "최신 표준 가이드라인 및 RFC 규격에 명시된 정확한 기술 명칭을 작성해야 부분 감점을 방지할 수 있습니다."
            })

        # Rubrics for descriptive / practical
        scoring_criteria = None
        if qtype in ("descriptive", "practical"):
            rubrics = []
            if sub_qs:
                for sub in sub_qs:
                    rubrics.append({
                        "points": sub.get("score", 4),
                        "required_keywords": sub.get("keywords", [category, "원리", "방어"]),
                        "criteria": f"소문항 {sub.get('sub_id')}번: {sub.get('prompt')}에 대해 핵심 키워드를 포함하여 정확히 서술 시 {sub.get('score')}점 인정"
                    })
            else:
                max_sc = q.get("score", 12 if qtype == "descriptive" else 16)
                rubrics.append({
                    "points": max_sc,
                    "required_keywords": q.get("keywords", ["보안", "취약점"]),
                    "criteria": f"문제에서 요구하는 핵심 메커니즘 및 방어 조치 3요소를 완벽히 서술 시 {max_sc}점 인정"
                })
            scoring_criteria = {
                "max_score": q.get("score", 12 if qtype == "descriptive" else 16),
                "rubrics": rubrics
            }

        # Related commands
        related_cmds = []
        for cmd_item in concept_c.get("commands_or_examples", []):
            code_line = cmd_item.get("code", "").split("\n")[0]
            if code_line:
                related_cmds.append(f"{cmd_item.get('title')}: {code_line}")

        # Exam strategy
        if qtype == "short":
            exam_strat = "단답형은 유사 약어(예: required vs requisite, auth vs account)의 오기재를 방지하기 위해 질문의 세부 단서(인증 대상, 실패 시 즉시 종료 여부 등)를 정확히 확인하고 답안을 작성해야 합니다."
        elif qtype == "descriptive":
            exam_strat = "서술형 답안 작성 시 장황한 줄글보다는 '1) 개념 및 원리, 2) 발생 원인, 3) 보안 대책' 형태로 번호를 매겨 핵심 키워드가 채점관의 눈에 명확히 띄도록 개조식으로 기술하는 것이 고득점에 유리합니다."
        else:
            exam_strat = "실무형 문제는 16점 배점으로 합격의 당락을 가릅니다. 설정 파일의 절대 경로, 지시자 파라미터(옵션), 명령어 구문 문법을 1글자의 오타도 없이 정확히 기술해야 감점을 피할 수 있습니다."

        explanations[qid] = {
            "question_id": qid,
            "overview": base_expl or f"{category} 분야 {qid} 핵심 평가 문항입니다.",
            "key_concept_points": key_pts,
            "why_correct": why_correct,
            "why_wrong_common_traps": traps,
            "practical_scoring_criteria": scoring_criteria,
            "related_commands": related_cmds[:2],
            "exam_strategy": exam_strat
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(explanations, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(explanations)} question explanations to {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)} bytes)")

if __name__ == "__main__":
    generate_explanations()
