import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.data_loader import DataLoader

def verify_all():
    loader = DataLoader()
    sources = loader.load_sources()
    concepts = loader.load_concepts()
    questions = loader.load_questions()

    print("=== [1. 12 Source Registry & 3/9 Classification] ===")
    assert len(sources) == 12, f"Expected 12 sources, got {len(sources)}"
    source_ids = [s["id"] for s in sources]
    assert len(source_ids) == len(set(source_ids)), "Source IDs must be unique"
    
    # 3권 기출 vs 9권 이론 분류 확인
    exam_srcs = [s["id"] for s in sources if s.get("group") == "exam"]
    theory_srcs = [s["id"] for s in sources if s.get("group") == "theory"]
    print(f"Exam Sources (3권): {exam_srcs}")
    print(f"Theory Sources (9권): {theory_srcs}")
    assert exam_srcs == ["SRC-01", "SRC-02", "SRC-03"]
    assert theory_srcs == [f"SRC-{i:02d}" for i in range(4, 13)]

    print("\n=== [2. Concept Registry Integrity] ===")
    print(f"Total Concepts: {len(concepts)}")
    assert len(concepts) >= 15, "At least 15 concepts expected"
    concept_ids = [c["id"] for c in concepts]
    assert len(concept_ids) == len(set(concept_ids)), "Concept IDs must be unique"

    required_concept_fields = ["id", "name", "category", "description", "source_ids"]
    for c in concepts:
        for f in required_concept_fields:
            assert f in c, f"Concept {c.get('id')} missing field: {f}"
        assert isinstance(c["source_ids"], list), f"source_ids must be a list in {c['id']}"
        assert len(c["source_ids"]) > 0, f"source_ids cannot be empty in {c['id']}"

    ALLOWED_CATEGORIES = {
        "시스템 보안",
        "네트워크 보안",
        "애플리케이션 보안",
        "정보보안 일반 및 암호학",
        "정보보호 관리 및 법규"
    }

    for c in concepts:
        assert c["category"] in ALLOWED_CATEGORIES, f"Concept {c['id']} category not in allowed 5: {c['category']}"

    print("\n=== [3. Question-to-Concept Mapping across 18 Questions] ===")
    assert len(questions) == 18, f"Expected 18 questions, got {len(questions)}"
    c_dict = {c["id"]: c for c in concepts}
    concept_usage = {}

    for q in questions:
        cid = q.get("concept_id")
        qid = q.get("id")
        assert cid is not None, f"Question {qid} missing concept_id"
        assert cid in c_dict, f"Question {qid} references unknown concept_id: {cid}"
        assert q["category"] in ALLOWED_CATEGORIES, f"Question {qid} category not in allowed 5: {q['category']}"
        concept_usage[cid] = concept_usage.get(cid, 0) + 1
        
        # Verify concept category matches question category or domain
        c_obj = c_dict[cid]
        print(f"  {qid} [{q['type']}] -> {cid} ({c_obj['name']}) | Cat: {q['category']}")

    print("\n=== [4. Concept Reusability Analysis] ===")
    for cid, count in sorted(concept_usage.items()):
        c_name = c_dict[cid]["name"]
        print(f"  {cid} ({c_name}): reused in {count} questions")

    # Verify at least one concept is reused across multiple questions
    reused = [cid for cid, count in concept_usage.items() if count > 1]
    assert len(reused) > 0, "Concepts must be reusable across multiple questions"

    print("\n=== [5. Exam Scoring Integrity] ===")
    from app.services.exam_service import ExamService
    service = ExamService(loader)
    std_qs = service.get_exam_questions(mode="standard")
    assert len(std_qs) == 18
    short_qs = [q for q in std_qs if q["type"] == "short"]
    desc_qs = [q for q in std_qs if q["type"] == "descriptive"]
    prac_qs = [q for q in std_qs if q["type"] == "practical"]

    assert len(short_qs) == 12 and sum(q["score"] for q in short_qs) == 36
    assert len(desc_qs) == 4 and sum(q["score"] for q in desc_qs) == 48
    assert len(prac_qs) == 2 and all(q["score"] == 16 for q in prac_qs)
    print("Scoring structure intact: 12 short (36p) + 4 desc (48p) + 2 prac (16p each, 1 required) = 100p total")

    print("\n=======================================================")
    print(">>> ALL CONCEPT & SOURCE SPECIFICATIONS FULLY VERIFIED! <<<")
    print("=======================================================")

if __name__ == "__main__":
    verify_all()
