import json
import os
import pypdf
from typing import Dict, List, Any

PDF_DIR = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)

with open(os.path.join(DATA_DIR, "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

source_map = {s["id"]: s for s in sources}
concept_map = {c["id"]: c for c in concepts}

# Check file existence for all sources
file_exists_map = {}
for s in sources:
    sid = s["id"]
    fname = s["filename"]
    fpath = os.path.join(PDF_DIR, fname)
    exists = os.path.exists(fpath)
    file_exists_map[sid] = exists
    if not exists:
        print(f"MISSING FILE: {fpath}")

print(f"Verified all 12 source files existence: {all(file_exists_map.values())}")

# Lazy PDF reader cache
pdf_readers = {}
def get_reader(sid):
    if sid not in pdf_readers:
        fname = source_map[sid]["filename"]
        fpath = os.path.join(PDF_DIR, fname)
        print(f"Opening reader for {sid}: {fname}...")
        pdf_readers[sid] = pypdf.PdfReader(fpath)
    return pdf_readers[sid]

page_text_cache = {}
def get_page_text(sid, page_idx):
    key = (sid, page_idx)
    if key not in page_text_cache:
        reader = get_reader(sid)
        if 0 <= page_idx < len(reader.pages):
            try:
                t = reader.pages[page_idx].extract_text() or ""
                page_text_cache[key] = t
            except Exception as e:
                page_text_cache[key] = ""
        else:
            page_text_cache[key] = ""
    return page_text_cache[key]

results = []

for idx, q in enumerate(questions, start=1):
    qid = q["id"]
    qtype = q["type"]
    sid = q["source_id"]
    spage = q["source_page"]
    cid = q["concept_id"]
    cat = q["category"]
    
    audit_item = {
        "id": qid,
        "type": qtype,
        "question": q["question"],
        "source_id": sid,
        "source_page": spage,
        "concept_id": cid,
        "category": cat,
        "findings": [],
        "verdict": "PASS"
    }

    # 1. Source and File Check
    if sid not in source_map:
        audit_item["findings"].append(f"FAIL: Source ID {sid} not in sources.json")
        audit_item["verdict"] = "FAIL"
    elif not file_exists_map.get(sid, False):
        audit_item["findings"].append(f"FAIL: PDF file for {sid} not accessible on disk")
        audit_item["verdict"] = "FAIL"
    else:
        reader = get_reader(sid)
        total_p = len(reader.pages)
        if spage < 1 or spage > total_p:
            audit_item["findings"].append(f"FAIL: Page {spage} out of range (1..{total_p})")
            audit_item["verdict"] = "FAIL"
        else:
            page_text = get_page_text(sid, spage - 1)
            prev_page_text = get_page_text(sid, spage - 2) if spage > 1 else ""
            next_page_text = get_page_text(sid, spage) if spage < total_p else ""

            audit_item["page_len"] = len(page_text)
            audit_item["page_snippet"] = page_text[:250].replace("\n", " ")

            # Collect terms to check
            answers_to_check = []
            if qtype == "short":
                if q.get("sub_questions"):
                    for sub in q["sub_questions"]:
                        ans = str(sub.get("answer", "")).strip()
                        if ans: answers_to_check.append(ans)
                        for acc in sub.get("accepted_answers", []):
                            acc_str = str(acc).strip()
                            if acc_str: answers_to_check.append(acc_str)
                else:
                    ans = str(q.get("answer", "")).strip()
                    if ans: answers_to_check.append(ans)
                    for acc in q.get("accepted_answers", []):
                        acc_str = str(acc).strip()
                        if acc_str: answers_to_check.append(acc_str)
            elif qtype in ("descriptive", "practical"):
                for sub in q.get("sub_questions", []):
                    rub = sub.get("rubric", {})
                    for kw in rub.get("keywords", []):
                        kw_str = str(kw).strip()
                        if kw_str and len(kw_str) > 1:
                            answers_to_check.append(kw_str)

            # verify presence of key terms (case insensitive)
            found_terms = [t for t in answers_to_check if t and t.lower() in page_text.lower()]
            found_in_adj = [t for t in answers_to_check if t and (t.lower() in prev_page_text.lower() or t.lower() in next_page_text.lower()) and t.lower() not in page_text.lower()]

            audit_item["found_terms_exact_page"] = list(set(found_terms))
            audit_item["found_terms_adjacent_page"] = list(set(found_in_adj))
            audit_item["total_terms_checked"] = len(set(answers_to_check))

            if not found_terms and not found_in_adj:
                audit_item["findings"].append(f"WARNING: Key terms not directly found in page {spage} or +-1 pages")
                if audit_item["verdict"] == "PASS":
                    audit_item["verdict"] = "WARNING"
            elif not found_terms and found_in_adj:
                audit_item["findings"].append(f"WARNING: Key terms found on adjacent page instead of page {spage}")
                if audit_item["verdict"] == "PASS":
                    audit_item["verdict"] = "WARNING"

    # 2. Rubric / Score checks
    if qtype == "short":
        if q.get("score") != 3:
            audit_item["findings"].append(f"FAIL: Short question score is {q.get('score')} != 3")
            audit_item["verdict"] = "FAIL"
        if q.get("sub_questions"):
            sub_sum = sum(s.get("score", 0) for s in q["sub_questions"])
            if abs(sub_sum - 3.0) > 0.01:
                audit_item["findings"].append(f"FAIL: Short sub-scores sum {sub_sum} != 3.0")
                audit_item["verdict"] = "FAIL"
    elif qtype == "descriptive":
        if q.get("score") != 12:
            audit_item["findings"].append(f"FAIL: Desc question score is {q.get('score')} != 12")
            audit_item["verdict"] = "FAIL"
        sub_sum = sum(s.get("score", 0) for s in q.get("sub_questions", []))
        if abs(sub_sum - 12.0) > 0.01:
            audit_item["findings"].append(f"FAIL: Desc sub-scores sum {sub_sum} != 12.0")
            audit_item["verdict"] = "FAIL"
    elif qtype == "practical":
        if q.get("score") != 16:
            audit_item["findings"].append(f"FAIL: Practical question score is {q.get('score')} != 16")
            audit_item["verdict"] = "FAIL"
        sub_sum = sum(s.get("score", 0) for s in q.get("sub_questions", []))
        if abs(sub_sum - 16.0) > 0.01:
            audit_item["findings"].append(f"FAIL: Practical sub-scores sum {sub_sum} != 16.0")
            audit_item["verdict"] = "FAIL"

    # 3. Concept and Category
    if cid not in concept_map:
        audit_item["findings"].append(f"FAIL: concept_id {cid} not in concepts.json")
        audit_item["verdict"] = "FAIL"
    
    ALLOWED_CATS = {"시스템 보안", "네트워크 보안", "애플리케이션 보안", "정보보안 일반 및 암호학", "정보보호 관리 및 법규"}
    if cat not in ALLOWED_CATS:
        audit_item["findings"].append(f"FAIL: category '{cat}' not in standard 5 categories")
        audit_item["verdict"] = "FAIL"

    results.append(audit_item)

# 4. Duplicate checks
duplicates = []
for i in range(len(questions)):
    for j in range(i + 1, len(questions)):
        q1 = questions[i]
        q2 = questions[j]
        # same concept and type
        if q1["concept_id"] == q2["concept_id"] and q1["type"] == q2["type"]:
            s1 = set(q1["question"].replace("\n", " ").split())
            s2 = set(q2["question"].replace("\n", " ").split())
            jaccard = len(s1 & s2) / max(len(s1 | s2), 1)
            if jaccard > 0.35:
                duplicates.append({
                    "q1": q1["id"],
                    "q2": q2["id"],
                    "jaccard": round(jaccard, 2),
                    "concept": q1["concept_id"]
                })

print(f"\n--- AUDIT SUMMARY ---")
pass_count = sum(1 for r in results if r["verdict"] == "PASS")
warn_count = sum(1 for r in results if r["verdict"] == "WARNING")
fail_count = sum(1 for r in results if r["verdict"] == "FAIL")
print(f"Total: {len(results)}, PASS: {pass_count}, WARNING: {warn_count}, FAIL: {fail_count}")

with open("reports_audit_raw.json", "w", encoding="utf-8") as f:
    json.dump({"results": results, "duplicates": duplicates}, f, ensure_ascii=False, indent=2)
print("Saved reports_audit_raw.json")
