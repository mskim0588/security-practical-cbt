# -*- coding: utf-8 -*-
import os
import json
import pypdf

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data")
with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)

src5 = [s for s in sources if s["id"] == "SRC-05"][0]
pdf_path = os.path.join(r"G:\내 드라이브\보안기사\보안기사 실기 관련자료", src5["filename"])

print(f"Reading {pdf_path} (pages: {src5['total_pages']})...")
reader = pypdf.PdfReader(pdf_path)

matches = []
for idx, page in enumerate(reader.pages):
    txt = (page.extract_text() or "").lower()
    if "pam" in txt or "auth" in txt and "account" in txt:
        matches.append((idx + 1, txt[:100].replace('\n', ' ')))

print(f"Found PAM in pages: {[m[0] for m in matches[:15]]}")
for pnum, snippet in matches[:5]:
    print(f"Page {pnum}: {snippet}")
