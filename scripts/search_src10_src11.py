# -*- coding: utf-8 -*-
import os
import sys
import json
import re
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
sources = json.load(open('app/data/sources.json', encoding='utf-8'))
source_map = {s['id']: s for s in sources}
PDF_DIR = os.environ.get("PRIVATE_SOURCE_DIR", "")
r11 = pypdf.PdfReader(os.path.join(PDF_DIR, source_map['SRC-11']['filename']))

print("=== 고유식별정보 in SRC-11 ===")
for i, page in enumerate(r11.pages):
    t = page.extract_text()
    if '고유식별정보' in t:
        lines = [l.strip() for l in t.splitlines() if '고유식별' in l or '주민등록' in l]
        print(f"p.{i+1}: {lines[:2]}")

print("\n=== 유출 통지/신고 in SRC-11 ===")
for i, page in enumerate(r11.pages):
    t = page.extract_text()
    if '유출' in t and ('통지' in t or '신고' in t):
        lines = [l.strip() for l in t.splitlines() if '유출' in l][:2]
        print(f"p.{i+1}: {lines}")

print("\n=== CCTV in SRC-11 ===")
for i, page in enumerate(r11.pages):
    t = page.extract_text()
    if '안내판' in t or 'cctv' in t.lower() or '영상정보처리기기' in t:
        lines = [l.strip() for l in t.splitlines() if '안내판' in l or 'cctv' in l.lower()][:2]
        print(f"p.{i+1}: {lines}")
