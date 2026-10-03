import unittest
from app.services.grader import Grader
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService

class TestGradingModes(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()

    def test_1_normalized_mode_existing_behavior(self):
        """1. normalized 기존 채점 동작 유지 검증 (대소문자 무시, 공백 정규화)"""
        # Log4j / log4j 대소문자 허용 정책 유지
        self.assertTrue(Grader.match_short_answer("Log4j", "Log4j", grading_mode="normalized"))
        self.assertTrue(Grader.match_short_answer("log4j", "Log4j", grading_mode="normalized"))
        self.assertTrue(Grader.match_short_answer("LOG4J", "Log4j", grading_mode="normalized"))
        # 띄어쓰기 유연성 허용
        self.assertTrue(Grader.match_short_answer("위험 식별", "위험식별", grading_mode="normalized"))
        self.assertTrue(Grader.match_short_answer("위험식별", "위험 식별", grading_mode="normalized"))
        # wpa2 대소문자 허용
        self.assertTrue(Grader.match_short_answer("wpa2", "WPA2", grading_mode="normalized"))
        # 다중 공백 허용
        self.assertTrue(Grader.match_short_answer("  Log4j  ", "Log4j", grading_mode="normalized"))

    def test_2_strict_exact_answer(self):
        """2. strict 정확한 답안 정답 처리 검증 (양끝 trim 허용, 정확한 문자열)"""
        # /proc == /proc -> 정답
        self.assertTrue(Grader.match_short_answer("/proc", "/proc", grading_mode="strict"))
        # chmod 644 == chmod 644 -> 정답
        self.assertTrue(Grader.match_short_answer("chmod 644", "chmod 644", grading_mode="strict"))
        # 파일명 및 Windows 로그 디렉터리
        self.assertTrue(Grader.match_short_answer("robots.txt", "robots.txt", grading_mode="strict"))
        self.assertTrue(Grader.match_short_answer("HTTPERR", "HTTPERR", grading_mode="strict"))
        # 양끝 불필요한 공백 trim 허용
        self.assertTrue(Grader.match_short_answer("  /proc  ", "/proc", grading_mode="strict"))
        self.assertTrue(Grader.match_short_answer("  chmod 644  ", "chmod 644", grading_mode="strict"))

    def test_3_strict_case_sensitive_and_different_paths_wrong(self):
        """3. strict에서 대소문자 차이 및 다른 경로 오답 처리 검증"""
        # /PROC != /proc -> 오답 (strict 기본 대소문자 보존)
        self.assertFalse(Grader.match_short_answer("/PROC", "/proc", grading_mode="strict"))
        self.assertFalse(Grader.match_short_answer("ROBOTS.TXT", "robots.txt", grading_mode="strict"))
        # /etc/passwd vs /etc/shadow -> 오답
        self.assertFalse(Grader.match_short_answer("/etc/shadow", "/etc/passwd", grading_mode="strict"))
        self.assertFalse(Grader.match_short_answer("/sys", "/proc", grading_mode="strict"))
        self.assertFalse(Grader.match_short_answer("IIS", "HTTPERR", grading_mode="strict"))

    def test_4_strict_different_commands_and_settings_wrong(self):
        """4. strict에서 다른 명령어/설정값 오답 처리 검증"""
        # chmod 644 != chmod 755 -> 오답
        self.assertFalse(Grader.match_short_answer("chmod 755", "chmod 644", grading_mode="strict"))
        # chmod 644 != chmod644 -> 오답 (내부 공백 보존)
        self.assertFalse(Grader.match_short_answer("chmod644", "chmod 644", grading_mode="strict"))
        # / proc != /proc -> 오답 (내부 공백 보존)
        self.assertFalse(Grader.match_short_answer("/ proc", "/proc", grading_mode="strict"))
        self.assertFalse(Grader.match_short_answer("robots . txt", "robots.txt", grading_mode="strict"))
        # 설정 키워드 불일치
        self.assertFalse(Grader.match_short_answer("session", "auth", grading_mode="strict"))

    def test_4_1_strict_optional_case_sensitive_support(self):
        """4-1. strict 모드에서 명시적 case_sensitive=False 옵션 지원 검증"""
        # 문제에 case_sensitive=False 명시 시 strict에서도 대소문자 허용 가능
        self.assertTrue(Grader.match_short_answer("/PROC", "/proc", grading_mode="strict", case_sensitive=False))
        self.assertTrue(Grader.match_short_answer("httperr", "HTTPERR", grading_mode="strict", case_sensitive=False))
        # 하지만 내부 공백은 여전히 엄격 보존
        self.assertFalse(Grader.match_short_answer("/ proc", "/proc", grading_mode="strict", case_sensitive=False))

    def test_5_accepted_answers_with_grading_modes(self):
        """5. accepted_answers와 grading_mode 조합 검증 (XSS, /robots.txt 등)"""
        # normalized에서 동의어/약어 매칭
        accepted_xss = ["Cross-Site Scripting", "XSS"]
        self.assertTrue(Grader.match_short_answer("XSS", "Cross Site Scripting", accepted=accepted_xss, grading_mode="normalized"))
        self.assertTrue(Grader.match_short_answer("Cross-Site Scripting", "Cross Site Scripting", accepted=accepted_xss, grading_mode="normalized"))
        self.assertTrue(Grader.match_short_answer("cross site scripting", "Cross Site Scripting", accepted=accepted_xss, grading_mode="normalized"))

        # strict에서 accepted_answers 매칭
        accepted_robots = ["/robots.txt"]
        self.assertTrue(Grader.match_short_answer("/robots.txt", "robots.txt", accepted=accepted_robots, grading_mode="strict"))
        self.assertTrue(Grader.match_short_answer("robots.txt", "robots.txt", accepted=accepted_robots, grading_mode="strict"))
        self.assertFalse(Grader.match_short_answer("robots.html", "robots.txt", accepted=accepted_robots, grading_mode="strict"))

    def test_6_backward_compatibility_without_grading_mode(self):
        """6. grading_mode가 없는 기존 문제의 하위 호환 검증 (기본값 normalized 동작)"""
        q_legacy = {
            "id": "Q-LEGACY-01",
            "type": "short",
            "score": 3,
            "answer": "위험 식별"
            # grading_mode 필드 누락
        }
        # grading_mode가 없어도 normalized로 자동 폴백되어 띄어쓰기 유연성 적용
        res = Grader.grade_short_question(q_legacy, "위험식별")
        self.assertEqual(res["earned_score"], 3.0)
        self.assertTrue(res["is_correct"])

    def test_7_normalized_categories_in_questions_and_concepts(self):
        """7. Category 값이 정규화된 5대 허용 목록 안에 존재하는지 전수 검증"""
        ALLOWED_CATEGORIES = {
            "시스템 보안",
            "네트워크 보안",
            "애플리케이션 보안",
            "정보보안 일반 및 암호학",
            "정보보호 관리 및 법규"
        }

        questions = self.loader.load_questions()
        concepts = self.loader.load_concepts()

        for q in questions:
            self.assertIn(q["category"], ALLOWED_CATEGORIES, f"문제 {q['id']}의 category '{q['category']}'는 표준 목록에 없습니다.")

        for c in concepts:
            self.assertIn(c["category"], ALLOWED_CATEGORIES, f"개념 {c['id']}의 category '{c['category']}'는 표준 목록에 없습니다.")

    def test_8_existing_18_questions_total_score_100(self):
        """8. 기존 18문제 총점 100점 및 만점 구조 불변 검증"""
        exam_service = ExamService(self.loader)
        exam_qs = exam_service.get_exam_questions(mode="standard")
        self.assertEqual(len(exam_qs), 18)

        short_qs = [q for q in exam_qs if q["type"] == "short"]
        desc_qs = [q for q in exam_qs if q["type"] == "descriptive"]
        prac_qs = [q for q in exam_qs if q["type"] == "practical"]

        self.assertEqual(len(short_qs), 12)
        self.assertEqual(sum(q["score"] for q in short_qs), 36)

        self.assertEqual(len(desc_qs), 4)
        self.assertEqual(sum(q["score"] for q in desc_qs), 48)

        self.assertEqual(len(prac_qs), 2)
        self.assertTrue(all(q["score"] == 16 for q in prac_qs))

        # 36 + 48 + 16 = 100점
        self.assertEqual(36 + 48 + 16, 100)

    def test_9_sources_and_concepts_referential_integrity(self):
        """9. Source/Concept 참조 무결성 유지 검증"""
        questions = self.loader.load_questions()
        sources_dict = self.loader.get_sources_dict()
        concepts_dict = {c["id"]: c for c in self.loader.load_concepts()}

        for q in questions:
            self.assertIn(q["source_id"], sources_dict, f"문제 {q['id']}의 source_id 유효성 검증 실패")
            self.assertIn(q["concept_id"], concepts_dict, f"문제 {q['id']}의 concept_id 유효성 검증 실패")

if __name__ == "__main__":
    unittest.main()
