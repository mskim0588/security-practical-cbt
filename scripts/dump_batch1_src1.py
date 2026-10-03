import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료\보안기사 실기 단답형.pdf"
reader = pypdf.PdfReader(pdf_path)

with open("batch1_src1_dump.txt", "w", encoding="utf-8") as out:
    for p in range(24, 40):
        if p <= len(reader.pages):
            out.write(f"\n=== SRC-01 Page {p} ===\n")
            out.write(reader.pages[p - 1].extract_text() or "")
            out.write("\n")

print("Dumped SRC-01 pages 24-39")
