import os
import sys
import json
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

def inspect_src(filename, pages_to_check):
    fp = os.path.join(pdf_dir, filename)
    reader = pypdf.PdfReader(fp)
    res = {}
    for p in pages_to_check:
        if 1 <= p <= len(reader.pages):
            res[p] = reader.pages[p - 1].extract_text() or ""
    return res

src1_pages = inspect_src("보안기사 실기 단답형.pdf", [20, 21, 22, 23, 24, 25])
src2_pages = inspect_src("보안기사 실기 서술형.pdf", list(range(1, 18)))

with open("candidates_dump.json", "w", encoding="utf-8") as f:
    json.dump({"SRC-01": src1_pages, "SRC-02": src2_pages}, f, ensure_ascii=False, indent=2)

print("Dump complete. Pages written to candidates_dump.json")
