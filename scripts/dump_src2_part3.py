import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_path = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료\보안기사 실기 서술형.pdf"
reader = pypdf.PdfReader(pdf_path)

pages_to_check = [41, 46, 50, 58, 82, 86, 91, 102, 106]
with open("candidate_details_3.txt", "w", encoding="utf-8") as out:
    for p in pages_to_check:
        if p <= len(reader.pages):
            out.write(f"\n--- SRC-02 Page {p} ---\n")
            out.write(reader.pages[p - 1].extract_text() or "")
            out.write("\n")

print("Dumped selected pages to candidate_details_3.txt")
