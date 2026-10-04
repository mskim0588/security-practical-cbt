import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = os.path.join(os.environ.get("PRIVATE_SOURCE_DIR", ""), "00. 정보보안기사_실기_요약_v1.0.pdf")
reader = pypdf.PdfReader(pdf_path)

with open("batch1_src5_dump.txt", "w", encoding="utf-8") as out:
    for p in range(1, 15):
        if p <= len(reader.pages):
            out.write(f"\n=== SRC-05 Page {p} ===\n")
            out.write(reader.pages[p - 1].extract_text() or "")
            out.write("\n")

print("Dumped SRC-05 pages 1-14")
