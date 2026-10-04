import json
import os
import pypdf
import re

PDF_DIR = os.environ.get("PRIVATE_SOURCE_DIR", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = {s["id"]: s for s in json.load(f)}

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

# Pre-extract all pages for the 3 exam files once
cached_pages = {}
for sid in ["SRC-01", "SRC-02", "SRC-03"]:
    fname = sources[sid]["filename"]
    fpath = os.path.join(PDF_DIR, fname)
    print(f"Reading {fname}...")
    reader = pypdf.PdfReader(fpath)
    pages = []
    for p in reader.pages:
        t = p.extract_text() or ""
        clean = re.sub(r'\s+', '', t).lower()
        pages.append(clean)
    cached_pages[sid] = pages
    print(f"Loaded {len(pages)} pages for {sid}")

page_mismatches = []

for q in questions:
    qid = q["id"]
    sid = q["source_id"]
    spage = q["source_page"]
    pages = cached_pages[sid]
    total_p = len(pages)
    
    # search key
    keywords = []
    if q["type"] == "short":
        if q.get("sub_questions"):
            for s in q["sub_questions"]:
                ans = str(s["answer"]).strip()
                if len(ans) >= 2:
                    keywords.append(ans)
        else:
            ans = str(q["answer"]).strip()
            if len(ans) >= 2:
                keywords.append(ans)
    else:
        for s in q.get("sub_questions", []):
            rub = s.get("rubric", {})
            for k in rub.get("keywords", []):
                k_str = str(k).strip()
                if len(k_str) >= 2:
                    keywords.append(k_str)

    page_scores = {}
    for p_idx, p_clean in enumerate(pages):
        score = sum(1 for kw in keywords if re.sub(r'\s+', '', kw).lower() in p_clean)
        if score > 0:
            page_scores[p_idx + 1] = score

    best_page = max(page_scores.keys(), key=lambda p: page_scores[p]) if page_scores else None
    cur_score = page_scores.get(spage, 0)

    if best_page and best_page != spage and cur_score == 0:
        page_mismatches.append({
            "id": qid,
            "type": q["type"],
            "source_id": sid,
            "filename": sources[sid]["filename"],
            "current_page": spage,
            "best_page": best_page,
            "current_score": cur_score,
            "best_score": page_scores[best_page],
            "total_keywords": len(keywords),
            "severity": "FAIL" if abs(best_page - spage) > 2 else "WARNING"
        })
    elif best_page and best_page != spage and cur_score > 0 and page_scores[best_page] > cur_score * 2:
        page_mismatches.append({
            "id": qid,
            "type": q["type"],
            "source_id": sid,
            "filename": sources[sid]["filename"],
            "current_page": spage,
            "best_page": best_page,
            "current_score": cur_score,
            "best_score": page_scores[best_page],
            "total_keywords": len(keywords),
            "severity": "WARNING"
        })

print(f"\nTotal Page Mismatches/Offset findings: {len(page_mismatches)}")
for m in page_mismatches:
    print(f"[{m['severity']}] {m['id']} ({m['source_id']} {m['filename']}): 현재 {m['current_page']}p -> 추천 {m['best_page']}p (현재매칭:{m['current_score']} vs 추천매칭:{m['best_score']})")

with open("page_mismatches.json", "w", encoding="utf-8") as f:
    json.dump(page_mismatches, f, ensure_ascii=False, indent=2)
