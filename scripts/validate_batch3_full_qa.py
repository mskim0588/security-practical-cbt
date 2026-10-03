# -*- coding: utf-8 -*-
"""
Batch 3 Comprehensive QA Gate Validation Script
Validates:
1. Baseline 140 questions immutability (SHA256 vs backup)
2. Schema, Score (Short 3, Desc 12, Prac 16), Concept ID, Category
3. Active Sources: All 12 PDF sources active
4. Ground truth token matching for all 40 new questions against SRC-06, SRC-07, SRC-08, SRC-12
5. De-duplication across all 180 questions (Jaccard similarity threshold 0.25)
"""
import os
import sys
import json
import re
import hashlib
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch3_chunk1_builder import CHUNK_1_QUESTIONS
from scripts.batch3_chunk2_builder import CHUNK_2_QUESTIONS
from scripts.batch3_chunk3_builder import CHUNK_3_QUESTIONS
from scripts.batch3_chunk4_builder import CHUNK_4_QUESTIONS

PDF_DIR = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)
source_map = {s["id"]: s for s in sources}

with open(os.path.join(DATA_DIR, "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)
concept_map = {c["id"]: c for c in concepts}

with open(os.path.join(DATA_DIR, "questions.json.batch3_pre_bak"), "rb") as f:
    pre_bak_bytes = f.read()
pre_bak_hash = hashlib.sha256(pre_bak_bytes).hexdigest()

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    current_baseline = json.load(f)
current_baseline_hash = hashlib.sha256(open(os.path.join(DATA_DIR, "questions.json"), "rb").read()).hexdigest()

baseline_ids = set(q["id"] for q in current_baseline)
new_questions = CHUNK_1_QUESTIONS + CHUNK_2_QUESTIONS + CHUNK_3_QUESTIONS + CHUNK_4_QUESTIONS
all_180 = current_baseline + new_questions

print("==================================================")
print("=== BATCH 3 COMPREHENSIVE QA GATE VALIDATION ===")
print("==================================================")
print(f"Baseline 140 questions SHA256: {current_baseline_hash}")
print(f"Pre-backup 140 questions SHA256: {pre_bak_hash}")
assert current_baseline_hash == pre_bak_hash, "ERROR: Baseline 140 questions modified!"
print(">> Baseline 140 Immutability: 100% IDENTICAL (PASS)")

print(f"\nBaseline 140 count: {len(current_baseline)}")
print(f"Batch 3 New questions: {len(new_questions)}")
print(f"Total after merge: {len(all_180)}")

# Check ID counts and types
shorts = [q for q in new_questions if q["type"] == "short"]
descs = [q for q in new_questions if q["type"] == "descriptive"]
pracs = [q for q in new_questions if q["type"] == "practical"]
print(f"New breakdown: Short={len(shorts)}, Desc={len(descs)}, Prac={len(pracs)}")
assert len(shorts) == 25, f"Short count {len(shorts)} != 25"
assert len(descs) == 10, f"Desc count {len(descs)} != 10"
assert len(pracs) == 5, f"Prac count {len(pracs)} != 5"
assert len(new_questions) == 40, f"Total new questions {len(new_questions)} != 40"

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
    sys.exit(1)
print(">> Schema / Score / Concept Check: PASS")

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
    sys.exit(1)
print(">> All 40 questions PDF Grounding Check: PASS")

# 3. De-duplication Check across all 180 questions
print(f"\n3. Verifying De-duplication across all 180 questions...")
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

high_sim = []
for i, q1 in enumerate(all_180):
    t1 = get_tokens(q1)
    for j, q2 in enumerate(all_180):
        if j <= i:
            continue
        t2 = get_tokens(q2)
        sim = len(t1 & t2) / len(t1 | t2) if (t1 | t2) else 0
        if sim > 0.25:
            high_sim.append((sim, q1["id"], q2["id"], q1["category"], q2["category"]))

print(f"Overlaps > 0.25: {len(high_sim)}")
if high_sim:
    for s, id1, id2, c1, c2 in sorted(high_sim, reverse=True):
        print(f"  ISSUE: {s:.3f} between {id1} and {id2}")
    sys.exit(1)
print(">> De-duplication Check (threshold 0.25): PASS (Zero duplicates)")

# 4. Source Registry 12-Source Full Activation Check
print(f"\n4. Verifying All 12 PDF Sources Activation...")
source_counts = {}
for q in all_180:
    sid = q["source_id"]
    source_counts[sid] = source_counts.get(sid, 0) + 1

inactive_sources = []
for s in sources:
    sid = s["id"]
    cnt = source_counts.get(sid, 0)
    print(f"  {sid} ({s['filename']}): {cnt} questions")
    if cnt == 0:
        inactive_sources.append(sid)

if inactive_sources:
    print(f"ERROR: Inactive sources remaining: {inactive_sources}")
    sys.exit(1)
print(">> All 12 PDF Sources Active: PASS (100% Activation)")

print("\n==================================================")
print("=== ALL BATCH 3 QA GATES PASSED SUCCESSFULLY! ===")
print("==================================================")
