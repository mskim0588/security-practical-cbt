# -*- coding: utf-8 -*-
"""
Deep Comprehensive Audit Script for 180 Questions (Goal 2E)
Analyzes:
1. Schema, Score, and Subquestion Integrity
2. Category and Concept Mapping
3. PDF Grounding across source_page and adjacent pages (p-1, p, p+1)
4. Short Question Answer Scope, Accepted Answers, and Grading Mode
5. Descriptive Rubrics, Keywords, and Scoring Balance
6. Practical Questions Technical Syntax and Consistency
7. Semantic Duplication Candidates (Jaccard > 0.20, Shared Core Terms)
8. Source Distribution and Page Over-concentration
9. Law / Management Freshness Candidates
"""
import os
import sys
import json
import re
import pypdf

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PDF_DIR = os.environ.get("PRIVATE_SOURCE_DIR", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "data")

with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(os.path.join(DATA_DIR, "sources.json"), "r", encoding="utf-8") as f:
    sources = json.load(f)
source_map = {s["id"]: s for s in sources}

with open(os.path.join(DATA_DIR, "concepts.json"), "r", encoding="utf-8") as f:
    concepts = json.load(f)
concept_map = {c["id"]: c for c in concepts}

print(f"Loaded {len(questions)} questions from questions.json")

# PDF Readers cache
pdf_readers = {}
def get_pdf_page_text(sid, page_num):
    if sid not in pdf_readers:
        fn = source_map[sid]["filename"]
        fpath = os.path.join(PDF_DIR, fn)
        if not os.path.exists(fpath):
            return ""
        pdf_readers[sid] = pypdf.PdfReader(fpath)
    reader = pdf_readers[sid]
    if 1 <= page_num <= len(reader.pages):
        return reader.pages[page_num - 1].extract_text() or ""
    return ""

findings = []

# Audit Rule 1: Schema, Score, Category, Concept
print("\n--- Auditing 1: Schema, Score, Category, Concept ---")
ALLOWED_CATS = {
    "시스템 보안": ["CON-SYS-01", "CON-SYS-02", "CON-SYS-03"],
    "네트워크 보안": ["CON-NET-01", "CON-NET-02", "CON-NET-03", "CON-NET-04"],
    "애플리케이션 보안": ["CON-APP-01", "CON-APP-02", "CON-APP-03", "CON-APP-04"],
    "정보보안 일반 및 암호학": ["CON-SEC-01", "CON-SEC-02", "CON-CRY-01", "CON-CRY-02", "CON-CRY-03"],
    "정보보호 관리 및 법규": ["CON-MGT-01", "CON-MGT-02", "CON-MGT-03", "CON-MGT-04", "CON-LAW-01", "CON-LAW-02"]
}
cat_for_concept = {}
for cat, cids in ALLOWED_CATS.items():
    for cid in cids:
        cat_for_concept[cid] = cat

for q in questions:
    qid = q["id"]
    qtype = q.get("type")
    score = q.get("score")
    cat = q.get("category")
    cid = q.get("concept_id")
    sid = q.get("source_id")
    spage = q.get("source_page", 0)

    # Category validity
    if cat not in ALLOWED_CATS:
        findings.append({
            "id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0",
            "issue": f"Invalid category '{cat}'"
        })
    # Concept validity
    if cid not in concept_map:
        findings.append({
            "id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0",
            "issue": f"Unregistered concept_id '{cid}'"
        })
    elif cat_for_concept.get(cid) != cat:
        # Cross-category concept warning
        findings.append({
            "id": qid, "type": qtype, "verdict": "WARNING", "priority": "P1",
            "issue": f"Category mismatch: concept {cid} normally belongs to '{cat_for_concept.get(cid)}', but question is categorized as '{cat}'"
        })

    # Score checks
    if qtype == "short":
        if score != 3:
            findings.append({"id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0", "issue": f"Short score {score} != 3"})
    elif qtype == "descriptive":
        if score != 12:
            findings.append({"id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0", "issue": f"Desc score {score} != 12"})
        subs = q.get("sub_questions", [])
        if sum(s.get("score", 0) for s in subs) != 12:
            findings.append({"id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0", "issue": f"Desc sub_questions sum != 12"})
    elif qtype == "practical":
        if score != 16:
            findings.append({"id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0", "issue": f"Prac score {score} != 16"})
        subs = q.get("sub_questions", [])
        if sum(s.get("score", 0) for s in subs) != 16:
            findings.append({"id": qid, "type": qtype, "verdict": "FAIL", "priority": "P0", "issue": f"Prac sub_questions sum != 16"})

