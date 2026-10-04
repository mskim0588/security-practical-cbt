# -*- coding: utf-8 -*-
"""
LearningService
Handles concept overview listings, concept detailed study packs, dynamic question mappings,
and integration with analytics and sources.
"""
from typing import Dict, List, Any, Optional
from app.services.data_loader import DataLoader
from app.services.analytics_service import AnalyticsService

class LearningService:
    def __init__(self, data_loader: Optional[DataLoader] = None, analytics_service: Optional[AnalyticsService] = None):
        self.loader = data_loader or DataLoader()
        self.analytics_svc = analytics_service or AnalyticsService(self.loader)

    def get_concept_overview_list(self) -> List[Dict[str, Any]]:
        """
        20개 개념 목록을 반환하며, 각 개념별 문항 분포 및 취약도 지수(VI)/성취도 데이터를 동적 결합.
        """
        concepts = self.loader.load_concepts()
        concept_contents = self.loader.load_concept_contents()
        questions = self.loader.load_questions()

        # 취약도 통계 매핑
        try:
            analytics_list = self.analytics_svc.get_concept_analytics()
            analytics_map = {item["concept_id"]: item for item in analytics_list}
        except Exception:
            analytics_map = {}

        # 문항 유형별 카운트 계산
        q_stats: Dict[str, Dict[str, int]] = {}
        for q in questions:
            cid = q.get("concept_id")
            if not cid:
                continue
            if cid not in q_stats:
                q_stats[cid] = {"total": 0, "short": 0, "descriptive": 0, "practical": 0}
            q_stats[cid]["total"] += 1
            q_type = q.get("type")
            if q_type in q_stats[cid]:
                q_stats[cid][q_type] += 1

        result = []
        for c in concepts:
            cid = c["id"]
            content = concept_contents.get(cid, {})
            stats = q_stats.get(cid, {"total": 0, "short": 0, "descriptive": 0, "practical": 0})
            ana = analytics_map.get(cid, {})

            summary_text = content.get("summary") or c.get("summary") or c.get("description", "")
            core_points = content.get("core_points", [])

            # 법령 상태
            law_status = content.get("law_review_status", {
                "status": "source_current",
                "effective_year": "2024",
                "note": ""
            })

            result.append({
                "concept_id": cid,
                "name": c.get("name", ""),
                "category": c.get("category", ""),
                "summary": summary_text,
                "core_points": core_points[:3] if core_points else [],  # 카드 미리보기용 최대 3개
                "question_count": stats["total"],
                "short_count": stats["short"],
                "desc_count": stats["descriptive"],
                "prac_count": stats["practical"],
                "attempts_count": ana.get("attempts_count", 0),
                "score_rate": ana.get("score_rate", 0.0),
                "vi": ana.get("vi", 0.0),
                "grade": ana.get("grade", "미응시"),
                "grade_code": ana.get("grade_code", "none"),
                "law_review_status": law_status
            })

        return result

    def get_concept_detail(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """
        개별 개념의 상세 학습서 패키지 반환 (개념 메타데이터 + 심층 학습서 + 동적 연계 문항 + 출처 정보)
        """
        concepts = self.loader.load_concepts()
        concept_meta = next((c for c in concepts if c["id"] == concept_id), None)
        if not concept_meta:
            return None

        concept_contents = self.loader.load_concept_contents()
        content = concept_contents.get(concept_id, {})

        # 동적 연계 문항 추출 (questions.json 180문항 중 해당 concept_id 매핑)
        questions = self.loader.load_questions()
        connected_questions = [
            q for q in questions if q.get("concept_id") == concept_id
        ]
        # 정렬: 단답형 -> 서술형 -> 실무형 순서
        type_order = {"short": 1, "descriptive": 2, "practical": 3}
        connected_questions.sort(key=lambda x: (type_order.get(x.get("type", ""), 99), x.get("id", "")))

        # 출처 딕셔너리 매핑
        sources_dict = self.loader.get_sources_dict()
        enriched_sources = []
        for sref in content.get("related_sources", []):
            sid = sref.get("source_id")
            sinfo = sources_dict.get(sid, {})
            enriched_sources.append({
                "source_id": sid,
                "title": sinfo.get("title", "공식 출처 문헌"),
                "filename": sinfo.get("filename", ""),
                "page_hint": sref.get("page_hint", ""),
                "relevance": sref.get("relevance", ""),
                "role": sinfo.get("role", "")
            })

        # 취약도 / 성취도 통계
        try:
            analytics_list = self.analytics_svc.get_concept_analytics()
            concept_analytics = next((a for a in analytics_list if a["concept_id"] == concept_id), None)
        except Exception:
            concept_analytics = None

        return {
            "concept_id": concept_id,
            "name": concept_meta.get("name", ""),
            "category": concept_meta.get("category", ""),
            "meta": concept_meta,
            "content": content,
            "questions": connected_questions,
            "sources": enriched_sources,
            "analytics": concept_analytics
        }

    def get_question_study_pack(self, question_id: str) -> Optional[Dict[str, Any]]:
        """
        문항 원본 + 심층 해설 + 소속 개념 메타데이터 패키지 반환
        """
        question = self.loader.get_question_by_id(question_id)
        if not question:
            return None

        explanation = self.loader.get_explanation_for_question(question_id)
        cid = question.get("concept_id")
        concept_detail = self.get_concept_detail(cid) if cid else None

        return {
            "question": question,
            "explanation": explanation,
            "concept": concept_detail
        }
