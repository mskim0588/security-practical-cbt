# -*- coding: utf-8 -*-
"""
Batch 2 - Chunk 2: SRC-09 Descriptive (4 questions) & SRC-04 Short (5 questions)
Q-DESC-025 ~ Q-DESC-028
Q-SHORT-075 ~ Q-SHORT-079
"""

CHUNK_2_QUESTIONS = [
    {
        "id": "Q-DESC-025",
        "type": "descriptive",
        "category": "정보보안 일반 및 암호학",
        "score": 12,
        "question": "암호 분석(Cryptanalysis)에서 공격자가 확보할 수 있는 정보의 양과 수준에 따라 분류되는 4대 암호 해독 공격 모델에 대하여 각 물음에 답하시오.\n\n1) 오직 도청 등을 통해 획득한 암호문(C)만을 가지고 평문이나 키를 알아내려는 가장 기본적인 공격 모델의 명칭과 영문 약어를 쓰시오. (3점)\n2) 공격자가 사전에 특정 평문(P)과 이에 대응하는 암호문(C) 쌍의 일부를 이미 알고 있는 상태에서 전체 암호 시스템을 해독하려는 공격 모델의 명칭과 영문 약어를 쓰시오. (3점)\n3) 공격자가 임의의 평문(P)을 선택하여 암호화 장치에 입력하고 그에 대응하는 암호문(C)을 얻을 수 있는 환경에서 키를 해독하려는 공격 모델의 명칭과 영문 약어를 쓰시오. (3점)\n4) 공격자가 임의의 암호문(C)을 선택하여 복호화 장치에 입력하고 그에 대응하는 평문(P)을 얻을 수 있는 환경에서 수행하는 가장 강력한 공격 모델의 명칭과 영문 약어를 쓰시오. (3점)",
        "model_answer": "1) 암호문 단독 공격 (COA; Ciphertext-Only Attack): 공격자가 암호문만을 가지고 평문의 통계적 특성이나 언어적 특성을 분석하여 해독하는 공격이다.\n2) 알려진 평문 공격 (KPA; Known-Plaintext Attack): 공격자가 일부 평문과 그에 대응하는 암호문 쌍을 이미 확보한 상태에서 암호키나 전체 평문을 해독하는 공격이다.\n3) 선택 평문 공격 (CPA; Chosen-Plaintext Attack): 공격자가 자신이 선택한 임의의 평문을 암호화 장치에 주입하여 대응하는 암호문을 획득함으로써 암호 알고리즘이나 키를 해독하는 공격이다.\n4) 선택 암호문 공격 (CCA; Chosen-Ciphertext Attack): 공격자가 자신이 선택한 임의의 암호문을 복호화 장치에 주입하여 대응하는 평문을 획득할 수 있는 가장 높은 수준의 공격 모델이다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 암호문(C)만을 확보한 상태에서 해독하는 공격 모델의 명칭과 영문 약어",
                "model_answer": "암호문 단독 공격 (COA; Ciphertext-Only Attack)",
                "rubric": {
                    "keywords": [
                        ["암호문 단독 공격", "암호문단독공격", "coa", "ciphertext-only attack"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 일부 평문-암호문 쌍을 알고 있는 상태에서 해독하는 공격 모델의 명칭과 영문 약어",
                "model_answer": "알려진 평문 공격 (KPA; Known-Plaintext Attack)",
                "rubric": {
                    "keywords": [
                        ["알려진 평문 공격", "알려진평문공격", "기지 평문 공격", "kpa", "known-plaintext attack"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 공격자가 선택한 평문에 대한 암호문을 얻을 수 있는 공격 모델의 명칭과 영문 약어",
                "model_answer": "선택 평문 공격 (CPA; Chosen-Plaintext Attack)",
                "rubric": {
                    "keywords": [
                        ["선택 평문 공격", "선택평문공격", "cpa", "chosen-plaintext attack"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 공격자가 선택한 암호문에 대한 평문을 얻을 수 있는 가장 강력한 공격 모델의 명칭과 영문 약어",
                "model_answer": "선택 암호문 공격 (CCA; Chosen-Ciphertext Attack)",
                "rubric": {
                    "keywords": [
                        ["선택 암호문 공격", "선택암호문공격", "cca", "chosen-ciphertext attack"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "암호 분석의 4대 공격 모델은 공격자가 확보한 정보 수준에 따라 COA, KPA, CPA, CCA로 분류됩니다 (SRC-09 p.5~8).",
        "source_id": "SRC-09",
        "source_page": 5,
        "concept_id": "CON-CRY-03",
        "difficulty": "medium",
        "tags": ["암호학", "암호분석", "COA", "KPA", "CPA", "CCA"]
    },
    {
        "id": "Q-DESC-026",
        "type": "descriptive",
        "category": "정보보안 일반 및 암호학",
        "score": 12,
        "question": "현대 대칭키 블록 암호 알고리즘의 양대 구조인 페이스텔(Feistel) 구조와 SPN(Substitution-Permutation Network) 구조에 대하여 다음 물음에 답하시오.\n\n1) 페이스텔(Feistel) 구조의 데이터 분할 방식 및 동작 원리를 라운드 함수 F와 XOR 연산을 중심으로 서술하시오. (4점)\n2) SPN 구조의 치환(Substitution) 계층과 전치(Permutation) 계층의 역할 및 혼돈(Confusion)과 확산(Diffusion) 관점에서의 동작 원리를 서술하시오. (4점)\n3) 두 구조의 복호화 과정에서 '라운드 함수(F함수 또는 S-box)의 역함수 존재 필요성' 관점의 결정적인 차이점을 비교하여 서술하시오. (4점)",
        "model_answer": "1) 페이스텔(Feistel) 구조: 평문 블록을 좌측(L)과 우측(R) 두 개의 반블록으로 분할한 후, 한쪽 반블록을 라운드 함수 F와 라운드 키에 입력하고 그 출력값을 다른 쪽 반블록과 XOR 연산한 뒤 두 반블록의 위치를 교환(Swap)하며 다단계 라운드를 반복한다.\n2) SPN 구조: 평문 블록 전체에 대해 S-box를 이용한 비트 치환(Substitution)을 통해 평문과 암호키 사이의 관계를 숨기는 혼돈(Confusion)을 제공하고, P-box를 이용한 위치 전치(Permutation)를 통해 평문의 통계적 특성을 블록 전체로 분산시키는 확산(Diffusion)을 교대로 반복 적용한다.\n3) 역함수 필요성 차이: 페이스텔 구조는 복호화 시 암호화와 동일한 회로 구조를 사용하고 라운드 키의 순서만 역순으로 적용하므로 라운드 함수 F의 역함수가 존재할 필요가 없다. 반면 SPN 구조는 복호화 시 치환과 전치 과정을 역방향으로 수행해야 하므로 S-box와 P-box의 역연산(역함수)이 반드시 수학적으로 존재해야 한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 페이스텔 구조의 데이터 분할 및 라운드 동작 원리",
                "model_answer": "평문을 좌/우 반블록으로 나누어 한쪽을 라운드 함수 F에 통과시킨 뒤 반대쪽과 XOR하고 좌우를 교환하는 과정을 반복한다.",
                "rubric": {
                    "keywords": [
                        ["좌우", "좌/우", "반블록", "두 개", "분할"],
                        ["라운드 함수", "f함수", "f 함수", "xor", "교환", "swap"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) SPN 구조의 치환(S-box)과 전치(P-box) 계층의 동작 원리",
                "model_answer": "S-box를 통한 비트 치환으로 혼돈을 달성하고, P-box를 통한 위치 전치로 확산을 달성하는 과정을 번갈아 반복한다.",
                "rubric": {
                    "keywords": [
                        ["s-box", "sbox", "치환", "혼돈", "confusion"],
                        ["p-box", "pbox", "전치", "확산", "diffusion"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 복호화 시 라운드 함수의 역함수 필요 여부 관점에서 두 구조 비교",
                "model_answer": "페이스텔은 라운드 키 순서만 바꾸면 되므로 F함수의 역함수가 불필요하나, SPN은 S-box와 P-box의 역연산이 반드시 존재해야 한다.",
                "rubric": {
                    "keywords": [
                        ["페이스텔", "역함수 불필요", "역함수 필요 없음", "역함수가 존재할 필요"],
                        ["spn", "역함수 필요", "역연산 필요", "역함수가 존재", "역연산이 존재"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "대칭키 블록 암호는 Feistel(DES, SEED)과 SPN(AES, ARIA) 구조로 나뉘며, 복호화 시 라운드 함수 역연산 필요 여부가 핵심 차이점입니다 (SRC-09 p.18, 23).",
        "source_id": "SRC-09",
        "source_page": 18,
        "concept_id": "CON-CRY-01",
        "difficulty": "hard",
        "tags": ["블록암호", "Feistel", "SPN", "혼돈", "확산", "역함수"]
    },
    {
        "id": "Q-DESC-027",
        "type": "descriptive",
        "category": "정보보안 일반 및 암호학",
        "score": 12,
        "question": "암호학적 일방향 해시 함수(Cryptographic Hash Function)가 안전성을 보장하기 위해 반드시 만족해야 하는 3대 안전성 특성에 대하여 다음 물음에 답하시오.\n\n1) '역상 저항성(제1 역상 저항성; Pre-image Resistance)'의 개념과 수학적 정의를 서술하시오. (4점)\n2) '제2 역상 저항성(약한 충돌 저항성; Second Pre-image Resistance)'의 개념과 수학적 정의를 서술하시오. (4점)\n3) '충돌 저항성(강한 충돌 저항성; Collision Resistance)'의 개념과 수학적 정의를 서술하시오. (4점)",
        "model_answer": "1) 역상 저항성(제1 역상 저항성): 임의의 주어진 해시값 y에 대해 H(x) = y를 만족하는 원래의 입력값 x를 찾아내는 것이 계산상 불가능해야 한다는 특성이다.\n2) 제2 역상 저항성(약한 충돌 저항성): 특정 입력값 x가 주어졌을 때, x와 다른 입력값 x'(x ≠ x')이면서 동일한 해시값 H(x) = H(x')을 갖는 x'를 찾아내는 것이 계산상 불가능해야 한다는 특성이다.\n3) 충돌 저항성(강한 충돌 저항성): 사전에 주어진 입력값 없이, 서로 다른 임의의 두 입력쌍 x1과 x2(x1 ≠ x2)에 대해 동일한 해시값 H(x1) = H(x2)을 만족하는 쌍을 찾아내는 것이 계산상 불가능해야 한다는 특성이다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 역상 저항성(제1 역상 저항성)의 개념과 정의",
                "model_answer": "주어진 해시값 y에 대하여 H(x) = y가 되는 원래 입력값 x를 계산하기 어렵다는 특성이다.",
                "rubric": {
                    "keywords": [
                        ["역상 저항성", "제1 역상", "pre-image"],
                        ["해시값", "y", "입력값", "x", "찾아내", "계산상 불가능", "원래"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 제2 역상 저항성(약한 충돌 저항성)의 개념과 정의",
                "model_answer": "주어진 입력값 x에 대해 동일한 해시값을 갖는 서로 다른 입력값 x'를 찾기 어렵다는 특성이다.",
                "rubric": {
                    "keywords": [
                        ["제2 역상", "약한 충돌", "second pre-image"],
                        ["동일한 해시값", "서로 다른 입력값", "x'", "x와 다른", "x != x'"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 충돌 저항성(강한 충돌 저항성)의 개념과 정의",
                "model_answer": "임의의 서로 다른 두 입력쌍 x1, x2가 동일한 해시값을 갖지 않도록 하는(쌍을 찾기 어렵다는) 특성이다.",
                "rubric": {
                    "keywords": [
                        ["충돌 저항성", "강한 충돌", "collision resistance"],
                        ["서로 다른 두", "임의의 두", "x1", "x2", "동일한 해시값"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "해시 함수의 3대 안전성 요건은 제1 역상 저항성, 제2 역상 저항성, 충돌 저항성입니다 (SRC-09 p.50).",
        "source_id": "SRC-09",
        "source_page": 50,
        "concept_id": "CON-CRY-02",
        "difficulty": "medium",
        "tags": ["해시함수", "역상저항성", "제2역상저항성", "충돌저항성"]
    },
    {
        "id": "Q-DESC-028",
        "type": "descriptive",
        "category": "정보보안 일반 및 암호학",
        "score": 12,
        "question": "공개키 암호 기반의 전자서명(Digital Signature) 메커니즘에 대하여 다음 물음에 답하시오.\n\n1) 송신자가 메시지 M에 대하여 전자서명을 생성하는 과정을 송신자 개인키(KR)와 해시 함수(H)를 이용하여 서술하시오. (4점)\n2) 수신자가 수신된 메시지와 전자서명을 검증하는 과정을 송신자 공개키(KU)와 해시 함수(H)를 이용하여 서술하시오. (4점)\n3) 전자서명이 제공하는 3대 핵심 보안 서비스(기밀성을 제외한 인증, 무결성, 부인방지)의 개념을 각각 서술하시오. (4점)",
        "model_answer": "1) 서명 생성 과정: 송신자는 원본 메시지 M을 일방향 해시 함수 H에 입력하여 고정 길이의 메시지 다이제스트 H(M)를 생성한 후, 송신자 자신의 개인키(KR)로 암호화하여 전자서명 S를 생성하고 원본 메시지와 함께 전송한다.\n2) 서명 검증 과정: 수신자는 전송받은 원본 메시지 M에 대해 동일한 해시 함수를 적용하여 다이제스트 H(M)를 직접 계산하고, 동시에 전송받은 전자서명 S를 송신자의 공개키(KU)로 복호화하여 추출된 다이제스트와 직접 계산한 다이제스트가 일치하는지 비교하여 검증한다.\n3) 3대 보안 서비스:\n- 서명자 인증(Authentication): 송신자의 개인키로 암호화되었으므로 서명자가 진정한 송신자임을 증명\n- 메시지 무결성(Integrity): 전송 중 메시지가 위·변조되지 않았음을 증명\n- 부인 방지(Non-repudiation): 송신자 본인의 개인키로 서명했으므로 사후에 메시지 송신 사실을 부인할 수 없음",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 송신자의 전자서명 생성 과정",
                "model_answer": "메시지를 해시하여 다이제스트를 생성한 뒤 송신자의 개인키로 암호화하여 서명을 생성한다.",
                "rubric": {
                    "keywords": [
                        ["해시", "다이제스트", "h(m)"],
                        ["송신자 개인키", "송신자의 개인키", "개인키로 암호화", "개인키"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 수신자의 전자서명 검증 과정",
                "model_answer": "서명을 송신자의 공개키로 복호화한 해시값과 원본 메시지를 직접 해시한 값이 일치하는지 비교한다.",
                "rubric": {
                    "keywords": [
                        ["송신자 공개키", "송신자의 공개키", "공개키로 복호화", "공개키"],
                        ["해시값 비교", "다이제스트 비교", "일치", "동일"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 전자서명의 3대 보안 서비스(인증, 무결성, 부인방지)의 개념",
                "model_answer": "서명자 신원을 확인하는 인증, 위변조 여부를 확인하는 무결성, 송신 사실을 부인할 수 없는 부인방지를 제공한다.",
                "rubric": {
                    "keywords": [
                        ["인증", "authentication", "신원 확인", "진정한 송신자"],
                        ["무결성", "integrity", "위변조", "변조되지"],
                        ["부인방지", "부인 방지", "non-repudiation", "부인할 수 없"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "전자서명은 송신자 개인키로 해시값을 암호화하고 송신자 공개키로 복호화하여 인증, 무결성, 부인방지를 제공합니다 (SRC-09 p.127).",
        "source_id": "SRC-09",
        "source_page": 127,
        "concept_id": "CON-CRY-02",
        "difficulty": "medium",
        "tags": ["전자서명", "공개키", "개인키", "인증", "무결성", "부인방지"]
    },
    {
        "id": "Q-SHORT-075",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "다음 설명에 해당하는 대표적인 오픈소스 침투 테스트 및 모의해킹 프레임워크의 명칭을 영문 또는 국문으로 쓰시오.\n\n[설명]\n- HD Moore가 2003년 펄(Perl) 기반으로 최초 개발하였으며, 이후 루비(Ruby) 언어로 전면 재작성된 침투 테스트 도구이다.\n- 대상 시스템의 취약점을 탐지하고 원격 공격을 수행하는 Exploit 모듈, 공격 성공 후 실행되는 Payload 모듈, 네트워크 스캐닝을 지원하는 Auxiliary 모듈 등으로 구성된다.\n- 칼리 리눅스(Kali Linux)에 기본 탑재되어 있으며, `msfconsole` 대화형 명령 인터페이스를 통해 사용된다.",
        "answer": "Metasploit",
        "accepted_answers": ["Metasploit", "메타스플로잇", "메타스플로이트", "Metasploit Framework", "MSF"],
        "grading_mode": "normalized",
        "explanation": "Metasploit은 취약점 점검, 익스플로잇 실행 및 침투 테스트를 위한 대표적인 모의해킹 프레임워크입니다 (SRC-04 p.61).",
        "source_id": "SRC-04",
        "source_page": 61,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["모의해킹", "침투테스트", "Metasploit", "msfconsole"]
    },
    {
        "id": "Q-SHORT-076",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "포트 스캐닝 도구 Nmap에서 3-way 핸드셰이킹을 완전하게 완료하지 않고 SYN 패킷만을 전송한 후 SYN+ACK 응답이 오면 즉시 RST 패킷을 전송하여 연결을 강제 종료함으로써 대상 시스템의 로그에 연결 흔적을 최소화하는 'TCP 반개방(Half-Open / Stealth) 스캔'을 수행하기 위한 명령줄 옵션을 쓰시오.",
        "answer": "-sS",
        "accepted_answers": ["-sS", "sS"],
        "grading_mode": "strict",
        "explanation": "Nmap의 -sS 옵션은 TCP SYN 반개방(Half-Open) 스텔스 스캔 옵션입니다 (SRC-04 p.70).",
        "source_id": "SRC-04",
        "source_page": 70,
        "concept_id": "CON-NET-01",
        "difficulty": "medium",
        "tags": ["Nmap", "스캔", "Half-Open", "SYN스캔"]
    },
    {
        "id": "Q-SHORT-077",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "리눅스 네트워크 패킷 캡처 및 분석 도구인 `tcpdump`에서 패킷 캡처 시 IP 주소를 도메인 네임(호스트명)으로 역방향 DNS 변환(Reverse DNS Resolution)하지 않고 숫자 형태의 IP 주소 그대로 화면에 빠르게 출력하도록 지정하는 명령줄 옵션을 쓰시오.",
        "answer": "-n",
        "accepted_answers": ["-n", "-nn"],
        "grading_mode": "strict",
        "explanation": "tcpdump에서 -n 옵션은 IP 주소를 호스트명으로 변환하지 않고 숫자 IP로 출력하며, -nn 옵션은 포트 번호까지 숫자로 출력합니다 (SRC-04 p.76, 77).",
        "source_id": "SRC-04",
        "source_page": 77,
        "concept_id": "CON-NET-01",
        "difficulty": "easy",
        "tags": ["tcpdump", "패킷캡처", "DNS변환방지"]
    },
    {
        "id": "Q-SHORT-078",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "다음 설명에 해당하는 웹 애플리케이션 서비스 거부(DoS) 공격 기법의 영문 명칭을 쓰시오.\n\n[설명]\n- HTTP POST 요청 시 헤더의 Content-Length를 수만 바이트 이상의 비정상적으로 큰 값으로 설정하여 웹 서버로 전송한다.\n- 이후 실제 메시지 본문(Body) 데이터를 한 번에 전송하지 않고 1바이트씩 매우 긴 시간 간격을 두고 지연 전송하여 웹 서버의 요청 수신 버퍼와 연결 세션을 장시간 점유함으로써 정상적인 사용자의 요청을 처리하지 못하게 고갈시키는 Slow HTTP DoS 공격이다.",
        "answer": "RUDY",
        "accepted_answers": ["RUDY", "R-U-Dead-Yet", "루디", "Slow HTTP POST DoS"],
        "grading_mode": "normalized",
        "explanation": "RUDY(R-U-Dead-Yet)는 Content-Length를 크게 설정한 후 본문 데이터를 극도로 지연 전송하여 웹서버 연결을 고갈시키는 공격입니다 (SRC-04 p.152).",
        "source_id": "SRC-04",
        "source_page": 152,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["DoS", "RUDY", "SlowHTTP", "Content-Length"]
    },
    {
        "id": "Q-SHORT-079",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "리눅스 및 유닉스 시스템의 기본 명령 쉘인 GNU Bash에서 환경변수의 함수 정의 구문 뒤에 임의의 악성 명령어를 삽입할 경우 환경변수 파싱 취약점으로 인해 비인가 명령어가 원격에서 루트 권한으로 실행되는 취약점(CVE-2014-6271)의 통칭을 쓰시오.",
        "answer": "Shellshock",
        "accepted_answers": ["Shellshock", "쉘쇼크", "셸쇼크", "Bashdoor"],
        "grading_mode": "normalized",
        "explanation": "Shellshock(CVE-2014-6271)는 GNU Bash 환경변수 함수 파싱 버그를 이용해 임의 명령어를 실행하는 취약점입니다 (SRC-04 p.132).",
        "source_id": "SRC-04",
        "source_page": 132,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["Bash", "Shellshock", "취약점", "CVE-2014-6271"]
    }
]
