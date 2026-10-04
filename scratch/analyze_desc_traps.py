import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    qs = [q for q in json.load(f) if q.get('type') == 'descriptive']

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    exps = json.load(f)

for q in qs:
    qid = q['id']
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    print(f"[{qid}] {stem[:60]}...")
