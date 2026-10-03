import unittest
import json
import re
from app import create_app
from app.config import Config
from app.models.database import init_db, close_db
from app.services.data_loader import DataLoader
from app.services.history_service import HistoryService
from app.services.wrong_answer_service import WrongAnswerService
from app.services.analytics_service import AnalyticsService

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class TestE2EScenarios(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db(self.app, uri="sqlite:///:memory:")
            self.loader = DataLoader(self.app.config["DATA_DIR"])
            self.history_service = HistoryService(self.loader)
            self.wrong_service = WrongAnswerService(self.loader)
            self.analytics_service = AnalyticsService(self.loader)

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def test_e2e_scenario_1_full_lifecycle(self):
        """Scenario 1: 홈 -> 시험응시 -> 제출 -> 결과 -> 이력목록 -> 상세복기 -> 오답노트 -> 대시보드"""
        # 1. 홈 진입
        r_home = self.client.get("/")
        self.assertEqual(r_home.status_code, 200)

        # 2. 랜덤 시험 시작
        r_exam = self.client.get("/exam?mode=random&seed=101")
        self.assertEqual(r_exam.status_code, 200)
        exam_html = r_exam.get_data(as_text=True)
        m = re.search(r'name="question_ids" value="([^"]+)"', exam_html)
        self.assertTrue(m, "question_ids hidden input must be present")
        q_ids = m.group(1).split(",")
        self.assertEqual(len(q_ids), 18)

        # 3. 답안 작성 및 제출 (Q-SHORT-001 정답, Q-SHORT-002 오답)
        first_short = [qid for qid in q_ids if "SHORT" in qid][0]
        second_short = [qid for qid in q_ids if "SHORT" in qid][1]
        first_prac = [qid for qid in q_ids if "PRAC" in qid][0]

        post_data = {
            "exam_mode": "random",
            "exam_seed": "101",
            "question_ids": ",".join(q_ids),
            "selected_practical_id": first_prac,
            f"ans_{first_short}": "intentional_fail_for_qa"
        }
        r_submit = self.client.post("/submit", data=post_data, follow_redirects=True)
        self.assertEqual(r_submit.status_code, 200)
        submit_html = r_submit.get_data(as_text=True)
        self.assertIn("성공적으로 저장되었습니다", submit_html)
        att_match = re.search(r'회차 #(\d+)', submit_html)
        self.assertTrue(att_match)
        att_id = int(att_match.group(1))

        # 4. 이력 목록 확인
        r_history = self.client.get("/history")
        self.assertEqual(r_history.status_code, 200)
        self.assertIn(f"#{att_id}", r_history.get_data(as_text=True))

        # 5. 상세 복기 확인
        r_detail = self.client.get(f"/history/{att_id}")
        self.assertEqual(r_detail.status_code, 200)
        detail_html = r_detail.get_data(as_text=True)
        self.assertIn("복기 리포트", detail_html)
        self.assertIn(first_short, detail_html)

        # 6. 오답노트 확인
        r_wrong = self.client.get("/wrong-notes")
        self.assertEqual(r_wrong.status_code, 200)
        wrong_html = r_wrong.get_data(as_text=True)
        self.assertIn(first_short, wrong_html)

        # 7. 대시보드 확인
        r_dash = self.client.get("/dashboard")
        self.assertEqual(r_dash.status_code, 200)
        dash_html = r_dash.get_data(as_text=True)
        self.assertIn("개인 학습현황", dash_html)
        self.assertIn("총 모의고사 응시", dash_html)

    def test_e2e_scenario_2_wrong_review_and_resolution(self):
        """Scenario 2: 오답노트 -> wrong_review 응시 -> 재응시 정답 -> 오답노트 자동 해소 -> 대시보드 갱신"""
        with self.app.app_context():
            # 초기 오답 생성: Q-SHORT-005
            res_fail = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-005", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res_fail, {"Q-SHORT-005": "wrong"})

        # 오답노트에 존재 확인
        r_w1 = self.client.get("/wrong-notes")
        self.assertIn("Q-SHORT-005", r_w1.get_data(as_text=True))

        # wrong_review 시험 생성 확인
        r_exam = self.client.get("/exam?mode=wrong_review")
        self.assertEqual(r_exam.status_code, 200)
        self.assertIn("Q-SHORT-005", r_exam.get_data(as_text=True))

        with self.app.app_context():
            # 재응시에서 Q-SHORT-005 정답 맞춤
            res_pass = {
                "total_score": 3.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-005", "type": "short", "earned_score": 3.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("wrong_review", None, None, res_pass, {"Q-SHORT-005": "correct"})

        # 오답노트 자동 해소 확인
        r_w2 = self.client.get("/wrong-notes")
        self.assertIn("미해결 오답: 0문항", r_w2.get_data(as_text=True))

        # 대시보드에서도 오답 0문항 확인
        r_dash = self.client.get("/dashboard")
        self.assertIn("0", r_dash.get_data(as_text=True))

    def test_e2e_scenario_3_adaptive_exam_and_concept_clinic(self):
        """Scenario 3: 대시보드 -> adaptive 시험 응시 -> 개념 통계 반영"""
        with self.app.app_context():
            # CON-APP-03 (Q-SHORT-002) 오답 등록
            res = {
                "total_score": 0.0,
                "is_passed": False,
                "summary": {},
                "details": [
                    {"question_id": "Q-SHORT-002", "type": "short", "earned_score": 0.0, "max_score": 3.0}
                ]
            }
            self.history_service.save_exam_attempt("standard", None, None, res, {})

        # 대시보드에서 취약 Concept 확인
        r_dash = self.client.get("/dashboard")
        self.assertEqual(r_dash.status_code, 200)
        self.assertIn("CON-APP-03", r_dash.get_data(as_text=True))

        # adaptive 시험 페이지 진입 확인
        r_adap = self.client.get("/exam?mode=adaptive")
        self.assertEqual(r_adap.status_code, 200)
        self.assertIn("취약 Concept 집중 모의고사", r_adap.get_data(as_text=True))
