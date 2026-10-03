# -*- coding: utf-8 -*-
import os
import sys
import json
import shutil
import hashlib

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch2_chunk1_builder import CHUNK_1_QUESTIONS
from scripts.batch2_chunk2_builder import CHUNK_2_QUESTIONS
from scripts.batch2_chunk3_builder import CHUNK_3_QUESTIONS
from scripts.batch2_chunk4_builder import CHUNK_4_QUESTIONS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")
Q_PATH = os.path.join(DATA_DIR, "questions.json")
BAK_PATH = os.path.join(DATA_DIR, "questions.json.batch2_pre_bak")

with open(Q_PATH, "r", encoding="utf-8") as f:
    baseline_data = f.read()

baseline_qs = json.loads(baseline_data)
assert len(baseline_qs) == 100, f"Expected 100 baseline questions, got {len(baseline_qs)}"

baseline_hash = hashlib.sha256(baseline_data.encode("utf-8")).hexdigest()
print(f"Baseline 100 questions count: {len(baseline_qs)}")
print(f"Baseline SHA256: {baseline_hash}")

# Create backup
shutil.copy2(Q_PATH, BAK_PATH)
print(f"Created backup at: {BAK_PATH}")

new_40 = CHUNK_1_QUESTIONS + CHUNK_2_QUESTIONS + CHUNK_3_QUESTIONS + CHUNK_4_QUESTIONS
assert len(new_40) == 40, f"Expected 40 new questions, got {len(new_40)}"

merged_qs = baseline_qs + new_40
assert len(merged_qs) == 140, f"Expected 140 questions, got {len(merged_qs)}"

# Verify first 100 questions in merged_qs are identical to baseline_qs
for i in range(100):
    assert merged_qs[i] == baseline_qs[i], f"Mismatch at index {i} ({merged_qs[i]['id']})"

# Write merged questions.json
with open(Q_PATH, "w", encoding="utf-8") as f:
    json.dump(merged_qs, f, ensure_ascii=False, indent=2)

print(f"Successfully merged {len(new_40)} questions into {Q_PATH} (Total: {len(merged_qs)})")

# Re-read and verify
with open(Q_PATH, "r", encoding="utf-8") as f:
    reloaded_qs = json.load(f)

assert len(reloaded_qs) == 140
for i in range(100):
    assert reloaded_qs[i] == baseline_qs[i], f"Reload mismatch at index {i}"

print("Baseline 100 questions fingerprint preserved with 100% immutability!")
print("Merged Breakdown:")
print("  Short:", len([q for q in reloaded_qs if q["type"] == "short"]))
print("  Descriptive:", len([q for q in reloaded_qs if q["type"] == "descriptive"]))
print("  Practical:", len([q for q in reloaded_qs if q["type"] == "practical"]))
print("  Total:", len(reloaded_qs))
