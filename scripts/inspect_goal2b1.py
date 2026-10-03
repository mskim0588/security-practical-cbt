import json
import sys

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

with open('app/data/questions.json', encoding='utf-8') as f:
    qs = json.load(f)
with open('app/data/concepts.json', encoding='utf-8') as f:
    cs = json.load(f)

ALLOWED_CATEGORIES = [
    "시스템 보안",
    "네트워크 보안",
    "애플리케이션 보안",
    "정보보안 일반 및 암호학",
    "정보보호 관리 및 법규"
]

print("=== Standard Categories (5개) ===")
for cat in ALLOWED_CATEGORIES:
    print(f"  * {cat}")

print("\n=== Questions Categories Audit ===")
for q in qs:
    cat = q.get('category')
    is_valid = cat in ALLOWED_CATEGORIES
    mark = "OK" if is_valid else "INVALID"
    print(f"[{mark:7s}] {q['id']:11s} : {cat}")

print("\n=== Concepts Categories Audit ===")
for c in cs:
    cat = c.get('category')
    is_valid = cat in ALLOWED_CATEGORIES
    mark = "OK" if is_valid else "INVALID"
    print(f"[{mark:7s}] {c['id']:11s} : {cat}")

print("\n=== Short Questions grading_mode Audit ===")
for q in qs:
    if q.get('type') == 'short':
        gm = q.get('grading_mode')
        ans = q.get('answer') or [sq.get('answer') for sq in q.get('sub_questions', [])]
        print(f"{q['id']:11s} : mode={gm} | ans={ans}")
