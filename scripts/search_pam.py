# -*- coding: utf-8 -*-
import os, sys, json, pypdf
sys.stdout.reconfigure(encoding='utf-8')
src5 = json.load(open("app/data/sources.json", encoding="utf-8"))[4]
reader = pypdf.PdfReader(os.path.join(r"G:\내 드라이브\보안기사\보안기사 실기 관련자료", src5["filename"]))
for idx, page in enumerate(reader.pages):
    txt = page.extract_text() or ""
    if "pam" in txt.lower():
        print(f"Page {idx+1} mentions PAM:")
        for line in txt.splitlines():
            if "pam" in line.lower() or "auth" in line.lower():
                print("   ", line.strip())