print("Schema audit completed.")

# Audit Rule 2: PDF Grounding Check (page & adjacent pages)
print("\n--- Auditing 2: PDF Grounding (Target & Adjacent Pages) ---")
pdf_grounding_results = {}
for q in questions:
    qid = q["id"]
    sid = q.get("source_id")
    spage = q.get("source_page", 0)
    
    if sid not in source_map:
        findings.append({"id": qid, "type": q["type"], "verdict": "FAIL", "priority": "P0", "issue": f"Invalid source_id {sid}"})
        continue
    max_p = source_map[sid]["total_pages"]
    if spage < 1 or spage > max_p:
        findings.append({"id": qid, "type": q["type"], "verdict": "FAIL", "priority": "P0", "issue": f"Invalid page {spage} for {sid} (max {max_p})"})
        continue

    # Extract text from page and neighbors
    cur_text = get_pdf_page_text(sid, spage)
    prev_text = get_pdf_page_text(sid, spage - 1) if spage > 1 else ""
    next_text = get_pdf_page_text(sid, spage + 1) if spage < max_p else ""

    combined_text = (cur_text + " " + prev_text + " " + next_text).lower()
    clean_cur = re.sub(r'\s+', '', cur_text).lower()
    clean_combined = re.sub(r'\s+', '', combined_text).lower()

    # Collect check tokens
    check_tokens = []
    if q.get("answer"):
        check_tokens.append(q["answer"])
        words_ans = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', str(q["answer"])) if len(w) >= 2]
        check_tokens.extend(words_ans)
        for a in q.get("accepted_answers", []):
            check_tokens.append(a)
            words_a = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', str(a)) if len(w) >= 2]
            check_tokens.extend(words_a)
    if q.get("question"):
        words_q = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', str(q["question"])) if len(w) >= 3]
        check_tokens.extend(words_q[:5])
    for s in (q.get("sub_questions") or []):
        if s.get("answer"):
            check_tokens.append(s["answer"])
        for a in s.get("accepted_answers", []):
            check_tokens.append(a)
        for g in s.get("rubric", {}).get("keywords", []):
            if isinstance(g, list):
                check_tokens.extend(g)
            else:
                check_tokens.append(g)
        ma = s.get("model_answer", "")
        words = [w for w in re.findall(r'[a-zA-Z0-9_\-\./]+|[가-힣]{2,}', ma) if len(w) >= 2]
        check_tokens.extend(words[:5])

    # Distinct tokens
    tokens_clean = [re.sub(r'\s+', '', str(t)).lower() for t in set(check_tokens) if len(str(t).strip()) >= 2]
    cur_matches = [t for t in tokens_clean if t in clean_cur]
    neighbor_matches = [t for t in tokens_clean if t in clean_combined]

    pdf_grounding_results[qid] = {
        "cur_matches": cur_matches,
        "neighbor_matches": neighbor_matches,
        "sid": sid,
        "spage": spage
    }

    if not cur_matches:
        if neighbor_matches:
            findings.append({
                "id": qid, "type": q["type"], "verdict": "WARNING", "priority": "P1",
                "issue": f"Exact target page {sid} p.{spage} has 0 matching tokens, but adjacent page has {len(neighbor_matches)} matches. Consider page adjustment."
            })
        else:
            findings.append({
                "id": qid, "type": q["type"], "verdict": "FAIL", "priority": "P0",
                "issue": f"No token matches found on {sid} p.{spage} or its adjacent pages."
            })

