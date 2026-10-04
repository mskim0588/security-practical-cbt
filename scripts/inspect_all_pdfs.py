import os
import sys
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

with open("app/data/sources.json", "r", encoding="utf-8") as f:
    sources = json.load(f)

print(f"Total registered sources: {len(sources)}")

pdf_profiles = []
for s in sources:
    sid = s["id"]
    fn = s["filename"]
    fp = os.path.join(pdf_dir, fn)
    group = s.get("group", "theory")
    role = s.get("role", "")
    subject = s.get("subject", "")
    
    if not os.path.exists(fp):
        print(f"[{sid}] File not found: {fp}")
        continue
    
    reader = pypdf.PdfReader(fp)
    total_pages = len(reader.pages)
    
    # Extract preview text from first 3 pages and mid pages
    sample_text = ""
    for p_idx in range(min(5, total_pages)):
        sample_text += f"\n--- Page {p_idx+1} ---\n" + (reader.pages[p_idx].extract_text() or "")[:300]
    
    pdf_profiles.append({
        "id": sid,
        "filename": fn,
        "title": s["title"],
        "group": group,
        "role": role,
        "subject": subject,
        "total_pages": total_pages,
        "sample": sample_text[:1200]
    })
    print(f"[{sid}] {fn} | Group: {group} | Pages: {total_pages} | Subject: {subject}")

with open("pdf_profiles.json", "w", encoding="utf-8") as f:
    json.dump(pdf_profiles, f, ensure_ascii=False, indent=2)

print("\nWrote pdf_profiles.json successfully.")
