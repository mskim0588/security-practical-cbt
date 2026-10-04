import json

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    explanations = json.load(f)

ph_count = 0
ph_questions = []

for q in questions:
    qid = q['id']
    exp = explanations.get(qid, {})
    wc = exp.get('why_correct', '')
    if '표준 정답' in wc:
        ph_count += 1
        ph_questions.append((qid, q.get('type'), q.get('answer'), q.get('sub_questions')))

print(f"Total questions with '표준 정답': {ph_count}")
print(f"Sample with sub_questions: {[p for p in ph_questions if p[3]]}")
print(f"First 10 ph questions:")
for p in ph_questions[:10]:
    print(f"  {p[0]}: type={p[1]}, ans={p[2]}")
