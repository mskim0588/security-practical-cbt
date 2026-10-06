import math
from typing import Dict, List, Any, Optional
from sqlalchemy import select, func, desc, asc
from app.models.database import db_session
from app.models.history import AnswerRecord, ExamAttempt, LEARNING_ONLY_EXAM_MODES
from app.services.data_loader import DataLoader

class AnalyticsService:
    CATEGORIES = [
        "시스템 보안",
        "네트워크 보안",
        "애플리케이션 보안",
        "정보보안 일반 및 암호학",
        "정보보호 관리 및 법규"
    ]

    def __init__(self, data_loader: Optional[DataLoader] = None):
        self.loader = data_loader or DataLoader()
        self.concepts = self.loader.load_concepts()
        self.concept_map = {c["id"]: c for c in self.concepts}
        self.all_questions = self.loader.get_enriched_questions()
        self.question_map = {q["id"]: q for q in self.all_questions}

    def get_summary_stats(self, is_owner: bool = True) -> Dict[str, Any]:
        """
        학습자의 전체 응시 요약 지표 (기본적으로 Owner 전용)
        """
        attempts_stmt = (
            select(ExamAttempt)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode.notin_(LEARNING_ONLY_EXAM_MODES),
            )
            .order_by(desc(ExamAttempt.created_at))
        )
        attempts = list(db_session.scalars(attempts_stmt).all())

        total_attempts = len(attempts)
        if total_attempts == 0:
            return {
                "total_attempts": 0,
                "passed_count": 0,
                "pass_rate": 0.0,
                "average_score": 0.0,
                "highest_score": 0.0,
                "latest_score": 0.0,
                "latest_attempt": None
            }

        passed_count = sum(1 for a in attempts if a.is_passed)
        pass_rate = round((passed_count / total_attempts) * 100, 1)
        total_score_sum = sum(a.total_score for a in attempts)
        average_score = round(total_score_sum / total_attempts, 1)
        highest_score = max(a.total_score for a in attempts)
        latest_attempt = attempts[0]

        return {
            "total_attempts": total_attempts,
            "passed_count": passed_count,
            "pass_rate": pass_rate,
            "average_score": average_score,
            "highest_score": highest_score,
            "latest_score": latest_attempt.total_score,
            "latest_attempt": latest_attempt.to_dict()
        }

    def get_all_valid_answer_records(self, is_owner: bool = True) -> List[AnswerRecord]:
        """미선택 실무형(unselected)을 제외한 모든 유효 답안 레코드 조회 (기본적으로 Owner 전용)"""
        stmt = (
            select(AnswerRecord)
            .join(ExamAttempt, AnswerRecord.attempt_id == ExamAttempt.id)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode.notin_(LEARNING_ONLY_EXAM_MODES),
                AnswerRecord.achievement_status != "unselected"
            )
        )
        return list(db_session.scalars(stmt).all())

    def get_category_analytics(self, is_owner: bool = True) -> List[Dict[str, Any]]:
        """
        5대 카테고리별 누적 성취도 분석 (기본적으로 Owner 전용)
        """
        records = self.get_all_valid_answer_records(is_owner=is_owner)

        # 카테고리별 문항 수 (전체 문제은행 기준)
        category_bank_counts = {cat: 0 for cat in self.CATEGORIES}
        for q in self.all_questions:
            c = q.get("category")
            if c in category_bank_counts:
                category_bank_counts[c] += 1

        cat_data = {
            cat: {
                "category": cat,
                "bank_question_count": category_bank_counts[cat],
                "attempts_count": 0,
                "earned_score_sum": 0.0,
                "max_score_sum": 0.0,
                "sufficient_count": 0,
                "partial_count": 0,
                "incorrect_count": 0
            }
            for cat in self.CATEGORIES
        }

        for rec in records:
            q_meta = self.question_map.get(rec.question_id)
            if not q_meta:
                continue
            cat = q_meta.get("category")
            if cat not in cat_data:
                continue

            entry = cat_data[cat]
            entry["attempts_count"] += 1
            entry["earned_score_sum"] += rec.earned_score
            entry["max_score_sum"] += rec.max_score

            if rec.achievement_status == "sufficient":
                entry["sufficient_count"] += 1
            elif rec.achievement_status == "partial":
                entry["partial_count"] += 1
            else:
                entry["incorrect_count"] += 1

        results = []
        for cat in self.CATEGORIES:
            entry = cat_data[cat]
            max_sum = entry["max_score_sum"]
            earned_sum = entry["earned_score_sum"]
            att_count = entry["attempts_count"]

            # 배점 가중 득점률
            score_rate = round((earned_sum / max_sum) * 100, 1) if max_sum > 0 else 0.0
            # 정답률 (부분정답은 0.5 가중)
            accuracy_rate = (
                round(((entry["sufficient_count"] + 0.5 * entry["partial_count"]) / att_count) * 100, 1)
                if att_count > 0 else 0.0
            )

            # 등급 판정
            if att_count == 0:
                grade = "미응시"
                grade_code = "none"
            elif score_rate >= 80.0:
                grade = "안전"
                grade_code = "safe"
            elif score_rate >= 60.0:
                grade = "주의"
                grade_code = "warning"
            else:
                grade = "취약"
                grade_code = "danger"

            results.append({
                "category": cat,
                "bank_question_count": entry["bank_question_count"],
                "attempts_count": att_count,
                "earned_score_sum": round(earned_sum, 1),
                "max_score_sum": round(max_sum, 1),
                "score_rate": score_rate,
                "accuracy_rate": accuracy_rate,
                "sufficient_count": entry["sufficient_count"],
                "partial_count": entry["partial_count"],
                "incorrect_count": entry["incorrect_count"],
                "grade": grade,
                "grade_code": grade_code
            })

        return results

    def get_concept_analytics(self, is_owner: bool = True) -> List[Dict[str, Any]]:
        """
        20개 Concept별 누적 성취도 및 취약도 지수(VI) 산출 (기본적으로 Owner 전용)
        """
        records = self.get_all_valid_answer_records(is_owner=is_owner)

        # 개념별 문제은행 문항 수
        concept_bank_counts = {cid: 0 for cid in self.concept_map}
        for q in self.all_questions:
            cid = q.get("concept_id")
            if cid in concept_bank_counts:
                concept_bank_counts[cid] += 1

        concept_stats = {
            cid: {
                "concept_id": cid,
                "name": self.concept_map[cid]["name"],
                "category": self.concept_map[cid]["category"],
                "description": self.concept_map[cid].get("description", ""),
                "bank_question_count": concept_bank_counts[cid],
                "attempts_count": 0,
                "earned_score_sum": 0.0,
                "max_score_sum": 0.0,
                "sufficient_count": 0,
                "partial_count": 0,
                "incorrect_count": 0
            }
            for cid in self.concept_map
        }

        for rec in records:
            q_meta = self.question_map.get(rec.question_id)
            if not q_meta:
                continue
            cid = q_meta.get("concept_id")
            if not cid or cid not in concept_stats:
                continue

            entry = concept_stats[cid]
            entry["attempts_count"] += 1
            entry["earned_score_sum"] += rec.earned_score
            entry["max_score_sum"] += rec.max_score

            if rec.achievement_status == "sufficient":
                entry["sufficient_count"] += 1
            elif rec.achievement_status == "partial":
                entry["partial_count"] += 1
            else:
                entry["incorrect_count"] += 1

        results = []
        for cid, entry in concept_stats.items():
            att = entry["attempts_count"]
            max_sc = entry["max_score_sum"]
            earned_sc = entry["earned_score_sum"]
            inc = entry["incorrect_count"]
            part = entry["partial_count"]

            score_rate = round((earned_sc / max_sc) * 100, 1) if max_sc > 0 else 0.0

            # 취약도 지수 (Vulnerability Index, VI)
            # VI = (100 - ScoreRate) * ((incorrect + 0.5*partial) / attempts) * log2(attempts + 1)
            if att > 0:
                fail_weight = (inc + 0.5 * part) / att
                sample_weight = math.log2(att + 1.0)
                vi = round((100.0 - score_rate) * fail_weight * sample_weight, 1)
            else:
                vi = 0.0

            if att == 0:
                grade = "미응시"
                grade_code = "none"
            elif score_rate >= 80.0:
                grade = "안전"
                grade_code = "safe"
            elif score_rate >= 60.0:
                grade = "주의"
                grade_code = "warning"
            else:
                grade = "취약"
                grade_code = "danger"

            results.append({
                "concept_id": cid,
                "name": entry["name"],
                "category": entry["category"],
                "description": entry["description"],
                "bank_question_count": entry["bank_question_count"],
                "attempts_count": att,
                "earned_score_sum": round(earned_sc, 1),
                "max_score_sum": round(max_sc, 1),
                "score_rate": score_rate,
                "sufficient_count": entry["sufficient_count"],
                "partial_count": part,
                "incorrect_count": inc,
                "vulnerability_index": vi,
                "grade": grade,
                "grade_code": grade_code
            })

        # Concept ID 순서 정렬
        results.sort(key=lambda x: x["concept_id"])
        return results

    def get_top_vulnerable_concepts(self, limit: int = 5, is_owner: bool = True) -> List[Dict[str, Any]]:
        """
        집중 보완 대상 취약 Concept Top N 산출 (기본적으로 Owner 전용)
        """
        concepts = self.get_concept_analytics(is_owner=is_owner)
        # 응시 이력이 있고 오답/감점이 있는 개념 우선
        attempted_vulnerable = [c for c in concepts if c["attempts_count"] > 0 and c["vulnerability_index"] > 0]
        attempted_vulnerable.sort(key=lambda x: x["vulnerability_index"], reverse=True)

        if len(attempted_vulnerable) >= limit:
            return attempted_vulnerable[:limit]

        # 부족한 경우 아직 응시하지 않은 개념으로 보충
        unattempted = [c for c in concepts if c["attempts_count"] == 0]
        combined = attempted_vulnerable + unattempted
        return combined[:limit]

    def get_recent_performance_trend(self, limit: int = 10, is_owner: bool = True) -> List[Dict[str, Any]]:
        """
        최근 회차별 점수 및 합격 추이 (기본적으로 Owner 전용)
        """
        stmt = (
            select(ExamAttempt)
            .where(
                ExamAttempt.is_owner == is_owner,
                ExamAttempt.exam_mode.notin_(LEARNING_ONLY_EXAM_MODES),
            )
            .order_by(desc(ExamAttempt.created_at))
            .limit(limit)
        )
        attempts = list(db_session.scalars(stmt).all())
        # 시간순으로 뒤집기
        attempts.reverse()

        return [
            {
                "attempt_id": a.id,
                "exam_mode": a.exam_mode,
                "total_score": a.total_score,
                "short_score": a.short_score,
                "descriptive_score": a.descriptive_score,
                "practical_score": a.practical_score,
                "is_passed": a.is_passed,
                "date_str": a.created_at.strftime("%m/%d %H:%M") if a.created_at else ""
            }
            for a in attempts
        ]
