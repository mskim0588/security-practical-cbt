import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    qs = json.load(f)

print(f"Total questions: {len(qs)}")

types = Counter(q["type"] for q in qs)
print("\n--- TYPE DISTRIBUTION ---")
for t, c in types.items():
    print(f"  {t}: {c}")

cats = Counter(q["category"] for q in qs)
print("\n--- CATEGORY DISTRIBUTION ---")
for cat, c in cats.items():
    print(f"  {cat}: {c} ({c/len(qs)*100:.1f}%)")

print("\n--- CATEGORY x TYPE BREAKDOWN ---")
by_cat_type = {}
for q in qs:
    c = q["category"]
    t = q["type"]
    by_cat_type.setdefault(c, Counter())[t] += 1
for cat, t_counts in sorted(by_cat_type.items()):
    print(f"  {cat}: short={t_counts.get('short', 0)}, desc={t_counts.get('descriptive', 0)}, prac={t_counts.get('practical', 0)}")

srcs = Counter(q["source_id"] for q in qs)
print("\n--- SOURCE DISTRIBUTION ---")
for s, c in sorted(srcs.items()):
    print(f"  {s}: {c}")

concepts = Counter(q["concept_id"] for q in qs)
print("\n--- CONCEPT DISTRIBUTION ---")
for cid, c in sorted(concepts.items()):
    print(f"  {cid}: {c}")

short_modes = Counter(q.get("grading_mode") for q in qs if q["type"] == "short")
print("\n--- SHORT GRADING MODE ---")
for m, c in short_modes.items():
    print(f"  {m}: {c}")
