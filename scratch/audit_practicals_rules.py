# -*- coding: utf-8 -*-
"""
Script to audit technical syntax and rules of the 24 Practical Questions.
"""
import os
import json
import re

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
QUESTIONS_FILE = os.path.join(BASE_DIR, "app", "data", "questions.json")
EXPLANATIONS_FILE = os.path.join(BASE_DIR, "app", "data", "explanations.json")

def audit_practicals_deep():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    practicals = [q for q in questions if q["type"] == "practical"]

    with open(EXPLANATIONS_FILE, "r", encoding="utf-8") as f:
        explanations = json.load(f)

    report_lines = []

    for idx, q in enumerate(practicals, 1):
        qid = q["id"]
        exp = explanations.get(qid, {})
        cid = q.get("concept_id")
        cat = q.get("category")
        q_text = q.get("question", "")
        model_ans = q.get("model_answer", "")
        subs = q.get("sub_questions") or []
        rubric_data = exp.get("practical_scoring_criteria", {})

        report_lines.append(f"### [{idx:02d}/24] {qid} (배점: {q.get('score')}점)")
        report_lines.append(f"- **분야/개념**: {cat} / `{cid}`")
        report_lines.append(f"- **출처**: `{q.get('source_id')}` (Page {q.get('source_page')})")
        report_lines.append(f"- **문제 개요**: {q_text[:120].strip()}...")
        report_lines.append(f"- **소문항 수**: {len(subs)}개")
        for s in subs:
            report_lines.append(f"  - 소문항 {s.get('sub_id')} ({s.get('score')}점): {s.get('prompt')}")
            report_lines.append(f"    - 필수 키워드: `{s.get('keywords')}`")
        report_lines.append(f"- **모범 답안 스니펫**:\n```\n{model_ans[:250].strip()}...\n```")
        
        # Technical analysis
        tech_findings = []
        full_text = f"{q_text}\n{model_ans}\n{exp.get('why_correct', '')}\n{' '.join(exp.get('related_commands', []))}"
        
        # 1. IPTables check
        if "iptables" in full_text.lower():
            # Check chains
            if "input" in full_text.lower() or "forward" in full_text.lower() or "output" in full_text.lower():
                pass
            # Check options: -A, -p, -s, -d, --dport, -j ACCEPT/DROP
            invalid_opt = re.findall(r'iptables\s+[^-][^\s]+', full_text)
            if invalid_opt:
                tech_findings.append(f"Potential invalid iptables syntax: {invalid_opt}")

        # 2. Snort check
        if "snort" in full_text.lower() or "alert " in full_text:
            # Check Snort rule header direction
            if "<-" in full_text:
                tech_findings.append("Snort rule direction '<-' found (invalid syntax)")
            # Check sid and rev
            if "sid:" in full_text and "rev:" not in full_text:
                tech_findings.append("Snort rule has sid but missing rev option")

        # 3. Path check
        paths = re.findall(r'(/[a-zA-Z0-9_\-\.]+/[a-zA-Z0-9_\-\.]+)', full_text)
        for p in paths:
            # common linux paths
            if not any(p.startswith(prefix) for prefix in ['/etc', '/var', '/usr', '/bin', '/sbin', '/proc', '/dev', '/sys', '/tmp', '/root', '/home']):
                # non-standard path
                pass

        # 4. Rubric alignment
        rubrics = rubric_data.get("rubrics", [])
        total_rubric_pts = sum(r.get("points", 0) for r in rubrics)
        if total_rubric_pts != q.get("score"):
            tech_findings.append(f"Rubric point sum ({total_rubric_pts}) != Question score ({q.get('score')})")

        # 5. Trap quality check
        traps = exp.get("why_wrong_common_traps", [])
        if not traps:
            tech_findings.append("No traps defined in explanation")

        # Evaluation verdict
        verdict = "PASS" if not tech_findings else "FLAGGED"
        report_lines.append(f"- **기술적 감사 결과**: `{verdict}`")
        if tech_findings:
            for tf in tech_findings:
                report_lines.append(f"  - ⚠️ {tf}")
        report_lines.append("")

    with open("scratch/practical_audit_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Generated {len(report_lines)} lines to scratch/practical_audit_report.md")

if __name__ == "__main__":
    audit_practicals_deep()
