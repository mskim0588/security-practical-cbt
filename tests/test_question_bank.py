import unittest
from app.services.data_loader import DataLoader

class TestQuestionBank(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.all_questions = self.loader.get_enriched_questions()
        self.sources = self.loader.load_sources()
        self.concepts = self.loader.load_concepts()

    def test_total_question_count_and_types(self):
        """문제은행 문항 규격 및 최소 요건 (단답 >= 12, 서술 >= 4, 실무 >= 2) 검증"""
        self.assertGreaterEqual(len(self.all_questions), 18)

        short_qs = [q for q in self.all_questions if q["type"] == "short"]
        desc_qs = [q for q in self.all_questions if q["type"] == "descriptive"]
        prac_qs = [q for q in self.all_questions if q["type"] == "practical"]

        self.assertGreaterEqual(len(short_qs), 12)
        self.assertGreaterEqual(len(desc_qs), 4)
        self.assertGreaterEqual(len(prac_qs), 2)

        # 배점 규격
        self.assertTrue(all(q["score"] == 3 for q in short_qs))
        self.assertTrue(all(q["score"] == 12 for q in desc_qs))
        self.assertTrue(all(q["score"] == 16 for q in prac_qs))

    def test_required_fields_and_source_integrity(self):
        """모든 문제의 필수 필드 및 출처 메타데이터 무결성 검사"""
        source_ids = {s["id"] for s in self.sources}
        concept_ids = {c["id"] for c in self.concepts}

        for q in self.all_questions:
            # 공통 필수 필드
            self.assertIn("id", q)
            self.assertIn("type", q)
            self.assertIn("category", q)
            self.assertIn("score", q)
            self.assertIn("question", q)
            self.assertIn("explanation", q)
            self.assertIn("source_id", q)
            self.assertIn("source_page", q)
            self.assertIn("concept_id", q)

            # 출처 유효성
            self.assertIn(q["source_id"], source_ids, f"Unknown source_id {q['source_id']} in {q['id']}")
            self.assertIsInstance(q["source_page"], int)
            self.assertGreater(q["source_page"], 0)

            # 개념 ID 유효성
            self.assertIn(q["concept_id"], concept_ids, f"Unknown concept_id {q['concept_id']} in {q['id']}")

            # 유형별 세부 필드
            if q["type"] == "short":
                self.assertIn("grading_mode", q)
                self.assertIn(q["grading_mode"], ("normalized", "strict"))
                if q.get("sub_questions"):
                    self.assertGreaterEqual(len(q["sub_questions"]), 2)
                    self.assertEqual(sum(sub["score"] for sub in q["sub_questions"]), 3.0)
                else:
                    self.assertIsNotNone(q.get("answer"))
            else:
                self.assertIsNotNone(q.get("sub_questions"))
                for sub in q["sub_questions"]:
                    self.assertIn("sub_id", sub)
                    self.assertIn("score", sub)
                    self.assertIn("model_answer", sub)
                    self.assertIn("rubric", sub)
                    self.assertIsInstance(sub["rubric"], dict)
                    self.assertIn("keywords", sub["rubric"])

    def test_pool_validation_via_data_loader(self):
        pool_val = self.loader.validate_dataset(scope="pool")
        self.assertTrue(pool_val["valid"])
        self.assertEqual(pool_val["total_candidate_count"], 180)
        self.assertEqual(pool_val["short_count"], 112)
        self.assertEqual(pool_val["desc_count"], 44)
        self.assertEqual(pool_val["prac_count"], 24)

    def test_goal_2b2_expansion_exact_metrics(self):
        """Goal 2D Batch 3 180문항(단답 112, 서술 44, 실무 24) 규모 및 ID 고유성 검증"""
        self.assertEqual(len(self.all_questions), 180)
        
        short_qs = [q for q in self.all_questions if q["type"] == "short"]
        desc_qs = [q for q in self.all_questions if q["type"] == "descriptive"]
        prac_qs = [q for q in self.all_questions if q["type"] == "practical"]

        self.assertEqual(len(short_qs), 112)
        self.assertEqual(len(desc_qs), 44)
        self.assertEqual(len(prac_qs), 24)

        # ID 고유성
        ids = [q["id"] for q in self.all_questions]
        self.assertEqual(len(ids), len(set(ids)), "모든 문제 ID는 고유해야 합니다.")

        # grading_mode 검증 (단답형 strict 22, normalized 90)
        strict_qs = [q for q in short_qs if q.get("grading_mode") == "strict"]
        norm_qs = [q for q in short_qs if q.get("grading_mode") == "normalized"]
        self.assertEqual(len(strict_qs), 22)
        self.assertEqual(len(norm_qs), 90)
        self.assertEqual(len(strict_qs) + len(norm_qs), 112)

    def test_goal_2b2_standard_categories_and_concepts(self):
        """5대 표준 카테고리 준수 및 20개 Concept 매핑 무결성 검증"""
        ALLOWED_CATEGORIES = {
            "시스템 보안",
            "네트워크 보안",
            "애플리케이션 보안",
            "정보보안 일반 및 암호학",
            "정보보호 관리 및 법규"
        }
        self.assertEqual(len(self.concepts), 20)
        concept_ids = {c["id"] for c in self.concepts}

        self.assertIn("CON-SEC-02", concept_ids)
        self.assertIn("CON-MGT-04", concept_ids)

        for q in self.all_questions:
            self.assertIn(q["category"], ALLOWED_CATEGORIES, f"{q['id']} 카테고리 불일치: {q['category']}")
            self.assertIn(q["concept_id"], concept_ids, f"{q['id']} concept_id 미등록: {q['concept_id']}")

    def test_goal_2b2_sub_question_scores_sum(self):
        """서술형(12점) 및 실무형(16점) 소문항 배점 합계 검증"""
        for q in self.all_questions:
            if q["type"] == "short" and q.get("sub_questions"):
                sub_sum = sum(s["score"] for s in q["sub_questions"])
                self.assertAlmostEqual(sub_sum, 3.0, places=2, msg=f"{q['id']} 단답형 소문항 합계 오류")
            elif q["type"] == "descriptive":
                self.assertEqual(q["score"], 12)
                sub_sum = sum(s["score"] for s in q["sub_questions"])
                self.assertAlmostEqual(sub_sum, 12.0, places=2, msg=f"{q['id']} 서술형 소문항 합계 오류")
            elif q["type"] == "practical":
                self.assertEqual(q["score"], 16)
                sub_sum = sum(s["score"] for s in q["sub_questions"])
                self.assertAlmostEqual(sub_sum, 16.0, places=2, msg=f"{q['id']} 실무형 소문항 합계 오류")

    def test_goal_2b2_original_18_questions_preservation(self):
        """기존 18문제의 ID, 배점, 표준 모의고사 세트 생성 완전 보존 검증"""
        from app.services.exam_generator import ExamGenerator
        all_ids = {q["id"] for q in self.all_questions}
        for qid in ExamGenerator.STANDARD_QUESTION_IDS:
            self.assertIn(qid, all_ids, f"표준 문제 {qid}가 문제은행에 누락되었습니다.")

        # 표준 모의고사 생성 시 정확히 기존 18문항 추출
        std_exam = ExamGenerator.generate_exam_set(self.all_questions, mode="standard")
        self.assertEqual(len(std_exam), 18)
        self.assertEqual([q["id"] for q in std_exam], ExamGenerator.STANDARD_QUESTION_IDS)

if __name__ == "__main__":
    unittest.main()
