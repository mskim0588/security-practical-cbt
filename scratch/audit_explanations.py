# -*- coding: utf-8 -*-
"""
Deep audit script for 180 question explanations in explanations.json.
Compares Question, Answer, Rubric, and Explanation across Short, Descriptive, and Practical.
"""
import os
import json
import re
from collections import Counter

BASE_DIR = r"C:\Users\mskim0588\Desktop\security-practical-cbt"
QUESTIONS_FILE = os.path.join(BASE_DIR, "app", "data", "questions.json")
EXPLANATIONS_FILE = os.path.join(BASE_DIR, "app", "data", "explanations.json")
SOURCES_FILE = os.path.join(BASE_DIR, "app", "data", "sources.json")
CONCEPTS_FILE = os.path.join(BASE_DIR, "app", "data", "concepts.json")

def audit_explanations():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = json.load(f)
    q_map = {q["id"]: q for q in questions}

    with open(EXPLANATIONS_FILE, "r", encoding="utf-8") as f:
        explanations = json.load(f)

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)
    source_map = {s["id"]: s for s in sources}

    with open(CONCEPTS_FILE, "r", encoding="utf-8") as f:
        concepts = json.load(f)
    concept_map = {c["id"]: c for c in concepts}

    findings = []
    
    # 1. Total counts & Coverage
    print(f"Total Questions in bank: {len(questions)}")
    print(f"Total Explanations in explanations.json: {len(explanations)}")

    missing_in_exp = [qid for qid in q_map if qid not in explanations]
    extra_in_exp = [qid for qid in explanations if qid not in q_map]
    if missing_in_exp:
        findings.append({"level": "P0", "type": "coverage", "qid": missing_in_exp, "issue": "Questions missing explanation"})
    if extra_in_exp:
        findings.append({"level": "P1", "type": "coverage", "qid": extra_in_exp, "issue": "Explanations with no question in bank"})

    # 2. Boilerplate / Generic phrase detection
    overview_texts = []
    strategy_texts = []
    why_correct_texts = []

    for qid, exp in explanations.items():
        q = q_map.get(qid)
        if not q:
            continue
        
        qtype = q["type"]
        overview = exp.get("overview", "").strip()
        why_correct = exp.get("why_correct", "").strip()
        strategy = exp.get("exam_strategy", "").strip()
        traps = exp.get("why_wrong_common_traps", [])
        scoring = exp.get("practical_scoring_criteria")

        overview_texts.append(overview)
        strategy_texts.append(strategy)
        why_correct_texts.append(why_correct)

        # Overview check
        if not overview or len(overview) < 10:
            findings.append({"level": "P1", "type": "overview", "qid": qid, "issue": "Overview empty or too short"})

        # Why correct check
        if not why_correct or len(why_correct) < 15:
            findings.append({"level": "P1", "type": "why_correct", "qid": qid, "issue": "Why_correct empty or too short"})

        # Rubric alignment for Descriptive and Practical
        if qtype in ("descriptive", "practical"):
            if not scoring:
                findings.append({"level": "P1", "type": "rubric", "qid": qid, "issue": f"{qtype} question lacks practical_scoring_criteria"})
            else:
                max_sc = scoring.get("max_score")
                expected_max = q.get("score", 12 if qtype == "descriptive" else 16)
                if max_sc != expected_max:
                    findings.append({"level": "P1", "type": "rubric", "qid": qid, "issue": f"Rubric max_score {max_sc} != question score {expected_max}"})
                rubrics = scoring.get("rubrics", [])
                if not rubrics:
                    findings.append({"level": "P1", "type": "rubric", "qid": qid, "issue": "Rubrics list empty"})
                else:
                    rubric_sum = sum(r.get("points", 0) for r in rubrics)
                    if rubric_sum != expected_max:
                        findings.append({"level": "P1", "type": "rubric", "qid": qid, "issue": f"Rubric points sum {rubric_sum} != expected {expected_max}"})

        # Short answer alignment: check strict mode questions
        if qtype == "short":
            grading_mode = q.get("grading_mode", "normalized")
            subs = q.get("sub_questions") or []
            if not subs:
                # single short answer
                ans = q.get("answer")
                if ans and ans.lower() not in why_correct.lower() and ans not in why_correct:
                    findings.append({"level": "P1", "type": "short_answer", "qid": qid, "issue": f"Expected answer '{ans}' not mentioned in why_correct"})
            else:
                for sub in subs:
                    sub_ans = sub.get("answer")
                    if sub_ans and len(sub_ans) > 1 and sub_ans.lower() not in why_correct.lower():
                        # Minor check
                        pass

        # Traps check
        if not traps:
            findings.append({"level": "P2", "type": "traps", "qid": qid, "issue": "No traps defined"})

        # Source Grounding check
        sid = q.get("source_id")
        spage = q.get("source_page")
        if not sid or sid not in source_map:
            findings.append({"level": "P1", "type": "source", "qid": qid, "issue": f"Invalid or missing source_id: {sid}"})
        elif spage is not None:
            max_p = source_map[sid].get("total_pages", 9999)
            if spage > max_p or spage < 1:
                findings.append({"level": "P1", "type": "source", "qid": qid, "issue": f"Source page {spage} out of range (1~{max_p}) for {sid}"})

        # Concept alignment check
        cid = q.get("concept_id")
        if not cid or cid not in concept_map:
            findings.append({"level": "P1", "type": "concept", "qid": qid, "issue": f"Invalid concept_id: {cid}"})
        else:
            # Check category match between question and concept
            qcat = q.get("category")
            ccat = concept_map[cid].get("category")
            if qcat != ccat:
                findings.append({"level": "P1", "type": "concept_cat", "qid": qid, "issue": f"Question category '{qcat}' != Concept category '{ccat}'"})

    # Boilerplate check: most common sentences
    print("\n--- Repetition & Boilerplate Check ---")
    strat_counter = Counter(strategy_texts)
    print("Most common exam strategies:")
    for s, c in strat_counter.most_common(5):
        print(f"  [{c} times] {s[:60]}...")

    print(f"\nTotal findings from automated check: {len(findings)}")
    by_level = Counter(f["level"] for f in findings)
    print(f"Findings by level: {dict(by_level)}")
    for f in findings:
        print(f"[{f['level']}] ({f['type']}) QID={f.get('qid')}: {f['issue']}")

    return findings

if __name__ == "__main__":
    audit_explanations()
