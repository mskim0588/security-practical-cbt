import json

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    qs = [q for q in json.load(f) if q["type"] == "short"]

ans_map = {}
for q in qs:
    answers = []
    if q.get("sub_questions"):
        for s in q["sub_questions"]:
            answers.append(str(s["answer"]).strip().lower())
    else:
        answers.append(str(q["answer"]).strip().lower())
    for a in answers:
        ans_map.setdefault(a, []).append(q["id"])

print("--- OVERLAPPING SHORT ANSWERS ---")
found = False
for a, qids in ans_map.items():
    if len(qids) > 1:
        found = True
        print(f"Answer '{a}': {qids}")
if not found:
    print("None! All short answers are distinct.")
