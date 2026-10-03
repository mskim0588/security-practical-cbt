import unittest
from app import create_app

class TestExamRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("정보보안기사 실기시험".encode("utf-8"), response.data)
        self.assertIn("36점".encode("utf-8"), response.data)
        self.assertIn("48점".encode("utf-8"), response.data)
        self.assertIn("16점".encode("utf-8"), response.data)

    def test_exam_route(self):
        response = self.client.get("/exam")
        self.assertEqual(response.status_code, 200)
        # 18개 문항 카드가 존재하는지 확인
        self.assertIn("Q-SHORT-001".encode("utf-8"), response.data)
        self.assertIn("Q-DESC-001".encode("utf-8"), response.data)
        self.assertIn("Q-PRAC-001".encode("utf-8"), response.data)
        self.assertIn("Q-PRAC-002".encode("utf-8"), response.data)

    def test_review_route(self):
        form_data = {
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_B": "법적 준거성",
            "ans_Q-SHORT-001_C": "2",
            "ans_Q-SHORT-003": "WPA2"
        }
        response = self.client.post("/review", data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("답안 최종 검토".encode("utf-8"), response.data)
        self.assertIn("17번 (IPTables) 선택됨".encode("utf-8"), response.data)

    def test_submit_route(self):
        form_data = {
            "selected_practical_id": "Q-PRAC-001",
            "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
            "ans_Q-SHORT-001_B": "법적 준거성",
            "ans_Q-SHORT-001_C": "2",
            "ans_Q-SHORT-003": "WPA2",
            "ans_Q-SHORT-005": "robots.txt",
            "ans_Q-SHORT-007": "DLP",
            "ans_Q-SHORT-008": "/proc",
            "ans_Q-SHORT-010": "Log4j"
        }
        response = self.client.post("/submit", data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("정보보안기사 실기 모의고사 채점 결과".encode("utf-8"), response.data)
        self.assertIn("/ 100점".encode("utf-8"), response.data)
        self.assertIn("출처:".encode("utf-8"), response.data)
        self.assertIn("Page".encode("utf-8"), response.data)

    def test_exam_route_random_mode_without_seed(self):
        response = self.client.get("/exam?mode=random")
        self.assertEqual(response.status_code, 200)
        self.assertIn("랜덤 실전 모의고사".encode("utf-8"), response.data)
        self.assertNotIn("시험 Seed:".encode("utf-8"), response.data)

    def test_exam_route_random_mode_with_seed_deterministic(self):
        """A. 동일 seed=123 반복 호출 시 동일 Question ID 조합 및 순서 반환 검증"""
        import re
        res1 = self.client.get("/exam?mode=random&seed=123")
        self.assertEqual(res1.status_code, 200)
        self.assertIn("시험 Seed: 123".encode("utf-8"), res1.data)

        res2 = self.client.get("/exam?mode=random&seed=123")
        self.assertEqual(res2.status_code, 200)

        qids1 = re.search(r'name="question_ids" value="([^"]+)"', res1.data.decode("utf-8")).group(1)
        qids2 = re.search(r'name="question_ids" value="([^"]+)"', res2.data.decode("utf-8")).group(1)
        self.assertEqual(qids1, qids2, "동일한 seed=123은 완전히 동일한 문제 세트를 반환해야 합니다.")

    def test_exam_route_random_mode_different_seeds(self):
        """B. 다른 seed(123 vs 456)는 서로 다른 세트 생성 검증"""
        import re
        res1 = self.client.get("/exam?mode=random&seed=123")
        res2 = self.client.get("/exam?mode=random&seed=456")
        qids1 = re.search(r'name="question_ids" value="([^"]+)"', res1.data.decode("utf-8")).group(1)
        qids2 = re.search(r'name="question_ids" value="([^"]+)"', res2.data.decode("utf-8")).group(1)
        self.assertNotEqual(qids1, qids2, "서로 다른 seed는 서로 다른 시험 세트를 생성해야 합니다.")

    def test_exam_route_random_mode_invalid_seed_fallback(self):
        """D. 잘못된 seed(?seed=abc) 전달 시 500 서버 오류 없이 200 OK 및 일반 랜덤으로 fallback"""
        response = self.client.get("/exam?mode=random&seed=abc")
        self.assertEqual(response.status_code, 200)
        self.assertIn("랜덤 실전 모의고사".encode("utf-8"), response.data)
        self.assertNotIn("시험 Seed:".encode("utf-8"), response.data)
    def test_exam_route_practical_radio_standard(self):
        """E. 표준 모의고사에서 실무형 라디오 버튼이 Q-PRAC-001, Q-PRAC-002와 일치하는지 검증"""
        import re
        response = self.client.get("/exam?mode=standard")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        radios = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"', html)
        self.assertEqual(radios, ["Q-PRAC-001", "Q-PRAC-002"])

    def test_exam_route_practical_radio_random_dynamic(self):
        """F. 랜덤 모의고사(seed=42)에서 practical ID가 Q-PRAC-001/002가 아닐 때도 라디오 value가 실제 출제 문제와 일치하는지 검증"""
        import re
        response = self.client.get("/exam?mode=random&seed=42")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")
        radios = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"', html)
        cards = re.findall(r'class="question-card practical-card"\s+id="q-([^"]+)"', html)
        self.assertEqual(len(radios), 2, "실무형 라디오 버튼은 2개여야 합니다.")
        self.assertEqual(radios, cards, "라디오 버튼의 value는 실제 출제된 실무형 카드의 ID와 정확히 일치해야 합니다.")
        # seed=42에서는 Q-PRAC-007, Q-PRAC-014가 출제되므로 하드코딩된 Q-PRAC-001/002가 아님을 확인
        self.assertNotEqual(radios, ["Q-PRAC-001", "Q-PRAC-002"])

if __name__ == "__main__":
    unittest.main()

