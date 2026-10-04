# -*- coding: utf-8 -*-
"""
Detailed Technical Audit Script for all 24 Practical Questions (Q-PRAC-001 ~ Q-PRAC-024).
Examines:
- Question text, sub-questions, model answers, keywords, rubrics
- Technical accuracy of commands, syntax, paths, directives, options
- Explanations.json alignment
"""
import os
import json

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
QUESTIONS_FILE = os.path.join(BASE_DIR, "app", "data", "questions.json")
EXPLANATIONS_FILE = os.path.join(BASE_DIR, "app", "data", "explanations.json")

def audit_practicals():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    practicals = [q for q in questions if q["type"] == "practical"]

    with open(EXPLANATIONS_FILE, "r", encoding="utf-8") as f:
        explanations = json.load(f)

    print(f"Total Practical Questions: {len(practicals)}")

    results = []
    for idx, q in enumerate(practicals, 1):
        qid = q["id"]
        exp = explanations.get(qid, {})
        category = q.get("category", "")
        cid = q.get("concept_id", "")
        score = q.get("score", 16)
        sub_qs = q.get("sub_questions") or []
        model_ans = q.get("model_answer", "")
        q_text = q.get("question", "")
        source_id = q.get("source_id", "")
        source_page = q.get("source_page", 1)

        # Check rubric alignment
        exp_rubric = exp.get("practical_scoring_criteria", {})
        rubrics = exp_rubric.get("rubrics", [])
        rubric_sum = sum(r.get("points", 0) for r in rubrics)

        # Check related commands in exp
        rel_cmds = exp.get("related_commands", [])

        # Technical syntax scan
        tech_indicators = []
        for word in ["iptables", "snort", "tcpdump", "named", "bind", "httpd", "apache", "logrotate", "chmod", "chown", "setuid", "select", "union", "netstat", "lsof", "find", "modsecurity", "pam", "reg", "powershell"]:
            if word in q_text.lower() or word in model_ans.lower():
                tech_indicators.append(word)

        entry = {
            "index": idx,
            "qid": qid,
            "category": category,
            "concept_id": cid,
            "score": score,
            "sub_count": len(sub_qs),
            "source": f"{source_id} p.{source_page}",
            "tech": list(set(tech_indicators)),
            "rubric_sum": rubric_sum,
            "has_overview": bool(exp.get("overview")),
            "has_why_correct": bool(exp.get("why_correct")),
            "has_traps": len(exp.get("why_wrong_common_traps", [])) > 0,
            "related_cmds": rel_cmds
        }
        results.append(entry)

    with open("scratch/practical_audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Summary written to scratch/practical_audit_summary.json")

if __name__ == "__main__":
    audit_practicals()
