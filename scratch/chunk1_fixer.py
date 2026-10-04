# -*- coding: utf-8 -*-
"""
Chunk 1 Fixer: Q-SHORT-001 to Q-SHORT-030
Fixes:
- P1-1: Eliminates "표준 정답" placeholder in why_correct and embeds the official representative answer.
- P1-3: Replaces concept-inherited traps with question-specific, realistic traps.
"""

import json

CHUNK1_FIXES = {
    "Q-SHORT-001": {
        # PIA risk formula: 자산가치(영향도) + ((침해요인 발생 가능성 + 법적 취약성) / 2)
        "traps": [
            {
                "confused_term_or_misunderstanding": "위험도 산정 공식에서 침해요인 발생 가능성과 법적 취약성의 평균(/2) 처리를 누락하고 단순 합산",
                "explanation": "개인정보 영향평가(PIA) 지침상 위험도는 '자산가치 + (침해요인 발생가능성 + 법적 취약성)/2'로 취약성 요인의 산술 평균을 가산하는 구조입니다."
            }
        ]
    },
    "Q-SHORT-002": {
        # DB encryption methods: API, Plug-in, TDE
        "traps": [
            {
                "confused_term_or_misunderstanding": "TDE 방식을 애플리케이션 레벨의 암호화로 혼동",
                "explanation": "TDE(Transparent Data Encryption)는 DB 커널/엔진 레벨에서 파일 및 테이블스페이스를 암호화하는 방식으로, 애플리케이션 수정이 전혀 필요 없는 특징이 있습니다."
            },
            {
                "confused_term_or_misunderstanding": "Plug-in 방식과 API 방식의 에이전트 설치 위치 혼동",
                "explanation": "API 방식은 애플리케이션 서버에서 암/복호화 API 라이브러리를 호출하며, Plug-in 방식은 DB 서버 엔진 내부에 모듈(확장 모듈) 형태로 설치되어 작동합니다."
            }
        ]
    },
    "Q-SHORT-003": {
        # WPA2 (IEEE 802.11i, AES-CCMP)
        "ans_replace": "WPA2",
        "traps": [
            {
                "confused_term_or_misunderstanding": "WPA2의 핵심 암호 알고리즘을 WEP/WPA의 RC4/TKIP으로 작성",
                "explanation": "초기 WEP 및 WPA는 RC4 기반의 취약한 스트림 암호(TKIP)를 사용했으나, WPA2는 강력한 AES-CCMP 블록 암호 알고리즘을 표준으로 강제합니다."
            },
            {
                "confused_term_or_misunderstanding": "WPA2-Enterprise의 인증 주체(Authenticator)를 백엔드 RADIUS 인증 서버로 혼동",
                "explanation": "802.1X 구조에서 무선 AP는 중간 중계자인 Authenticator이며, 실제 인증 및 자격증명 검증은 백엔드의 Authentication Server(RADIUS)가 수행합니다."
            }
        ]
    },
    "Q-SHORT-004": {
        # VLAN: Static(포트 기반) vs Dynamic(MAC/IP 기반)
        "traps": [
            {
                "confused_term_or_misunderstanding": "정적 VLAN을 MAC 주소 기반 매핑으로 혼동",
                "explanation": "정적(Static) VLAN은 스위치의 물리적 포트 번호에 VLAN ID를 고정 할당하는 포트 기반 매핑 방식이며, 단말의 MAC 주소에 따라 유동적으로 할당되는 방식은 동적(Dynamic) VLAN입니다."
            }
        ]
    },
    "Q-SHORT-005": {
        # robots.txt (검색엔진 크롤러 제어)
        "ans_replace": "robots.txt",
        "traps": [
            {
                "confused_term_or_misunderstanding": "robots.txt 파일에 기밀 디렉터리를 Disallow로 등록하면 웹 접근이 원천 차단된다고 오해",
                "explanation": "robots.txt는 정직한 검색엔진 크롤러에 대한 권고안일 뿐 강제적인 접근 통제 메커니즘이 아니며, 오히려 공격자에게 은닉 관리자 URL/디렉터리 목록을 알려주는 정보 노출 취약점이 될 수 있습니다."
            },
            {
                "confused_term_or_misunderstanding": "robots.txt의 제어 대상을 일반 웹 브라우저 클라이언트로 혼동",
                "explanation": "robots.txt는 웹 크롤러(User-agent: Googlebot 등)를 대상으로 수집 정책을 선언하는 규약이며, 일반 웹 사용자의 페이지 요청에는 웹 서버 인가 정책(.htaccess, Web Server Config)이 적용됩니다."
            }
        ]
    },
    "Q-SHORT-006": {
        # ISO 31000 위험사정 3단계: 식별, 분석, 평가
        "traps": [
            {
                "confused_term_or_misunderstanding": "위험사정(Risk Assessment) 단계와 위험처리(Risk Treatment) 단계를 혼동",
                "explanation": "위험사정(Risk Assessment)은 위험 식별(Identification) -> 위험 분석(Analysis) -> 위험 평가(Evaluation) 3단계로 구성되며, 위험 완화/회피 등 대응 방안 수립은 이후의 '위험처리' 단계입니다."
            }
        ]
    },
    "Q-SHORT-007": {
        # DLP (Data Loss Prevention, 정보유출방지)
        "ans_replace": "DLP",
        "traps": [
            {
                "confused_term_or_misunderstanding": "DLP를 문서 자체를 암호화하는 DRM과 동일시",
                "explanation": "DRM은 파일 자체를 암호화하여 인가된 권한자만 열람/편집하도록 제어하는 기술인 반면, DLP는 네트워크나 USB 등 엔드포인트 전송 채널에서 주민번호/기밀 패턴을 탐지하여 전송 및 유출을 차단하는 솔루션입니다."
            }
        ]
    },
    "Q-SHORT-008": {
        # /proc (가상 파일시스템 procfs)
        "ans_replace": "/proc",
        "traps": [
            {
                "confused_term_or_misunderstanding": "/proc을 디스크 공간을 실질적으로 차지하는 영구 저장소 디렉터리로 오해",
                "explanation": "/proc 디렉터리는 리눅스 커널 메모리에 상주하는 프로세스 및 시스템 리소스 정보를 파일 형태로 투영해 주는 가상 파일시스템(procfs)으로, 실제 하드디스크 블록을 소비하지 않습니다."
            },
            {
                "confused_term_or_misunderstanding": "/sys 디렉터리나 /dev 디렉터리와 역할 혼동",
                "explanation": "/dev는 물리/가상 하드웨어 장치 노드 파일들을 관리하고, /sys는 디바이스 모델 트리와 드라이버 매개변수를 관리하며, 실행 중인 프로세스(PID)별 상세 런타임 정보는 /proc에서 관리합니다."
            }
        ]
    },
    "Q-SHORT-009": {
        # 랜덤 라운딩 (Random Rounding)
        "ans_replace": "랜덤 라운딩",
        "traps": [
            {
                "confused_term_or_misunderstanding": "랜덤 라운딩을 일반 올림/내림(제어 올림)과 동일하다고 생각",
                "explanation": "일반 제어 올림(Rounding)은 수학적 반올림 기준(예: 5 이상 올림)을 일관되게 적용하지만, 랜덤 라운딩은 특정 확률(가중치)에 따라 올림 또는 내림을 무작위 결정하여 통계적 편향을 완화하는 비식별화 기법입니다."
            }
        ]
    },
    "Q-SHORT-010": {
        # Log4j (Log4Shell CVE-2021-44228, JNDI Injection)
        "ans_replace": "Log4j",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Log4Shell 취약점을 단순한 로그 줄바꿈/인젝션(CRLF)으로 오해",
                "explanation": "Log4Shell은 단순 로그 조작이 아니라 Log4j의 JNDI Lookup 기능(${jndi:ldap://...})을 악용하여 원격 공격자가 제어하는 악성 자바 클래스를 서버가 직접 다운로드/실행하게 만드는 치명적인 원격 코드 실행(RCE) 취약점입니다."
            }
        ]
    },
    "Q-SHORT-011": {
        # Windows Server HTTP.sys 로그 저장 경로 (HTTPERR, DHCP)
        "traps": [
            {
                "confused_term_or_misunderstanding": "HTTP.sys 오류 로그 폴더명을 IIS 웹사이트 로그 폴더(W3SVC1)와 혼동",
                "explanation": "IIS 사이트의 일반 액세스 로그는 'W3SVC<사이트ID>' 폴더에 저장되지만, 커널 레벨 드라이버인 HTTP.sys에서 요청을 거부하거나 큐 초과로 발생한 오류는 'HTTPERR' 폴더에 기록됩니다."
            }
        ]
    },
    "Q-SHORT-012": {
        # Linux PAM 4대 모듈 타입: auth, account, password, session
        "traps": [
            {
                "confused_term_or_misunderstanding": "account 모듈의 역할을 패스워드 일치 검증으로 오해",
                "explanation": "패스워드나 인증 토큰의 유효성을 검증하는 것은 'auth' 모듈의 역할이며, 'account' 모듈은 계정 유효기간 만료 여부, 로그인 가능 시간대, 접근 권한 등 계정의 상태 조건을 검사합니다."
            },
            {
                "confused_term_or_misunderstanding": "session 모듈을 사용자 인증 단계로 혼동",
                "explanation": "session 모듈은 인증 전후에 사용자 환경(홈 디렉터리 마운트, 리소스 한도 설정, 로그인/로그아웃 로깅 등)을 설정하고 정리하는 역할을 수행합니다."
            }
        ]
    },
    "Q-SHORT-013": {
        # 위험관리 3단계: (A) 위험분석, (B) 위험평가
        "traps": [
            {
                "confused_term_or_misunderstanding": "위험분석(Risk Analysis)과 위험평가(Risk Evaluation)의 순서 및 정의 혼동",
                "explanation": "위험분석은 자산 가치, 위협, 취약성을 종합하여 위험의 크기(수치/수준)를 도출하는 과정이며, 위험평가는 도출된 위험을 수용 가능 위험 수준(DoA)과 비교하여 처리 우선순위를 결정하는 과정입니다."
            }
        ]
    },
    "Q-SHORT-014": {
        # 라우팅 프로토콜: (A) IGP, (B) EGP (또는 BGP)
        "traps": [
            {
                "confused_term_or_misunderstanding": "동일 자치시스템(AS) 내부 라우팅 프로토콜과 AS 간 라우팅 프로토콜 명칭 혼동",
                "explanation": "단일 조직/관리 도메인(AS) 내부에서 경로 정보를 주고받는 것은 IGP(RIP, OSPF)이며, 서로 다른 독립된 AS 간에 경로를 교환하는 외부 게이트웨이 프로토콜은 EGP/BGP입니다."
            }
        ]
    },
    "Q-SHORT-015": {
        # 리눅스 주요 로그: (A) wtmp, (B) btmp, (C) lastlog
        "traps": [
            {
                "confused_term_or_misunderstanding": "wtmp와 utmp의 기록 범위 혼동",
                "explanation": "utmp는 현재 시스템에 로그인되어 있는 사용자의 상태만을 실시간으로 유지하는 반면, wtmp는 성공한 모든 로그인/로그아웃 및 시스템 재부팅 이력을 누적 기록합니다."
            },
            {
                "confused_term_or_misunderstanding": "btmp 로그를 일반 텍스트 편집기(vi, cat)로 열람 가능하다고 오해",
                "explanation": "btmp와 wtmp는 바이너리 포맷 파일이므로 cat이나 vi로 열면 깨져 보이며, 반드시 'last -f /var/log/btmp' 또는 'lastb' 전용 명령어로 열람해야 합니다."
            }
        ]
    },
    "Q-SHORT-016": {
        # /etc/passwd 필드: root:x:0:0:root:/root:/bin/bash (UID, GID, 홈디렉터리, 쉘)
        "traps": [
            {
                "confused_term_or_misunderstanding": "두 번째 필드의 'x'를 패스워드가 설정되지 않은 상태로 오해",
                "explanation": "'x'는 패스워드가 없는 것이 아니라, 보안 강화를 위해 암호화된 해시값이 쉐도우 파일(/etc/shadow)로 이전되어 안전하게 분리 보관되고 있음을 의미합니다."
            },
            {
                "confused_term_or_misunderstanding": "세 번째 필드(UID)와 네 번째 필드(GID)의 순서 혼동",
                "explanation": "/etc/passwd 필드 순서는 '계정명:패스워드:UID:GID:코멘트:홈디렉터리:로그인쉘'로, 사용자 식별번호(UID)가 그룹 식별번호(GID)보다 앞섭니다."
            }
        ]
    },
    "Q-SHORT-017": {
        # HTTP 응답 분할(HTTP Response Splitting): CR(\r, %0D), LF(\n, %0A)
        "traps": [
            {
                "confused_term_or_misunderstanding": "HTTP Response Splitting 공격을 단순 XSS나 SQL Injection으로 혼동",
                "explanation": "HTTP Response Splitting은 사용자의 악의적 입력값에 CR/LF(%0D%0A) 제어문자가 포함되어 서버의 HTTP 응답 헤더가 두 개로 분할되는 취약점으로, 악성 쿠키 주입이나 웹 캐시 포이즈닝으로 이어집니다."
            }
        ]
    },
    "Q-SHORT-018": {
        # PHP 원격 파일 삽입(RFI/LFI) 설정: allow_url_fopen, allow_url_include
        "traps": [
            {
                "confused_term_or_misunderstanding": "allow_url_fopen만 Off로 설정하면 RFI가 완전 차단된다고 오해",
                "explanation": "PHP 5.2 이후 RFI의 핵심 차단 지시자는 'allow_url_include = Off'이며, require/include 구문에서 외부 URL 실행을 방어하기 위해 반드시 두 설정 모두 Off(특히 allow_url_include Off)로 구성해야 합니다."
            }
        ]
    },
    "Q-SHORT-019": {
        # Snort threshold: (A) limit, (B) threshold, (C) both
        "traps": [
            {
                "confused_term_or_misunderstanding": "threshold의 'limit'과 'threshold' 동작 방식 혼동",
                "explanation": "limit은 지정 시간 동안 매칭된 이벤트 중 최대 M개까지만 알람을 로깅하는 방식이고, threshold는 지정 시간 동안 최소 M개 이상 발생해야 알람을 생성하기 시작하는 방식입니다."
            }
        ]
    },
    "Q-SHORT-020": {
        # ARP Request 목적지 MAC: FF:FF:FF:FF:FF:FF
        "ans_replace": "FF:FF:FF:FF:FF:FF",
        "traps": [
            {
                "confused_term_or_misunderstanding": "목적지 MAC 주소를 브로드캐스트가 아닌 00:00:00:00:00:00으로 작성",
                "explanation": "00:00:00:00:00:00은 주소가 미할당되었거나 알 수 없음을 뜻하는 널(Null) 주소이며, 로컬 서브넷의 모든 호스트에게 전달되는 이더넷 브로드캐스트 MAC 주소는 48비트가 모두 1인 'FF:FF:FF:FF:FF:FF'입니다."
            }
        ]
    },
    "Q-SHORT-021": {
        # DNS 포트 53: UDP vs TCP (존 전송 512바이트 초과)
        "traps": [
            {
                "confused_term_or_misunderstanding": "DNS 서비스는 오직 UDP 프로토콜만 사용한다고 오해",
                "explanation": "일반 클라이언트 질의는 빠른 처리를 위해 UDP 53을 주로 사용하지만, 마스터-슬레이브 간 Zone Transfer(영역 전송) 및 512바이트(EDNS 미적용 시)를 초과하는 대용량 응답은 신뢰성 있는 TCP 53을 사용합니다."
            }
        ]
    },
    "Q-SHORT-022": {
        # 소프트웨어 취약점 테스트: (A) 정적 분석(SAST), (B) 동적 분석(DAST)
        "traps": [
            {
                "confused_term_or_misunderstanding": "정적 분석(SAST)과 동적 분석(DAST)의 실행 여부 기준 혼동",
                "explanation": "정적 분석은 프로그램을 실행하지 않고 소스코드나 바이너리의 구문을 정밀 검사하는 방식이며, 동적 분석은 프로그램을 실제 런타임 환경에서 실행하며 입출력과 취약점을 점검하는 방식입니다."
            }
        ]
    },
    "Q-SHORT-023": {
        # 접속기록 보관 기준: 기본 1년, 5만명 이상/민감정보 2년
        "traps": [
            {
                "confused_term_or_misunderstanding": "5만 명 이상 정보주체 또는 고유식별정보 처리 시의 접속기록 보관 기한을 1년으로 오해",
                "explanation": "개인정보의 안전성 확보조치 기준에 따라 일반 개인정보처리시스템의 접속기록은 최소 1년 이상 보관해야 하지만, 5만 명 이상의 정보주체 정보를 처리하거나 고유식별/민감정보를 처리하는 시스템은 최소 2년 이상 보관해야 합니다."
            }
        ]
    },
    "Q-SHORT-024": {
        # 위험관리 용어: (A) 단일예상손실액(SLE), (B) 연간예상손실액(ALE)
        "traps": [
            {
                "confused_term_or_misunderstanding": "SLE(단일예상손실액) 산출 시 노출계수(EF)의 곱셈 누락",
                "explanation": "단일예상손실액(SLE)은 자산가치(AV)에 위협 발생 시 예상 손실 비율인 노출계수(EF)를 곱하여 산출(SLE = AV * EF)합니다."
            },
            {
                "confused_term_or_misunderstanding": "연간예상손실액(ALE) 공식에서 ARO의 단위를 월 단위나 일 단위로 오해",
                "explanation": "ALE는 연간 단위 손실액이므로 SLE에 '연간발생률(Annualized Rate of Occurrence, ARO)'을 곱해야 합니다."
            }
        ]
    },
    "Q-SHORT-025": {
        # Sendmail access.db 생성: makemap hash /etc/mail/access < /etc/mail/access
        "traps": [
            {
                "confused_term_or_misunderstanding": "access 텍스트 파일을 수정한 뒤 makemap 컴파일 명령을 수행하지 않아도 즉시 적용된다고 오해",
                "explanation": "Sendmail 데몬은 텍스트 형태의 /etc/mail/access 파일을 직접 읽지 않고 해시 DB 포맷인 /etc/mail/access.db를 참조하므로, 반드시 'makemap hash' 명령으로 DB를 재생성해야 설정이 반영됩니다."
            }
        ]
    },
    "Q-SHORT-026": {
        # BIA (Business Impact Analysis, 업무영향분석)
        "ans_replace": "BIA",
        "traps": [
            {
                "confused_term_or_misunderstanding": "BIA를 단순 기술적 취약점 평가(Vulnerability Assessment)로 혼동",
                "explanation": "BIA는 기술적 취약점 진단이 아니라, 재해나 업무 중단 시 각 비즈니스 프로세스가 조직에 미치는 재무적/운영적 손실 규모를 산정하고 우선 복구 대상과 RTO/RPO를 도출하는 경영 관리 프로세스입니다."
            }
        ]
    },
    "Q-SHORT-027": {
        # APT (Advanced Persistent Threat, 지능형 지속 위협)
        "ans_replace": "APT",
        "traps": [
            {
                "confused_term_or_misunderstanding": "APT 공격을 불특정 다수를 노린 대량 유포형 웜/바이러스 공격으로 혼동",
                "explanation": "APT는 불특정 다수를 상대로 한 일회성 유포가 아니라, 명확한 특정 타깃(기업/기관)을 정해놓고 장기간 잠복하며 정찰, 스피어 피싱, 횡적 이동(Lateral Movement)을 통해 핵심 정보를 탈취하는 고도화된 타깃형 공격입니다."
            }
        ]
    },
    "Q-SHORT-028": {
        # IPSec 프로토콜: (A) AH (인증), (B) ESP (인증+암호화)
        "traps": [
            {
                "confused_term_or_misunderstanding": "AH 프로토콜이 페이로드 기밀성(암호화)을 제공한다고 오해",
                "explanation": "AH(Authentication Header)는 IP 패킷의 무결성과 송신처 인증만을 제공하며 데이터 암호화는 수행하지 않습니다. 데이터 암호화(기밀성)를 제공하는 프로토콜은 ESP(Encapsulating Security Payload)입니다."
            }
        ]
    },
    "Q-SHORT-029": {
        # 버퍼 오버플로우: (A) 스택(Stack), (B) RET(Return Address)
        "traps": [
            {
                "confused_term_or_misunderstanding": "지역 변수가 저장되는 메모리 영역을 힙(Heap) 영역으로 혼동",
                "explanation": "함수 내 지역 변수와 매개변수, 복귀 주소가 할당되는 공간은 스택(Stack) 영역이며, malloc/new 등 동적으로 할당되는 메모리는 힙(Heap) 영역입니다."
            },
            {
                "confused_term_or_misunderstanding": "버퍼 오버플로우 공격이 변조하는 핵심 제어 포인터를 SFP로 오해",
                "explanation": "SFP(Saved Frame Pointer)도 버퍼와 RET 사이에 위치하지만, 공격자가 실행 흐름을 쉘코드로 직접 가로채기 위해 덮어써야 하는 최종 목표는 함수의 복귀 주소인 RET(Return Address)입니다."
            }
        ]
    },
    "Q-SHORT-030": {
        # hping3 (패킷 생성/스캔/DoS 도구)
        "ans_replace": "hping3",
        "traps": [
            {
                "confused_term_or_misunderstanding": "hping3를 단순 수동 패킷 캡처 도구인 Wireshark/tcpdump로 혼동",
                "explanation": "tcpdump는 유입되는 트래픽을 수신/모니터링하는 수동 패킷 스니핑 도구인 반면, hping3는 TCP/UDP/ICMP 패킷의 헤더 플래그, 바이트, 소스 IP를 임의로 조작하여 능동적으로 생성/전송하는 보안 진단 및 침투 테스트 도구입니다."
            }
        ]
    }
}

