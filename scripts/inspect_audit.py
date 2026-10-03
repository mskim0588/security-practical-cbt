import json

with open("reports_audit_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total results: {len(data['results'])}")
warns = [r for r in data["results"] if r["verdict"] == "WARNING"]
print(f"Total warnings: {len(warns)}\n")

for w in warns:
    print(f"[{w['id']}] ({w['type']}) {w['source_id']} Page {w['source_page']} - {w['concept_id']}")
    print(f"  Findings: {w['findings']}")
    print(f"  Exact terms found: {w['found_terms_exact_page']}")
    print(f"  Adj terms found: {w['found_terms_adjacent_page']}")
    print(f"  Snippet: {w['page_snippet'][:150]}...")
    print("-" * 60)

print("\n--- DUPLICATE CANDIDATES ---")
for d in data.get("duplicates", []):
    print(f"{d['q1']} <-> {d['q2']} (Jaccard: {d['jaccard']}, Concept: {d['concept']})")
