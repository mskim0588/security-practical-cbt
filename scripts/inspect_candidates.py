import os
import pypdf

def dump_pages(pdf_path, name):
    print(f"=== {name} ===")
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        preview = lines[:3] if lines else ["EMPTY"]
        print(f"Page {i+1}: {preview}")

if __name__ == "__main__":
    dump_pages(os.path.join(os.environ.get("PRIVATE_SOURCE_DIR", ""), "보안기사 실기 단답형.pdf"), "SRC-01")
    dump_pages(os.path.join(os.environ.get("PRIVATE_SOURCE_DIR", ""), "보안기사 실기 서술형.pdf"), "SRC-02")
    dump_pages(os.path.join(os.environ.get("PRIVATE_SOURCE_DIR", ""), "정보보안기사 실기 서술형 TOP 20.pdf"), "SRC-03")
