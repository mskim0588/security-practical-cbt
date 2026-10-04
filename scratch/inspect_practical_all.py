import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    qs = [q for q in json.load(f) if q.get('type') == 'practical']

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    exps = json.load(f)

print(f"Total practical questions: {len(qs)}")
for q in qs:
    qid = q['id']
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    subs = q.get('sub_questions', [])
    print(f"[{qid}] subs={len(subs)} | score={q.get('score')} | stem={stem[:60]}...")
    for s in subs:
        print(f"   Sub {s.get('sub_id')} ({s.get('score')}점): {s.get('prompt')}")
        print(f"      keywords: {s.get('rubric', {}).get('keywords')}")
