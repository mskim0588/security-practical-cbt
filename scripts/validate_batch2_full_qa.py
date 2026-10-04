# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch2_chunk1_builder import CHUNK_1_QUESTIONS
from scripts.batch2_chunk2_builder import CHUNK_2_QUESTIONS
from scripts.batch2_chunk3_builder import CHUNK_3_QUESTIONS
from scripts.batch2_chunk4_builder import CHUNK_4_QUESTIONS

PDF_DIR = os.environ.get("PRIVATE_SOURCE_DIR", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)
source_map = {s["id"]: s for s in sources}

with open(os.path.join(DATA_DIR, "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)
concept_map = {c["id"]: c for c in concepts}

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    baseline_100 = json.load(f)
baseline_ids = set(q["id"] for q in baseline_100)

new_questions = CHUNK_1_QUESTIONS + CHUNK_2_QUESTIONS + CHUNK_3_QUESTIONS + CHUNK_4_QUESTIONS

print("==================================================")
print("=== BATCH 2 COMPREHENSIVE QA GATE VALIDATION ===")
print("==================================================")
print(f"Baseline 100 questions: {len(baseline_100)}")
print(f"Batch 2 New questions: {len(new_questions)}")
print(f"Total after merge: {len(baseline_100) + len(new_questions)}")

# Check ID counts and types
shorts = [q for q in new_questions if q["type"] == "short"]
descs = [q for q in new_questions if q["type"] == "descriptive"]
pracs = [q for q in new_questions if q["type"] == "practical"]
print(f"New breakdown: Short={len(shorts)}, Desc={len(descs)}, Prac={len(pracs)}")

# 1. Schema, Score, Category, Concept Check
errors = []
ALLOWED_CATS = {
    "시스템 보안",
    "네트워크 보안",
    "애플리케이션 보안",
    "정보보안 일반 및 암호학",
    "정보보호 관리 및 법규"
}

seen_ids = set()
for q in new_questions:
    qid = q["id"]
    if qid in baseline_ids:
        errors.append(f"Collision with baseline ID: {qid}")
    if qid in seen_ids:
        errors.append(f"Duplicate new ID: {qid}")
    seen_ids.add(qid)

    cat = q.get("category")
    if cat not in ALLOWED_CATS:
        errors.append(f"Invalid category in {qid}: {cat}")

    cid = q.get("concept_id")
    if cid not in concept_map:
        errors.append(f"Unregistered concept_id in {qid}: {cid}")

    sid = q.get("source_id")
    if sid not in source_map:
        errors.append(f"Unregistered source_id in {qid}: {sid}")
    else:
        max_p = source_map[sid]["total_pages"]
        spage = q.get("source_page", 0)
        if spage < 1 or spage > max_p:
            errors.append(f"Invalid page {spage} for {sid} (max {max_p}) in {qid}")

    qtype = q["type"]
    score = q["score"]
    if qtype == "short":
        if score != 3:
            errors.append(f"Short score {score} != 3 in {qid}")
        if not q.get("answer"):
            errors.append(f"Missing answer in {qid}")
        if q.get("grading_mode") not in ("normalized", "strict"):
            errors.append(f"Invalid grading_mode in {qid}: {q.get('grading_mode')}")
    elif qtype == "descriptive":
        if score != 12:
            errors.append(f"Desc score {score} != 12 in {qid}")
        s_sum = sum(s["score"] for s in q.get("sub_questions", []))
        if s_sum != 12:
            errors.append(f"Desc sub_questions sum {s_sum} != 12 in {qid}")
        for s in q.get("sub_questions", []):
            if "prompt" not in s:
                errors.append(f"Missing prompt in sub_question of {qid}")
            if "keywords" not in s.get("rubric", {}):
                errors.append(f"Missing keywords in sub_question of {qid}")
            for g in s.get("rubric", {}).get("keywords", []):
                if not isinstance(g, list):
                    errors.append(f"Keyword group not list in {qid}: {g}")
    elif qtype == "practical":
        if score != 16:
            errors.append(f"Prac score {score} != 16 in {qid}")
        s_sum = sum(s["score"] for s in q.get("sub_questions", []))
        if s_sum != 16:
            errors.append(f"Prac sub_questions sum {s_sum} != 16 in {qid}")
        for s in q.get("sub_questions", []):
            if "prompt" not in s:
                errors.append(f"Missing prompt in sub_question of {qid}")
            if "keywords" not in s.get("rubric", {}):
                errors.append(f"Missing keywords in sub_question of {qid}")
            for g in s.get("rubric", {}).get("keywords", []):
                if not isinstance(g, list):
                    errors.append(f"Keyword group not list in {qid}: {g}")

print(f"\n1. Schema / Score / Concept Check: {len(errors)} errors")
if errors:
    for e in errors:
        print("  ERROR:", e)

# 2. PDF Grounding Check
pdf_readers = {}
def get_reader(sid):
    if sid not in pdf_readers:
        fn = source_map[sid]["filename"]
        pdf_readers[sid] = pypdf.PdfReader(os.path.join(PDF_DIR, fn))
    return pdf_readers[sid]

grounding_issues = []
print(f"\n2. Verifying PDF Grounding for {len(new_questions)} new questions...")
for q in new_questions:
    qid = q["id"]
    sid = q["source_id"]
    spage = q["source_page"]
    reader = get_reader(sid)
    page_text = reader.pages[spage - 1].extract_text() or ""
    page_clean = re.sub(r'\s+', '', page_text).lower()

    check_tokens = []
    if q.get("answer"):
        check_tokens.append(q["answer"])
        for a in q.get("accepted_answers", []):
            check_tokens.append(a)
    for s in q.get("sub_questions", []):
        for g in s.get("rubric", {}).get("keywords", []):
            check_tokens.extend(g)
        ma = s.get("model_answer", "")
        words = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', ma) if len(w) >= 2]
        check_tokens.extend(words[:5])

    matched = [t for t in set(check_tokens) if re.sub(r'\s+', '', str(t)).lower() in page_clean]
    if not matched:
        grounding_issues.append((qid, sid, spage, "0 tokens matched"))
        print(f"  FAIL: [{qid}] {sid} p.{spage} - 0 tokens matched")
    else:
        print(f"  PASS: [{qid}] {sid} p.{spage} ({len(matched)} matches): {list(matched)[:3]}")

print(f"\nGrounding Issues: {len(grounding_issues)}")
if grounding_issues:
    for g in grounding_issues:
        print("  ISSUE:", g)

# 3. De-duplication Check across 140 questions
print(f"\n3. Verifying De-duplication across all 140 questions...")
all_140 = baseline_100 + new_questions

def get_tokens(q):
    t = q["question"] + " "
    if q.get("answer"):
        t += str(q["answer"]) + " "
    for s in (q.get("sub_questions") or []):
        t += str(s.get("prompt", "")) + " "
        t += str(s.get("model_answer", "")) + " "
    tokens = set(re.findall(r'[가-힣]{2,}|[a-zA-Z0-9_\-\.]{3,}', t.lower()))
    stopwords = {"설명하시오", "기술하시오", "무엇인가", "대하여", "대해", "다음은", "관련하여", "위한", "있는", "하는", "경우", "각각"}
    return tokens - stopwords

tokens_list = [get_tokens(q) for q in all_140]
duplicates = []

for i in range(len(all_140)):
    for j in range(i + 1, len(all_140)):
        s1 = tokens_list[i]
        s2 = tokens_list[j]
        inter = s1 & s2
        union = s1 | s2
        sim = len(inter) / max(len(union), 1)
        if sim > 0.25:
            duplicates.append((sim, all_140[i]["id"], all_140[j]["id"], list(inter)[:8]))

print(f"Potential Duplicates found (Threshold > 0.25): {len(duplicates)}")
if duplicates:
    for sim, q1, q2, inter in duplicates:
        print(f"  SIMILARITY {sim:.2f}: {q1} vs {q2} | Shared: {inter}")

if not errors and not grounding_issues and len(duplicates) == 0:
    print("\n>>> ALL BATCH 2 QA GATE CHECKS PASSED PERFECTLY! (0 Errors, 0 Issues, 0 Duplicates) <<<")
