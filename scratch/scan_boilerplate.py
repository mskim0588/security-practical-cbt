import json
from collections import Counter

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    exps = json.load(f)

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    qs = {q['id']: q for q in json.load(f)}

print(f"Total explanations: {len(exps)}")

# 1. Check overview diversity
overview_counts = Counter(e.get('overview', '') for e in exps.values())
print(f"Unique overviews: {len(overview_counts)} / {len(exps)}")
common_overviews = [ov for ov, cnt in overview_counts.items() if cnt > 1]
print(f"Overviews appearing > 1 time: {len(common_overviews)}")
for ov in common_overviews[:5]:
    print(f"  [{overview_counts[ov]} times]: {ov[:60]}...")

# 2. Check why_correct diversity
wc_counts = Counter(e.get('why_correct', '') for e in exps.values())
print(f"\nUnique why_correct: {len(wc_counts)} / {len(exps)}")
common_wc = [(wc, cnt) for wc, cnt in wc_counts.items() if cnt > 1]
print(f"why_correct appearing > 1 time: {len(common_wc)}")
for wc, cnt in common_wc:
    print(f"  [{cnt} times]: {wc[:80]}...")

# 3. Check exam_strategy diversity
es_counts = Counter(e.get('exam_strategy', '') for e in exps.values())
print(f"\nUnique exam_strategy: {len(es_counts)} / {len(exps)}")
for es, cnt in es_counts.most_common(10):
    print(f"  [{cnt} times]: {es[:80]}...")

# 4. Check why_wrong_common_traps diversity
traps_flat = []
for qid, e in exps.items():
    traps = e.get('why_wrong_common_traps', [])
    for t in traps:
        traps_flat.append(t)

traps_counts = Counter(traps_flat)
print(f"\nTotal trap items: {len(traps_flat)}, Unique traps: {len(traps_counts)}")
for t, cnt in traps_counts.most_common(5):
    print(f"  [{cnt} times]: {t[:80]}...")

# 5. Check key_concept_points
kcp_flat = []
for qid, e in exps.items():
    for p in e.get('key_concept_points', []):
        kcp_flat.append(p)
kcp_counts = Counter(kcp_flat)
print(f"\nTotal key concept points: {len(kcp_flat)}, Unique: {len(kcp_counts)}")
for p, cnt in kcp_counts.most_common(5):
    print(f"  [{cnt} times]: {p[:80]}...")
