# -*- coding: utf-8 -*-
import os
import sys
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data")
with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)

src5 = [s for s in sources if s["id"] == "SRC-05"][0]
pdf_path = os.path.join(r"G:\내 드라이브\보안기사\보안기사 실기 관련자료", src5["filename"])

reader = pypdf.PdfReader(pdf_path)

for pnum in [8, 9, 10, 11, 12, 13]:
    txt = reader.pages[pnum - 1].extract_text() or ""
    print(f"=== SRC-05 Page {pnum} ===")
    lines = [line.strip() for line in txt.splitlines() if line.strip()]
    for l in lines[:15]:
        print("  ", l)
