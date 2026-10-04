# -*- coding: utf-8 -*-
"""
Chunk 3 Fixer: Q-SHORT-061 to Q-SHORT-112 (52 questions)
Fixes:
- P1-1: Eliminates "표준 정답" placeholder in why_correct and embeds the official representative answer.
- P1-3: Replaces concept-inherited traps with question-specific, realistic traps.
"""

import json

CHUNK3_FIXES = {
    "Q-SHORT-061": {
        "ans_replace": "auth, account, password, session",
        "traps": [
            {
                "confused_term_or_misunderstanding": "account 모듈의 역할을 패스워드 인증(auth)으로 혼동",
                "explanation": "auth 모듈은 자격증명(패스워드) 검증을 담당하며, account 모듈은 계정 유효기간, 접속 시간대, 접근 권한 등의 계정 상태 유효성을 점검합니다."
            }
        ]
    },
    "Q-SHORT-062": {
        "ans_replace": "/var/log/btmp",
        "traps": [
            {
                "confused_term_or_misunderstanding": "로그인 실패 로그 파일(/var/log/btmp)을 성공 이력 로그 파일(/var/log/wtmp)과 혼동",
                "explanation": "wtmp는 성공한 모든 로그인/로그아웃 및 리부팅 정보를 기록하고, 실패한 로그인 시도(Bad login)는 btmp에 바이너리 형태로 기록됩니다."
            }
        ]
    },
    "Q-SHORT-063": {
        "ans_replace": "SEED",
        "traps": [
            {
                "confused_term_or_misunderstanding": "SEED의 블록 크기를 64비트나 256비트로 오해",
                "explanation": "KISA가 1999년 개발한 SEED는 128비트 블록 크기와 128비트 비밀키를 사용하는 순수 국산 표준 대칭키 블록 암호 알고리즘입니다."
            }
        ]
    },
    "Q-SHORT-064": {
        "ans_replace": "HIGHT",
        "traps": [
            {
                "confused_term_or_misunderstanding": "경량 암호 HIGHT를 128비트 블록 암호인 ARIA나 LEA와 혼동",
                "explanation": "HIGHT(HIGh security and light weigHT)는 RFID, 센서 등 초경량 임베디드 기기를 위해 개발된 64비트 블록 크기, 128비트 키 크기의 경량 대칭키 암호입니다."
            }
        ]
    },
    "Q-SHORT-065": {
        "ans_replace": "LEA",
        "traps": [
            {
                "confused_term_or_misunderstanding": "LEA를 S-Box 기반의 구조로 오해",
                "explanation": "국가보안기술연구소가 개발한 LEA(Lightweight Encryption Algorithm)는 소프트웨어 환경에서 고속 연산을 위해 S-Box 대신 ARX(Addition, Rotation, XOR) 연산 구조를 채택한 128비트 블록 암호입니다."
            }
        ]
    },
    "Q-SHORT-066": {
        "ans_replace": "ARIA",
        "traps": [
            {
                "confused_term_or_misunderstanding": "ARIA의 키 길이를 128비트 단일 규격으로만 오해",
                "explanation": "국가보안기술연구소와 학계가 공동 개발한 ARIA는 AES와 동일하게 128비트 블록 크기를 가지며 128/192/256비트 3가지 가변 키 길이를 지원합니다."
            }
        ]
    },
    "Q-SHORT-067": {
        "ans_replace": "일회용 패드",
        "traps": [
            {
                "confused_term_or_misunderstanding": "일회용 패드(OTP)를 2차 인증 도구인 일회용 비밀번호(One-Time Password)와 혼동",
                "explanation": "암호학에서 일회용 패드(One-Time Pad)는 평문과 동일한 길이의 무작위 키를 XOR 연산하고 한 번만 사용 후 폐기하여 무조건적 안전성(완전 비밀성)을 제공하는 암호 체계입니다."
            }
        ]
    },
    "Q-SHORT-068": {
        "ans_replace": "디피-헬만",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Diffie-Hellman 프로토콜 자체가 상호 인증을 제공하여 중간자 공격(MITM)에 안전하다고 오해",
                "explanation": "기본 Diffie-Hellman 키 교환은 공개 채널에서 비밀키를 공유할 수 있게 해주지만 개체 인증 기능이 없어 중간자 공격에 취약하므로 전자서명이나 인증서와 결합해야 합니다."
            }
        ]
    },
    "Q-SHORT-069": {
        "ans_replace": "ECC",
        "traps": [
            {
                "confused_term_or_misunderstanding": "ECC(타원곡선 암호)의 수학적 기반을 소인수분해 문제로 혼동",
                "explanation": "소인수분해 난해성에 기반하는 암호는 RSA이며, ECC는 타원곡선 군에서의 이산대수 문제(ECDLP)의 난해성에 기반하여 256비트 키 길이로도 RSA 3072비트 급의 보안 강도를 제공합니다."
            }
        ]
    },
    "Q-SHORT-070": {
        "ans_replace": "충돌 저항성",
        "traps": [
            {
                "confused_term_or_misunderstanding": "강한 충돌 저항성과 제2 역상 저항성(약한 충돌 저항성)의 차이 혼동",
                "explanation": "제2 역상 저항성은 '주어진 x에 대해 H(x)=H(y)인 y'를 찾기 어려운 성질이며, 충돌 저항성은 '임의의 서로 다른 두 입력 x, y에 대해 H(x)=H(y)'인 쌍을 찾기 어려운 성질입니다."
            }
        ]
    },
    "Q-SHORT-071": {
        "ans_replace": "비둘기집 원리",
        "traps": [
            {
                "confused_term_or_misunderstanding": "비둘기집 원리를 확률론적 생일 패러독스(Birthday Paradox)와 혼동",
                "explanation": "생일 공격은 확률적(50% 이상)으로 충돌 쌍이 존재할 확률(2^(n/2))을 다루는 반면, 비둘기집 원리는 n개의 상자에 n+1개 이상의 항목을 넣으면 적어도 한 상자에는 둘 이상의 항목이 반드시 존재한다는 수학적 원리입니다."
            }
        ]
    },
    "Q-SHORT-072": {
        "ans_replace": "커버로스",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Kerberos 인증의 핵심 주체를 공개키 기반 구조(PKI)의 CA로 오해",
                "explanation": "전통적인 커버로스(Kerberos)는 비대칭키가 아니라 대칭키 암호화 기반의 신뢰받는 제3자 인증 서버(KDC: AS 및 TGS)와 티켓(TGT) 메커니즘을 사용합니다."
            }
        ]
    },
    "Q-SHORT-073": {
        "ans_replace": "인증서 핀닝",
        "traps": [
            {
                "confused_term_or_misunderstanding": "인증서 핀닝(Certificate Pinning)을 단순 SSL/TLS 암호화 통신으로 혼동",
                "explanation": "인증서 핀닝은 클라이언트 앱 내부에 특정 서버의 공개키 해시나 인증서 정보를 하드코딩(고정)해 두어, 단말기에 악의적인 사설 CA 루트 인증서가 설치되더라도 가짜 인증서를 통한 프록시 패킷 감청을 원천 차단하는 기술입니다."
            }
        ]
    },
    "Q-SHORT-074": {
        "ans_replace": "OCSP",
        "traps": [
            {
                "confused_term_or_misunderstanding": "OCSP를 주기적으로 다운로드받는 인증서 폐기 목록(CRL)과 동일시",
                "explanation": "CRL은 폐기된 인증서 목록 파일 전체를 주기적으로 다운로드받아야 하여 최신성 지연 및 대역폭 낭비가 발생하는 반면, OCSP는 특정 인증서 일련번호의 유효성 여부만을 실시간으로 조회하는 경량 프로토콜입니다."
            }
        ]
    },
    "Q-SHORT-075": {
        "ans_replace": "Metasploit",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Metasploit을 단순 취약점 스캐너(OpenVAS, Nessus)로 오해",
                "explanation": "Nessus는 취약점을 스캔/탐색하는 도구인 반면, Metasploit은 발견된 보안 취약점에 대한 실제 공격 익스플로잇(Exploit) 코드와 페이로드를 실행하여 침투 가능성을 검증하는 모의해킹 프레임워크입니다."
            }
        ]
    },
    "Q-SHORT-076": {
        "ans_replace": "-sS",
        "traps": [
            {
                "confused_term_or_misunderstanding": "TCP SYN 스캔(-sS)을 완전 3-Way Handshake를 수행하는 TCP Connect 스캔(-sT)과 혼동",
                "explanation": "-sT는 connect() 시스템 콜을 통해 연결을 완전히 수립하여 타깃 서버 로그에 기록이 남는 반면, -sS(Stealth Scan)는 SYN 수신 후 SYN/ACK 응답이 오면 RST 패킷을 즉시 보내 연결을 강제 종료하여 로그를 최소화합니다."
            }
        ]
    },
    "Q-SHORT-077": {
        "ans_replace": "-n",
        "traps": [
            {
                "confused_term_or_misunderstanding": "IP 주소를 숫자로 출력하는 -n 옵션을 포트 번호까지 숫자로 변환하는 -nn 옵션과 혼동",
                "explanation": "tcpdump에서 '-n'은 호스트 주소(IP)를 DNS 역방향 질의하지 않고 숫자로 출력하며, '-nn'은 호스트 주소뿐만 아니라 포트 번호(서비스명)까지 숫자로 출력하는 옵션입니다."
            }
        ]
    },
    "Q-SHORT-078": {
        "ans_replace": "RUDY",
        "traps": [
            {
                "confused_term_or_misunderstanding": "RUDY(Slow HTTP POST) 공격을 Slowloris(Slow HTTP Header) 공격과 혼동",
                "explanation": "Slowloris는 HTTP 요청 '헤더'의 끝을 보내지 않고 세션을 유지하는 반면, RUDY(R-U-Dead-Yet)는 Content-Length를 대용량으로 선언한 후 'POST 본문' 데이터를 1바이트씩 극도로 지연 전송하여 세션을 고갈시키는 기법입니다."
            }
        ]
    },
    "Q-SHORT-079": {
        "ans_replace": "Shellshock",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Shellshock 취약점을 단순 PHP 인젝션이나 웹쉘 업로드로 오해",
                "explanation": "Shellshock(CVE-2014-6271)는 GNU Bash 쉘이 환경변수에 정의된 함수 선언문 뒤의 추가 악성 쉘 명령어를 검증 없이 자동 실행해 버리는 쉘 자체의 취약점입니다."
            }
        ]
    },
    "Q-SHORT-080": {
        "ans_replace": "ALE",
        "traps": [
            {
                "confused_term_or_misunderstanding": "연간예상손실액(ALE)을 단일예상손실액(SLE)과 혼동",
                "explanation": "단일 사건 발생 시 1회 손실액은 SLE(Single Loss Expectancy)이며, 여기에 연간 발생 빈도(ARO)를 곱하여 연간 총 손실 기대치를 도출한 것이 ALE(Annualized Loss Expectancy)입니다."
            }
        ]
    },
    "Q-SHORT-081": {
        "ans_replace": "PP",
        "traps": [
            {
                "confused_term_or_misunderstanding": "보호프로파일(PP)을 특정 벤더 제품의 보안목표명세서(ST)와 혼동",
                "explanation": "보호프로파일(PP: Protection Profile)은 특정 제품군(예: 방화벽)에 공통으로 요구되는 구현 독립적인 보안 요구사항 정의서이며, 이를 바탕으로 특정 개발사가 자사 제품에 맞춰 작성한 것은 보안목표명세서(ST: Security Target)입니다."
            }
        ]
    },
    "Q-SHORT-082": {
        "ans_replace": "관심, 주의, 경계, 심각",
        "traps": [
            {
                "confused_term_or_misunderstanding": "사이버안보 위기경보 4단계를 재난 안전 경보의 색상이나 5단계로 혼동",
                "explanation": "국가 사이버위기 경보 단계는 위기 상황에 따라 '관심(파랑) -> 주의(노랑) -> 경계(주황) -> 심각(빨강)'의 4단계 체계로 상향 발령됩니다."
            }
        ]
    },
    "Q-SHORT-083": {
        "ans_replace": "정보공유·분석센터",
        "traps": [
            {
                "confused_term_or_misunderstanding": "ISAC(정보공유·분석센터)을 CERT(침해사고대응팀)와 혼동",
                "explanation": "CERT는 개별 조직 또는 국가 차원의 침해사고 조사 및 기술 지원을 수행하는 반면, ISAC은 금융, 통신 등 특정 산업 분야별로 침해사고 정보와 취약점 정보를 공유하고 공동 대응하기 위한 협의체 센터입니다."
            }
        ]
    },
    "Q-SHORT-084": {
        "ans_replace": "고유식별정보",
        "traps": [
            {
                "confused_term_or_misunderstanding": "고유식별정보를 사상·신념·건강 정보 등이 포함된 '민감정보'와 혼동",
                "explanation": "개인정보보호법상 법령에 근거하여 개인을 고유하게 식별하도록 부여된 4가지 정보(주민등록번호, 여권번호, 운전면허번호, 외국인등록번호)는 '고유식별정보'로 분류됩니다."
            }
        ]
    },
    "Q-SHORT-085": {
        "ans_replace": "지체 없이",
        "traps": [
            {
                "confused_term_or_misunderstanding": "개인정보 유출 사실을 알게 되었을 때의 정보주체 통지 시한을 구 망법 기준(24시간)으로 오해",
                "explanation": "개인정보보호법 제34조 제1항에 따라 개인정보가 유출되었음을 알게 되었을 때에는 정당한 사유가 없는 한 정보주체에게 '지체 없이' 통지해야 합니다."
            }
        ]
    },
    "Q-SHORT-086": {
        "ans_replace": "EAL",
        "traps": [
            {
                "confused_term_or_misunderstanding": "공통평가기준(CC)의 보증 등급(EAL)을 보안 등급(Security Level)으로 혼동",
                "explanation": "EAL(Evaluation Assurance Level)은 제품의 보안 기능이 많고 적음이 아니라, 해당 보안 목표가 얼마나 신뢰성 있게 설계, 검증, 시험되었는지를 나타내는 보증 수준(EAL1~EAL7) 지표입니다."
            }
        ]
    },
    "Q-SHORT-087": {
        "ans_replace": "설치 목적 및 장소",
        "traps": [
            {
                "confused_term_or_misunderstanding": "CCTV 안내판 필수 기재 항목 중 관리책임자 연락처나 촬영 범위를 누락",
                "explanation": "개인정보보호법 제25조에 따른 안내판 필수 기재 사항은 '1. 설치 목적 및 장소', '2. 촬영 범위 및 시간', '3. 관리책임자 성명(직책) 및 연락처'입니다."
            }
        ]
    },
    "Q-SHORT-088": {
        "ans_replace": "웹 프록시",
        "traps": [
            {
                "confused_term_or_misunderstanding": "로컬 프록시(Burp Suite 등)를 포트 스캐너나 웹 취약점 자동 점검기로 오해",
                "explanation": "Burp Suite, OWASP ZAP 등은 브라우저와 웹 서버 사이의 HTTP/HTTPS 패킷을 실시간 인터셉트하여 파라미터 변조 및 응답 분석을 수행하는 웹 프록시 도구입니다."
            }
        ]
    },
    "Q-SHORT-089": {
        "ans_replace": "디렉터리 접근",
        "traps": [
            {
                "confused_term_or_misunderstanding": "경로 순회(Directory Traversal) 취약점을 단순 파일 업로드 취약점과 혼동",
                "explanation": "디렉터리 접근(Path Traversal)은 상위 디렉터리 이동 문자열('../')을 파일 경로 파라미터에 삽입하여 웹 루트를 벗어나 /etc/passwd 등 시스템 내부 중요 파일에 무단 접근하는 취약점입니다."
            }
        ]
    },
    "Q-SHORT-090": {
        "ans_replace": "XXE",
        "traps": [
            {
                "confused_term_or_misunderstanding": "XXE 취약점을 단순 XSS나 XML 구조 파싱 오류로 오해",
                "explanation": "XXE(XML External Entity) 공격은 XML 파서가 외부 엔티티(SYSTEM)를 해석하도록 허용되어 있을 때 로컬 시스템 파일(/etc/passwd) 열람, 내부망 SSRF, DoS 등을 유발하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-091": {
        "ans_replace": "SSRF",
        "traps": [
            {
                "confused_term_or_misunderstanding": "SSRF를 사용자의 브라우저를 악용하는 CSRF와 혼동",
                "explanation": "CSRF는 공격자가 사용자의 브라우저 권한을 빌려 서버로 위조 요청을 보내는 것이며, SSRF(Server-Side Request Forgery)는 취약한 백엔드 웹 서버가 공격자가 지정한 내부 사설망 IP나 클라우드 메타데이터 URL로 직접 요청을 생성하도록 악용하는 기법입니다."
            }
        ]
    },
    "Q-SHORT-092": {
        "ans_replace": "탭내빙",
        "traps": [
            {
                "confused_term_or_misunderstanding": "탭내빙(Tabnabbing) 공격을 단순 피싱 이메일 링크와 혼동",
                "explanation": "탭내빙은 새 탭(target='_blank') 링크에 'rel=\"noopener noreferrer\"' 속성이 누락되었을 때, 새 창의 악성 스크립트가 'window.opener.location'을 조작하여 원래 보고 있던 탭의 페이지를 가짜 로그인 피싱 창으로 변조하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-093": {
        "ans_replace": "bind-address",
        "traps": [
            {
                "confused_term_or_misunderstanding": "MySQL 외부 접속 제어 지시자를 포트 번호 설정(port)으로 오해",
                "explanation": "MySQL에서 특정 IP 인터페이스(로컬 127.0.0.1 등)에서만 연결을 수신하도록 리슨 IP를 제한하는 핵심 설정 지시자는 'bind-address'입니다."
            }
        ]
    },
    "Q-SHORT-094": {
        "ans_replace": "randomize_va_space",
        "traps": [
            {
                "confused_term_or_misunderstanding": "ASLR 커널 제어 파라미터를 일반 가상 메모리 스왑 관련 파라미터로 혼동",
                "explanation": "리눅스에서 주소 공간 배치 난수화(ASLR)를 활성화/비활성화(0: 해제, 1: 보수적, 2: 완전 적용)하는 procfs 시스템 파라미터는 '/proc/sys/kernel/randomize_va_space'입니다."
            }
        ]
    },
    "Q-SHORT-095": {
        "ans_replace": "HKLM",
        "traps": [
            {
                "confused_term_or_misunderstanding": "시스템 전체에 적용되는 HKLM 키를 현재 로그인한 사용자 전용인 HKCU 키와 혼동",
                "explanation": "HKCU(HKEY_CURRENT_USER)는 개별 로그인 사용자의 개인 설정만 관리하는 반면, 시스템 하드웨어, 드라이버, 서비스 및 전역 보안 정책은 HKLM(HKEY_LOCAL_MACHINE) 하위에서 관리됩니다."
            }
        ]
    },
    "Q-SHORT-096": {
        "ans_replace": "TPM",
        "traps": [
            {
                "confused_term_or_misunderstanding": "TPM을 단순 BIOS/UEFI 펌웨어로 혼동",
                "explanation": "TPM(Trusted Platform Module)은 메인보드에 장착된 전용 하드웨어 암호화 프로세서 칩으로, 하드디스크 암호화 키(BitLocker 등)를 안전하게 보호하고 플랫폼 부팅 무결성을 측정(측정 부팅)합니다."
            }
        ]
    },
    "Q-SHORT-097": {
        "ans_replace": "PFS",
        "traps": [
            {
                "confused_term_or_misunderstanding": "PFS(완전 순방향 비밀성)를 일반 비대칭 암호키의 영구 비밀성으로 오해",
                "explanation": "PFS(Perfect Forward Secrecy)는 과거 통신 세션의 비밀키가 장기 개인키 유출로부터 독립되도록 매 세션마다 임시 키(DHE, ECDHE)를 동적으로 교환하여, 향후 개인키가 유출되어도 과거의 암호화 트래픽을 소급 복호화할 수 없도록 보장하는 특성입니다."
            }
        ]
    },
    "Q-SHORT-098": {
        "ans_replace": "XPath 인젝션",
        "traps": [
            {
                "confused_term_or_misunderstanding": "XPath 인젝션을 RDBMS 대상의 SQL 인젝션과 동일시",
                "explanation": "SQL 인젝션은 관계형 데이터베이스를 대상으로 수행되는 반면, XPath 인젝션은 XML 구조 문서를 쿼리하는 XPath 표현식에 악의적 논리 연산자(' or '1'='1)를 주입하여 인증을 우회하거나 XML 노드 데이터를 탈취하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-099": {
        "ans_replace": "REJECT",
        "traps": [
            {
                "confused_term_or_misunderstanding": "REJECT 타깃과 DROP 타깃의 응답 동작 혼동",
                "explanation": "DROP은 패킷을 조용히 폐기하고 송신자에게 아무런 응답을 주지 않아 타임아웃을 유발하는 반면, REJECT는 패킷을 차단한 후 송신자에게 거부 응답(TCP RST 또는 ICMP Port Unreachable)을 즉시 반환합니다."
            }
        ]
    },
    "Q-SHORT-100": {
        "ans_replace": "분할 난독화",
        "traps": [
            {
                "confused_term_or_misunderstanding": "문자열 연결/분할 난독화를 패킹(Packing)이나 암호화(Encryption)로 혼동",
                "explanation": "패킹은 바이너리 전체를 압축/은닉하는 기술이며, 스크립트 상에서 'cmd' + '.exe'처럼 악성 키워드를 여러 조각으로 쪼개어 정적 시그니처 탐지를 우회하는 기법은 분할 난독화(String Concatenation Obfuscation)입니다."
            }
        ]
    },
    "Q-SHORT-101": {
        "ans_replace": "lastcomm",
        "traps": [
            {
                "confused_term_or_misunderstanding": "프로세스 실행 이력 명령어 lastcomm을 로그인 이력 명령어 last와 혼동",
                "explanation": "'last'는 /var/log/wtmp를 참조하여 사용자 로그인/로그아웃 이력을 조회하는 명령어이고, 'lastcomm'은 pacct/acct 시스템 회계 로그를 참조하여 과거 사용자가 실행했던 개별 명령어 이력을 조회하는 도구입니다."
            }
        ]
    },
    "Q-SHORT-102": {
        "ans_replace": "logrotate",
        "traps": [
            {
                "confused_term_or_misunderstanding": "logrotate를 로그 수집 데몬인 rsyslog나 journald와 혼동",
                "explanation": "rsyslog는 시스템 로그를 생성/수신/기록하는 서비스이며, 생성된 로그 파일들을 주기적으로 순환(Rotate), 압축(Compress), 삭제(Remove)하여 디스크를 관리하는 유틸리티는 logrotate입니다."
            }
        ]
    },
    "Q-SHORT-103": {
        "ans_replace": "비트락커",
        "traps": [
            {
                "confused_term_or_misunderstanding": "드라이브 전체를 암호화하는 BitLocker를 개별 파일/폴더 암호화 기술인 EFS와 혼동",
                "explanation": "EFS(Encrypting File System)는 NTFS 파일시스템 내 특정 파일이나 폴더 단위로 암호화를 적용하지만, BitLocker는 OS 볼륨 및 전체 드라이브 볼륨을 FDE(Full Disk Encryption) 방식으로 암호화하여 물리적 도난 시 데이터 유출을 방어합니다."
            }
        ]
    },
    "Q-SHORT-104": {
        "ans_replace": "UAC",
        "traps": [
            {
                "confused_term_or_misunderstanding": "UAC(사용자 계정 컨트롤)를 단순 Windows 방화벽으로 오해",
                "explanation": "UAC(User Account Control)는 관리자 권한을 가진 계정이라도 평소에는 일반 사용자 표준 권한 토큰으로 프로세스를 실행하다가, 시스템 설정 변경이나 프로그램 설치 시 관리자 승인 동의창을 띄워 권한 상승을 통제하는 보안 기술입니다."
            }
        ]
    },
    "Q-SHORT-105": {
        "ans_replace": "PE",
        "traps": [
            {
                "confused_term_or_misunderstanding": "윈도우의 PE(Portable Executable) 포맷을 리눅스의 ELF 포맷과 혼동",
                "explanation": "리눅스/유닉스 실행 바이너리 포맷은 ELF(Executable and Linkable Format)이며, 윈도우 운영체제의 실행 파일(EXE), DLL, 드라이버(SYS) 포맷은 PE(Portable Executable) 구조입니다."
            }
        ]
    },
    "Q-SHORT-106": {
        "ans_replace": "환형 대기",
        "traps": [
            {
                "confused_term_or_misunderstanding": "교착상태(Deadlock) 4대 조건(상호배제, 점유와 대기, 비선점, 환형 대기) 간의 개념 혼동",
                "explanation": "환형 대기(Circular Wait)는 프로세스들이 원형으로 자원을 요청하며 대기하는 상태를 의미하며, 이미 할당된 자원을 강제로 뺏을 수 없는 조건은 비선점(No Preemption)입니다."
            }
        ]
    },
    "Q-SHORT-107": {
        "ans_replace": "SOAR",
        "traps": [
            {
                "confused_term_or_misunderstanding": "SOAR를 단순 로그 수집/분석 시스템인 SIEM과 동일시",
                "explanation": "SIEM은 방대한 이종 보안 장비 로그를 수집·상관분석하여 위협을 탐지하는 시스템인 반면, SOAR는 SIEM이 탐지한 위협에 대해 플레이북(Playbook) 기반으로 분석, 오케스트레이션, 방화벽 IP 차단 등 대응 조치를 자동화하는 상위 플랫폼입니다."
            }
        ]
    },
    "Q-SHORT-108": {
        "ans_replace": "티어드롭",
        "traps": [
            {
                "confused_term_or_misunderstanding": "티어드롭(Teardrop) 공격을 대용량 ICMP를 보내는 Ping of Death와 혼동",
                "explanation": "Ping of Death는 규격(65,535바이트)을 초과하는 거대 패킷을 전송하는 공격이며, 티어드롭은 단편화 오프셋(Fragment Offset) 값을 고의로 중첩(Overlap)되게 조작하여 재조합 과정에서 커널 충돌이나 시스템 다운을 유발하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-109": {
        "ans_replace": "랜드 어택",
        "traps": [
            {
                "confused_term_or_misunderstanding": "랜드 어택(Land Attack)을 스머프(Smurf) 공격과 혼동",
                "explanation": "스머프는 출발지 IP를 피해자로 위조하여 브로드캐스트 주소로 ICMP Echo를 보내 반사 응답을 유발하는 반면, 랜드 어택은 패킷의 출발지 IP/포트와 목적지 IP/포트를 피해자 자신의 주소로 일치시켜 서버가 자기 자신과 무한 루프 연결을 맺게 만드는 DoS 공격입니다."
            }
        ]
    },
    "Q-SHORT-110": {
        "ans_replace": "no ip directed-broadcast",
        "traps": [
            {
                "confused_term_or_misunderstanding": "시스코 라우터의 브로드캐스트 전달 차단 명령어를 단순 IP 차단 ACL로 오해",
                "explanation": "외부에서 특정 서브넷으로 유입된 유니캐스트 패킷이 목적지 네트워크에서 브로드캐스트로 변환(증폭)되어 스머프 공격에 악용되는 것을 방지하기 위해 해당 인터페이스에 'no ip directed-broadcast'를 설정해야 합니다."
            }
        ]
    },
    "Q-SHORT-111": {
        "ans_replace": "포트 기반 VLAN",
        "traps": [
            {
                "confused_term_or_misunderstanding": "포트 기반 VLAN(정적 VLAN)을 MAC 주소 기반의 동적 VLAN과 혼동",
                "explanation": "스위치의 물리적 포트 번호에 VLAN 번호를 고정 매핑하는 방식은 포트 기반 VLAN(Static VLAN)이며, 접속하는 단말기의 MAC 주소에 따라 유동적으로 VLAN을 배정하는 것은 동적(MAC 기반) VLAN입니다."
            }
        ]
    },
    "Q-SHORT-112": {
        "ans_replace": "show vlan",
        "traps": [
            {
                "confused_term_or_misunderstanding": "VLAN 정보 조회 명령어를 스위치 포트 인터페이스 조회(show interfaces)로 오해",
                "explanation": "시스코 스위치에서 장비에 생성된 모든 VLAN의 번호, 이름, 상태 및 포트 매핑 현황을 종합 조회하는 표준 명령어는 'show vlan' 또는 'show vlan brief'입니다."
            }
        ]
    }
}

def apply_chunk3(explanations, questions_map):
    applied_count = 0
    ph_fixed_count = 0
    traps_fixed_count = 0

    for qid, fixes in CHUNK3_FIXES.items():
        if qid not in explanations:
            continue
        exp = explanations[qid]
        q = questions_map[qid]

        # 1. P1-1 Fix: Placeholder removal in why_correct
        if "ans_replace" in fixes:
            ans = fixes["ans_replace"]
            wc = exp.get("why_correct", "")
            if "표준 정답" in wc:
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

    print(f"Chunk 3 applied: {applied_count} questions updated.")
    print(f"  - P1-1 placeholders fixed: {ph_fixed_count}")
    print(f"  - P1-3 traps updated: {traps_fixed_count}")

if __name__ == "__main__":
    with open("app/data/explanations.json", "r", encoding="utf-8") as f:
        exps = json.load(f)
    with open("app/data/questions.json", "r", encoding="utf-8") as f:
        qs = {q["id"]: q for q in json.load(f)}

    apply_chunk3(exps, qs)

    with open("app/data/explanations.json", "w", encoding="utf-8") as f:
        json.dump(exps, f, indent=2, ensure_ascii=False)
    print("Chunk 3 changes saved successfully to explanations.json")
