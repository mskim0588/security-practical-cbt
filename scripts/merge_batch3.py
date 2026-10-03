# -*- coding: utf-8 -*-
"""
Merge Batch 3 (40 questions) into app/data/questions.json
Preserves baseline 140 questions 100% untouched.
"""
import os
import sys
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch3_chunk1_builder import CHUNK_1_QUESTIONS
from scripts.batch3_chunk2_builder import CHUNK_2_QUESTIONS
from scripts.batch3_chunk3_builder import CHUNK_3_QUESTIONS
from scripts.batch3_chunk4_builder import CHUNK_4_QUESTIONS

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data", "questions.json")
BACKUP_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data", "questions.json.batch3_pre_bak")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    baseline = json.load(f)

baseline_hash = hashlib.sha256(open(DATA_PATH, "rb").read()).hexdigest()
backup_hash = hashlib.sha256(open(BACKUP_PATH, "rb").read()).hexdigest()
assert baseline_hash == backup_hash, "Baseline modified before merge!"

new_questions = CHUNK_1_QUESTIONS + CHUNK_2_QUESTIONS + CHUNK_3_QUESTIONS + CHUNK_4_QUESTIONS
assert len(new_questions) == 40, f"Expected 40 new questions, got {len(new_questions)}"

all_180 = baseline + new_questions
assert len(all_180) == 180, f"Expected 180 total questions, got {len(all_180)}"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(all_180, f, ensure_ascii=False, indent=2)

print(f"Successfully merged 40 questions into {DATA_PATH}!")
print(f"Total questions in questions.json: {len(all_180)}")

# Verify the first 140 elements match baseline exactly
with open(DATA_PATH, "r", encoding="utf-8") as f:
    reloaded = json.load(f)

assert reloaded[:140] == baseline, "First 140 elements do not match baseline!"
print(">> Verification passed: Baseline 140 elements are 100% identical.")
