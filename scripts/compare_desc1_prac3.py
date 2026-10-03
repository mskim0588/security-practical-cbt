import json

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    qs = {q["id"]: q for q in json.load(f)}

print("=== Q-DESC-001 ===")
print("Source:", qs["Q-DESC-001"]["source_id"], "p.", qs["Q-DESC-001"]["source_page"])
print("Question:", qs["Q-DESC-001"]["question"])
for sub in qs["Q-DESC-001"]["sub_questions"]:
    print(f"Sub {sub['sub_id']} ({sub['score']}pt): {sub['model_answer']}")

print("\n=== Q-PRAC-003 ===")
print("Source:", qs["Q-PRAC-003"]["source_id"], "p.", qs["Q-PRAC-003"]["source_page"])
print("Question:", qs["Q-PRAC-003"]["question"])
for sub in qs["Q-PRAC-003"]["sub_questions"]:
    print(f"Sub {sub['sub_id']} ({sub['score']}pt): {sub['model_answer']}")
