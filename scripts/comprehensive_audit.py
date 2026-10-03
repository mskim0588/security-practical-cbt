import json
import os
import pypdf
import re

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

# Lazy PDF reader
pdf_readers = {}
def get_reader(sid):
    if sid not in pdf_readers:
        fname = source_map[sid]["filename"]
        fpath = os.path.join(PDF_DIR, fname)
        pdf_readers[sid] = pypdf.PdfReader(fpath)
    return pdf_readers[sid]

page_cache = {}
def get_page(sid, page_num):
    key = (sid, page_num)
    if key not in page_cache:
        reader = get_reader(sid)
        if 1 <= page_num <= len(reader.pages):
            page_cache[key] = reader.pages[page_num - 1].extract_text() or ""
        else:
            page_cache[key] = ""
    return page_cache[key]

audit_records = []

for q in questions:
    qid = q["id"]
    qtype = q["type"]
    sid = q["source_id"]
    spage = q["source_page"]
    cid = q["concept_id"]
    cat = q["category"]
    gmode = q.get("grading_mode")
    
    rec = {
        "id": qid,
        "type": qtype,
        "question": q["question"],
        "source_id": sid,
        "source_filename": source_map.get(sid, {}).get("filename", "UNKNOWN"),
        "source_page": spage,
        "concept_id": cid,
        "category": cat,
        "grading_mode": gmode,
        "verdict": "PASS",
        "issues": [],
        "notes": "",
        "pdf_match_summary": ""
    }

    # 1. Source existence
    if sid not in source_map:
        rec["issues"].append(f"Source ID '{sid}' not in sources.json")
        rec["verdict"] = "FAIL"
        audit_records.append(rec)
        continue

    fname = source_map[sid]["filename"]
    fpath = os.path.join(PDF_DIR, fname)
    if not os.path.exists(fpath):
        rec["issues"].append(f"PDF file '{fname}' not found in PDF directory")
        rec["verdict"] = "FAIL"
        audit_records.append(rec)
        continue

    reader = get_reader(sid)
    total_pages = len(reader.pages)
    if spage < 1 or spage > total_pages:
        rec["issues"].append(f"Page {spage} out of range (1..{total_pages})")
        rec["verdict"] = "FAIL"
        audit_records.append(rec)
        continue

    # 2. Extract page text
    p_cur = get_page(sid, spage)
    p_prev = get_page(sid, spage - 1) if spage > 1 else ""
    p_next = get_page(sid, spage + 1) if spage < total_pages else ""

    # Clean whitespace for search
    cur_clean = re.sub(r'\s+', '', p_cur)
    prev_clean = re.sub(r'\s+', '', p_prev)
    next_clean = re.sub(r'\s+', '', p_next)
    adj_clean = prev_clean + cur_clean + next_clean

    # Determine core keywords to verify
    check_terms = []
    if qtype == "short":
        if q.get("sub_questions"):
            for sub in q["sub_questions"]:
                ans = str(sub.get("answer", "")).strip()
                if ans: check_terms.append(ans)
                for a in sub.get("accepted_answers", []):
                    check_terms.append(str(a).strip())
        else:
            ans = str(q.get("answer", "")).strip()
            if ans: check_terms.append(ans)
            for a in q.get("accepted_answers", []):
                check_terms.append(str(a).strip())
    elif qtype in ("descriptive", "practical"):
        for sub in q.get("sub_questions", []):
            rub = sub.get("rubric", {})
            for kw in rub.get("keywords", []):
                kw_clean = str(kw).strip()
                if kw_clean: check_terms.append(kw_clean)
        # Also check model_answer keywords
        for sub in q.get("sub_questions", []):
            ma = sub.get("model_answer", "")
            # extract key terms
            words = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', ma) if len(w) >= 2]
            check_terms.extend(words[:6])

    # Check keyword presence
    matched_exact = []
    matched_adj = []
    missing = []

    for t in check_terms:
        t_clean = re.sub(r'\s+', '', t).lower()
        if not t_clean: continue
        if t_clean in cur_clean.lower():
            matched_exact.append(t)
        elif t_clean in adj_clean.lower():
            matched_adj.append(t)
        else:
            missing.append(t)

    rec["matched_exact_count"] = len(set(matched_exact))
    rec["matched_adj_count"] = len(set(matched_adj))
    rec["missing_count"] = len(set(missing))
    rec["total_checked"] = len(set(check_terms))

    # Evaluate match quality
    if rec["matched_exact_count"] == 0 and rec["matched_adj_count"] == 0:
        rec["issues"].append(f"핵심 키워드가 {spage}페이지 및 인접 페이지에서 직접 확인되지 않음 (수동 검토 필요)")
        rec["verdict"] = "WARNING"
    elif rec["matched_exact_count"] == 0 and rec["matched_adj_count"] > 0:
        rec["issues"].append(f"핵심 키워드가 {spage}페이지가 아닌 인접 페이지(전후 1페이지)에서 주로 확인됨")
        rec["verdict"] = "WARNING"

    # Rubric / Sub-score validation
    if qtype == "short":
        if q.get("sub_questions"):
            s_sum = sum(s.get("score", 0) for s in q["sub_questions"])
            if abs(s_sum - 3.0) > 0.01:
                rec["issues"].append(f"소문항 배점 합계 오류 ({s_sum} != 3.0)")
                rec["verdict"] = "FAIL"
    elif qtype == "descriptive":
        if q.get("score") != 12:
            rec["issues"].append(f"서술형 총점 오류 ({q.get('score')} != 12)")
            rec["verdict"] = "FAIL"
        s_sum = sum(s.get("score", 0) for s in q.get("sub_questions", []))
        if abs(s_sum - 12.0) > 0.01:
            rec["issues"].append(f"서술형 소문항 배점 합계 오류 ({s_sum} != 12.0)")
            rec["verdict"] = "FAIL"
    elif qtype == "practical":
        if q.get("score") != 16:
            rec["issues"].append(f"실무형 총점 오류 ({q.get('score')} != 16)")
            rec["verdict"] = "FAIL"
        s_sum = sum(s.get("score", 0) for s in q.get("sub_questions", []))
        if abs(s_sum - 16.0) > 0.01:
            rec["issues"].append(f"실무형 소문항 배점 합계 오류 ({s_sum} != 16.0)")
            rec["verdict"] = "FAIL"

    # Category / Concept validation
    ALLOWED_CATS = {"시스템 보안", "네트워크 보안", "애플리케이션 보안", "정보보안 일반 및 암호학", "정보보호 관리 및 법규"}
    if cat not in ALLOWED_CATS:
        rec["issues"].append(f"표준 5대 카테고리 불일치: {cat}")
        rec["verdict"] = "FAIL"
    if cid not in concept_map:
        rec["issues"].append(f"미등록 Concept ID: {cid}")
        rec["verdict"] = "FAIL"

    audit_records.append(rec)

