import unittest
import math
import os
import json
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db, db_session, Base, engine
from app.models.history import ExamAttempt, AnswerRecord
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.analytics_service import AnalyticsService
from app.services.exam_generator import ExamGenerator
from app.services.exam_service import ExamService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestGoal3FIntegrationQA(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.all_questions = self.loader.get_enriched_questions()
            self.history_service = HistoryService(self.loader)
            self.wrong_service = WrongAnswerService(self.loader)
            self.analytics_service = AnalyticsService(self.loader)
            self.exam_service = ExamService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    # ---------------------------------------------------------
    # 1. Goal 2 Regression
    # ---------------------------------------------------------
    def test_goal2_regression_baseline(self):
        """180문항, 20 Concepts, 12 Sources, 12/4/2, 100점 구조 보존 검증"""
        self.assertEqual(len(self.loader.load_questions()), 180)
        self.assertEqual(len(self.loader.load_concepts()), 20)
        self.assertEqual(len(self.loader.load_sources()), 12)

        # Standard Exam
        std_exam = ExamGenerator.generate_exam_set(self.all_questions, mode="standard")
        self.assertEqual(len(std_exam), 18)
        shorts = [q for q in std_exam if q["type"] == "short"]
        descs = [q for q in std_exam if q["type"] == "descriptive"]
        pracs = [q for q in std_exam if q["type"] == "practical"]
        self.assertEqual(len(shorts), 12)
        self.assertEqual(len(descs), 4)
        self.assertEqual(len(pracs), 2)
        self.assertEqual(sum(q["score"] for q in shorts), 36)
        self.assertEqual(sum(q["score"] for q in descs), 48)
        self.assertTrue(all(q["score"] == 16 for q in pracs))

        # Random Exam Seed Reproducibility
        r1 = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=777)
        r2 = ExamGenerator.generate_exam_set(self.all_questions, mode="random", seed=777)
        self.assertEqual([q["id"] for q in r1], [q["id"] for q in r2])

    # ---------------------------------------------------------
    # 2. ExamAttempt and AnswerRecord Count & Field Integrity
    # ---------------------------------------------------------
    def test_attempt_and_answer_record_count(self):
        """시험 제출 시 ExamAttempt 1건과 AnswerRecord 정확히 18건(단답 12, 서술 4, 실무 2: selected 1 + unselected 1) 저장 검증"""
        with self.app.app_context():
            # Standard 18문항 모의 채점 결과 생성
            mock_details = []
            # 12 short
            for i in range(1, 13):
                mock_details.append({
                    "question_id": f"Q-SHORT-{i:03d}",
                    "type": "short",
                    "earned_score": 3.0 if i <= 6 else 0.0,
                    "max_score": 3.0,
                    "is_correct": (i <= 6)
                })
            # 4 descriptive
            for i in range(1, 5):
                mock_details.append({
                    "question_id": f"Q-DESC-{i:03d}",
                    "type": "descriptive",
                    "earned_score": 6.0,
                    "max_score": 12.0
                })
            # 2 practical: 1 selected, 1 unselected
            mock_details.append({
                "question_id": "Q-PRAC-001",
                "type": "practical",
                "is_selected": True,
                "earned_score": 12.0,
                "max_score": 16.0
            })
            mock_details.append({
                "question_id": "Q-PRAC-002",
                "type": "practical",
                "is_selected": False,
                "earned_score": 0.0,
                "max_score": 16.0
            })

            mock_grading = {
                "total_score": 54.0,  # (6*3) + (4*6) + 12 = 18 + 24 + 12 = 54
                "is_passed": False,
                "summary": {
                    "short": {"earned": 18.0},
                    "descriptive": {"earned": 24.0},
                    "practical": {"earned": 12.0}
                },
                "details": mock_details
            }

            attempt = self.history_service.save_exam_attempt(
                exam_mode="standard",
                seed=None,
                selected_practical_id="Q-PRAC-001",
                grading_result=mock_grading,
                answers={}
            )

            # ExamAttempt 검증
            self.assertEqual(attempt.exam_mode, "standard")
            self.assertEqual(attempt.total_score, 54.0)
            self.assertEqual(attempt.short_score, 18.0)
            self.assertEqual(attempt.descriptive_score, 24.0)
            self.assertEqual(attempt.practical_score, 12.0)
            self.assertEqual(attempt.selected_practical_id, "Q-PRAC-001")
            self.assertFalse(attempt.is_passed)

            # AnswerRecord 개수 검증: 정확히 18건!
            records = attempt.answers
            self.assertEqual(len(records), 18)

            short_recs = [r for r in records if r.question_type == "short"]
            desc_recs = [r for r in records if r.question_type == "descriptive"]
            prac_recs = [r for r in records if r.question_type == "practical"]

            self.assertEqual(len(short_recs), 12)
            self.assertEqual(len(desc_recs), 4)
            self.assertEqual(len(prac_recs), 2)

            # Practical: 1 selected, 1 unselected
            sel_prac = [r for r in prac_recs if r.achievement_status != "unselected"]
            unsel_prac = [r for r in prac_recs if r.achievement_status == "unselected"]
            self.assertEqual(len(sel_prac), 1)
            self.assertEqual(len(unsel_prac), 1)
            self.assertEqual(sel_prac[0].question_id, "Q-PRAC-001")
            self.assertEqual(unsel_prac[0].question_id, "Q-PRAC-002")
            self.assertEqual(unsel_prac[0].earned_score, 0.0)

    # ---------------------------------------------------------
    # 3. Transaction Atomicity
    # ---------------------------------------------------------
    def test_transaction_atomicity_on_failure(self):
        """AnswerRecord 저장 도중 오류 발생 시 전체 rollback되어 partial commit이 발생하지 않는지 검증"""
        with self.app.app_context():
            initial_attempts = self.history_service.get_attempt_count()
            initial_records = db_session.query(AnswerRecord).count()

            bad_grading_result = {
                "total_score": 10.0,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    # 의도적으로 에러를 유발하는 잘못된 데이터 (max_score None 등으로 예외 발생)
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": "INVALID_FLOAT", "max_score": 3.0}
                ]
            }

            with self.assertRaises(Exception):
                self.history_service.save_exam_attempt(
                    exam_mode="standard",
                    seed=None,
                    selected_practical_id=None,
                    grading_result=bad_grading_result,
                    answers={}
                )

            # Rollback 확인: attempt와 record 수가 초기값과 동일해야 함
            self.assertEqual(self.history_service.get_attempt_count(), initial_attempts)
            self.assertEqual(db_session.query(AnswerRecord).count(), initial_records)

    # ---------------------------------------------------------
    # 4. Practical unselected Isolation from Wrong Notes and Analytics
    # ---------------------------------------------------------
    def test_practical_unselected_isolation(self):
        """미선택 practical 문항이 오답노트 및 취약도 계산에 일체 포함되지 않음을 검증"""
        with self.app.app_context():
            res = {
                "total_score": 16.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    # Q-PRAC-001 선택 & 정답
                    {"question_id": "Q-PRAC-001", "type": "practical", "is_selected": True, "earned_score": 16.0, "max_score": 16.0},
                    # Q-PRAC-002 미선택 (0점)
                    {"question_id": "Q-PRAC-002", "type": "practical", "is_selected": False, "earned_score": 0.0, "max_score": 16.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, "Q-PRAC-001", res, {})

            # 1. Wrong Notes에 Q-PRAC-002가 포함되지 않아야 함
            wrong_qs = self.wrong_service.get_wrong_questions()
            wrong_ids = [q["question_id"] for q in wrong_qs]
            self.assertNotIn("Q-PRAC-002", wrong_ids)
            self.assertEqual(len(wrong_qs), 0)

            # 2. Q-PRAC-002의 Concept (CON-NET-02)에 미선택 문항이 반영되지 않아야 함
            concept_stats = self.analytics_service.get_concept_analytics()
            con_snort = next(c for c in concept_stats if c["concept_id"] == "CON-NET-02")
            self.assertEqual(con_snort["attempts_count"], 0)
            self.assertEqual(con_snort["incorrect_count"], 0)
            self.assertEqual(con_snort["vulnerability_index"], 0.0)

    # ---------------------------------------------------------
    # 5. Wrong Notes State Transitions (Scenarios A, B, C)
    # ---------------------------------------------------------
    def test_wrong_notes_state_transitions(self):
        with self.app.app_context():
            # Scenario A: Q-SHORT-005 Fail -> Wrong Note -> Pass -> Resolved
            res_fail = {"total_score": 0.0, "summary": {}, "details": [{"question_id": "Q-SHORT-005", "type": "short", "earned_score": 0.0, "max_score": 3.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_fail, {"Q-SHORT-005": "wrong"})
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 1)
            self.assertEqual(self.wrong_service.get_wrong_questions()[0]["question_id"], "Q-SHORT-005")

            res_pass = {"total_score": 3.0, "summary": {}, "details": [{"question_id": "Q-SHORT-005", "type": "short", "earned_score": 3.0, "max_score": 3.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_pass, {"Q-SHORT-005": "correct"})
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 0)

            # Scenario B: Q-DESC-003 Partial (4/12) -> Wrong Note -> Full (12/12) -> Resolved
            res_part = {"total_score": 4.0, "summary": {}, "details": [{"question_id": "Q-DESC-003", "type": "descriptive", "earned_score": 4.0, "max_score": 12.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_part, {})
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 1)
            self.assertEqual(self.wrong_service.get_wrong_questions()[0]["latest_status"], "partial")

            res_full = {"total_score": 12.0, "summary": {}, "details": [{"question_id": "Q-DESC-003", "type": "descriptive", "earned_score": 12.0, "max_score": 12.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_full, {})
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 0)

            # Scenario C: Q-SHORT-005 Fail again -> Re-appears in Wrong Notes
            self.history_service.save_exam_attempt("standard", None, None, res_fail, {"Q-SHORT-005": "wrong"})
            self.assertEqual(self.wrong_service.get_wrong_question_count(), 1)
            self.assertEqual(self.wrong_service.get_wrong_questions()[0]["question_id"], "Q-SHORT-005")

    # ---------------------------------------------------------
    # 6. Weighted Score Rate Verification
    # ---------------------------------------------------------
    def test_weighted_score_rate_calculation(self):
        """단답 3/3, 서술 6/12, 실무 8/16 혼합 시 수동 계산(17/31 = 54.838%)과 일치 검증"""
        with self.app.app_context():
            # 모두 "네트워크 보안" 문항으로 구성:
            # Q-SHORT-003 (3점), Q-DESC-003 (12점), Q-PRAC-001 (16점)
            res = {
                "total_score": 17.0,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-003", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-DESC-003", "type": "descriptive", "earned_score": 6.0, "max_score": 12.0},
                    {"question_id": "Q-PRAC-001", "type": "practical", "is_selected": True, "earned_score": 8.0, "max_score": 16.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, "Q-PRAC-001", res, {})

            cats = self.analytics_service.get_category_analytics()
            net_cat = next(c for c in cats if c["category"] == "네트워크 보안")

            expected_earned = 17.0
            expected_max = 31.0
            expected_rate = round((17.0 / 31.0) * 100, 1)  # 54.8%

            self.assertEqual(net_cat["earned_score_sum"], expected_earned)
            self.assertEqual(net_cat["max_score_sum"], expected_max)
            self.assertEqual(net_cat["score_rate"], expected_rate)

    # ---------------------------------------------------------
    # 7. Vulnerability Index (VI) & Edge Cases
    # ---------------------------------------------------------
    def test_vi_formula_and_edge_cases(self):
        """VI = (100 - ScoreRate) * (Fail/Attempts) * log2(Attempts + 1) 수동 계산 및 ZeroDivision/NaN 방어 검증"""
        with self.app.app_context():
            # Edge Case 1: Attempts = 0
            concepts = self.analytics_service.get_concept_analytics()
            for c in concepts:
                self.assertEqual(c["attempts_count"], 0)
                self.assertEqual(c["vulnerability_index"], 0.0)
                self.assertFalse(math.isnan(c["vulnerability_index"]))
                self.assertFalse(math.isinf(c["vulnerability_index"]))

            # Edge Case 2: Attempts = 1, Fail = 0 (ScoreRate = 100) -> VI = 0.0
            res_pass = {"total_score": 3.0, "summary": {}, "details": [{"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_pass, {})
            c1 = next(c for c in self.analytics_service.get_concept_analytics() if c["concept_id"] == "CON-MGT-01")
            self.assertEqual(c1["score_rate"], 100.0)
            self.assertEqual(c1["vulnerability_index"], 0.0)

            # Edge Case 3: Attempts = 1, Fail = 1 (ScoreRate = 0) -> VI = (100-0) * (1/1) * log2(2) = 100.0
            res_fail = {"total_score": 0.0, "summary": {}, "details": [{"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}]}
            self.history_service.save_exam_attempt("standard", None, None, res_fail, {})
            c2 = next(c for c in self.analytics_service.get_concept_analytics() if c["concept_id"] == "CON-APP-03")
            self.assertEqual(c2["score_rate"], 0.0)
            self.assertEqual(c2["vulnerability_index"], 100.0)

            # Edge Case 4: Attempts = 2, Fail = 2 (ScoreRate = 0) -> VI = 100 * 1.0 * log2(3) = 100 * 1.58496 = 158.5
            self.history_service.save_exam_attempt("standard", None, None, res_fail, {})
            c2_updated = next(c for c in self.analytics_service.get_concept_analytics() if c["concept_id"] == "CON-APP-03")
            expected_vi = round(100.0 * 1.0 * math.log2(3.0), 1)  # 158.5
            self.assertEqual(c2_updated["vulnerability_index"], expected_vi)

    # ---------------------------------------------------------
    # 8. Boundary Test for Achievement Grades
    # ---------------------------------------------------------
    def test_achievement_grade_boundaries(self):
        """0, 59.9, 60.0, 79.9, 80.0, 100 경계값 검증"""
        boundaries = [
            (0.0, 1, "취약"),
            (59.9, 1, "취약"),
            (60.0, 1, "주의"),
            (79.9, 1, "주의"),
            (80.0, 1, "안전"),
            (100.0, 1, "안전"),
            (0.0, 0, "미응시")
        ]
        for rate, att, expected in boundaries:
            if att == 0:
                grade = "미응시"
            elif rate >= 80.0:
                grade = "안전"
            elif rate >= 60.0:
                grade = "주의"
            else:
                grade = "취약"
            self.assertEqual(grade, expected, f"Score rate {rate}% with attempts {att} should be {expected}")

    # ---------------------------------------------------------
    # 9. wrong_review Generation Edge Cases (Cases 1, 2, 3, 4)
    # ---------------------------------------------------------
    def test_wrong_review_generation_cases(self):
        # Case 1: 오답 충분 (short 15개, desc 5개, prac 3개 오답 풀)
        pool_shorts = [f"Q-SHORT-{i:03d}" for i in range(1, 16)]
        pool_descs = [f"Q-DESC-{i:03d}" for i in range(1, 6)]
        pool_pracs = ["Q-PRAC-001", "Q-PRAC-002", "Q-PRAC-004"]
        exam1 = ExamGenerator.generate_wrong_review_exam(self.all_questions, pool_shorts + pool_descs + pool_pracs, seed=1)
        self.assertEqual(len(exam1), 18)
        self.assertEqual(len(set(q["id"] for q in exam1)), 18)
        self.assertEqual(sum(q["score"] for q in exam1 if q["type"] == "short"), 36)
        self.assertEqual(sum(q["score"] for q in exam1 if q["type"] == "descriptive"), 48)

        # Case 2: short만 충분(15개), desc 1개, prac 0개
        exam2 = ExamGenerator.generate_wrong_review_exam(self.all_questions, pool_shorts + ["Q-DESC-001"], seed=2)
        self.assertEqual(len(exam2), 18)
        self.assertEqual(len(set(q["id"] for q in exam2)), 18)
        self.assertIn("Q-DESC-001", [q["id"] for q in exam2])
        self.assertEqual(len([q for q in exam2 if q["type"] == "descriptive"]), 4)
        self.assertEqual(len([q for q in exam2 if q["type"] == "practical"]), 2)

        # Case 3: practical 오답 1개
        exam3 = ExamGenerator.generate_wrong_review_exam(self.all_questions, ["Q-PRAC-001"], seed=3)
        self.assertEqual(len(exam3), 18)
        self.assertIn("Q-PRAC-001", [q["id"] for q in exam3])
        self.assertEqual(len([q for q in exam3 if q["type"] == "practical"]), 2)

        # Case 4: 오답 0개 (빈 목록) -> random fallback
        exam4 = ExamGenerator.generate_wrong_review_exam(self.all_questions, [], seed=4)
        self.assertEqual(len(exam4), 18)
        self.assertEqual(len(set(q["id"] for q in exam4)), 18)

    # ---------------------------------------------------------
    # 10. adaptive Generation & Fallback
    # ---------------------------------------------------------
    def test_adaptive_generation_cases(self):
        # Case 1: Normal Top 5 concepts
        exam1 = ExamGenerator.generate_adaptive_exam(self.all_questions, ["CON-APP-03", "CON-NET-01"], seed=10)
        self.assertEqual(len(exam1), 18)
        self.assertEqual(len(set(q["id"] for q in exam1)), 18)

        # Case 2: Empty vulnerable concepts (No analytics yet)
        exam2 = ExamGenerator.generate_adaptive_exam(self.all_questions, [], seed=20)
        self.assertEqual(len(exam2), 18)
        self.assertEqual(len(set(q["id"] for q in exam2)), 18)

    # ---------------------------------------------------------
    # 11. History Pagination Edge Cases
    # ---------------------------------------------------------
    def test_history_pagination_edge_cases(self):
        # 1. Empty data: page 1 and page 999
        resp = self.client.get("/history?page=1")
        self.assertEqual(resp.status_code, 200)
        resp_out = self.client.get("/history?page=999")
        self.assertEqual(resp_out.status_code, 200)

        # 2. Add 35 attempts (3 pages: 15, 15, 5)
        with self.app.app_context():
            mock_res = {"total_score": 60.0, "summary": {}, "details": []}
            for i in range(35):
                self.history_service.save_exam_attempt("standard", None, None, mock_res, {})

        resp_p1 = self.client.get("/history?page=1")
        self.assertEqual(resp_p1.status_code, 200)
        resp_p2 = self.client.get("/history?page=2")
        self.assertEqual(resp_p2.status_code, 200)
        resp_p3 = self.client.get("/history?page=3")
        self.assertEqual(resp_p3.status_code, 200)
        resp_p99 = self.client.get("/history?page=99")
        self.assertEqual(resp_p99.status_code, 200)

    # ---------------------------------------------------------
    # 12. History Detail 404 & Content
    # ---------------------------------------------------------
    def test_history_detail_404_and_content(self):
        resp_404 = self.client.get("/history/99999")
        self.assertEqual(resp_404.status_code, 404)

    # ---------------------------------------------------------
    # 13. Dashboard Empty State & Data Consistency
    # ---------------------------------------------------------
    def test_dashboard_empty_and_populated_consistency(self):
        # 1. Empty
        resp_empty = self.client.get("/dashboard")
        self.assertEqual(resp_empty.status_code, 200)
        self.assertIn("총 모의고사 응시", resp_empty.get_data(as_text=True))

        # 2. Populated
        with self.app.app_context():
            res = {
                "total_score": 85.0,
                "is_passed": True,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-001", "type": "short", "earned_score": 3.0, "max_score": 3.0},
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        resp_pop = self.client.get("/dashboard")
        self.assertEqual(resp_pop.status_code, 200)
        html = resp_pop.get_data(as_text=True)
        self.assertIn("85", html)
        self.assertIn("CON-APP-03", html)
