import json
import shutil
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch1_draft_builder import BATCH1_SHORT, BATCH1_DESC, BATCH1_PRAC

questions_path = "app/data/questions.json"
backup_path = "app/data/questions.json.batch1_bak"

shutil.copyfile(questions_path, backup_path)
print(f"Created backup at {backup_path}")

with open(questions_path, "r", encoding="utf-8") as f:
    existing_questions = json.load(f)

assert len(existing_questions) == 64, f"Expected 64 existing questions, found {len(existing_questions)}"

# Store fingerprint of existing 64 questions
existing_fingerprint = [(q["id"], q["question"][:30], q["score"]) for q in existing_questions]

new_questions = BATCH1_SHORT + BATCH1_DESC + BATCH1_PRAC
assert len(new_questions) == 36, f"Expected 36 new questions, found {len(new_questions)}"

combined = existing_questions + new_questions
assert len(combined) == 100, f"Expected 100 combined questions, found {len(combined)}"

# Verify first 64 questions are untouched
for i, q in enumerate(existing_questions):
    assert combined[i]["id"] == existing_fingerprint[i][0]
    assert combined[i]["question"][:30] == existing_fingerprint[i][1]
    assert combined[i]["score"] == existing_fingerprint[i][2]

with open(questions_path, "w", encoding="utf-8") as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print("Successfully written 100 questions to app/data/questions.json!")
