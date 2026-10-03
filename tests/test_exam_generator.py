import unittest
from app.services.data_loader import DataLoader
from app.services.exam_generator import ExamGenerator

class TestExamGenerator(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()
        self.all_questions = self.loader.get_enriched_questions()

    def test_standard_exam_structure(self):
        exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="standard")
        self.assertEqual(len(exam_set), 18)

        short_qs = [q for q in exam_set if q["type"] == "short"]
        desc_qs = [q for q in exam_set if q["type"] == "descriptive"]
        prac_qs = [q for q in exam_set if q["type"] == "practical"]

        self.assertEqual(len(short_qs), 12)
        self.assertEqual(len(desc_qs), 4)
        self.assertEqual(len(prac_qs), 2)

        # 표준 ID 일치 확인
        self.assertEqual([q["id"] for q in exam_set], ExamGenerator.STANDARD_QUESTION_IDS)

        # 배점 확인
        self.assertEqual(sum(q["score"] for q in short_qs), 36)
        self.assertEqual(sum(q["score"] for q in desc_qs), 48)
        self.assertTrue(all(q["score"] == 16 for q in prac_qs))

    def test_random_exam_reproducibility_with_seed(self):
        set1 = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=42)
        set2 = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=42)
        self.assertEqual([q["id"] for q in set1], [q["id"] for q in set2])

    def test_random_exam_100_runs_integrity(self):
        """100회 랜덤 생성 반복 시에도 18문항 / 100점 / 중복 없음 불변 보장"""
        for i in range(100):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            
            # 1. 총 18문항
            self.assertEqual(len(exam_set), 18, f"Iteration {i}: Total count should be 18")
            
            # 2. 중복 문항 ID 없음
            ids = [q["id"] for q in exam_set]
            self.assertEqual(len(set(ids)), 18, f"Iteration {i}: Found duplicate question IDs: {ids}")
            
            # 3. 유형별 구성
            short_qs = [q for q in exam_set if q["type"] == "short"]
            desc_qs = [q for q in exam_set if q["type"] == "descriptive"]
            prac_qs = [q for q in exam_set if q["type"] == "practical"]
            
            self.assertEqual(len(short_qs), 12)
            self.assertEqual(len(desc_qs), 4)
            self.assertEqual(len(prac_qs), 2)
            
            # 4. 배점 무결성
            self.assertEqual(sum(q["score"] for q in short_qs), 36)
            self.assertEqual(sum(q["score"] for q in desc_qs), 48)
            self.assertTrue(all(q["score"] == 16 for q in prac_qs))
            
            # 5. 출처 페이지 및 파일명 존재
            for q in exam_set:
                self.assertIn("source_info", q)
                self.assertIn("source_page", q)
                self.assertGreater(q["source_page"], 0)

    def test_random_exam_pool_coverage(self):
        """랜덤 모의고사 반복 생성 시 문제은행 전체 풀(180문항)이 100% 활용되는지 검증"""
        used_100 = set()
        for i in range(100):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            for q in exam_set:
                used_100.add(q["id"])
        self.assertGreaterEqual(len(used_100), 100, "100회 실행 시 최소 100문항 이상이 출제되어야 합니다.")

        used_500 = set(used_100)
        for i in range(100, 500):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            for q in exam_set:
                used_500.add(q["id"])
        self.assertEqual(len(used_500), len(self.all_questions), "500회 실행 시 문제은행 전체 풀(180문항)이 100% 활용되어야 합니다.")

    def test_random_exam_short_category_distribution(self):
        """100회 랜덤 생성 시 단답형 12문제가 5대 표준 카테고리를 골고루 포함하는지 검증"""
        ALLOWED_CATEGORIES = {
            "시스템 보안",
            "네트워크 보안",
            "애플리케이션 보안",
            "정보보안 일반 및 암호학",
            "정보보호 관리 및 법규"
        }
        for i in range(100):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            short_qs = [q for q in exam_set if q["type"] == "short"]
            self.assertEqual(len(short_qs), 12)
            categories_in_shorts = set(q["category"] for q in short_qs)
            # 5개 표준 카테고리가 100% 모두 포함되어야 함
            self.assertEqual(categories_in_shorts, ALLOWED_CATEGORIES, f"Iteration {i}: 카테고리 누락 {ALLOWED_CATEGORIES - categories_in_shorts}")

    def test_random_exam_descriptive_concept_and_category_diversity(self):
        """서술형 4문제 선별 시 단답형 미사용 Concept 우선 및 Category 다양성 검증"""
        for i in range(100):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            short_qs = [q for q in exam_set if q["type"] == "short"]
            desc_qs = [q for q in exam_set if q["type"] == "descriptive"]

            self.assertEqual(len(desc_qs), 4)

            # 1. 서술형 내부 카테고리 다양성 (최소 2개 이상의 서로 다른 카테고리 포함)
            desc_cats = set(q["category"] for q in desc_qs)
            self.assertGreaterEqual(len(desc_cats), 2, f"Iteration {i}: 서술형 카테고리 다양성 부족 {desc_cats}")

            # 2. 단답형과의 Concept 중복 최소화 (단답형 사용 Concept 회피)
            short_concepts = set(q.get("concept_id") for q in short_qs if q.get("concept_id"))
            desc_concepts = set(q.get("concept_id") for q in desc_qs if q.get("concept_id"))
            overlap = short_concepts & desc_concepts
            # 단답형 12문항이 많은 Concept을 사용하더라도 서술형 4문항 중 중복은 최대 2개 이하로 제한
            self.assertLessEqual(len(overlap), 2, f"Iteration {i}: Concept 과다 중복 {overlap}")

    def test_random_exam_practical_diversity(self):
        """실무형 2문항 선별 시 서로 다른 Category 및 Concept 우선 선별 검증"""
        for i in range(100):
            exam_set = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=i)
            prac_qs = [q for q in exam_set if q["type"] == "practical"]

            self.assertEqual(len(prac_qs), 2)
            # 현재 8개 실무형 풀에서 서로 다른 카테고리와 컨셉이 정상 분산되는지 검증
            self.assertNotEqual(prac_qs[0]["category"], prac_qs[1]["category"], f"Iteration {i}: 동일 카테고리 실무형 출제 {prac_qs[0]['category']}")
            self.assertNotEqual(prac_qs[0]["concept_id"], prac_qs[1]["concept_id"], f"Iteration {i}: 동일 Concept 실무형 출제 {prac_qs[0]['concept_id']}")

    def test_generator_graceful_fallbacks(self):
        """풀 부족 또는 단일 카테고리 등 극한 상황에서의 Graceful Fallback 검증"""
        import random
        rng = random.Random(42)

        # 1. 서술형 풀이 target_count(4) 이하인 경우
        small_desc_pool = [q for q in self.all_questions if q["type"] == "descriptive"][:3]
        picked_desc = ExamGenerator._pick_balanced_descriptive(small_desc_pool, 4, avoid_concept_ids=set(), rng=rng)
        self.assertEqual(len(picked_desc), 3)

        # 2. 실무형 풀이 target_count(2) 이하인 경우
        small_prac_pool = [q for q in self.all_questions if q["type"] == "practical"][:1]
        picked_prac = ExamGenerator._pick_balanced_practical(small_prac_pool, 2, rng=rng)
        self.assertEqual(len(picked_prac), 1)

        # 3. 실무형 풀이 동일 카테고리만 존재하는 경우
        same_cat_prac_pool = [
            {"id": "Q-P1", "category": "네트워크 보안", "concept_id": "C1"},
            {"id": "Q-P2", "category": "네트워크 보안", "concept_id": "C2"},
            {"id": "Q-P3", "category": "네트워크 보안", "concept_id": "C1"}
        ]
        picked_same = ExamGenerator._pick_balanced_practical(same_cat_prac_pool, 2, rng=rng)
        self.assertEqual(len(picked_same), 2)
        # 카테고리가 같더라도 컨셉이 다른 것(C1 vs C2)을 우선 선택했는지 확인
        self.assertNotEqual(picked_same[0]["concept_id"], picked_same[1]["concept_id"])

if __name__ == "__main__":
    unittest.main()