print("PDF Grounding audit completed.")

# Audit Rule 3: Short Questions Analysis (Strict vs Normalized, Answer Scope)
print("\n--- Auditing 3: Short Questions Analysis ---")
for q in [q for q in questions if q["type"] == "short"]:
    qid = q["id"]
    mode = q.get("grading_mode", "normalized")

    if q.get("sub_questions"):
        # Multi-blank short question
        for sub in q["sub_questions"]:
            lbl = sub.get("label", "?")
            s_ans = str(sub.get("answer", "")).strip()
            s_accepted = [str(a).strip() for a in sub.get("accepted_answers", [])]
            if not s_ans:
                findings.append({"id": qid, "type": "short", "verdict": "FAIL", "priority": "P0", "issue": f"Blank ({lbl}) missing answer in multi-blank short question"})
            if s_ans not in s_accepted and s_ans.lower() not in [a.lower() for a in s_accepted]:
                findings.append({
                    "id": qid, "type": "short", "verdict": "WARNING", "priority": "P1",
                    "issue": f"Blank ({lbl}) answer '{s_ans}' not explicitly in accepted_answers {s_accepted}"
                })
    else:
        # Single-blank short question
        ans = str(q.get("answer", "")).strip()
        accepted = [str(a).strip() for a in q.get("accepted_answers", [])]

        # Check answer presence
        if not ans:
            findings.append({"id": qid, "type": "short", "verdict": "FAIL", "priority": "P0", "issue": "Missing answer in single-blank short question"})

        # Check accepted_answers includes answer
        if ans not in accepted and ans.lower() not in [a.lower() for a in accepted]:
            findings.append({
                "id": qid, "type": "short", "verdict": "WARNING", "priority": "P1",
                "issue": f"Primary answer '{ans}' not explicitly in accepted_answers {accepted}"
            })

        # Check strict appropriateness
        if mode == "strict":
            if re.search(r'^[가-힣\s]+$', ans):
                findings.append({
                    "id": qid, "type": "short", "verdict": "WARNING", "priority": "P1",
                    "issue": f"Strict grading_mode applied to pure Korean term '{ans}'. Consider if normalized is more appropriate."
                })

        # Check if accepted_answers is too sparse (only 1 entry and has obvious English/Korean equivalent)
        if len(accepted) <= 1:
            if re.search(r'^[a-zA-Z0-9_\-\.]+$', ans) and len(ans) > 3:
                # English term without Korean representation or vice versa
                pass

        # Check for overbroad accepted answers
        OVERBROAD_STOPWORDS = {"보안", "취약점", "공격", "시스템", "네트워크", "파일", "인증", "관리", "데이터", "서버"}
        for a in accepted:
            if a.strip() in OVERBROAD_STOPWORDS:
                findings.append({
                    "id": qid, "type": "short", "verdict": "WARNING", "priority": "P1",
                    "issue": f"Overbroad accepted answer '{a}' may allow false positives"
                })

print("Short questions audit completed.")

# Audit Rule 4: Descriptive Questions Rubric & Scoring
print("\n--- Auditing 4: Descriptive Questions Analysis ---")
for q in [q for q in questions if q["type"] == "descriptive"]:
    qid = q["id"]
    subs = q.get("sub_questions") or []
    if not subs:
        findings.append({"id": qid, "type": "descriptive", "verdict": "FAIL", "priority": "P0", "issue": "No sub_questions defined"})
        continue

    for s in subs:
        sid = s.get("sub_id")
        rub = s.get("rubric", {})
        kws = rub.get("keywords", [])
        if not kws:
            findings.append({
                "id": qid, "type": "descriptive", "verdict": "WARNING", "priority": "P1",
                "issue": f"Subquestion {sid} rubric has empty keywords"
            })
        for group in kws:
            if not isinstance(group, list):
                findings.append({
                    "id": qid, "type": "descriptive", "verdict": "FAIL", "priority": "P0",
                    "issue": f"Subquestion {sid} rubric keyword group is not a list: {group}"
                })
            elif len(group) == 0:
                findings.append({
                    "id": qid, "type": "descriptive", "verdict": "WARNING", "priority": "P1",
                    "issue": f"Subquestion {sid} has an empty keyword group list"
                })

        # Check scoring logic
        all_pts = rub.get("all_match_points")
        part_pts = rub.get("partial_match_points")
        sub_score = s.get("score")
        if all_pts != sub_score:
            findings.append({
                "id": qid, "type": "descriptive", "verdict": "WARNING", "priority": "P1",
                "issue": f"Subquestion {sid} all_match_points ({all_pts}) != sub_score ({sub_score})"
            })

