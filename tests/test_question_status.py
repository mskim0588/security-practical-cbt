import unittest
from app.services.exam_service import ExamService

class TestQuestionStatus(unittest.TestCase):
    def test_single_short_question_status(self):
        q = {
            "id": "Q-SHORT-003",
            "type": "short",
            "sub_questions": None
        }
        # 1. 미작성
        res_empty = ExamService.calculate_question_status(q, "", False)
        self.assertEqual(res_empty["status_text"], "미작성")
        self.assertEqual(res_empty["status_code"], "empty")

        res_spaces = ExamService.calculate_question_status(q, "   ", False)
        self.assertEqual(res_spaces["status_text"], "미작성")

        # 3. 작성 완료
        res_filled = ExamService.calculate_question_status(q, "WPA2", False)
        self.assertEqual(res_filled["status_text"], "작성 완료")
        self.assertEqual(res_filled["status_code"], "complete")

    def test_sub_short_question_status(self):
        q = {
            "id": "Q-SHORT-001",
            "type": "short",
            "sub_questions": [
                {"label": "A"},
                {"label": "B"},
                {"label": "C"}
            ]
        }
        # 1. 미작성
        res_empty = ExamService.calculate_question_status(q, {}, False)
        self.assertEqual(res_empty["status_text"], "미작성")
        self.assertEqual(res_empty["status_code"], "empty")

        res_empty_dict = ExamService.calculate_question_status(q, {"A": "", "B": "   ", "C": ""}, False)
        self.assertEqual(res_empty_dict["status_text"], "미작성")

        # 2. 일부 작성 (1/3)
        res_part1 = ExamService.calculate_question_status(q, {"A": "침해요인", "B": "", "C": ""}, False)
        self.assertEqual(res_part1["status_text"], "일부 작성 (1/3)")
        self.assertEqual(res_part1["status_code"], "partial")

        # 2. 일부 작성 (2/3)
        res_part2 = ExamService.calculate_question_status(q, {"A": "침해요인", "B": "법적 준거성", "C": ""}, False)
        self.assertEqual(res_part2["status_text"], "일부 작성 (2/3)")
        self.assertEqual(res_part2["status_code"], "partial")

        # 3. 작성 완료
        res_full = ExamService.calculate_question_status(q, {"A": "침해요인", "B": "법적 준거성", "C": "2"}, False)
        self.assertEqual(res_full["status_text"], "작성 완료")
        self.assertEqual(res_full["status_code"], "complete")

    def test_descriptive_question_status(self):
        q = {
            "id": "Q-DESC-001",
            "type": "descriptive",
            "sub_questions": [
                {"sub_id": 1},
                {"sub_id": 2},
                {"sub_id": 3}
            ]
        }
        # 1. 미작성
        res_empty = ExamService.calculate_question_status(q, {}, False)
        self.assertEqual(res_empty["status_text"], "미작성")
        self.assertEqual(res_empty["status_code"], "empty")

        # 2. 일부 작성 (1/3)
        res_part = ExamService.calculate_question_status(q, {"1": "파라미터 설명"}, False)
        self.assertEqual(res_part["status_text"], "일부 작성 (1/3)")
        self.assertEqual(res_part["status_code"], "partial")

        # 3. 작성 완료
        res_full = ExamService.calculate_question_status(q, {"1": "설명1", "2": "설명2", "3": "설명3"}, False)
        self.assertEqual(res_full["status_text"], "작성 완료")
        self.assertEqual(res_full["status_code"], "complete")

    def test_practical_selected_question_status(self):
        q = {
            "id": "Q-PRAC-001",
            "type": "practical",
            "sub_questions": [
                {"sub_id": 1},
                {"sub_id": 2}
            ]
        }
        # 4-1. 선택됨 · 미작성
        res_empty = ExamService.calculate_question_status(q, {}, is_selected_practical=True)
        self.assertEqual(res_empty["status_text"], "선택됨 · 미작성")
        self.assertEqual(res_empty["status_code"], "empty")

        # 4-2. 선택됨 · 일부 작성 (1/2)
        res_part = ExamService.calculate_question_status(q, {"1": "체인 설명"}, is_selected_practical=True)
        self.assertEqual(res_part["status_text"], "선택됨 · 일부 작성 (1/2)")
        self.assertEqual(res_part["status_code"], "partial")

        # 4-3. 선택됨 · 작성 완료
        res_full = ExamService.calculate_question_status(q, {"1": "체인 설명", "2": "룰 분석"}, is_selected_practical=True)
        self.assertEqual(res_full["status_text"], "선택됨 · 작성 완료")
        self.assertEqual(res_full["status_code"], "complete")

    def test_practical_unselected_question_status(self):
        q = {
            "id": "Q-PRAC-002",
            "type": "practical",
            "sub_questions": [
                {"sub_id": 1},
                {"sub_id": 2}
            ]
        }
        # 5. 선택하지 않은 실무형 문제 -> 미선택 · 채점 제외
        res1 = ExamService.calculate_question_status(q, {}, is_selected_practical=False)
        self.assertEqual(res1["status_text"], "미선택 · 채점 제외")
        self.assertEqual(res1["status_code"], "unselected")

        # 답안이 들어있더라도 미선택 상태이면 미선택 · 채점 제외
        res2 = ExamService.calculate_question_status(q, {"1": "임의작성"}, is_selected_practical=False)
        self.assertEqual(res2["status_text"], "미선택 · 채점 제외")
        self.assertEqual(res2["status_code"], "unselected")

if __name__ == "__main__":
    unittest.main()
