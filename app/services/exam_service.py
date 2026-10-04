from typing import Dict, List, Any, Optional
from app.services.data_loader import DataLoader
from app.services.grader import Grader
from app.services.exam_generator import ExamGenerator

class ExamService:
    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.data_loader = data_loader or DataLoader()

    def get_exam_questions(self, mode: str = "standard", seed: Optional[int] = None, is_owner: bool = True) -> List[Dict[str, Any]]:
        """시험 응시용 문항 목록 (mode: 'standard' | 'random' | 'wrong_review' | 'adaptive', seed: Optional[int])"""
        all_qs = self.data_loader.get_enriched_questions()
        
        extra_kwargs = {}
        if mode == "wrong_review":
            if is_owner:
                from app.services.wrong_answer_service import WrongAnswerService
                wrong_service = WrongAnswerService(self.data_loader)
                wrong_qs = wrong_service.get_wrong_questions(is_owner=True)
                extra_kwargs["wrong_question_ids"] = [q["question_id"] for q in wrong_qs]
            else:
                extra_kwargs["wrong_question_ids"] = []
        elif mode == "adaptive":
            if is_owner:
                from app.services.analytics_service import AnalyticsService
                analytics_service = AnalyticsService(self.data_loader)
                top_vuln = analytics_service.get_top_vulnerable_concepts(limit=5, is_owner=True)
                extra_kwargs["vulnerable_concept_ids"] = [c["concept_id"] for c in top_vuln]
            else:
                extra_kwargs["vulnerable_concept_ids"] = []

        return ExamGenerator.generate_exam_set(all_qs, mode=mode, seed=seed, **extra_kwargs)

    def parse_submission(self, form_data: Dict[str, Any], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        웹 폼(POST) 데이터에서 answers 딕셔너리와 selected_practical_id를 파싱
        """
        selected_practical_id = form_data.get("selected_practical_id", "").strip()
        answers: Dict[str, Any] = {}

        for q in questions:
            q_id = q["id"]
            q_type = q["type"]

            if q_type == "short":
                sub_qs = q.get("sub_questions")
                if sub_qs:
                    sub_dict = {}
                    for sub in sub_qs:
                        label = sub.get("label")
                        field_name = f"ans_{q_id}_{label}"
                        sub_dict[label] = form_data.get(field_name, "").strip()
                    answers[q_id] = sub_dict
                else:
                    field_name = f"ans_{q_id}"
                    answers[q_id] = form_data.get(field_name, "").strip()

            elif q_type in ("descriptive", "practical"):
                sub_qs = q.get("sub_questions", [])
                sub_dict = {}
                for sub in sub_qs:
                    sub_id = str(sub.get("sub_id"))
                    field_name = f"ans_{q_id}_{sub_id}"
                    sub_dict[sub_id] = form_data.get(field_name, "").strip()
                answers[q_id] = sub_dict

        return {
            "selected_practical_id": selected_practical_id,
            "answers": answers
        }

    def get_questions_by_ids(self, q_ids: List[str]) -> List[Dict[str, Any]]:
        """ID 목록에 해당하는 문항 객체들을 순서대로 반환"""
        all_qs = self.data_loader.get_enriched_questions()
        all_qs_dict = {q["id"]: q for q in all_qs}
        return [all_qs_dict[qid] for qid in q_ids if qid in all_qs_dict]

    def resolve_submitted_questions(self, form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """폼 데이터에 포함된 question_ids로부터 시험 문항 세트 복원 (없으면 standard 모드)"""
        q_ids_raw = form_data.get("question_ids", "").strip()
        if q_ids_raw:
            q_ids = [qid.strip() for qid in q_ids_raw.split(",") if qid.strip()]
            resolved = self.get_questions_by_ids(q_ids)
            if len(resolved) == 18:
                return resolved
        return self.get_exam_questions(mode="standard")

    def grade_exam(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """폼 데이터를 받아 채점 수행 후 종합 결과 반환"""
        questions = self.resolve_submitted_questions(form_data)
        submission = self.parse_submission(form_data, questions)
        return Grader.grade_full_exam(questions, submission)

    @staticmethod
    def calculate_question_status(question: Dict[str, Any], q_ans: Any, is_selected_practical: bool) -> Dict[str, Any]:
        """
        답안 작성 상태 판정 (표시 계층용)
        1. 답안을 하나도 작성하지 않은 경우 -> '미작성'
        2. 복수 답안/소문항 중 일부만 작성한 경우 -> '일부 작성 (작성 수/전체 수)'
        3. 모든 입력란을 작성한 경우 -> '작성 완료'
        4. 실무형에서 사용자가 선택한 문제:
           - 답안 없음 -> '선택됨 · 미작성'
           - 일부 작성 -> '선택됨 · 일부 작성 (작성 수/전체 수)'
           - 모두 작성 -> '선택됨 · 작성 완료'
        5. 선택하지 않은 실무형 문제 -> '미선택 · 채점 제외'
        """
        q_type = question.get("type")

        # 1. total_count 및 filled_count 계산
        if q_type == "short":
            sub_qs = question.get("sub_questions")
            if sub_qs:
                total_count = len(sub_qs)
                user_dict = q_ans if isinstance(q_ans, dict) else {}
                filled_count = sum(1 for sub in sub_qs if str(user_dict.get(sub.get("label"), "")).strip())
            else:
                total_count = 1
                val = str(q_ans).strip() if q_ans is not None else ""
                filled_count = 1 if val else 0
        elif q_type in ("descriptive", "practical"):
            sub_qs = question.get("sub_questions", [])
            total_count = len(sub_qs) if sub_qs else 1
            user_dict = q_ans if isinstance(q_ans, dict) else {}
            filled_count = sum(1 for sub in sub_qs if str(user_dict.get(str(sub.get("sub_id")), "")).strip())
        else:
            total_count = 1
            filled_count = 1 if str(q_ans or "").strip() else 0

        # 2. 상태 결정
        if q_type == "practical":
            if not is_selected_practical:
                return {
                    "status_text": "미선택 · 채점 제외",
                    "status_code": "unselected",
                    "filled_count": filled_count,
                    "total_count": total_count,
                    "is_filled": False,
                    "is_complete": False
                }
            else:
                if filled_count == 0:
                    status_text = "선택됨 · 미작성"
                    status_code = "empty"
                elif filled_count < total_count:
                    status_text = f"선택됨 · 일부 작성 ({filled_count}/{total_count})"
                    status_code = "partial"
                else:
                    status_text = "선택됨 · 작성 완료"
                    status_code = "complete"

                return {
                    "status_text": status_text,
                    "status_code": status_code,
                    "filled_count": filled_count,
                    "total_count": total_count,
                    "is_filled": (filled_count > 0),
                    "is_complete": (filled_count == total_count)
                }

        # 일반 문항 (단답형, 서술형)
        if filled_count == 0:
            status_text = "미작성"
            status_code = "empty"
        elif filled_count < total_count:
            status_text = f"일부 작성 ({filled_count}/{total_count})"
            status_code = "partial"
        else:
            status_text = "작성 완료"
            status_code = "complete"

        return {
            "status_text": status_text,
            "status_code": status_code,
            "filled_count": filled_count,
            "total_count": total_count,
            "is_filled": (filled_count > 0),
            "is_complete": (filled_count == total_count)
        }
