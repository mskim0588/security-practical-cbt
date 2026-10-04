import pypdf
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

def print_page(fn, p):
    reader = pypdf.PdfReader(os.path.join(pdf_dir, fn))
    print(f"\n=== {fn} Page {p} ===")
    print(reader.pages[p-1].extract_text()[:600])

print_page("00. 정보보안기사_실기_요약_v1.0.pdf", 9)
print_page("00. 정보보안기사_실기_요약_v1.0.pdf", 10)
print_page("00. 정보보안기사_실기_요약_v1.0.pdf", 11)
print_page("5과목.pdf", 30)
