import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.data_loader import DataLoader

loader = DataLoader()
questions = loader.load_questions()
concepts = loader.load_concepts()
c_dict = {c["id"]: c for c in concepts}

print(f"Total Questions: {len(questions)}")
print(f"Total Concepts: {len(concepts)}\n")

for idx, q in enumerate(questions, 1):
    qid = q["id"]
    qtype = q["type"]
    cat = q["category"]
    cid = q.get("concept_id")
    c_info = c_dict.get(cid, {})
    c_name = c_info.get("name", "UNKNOWN")
    c_cat = c_info.get("category", "UNKNOWN")
    
    ans = q.get("answer")
    if not ans and q.get("sub_questions"):
        ans = [s.get("answer") or s.get("model_answer", "")[:30] for s in q["sub_questions"]]
        
    print(f"[{idx:02d}] {qid} ({qtype})")
    print(f"     Category: {cat}")
    print(f"     Concept : {cid} -> [{c_name}] (Concept Category: {c_cat})")
    print(f"     Q       : {q['question'].splitlines()[0]}")
    print(f"     Answer  : {ans}")
    print(f"     Tags    : {q.get('tags')}")
    print("=" * 80)
