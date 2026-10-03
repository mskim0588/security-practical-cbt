import random
from typing import Dict, List, Any, Optional

class ExamGenerator:
    STANDARD_SHORT_IDS = [f"Q-SHORT-{i:03d}" for i in range(1, 13)]
    STANDARD_DESC_IDS = [f"Q-DESC-{i:03d}" for i in range(1, 5)]
    STANDARD_PRAC_IDS = [f"Q-PRAC-{i:03d}" for i in range(1, 3)]
    STANDARD_QUESTION_IDS = STANDARD_SHORT_IDS + STANDARD_DESC_IDS + STANDARD_PRAC_IDS

    @classmethod
    def generate_exam_set(
        cls,
        all_questions: List[Dict[str, Any]],
        mode: str = "standard",
        seed: Optional[int] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        시험 세트 생성기
        - mode == "standard": 제1회 표준 기출 모의고사 (고정 18문항)
        - mode == "random": 카테고리 분산 및 중복 방지 지능형 랜덤 시험 세트 생성
        - mode == "wrong_review": 오답노트 등록 문항 우선 출제 모의고사
        - mode == "adaptive": 취약 Concept 집중 출제 모의고사
        """
        if mode == "standard":
            # 표준 모드: 고정 18문항 (Goal 1 보존)
            q_map = {q["id"]: q for q in all_questions}
            standard_set = [q_map[qid] for qid in ExamGenerator.STANDARD_QUESTION_IDS if qid in q_map]
            if len(standard_set) == 18:
                return standard_set
            # Fallback: 표준 ID가 온전히 없을 경우 기존 순서대로 12 + 4 + 2 추출
            short_pool = [q for q in all_questions if q["type"] == "short"][:12]
            desc_pool = [q for q in all_questions if q["type"] == "descriptive"][:4]
            prac_pool = [q for q in all_questions if q["type"] == "practical"][:2]
            return short_pool + desc_pool + prac_pool

        if mode == "wrong_review":
            wrong_ids = kwargs.get("wrong_question_ids", [])
            return cls.generate_wrong_review_exam(all_questions, wrong_ids, seed)

        if mode == "adaptive":
            vuln_concepts = kwargs.get("vulnerable_concept_ids", [])
            return cls.generate_adaptive_exam(all_questions, vuln_concepts, seed)

        # 랜덤 모드: 카테고리 분산 및 지능형 선별
        rng = random.Random(seed)

        short_pool = [q for q in all_questions if q["type"] == "short"]
        desc_pool = [q for q in all_questions if q["type"] == "descriptive"]
        prac_pool = [q for q in all_questions if q["type"] == "practical"]

        # 1. 단답형 12문제 선별 (카테고리 분산)
        selected_shorts = ExamGenerator._pick_balanced_questions(short_pool, 12, rng)

        # 2. 서술형 4문제 선별 (단답형과 동일 concept_id 과다 중복 방지)
        used_concept_ids = set(q.get("concept_id") for q in selected_shorts if q.get("concept_id"))
        selected_descs = ExamGenerator._pick_balanced_descriptive(desc_pool, 4, used_concept_ids, rng)

        # 3. 실무형 2문제 선별 (상호 다른 카테고리 우선)
        selected_pracs = ExamGenerator._pick_balanced_practical(prac_pool, 2, rng)

        # 4. 최종 18문항 결합
        exam_set = selected_shorts + selected_descs + selected_pracs

        # 5. 유효성 검증 (12 + 4 + 2 = 18)
        assert len(exam_set) == 18, f"시험 문항 수는 18개여야 하나 {len(exam_set)}개가 생성되었습니다."
        return exam_set

    @classmethod
    def generate_wrong_review_exam(
        cls,
        all_questions: List[Dict[str, Any]],
        wrong_question_ids: List[str],
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        오답노트 등록 문항 우선 출제 모의고사 (100점 / 18문항: 단답 12, 서술 4, 실무 2)
        - 오답 문항이 있으면 해당 유형 슬롯에 우선 배정
        - 오답 문항이 부족한 경우 일반 풀에서 카테고리 균형을 맞춰 보충
        """
        rng = random.Random(seed)
        wrong_set = set(wrong_question_ids)

        short_pool = [q for q in all_questions if q["type"] == "short"]
        desc_pool = [q for q in all_questions if q["type"] == "descriptive"]
        prac_pool = [q for q in all_questions if q["type"] == "practical"]

        # 1. 단답형 12문항
        short_wrong = [q for q in short_pool if q["id"] in wrong_set]
        rng.shuffle(short_wrong)
        picked_shorts = short_wrong[:12]
        if len(picked_shorts) < 12:
            remaining_shorts = [q for q in short_pool if q["id"] not in {q["id"] for q in picked_shorts}]
            needed = 12 - len(picked_shorts)
            picked_shorts.extend(cls._pick_balanced_questions(remaining_shorts, needed, rng))

        # 2. 서술형 4문항
        desc_wrong = [q for q in desc_pool if q["id"] in wrong_set]
        rng.shuffle(desc_wrong)
        picked_descs = desc_wrong[:4]
        if len(picked_descs) < 4:
            used_concepts = set(q.get("concept_id") for q in picked_shorts + picked_descs if q.get("concept_id"))
            remaining_descs = [q for q in desc_pool if q["id"] not in {q["id"] for q in picked_descs}]
            needed = 4 - len(picked_descs)
            picked_descs.extend(cls._pick_balanced_descriptive(remaining_descs, needed, used_concepts, rng))

        # 3. 실무형 2문항
        prac_wrong = [q for q in prac_pool if q["id"] in wrong_set]
        rng.shuffle(prac_wrong)
        picked_pracs = prac_wrong[:2]
        if len(picked_pracs) < 2:
            remaining_pracs = [q for q in prac_pool if q["id"] not in {q["id"] for q in picked_pracs}]
            needed = 2 - len(picked_pracs)
            picked_pracs.extend(cls._pick_balanced_practical(remaining_pracs, needed, rng))

        exam_set = picked_shorts + picked_descs + picked_pracs
        assert len(exam_set) == 18, f"시험 문항 수는 18개여야 하나 {len(exam_set)}개가 생성되었습니다."
        return exam_set

    @classmethod
    def generate_adaptive_exam(
        cls,
        all_questions: List[Dict[str, Any]],
        vulnerable_concept_ids: List[str],
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        취약 Concept 집중 모의고사 (100점 / 18문항: 단답 12, 서술 4, 실무 2)
        - 취약도 상위 Concept에 속한 문항을 60~70% 이상 우선 선발
        - 나머지 슬롯은 카테고리 균형을 위해 일반 문제로 보충
        """
        rng = random.Random(seed)
        vuln_set = set(vulnerable_concept_ids)

        short_pool = [q for q in all_questions if q["type"] == "short"]
        desc_pool = [q for q in all_questions if q["type"] == "descriptive"]
        prac_pool = [q for q in all_questions if q["type"] == "practical"]

        # 1. 단답형 12문항 (취약 Concept 문항 최대 8개 우선)
        short_vuln = [q for q in short_pool if q.get("concept_id") in vuln_set]
        rng.shuffle(short_vuln)
        picked_shorts = short_vuln[:8]
        remaining_shorts = [q for q in short_pool if q["id"] not in {q["id"] for q in picked_shorts}]
        needed_shorts = 12 - len(picked_shorts)
        picked_shorts.extend(cls._pick_balanced_questions(remaining_shorts, needed_shorts, rng))

        # 2. 서술형 4문항 (취약 Concept 문항 최대 3개 우선)
        desc_vuln = [q for q in desc_pool if q.get("concept_id") in vuln_set]
        rng.shuffle(desc_vuln)
        picked_descs = desc_vuln[:3]
        used_concepts = set(q.get("concept_id") for q in picked_shorts + picked_descs if q.get("concept_id"))
        remaining_descs = [q for q in desc_pool if q["id"] not in {q["id"] for q in picked_descs}]
        needed_descs = 4 - len(picked_descs)
        picked_descs.extend(cls._pick_balanced_descriptive(remaining_descs, needed_descs, used_concepts, rng))

        # 3. 실무형 2문항 (취약 Concept 문항 최대 1개 우선)
        prac_vuln = [q for q in prac_pool if q.get("concept_id") in vuln_set]
        rng.shuffle(prac_vuln)
        picked_pracs = prac_vuln[:1]
        remaining_pracs = [q for q in prac_pool if q["id"] not in {q["id"] for q in picked_pracs}]
        needed_pracs = 2 - len(picked_pracs)
        picked_pracs.extend(cls._pick_balanced_practical(remaining_pracs, needed_pracs, rng))

        exam_set = picked_shorts + picked_descs + picked_pracs
        assert len(exam_set) == 18, f"시험 문항 수는 18개여야 하나 {len(exam_set)}개가 생성되었습니다."
        return exam_set

    @staticmethod
    def _pick_balanced_questions(pool: List[Dict[str, Any]], target_count: int, rng: random.Random) -> List[Dict[str, Any]]:
        """카테고리별로 고르게 분산하여 target_count 문항 선별"""
        if len(pool) <= target_count:
            # 풀의 크기가 목표치 이하인 경우 셔플 후 전체 반환 (fallback)
            shuffled = list(pool)
            rng.shuffle(shuffled)
            return shuffled

        # 카테고리별 그룹화
        by_cat: Dict[str, List[Dict[str, Any]]] = {}
        for q in pool:
            cat = q.get("category", "기타")
            by_cat.setdefault(cat, []).append(q)

        # 카테고리 내에서 셔플
        for cat in by_cat:
            rng.shuffle(by_cat[cat])

        selected: List[Dict[str, Any]] = []
        selected_ids = set()

        # 라운드 로빈 방식으로 카테고리별 1개씩 선별
        categories = list(by_cat.keys())
        rng.shuffle(categories)

        while len(selected) < target_count:
            added_in_round = False
            for cat in categories:
                if len(selected) >= target_count:
                    break
                if by_cat[cat]:
                    candidate = by_cat[cat].pop()
                    if candidate["id"] not in selected_ids:
                        selected.append(candidate)
                        selected_ids.add(candidate["id"])
                        added_in_round = True
            if not added_in_round:
                # 더 이상 뽑을 수 없는 경우 중단
                break

        # 부족한 경우 남은 풀에서 보충 (Graceful Fallback)
        if len(selected) < target_count:
            remaining = [q for q in pool if q["id"] not in selected_ids]
            rng.shuffle(remaining)
            selected.extend(remaining[:target_count - len(selected)])

        return selected

    @staticmethod
    def _pick_balanced_descriptive(
        pool: List[Dict[str, Any]],
        target_count: int,
        avoid_concept_ids: set,
        rng: random.Random
    ) -> List[Dict[str, Any]]:
        """서술형 선별: 단답형 미사용 Concept 우선 + 서술형 내부 Category 다양성 고려"""
        if len(pool) <= target_count:
            shuffled = list(pool)
            rng.shuffle(shuffled)
            return shuffled

        # 1. 단답형 미사용 Concept 후보군(preferred)과 중복 Concept 후보군(others) 분리
        preferred = [q for q in pool if q.get("concept_id") not in avoid_concept_ids]
        others = [q for q in pool if q.get("concept_id") in avoid_concept_ids]

        selected: List[Dict[str, Any]] = []
        selected_ids = set()

        def pick_round_robin_categories(candidates: List[Dict[str, Any]], needed: int) -> List[Dict[str, Any]]:
            if needed <= 0 or not candidates:
                return []
            by_cat: Dict[str, List[Dict[str, Any]]] = {}
            for q in candidates:
                if q["id"] not in selected_ids:
                    by_cat.setdefault(q.get("category", "기타"), []).append(q)
            for cat in by_cat:
                rng.shuffle(by_cat[cat])

            picked = []
            cats = list(by_cat.keys())
            rng.shuffle(cats)
            while len(picked) < needed:
                added = False
                for cat in cats:
                    if len(picked) >= needed:
                        break
                    if by_cat[cat]:
                        item = by_cat[cat].pop()
                        picked.append(item)
                        selected_ids.add(item["id"])
                        added = True
                if not added:
                    break
            return picked

        # 1순위 & 2순위: preferred 후보군에서 카테고리 다양성(라운드로빈)으로 선별
        selected.extend(pick_round_robin_categories(preferred, target_count))

        # 3순위 (Fallback): preferred로 target_count를 못 채우면 others에서 카테고리 다양성 고려하여 보충
        if len(selected) < target_count:
            needed = target_count - len(selected)
            selected.extend(pick_round_robin_categories(others, needed))

        # 4순위 (Graceful Fallback): 그래도 부족할 경우 남은 전체 풀에서 보충
        if len(selected) < target_count:
            remaining = [q for q in pool if q["id"] not in selected_ids]
            rng.shuffle(remaining)
            selected.extend(remaining[:target_count - len(selected)])

        return selected[:target_count]

    @staticmethod
    def _pick_balanced_practical(pool: List[Dict[str, Any]], target_count: int, rng: random.Random) -> List[Dict[str, Any]]:
        """실무형 선별: 서로 다른 Category 및 Concept 우선 선별"""
        if len(pool) <= target_count:
            shuffled = list(pool)
            rng.shuffle(shuffled)
            return shuffled

        shuffled = list(pool)
        rng.shuffle(shuffled)

        selected: List[Dict[str, Any]] = [shuffled[0]]
        selected_ids = {shuffled[0]["id"]}
        used_cats = {shuffled[0].get("category")}
        used_concepts = {shuffled[0].get("concept_id")}

        while len(selected) < target_count:
            candidates = [q for q in shuffled if q["id"] not in selected_ids]
            if not candidates:
                break

            # 1순위: 서로 다른 Category AND 서로 다른 Concept
            tier1 = [q for q in candidates if q.get("category") not in used_cats and q.get("concept_id") not in used_concepts]
            if tier1:
                chosen = tier1[0]
            else:
                # 1순위 보조: 서로 다른 Category (Concept은 동일할 수 있으나 Category 상이)
                tier1_sub = [q for q in candidates if q.get("category") not in used_cats]
                if tier1_sub:
                    chosen = tier1_sub[0]
                else:
                    # 2순위: 동일 Category라도 서로 다른 Concept
                    tier2 = [q for q in candidates if q.get("concept_id") not in used_concepts]
                    if tier2:
                        chosen = tier2[0]
                    else:
                        # 3순위 (Fallback): 남은 전체 후보에서 선별
                        chosen = candidates[0]

            selected.append(chosen)
            selected_ids.add(chosen["id"])
            if chosen.get("category"):
                used_cats.add(chosen.get("category"))
            if chosen.get("concept_id"):
                used_concepts.add(chosen.get("concept_id"))

        # 부족분 최종 안전장치 (Graceful Fallback)
        if len(selected) < target_count:
            remaining = [q for q in pool if q["id"] not in selected_ids]
            rng.shuffle(remaining)
            selected.extend(remaining[:target_count - len(selected)])

        return selected[:target_count]
