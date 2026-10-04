import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    qs = {q['id']: q for q in json.load(f)}

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    exps = json.load(f)

for i in range(1, 31):
    qid = f'Q-SHORT-{i:03d}'
    q = qs[qid]
    exp = exps[qid]
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    print(f"[{qid}] ans='{q.get('answer')}' | cid={q.get('concept_id')} | stem={stem[:50]}...")
    ph = "표준 정답" in exp.get('why_correct', '')
    traps = [t.get('confused_term_or_misunderstanding', '') for t in exp.get('why_wrong_common_traps', [])]
    print(f"   ph={ph} | traps={traps}")
