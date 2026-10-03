import json

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    qs = [q for q in json.load(f) if q.get("grading_mode") == "strict"]

print(f"Total strict questions: {len(qs)}")
for q in qs:
    ans = [s["answer"] for s in q["sub_questions"]] if q.get("sub_questions") else q.get("answer")
    acc = [s["accepted_answers"] for s in q["sub_questions"]] if q.get("sub_questions") else q.get("accepted_answers")
    print(f"[{q['id']}] Page {q['source_page']} - {q['concept_id']}")
    print(f"  Question: {q['question'][:60]}...")
    print(f"  Ans: {ans}")
    print(f"  Acc: {acc}")
