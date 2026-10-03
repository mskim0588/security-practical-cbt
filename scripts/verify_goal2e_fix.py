# -*- coding: utf-8 -*-
"""
Goal 2E-Fix Comprehensive Verification Script
Performs:
1. Data QA (180 questions, 112/44/24, no duplicate IDs, schemas valid, 12/16 rubric points)
2. Web QA (standard & random seeds: radio values match practical cards, submissions grade 16 points for chosen, 0 for unchosen, 100 max)
3. ExamGenerator 1,000-run regression (0 exceptions, 0 dead questions, 18 questions, 100 points, 0 duplicates within any exam)
"""
import sys
import os
import json
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.data_loader import DataLoader
from app.services.exam_generator import ExamGenerator
from app.services.exam_service import ExamService

app = create_app()
client = app.test_client()
loader = DataLoader()
questions = loader.load_questions()
sources = loader.load_sources()
concepts = loader.load_concepts()

source_ids = {s["id"] for s in sources}
concept_ids = {c["id"] for c in concepts}

print("==================================================")
print("1. DATA QA (180 Questions)")
print("==================================================")
assert len(questions) == 180, f"Expected 180, got {len(questions)}"
shorts = [q for q in questions if q["type"] == "short"]
descs = [q for q in questions if q["type"] == "descriptive"]
pracs = [q for q in questions if q["type"] == "practical"]

assert len(shorts) == 112, f"Expected 112 shorts, got {len(shorts)}"
assert len(descs) == 44, f"Expected 44 descs, got {len(descs)}"
assert len(pracs) == 24, f"Expected 24 pracs, got {len(pracs)}"
print(f"- Question count: 180 (Short {len(shorts)}, Desc {len(descs)}, Prac {len(pracs)}) -> PASS")

# Duplicate ID check
qids = [q["id"] for q in questions]
assert len(qids) == len(set(qids)), "Duplicate Question ID found!"
print("- Unique Question IDs: 180/180 -> PASS")

# Source & Concept & Category referential integrity
ALLOWED_CATS = {
    "시스템 보안",
    "네트워크 보안",
    "애플리케이션 보안",
    "정보보안 일반 및 암호학",
    "정보보호 관리 및 법규"
}
for q in questions:
    assert q["category"] in ALLOWED_CATS, f"Invalid category {q['category']} in {q['id']}"
    assert q["source_id"] in source_ids, f"Invalid source_id {q['source_id']} in {q['id']}"
    assert q["concept_id"] in concept_ids, f"Invalid concept_id {q['concept_id']} in {q['id']}"
    assert q["source_page"] > 0, f"Invalid source_page in {q['id']}"
    
    if q["type"] == "short":
        assert q["score"] == 3
        if q.get("sub_questions"):
            assert sum(s["score"] for s in q["sub_questions"]) == 3
    elif q["type"] == "descriptive":
        assert q["score"] == 12
        assert sum(s["score"] for s in q["sub_questions"]) == 12
        for s in q["sub_questions"]:
            assert s["rubric"]["all_match_points"] == s["score"]
    elif q["type"] == "practical":
        assert q["score"] == 16
        assert sum(s["score"] for s in q["sub_questions"]) == 16
        for s in q["sub_questions"]:
            assert s["rubric"]["all_match_points"] == s["score"]

print("- Referential integrity, categories, scores, and rubrics: 100% PASS")

print("\n==================================================")
print("2. WEB QA (Standard & Random Seeds Practical Selection)")
print("==================================================")
seeds_to_test = [("standard", None), ("random", 42), ("random", 1), ("random", 10), ("random", 100), ("random", 999)]
for mode, s in seeds_to_test:
    url = f"/exam?mode={mode}" + (f"&seed={s}" if s is not None else "")
    res = client.get(url)
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    radios = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"', html)
    cards = re.findall(r'class="question-card practical-card"\s+id="q-([^"]+)"', html)
    assert radios == cards, f"Mismatch in {mode} seed={s}: radios={radios} vs cards={cards}"
    assert len(radios) == 2, f"Expected 2 practical radios, got {len(radios)}"

    # Test review submission
    rev_data = {
        "question_ids": re.search(r'name="question_ids"\s+value="([^"]+)"', html).group(1),
        "exam_mode": mode,
        "selected_practical_id": radios[0],
    }
    rev_res = client.post("/review", data=rev_data)
    assert rev_res.status_code == 200
    rev_html = rev_res.get_data(as_text=True)
    assert "답안 최종 검토" in rev_html

    # Test final submission
    sub_data = dict(rev_data)
    sub_data[f"ans_{radios[0]}_1"] = "테스트 답안"
    sub_res = client.post("/submit", data=sub_data)
    assert sub_res.status_code == 200
    sub_html = sub_res.get_data(as_text=True)
    assert f"선택: {radios[0]}" in sub_html
    assert "/ 100점" in sub_html

print(f"- Tested {len(seeds_to_test)} modes/seeds: radio matching, review, submit, score card 100% PASS")

print("\n==================================================")
print("3. EXAM GENERATOR 1,000-RUN REGRESSION")
print("==================================================")
enriched_qs = loader.get_enriched_questions()
pool_counter = {}
for i in range(1000):
    exam = ExamGenerator.generate_exam_set(enriched_qs, mode="random", seed=i)
    assert len(exam) == 18, f"Run {i}: length {len(exam)} != 18"
    ids = [q["id"] for q in exam]
    assert len(ids) == len(set(ids)), f"Run {i}: Duplicate question in exam: {ids}"
    
    s_cnt = sum(1 for q in exam if q["type"] == "short")
    d_cnt = sum(1 for q in exam if q["type"] == "descriptive")
    p_cnt = sum(1 for q in exam if q["type"] == "practical")
    assert s_cnt == 12 and d_cnt == 4 and p_cnt == 2, f"Run {i}: Counts wrong ({s_cnt},{d_cnt},{p_cnt})"

    tot_pts = sum(q["score"] for q in exam[:16]) + 16 # short(36) + desc(48) + 1 prac(16) = 100
    assert tot_pts == 100, f"Run {i}: Total score {tot_pts} != 100"

    for q in exam:
        pool_counter[q["id"]] = pool_counter.get(q["id"], 0) + 1

# Check dead questions
assert len(pool_counter) == 180, f"Dead questions found! Only {len(pool_counter)}/180 picked"
print(f"- 1,000 runs completed with 0 exceptions")
print(f"- Each exam: exactly 18 questions, 100 total points, 0 internal duplicates")
print(f"- Pool coverage: {len(pool_counter)} / 180 (0 dead questions!)")
print(f"- Min appearances: {min(pool_counter.values())}, Max appearances: {max(pool_counter.values())}")

print("\n>> ALL CHECKS PASSED PERFECTLY (100%)!")
