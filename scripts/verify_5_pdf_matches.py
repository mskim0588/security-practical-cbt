import os
import pypdf

pdf_dir = os.environ.get("PRIVATE_SOURCE_DIR", "")

def verify_item(pdf_name, page_num, expected_tokens):
    fp = os.path.join(pdf_dir, pdf_name)
    reader = pypdf.PdfReader(fp)
    text = reader.pages[page_num - 1].extract_text() or ""
    missing = [token for token in expected_tokens if token.lower() not in text.lower()]
    found = [token for token in expected_tokens if token.lower() in text.lower()]
    print(f"[{pdf_name} p.{page_num}]")
    print(f"  Found ({len(found)}): {found}")
    if missing:
        print(f"  MISSING ({len(missing)}): {missing}")
    else:
        print("  ALL TOKENS MATCHED! PASS")

print("--- 1. Q-PRAC-002: SRC-03 p.5 ---")
verify_item("정보보안기사 실기 서술형 TOP 20.pdf", 5, ["Snort", "Rule", "Header", "액션", "프로토콜"])

print("\n--- 2. Q-PRAC-006: SRC-03 p.6 ---")
verify_item("정보보안기사 실기 서술형 TOP 20.pdf", 6, ["HTTP GET Flooding", "depth", "threshold", "count 100", "seconds 1"])

print("\n--- 3. Q-SHORT-036: SRC-01 p.21 ---")
verify_item("보안기사 실기 단답형.pdf", 21, ["DDoS", "C&C", "도메인명", "DGA", "Domain Generation Algorithm"])

print("\n--- 4. Q-DESC-005: SRC-02 p.13 ---")
verify_item("보안기사 실기 서술형.pdf", 13, ["침입탐지", "오용 탐지", "이상 탐지", "오탐률"])

print("\n--- 5. Q-PRAC-003: SRC-02 p.41 ---")
verify_item("보안기사 실기 서술형.pdf", 41, ["백업 스크립트", "tar", "umask", "operator"])
