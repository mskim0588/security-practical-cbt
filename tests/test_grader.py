import unittest
from app.services.grader import Grader
from app.services.data_loader import DataLoader

class TestGrader(unittest.TestCase):
    def test_short_normalization(self):
        # 대소문자 무시
        self.assertEqual(Grader.normalize_short_answer("Log4J"), "log4j")
        # 다중 공백 및 양끝 공백 제거
        self.assertEqual(Grader.normalize_short_answer("  위험   식별  "), "위험 식별")
        # 유니코드 대시 정규화
        self.assertEqual(Grader.normalize_short_answer("WPA–2"), "wpa-2")
        # 양끝 따옴표 및 마침표 제거
        self.assertEqual(Grader.normalize_short_answer("'robots.txt.'"), "robots.txt")

    def test_short_match(self):
        # 1차 직접 일치 (대소문자 불문)
        self.assertTrue(Grader.match_short_answer("WPA2", "WPA2", ["IEEE 802.11i"]))
        self.assertTrue(Grader.match_short_answer("wpa2", "WPA2"))
        # accepted_answers 매칭
        self.assertTrue(Grader.match_short_answer("IEEE 802.11i", "WPA2", ["IEEE 802.11i"]))
        # 띄어쓰기 유연성 매칭 (예: "위험 식별" vs "위험식별")
        self.assertTrue(Grader.match_short_answer("위험 식별", "위험식별"))
        self.assertTrue(Grader.match_short_answer("위험식별", "위험 식별"))
        # 오답
        self.assertFalse(Grader.match_short_answer("WPA3", "WPA2"))

    def test_grade_short_sub_questions(self):
        q = {
            "id": "Q-SHORT-001",
            "score": 3,
            "sub_questions": [
                {"label": "A", "score": 1, "answer": "침해요인 발생 가능성", "accepted_answers": ["발생가능성"]},
                {"label": "B", "score": 1, "answer": "법적 준거성", "accepted_answers": ["법적준거성"]},
                {"label": "C", "score": 1, "answer": "2", "accepted_answers": ["2.0"]}
            ]
        }
        # 3개 다 맞춤
        res = Grader.grade_short_question(q, {"A": "침해요인 발생가능성", "B": "법적 준거성", "C": "2"})
        self.assertEqual(res["earned_score"], 3.0)
        self.assertTrue(res["is_correct"])

        # 1개만 맞춤
        res_part = Grader.grade_short_question(q, {"A": "침해요인 발생가능성", "B": "틀린답", "C": "3"})
        self.assertEqual(res_part["earned_score"], 1.0)
        self.assertFalse(res_part["is_correct"])

    def test_descriptive_rubric(self):
        sub_q = {
            "sub_id": 1,
            "score": 4,
            "prompt": "안전한 소유자 설정",
            "model_answer": "/etc/hosts.equiv는 root, $HOME/.rhosts는 root 또는 해당 사용자 계정 소유",
            "rubric": {
                "keywords": [
                    ["root", "루트"],
                    ["해당 계정", "해당 사용자"]
                ],
                "all_match_points": 4,
                "partial_match_points": 2
            }
        }
        # 만점 답변 (둘 다 포함)
        full_res = Grader.grade_rubric_sub_question("root 및 해당 사용자로 변경합니다", sub_q)
        self.assertEqual(full_res["earned_score"], 4.0)
        self.assertEqual(len(full_res["matched_keywords"]), 2)

        # 부분점수 답변 (root만 포함)
        part_res = Grader.grade_rubric_sub_question("관리자 root로 설정합니다", sub_q)
        self.assertEqual(part_res["earned_score"], 2.0)
        self.assertEqual(len(part_res["matched_keywords"]), 1)

        # 0점 답변
        zero_res = Grader.grade_rubric_sub_question("모르겠습니다", sub_q)
        self.assertEqual(zero_res["earned_score"], 0.0)

    def test_practical_selection_grading(self):
        q_prac1 = {
            "id": "Q-PRAC-001",
            "type": "practical",
            "score": 16,
            "sub_questions": [
                {
                    "sub_id": 1,
                    "score": 16,
                    "rubric": {"keywords": [["INPUT"], ["FORWARD"], ["OUTPUT"]], "all_match_points": 16, "partial_match_points": 8}
                }
            ]
        }

        # 1. 선택된 경우 -> 정상 채점
        res_sel = Grader.grade_practical_question(q_prac1, {"1": "INPUT FORWARD OUTPUT 체인이 있습니다"}, is_selected=True)
        self.assertTrue(res_sel["is_selected"])
        self.assertEqual(res_sel["earned_score"], 16.0)

        # 2. 선택되지 않은 경우 -> 0점 및 채점 제외 처리
        res_unsel = Grader.grade_practical_question(q_prac1, {"1": "INPUT FORWARD OUTPUT 체인이 있습니다"}, is_selected=False)
        self.assertFalse(res_unsel["is_selected"])
        self.assertEqual(res_unsel["earned_score"], 0.0)

    def test_full_exam_100_points(self):
        from app.services.exam_generator import ExamGenerator
        loader = DataLoader()
        all_questions = loader.get_enriched_questions()
        questions = ExamGenerator.generate_exam_set(all_questions, mode="standard")

        # 만점 시뮬레이션
        answers = {}
        for q in questions:
            q_id = q["id"]
            if q["type"] == "short":
                if q.get("sub_questions"):
                    answers[q_id] = {sub["label"]: sub["answer"] for sub in q["sub_questions"]}
                else:
                    answers[q_id] = q.get("answer")
            elif q["type"] == "descriptive":
                answers[q_id] = {str(sub["sub_id"]): sub["model_answer"] for sub in q.get("sub_questions", [])}
            elif q["type"] == "practical":
                answers[q_id] = {str(sub["sub_id"]): sub["model_answer"] for sub in q.get("sub_questions", [])}

        submission = {
            "selected_practical_id": "Q-PRAC-001",
            "answers": answers
        }

        res = Grader.grade_full_exam(questions, submission)
        self.assertEqual(res["max_total_score"], 100.0)
        self.assertEqual(res["summary"]["short"]["max"], 36.0)
        self.assertEqual(res["summary"]["descriptive"]["max"], 48.0)
        self.assertEqual(res["summary"]["practical"]["max"], 16.0)
        # 만점 점수 합산 검증
        self.assertEqual(res["total_score"], 100.0)
        self.assertTrue(res["is_passed"])

if __name__ == "__main__":
    unittest.main()
