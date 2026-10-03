import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.expand_questions import EXPANDED_SHORT, EXPANDED_DESC, EXPANDED_PRAC

ALLOWED_CATEGORIES = {
    "시스템 보안",
    "네트워크 보안",
    "애플리케이션 보안",
    "정보보안 일반 및 암호학",
    "정보보호 관리 및 법규"
}

with open('app/data/concepts.json', encoding='utf-8') as f:
    concepts = json.load(f)
c_dict = {c['id']: c for c in concepts}

print(f"Loaded {len(EXPANDED_SHORT)} short, {len(EXPANDED_DESC)} desc, {len(EXPANDED_PRAC)} prac.")

errors = []

# 1. 단답형 검증
for q in EXPANDED_SHORT:
    qid = q['id']
    if q['category'] not in ALLOWED_CATEGORIES:
        errors.append(f"{qid}: Invalid category '{q['category']}'")
    if q['concept_id'] not in c_dict:
        errors.append(f"{qid}: Unknown concept_id '{q['concept_id']}'")
    if q.get('grading_mode') not in ('normalized', 'strict'):
        errors.append(f"{qid}: Invalid grading_mode '{q.get('grading_mode')}'")
    if q['score'] != 3:
        errors.append(f"{qid}: Score is {q['score']}, expected 3")
    if q.get('sub_questions'):
        sub_sum = sum(sq['score'] for sq in q['sub_questions'])
        if abs(sub_sum - 3.0) > 0.01:
            errors.append(f"{qid}: Sub-questions sum {sub_sum} != 3.0")

# 2. 서술형 검증
for q in EXPANDED_DESC:
    qid = q['id']
    if q['category'] not in ALLOWED_CATEGORIES:
        errors.append(f"{qid}: Invalid category '{q['category']}'")
    if q['concept_id'] not in c_dict:
        errors.append(f"{qid}: Unknown concept_id '{q['concept_id']}'")
    if q['score'] != 12:
        errors.append(f"{qid}: Score is {q['score']}, expected 12")
    if not q.get('sub_questions'):
        errors.append(f"{qid}: Missing sub_questions")
    else:
        sub_sum = sum(sq['score'] for sq in q['sub_questions'])
        if abs(sub_sum - 12.0) > 0.01:
            errors.append(f"{qid}: Sub-questions sum {sub_sum} != 12.0")

# 3. 실무형 검증
for q in EXPANDED_PRAC:
    qid = q['id']
    if q['category'] not in ALLOWED_CATEGORIES:
        errors.append(f"{qid}: Invalid category '{q['category']}'")
    if q['concept_id'] not in c_dict:
        errors.append(f"{qid}: Unknown concept_id '{q['concept_id']}'")
    if q['score'] != 16:
        errors.append(f"{qid}: Score is {q['score']}, expected 16")
    if not q.get('sub_questions'):
        errors.append(f"{qid}: Missing sub_questions")
    else:
        sub_sum = sum(sq['score'] for sq in q['sub_questions'])
        if abs(sub_sum - 16.0) > 0.01:
            errors.append(f"{qid}: Sub-questions sum {sub_sum} != 16.0")

print(f"Total Errors Found: {len(errors)}")
for e in errors:
    print(" - ", e)
