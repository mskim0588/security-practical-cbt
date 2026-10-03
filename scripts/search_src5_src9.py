import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"

def search_text(fn, keywords):
    fp = os.path.join(pdf_dir, fn)
    reader = pypdf.PdfReader(fp)
    print(f"\n=== Searching {fn} ({len(reader.pages)} pages) ===")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        matched = [kw for kw in keywords if kw.lower() in text.lower()]
        if matched:
            print(f"  Page {i+1}: matched {matched}")

search_text("00. 정보보안기사_실기_요약_v1.0.pdf", ["cron", "PAM", "btmp", "버퍼", "xinetd"])
search_text("5과목.pdf", ["대칭키", "비대칭키", "공개키"])
