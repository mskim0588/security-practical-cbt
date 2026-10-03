# -*- coding: utf-8 -*-
"""
Apply Goal 2E-Fixes to questions.json
1. Q-SHORT-001: Add primary answers to accepted_answers (Sub A: '침해요인 발생 가능성', Sub B: '법적 준거성')
2. Q-SHORT-002: Add primary answers to accepted_answers (Sub A: 'API', Sub B: 'Plug-in', Sub C: 'TDE')
3. Q-DESC-011: Align category to '정보보안 일반 및 암호학' matching CON-SEC-02 (Digital Forensics 5 Principles)
4. Q-SHORT-082: Align category to '정보보안 일반 및 암호학' matching CON-SEC-02 (Cyber Crisis Alert)
"""
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data", "questions.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

assert len(questions) == 180, f"Expected 180 questions, got {len(questions)}"

modified_count = 0

for q in questions:
    qid = q["id"]

    # 1. Q-SHORT-001
    if qid == "Q-SHORT-001":
        print("Modifying Q-SHORT-001...")
        for sub in q.get("sub_questions", []):
            if sub["label"] == "A":
                ans = sub["answer"] # '침해요인 발생 가능성'
                if ans not in sub["accepted_answers"]:
                    sub["accepted_answers"].insert(0, ans)
                    print(f"  Sub A accepted_answers updated: {sub['accepted_answers']}")
            elif sub["label"] == "B":
                ans = sub["answer"] # '법적 준거성'
                if ans not in sub["accepted_answers"]:
                    sub["accepted_answers"].insert(0, ans)
                    print(f"  Sub B accepted_answers updated: {sub['accepted_answers']}")
        modified_count += 1

    # 2. Q-SHORT-002
    elif qid == "Q-SHORT-002":
        print("Modifying Q-SHORT-002...")
        for sub in q.get("sub_questions", []):
            if sub["label"] == "A":
                ans = sub["answer"] # 'API'
                if ans not in sub["accepted_answers"]:
                    sub["accepted_answers"].insert(0, ans)
                    print(f"  Sub A accepted_answers updated: {sub['accepted_answers']}")
            elif sub["label"] == "B":
                ans = sub["answer"] # 'Plug-in'
                if ans not in sub["accepted_answers"]:
                    sub["accepted_answers"].insert(0, ans)
                    print(f"  Sub B accepted_answers updated: {sub['accepted_answers']}")
            elif sub["label"] == "C":
                ans = sub["answer"] # 'TDE'
                if ans not in sub["accepted_answers"]:
                    sub["accepted_answers"].insert(0, ans)
                    print(f"  Sub C accepted_answers updated: {sub['accepted_answers']}")
        modified_count += 1

    # 3. Q-DESC-011
    elif qid == "Q-DESC-011":
        print(f"Modifying Q-DESC-011: category '{q['category']}' -> '정보보안 일반 및 암호학' (matches CON-SEC-02)")
        q["category"] = "정보보안 일반 및 암호학"
        modified_count += 1

    # 4. Q-SHORT-082
    elif qid == "Q-SHORT-082":
        print(f"Modifying Q-SHORT-082: category '{q['category']}' -> '정보보안 일반 및 암호학' (matches CON-SEC-02)")
        q["category"] = "정보보안 일반 및 암호학"
        modified_count += 1

print(f"\nTotal questions modified: {modified_count} (Expected: 4)")
assert modified_count == 4, f"Modified count {modified_count} != 4"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("Saved updated questions.json successfully.")
