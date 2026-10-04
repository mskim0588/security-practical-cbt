import json

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    explanations = json.load(f)

desc_issues = []
descriptive_qs = [q for q in questions if q.get('type') == 'descriptive']

for q in descriptive_qs:
    qid = q['id']
    exp = explanations.get(qid)
    if not exp:
        desc_issues.append((qid, 'Missing explanation'))
        continue
    # Check rubric alignment
    q_score = q.get('score', 12)
    rubrics = exp.get('practical_scoring_criteria') or []
    rubric_sum = sum(r.get('score', 0) for r in rubrics)
    if rubric_sum != q_score:
        desc_issues.append((qid, f'Score mismatch: q={q_score}, rubric={rubric_sum}'))
    
    # Check overview
    overview = exp.get('overview', '')
    if len(overview) < 20:
        desc_issues.append((qid, f'Short overview: {overview}'))
    
    # Check why_correct content
    wc = exp.get('why_correct', '')
    if len(wc) < 30:
        desc_issues.append((qid, f'Short why_correct: {wc}'))
    
    # Check why_wrong_common_traps
    traps = exp.get('why_wrong_common_traps') or []
    if len(traps) == 0:
        desc_issues.append((qid, 'No common traps defined'))

    # Check sub_questions alignment
    sub_qs = q.get('sub_questions') or []
    if len(sub_qs) > 0 and len(rubrics) != len(sub_qs):
        desc_issues.append((qid, f'Subquestion count ({len(sub_qs)}) != rubric count ({len(rubrics)})'))

print(f"Total descriptive questions: {len(descriptive_qs)}")
print(f"Issues found: {len(desc_issues)}")
for item in desc_issues:
    print(f"  - {item[0]}: {item[1]}")
