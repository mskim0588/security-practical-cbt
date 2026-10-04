# -*- coding: utf-8 -*-
"""
Inspect all 24 Practical Questions in detail for technical accuracy.
"""
import os
import json

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
QUESTIONS_FILE = os.path.join(BASE_DIR, "app", "data", "questions.json")
EXPLANATIONS_FILE = os.path.join(BASE_DIR, "app", "data", "explanations.json")

def inspect_all_practicals():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    practicals = [q for q in questions if q["type"] == "practical"]

    with open(EXPLANATIONS_FILE, "r", encoding="utf-8") as f:
        explanations = json.load(f)

    for idx, q in enumerate(practicals, 1):
        qid = q["id"]
        exp = explanations.get(qid, {})
        cid = q.get("concept_id", "")
        cat = q.get("category", "")
        q_text = q.get("question", "")
        model_ans = q.get("model_answer", "")
        subs = q.get("sub_questions") or []

        print("=" * 80)
        print(f"[{idx:02d}/24] {qid} | Concept: {cid} | Category: {cat} | Score: {q.get('score')}점")
        print(f"Source: {q.get('source_id')} p.{q.get('source_page')}")
        print("-" * 80)
        print(f"[지문/요구사항]:\n{q_text}")
        print("-" * 80)
        print(f"[모범 답안]:\n{model_ans}")
        print("-" * 80)
        print(f"[소문항 ({len(subs)}개)]:")
        for s in subs:
            print(f"  - 소문항 {s.get('sub_id')} ({s.get('score')}점): {s.get('prompt')}")
            print(f"    키워드: {s.get('keywords')}")
        print("-" * 80)
        print(f"[해설 - Overview]: {exp.get('overview')}")
        print(f"[해설 - 관련 명령어]: {exp.get('related_commands')}")
        print(f"[해설 - 오답 함정]: {exp.get('why_wrong_common_traps')}")
        print()

if __name__ == "__main__":
    inspect_all_practicals()
