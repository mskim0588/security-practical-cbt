import json

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    explanations = json.load(f)

desc_and_prac = [q for q in questions if q.get('type') in ('descriptive', 'practical')]
print(f"Total descriptive + practical questions: {len(desc_and_prac)}")

sample_q = desc_and_prac[0]
print(f"\n--- Sample {sample_q['id']} ---")
for s in sample_q.get('sub_questions', []):
    print(f"Sub {s.get('sub_id')}: prompt='{s.get('prompt')}', score={s.get('score')}")
    print(f"  model_answer: {s.get('model_answer')}")
    print(f"  rubric: {s.get('rubric')}")

sample_prac = [q for q in desc_and_prac if q.get('type') == 'practical'][0]
print(f"\n--- Sample Practical {sample_prac['id']} ---")
for s in sample_prac.get('sub_questions', []):
    print(f"Sub {s.get('sub_id')}: prompt='{s.get('prompt')}', score={s.get('score')}")
    print(f"  model_answer: {s.get('model_answer')}")
    print(f"  rubric: {s.get('rubric')}")
