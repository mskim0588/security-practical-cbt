import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple


class DescriptiveTrainingEvaluator:
    """Deterministic training feedback derived from the canonical question rubric."""

    STATUS_LABELS = {
        "sufficient": "충족",
        "partial": "부분 충족",
        "incorrect": "미충족",
    }

    @staticmethod
    def _normalize(value: Any) -> str:
        text = unicodedata.normalize("NFKC", str(value or "")).lower()
        text = re.sub(r"[\u2010-\u2015\u2212\ufe58\ufe63\uff0d]", "-", text)
        return re.sub(r"\s+", " ", text).strip()

    @classmethod
    def _keyword_span(cls, answer: str, keyword: Any) -> Optional[Tuple[int, int]]:
        """Match canonical keywords without accepting fragments inside ASCII tokens."""
        haystack = cls._normalize(answer)
        needle = cls._normalize(keyword)
        if not haystack or not needle:
            return None

        escaped = re.escape(needle).replace(r"\ ", r"\s+")
        if re.search(r"[a-z0-9]", needle):
            pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
        elif needle == "+":
            pattern = r"(?<![\w+])\+(?![\w+])"
        elif len(needle) == 1 and not needle.isalnum():
            pattern = rf"(?<!\w){escaped}(?!\w)"
        else:
            pattern = escaped
        for match in re.finditer(pattern, haystack, flags=re.IGNORECASE):
            before = haystack[max(0, match.start() - 2):match.start()]
            after = haystack[match.end():match.end() + 16]
            if before.endswith(("미", "비", "불", "무")):
                continue
            if re.match(r"\s*(?:아님|아니다|아니며|하지\s*않|안\s*(?:함|된다)|금지)", after):
                continue
            return match.span()
        return None

    @classmethod
    def _match_group(cls, answer: str, group: Any) -> Optional[str]:
        candidates = group if isinstance(group, list) else [group]
        for keyword in candidates:
            if cls._keyword_span(answer, keyword):
                return str(keyword)
        return None

    @staticmethod
    def _rubric_score(rubric: Dict[str, Any], matched_indices: List[int], maximum: float) -> float:
        groups = rubric.get("keywords", [])
        if "keyword_points" in rubric:
            points = rubric.get("keyword_points") or []
            earned = sum(float(points[index]) for index in matched_indices if index < len(points))
            return round(min(earned, maximum), 1)

        if not groups:
            return maximum
        ratio = len(matched_indices) / len(groups)
        if ratio == 1:
            earned = float(rubric.get("all_match_points", maximum))
        elif ratio >= 0.5:
            earned = float(rubric.get("partial_match_points", maximum / 2))
        else:
            earned = 0.0
        return round(min(earned, maximum), 1)

    @classmethod
    def evaluate(cls, question: Dict[str, Any], answers: Any) -> Dict[str, Any]:
        user_answers = answers if isinstance(answers, dict) else {}
        sub_results: List[Dict[str, Any]] = []
        total_earned = 0.0
        completed_fields = 0
        matched_core: List[str] = []
        missing_groups: List[str] = []

        for sub in question.get("sub_questions", []):
            sub_id = str(sub.get("sub_id"))
            user_text = str(user_answers.get(sub_id, "")).strip()
            is_completed = bool(user_text)
            canonical_model_match = bool(user_text) and cls._normalize(user_text) == cls._normalize(sub.get("model_answer", ""))
            completed_fields += int(is_completed)
            rubric = sub.get("rubric") or {}
            groups = rubric.get("keywords") or []
            matched_indices: List[int] = []
            sub_matched: List[str] = []
            sub_missing: List[str] = []

            for index, group in enumerate(groups):
                matched = cls._match_group(user_text, group)
                if matched:
                    matched_indices.append(index)
                    sub_matched.append(matched)
                    if matched not in matched_core:
                        matched_core.append(matched)
                else:
                    group_label = "/".join(str(value) for value in (group if isinstance(group, list) else [group]))
                    sub_missing.append(group_label)
                    if group_label not in missing_groups:
                        missing_groups.append(group_label)

            if canonical_model_match and groups:
                matched_indices = list(range(len(groups)))
                sub_missing = []
                if "모범답안과 일치" not in sub_matched:
                    sub_matched.append("모범답안과 일치")
                missing_groups = [value for value in missing_groups if value not in {
                    "/".join(str(item) for item in (group if isinstance(group, list) else [group]))
                    for group in groups
                }]

            maximum = float(sub.get("score", 0.0))
            earned = cls._rubric_score(rubric, matched_indices, maximum) if is_completed else 0.0
            total_earned += earned
            sub_results.append({
                "sub_id": sub_id,
                "prompt": sub.get("prompt", ""),
                "user_text": user_text,
                "model_answer": sub.get("model_answer", ""),
                "earned_score": earned,
                "max_score": maximum,
                "structure_status": "sufficient" if is_completed else "incorrect",
                "structure_label": "충족" if is_completed else "미충족",
                "matched_keywords": sub_matched,
                "missing_keywords": sub_missing,
                "matched_group_count": len(matched_indices),
                "required_group_count": len(groups),
                "canonical_model_match": canonical_model_match,
            })

        required_fields = len(question.get("sub_questions", []))
        missing_groups = []
        for item in sub_results:
            for group_label in item["missing_keywords"]:
                if group_label not in missing_groups:
                    missing_groups.append(group_label)
        if required_fields and completed_fields == required_fields:
            structure_status = "sufficient"
        elif completed_fields:
            structure_status = "partial"
        else:
            structure_status = "incorrect"

        maximum = float(question.get("score", 0.0))
        total_earned = round(min(total_earned, maximum), 1)
        if maximum > 0 and total_earned >= maximum:
            achievement_status = "sufficient"
        elif total_earned > 0:
            achievement_status = "partial"
        else:
            achievement_status = "incorrect"

        return {
            "question_id": question.get("id"),
            "earned_score": total_earned,
            "max_score": maximum,
            "achievement_status": achievement_status,
            "achievement_label": cls.STATUS_LABELS[achievement_status],
            "structure_evaluation": {
                "status": structure_status,
                "label": cls.STATUS_LABELS[structure_status],
                "completed_fields": completed_fields,
                "required_fields": required_fields,
            },
            "keyword_analysis": {
                "matched_keywords": matched_core,
                "missing_keywords": missing_groups,
                "matched_group_count": sum(item["matched_group_count"] for item in sub_results),
                "required_group_count": sum(item["required_group_count"] for item in sub_results),
                "false_positive_control": "영문·숫자 키워드는 독립 토큰 경계에서만 일치하고, 부정 표현과 부분 문자열은 제외합니다.",
            },
            "sub_results": sub_results,
            "model_answer": question.get("model_answer", ""),
            "explanation": question.get("explanation", ""),
        }
