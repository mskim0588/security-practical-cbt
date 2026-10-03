# -*- coding: utf-8 -*-
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data")
with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

pracs = [q for q in questions if q["type"] == "practical"]
print(f"Total Practical Questions: {len(pracs)}")

for p in pracs:
    qid = p["id"]
    cat = p.get("category")
    sid = p.get("source_id")
    spage = p.get("source_page")
    subs = p.get("sub_questions", [])
    scores = [s.get("score", 0) for s in subs]
    tot_score = sum(scores)
    
    print(f"\n==================================================")
    print(f"[{qid}] Category: {cat} | Source: {sid} p.{spage} | Total: {tot_score}점 (Subs: {scores})")
    print(f"Question: {p['question'][:120]}...")
    for sub in subs:
        print(f"  Sub {sub['sub_id']} ({sub['score']}점): {sub['prompt'][:80]}...")
        ma = sub.get("model_answer", "").replace('\n', ' ')
        print(f"    Ans: {ma[:80]}...")
        kws = sub.get("rubric", {}).get("keywords", [])
        print(f"    Keywords: {kws}")
