import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.expand_questions import EXPANDED_SHORT, EXPANDED_DESC, EXPANDED_PRAC
from scripts.new_questions_batch import NEW_SHORT_QUESTIONS, NEW_DESC_QUESTIONS, NEW_PRAC_QUESTIONS

# 1. 기존 18문항 로드
with open('app/data/questions.json', encoding='utf-8') as f:
    existing_18 = json.load(f)
assert len(existing_18) == 18, f"Expected 18 existing questions, got {len(existing_18)}"

# 2. expand_questions 보정 적용
adjusted_short = []
for q in EXPANDED_SHORT:
    q_copy = dict(q)
    if q_copy['id'] == 'Q-SHORT-019':
        q_copy['category'] = '네트워크 보안'
    elif q_copy['id'] == 'Q-SHORT-023':
        q_copy['concept_id'] = 'CON-MGT-03'
    elif q_copy['id'] == 'Q-SHORT-026':
        q_copy['concept_id'] = 'CON-MGT-04'
    elif q_copy['id'] == 'Q-SHORT-034':
        q_copy['concept_id'] = 'CON-MGT-03'
    elif q_copy['id'] == 'Q-SHORT-036':
        q_copy['concept_id'] = 'CON-MGT-02'
    adjusted_short.append(q_copy)

adjusted_desc = []
for q in EXPANDED_DESC:
    q_copy = dict(q)
    if q_copy['id'] == 'Q-DESC-011':
        q_copy['concept_id'] = 'CON-SEC-02'
    adjusted_desc.append(q_copy)

adjusted_prac = []
for q in EXPANDED_PRAC:
    q_copy = dict(q)
    if q_copy['id'] == 'Q-PRAC-006':
        q_copy['category'] = '네트워크 보안'
    adjusted_prac.append(q_copy)

# 3. 조립: 기존 18문항 유지 + 추가 문항 순서대로 결합
all_short = [q for q in existing_18 if q['type'] == 'short'] + adjusted_short + NEW_SHORT_QUESTIONS
all_desc = [q for q in existing_18 if q['type'] == 'descriptive'] + adjusted_desc + NEW_DESC_QUESTIONS
all_prac = [q for q in existing_18 if q['type'] == 'practical'] + adjusted_prac + NEW_PRAC_QUESTIONS

final_bank = all_short + all_desc + all_prac

print(f"=== Assembled Bank Statistics ===")
print(f"Total Short Questions: {len(all_short)} (12 existing + 24 batch1 + 5 batch2)")
print(f"Total Desc  Questions: {len(all_desc)} (4 existing + 8 batch1 + 3 batch2)")
print(f"Total Prac  Questions: {len(all_prac)} (2 existing + 4 batch1 + 2 batch2)")
print(f"Total Bank Questions : {len(final_bank)}")

# 4. 검증
with open('app/data/concepts.json', encoding='utf-8') as f:
    concepts = json.load(f)
c_ids = {c['id'] for c in concepts}

with open('app/data/sources.json', encoding='utf-8') as f:
    sources = json.load(f)
s_ids = {s['id'] for s in sources}

ALLOWED_CATEGORIES = {
    "시스템 보안",
    "네트워크 보안",
    "애플리케이션 보안",
    "정보보안 일반 및 암호학",
    "정보보호 관리 및 법규"
}

q_ids = set()
for q in final_bank:
    # ID 고유성
    assert q['id'] not in q_ids, f"Duplicate Question ID: {q['id']}"
    q_ids.add(q['id'])
    
    # Category
    assert q['category'] in ALLOWED_CATEGORIES, f"Invalid category in {q['id']}: {q['category']}"
    
    # Concept & Source
    assert q['concept_id'] in c_ids, f"Unknown concept_id in {q['id']}: {q['concept_id']}"
    assert q['source_id'] in s_ids, f"Unknown source_id in {q['id']}: {q['source_id']}"
    assert isinstance(q['source_page'], int) and q['source_page'] > 0, f"Invalid page in {q['id']}"
    
    # 배점 및 루브릭
    if q['type'] == 'short':
        assert q['score'] == 3
        assert q['grading_mode'] in ('normalized', 'strict')
        if q.get('sub_questions'):
            assert abs(sum(sq['score'] for sq in q['sub_questions']) - 3.0) < 0.01
        else:
            assert q.get('answer') is not None
    elif q['type'] == 'descriptive':
        assert q['score'] == 12
        assert q.get('sub_questions') is not None
        assert abs(sum(sq['score'] for sq in q['sub_questions']) - 12.0) < 0.01
    elif q['type'] == 'practical':
        assert q['score'] == 16
        assert q.get('sub_questions') is not None
        assert abs(sum(sq['score'] for sq in q['sub_questions']) - 16.0) < 0.01

print("\nALL 64 QUESTIONS PASSED FULL SCHEMA AND INTEGRITY VALIDATION!")

# 5. questions.json 저장
with open('app/data/questions.json', 'w', encoding='utf-8') as f:
    json.dump(final_bank, f, ensure_ascii=False, indent=2)

print("Successfully written 64 questions to app/data/questions.json!")