def apply_chunk1(explanations, questions_map):
    applied_count = 0
    ph_fixed_count = 0
    traps_fixed_count = 0

    for qid, fixes in CHUNK1_FIXES.items():
        if qid not in explanations:
            continue
        exp = explanations[qid]
        q = questions_map[qid]

        # 1. P1-1 Fix: Placeholder removal in why_correct
        if "ans_replace" in fixes:
            ans = fixes["ans_replace"]
            wc = exp.get("why_correct", "")
            if "표준 정답입니다" in wc or "표준 정답" in wc:
                # Replace generic sentence with precise official answer
                old_ph_sent1 = "본 문항에서 요구하는 정확한 용어는 표준 정답입니다."
                old_ph_sent2 = "본 문항에서 요구하는 정확한 용어는 표준 정답입니다. 실기 시험 채점 특성상 표준 지침 및 관련 법령에 명시된 공식 명칭을 작성해야 만점이 인정됩니다."
                
                new_sent = f"본 문항에서 요구하는 정확한 정답은 '{ans}'입니다. 실기 시험 채점 특성상 관련 규정 및 표준 지침에 명시된 정식 명칭을 정확히 작성해야 정답으로 인정됩니다."
                
                if old_ph_sent2 in wc:
                    exp["why_correct"] = wc.replace(old_ph_sent2, new_sent)
                elif old_ph_sent1 in wc:
                    exp["why_correct"] = wc.replace(old_ph_sent1, new_sent)
                elif "공식 표준 정답은" in wc:
                    exp["why_correct"] = wc.replace("공식 표준 정답은", "정확한 정답은")
                else:
                    exp["why_correct"] = wc.replace("표준 정답", f"'{ans}'")
                ph_fixed_count += 1

        # 2. P1-3 Fix: Question-specific traps
        if "traps" in fixes:
            exp["why_wrong_common_traps"] = fixes["traps"]
            traps_fixed_count += 1

        applied_count += 1

    print(f"Chunk 1 applied: {applied_count} questions updated.")
    print(f"  - P1-1 placeholders fixed: {ph_fixed_count}")
    print(f"  - P1-3 traps updated: {traps_fixed_count}")

if __name__ == "__main__":
    with open("app/data/explanations.json", "r", encoding="utf-8") as f:
        exps = json.load(f)
    with open("app/data/questions.json", "r", encoding="utf-8") as f:
        qs = {q["id"]: q for q in json.load(f)}

    apply_chunk1(exps, qs)

    with open("app/data/explanations.json", "w", encoding="utf-8") as f:
        json.dump(exps, f, indent=2, ensure_ascii=False)
    print("Chunk 1 changes saved successfully to explanations.json")
