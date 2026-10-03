# -*- coding: utf-8 -*-
"""
Batch 2 - Chunk 3: SRC-10 Management & SRC-11 Law (12 questions)
Q-SHORT-080 ~ Q-SHORT-087
Q-DESC-029 ~ Q-DESC-032
"""

CHUNK_3_QUESTIONS = [
    {
        "id": "Q-SHORT-080",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "조직의 정보자산 위험 분석 기법 중 정량적 위험 분석(Quantitative Risk Analysis)에서 단일 위험 사건 발생 시 예상 손실액(SLE)과 발생 빈도(ARO)를 곱하여 산출하는 '연간 예상 손실액'의 영문 약어를 쓰시오.",
        "answer": "ALE",
        "accepted_answers": ["ALE", "Annual Loss Expectancy", "연간 예상 손실액", "연간예상손실액", "ALE = SLE * ARO"],
        "grading_mode": "normalized",
        "explanation": "정량적 위험 분석에서 연간 예상 손실액(ALE)은 단일 예상 손실액(SLE)과 연간 발생률(ARO)의 곱으로 산출됩니다 (SRC-10 p.109).",
        "source_id": "SRC-10",
        "source_page": 109,
        "concept_id": "CON-MGT-01",
        "difficulty": "medium",
        "tags": ["위험분석", "정량적위험분석", "ALE", "SLE", "ARO"]
    },
    {
        "id": "Q-SHORT-081",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "정보보호시스템 공통평가기준(CC; Common Criteria)의 3대 핵심 구성요소 중, 특정 정보보호 제품군이 갖추어야 할 공통적인 보안 목표와 요구사항을 구현과 독립적으로 명세화한 문서인 '보호프로파일'의 영문 약어를 쓰시오.",
        "answer": "PP",
        "accepted_answers": ["PP", "Protection Profile", "보호프로파일"],
        "grading_mode": "normalized",
        "explanation": "PP(Protection Profile; 보호프로파일)는 특정 제품군에 공통으로 요구되는 보안 요구사항 명세서입니다 (SRC-10 p.190).",
        "source_id": "SRC-10",
        "source_page": 190,
        "concept_id": "CON-MGT-01",
        "difficulty": "medium",
        "tags": ["CC인증", "보호프로파일", "PP", "공통평가기준"]
    },
    {
        "id": "Q-SHORT-082",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "국가 사이버안보 위기관리 매뉴얼에 따라 국가정보원 등 관계기관이 사이버 공격 및 침해사고 위협 수준에 따라 발령하는 '국가 사이버위기경보'의 4단계를 위험도가 낮은 단계부터 높은 단계 순으로 차례대로 나열하여 쓰시오.",
        "answer": "관심, 주의, 경계, 심각",
        "accepted_answers": [
            "관심, 주의, 경계, 심각",
            "관심,주의,경계,심각",
            "관심-주의-경계-심각",
            "관심 -> 주의 -> 경계 -> 심각",
            "관심 > 주의 > 경계 > 심각"
        ],
        "grading_mode": "normalized",
        "explanation": "국가 사이버위기경보는 파랑(관심) -> 노랑(주의) -> 주황(경계) -> 빨강(심각)의 4단계로 발령됩니다 (SRC-10 p.142).",
        "source_id": "SRC-10",
        "source_page": 142,
        "concept_id": "CON-SEC-02",
        "difficulty": "easy",
        "tags": ["사이버위기경보", "관심", "주의", "경계", "심각"]
    },
    {
        "id": "Q-SHORT-083",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "「정보통신기반 보호법」 제16조에 따라 금융·통신 등 분야별 정보통신기반시설을 보호하기 위하여 취약점 및 침해요인과 그 대응방안에 관한 정보를 제공하고, 침해사고 발생 시 실시간 경보·분석체계를 운영하기 위해 구축·운영할 수 있는 전문 조직의 명칭(또는 영문 약어)을 쓰시오.",
        "answer": "정보공유·분석센터",
        "accepted_answers": [
            "정보공유·분석센터",
            "정보공유분석센터",
            "정보공유 분석센터",
            "ISAC",
            "Information Sharing and Analysis Center"
        ],
        "grading_mode": "normalized",
        "explanation": "정보통신기반 보호법 제16조에 따른 정보공유·분석센터(ISAC)는 금융·통신 등 분야별 침해사고 대응 및 경보·분석을 수행하는 조직입니다 (SRC-10 p.139, 145, 13회 기출).",
        "source_id": "SRC-10",
        "source_page": 139,
        "concept_id": "CON-MGT-01",
        "difficulty": "medium",
        "tags": ["정보통신기반보호법", "ISAC", "정보공유분석센터", "침해사고대응"]
    },
    {
        "id": "Q-SHORT-084",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "「개인정보의 안전성 확보조치 기준」 제7조(개인정보의 암호화)에 따라 개인정보처리자가 인터넷망 구간이나 DMZ에 저장할 때 반드시 암호화해야 하며, 내부망에 저장할 때도 원칙적으로 암호화해야 하는 주민등록번호, 여권번호, 운전면허번호, 외국인등록번호의 법정 분류 명칭을 쓰시오.",
        "answer": "고유식별정보",
        "accepted_answers": ["고유식별정보", "고유식별정보등", "고유식별정보 등"],
        "grading_mode": "normalized",
        "explanation": "개인정보보호법상 4대 고유식별정보(주민등록번호, 여권번호, 운전면허번호, 외국인등록번호)는 DMZ 및 내부망 저장 시 암호화 대상입니다 (SRC-11 p.160).",
        "source_id": "SRC-11",
        "source_page": 160,
        "concept_id": "CON-MGT-02",
        "difficulty": "easy",
        "tags": ["개인정보보호법", "고유식별정보", "안전성확보조치", "암호화"]
    },
    {
        "id": "Q-SHORT-085",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "「개인정보 보호법」 제34조 제1항에 따라 개인정보처리자는 개인정보가 분실·도난·유출되었음을 알게 되었을 때 정당한 사유가 없는 한 (          ) 해당 정보주체에게 유출된 항목, 시점 등의 사실을 알려야 한다. 빈칸에 들어갈 법정 통지 시점 원칙을 쓰시오.",
        "answer": "지체 없이",
        "accepted_answers": ["지체 없이", "지체없이", "지체 없이 통지", "지체없이 통지"],
        "grading_mode": "normalized",
        "explanation": "개인정보보호법 제34조 제1항에 따라 유출을 알게 되었을 때에는 지체 없이 정보주체에게 통지하여야 합니다 (SRC-11 p.112).",
        "source_id": "SRC-11",
        "source_page": 112,
        "concept_id": "CON-MGT-02",
        "difficulty": "easy",
        "tags": ["개인정보보호법", "유출통지", "지체없이"]
    },
    {
        "id": "Q-SHORT-086",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "정보보호시스템 공통평가기준(CC; Common Criteria)에서 정보보호 제품의 보안 기능이 안전하게 구현되고 평가되었음을 보증하는 척도로, 1부터 7까지의 7개 단계로 규정된 '평가보증등급'의 영문 약어를 쓰시오.",
        "answer": "EAL",
        "accepted_answers": ["EAL", "Evaluation Assurance Level"],
        "grading_mode": "normalized",
        "explanation": "EAL(Evaluation Assurance Level)은 CC 인증에서 보안 기능의 보증 신뢰성을 1~7등급으로 평가하는 등급 체계입니다 (SRC-10 p.191).",
        "source_id": "SRC-10",
        "source_page": 191,
        "concept_id": "CON-MGT-01",
        "difficulty": "medium",
        "tags": ["CC인증", "EAL", "평가보증등급"]
    },
    {
        "id": "Q-SHORT-087",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "question": "「개인정보 보호법」 제25조(고정형 영상정보처리기기의 설치·운영 제한)에 따라 CCTV를 설치·운영하는 자가 정보주체가 쉽게 알아볼 수 있도록 안내판에 반드시 포함해야 하는 법정 필수 기재사항 중, 아래 빈칸에 들어갈 항목을 쓰시오.\n\n[안내판 기재사항]\n1. (  빈칸  )\n2. 촬영범위 및 시간\n3. 관리책임자의 연락처\n4. 그 밖에 대통령령으로 정하는 사항",
        "answer": "설치 목적 및 장소",
        "accepted_answers": [
            "설치 목적 및 장소",
            "설치목적 및 장소",
            "설치목적및장소",
            "설치 목적 및 설치 장소",
            "설치목적",
            "설치 목적"
        ],
        "grading_mode": "normalized",
        "explanation": "CCTV 안내판의 필수 기재사항은 (1) 설치 목적 및 장소, (2) 촬영범위 및 시간, (3) 관리책임자 연락처 등입니다 (SRC-01 p.65, SRC-11 p.158).",
        "source_id": "SRC-01",
        "source_page": 65,
        "concept_id": "CON-MGT-02",
        "difficulty": "easy",
        "tags": ["CCTV", "안내판", "개인정보보호법", "영상정보처리기기"]
    },
    {
        "id": "Q-DESC-029",
        "type": "descriptive",
        "category": "정보보호 관리 및 법규",
        "score": 12,
        "question": "위험 평가(Risk Assessment) 후 도출된 위험 수준이 수용 가능한 위험 수준(DoA; Degree of Acceptance)을 초과하는 잔여 위험에 대하여 조직이 취할 수 있는 '위험 처리(대응) 4대 기법'의 명칭과 각 기법의 개념 및 적용 방안을 서술하시오.\n\n1) 위험을 유발하는 활동 자체를 중단하거나 포기하는 기법 (3점)\n2) 위험에 따른 손실 책임을 제3자에게 이전하는 기법 (3점)\n3) 보안 통제 대책을 적용하여 위험의 발생 가능성이나 손실 규모를 줄이는 기법 (3점)\n4) 위험의 통제 비용이 손실 비용보다 크거나 수용 가능한 한도 내에 있어 감수하는 기법 (3점)",
        "model_answer": "1) 위험 회피 (Risk Avoidance): 위험을 유발하는 시스템 운영, 비즈니스 프로세스, 서비스 개발 자체를 중단하거나 포기함으로써 위험 발생 원인을 원천 제거하는 전략이다.\n2) 위험 전가 (Risk Transference): 보험 가입, 외주 계약(아웃소싱), 손해배상 조항 등을 통해 위험으로 인해 발생하는 재정적·법적 손실의 책임을 제3자에게 이전하는 전략이다.\n3) 위험 완화 (Risk Mitigation/Reduction): 방화벽 구축, 접근통제 강화, 패치 적용, 암호화 등 적절한 보안 통제를 구현하여 위험의 발생 빈도나 손실 규모를 허용 가능한 수준 이하로 낮추는 전략이다.\n4) 위험 수용 (Risk Acceptance): 위험 완화에 소요되는 비용이 위험이 초래할 손실액보다 크거나 잔여 위험이 DoA 이하로 경미할 때 별도의 추가 대책 없이 위험을 감수하고 모니터링하는 전략이다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 위험 유발 활동을 중단·포기하여 원인을 원천 제거하는 기법",
                "model_answer": "위험 회피(Risk Avoidance): 위험을 초래하는 사업이나 시스템 운영을 중단·포기하여 위험을 원천 제거한다.",
                "rubric": {
                    "keywords": [
                        ["위험 회피", "위험회피", "risk avoidance"],
                        ["중단", "포기", "원천 제거", "제거", "철수"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 손실 책임을 제3자에게 이전하는 기법",
                "model_answer": "위험 전가(Risk Transference): 보험 가입이나 아웃소싱 등을 통해 손실 책임을 제3자에게 이전한다.",
                "rubric": {
                    "keywords": [
                        ["위험 전가", "위험전가", "risk transference"],
                        ["제3자", "보험", "외주", "아웃소싱", "이전", "넘기"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 보안 통제를 적용하여 위험 발생 가능성이나 손실을 줄이는 기법",
                "model_answer": "위험 완화(Risk Mitigation/Reduction): 통제 대책을 적용하여 위험의 발생 가능성과 손실 규모를 줄인다.",
                "rubric": {
                    "keywords": [
                        ["위험 완화", "위험완화", "위험 감소", "risk mitigation", "risk reduction"],
                        ["보안 통제", "가능성", "손실", "줄이", "감소", "낮추"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 비용 효과 또는 경미함을 고려하여 위험을 감수하는 기법",
                "model_answer": "위험 수용(Risk Acceptance): 통제 비용이 손실보다 크거나 잔여 위험이 DoA 이하일 때 위험을 감수한다.",
                "rubric": {
                    "keywords": [
                        ["위험 수용", "위험수용", "risk acceptance"],
                        ["doa", "감수", "비용", "그대로", "수용"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "위험 처리의 4대 전략은 회피, 전가, 완화, 수용으로 분류됩니다 (SRC-10 p.112).",
        "source_id": "SRC-10",
        "source_page": 112,
        "concept_id": "CON-MGT-01",
        "difficulty": "medium",
        "tags": ["위험관리", "위험처리", "위험회피", "위험전가", "위험완화", "위험수용"]
    },
    {
        "id": "Q-DESC-030",
        "type": "descriptive",
        "category": "정보보호 관리 및 법규",
        "score": 12,
        "question": "업무 연속성 계획(BCP)에서 대규모 재난·재해 발생 시 비즈니스를 지속하기 위해 운영하는 재해복구센터(DRS; Disaster Recovery Site)의 4대 구축 유형에 대하여 다음 물음에 답하시오.\n\n1) 주 센터와 완전히 동일한 전산 장비를 갖추고 데이터를 실시간 동기 복제하여 목표 복구 시간(RTO)이 0에 수렴하는 '미러 사이트(Mirror Site)'의 특징과 단점을 서술하시오. (3점)\n2) 주 센터와 동일한 전산 장비를 갖추고 대기 상태를 유지하며 데이터 비동기 복제나 주기적 백업을 통해 수시간(4~24시간) 내 복구 가능한 '핫 사이트(Hot Site)'의 특징을 서술하시오. (3점)\n3) 중요 장비 일부만 설치해 두고 주기적인 백업본을 통해 수일에서 수주 내 복구하는 '웜 사이트(Warm Site)'의 특징을 서술하시오. (3점)\n4) 최소한의 상면 시설(공조, 전력, 네트워크)만 확보해 두고 재해 시 장비를 조달하여 수주에서 수개월이 소요되는 '콜드 사이트(Cold Site)'의 특징과 장점을 서술하시오. (3점)",
        "model_answer": "1) 미러 사이트 (Mirror Site): 주 센터와 동일한 하드웨어 구성을 갖추고 실시간 데이터 동기 복제를 수행하여 재해 시 데이터 손실 없이 즉각(RTO = 0) 업무 전환이 가능하지만, 구축 및 유지관리 비용이 가장 비싸다는 단점이 있다.\n2) 핫 사이트 (Hot Site): 주 센터와 동일한 전산 자원을 상시 대기 가동 상태로 유지하고 비동기 데이터 미러링이나 백업본을 통해 수시간(약 4~24시간) 이내에 업무를 복구할 수 있는 사이트이다.\n3) 웜 사이트 (Warm Site): 주 센터의 중요 장비 일부만을 구축해 두고 데이터는 주기적인 백업 매체로 보관하여, 재해 발생 시 수일~수주 내에 장비를 보완하고 백업본을 복원하여 서비스를 재개하는 절충형 사이트이다.\n4) 콜드 사이트 (Cold Site): 상면 공간, 전력, 공조 등 물리적 인프라만 준비해 두고 서버 장비는 재해 발생 후 조달하여 복구하는 방식으로, RTO가 수주~수개월로 가장 길지만 구축 비용이 가장 저렴하다는 장점이 있다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 미러 사이트(Mirror Site)의 복구 수준과 단점",
                "model_answer": "실시간 데이터 동기 복제를 통해 RTO 0의 즉각 복구가 가능하나 구축 비용이 가장 비싸다.",
                "rubric": {
                    "keywords": [
                        ["미러 사이트", "mirror site", "실시간 동기", "동기 복제", "rto 0", "즉각"],
                        ["비용", "가장 비싸", "고비용", "단점"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 핫 사이트(Hot Site)의 복구 수준과 특징",
                "model_answer": "주 센터와 동일한 장비가 상시 가동 대기 중이며 수시간 내에 업무 복구가 가능하다.",
                "rubric": {
                    "keywords": [
                        ["핫 사이트", "hot site", "상시 대기", "가동 대기", "동일한 장비"],
                        ["수시간", "비동기", "4~24시간", "몇 시간"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 웜 사이트(Warm Site)의 복구 수준과 특징",
                "model_answer": "중요 장비 일부만 설치되어 있으며 백업 데이터를 복원하여 수일~수주 내에 복구한다.",
                "rubric": {
                    "keywords": [
                        ["웜 사이트", "warm site", "일부", "중요 장비 일부"],
                        ["수일", "수주", "백업 데이터", "복원"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 콜드 사이트(Cold Site)의 복구 수준과 장점",
                "model_answer": "상면 인프라만 갖추고 장비는 재해 후 조달하므로 복구는 수주 이상 걸리나 비용이 가장 저렴하다.",
                "rubric": {
                    "keywords": [
                        ["콜드 사이트", "cold site", "상면", "공간만", "인프라만", "조달"],
                        ["저렴", "가장 저렴", "비용 절감", "장점"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "재해복구센터 구축 유형은 복구 시간과 비용에 따라 Mirror Site, Hot Site, Warm Site, Cold Site로 구분됩니다 (SRC-10 p.126, 134).",
        "source_id": "SRC-10",
        "source_page": 126,
        "concept_id": "CON-MGT-04",
        "difficulty": "medium",
        "tags": ["BCP", "DRS", "Mirror", "Hot", "Warm", "Cold"]
    },
    {
        "id": "Q-DESC-031",
        "type": "descriptive",
        "category": "정보보호 관리 및 법규",
        "score": 12,
        "question": "정보통신망법 제45조의3 및 ISMS-P 인증기준에 따라 정보통신서비스 제공자가 지정하는 '정보보호최고책임자(CISO; Chief Information Security Officer)'의 법정 역할 및 업무 내용 4가지를 서술하시오.",
        "model_answer": "1) 정보보호관리체계의 수립·시행 및 지속적 개선\n2) 정보보호 실태와 관행의 정기적인 감사 및 취약점 개선\n3) 정보보호 위험의 식별·평가 및 정보보호 대책의 수립·마련\n4) 정보보호 교육 계획 및 침해사고 모의훈련 계획의 수립·시행",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) CISO의 관리체계 관련 핵심 역할",
                "model_answer": "정보보호관리체계(ISMS)의 수립, 시행 및 개선을 총괄한다.",
                "rubric": {
                    "keywords": [
                        ["정보보호관리체계", "관리체계", "isms"],
                        ["수립", "시행", "개선", "총괄"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) CISO의 점검 및 감사 관련 역할",
                "model_answer": "정보보호 실태와 관행에 대한 정기적인 감사 및 취약점 개선 조치를 수행한다.",
                "rubric": {
                    "keywords": [
                        ["실태", "관행", "감사", "점검", "취약점 개선"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) CISO의 위험관리 관련 역할",
                "model_answer": "정보보호 위험을 식별 및 평가하고 이에 대응하는 정보보호 대책을 마련한다.",
                "rubric": {
                    "keywords": [
                        ["위험", "식별", "평가"],
                        ["보호 대책", "대책 수립", "대책 마련"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) CISO의 교육 및 훈련 관련 역할",
                "model_answer": "임직원 정보보호 교육 및 침해사고 대응 모의훈련 계획을 수립하고 시행한다.",
                "rubric": {
                    "keywords": [
                        ["정보보호 교육", "교육"],
                        ["모의훈련", "훈련", "침해사고"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "CISO는 관리체계 수립, 실태 감사, 위험평가 및 대책 마련, 교육/모의훈련 총괄 등의 법정 R&R을 갖습니다 (SRC-10 p.165, 181).",
        "source_id": "SRC-10",
        "source_page": 181,
        "concept_id": "CON-MGT-03",
        "difficulty": "medium",
        "tags": ["CISO", "정보통신망법", "ISMS-P", "직무역할"]
    },
    {
        "id": "Q-DESC-032",
        "type": "descriptive",
        "category": "정보보호 관리 및 법규",
        "score": 12,
        "question": "개인정보보호위원회 고시 「개인정보의 안전성 확보조치 기준」에 따른 '접근권한 관리' 및 '인터넷망 차단(망분리)' 의무 사항에 대하여 다음 물음에 답하시오.\n\n1) 개인정보취급자의 인사이동, 퇴직 등 변경 사유가 발생했을 때 접근권한의 변경·말소 조치 기한과, 접근권한 부여·변경·말소 내역의 최소 법정 보관 기간을 각각 쓰시오. (4점)\n2) 개인정보취급자가 개인정보처리시스템에 접속할 때 적용해야 하는 패스워드 및 인증 안전성 확보 기준 2가지를 서술하시오. (4점)\n3) 개인정보처리자가 개인정보취급자의 컴퓨터 등에 대해 물리적 또는 논리적으로 인터넷망을 차단(망분리)해야 하는 법적 대상 기준을 서술하시오. (4점)",
        "model_answer": "1) 권한 변경 기한 및 보관 기간: 인사이동, 퇴직 등으로 개인정보취급자의 업무가 변경된 경우 '지체 없이(5일 이내)' 접근권한을 변경 또는 말소하여야 하며, 권한 부여·변경·말소에 대한 기록은 최소 '3년' 이상 보관하여야 한다.\n2) 패스워드 및 인증 기준:\n- 일정 횟수 이상 인증 실패 시 접근 차단 또는 지연 조치\n- 외부에서 접속 시 VPN 또는 전용선 등 안전한 접속수단 및 2차 인증 적용\n3) 망분리 의무 대상 기준: 개인정보처리시스템에서 개인정보를 다운로드 또는 파기하거나, 개인정보처리시스템의 접근권한을 설정할 수 있는 권한을 가진 개인정보취급자의 컴퓨터 등에 대해서는 물리적 또는 논리적으로 인터넷망을 차단하여야 한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 접근권한 변경 조치 기한과 권한 관리 기록 보관 기간",
                "model_answer": "지체 없이 권한을 변경·말소하며, 기록은 최소 3년 이상 보관해야 한다.",
                "rubric": {
                    "keywords": [
                        ["지체 없이", "지체없이", "5일 이내"],
                        ["3년", "3년 이상"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 개인정보처리시스템 접속 시 인증 안전성 조치 2가지",
                "model_answer": "일정 횟수 인증 실패 시 접속 차단, 외부 접속 시 VPN 또는 2차 인증 등 안전한 접속수단을 적용한다.",
                "rubric": {
                    "keywords": [
                        ["인증 실패", "실패 횟수", "차단", "지연"],
                        ["vpn", "2차 인증", "전용선", "안전한 접속수단", "비밀번호 규칙"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 개인정보취급자 컴퓨터의 인터넷망 차단(망분리) 대상 기준",
                "model_answer": "개인정보를 다운로드, 파기하거나 접근권한을 설정할 수 있는 취급자의 컴퓨터를 대상으로 한다.",
                "rubric": {
                    "keywords": [
                        ["다운로드", "파기", "출력"],
                        ["접근권한 설정", "권한 설정", "접근 권한 설정", "인터넷망 차단", "망분리"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "안전성 확보조치 기준에 따라 권한 기록은 3년 보관해야 하며 다운로드/파기 권한자는 인터넷망 차단 대상입니다 (SRC-11 p.122~125).",
        "source_id": "SRC-11",
        "source_page": 125,
        "concept_id": "CON-MGT-02",
        "difficulty": "medium",
        "tags": ["개인정보보호법", "안전성확보조치", "망분리", "접근권한"]
    }
]
