import os
import sys
import json
import re
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.batch1_draft_builder import BATCH1_SHORT, BATCH1_DESC, BATCH1_PRAC

PDF_DIR = os.environ.get("PRIVATE_SOURCE_DIR", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)
source_map = {s["id"]: s for s in sources}

with open(os.path.join(DATA_DIR, "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)
concept_map = {c["id"]: c for c in concepts}

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    existing_questions = json.load(f)
existing_ids = set(q["id"] for q in existing_questions)

new_questions = BATCH1_SHORT + BATCH1_DESC + BATCH1_PRAC

print(f"=== BATCH 1 QA GATE VALIDATION ===")
print(f"Existing questions: {len(existing_questions)}")
print(f"New questions to validate: {len(new_questions)}")

# 1. Schema, Score, Category, Concept Check
errors = []
ALLOWED_CATS = {"시스템 보안", "네트워크 보안", "애플리케이션 보안", "정보보안 일반 및 암호학", "정보보호 관리 및 법규"}

for q in new_questions:
    qid = q["id"]
    if qid in existing_ids:
        errors.append(f"Duplicate ID with existing: {qid}")
    
    cat = q["category"]
    if cat not in ALLOWED_CATS:
        errors.append(f"Invalid category in {qid}: {cat}")
        
    cid = q["concept_id"]
    if cid not in concept_map:
        errors.append(f"Unregistered concept_id in {qid}: {cid}")
        
    sid = q["source_id"]
    if sid not in source_map:
        errors.append(f"Unregistered source_id in {qid}: {sid}")
    else:
        max_p = source_map[sid]["total_pages"]
        spage = q["source_page"]
        if spage < 1 or spage > max_p:
            errors.append(f"Invalid page {spage} for {sid} (max {max_p}) in {qid}")
            
    qtype = q["type"]
    score = q["score"]
    if qtype == "short":
        if score != 3: errors.append(f"Short score {score} != 3 in {qid}")
        if not q.get("answer"): errors.append(f"Missing answer in {qid}")
        if q.get("grading_mode") not in ("normalized", "strict"):
            errors.append(f"Invalid grading_mode in {qid}: {q.get('grading_mode')}")
    elif qtype == "descriptive":
        if score != 12: errors.append(f"Desc score {score} != 12 in {qid}")
        s_sum = sum(s["score"] for s in q.get("sub_questions", []))
        if s_sum != 12: errors.append(f"Desc sub_questions sum {s_sum} != 12 in {qid}")
    elif qtype == "practical":
        if score != 16: errors.append(f"Prac score {score} != 16 in {qid}")
        s_sum = sum(s["score"] for s in q.get("sub_questions", []))
        if s_sum != 16: errors.append(f"Prac sub_questions sum {s_sum} != 16 in {qid}")

print(f"1. Schema, Score, Category, Concept Errors: {len(errors)}")
if errors:
    for e in errors: print("  ERROR:", e)

# 2. PDF Grounding Check
pdf_readers = {}
def get_reader(sid):
    if sid not in pdf_readers:
        fname = source_map[sid]["filename"]
        pdf_readers[sid] = pypdf.PdfReader(os.path.join(PDF_DIR, fname))
    return pdf_readers[sid]

grounding_issues = []
print("\n2. Verifying PDF Page Grounding for 36 questions...")
for q in new_questions:
    qid = q["id"]
    sid = q["source_id"]
    spage = q["source_page"]
    reader = get_reader(sid)
    page_text = reader.pages[spage - 1].extract_text() or ""
    page_clean = re.sub(r'\s+', '', page_text).lower()
    
    # Check tokens
    check_tokens = []
    if q["type"] == "short":
        check_tokens.append(q["answer"])
        check_tokens.extend(q.get("accepted_answers", []))
        for a in [q["answer"]] + q.get("accepted_answers", []):
            if "," in str(a):
                check_tokens.extend([part.strip() for part in str(a).split(",") if part.strip()])
    else:
        for s in q.get("sub_questions", []):
            check_tokens.append(s.get("prompt", ""))
            ma = s.get("model_answer", "")
            words = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', ma) if len(w) >= 2]
            check_tokens.extend(words[:5])
            
    matched = [t for t in set(check_tokens) if re.sub(r'\s+', '', str(t)).lower() in page_clean]
    if len(matched) == 0:
        grounding_issues.append((qid, sid, spage, "0 tokens matched on page"))
    else:
        print(f"  [{qid}] {sid} p.{spage} -> Matched tokens ({len(matched)}): {list(matched)[:4]}")

print(f"Grounding Issues: {len(grounding_issues)}")
if grounding_issues:
    for g in grounding_issues: print("  ISSUE:", g)

# 3. De-duplication Check against All (Existing 64 + New 36)
print("\n3. Verifying De-duplication across all 100 questions...")
all_pool = existing_questions + new_questions

def get_tokens(q):
    t = q["question"] + " "
    if q.get("answer"): t += str(q["answer"]) + " "
    for s in (q.get("sub_questions") or []):
        t += str(s.get("prompt", "")) + " "
        t += str(s.get("model_answer", "")) + " "
    tokens = set(re.findall(r'[가-힣]{2,}|[a-zA-Z0-9_\-\.]{3,}', t.lower()))
    stopwords = {"설명하시오", "기술하시오", "무엇인가", "대하여", "대해", "다음은", "관련하여", "위한", "있는", "하는", "경우", "각각"}
    return tokens - stopwords

tokens_list = [get_tokens(q) for q in all_pool]
duplicates = []

for i in range(len(all_pool)):
    for j in range(i + 1, len(all_pool)):
        s1 = tokens_list[i]
        s2 = tokens_list[j]
        inter = s1 & s2
        union = s1 | s2
        sim = len(inter) / max(len(union), 1)
        if sim > 0.20:
            duplicates.append((sim, all_pool[i]["id"], all_pool[j]["id"], list(inter)[:8]))

print(f"Duplicates found (Threshold > 0.20): {len(duplicates)}")
if duplicates:
    for sim, q1, q2, inter in duplicates:
        print(f"  SIMILARITY {sim:.2f}: {q1} vs {q2} | Shared: {inter}")

if not errors and not grounding_issues and not duplicates:
    print("\n>>> ALL QA GATE CHECKS PASSED PERFECTLY! (0 Errors, 0 Issues, 0 Duplicates) <<<")