print("Descriptive questions audit completed.")

# Audit Rule 5: Practical Questions Technical Validity & Commands
print("\n--- Auditing 5: Practical Questions Technical Analysis ---")
for q in [q for q in questions if q["type"] == "practical"]:
    qid = q["id"]
    text = q.get("question", "")
    subs = q.get("sub_questions") or []
    
    # Check that practical question has rich technical data (log, config, command, prompt, table, form)
    technical_markers = [
        "#", "$", "log", "conf", "iptables", "rule", "snort", "access-list",
        "find", "cat", "chmod", "rpm", "named", "httpd", "select", "where",
        "alert", "tcpdump", "xinetd", "allow", "deny", "http", "post", "|", "양식", "신청서"
    ]
    has_tech = any(m in text.lower() for m in technical_markers)
    if not has_tech:
        findings.append({
            "id": qid, "type": "practical", "verdict": "WARNING", "priority": "P1",
            "issue": "Practical question lacks visible log/command/rule/configuration artifact in question text"
        })

    for s in subs:
        sid = s.get("sub_id")
        prompt = s.get("prompt", "")
        ma = s.get("model_answer", "")
        rub = s.get("rubric", {})
        kws = rub.get("keywords", [])

        if not prompt:
            findings.append({"id": qid, "type": "practical", "verdict": "FAIL", "priority": "P0", "issue": f"Subquestion {sid} missing prompt"})
        if not ma:
            findings.append({"id": qid, "type": "practical", "verdict": "FAIL", "priority": "P0", "issue": f"Subquestion {sid} missing model_answer"})
        if not kws:
            findings.append({"id": qid, "type": "practical", "verdict": "WARNING", "priority": "P1", "issue": f"Subquestion {sid} missing rubric keywords"})

        # Check for command validity in model_answer
        # If prompt asks for a command, check if command syntax has obvious syntax issues
        if "명령어" in prompt or "명령" in prompt or "설정" in prompt:
            if "iptables" in ma and not any(f in ma for f in ["-A", "-I", "-D", "-P"]):
                findings.append({
                    "id": qid, "type": "practical", "verdict": "WARNING", "priority": "P2",
                    "issue": f"Subquestion {sid} iptables command in model_answer may lack chain operation flag (-A, -I, -P)"
                })

print("Practical questions audit completed.")

# Audit Rule 6: Semantic Duplication Check
print("\n--- Auditing 6: Semantic Duplication Check ---")
def get_tokens(q):
    t = q["question"] + " "
    if q.get("answer"):
        t += str(q["answer"]) + " "
    for a in q.get("accepted_answers", []):
        t += str(a) + " "
    for s in (q.get("sub_questions") or []):
        t += str(s.get("prompt", "")) + " "
        t += str(s.get("model_answer", "")) + " "
    tokens = set(re.findall(r'[가-힣]{2,}|[a-zA-Z0-9_\-\.]{3,}', t.lower()))
    stopwords = {"설명하시오", "기술하시오", "무엇인가", "대하여", "대해", "다음은", "관련하여", "위한", "있는", "하는", "경우", "각각", "보안", "기사", "실기"}
    return tokens - stopwords

