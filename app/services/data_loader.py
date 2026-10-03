import os
import json
from typing import Dict, List, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

class DataLoader:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        self._sources: Optional[List[Dict[str, Any]]] = None
        self._concepts: Optional[List[Dict[str, Any]]] = None
        self._questions: Optional[List[Dict[str, Any]]] = None

    def load_sources(self) -> List[Dict[str, Any]]:
        if self._sources is None:
            path = os.path.join(self.data_dir, "sources.json")
            with open(path, "r", encoding="utf-8") as f:
                self._sources = json.load(f)
        return self._sources

    def load_concepts(self) -> List[Dict[str, Any]]:
        if self._concepts is None:
            path = os.path.join(self.data_dir, "concepts.json")
            with open(path, "r", encoding="utf-8") as f:
                self._concepts = json.load(f)
        return self._concepts

    def load_questions(self) -> List[Dict[str, Any]]:
        if self._questions is None:
            path = os.path.join(self.data_dir, "questions.json")
            with open(path, "r", encoding="utf-8") as f:
                self._questions = json.load(f)
        return self._questions

    def get_sources_dict(self) -> Dict[str, Dict[str, Any]]:
        sources = self.load_sources()
        return {s["id"]: s for s in sources}

    def get_enriched_questions(self) -> List[Dict[str, Any]]:
        """문항 데이터에 출처 메타데이터를 결합하여 반환"""
        questions = self.load_questions()
        sources_dict = self.get_sources_dict()

        enriched = []
        for q in questions:
            q_copy = dict(q)
            src_id = q.get("source_id")
            if src_id and src_id in sources_dict:
                q_copy["source_info"] = sources_dict[src_id]
            else:
                q_copy["source_info"] = {
                    "filename": "Unknown",
                    "title": "미확인 출처"
                }
            enriched.append(q_copy)
        return enriched

    def validate_dataset(self, scope: str = "standard") -> Dict[str, Any]:
        """
        데이터셋 정합성 검증
        - scope == "standard": 제1회 표준 기출 모의고사 (18문항, 100점 만점 구조) 검증 (Goal 1 하위호환)
        - scope == "pool" 또는 "all": 문제은행 전체 풀 무결성 검증
        """
        questions = self.load_questions()

        if scope == "standard":
            from app.services.exam_generator import ExamGenerator
            std_ids = ExamGenerator.STANDARD_QUESTION_IDS
            std_qs = [q for q in questions if q["id"] in std_ids]

            short_qs = [q for q in std_qs if q["type"] == "short"]
            desc_qs = [q for q in std_qs if q["type"] == "descriptive"]
            prac_qs = [q for q in std_qs if q["type"] == "practical"]

            short_score = sum(q.get("score", 0) for q in short_qs)
            desc_score = sum(q.get("score", 0) for q in desc_qs)
            prac_scores = [q.get("score", 0) for q in prac_qs]

            is_valid = (
                len(short_qs) == 12 and
                short_score == 36 and
                len(desc_qs) == 4 and
                desc_score == 48 and
                len(prac_qs) == 2 and
                all(s == 16 for s in prac_scores)
            )

            return {
                "valid": is_valid,
                "short_count": len(short_qs),
                "short_score": short_score,
                "desc_count": len(desc_qs),
                "desc_score": desc_score,
                "prac_count": len(prac_qs),
                "prac_scores": prac_scores,
                "total_candidate_count": len(std_qs),
                "target_graded_count": 17,
                "target_total_score": 100
            }
        else:
            short_qs = [q for q in questions if q["type"] == "short"]
            desc_qs = [q for q in questions if q["type"] == "descriptive"]
            prac_qs = [q for q in questions if q["type"] == "practical"]

            is_valid = (
                len(short_qs) >= 12 and
                all(q.get("score") == 3 for q in short_qs) and
                len(desc_qs) >= 4 and
                all(q.get("score") == 12 for q in desc_qs) and
                len(prac_qs) >= 2 and
                all(q.get("score") == 16 for q in prac_qs)
            )

            return {
                "valid": is_valid,
                "short_count": len(short_qs),
                "desc_count": len(desc_qs),
                "prac_count": len(prac_qs),
                "total_candidate_count": len(questions)
            }

    def get_source_usage_counts(self) -> Dict[str, int]:
        """각 Source ID별 현재 문제에서 참조 중인 문항 수 계산"""
        questions = self.load_questions()
        counts: Dict[str, int] = {}
        for q in questions:
            sid = q.get("source_id")
            if sid:
                counts[sid] = counts.get(sid, 0) + 1
        return counts

    def get_sources_summary(self) -> Dict[str, Any]:
        """출처 메타데이터 요약 및 questions.json 기준 동적 사용 현황 제공"""
        sources = self.load_sources()
        questions = self.load_questions()
        usage_counts = self.get_source_usage_counts()

        all_sources = []
        exam_sources = []
        theory_sources = []

        for s in sources:
            s_copy = dict(s)
            sid = s["id"]
            count = usage_counts.get(sid, 0)
            is_active = (count > 0)
            
            s_copy["question_count"] = count
            s_copy["is_active"] = is_active
            s_copy["status_text"] = f"사용 중 · {count}문제" if is_active else "등록됨 · 현재 미사용"
            s_copy["status_type"] = "active" if is_active else "inactive"

            all_sources.append(s_copy)
            if s.get("group") == "exam":
                exam_sources.append(s_copy)
            else:
                theory_sources.append(s_copy)

        active_sources_count = sum(1 for s in sources if usage_counts.get(s["id"], 0) > 0)

        return {
            "total_sources": len(sources),
            "active_sources_count": active_sources_count,
            "total_questions_count": len(questions),
            "all_sources": all_sources,
            "exam_sources": exam_sources,
            "theory_sources": theory_sources
        }
