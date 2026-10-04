import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

def search_practical_in_pdf(filename, name):
    fp = os.path.join(pdf_dir, filename)
    reader = pypdf.PdfReader(fp)
    print(f"\n=================== {name} ({len(reader.pages)} pages) ===================")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        # Check if text contains log, config, script, etc.
        keywords = ["설정", "분석", "로그", "conf", "config", "rule", "명령어", "실무"]
        matches = [kw for kw in keywords if kw in text]
        if len(matches) >= 3 or "실무" in text or "단답" in text or "기출" in text:
            first_few = [l.strip() for l in text.split("\n") if l.strip()][:2]
            print(f"Page {i+1}: {' / '.join(first_few)}")

if __name__ == "__main__":
    search_practical_in_pdf("보안기사 실기 서술형.pdf", "SRC-02")
