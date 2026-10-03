import json

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Group by concept
by_concept = {}
for q in questions:
    by_concept.setdefault(q["concept_id"], []).append(q)

print(f"Total Concepts used: {len(by_concept)}")
for cid, qlist in by_concept.items():
    print(f"\nConcept: {cid} ({len(qlist)} questions)")
    for q in qlist:
        ans_preview = ""
        if q["type"] == "short":
            if q.get("sub_questions"):
                ans_preview = str([s["answer"] for s in q["sub_questions"]])
            else:
                ans_preview = str(q.get("answer"))
        else:
            ans_preview = f"Sub-qs: {len(q.get('sub_questions', []))}"
        print(f"  [{q['id']}] ({q['type']}) Page {q['source_page']} - Ans: {ans_preview} | Q: {q['question'][:40]}...")