duplicate_candidates = []
for i, q1 in enumerate(questions):
    t1 = get_tokens(q1)
    for j, q2 in enumerate(questions):
        if j <= i:
            continue
        t2 = get_tokens(q2)
        sim = len(t1 & t2) / len(t1 | t2) if (t1 | t2) else 0
        
        # Check high similarity or shared exact core answers
        core_ans_match = False
        if q1.get("answer") and q2.get("answer"):
            if str(q1["answer"]).strip().lower() == str(q2["answer"]).strip().lower():
                core_ans_match = True

        if sim > 0.22 or core_ans_match:
            duplicate_candidates.append({
                "q1_id": q1["id"],
                "q2_id": q2["id"],
                "q1_type": q1["type"],
                "q2_type": q2["type"],
                "similarity": round(sim, 3),
                "core_ans_match": core_ans_match,
                "q1_source": f"{q1['source_id']} p.{q1['source_page']}",
                "q2_source": f"{q2['source_id']} p.{q2['source_page']}",
                "q1_concept": q1.get("concept_id"),
                "q2_concept": q2.get("concept_id"),
                "shared_tokens": list(t1 & t2)[:8]
            })

print(f"Potential semantic duplicate candidates (sim > 0.22 or exact core answer): {len(duplicate_candidates)}")
for d in duplicate_candidates:
    print(f"  [{d['q1_id']} vs {d['q2_id']}] sim={d['similarity']}, core_match={d['core_ans_match']}, shared={d['shared_tokens'][:4]}")

# Audit Rule 7: Source Page Concentration Check
print("\n--- Auditing 7: Source Distribution & Page Concentration ---")
page_counts = {}
for q in questions:
    key = (q["source_id"], q["source_page"])
    page_counts.setdefault(key, []).append(q["id"])

over_concentrated = {k: v for k, v in page_counts.items() if len(v) >= 3}
print(f"Pages with >= 3 questions: {len(over_concentrated)}")
for (sid, spage), qlist in over_concentrated.items():
    print(f"  {sid} p.{spage}: {len(qlist)} questions -> {qlist}")
    findings.append({
        "id": ", ".join(qlist),
        "type": "multiple",
        "verdict": "WARNING",
        "priority": "P2",
        "issue": f"{sid} p.{spage} has {len(qlist)} derived questions ({', '.join(qlist)}). Check for over-concentration."
    })

# Audit Rule 8: Law / Management Freshness Check
print("\n--- Auditing 8: Law and Management Freshness ---")
law_mgt_questions = [q for q in questions if q.get("category") == "정보보호 관리 및 법규"]
print(f"Total Law/Management questions: {len(law_mgt_questions)}")
law_terms = ["개인정보", "보호법", "정보통신망법", "망법", "기반보호법", "과징금", "과태료", "보호최고책임자", "ciso", "cpo", "유출", "통지", "신고", "isms", "isms-p"]
for q in law_mgt_questions:
    qid = q["id"]
    full_text = q["question"] + " " + str(q.get("answer", "")) + " " + str(q.get("model_answer", ""))
    matched_law_terms = [t for t in law_terms if t in full_text.lower()]
    if any(t in full_text.lower() for t in ["과징금", "통지", "신고", "ciso"]):
        findings.append({
            "id": qid, "type": q["type"], "verdict": "WARNING", "priority": "P2",
            "issue": f"Contains legal criteria/period/officer requirements ({matched_law_terms[:3]}). Verify alignment with PDF baseline vs latest statutory revisions."
        })

print("\n--- AUDIT SUMMARY ---")
fails = [f for f in findings if f.get("verdict") == "FAIL"]
warns = [f for f in findings if f.get("verdict") == "WARNING"]
print(f"Total Findings: {len(findings)}")
print(f"FAIL (P0): {len(fails)}")
print(f"WARNING (P1/P2): {len(warns)}")

# Save raw findings JSON for report generator
with open("scripts/audit_findings_raw.json", "w", encoding="utf-8") as f:
    json.dump({
        "findings": findings,
        "duplicate_candidates": duplicate_candidates,
        "over_concentrated": {f"{k[0]}_p{k[1]}": v for k, v in over_concentrated.items()},
        "total_questions": len(questions)
    }, f, ensure_ascii=False, indent=2)

print("Saved audit_findings_raw.json.")
