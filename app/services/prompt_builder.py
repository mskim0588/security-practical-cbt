# -*- coding: utf-8 -*-
"""
PromptBuilder Service
Constructs optimized, structured study prompts for ChatGPT and Gemini.
Zero-cost, zero-API dependency, runs completely deterministic prompt templates.
"""
from typing import Dict, Any, Optional

class PromptBuilder:
    TEMPLATE_WHY_WRONG = "why_wrong"
    TEMPLATE_REAL_WORLD = "real_world"
    TEMPLATE_SIMILAR_QUESTION = "similar_question"

    @classmethod
    def build_prompt(
        cls,
        template_type: str,
        question_text: str,
        concept_id: Optional[str] = None,
        concept_name: Optional[str] = None,
        user_answer: Optional[str] = None,
        model_answer: Optional[str] = None,
        question_type: Optional[str] = None,
        score: Optional[int] = None
    ) -> str:
        """
        주어진 문항 정보와 수험자 응시 데이터를 바탕으로 유형별 최적화된 프롬프트 텍스트를 생성합니다.
        """
        c_str = f"{concept_id} ({concept_name})" if (concept_id and concept_name) else (concept_id or concept_name or "보안 핵심 개념")
        u_ans = user_answer.strip() if user_answer and str(user_answer).strip() else "(미작성 또는 오답)"
        m_ans = model_answer.strip() if model_answer and str(model_answer).strip() else "(표준 정답 기준)"

        if template_type == cls.TEMPLATE_REAL_WORLD:
            return f"""[정보보안기사 실기 실무 연계 질문]
- 관련 개념: {c_str}
- 시험 문제:
{question_text.strip()}

질문:
실제 기업 보안 환경(Linux 서버/네트워크 장비/클라우드)에서 이 개념과 관련된 취약점을 점검하고 방어 조치하는 구체적인 명령어 및 설정 예시(config) 3가지를 초보자도 이해하기 쉽게 단계별로 설명해 주세요."""

        elif template_type == cls.TEMPLATE_SIMILAR_QUESTION:
            q_t_str = "단답형" if question_type == "short" else ("서술형" if question_type == "descriptive" else "실무형")
            pts_str = f"{score}점" if score else "실기 기준 배점"
            return f"""[정보보안기사 실기 모의 출제 요청]
- 관련 개념: {c_str}
- 출제 희망 유형: {q_t_str} (배점: {pts_str})

요청:
위 보안 개념을 바탕으로 정보보안기사 실기 시험에 출제될 수 있는 새로운 변형 문제 1문항을 만들어 주세요.
1. 문제 지문 (로그/명령어/설정 파일 스니펫 포함)
2. 모범 정답 및 필수 채점 키워드
3. 단계별 부분 점수 채점 루브릭(기준)"""

        else:
            # Default: cls.TEMPLATE_WHY_WRONG
            return f"""[정보보안기사 실기 수험 오답 분석 질문]
- 관련 개념: {c_str}
- 문제 지문:
{question_text.strip()}

- 출제 정답 (모범 답안):
{m_ans}

- 내가 작성한 답안:
{u_ans}

질문:
1. 제가 작성한 답안이 정답과 비교했을 때 기술적으로 어떤 오류, 왜곡, 또는 누락이 있나요?
2. 국가기술자격 실기 채점관 관점에서 제 답안에 부분 점수를 줄 수 없는 결정적 이유는 무엇인가요?
3. 이 문제에서 요구하는 핵심 키워드가 무엇인지, 어떻게 기억해야 실전에서 틀리지 않을지 알기 쉽게 설명해 주세요."""

    @classmethod
    def get_chatgpt_url(cls, prompt_text: Optional[str] = None) -> str:
        """Return the provider homepage without transmitting prompt content."""
        return "https://chatgpt.com/"

    @classmethod
    def get_gemini_url(cls, prompt_text: Optional[str] = None) -> str:
        """Return the provider homepage without transmitting prompt content."""
        return "https://gemini.google.com/app"
