import json
import os
import pypdf
import re

PDF_DIR = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = {s["id"]: s for s in json.load(f)}

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

# Open readers
readers = {}
for sid, s in sources.items():
    fpath = os.path.join(PDF_DIR, s["filename"])
    if os.path.exists(fpath):
        readers[sid] = pypdf.PdfReader(fpath)

output_lines = []

for q in questions:
    qid = q["id"]
    qtype = q["type"]
    sid = q["source_id"]
    spage = q["source_page"]
    cid = q["concept_id"]
    cat = q["category"]
    gmode = q.get("grading_mode", "N/A")
    
    reader = readers.get(sid)
    page_text = ""
    if reader and 1 <= spage <= len(reader.pages):
        page_text = reader.pages[spage - 1].extract_text() or ""
    
    clean_pdf = re.sub(r'\s+', ' ', page_text).strip()
    
    output_lines.append(f"==================================================")
    output_lines.append(f"[{qid}] Type: {qtype} | Cat: {cat} | Concept: {cid} | Mode: {gmode}")
    output_lines.append(f"Source: {sid} ({sources[sid]['filename']}) Page: {spage} (Total: {len(reader.pages)})")
    output_lines.append(f"Question: {q['question']}")
    
    if qtype == "short":
        if q.get("sub_questions"):
            for sub in q["sub_questions"]:
                output_lines.append(f"  Sub ({sub['label']}) [Score: {sub['score']}]: Answer: {sub.get('answer')} | Accepted: {sub.get('accepted_answers')}")
        else:
            output_lines.append(f"  Answer: {q.get('answer')} | Accepted: {q.get('accepted_answers')} | Score: {q.get('score')}")
    else:
        for sub in q.get("sub_questions", []):
            output_lines.append(f"  Sub {sub.get('sub_id')} [Score: {sub.get('score')}]:")
            output_lines.append(f"    Model Ans: {sub.get('model_answer')}")
            rub = sub.get("rubric", {})
            output_lines.append(f"    Rubric Keywords: {rub.get('keywords')} (min_match: {rub.get('min_keywords_to_full_score', 'N/A')})")
    
    output_lines.append(f"\n--- PDF Text Excerpt (Page {spage}) ---")
    output_lines.append(clean_pdf[:500] if len(clean_pdf) > 500 else clean_pdf)
    output_lines.append("\n")

with open("audit_full_dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Dumped audit details for all {len(questions)} questions to audit_full_dump.txt")
