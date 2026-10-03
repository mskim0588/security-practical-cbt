import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open("pdf_profiles.json", "r", encoding="utf-8") as f:
    profiles = json.load(f)

for p in profiles:
    print(f"================================")
    print(f"[{p['id']}] {p['filename']} ({p['group']}, {p['total_pages']}p)")
    print(f"Subject: {p['subject']} | Role: {p['role']}")
    # print sample lines
    lines = [l.strip() for l in p['sample'].split('\n') if l.strip() and not l.startswith('---')][:6]
    print("Preview:\n  " + "\n  ".join(lines[:4]))
