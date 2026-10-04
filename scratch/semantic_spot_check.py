import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/data/questions.json', 'r', encoding='utf-8') as f:
    qs = {q['id']: q for q in json.load(f)}

with open('app/data/explanations.json', 'r', encoding='utf-8') as f:
    exps = json.load(f)

print("=== SAMPLE PRACTICAL AUDIT ===")
for qid in ["Q-PRAC-001", "Q-PRAC-004", "Q-PRAC-009", "Q-PRAC-014", "Q-PRAC-018", "Q-PRAC-020", "Q-PRAC-021"]:
    exp = exps[qid]
    q = qs[qid]
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    print(f"\n[{qid}] {stem[:45]}...")
    psc = exp.get("practical_scoring_criteria", {})
    print(f"  Max score: {psc.get('max_score')}, Rubrics count: {len(psc.get('rubrics', []))}")
    for r in psc.get("rubrics", []):
        print(f"    - +{r['points']}점: {r['criteria'][:50]} | kws: {r['required_keywords']}")
    print(f"  Traps ({len(exp.get('why_wrong_common_traps', []))}):")
    for t in exp.get("why_wrong_common_traps", []):
        print(f"    * {t['confused_term_or_misunderstanding']}")

print("\n=== SAMPLE DESCRIPTIVE AUDIT ===")
for qid in ["Q-DESC-001", "Q-DESC-004", "Q-DESC-010", "Q-DESC-020", "Q-DESC-035"]:
    exp = exps[qid]
    q = qs[qid]
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    print(f"\n[{qid}] {stem[:45]}...")
    psc = exp.get("practical_scoring_criteria", {})
    print(f"  Max score: {psc.get('max_score')}, Rubrics count: {len(psc.get('rubrics', []))}")
    for r in psc.get("rubrics", []):
        print(f"    - +{r['points']}점: {r['criteria'][:50]} | kws: {r['required_keywords']}")
    print(f"  Traps ({len(exp.get('why_wrong_common_traps', []))}):")
    for t in exp.get("why_wrong_common_traps", []):
        print(f"    * {t['confused_term_or_misunderstanding']}")

print("\n=== SAMPLE SHORT AUDIT ===")
for qid in ["Q-SHORT-003", "Q-SHORT-005", "Q-SHORT-008", "Q-SHORT-041", "Q-SHORT-058", "Q-SHORT-084"]:
    exp = exps[qid]
    q = qs[qid]
    stem = (q.get('stem') or q.get('question') or '').replace('\n', ' ')
    print(f"\n[{qid}] {q.get('answer')} | {stem[:45]}...")
    print(f"  why_correct: {exp.get('why_correct')[:100]}...")
    for t in exp.get("why_wrong_common_traps", []):
        print(f"    * {t['confused_term_or_misunderstanding']}")
