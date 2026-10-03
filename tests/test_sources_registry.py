import unittest
import os
from app.services.data_loader import DataLoader

PDF_DIR = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"

class TestSourcesRegistry(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()

    def test_sources_count_and_fields(self):
        sources = self.loader.load_sources()
        self.assertEqual(len(sources), 12, "sources.json에는 12개 PDF가 모두 등록되어야 합니다.")

        required_fields = ["id", "filename", "title", "source_type", "subject", "role", "priority", "total_pages", "description"]
        for s in sources:
            for field in required_fields:
                self.assertIn(field, s, f"Source {s.get('id')}에 필수 필드 '{field}'가 누락되었습니다.")
            self.assertIsInstance(s["total_pages"], int)
            self.assertGreater(s["total_pages"], 0)

    def test_sources_match_google_drive_files(self):
        """Google Drive의 12개 실제 파일명과 sources.json의 파일명이 1:1 일치하는지 검증"""
        if os.path.exists(PDF_DIR):
            drive_files = set(f for f in os.listdir(PDF_DIR) if f.endswith(".pdf"))
            registered_files = set(s["filename"] for s in self.loader.load_sources())
            self.assertEqual(drive_files, registered_files, "Google Drive의 12개 파일과 sources.json 등록 파일명이 완벽히 일치해야 합니다.")

    def test_concepts_integrity(self):
        """concepts.json의 15개 핵심 개념 및 Source ID 유효성 검증"""
        concepts = self.loader.load_concepts()
        self.assertGreaterEqual(len(concepts), 15, "concepts.json에 최소 15개 핵심 개념이 등록되어야 합니다.")

        source_dict = self.loader.get_sources_dict()
        for c in concepts:
            self.assertIn("id", c)
            self.assertIn("name", c)
            self.assertIn("category", c)
            self.assertIn("primary_source_id", c)
            self.assertIn(c["primary_source_id"], source_dict, f"Concept {c['id']}의 primary_source_id가 sources.json에 없습니다.")

    def test_sources_summary(self):
        """DataLoader의 출처 요약 및 동적 집계 검증"""
        summary = self.loader.get_sources_summary()
        self.assertEqual(summary["total_sources"], 12, "등록된 전체 PDF 자료 수는 12여야 합니다.")
        self.assertEqual(summary["active_sources_count"], 12, "현재 사용 중인 Source 수는 12여야 합니다.")
        self.assertEqual(summary["total_questions_count"], 180, "현재 등록된 전체 문제 수는 180이어야 합니다.")
        self.assertEqual(len(summary["exam_sources"]), 3)
        self.assertEqual(len(summary["theory_sources"]), 9)

        # 개별 Source 상태 검증
        sources_by_id = {s["id"]: s for s in summary["all_sources"]}
        
        # 1. SRC-01 (단답형): 사용 중 · 59문제
        self.assertTrue(sources_by_id["SRC-01"]["is_active"])
        self.assertEqual(sources_by_id["SRC-01"]["question_count"], 59)
        self.assertEqual(sources_by_id["SRC-01"]["status_text"], "사용 중 · 59문제")

        # 2. SRC-02 (서술형): 사용 중 · 25문제
        self.assertTrue(sources_by_id["SRC-02"]["is_active"])
        self.assertEqual(sources_by_id["SRC-02"]["question_count"], 25)
        self.assertEqual(sources_by_id["SRC-02"]["status_text"], "사용 중 · 25문제")

        # 3. SRC-03 (서술형 TOP20): 사용 중 · 7문제
        self.assertTrue(sources_by_id["SRC-03"]["is_active"])
        self.assertEqual(sources_by_id["SRC-03"]["question_count"], 7)
        self.assertEqual(sources_by_id["SRC-03"]["status_text"], "사용 중 · 7문제")

        # 4. SRC-04 (4과목): 사용 중 · 10문제
        self.assertTrue(sources_by_id["SRC-04"]["is_active"])
        self.assertEqual(sources_by_id["SRC-04"]["question_count"], 10)
        self.assertEqual(sources_by_id["SRC-04"]["status_text"], "사용 중 · 10문제")

        # 5. SRC-05 (요약노트): 사용 중 · 9문제
        self.assertTrue(sources_by_id["SRC-05"]["is_active"])
        self.assertEqual(sources_by_id["SRC-05"]["question_count"], 9)
        self.assertEqual(sources_by_id["SRC-05"]["status_text"], "사용 중 · 9문제")

        # 6. SRC-06 (1과목 시스템): 사용 중 · 10문제
        self.assertTrue(sources_by_id["SRC-06"]["is_active"])
        self.assertEqual(sources_by_id["SRC-06"]["question_count"], 10)
        self.assertEqual(sources_by_id["SRC-06"]["status_text"], "사용 중 · 10문제")

        # 7. SRC-07 (2과목 네트워크): 사용 중 · 10문제
        self.assertTrue(sources_by_id["SRC-07"]["is_active"])
        self.assertEqual(sources_by_id["SRC-07"]["question_count"], 10)
        self.assertEqual(sources_by_id["SRC-07"]["status_text"], "사용 중 · 10문제")

        # 8. SRC-08 (3과목 애플리케이션): 사용 중 · 10문제
        self.assertTrue(sources_by_id["SRC-08"]["is_active"])
        self.assertEqual(sources_by_id["SRC-08"]["question_count"], 10)
        self.assertEqual(sources_by_id["SRC-08"]["status_text"], "사용 중 · 10문제")

        # 9. SRC-09 (암호학): 사용 중 · 17문제
        self.assertTrue(sources_by_id["SRC-09"]["is_active"])
        self.assertEqual(sources_by_id["SRC-09"]["question_count"], 17)
        self.assertEqual(sources_by_id["SRC-09"]["status_text"], "사용 중 · 17문제")

        # 10. SRC-10 (정보보호 관리): 사용 중 · 9문제
        self.assertTrue(sources_by_id["SRC-10"]["is_active"])
        self.assertEqual(sources_by_id["SRC-10"]["question_count"], 9)
        self.assertEqual(sources_by_id["SRC-10"]["status_text"], "사용 중 · 9문제")

        # 11. SRC-11 (법규): 사용 중 · 4문제
        self.assertTrue(sources_by_id["SRC-11"]["is_active"])
        self.assertEqual(sources_by_id["SRC-11"]["question_count"], 4)
        self.assertEqual(sources_by_id["SRC-11"]["status_text"], "사용 중 · 4문제")

        # 12. SRC-12 (종합 정리): 사용 중 · 10문제
        self.assertTrue(sources_by_id["SRC-12"]["is_active"])
        self.assertEqual(sources_by_id["SRC-12"]["question_count"], 10)
        self.assertEqual(sources_by_id["SRC-12"]["status_text"], "사용 중 · 10문제")

    def test_existing_18_questions_source_integrity(self):
        """기존 문제를 포함한 전체 문제의 source_id 및 source_page 참조 무결성 검증"""
        questions = self.loader.load_questions()
        self.assertEqual(len(questions), 180, "Batch 3 확장에 따라 총 180문제여야 합니다.")
        source_dict = self.loader.get_sources_dict()

        for q in questions:
            self.assertIn(q["source_id"], source_dict)
            self.assertIsInstance(q["source_page"], int)
            self.assertGreater(q["source_page"], 0)

    def test_source_group_3_and_9_split(self):
        """기출/문제형 3권(SRC-01~03)과 이론/교안형 9권(SRC-04~12) 명확한 구분 검증"""
        sources = self.loader.load_sources()
        exam_srcs = [s["id"] for s in sources if s.get("group") == "exam"]
        theory_srcs = [s["id"] for s in sources if s.get("group") == "theory"]

        self.assertEqual(exam_srcs, ["SRC-01", "SRC-02", "SRC-03"], "기출/문제형은 SRC-01~SRC-03 3권이어야 합니다.")
        self.assertEqual(theory_srcs, [f"SRC-{i:02d}" for i in range(4, 13)], "이론/교안형은 SRC-04~SRC-12 9권이어야 합니다.")

    def test_questions_concept_mapping_integrity(self):
        """기존 18문제의 concept_id 유효성, Concept 재사용성, category-concept 분리 검증"""
        questions = self.loader.load_questions()
        concepts = self.loader.load_concepts()
        concept_dict = {c["id"]: c for c in concepts}

        concept_usage = {}
        for q in questions:
            cid = q.get("concept_id")
            self.assertIsNotNone(cid, f"문제 {q['id']}에 concept_id가 없습니다.")
            self.assertIn(cid, concept_dict, f"문제 {q['id']}의 concept_id({cid})가 concepts.json에 없습니다.")
            concept_usage[cid] = concept_usage.get(cid, 0) + 1

            # category와 concept_id가 논리적으로 분리되어 있는지 확인
            self.assertIn("category", q)
            self.assertNotEqual(q["category"], cid)

        # 하나의 Concept이 여러 문제에서 재사용되는 구조인지 검증
        reused_concepts = [cid for cid, count in concept_usage.items() if count > 1]
        self.assertGreater(len(reused_concepts), 0, "최소 1개 이상의 Concept이 여러 문제에서 재사용되어야 합니다.")

    def test_semantic_concept_mapping_18_questions(self):
        """18문제 전체의 Question ↔ Category ↔ Concept 의미적 정합성 전수 검증"""
        expected_mappings = {
            "Q-SHORT-001": ("정보보호 관리 및 법규", "CON-MGT-01"),
            "Q-SHORT-002": ("애플리케이션 보안", "CON-APP-03"),
            "Q-SHORT-003": ("네트워크 보안", "CON-NET-02"),
            "Q-SHORT-004": ("네트워크 보안", "CON-NET-04"),
            "Q-SHORT-005": ("애플리케이션 보안", "CON-APP-02"),
            "Q-SHORT-006": ("정보보호 관리 및 법규", "CON-MGT-01"),
            "Q-SHORT-007": ("정보보안 일반 및 암호학", "CON-SEC-01"),
            "Q-SHORT-008": ("시스템 보안", "CON-SYS-03"),
            "Q-SHORT-009": ("정보보호 관리 및 법규", "CON-MGT-02"),
            "Q-SHORT-010": ("애플리케이션 보안", "CON-APP-04"),
            "Q-SHORT-011": ("시스템 보안", "CON-SYS-02"),
            "Q-SHORT-012": ("시스템 보안", "CON-SYS-01"),
            "Q-DESC-001": ("애플리케이션 보안", "CON-APP-01"),
            "Q-DESC-002": ("시스템 보안", "CON-SYS-01"),
            "Q-DESC-003": ("네트워크 보안", "CON-NET-03"),
            "Q-DESC-004": ("애플리케이션 보안", "CON-APP-01"),
            "Q-PRAC-001": ("네트워크 보안", "CON-NET-01"),
            "Q-PRAC-002": ("네트워크 보안", "CON-NET-01"),
        }

        ALLOWED_CATEGORIES = {
            "시스템 보안",
            "네트워크 보안",
            "애플리케이션 보안",
            "정보보안 일반 및 암호학",
            "정보보호 관리 및 법규"
        }

        questions = {q["id"]: q for q in self.loader.load_questions()}
        self.assertGreaterEqual(len(questions), 18)

        for qid, (exp_cat, exp_cid) in expected_mappings.items():
            self.assertIn(qid, questions, f"문제 {qid}가 존재하지 않습니다.")
            q = questions[qid]
            self.assertIn(q["category"], ALLOWED_CATEGORIES, f"문제 {qid}의 category가 표준 5대 카테고리에 속하지 않습니다: {q['category']}")
            self.assertEqual(q["category"], exp_cat, f"문제 {qid}의 category가 일치하지 않습니다: {q['category']} != {exp_cat}")
            self.assertEqual(q["concept_id"], exp_cid, f"문제 {qid}의 concept_id가 일치하지 않습니다: {q['concept_id']} != {exp_cid}")

if __name__ == "__main__":
    unittest.main()
