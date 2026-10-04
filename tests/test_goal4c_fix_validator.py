# -*- coding: utf-8 -*-
"""
Automated Validator Tests for Goal 4C-QA-Fix
Verifies:
1. Zero "표준 정답" placeholders in explanations.json.
2. Authentic rubric keywords from questions.json without boilerplate.
3. Accurate rubric score sums (descriptive: 12, practical: 16).
4. No context-mismatched common traps across all 180 questions.
5. Pristine baseline integrity for questions.json, concepts.json, sources.json.
6. CON-MGT-02 law review status update.
"""

import os
import json
import hashlib
import unittest

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")

class TestGoal4CFixQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
            cls.questions = {q["id"]: q for q in json.load(f)}
        with open(os.path.join(DATA_DIR, "explanations.json"), "r", encoding="utf-8") as f:
            cls.explanations = json.load(f)
        with open(os.path.join(DATA_DIR, "concept_contents.json"), "r", encoding="utf-8") as f:
            cls.concept_contents = json.load(f)

    def test_baseline_hashes_unmodified(self):
        """Verify baseline core files remain strictly unmodified."""
        expected_hashes = {
            "questions.json": "661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9",
            "concepts.json": "d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943",
            "sources.json": "9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21"
        }
        for filename, expected_sha in expected_hashes.items():
            path = os.path.join(DATA_DIR, filename)
            with open(path, "rb") as f:
                actual_sha = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(actual_sha, expected_sha, f"Baseline hash altered for {filename}!")

    def test_no_standard_answer_placeholder_in_short_questions(self):
        """P1-1: Verify zero '표준 정답' placeholders remain in why_correct."""
        ph_found = []
        for qid, exp in self.explanations.items():
            wc = exp.get("why_correct", "")
            if "표준 정답입니다" in wc or "표준 정답" in wc:
                ph_found.append(qid)
        self.assertEqual(len(ph_found), 0, f"Found placeholders in questions: {ph_found}")

    def test_rubrics_alignment_and_no_boilerplate(self):
        """P1-2: Verify rubrics match sub_questions score and have no category boilerplate."""
        boilerplate_keywords = [
            ["애플리케이션 보안", "원리", "방어"],
            ["시스템 보안", "원리", "방어"],
            ["네트워크 보안", "원리", "방어"],
            ["정보보호 관리 및 법규", "원리", "방어"],
            ["암호학", "원리", "방어"]
        ]

        for qid, q in self.questions.items():
            q_type = q.get("type")
            if q_type not in ("descriptive", "practical"):
                continue

            exp = self.explanations.get(qid)
            self.assertIsNotNone(exp, f"Missing explanation for {qid}")
            psc = exp.get("practical_scoring_criteria", {})
            self.assertIn("rubrics", psc, f"Missing rubrics in {qid}")

            expected_total = 12 if q_type == "descriptive" else 16
            rubrics = psc.get("rubrics", [])
            total_points = sum(r.get("points", 0) for r in rubrics)
            self.assertEqual(total_points, expected_total, f"{qid} rubric sum {total_points} != {expected_total}")

            # Check sub_questions alignment
            sub_qs = q.get("sub_questions") or []
            self.assertEqual(len(rubrics), len(sub_qs), f"{qid} rubric count != sub_questions count")

            # Check for generic boilerplate
            for r in rubrics:
                kws = r.get("required_keywords", [])
                for bp in boilerplate_keywords:
                    self.assertNotEqual(kws, bp, f"{qid} has boilerplate rubric keywords: {kws}")
                self.assertGreater(len(kws), 0, f"{qid} has empty required_keywords")

    def test_no_context_mismatched_traps(self):
        """P1-3: Verify common traps are context-specific and not cross-topic generic defaults."""
        generic_phrases = ["개념을 정확히 이해해야", "원리와 방어를 혼동", "문제를 꼼꼼히"]

        for qid, exp in self.explanations.items():
            q = self.questions[qid]
            stem = (q.get("stem") or q.get("question") or "").lower()
            ans = str(q.get("answer") or "").lower()
            traps = exp.get("why_wrong_common_traps", [])
            self.assertGreater(len(traps), 0, f"{qid} has no traps")

            for t in traps:
                term = t.get("confused_term_or_misunderstanding", "")
                expl = t.get("explanation", "")
                
                # Check for empty or generic
                for gp in generic_phrases:
                    self.assertNotIn(gp, term, f"{qid} has generic trap: {term}")
                    self.assertNotIn(gp, expl, f"{qid} has generic trap explanation: {expl}")

                # Context mismatch checks:
                # 1. Non-SQL questions should not have Blind SQL / MyBatis traps
                if "mybatis" in term.lower() or "blind sql" in term.lower():
                    is_sql = any(k in stem or k in ans for k in ["sql", "인젝션", "injection", "쿼리", "query"])
                    self.assertTrue(is_sql, f"{qid} non-SQL question has SQL trap: {term}")

                # 2. Non-PAM questions should not have PAM required/requisite traps
                if "required와 requisite" in term or "account 모듈" in term:
                    is_pam = "pam" in stem or "pam" in ans or "모듈" in stem
                    self.assertTrue(is_pam, f"{qid} non-PAM question has PAM trap: {term}")

                # 3. Non-Snort questions should not have Snort direction '<-' trap
                if "snort 룰에서 양방향" in term or "snort" in term.lower():
                    is_snort = "snort" in stem or "snort" in ans or "탐지 룰" in stem
                    self.assertTrue(is_snort, f"{qid} non-Snort question has Snort trap: {term}")

    def test_con_mgt_02_law_status(self):
        """P2-4: Verify CON-MGT-02 law review status adjusted to current_law_review_required."""
        con_mgt_02 = self.concept_contents.get("CON-MGT-02", {})
        law_status = con_mgt_02.get("law_review_status", {})
        self.assertEqual(law_status.get("status"), "current_law_review_required")
        self.assertIn("개인정보", law_status.get("note", ""))

    def test_total_explanation_coverage(self):
        """Verify all 180 questions have complete explanations."""
        self.assertEqual(len(self.explanations), 180)
        for qid in self.questions:
            self.assertIn(qid, self.explanations, f"Question {qid} missing from explanations.json")

if __name__ == "__main__":
    unittest.main()