# Check duplicates
duplicate_pairs = []
for i in range(len(questions)):
    for j in range(i + 1, len(questions)):
        q1 = questions[i]
        q2 = questions[j]
        # same type and concept
        if q1["type"] == q2["type"] and q1["concept_id"] == q2["concept_id"]:
            s1 = set(re.findall(r'[가-힣a-zA-Z0-9]+', q1["question"]))
            s2 = set(re.findall(r'[가-힣a-zA-Z0-9]+', q2["question"]))
            jac = len(s1 & s2) / max(len(s1 | s2), 1)
            if jac > 0.35:
                duplicate_pairs.append({
                    "q1": q1["id"],
                    "q2": q2["id"],
                    "jaccard": round(jac, 2),
                    "concept": q1["concept_id"],
                    "reason": f"동일 Concept({q1['concept_id']}) 및 유사 질문 지문 (유사도 {jac:.2f})"
                })

with open("audit_summary_temp.json", "w", encoding="utf-8") as f:
    json.dump({
        "records": audit_records,
        "duplicates": duplicate_pairs
    }, f, ensure_ascii=False, indent=2)

print("Comprehensive audit finished.")
print("PASS:", sum(1 for r in audit_records if r["verdict"] == "PASS"))
print("WARNING:", sum(1 for r in audit_records if r["verdict"] == "WARNING"))
print("FAIL:", sum(1 for r in audit_records if r["verdict"] == "FAIL"))
print("Duplicates found:", len(duplicate_pairs))
