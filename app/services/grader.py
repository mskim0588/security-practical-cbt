import re
from typing import Dict, List, Any, Optional, Tuple

class Grader:
    @staticmethod
    def normalize_short_answer(text: str) -> str:
        """단답형 텍스트 정규화 파이프라인"""
        if not text:
            return ""
        # 1. 양끝 공백 제거 및 소문자 변환
        norm = str(text).strip().lower()
        # 2. 유니코드 특수 대시/하이픈 통일
        norm = re.sub(r'[\u2010-\u2015\u2212\uFE58\uFE63\uFF0D]', '-', norm)
        # 3. 연속 공백 단일 공백 치환
        norm = re.sub(r'\s+', ' ', norm)
        # 4. 양끝 따옴표, 괄호, 마침표 제거
        norm = norm.strip(".'\"`")
        return norm

    @classmethod
    def match_short_answer(
        cls,
        user_ans: str,
        expected: str,
        accepted: Optional[List[str]] = None,
        grading_mode: str = "normalized",
        case_sensitive: Optional[bool] = None
    ) -> bool:
        """
        단답형 정답 일치 여부 판정
        - grading_mode: 'normalized' | 'strict'
        - strict 모드 기본: case-sensitive (대소문자 보존)
        - normalized 모드 기본: case-insensitive (대소문자 무시)
        """
        if not user_ans:
            return False

        if grading_mode == "strict":
            # strict 모드 기본 정책: case-sensitive
            is_case_sensitive = True if case_sensitive is None else case_sensitive
            norm_user = str(user_ans).strip()
            if not is_case_sensitive:
                norm_user = norm_user.lower()

            if not norm_user:
                return False

            candidates = [expected] + (accepted or [])
            if is_case_sensitive:
                norm_candidates = [str(c).strip() for c in candidates if c]
            else:
                norm_candidates = [str(c).strip().lower() for c in candidates if c]

            return norm_user in norm_candidates
        else:
            # normalized 모드: 공백 정규화, 유니코드 대시, 띄어쓰기 유연성 매칭 지원
            norm_user = cls.normalize_short_answer(user_ans)
            if not norm_user:
                return False

            candidates = [expected] + (accepted or [])
            norm_candidates = [cls.normalize_short_answer(c) for c in candidates if c]

            # 1차 직접 일치
            if norm_user in norm_candidates:
                return True

            # 2차: 띄어쓰기 완전 제거 비교 (예: "위험 식별" vs "위험식별")
            no_space_user = norm_user.replace(" ", "")
            for c in norm_candidates:
                if no_space_user == c.replace(" ", ""):
                    return True

            return False

    @classmethod
    def grade_short_question(cls, question: Dict[str, Any], user_ans_data: Any) -> Dict[str, Any]:
        """단답형 1문항 채점 (최대 3점, grading_mode 및 case_sensitive 지원)"""
        sub_questions = question.get("sub_questions")
        max_score = question.get("score", 3)
        grading_mode = question.get("grading_mode", "normalized")
        case_sensitive = question.get("case_sensitive")
        earned_score = 0.0
        sub_results = []

        if sub_questions:
            # 괄호 소문항 분할형 (A, B, C 등)
            user_dict = user_ans_data if isinstance(user_ans_data, dict) else {}
            for sub in sub_questions:
                label = sub.get("label")
                sub_score = float(sub.get("score", 1))
                sub_expected = sub.get("answer", "")
                sub_accepted = sub.get("accepted_answers", [])
                sub_case_sens = sub.get("case_sensitive", case_sensitive)

                user_val = str(user_dict.get(label, "")).strip()
                is_correct = cls.match_short_answer(
                    user_val, sub_expected, sub_accepted,
                    grading_mode=grading_mode,
                    case_sensitive=sub_case_sens
                )

                points = sub_score if is_correct else 0.0
                earned_score += points

                sub_results.append({
                    "label": label,
                    "user_answer": user_val,
                    "expected_answer": sub_expected,
                    "accepted_answers": sub_accepted,
                    "is_correct": is_correct,
                    "score": points,
                    "max_score": sub_score
                })
        else:
            # 단일 입력형
            user_val = str(user_ans_data).strip() if user_ans_data else ""
            expected = question.get("answer", "")
            accepted = question.get("accepted_answers", [])
            is_correct = cls.match_short_answer(
                user_val, expected, accepted,
                grading_mode=grading_mode,
                case_sensitive=case_sensitive
            )
            earned_score = float(max_score) if is_correct else 0.0

            sub_results.append({
                "label": "단일답안",
                "user_answer": user_val,
                "expected_answer": expected,
                "accepted_answers": accepted,
                "is_correct": is_correct,
                "score": earned_score,
                "max_score": float(max_score)
            })

        earned_score = round(earned_score, 1)
        is_all_correct = (earned_score == float(max_score))

        return {
            "question_id": question["id"],
            "type": "short",
            "earned_score": earned_score,
            "max_score": float(max_score),
            "is_correct": is_all_correct,
            "sub_results": sub_results,
            "user_answer_summary": user_ans_data,
            "explanation": question.get("explanation", "")
        }

    @classmethod
    def grade_rubric_sub_question(cls, user_text: str, sub_q: Dict[str, Any]) -> Dict[str, Any]:
        """서술/실무 소문항 루브릭 채점"""
        max_score = float(sub_q.get("score", 4))
        rubric = sub_q.get("rubric", {})
        keyword_groups = rubric.get("keywords", [])
        user_norm = user_text.lower()

        matched_groups = []
        missing_groups = []

        for group in keyword_groups:
            matched_word = None
            for kw in group:
                pattern = re.escape(kw.lower())
                if re.search(pattern, user_norm):
                    matched_word = kw
                    break
            if matched_word:
                matched_groups.append(matched_word)
            else:
                missing_groups.append("/".join(group))

        total_groups = len(keyword_groups)
        earned_score = 0.0

        if "keyword_points" in rubric:
            # 키워드 그룹별 개별 배점 지정 방식
            kw_points = rubric["keyword_points"]
            for i, group in enumerate(keyword_groups):
                if i < len(matched_groups):
                    earned_score += float(kw_points[i])
        else:
            all_match_pts = float(rubric.get("all_match_points", max_score))
            partial_match_pts = float(rubric.get("partial_match_points", max_score / 2))

            if total_groups > 0:
                match_ratio = len(matched_groups) / total_groups
                if match_ratio == 1.0:
                    earned_score = all_match_pts
                elif match_ratio >= 0.5:
                    earned_score = partial_match_pts
                else:
                    earned_score = 0.0
            else:
                earned_score = max_score if len(user_text.strip()) > 5 else 0.0

        earned_score = round(min(earned_score, max_score), 1)

        return {
            "sub_id": sub_q.get("sub_id"),
            "prompt": sub_q.get("prompt"),
            "user_text": user_text,
            "model_answer": sub_q.get("model_answer"),
            "earned_score": earned_score,
            "max_score": max_score,
            "matched_keywords": matched_groups,
            "missing_keywords": missing_groups
        }

    @classmethod
    def grade_descriptive_question(cls, question: Dict[str, Any], user_ans_data: Any) -> Dict[str, Any]:
        """서술형 1문항 채점 (최대 12점)"""
        max_score = float(question.get("score", 12))
        sub_questions = question.get("sub_questions", [])
        total_earned = 0.0
        sub_results = []

        user_dict = user_ans_data if isinstance(user_ans_data, dict) else {}

        for sub in sub_questions:
            sub_id = str(sub.get("sub_id"))
            sub_text = str(user_dict.get(sub_id, "")).strip()
            sub_res = cls.grade_rubric_sub_question(sub_text, sub)
            total_earned += sub_res["earned_score"]
            sub_results.append(sub_res)

        total_earned = round(min(total_earned, max_score), 1)

        return {
            "question_id": question["id"],
            "type": "descriptive",
            "earned_score": total_earned,
            "max_score": max_score,
            "sub_results": sub_results,
            "model_answer": question.get("model_answer", ""),
            "explanation": question.get("explanation", "")
        }

    @classmethod
    def grade_practical_question(cls, question: Dict[str, Any], user_ans_data: Any, is_selected: bool) -> Dict[str, Any]:
        """실무형 1문항 채점 (선택 시 최대 16점, 미선택 시 0점)"""
        max_score = float(question.get("score", 16))

        if not is_selected:
            return {
                "question_id": question["id"],
                "type": "practical",
                "is_selected": False,
                "earned_score": 0.0,
                "max_score": max_score,
                "sub_results": [],
                "model_answer": question.get("model_answer", ""),
                "explanation": question.get("explanation", ""),
                "note": "응시자가 선택하지 않은 문항입니다. (채점 제외)"
            }

        # 선택된 문항 채점
        sub_questions = question.get("sub_questions", [])
        total_earned = 0.0
        sub_results = []
        user_dict = user_ans_data if isinstance(user_ans_data, dict) else {}

        for sub in sub_questions:
            sub_id = str(sub.get("sub_id"))
            sub_text = str(user_dict.get(sub_id, "")).strip()
            sub_res = cls.grade_rubric_sub_question(sub_text, sub)
            total_earned += sub_res["earned_score"]
            sub_results.append(sub_res)

        total_earned = round(min(total_earned, max_score), 1)

        return {
            "question_id": question["id"],
            "type": "practical",
            "is_selected": True,
            "earned_score": total_earned,
            "max_score": max_score,
            "sub_results": sub_results,
            "model_answer": question.get("model_answer", ""),
            "explanation": question.get("explanation", ""),
            "note": "응시자가 선택하여 채점된 실무형 문항입니다."
        }

    @classmethod
    def grade_full_exam(cls, questions: List[Dict[str, Any]], submission: Dict[str, Any]) -> Dict[str, Any]:
        """
        전체 모의고사 1회 종합 채점
        - 단답형 12문항: 36점
        - 서술형 4문항: 48점
        - 실무형 2문항 중 선택 1문항: 16점
        - 총점: 100점 만점
        """
        selected_prac_id = submission.get("selected_practical_id")
        answers = submission.get("answers", {})

        short_earned = 0.0
        desc_earned = 0.0
        prac_earned = 0.0

        details = []

        for q in questions:
            q_id = q["id"]
            q_type = q["type"]
            q_ans = answers.get(q_id, {})

            if q_type == "short":
                res = cls.grade_short_question(q, q_ans)
                short_earned += res["earned_score"]
            elif q_type == "descriptive":
                res = cls.grade_descriptive_question(q, q_ans)
                desc_earned += res["earned_score"]
            elif q_type == "practical":
                is_sel = (q_id == selected_prac_id)
                res = cls.grade_practical_question(q, q_ans, is_sel)
                if is_sel:
                    prac_earned += res["earned_score"]
            else:
                continue

            # 출처 메타데이터 병합
            res["category"] = q.get("category")
            res["source_info"] = q.get("source_info")
            res["source_page"] = q.get("source_page")
            res["question_text"] = q.get("question")
            details.append(res)

        total_earned = round(short_earned + desc_earned + prac_earned, 1)
        is_passed = (total_earned >= 60.0)

        return {
            "total_score": total_earned,
            "max_total_score": 100.0,
            "is_passed": is_passed,
            "summary": {
                "short": {
                    "earned": round(short_earned, 1),
                    "max": 36.0,
                    "percentage": round((short_earned / 36.0) * 100, 1)
                },
                "descriptive": {
                    "earned": round(desc_earned, 1),
                    "max": 48.0,
                    "percentage": round((desc_earned / 48.0) * 100, 1)
                },
                "practical": {
                    "earned": round(prac_earned, 1),
                    "max": 16.0,
                    "percentage": round((prac_earned / 16.0) * 100, 1),
                    "selected_id": selected_prac_id
                }
            },
            "graded_count": 17,
            "details": details
        }
