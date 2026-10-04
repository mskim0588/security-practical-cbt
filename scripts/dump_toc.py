import os
import sys
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

def dump_toc(fn, sid, max_p=8):
    fp = os.path.join(pdf_dir, fn)
    reader = pypdf.PdfReader(fp)
    print(f"\n=== [{sid}] {fn} (Total: {len(reader.pages)}p) ===")
    for p in range(min(max_p, len(reader.pages))):
        t = reader.pages[p].extract_text() or ""
        lines = [l.strip() for l in t.split("\n") if l.strip()]
        if lines:
            print(f"  P.{p+1}: {' | '.join(lines[:3])}")

dump_toc("00. 정보보안기사_실기_요약_v1.0.pdf", "SRC-05", 5)
dump_toc("5과목.pdf", "SRC-09", 5)
dump_toc("6과목.pdf", "SRC-10", 5)
dump_toc("7과목.pdf", "SRC-11", 5)
dump_toc("정보보안기사 정리_260214.pdf", "SRC-12", 6)
