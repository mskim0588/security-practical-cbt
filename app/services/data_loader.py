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
        self._concept_contents: Optional[Dict[str, Any]] = None
        self._explanations: Optional[Dict[str, Any]] = None
        self._topics: Optional[List[Dict[str, Any]]] = None
        self._question_topics: Optional[List[Dict[str, str]]] = None

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

    def load_topics(self) -> List[Dict[str, Any]]:
        """Load the additive Topic learning taxonomy."""
        if self._topics is None:
            path = os.path.join(self.data_dir, "topics.json")
            with open(path, "r", encoding="utf-8") as f:
                self._topics = json.load(f)
        return self._topics

    def load_question_topics(self) -> List[Dict[str, str]]:
        """Load primary Question-to-Topic mappings without changing questions.json."""
        if self._question_topics is None:
            path = os.path.join(self.data_dir, "question_topics.json")
            with open(path, "r", encoding="utf-8") as f:
                self._question_topics = json.load(f)
        return self._question_topics

    def load_concept_contents(self) -> Dict[str, Any]:
        """concept_contents.json을 안전하게 로드하며 메모리 캐싱 적용"""
        if self._concept_contents is None:
            path = os.path.join(self.data_dir, "concept_contents.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self._concept_contents = json.load(f)
            else:
                self._concept_contents = {}
        return self._concept_contents

    def load_explanations(self) -> Dict[str, Any]:
        """explanations.json을 안전하게 로드하며 메모리 캐싱 적용"""
        if self._explanations is None:
            path = os.path.join(self.data_dir, "explanations.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self._explanations = json.load(f)
            else:
                self._explanations = {}
        return self._explanations

    def get_explanation_for_question(self, question_id: str) -> Dict[str, Any]:
        """explanations.json 조회 -> 미존재 시 questions.json의 기존 explanation으로 fallback dict 반환"""
        explanations = self.load_explanations()
        if question_id in explanations:
            return explanations[question_id]
        
        q = self.get_question_by_id(question_id)
        if q:
            return {
                "question_id": question_id,
                "overview": q.get("explanation", ""),
                "key_concept_points": [],
                "why_correct": q.get("explanation", ""),
                "why_wrong_common_traps": [],
                "related_commands": [],
                "exam_strategy": ""
            }
        return {
            "question_id": question_id,
            "overview": "해설 정보가 없습니다.",
            "key_concept_points": [],
            "why_correct": "",
            "why_wrong_common_traps": [],
            "related_commands": [],
            "exam_strategy": ""
        }

    def get_sources_dict(self) -> Dict[str, Dict[str, Any]]:
        sources = self.load_sources()
        return {s["id"]: s for s in sources}

    def get_enriched_questions(self) -> List[Dict[str, Any]]:
        """문항 데이터에 출처 메타데이터를 결합하여 반환"""
        questions = self.load_questions()
        sources_dict = self.get_sources_dict()
        concepts_dict = {c["id"]: c.get("name", "") for c in self.load_concepts()}

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
            cid = q.get("concept_id")
            if cid and cid in concepts_dict:
                q_copy["concept_name"] = concepts_dict[cid]
            enriched.append(q_copy)
        return enriched

    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """문항 ID로 단건 조회 (출처 및 개념 메타데이터 결합)"""
        if not hasattr(self, "_q_map") or self._q_map is None:
            self._q_map = {q["id"]: q for q in self.get_enriched_questions()}
        return self._q_map.get(question_id)

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
