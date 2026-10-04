# -*- coding: utf-8 -*-
"""
Chunk 4 Fixer: Q-DESC-001 to Q-DESC-044 (44 questions)
Fixes:
- P1-2: Replaces category boilerplate in practical_scoring_criteria with authentic rubric keywords from questions.json.
  Guarantees rubric points sum to 12.
- P1-3: Replaces concept-inherited traps with question-specific, realistic traps.
"""

import json

DESC_TRAPS = {
    "Q-DESC-001": [
        {
            "confused_term_or_misunderstanding": "Referer 헤더를 목적지 페이지(호출될 대상 페이지)로 오해",
            "explanation": "Referer 헤더는 현재 요청된 페이지를 링크하거나 경유하여 호출한 '직전 출발지(이전 페이지)' URL을 나타내며, 목적지 페이지 자체를 가리키지 않습니다."
        },
        {
            "confused_term_or_misunderstanding": "HTTP 상태코드 200을 클라이언트의 단순 접속 요청 코드로 혼동",
            "explanation": "HTTP 200은 서버가 클라이언트의 요청(GET)을 성공적으로 수신하여 정상 처리하고 요청된 엔티티(본문 3549바이트)를 반환했음을 의미하는 표준 성공 응답(OK)입니다."
        }
    ],
    "Q-DESC-002": [
        {
            "confused_term_or_misunderstanding": ".rhosts 파일 소유자를 일반 사용자 대신 아무 시스템 계정이나 가능하다고 오해",
            "explanation": "보안 가이드상 r-command 인증 파일은 반드시 root 또는 해당 사용자 본인 계정 소유여야 하며, 권한은 타인이 읽거나 쓸 수 없도록 600(rw-------) 이하로 엄격히 제한되어야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "+ (와일드카드) 설정을 특정 서브넷 전체 허용으로만 오해",
            "explanation": "hosts.equiv나 .rhosts 파일에 '+' 기호만 단독으로 설정하면 모든 원격 호스트와 모든 계정으로부터의 패스워드 없는 무인증 로그인을 허용하는 최악의 보안 결함이 발생합니다."
        }
    ],
    "Q-DESC-003": [
        {
            "confused_term_or_misunderstanding": "SNMPv1/v2c의 취약점을 단순 포트 번호 노출로만 오해",
            "explanation": "SNMPv1과 v2c는 인증 암호 역할을 하는 Community String이 네트워크 상에 평문(Plaintext)으로 전송되어 스니핑에 취약하므로, 사용자 기반 인증(USM)과 데이터 암호화(VACM)를 제공하는 SNMPv3를 적용해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "기본 커뮤니티 스트링(public, private) 유지만으로 안전하다고 생각",
            "explanation": "public(기본 RO), private(기본 RW)은 공격자들이 무차별 대입 없이 첫 번째로 시도하는 잘 알려진 기본값이므로 반드시 유추하기 어려운 복잡한 문자열로 변경해야 합니다."
        }
    ],
    "Q-DESC-004": [
        {
            "confused_term_or_misunderstanding": "Blind SQL Injection 방어책으로 'DB 에러 메시지 미출력'만을 유일한 해결책으로 서술",
            "explanation": "에러 메시지를 숨기더라도 참/거짓 논리 검증(Boolean-based)이나 sleep()을 이용한 시간 지연(Time-based) 방식으로 여전히 데이터를 탈취할 수 있으므로, 근본 방어책인 정적 쿼리 바인딩(Prepared Statement)을 적용해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "PreparedStatement를 사용하면서 동적 문자열 연결(+, concat)을 병행하는 실수",
            "explanation": "PreparedStatement를 선언하더라도 SQL 쿼리 문장에 파라미터 바인딩(?) 대신 변수를 문자열로 직접 이어붙이면 사전 컴파일의 보안 이점이 완전히 무력화됩니다."
        }
    ],
    "Q-DESC-005": [
        {
            "confused_term_or_misunderstanding": "오용 탐지(Misuse Detection)가 제로데이(신종) 공격을 탐지할 수 있다고 오해",
            "explanation": "오용 탐지는 기존에 알려진 공격 패턴(시그니처) 데이터베이스와 비교하는 방식이므로 오탐률(False Positive)이 낮지만, 아직 패턴이 등록되지 않은 신종/변종 공격 및 제로데이 취약점은 탐지할 수 없습니다."
        },
        {
            "confused_term_or_misunderstanding": "이상 탐지(Anomaly Detection)의 단점을 미탐률(False Negative) 증가로만 국한",
            "explanation": "이상 탐지는 정상 트래픽 베이스라인에서 벗어난 행위를 탐지하므로 미등록 공격도 탐지할 수 있으나, 정상 사용자의 비정형 활동이나 대량 작업까지 침입으로 간주하여 오탐률(False Positive)이 매우 높은 치명적인 단점이 있습니다."
        }
    ],
    "Q-DESC-006": [
        {
            "confused_term_or_misunderstanding": "FIN 플래그와 RST 플래그의 종료 성격 혼동",
            "explanation": "FIN 플래그는 정상적으로 송신할 데이터가 모두 전송된 후 상호 합의 하에 연결을 정상 해제(4-Way Handshake)할 때 사용되며, RST 플래그는 비정상적인 세션 오류나 침입 차단 시 즉시 연결을 강제 초기화(리셋)할 때 사용됩니다."
        },
        {
            "confused_term_or_misunderstanding": "SYN 플래그의 역할을 단순 패킷 도착 확인으로 혼동",
            "explanation": "단순 패킷 수신 확인은 ACK의 역할이며, SYN 플래그는 TCP 3-Way Handshake 시 양단 간 초기 순서 번호(ISN: Initial Sequence Number)를 동기화하고 가상 회선을 수립하기 위해 전송됩니다."
        }
    ],
    "Q-DESC-007": [
        {
            "confused_term_or_misunderstanding": "클라이언트 자바스크립트 확장자 검증만으로 파일 업로드가 충분히 방어된다고 오해",
            "explanation": "공격자는 Burp Suite 등 로컬 프록시 도구를 사용하여 브라우저 검증을 쉽게 우회하거나 Content-Type 헤더를 변조할 수 있으므로, 반드시 서버 측에서 확장자 화이트리스트 검증을 수행해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "업로드 디렉터리의 읽기 권한을 제거하는 것을 해결책으로 서술",
            "explanation": "웹 서버가 정상적으로 파일(이미지 등)을 제공하기 위해서는 읽기 권한이 필요하며, 웹쉘 방어의 핵심은 아파치 설정이나 파일시스템 퍼미션을 통해 업로드 디렉터리 내 파일의 '실행 권한(ExecCGI, Script)'을 원천 제거하는 것입니다."
        }
    ],
    "Q-DESC-008": [
        {
            "confused_term_or_misunderstanding": "Cache-Control: max-age=0 공격을 단순 캐시 서버 다운 공격으로 오해",
            "explanation": "공격자가 max-age=0 또는 no-cache를 지정하는 이유는 중간 프록시/CDN 캐시 서버가 저장된 응답을 반환하지 못하게 강제하여, 모든 대량 요청이 백엔드 원본 웹서버로 직접 전달되어 시스템 자원을 고갈시키도록 만들기 위함입니다."
        },
        {
            "confused_term_or_misunderstanding": "HTTP GET Flooding을 네트워크 계층의 SYN Flood와 동일시",
            "explanation": "SYN Flood는 3계층/4계층의 백로그 큐를 고갈시키는 네트워크 DoS인 반면, HTTP GET Flooding은 7계층(애플리케이션 계층)에서 정상적인 웹 접속 세션을 대량 생성하여 웹 데몬과 DB 연결 풀을 고갈시키는 공격입니다."
        }
    ],
    "Q-DESC-009": [
        {
            "confused_term_or_misunderstanding": "MDM(모바일 단말 관리)과 MAM(모바일 애플리케이션 관리)의 통제 대상 범위 혼동",
            "explanation": "MDM은 기기 전체(카메라 통제, GPS, 단말 원격 초기화)를 제어하여 개인 사생활 침해 우려가 발생할 수 있는 반면, MAM 및 컨테이너화 기술은 단말 내의 특정 기업 업무용 앱과 데이터만을 논리적으로 분리 격리하여 프라이버시를 보호합니다."
        }
    ],
    "Q-DESC-010": [
        {
            "confused_term_or_misunderstanding": "HttpOnly 쿠키 설정이 XSS 공격 자체를 차단한다고 오해",
            "explanation": "HttpOnly는 브라우저의 document.cookie 스크립트 접근을 차단하여 세션 하이재킹 피해를 예방하는 완화 대책일 뿐, DOM 조작이나 가짜 폼 피싱 등 XSS의 다른 실행 취약점을 원천 차단하는 방어책은 아닙니다."
        },
        {
            "confused_term_or_misunderstanding": "Stored XSS와 Reflected XSS의 악성 스크립트 저장 위치 혼동",
            "explanation": "Stored XSS는 공격 스크립트가 게시판 DB에 영구 저장되어 열람하는 불특정 다수에게 피해를 주지만, Reflected XSS는 URL 파라미터에 포함된 스크립트가 서버를 거쳐 요청자 본인의 브라우저로 즉시 반사되어 실행됩니다."
        }
    ],
    "Q-DESC-011": [
        {
            "confused_term_or_misunderstanding": "연계보관성(Chain of Custody)과 무결성(Integrity)의 개념 혼동",
            "explanation": "무결성은 해시값(MD5/SHA) 대조를 통해 증거 데이터가 수집 시점부터 전혀 변경되지 않았음을 입증하는 것이며, 연계보관성은 증거가 누구의 손을 거쳐 어디에 보관/이송되었는지 인계인수 과정을 명확히 문서화하는 원칙입니다."
        }
    ],
    "Q-DESC-012": [
        {
            "confused_term_or_misunderstanding": "노출계수(EF)를 백분율(비율)이 아닌 고정 금액으로 혼동",
            "explanation": "노출계수(Exposure Factor)는 위협 발생 시 자산이 손실되는 피해 비율(0%~100%)을 나타내며, 자산가치(AV)에 이 비율(EF)을 곱하여 1회 손실액인 SLE(Single Loss Expectancy)를 계산합니다."
        }
    ],
    "Q-DESC-013": [
        {
            "confused_term_or_misunderstanding": "기준선(Baseline) 접근법을 고비용 정밀 분석 기법으로 오해",
            "explanation": "기준선 접근법은 공인된 표준 보안 통제 항목(체크리스트)을 일괄 적용하여 시간과 비용이 적게 드는 장점이 있지만, 조직 고유의 특화된 보안 위협과 취약성을 식별하지 못해 보안 과잉이나 과소가 발생할 수 있습니다."
        }
    ],
    "Q-DESC-014": [
        {
            "confused_term_or_misunderstanding": "DNS 증폭 공격에서 공격 대상(희생자)의 IP가 패킷의 목적지 IP로 전송된다고 오해",
            "explanation": "공격자는 개방형 DNS 리졸버(Open Resolver)로 요청을 보낼 때 출발지 IP(Source IP)를 희생자의 IP 주소로 위조(스푸핑)하여, 대용량 ANY 응답 패킷이 반사되어 희생자에게 집중되도록 만듭니다."
        }
    ],
    "Q-DESC-015": [
        {
            "confused_term_or_misunderstanding": "비밀번호 암호화에 양방향 암호화 알고리즘(AES, RSA)을 적용해야 한다고 오해",
            "explanation": "비밀번호는 복호화될 필요가 없으므로 복호화가 불가능한 안전한 일방향 해시 함수(SHA-256 이상)에 솔트(Salt)를 추가하여 암호화 저장해야 합니다."
        }
    ],
    "Q-DESC-016": [
        {
            "confused_term_or_misunderstanding": "Promiscuous 모드가 활성화되어도 브로드캐스트 패킷만 수신할 수 있다고 생각",
            "explanation": "일반 모드의 NIC는 자신에게 지정된 유니캐스트와 브로드캐스트만 수신하지만, Promiscuous(무차별) 모드로 전환되면 동일 LAN 세그먼트를 지나가는 다른 모든 호스트의 유니캐스트 패킷까지 필터링 없이 수집하여 스니핑을 수행합니다."
        }
    ],
    "Q-DESC-017": [
        {
            "confused_term_or_misunderstanding": "DRDoS 공격의 3자 구성에서 반사체(Reflector)를 좀비 PC(봇넷)로만 혼동",
            "explanation": "전통적인 DDoS와 달리 DRDoS의 반사체(DNS, NTP, SNMP 서버 등)는 악성코드에 감염된 장비가 아니라 인터넷 상에서 정상 서비스 중인 제3의 합법적인 공용 서버들입니다."
        }
    ],
    "Q-DESC-018": [
        {
            "confused_term_or_misunderstanding": "Ingress 필터링을 내부에서 외부로 나가는 패킷 필터링으로 혼동",
            "explanation": "내부에서 외부로 나가는 트래픽의 출발지 IP 위조를 검사하는 것은 Egress 필터링이며, 외부 인터넷에서 내부 네트워크로 유입되는 패킷 중 사설 IP(RFC 1918)나 루프백 대역을 차단하는 것은 Ingress 필터링입니다."
        }
    ],
    "Q-DESC-019": [
        {
            "confused_term_or_misunderstanding": "가명정보를 처리할 때 정보주체의 개별 동의를 반드시 받아야 한다고 오해",
            "explanation": "개인정보보호법 제28조의2에 따라 통계작성, 과학적 연구, 공익적 기록보존 등의 목적으로 가명정보를 처리하는 경우에는 정보주체의 별도 사전 동의 없이도 처리 및 활용이 가능합니다."
        }
    ],
    "Q-DESC-020": [
        {
            "confused_term_or_misunderstanding": "NAC의 격리(Quarantine) 기능을 단순 전원 차단으로 오해",
            "explanation": "NAC의 격리는 단말기의 네트워크 접근을 격리 VLAN(Quarantine VLAN)으로 우회 할당하여 사내 내부망 접근을 차단하고 필수 백신 설치나 보안 패치를 수행할 수 있는 치료 서버로만 접속을 허용하는 기술입니다."
        }
    ],
    "Q-DESC-021": [
        {
            "confused_term_or_misunderstanding": "Windows SAM 파일에 사용자의 비밀번호가 평문으로 저장된다고 오해",
            "explanation": "SAM(Security Account Manager) 데이터베이스에는 패스워드 원문이 아니라 단방향 암호화 해시값인 NTLM 해시가 저장되며, SYSKEY를 통해 추가 암호화되어 보호됩니다."
        }
    ],
    "Q-DESC-022": [
        {
            "confused_term_or_misunderstanding": "/etc/shadow 두 번째 필드에 느낌표(!)나 'x'가 있는 의미 혼동",
            "explanation": "'x'는 /etc/passwd에서 패스워드가 shadow로 분리되었음을 의미하며, /etc/shadow의 해시 필드 앞에 느낌표(!)나 별표(*)가 붙어 있는 것은 해당 계정의 로그인이 잠금(Lock) 상태임을 의미합니다."
        }
    ],
    "Q-DESC-023": [
        {
            "confused_term_or_misunderstanding": "ASLR(주소 공간 배치 난수화)을 컴파일 시점의 정적 방어 기법으로 오해",
            "explanation": "Stack Canary는 컴파일러가 스택에 카나리 코드를 삽입하는 정적 기법인 반면, ASLR은 프로그램이 메모리에 로드될 때 커널이 스택, 힙, 라이브러리 시작 주소를 무작위로 변경하는 동적 런타임 방어 기술입니다."
        }
    ],
    "Q-DESC-024": [
        {
            "confused_term_or_misunderstanding": "대칭키 방식과 비대칭키 방식의 키 개수 공식 혼동",
            "explanation": "n명의 사용자가 상호 기밀 통신을 할 때 필요한 키 개수는 대칭키 방식의 경우 'n(n-1)/2'개로 기하급수적으로 증가하지만, 비대칭키 방식은 1인당 2개씩 총 '2n'개의 키만 관리하면 됩니다."
        }
    ],
    "Q-DESC-025": [
        {
            "confused_term_or_misunderstanding": "기지 평문 공격(KPA)과 선택 평문 공격(CPA)의 공격자 통제 권한 차이 혼동",
            "explanation": "KPA는 공격자가 사전에 이미 매칭된 평문-암호문 쌍을 수동적으로 확보한 상태에서 분석하는 것이며, CPA는 공격자가 원하는 특정 평문을 암호기에 직접 주입하여 그에 대응하는 암호문을 능동적으로 생성/확보할 수 있는 공격입니다."
        }
    ],
    "Q-DESC-026": [
        {
            "confused_term_or_misunderstanding": "SPN 구조에서 복호화 과정이 암호화 함수와 완전히 동일하다고 오해",
            "explanation": "Feistel 구조는 라운드 함수 F의 역함수가 불필요하여 복호화 시 암호화 루틴을 그대로 사용할 수 있지만, SPN(Substitution-Permutation Network) 구조는 복호화를 위해 S-Box와 P-Box의 역연산(역함수)이 반드시 별도로 구현되어야 합니다."
        }
    ],
    "Q-DESC-027": [
        {
            "confused_term_or_misunderstanding": "제1 역상 저항성과 제2 역상 저항성의 정의 혼동",
            "explanation": "제1 역상 저항성은 출력값 y가 주어졌을 때 H(x)=y를 만족하는 입력 x를 찾기 어려운 성질이며, 제2 역상 저항성은 특정 입력 x가 주어졌을 때 H(x)=H(x')를 만족하는 다른 입력 x'를 찾기 어려운 성질입니다."
        }
    ],
    "Q-DESC-028": [
        {
            "confused_term_or_misunderstanding": "전자서명 생성 시 수신자의 공개키로 서명한다고 오해",
            "explanation": "기밀성 암호화 통신에서는 수신자의 공개키로 암호화하지만, 전자서명은 오직 서명자 본인만이 생성할 수 있어야 하므로 '송신자의 개인키(비밀키)'로 서명하고 수신자는 송신자의 공개키로 이를 검증합니다."
        }
    ],
    "Q-DESC-029": [
        {
            "confused_term_or_misunderstanding": "보안 대책을 외주 위탁하거나 보험에 가입하는 전략을 '위험 완화'로 혼동",
            "explanation": "방화벽 설치, 취약점 패치 등 기술적 조치는 위험을 낮추는 '위험 완화(Mitigation)'이지만, 보안 보험 가입이나 보안 관제 외주 위탁은 위험의 금전적 피해나 책임을 제3자에게 이전하는 '위험 전가(Transference)'입니다."
        }
    ],
    "Q-DESC-030": [
        {
            "confused_term_or_misunderstanding": "Hot Site와 Warm Site의 복구 목표 시간(RTO) 및 장비 구비 수준 혼동",
            "explanation": "Hot Site는 주 센터와 동일한 하드웨어, 네트워크, 최신 동기화 데이터를 유지하여 수시간 이내 복구가 가능한 반면, Warm Site는 중요 장비는 구비되어 있으나 데이터는 주기적 백업본을 수동 복원해야 하여 수일의 시간이 소요됩니다."
        }
    ],
    "Q-DESC-031": [
        {
            "confused_term_or_misunderstanding": "대규모 기업에서 CISO가 개인정보보호책임자(CPO)나 CIO를 자유롭게 겸직할 수 있다고 오해",
            "explanation": "정보통신망법 개정에 따라 자산총액 또는 매출액 일정 기준 이상의 대규모 기업은 정보보호 업무의 독립성과 실효성 확보를 위해 CISO의 타 직무(CIO, CPO 등 IT 총괄 업무) 겸직을 엄격히 금지하고 있습니다."
        }
    ],
    "Q-DESC-032": [
        {
            "confused_term_or_misunderstanding": "개인정보 접근권한 변경 이력의 법정 보관 기한을 1년으로 오해",
            "explanation": "개인정보처리시스템의 일반 접속기록은 1년(또는 2년) 이상 보관하지만, 권한 오남용 감사를 위한 '접근권한의 부여, 변경, 말소 기록'은 최소 3년 이상 안전하게 보관해야 합니다."
        }
    ],
    "Q-DESC-033": [
        {
            "confused_term_or_misunderstanding": "Metasploit의 Exploit 모듈과 Payload 모듈의 역할 혼동",
            "explanation": "Exploit은 타깃 시스템의 취약점을 공략하여 방어벽을 뚫고 들어가는 공격 수단이며, 침투 성공 후 타깃 머신에서 실행되어 원격 쉘을 연결하거나 명령을 수행하는 실제 악성 코드는 Payload 모듈입니다."
        }
    ],
    "Q-DESC-034": [
        {
            "confused_term_or_misunderstanding": "Slowloris와 RUDY 공격이 대량의 네트워크 대역폭(Gbps)을 점유한다고 오해",
            "explanation": "Slowloris와 RUDY는 네트워크 대역폭을 고갈시키는 L3/L4 플러딩이 아니라, 극소량의 트래픽을 매우 느린 속도로 지연 전송하여 웹 서버의 가용 연결 스레드(MaxClients)만을 고갈시키는 7계층 저대역폭 DoS 공격입니다."
        }
    ],
    "Q-DESC-035": [
        {
            "confused_term_or_misunderstanding": "CSRF 공격을 세션 쿠키를 직접 탈취하는 XSS와 동일시",
            "explanation": "XSS는 자바스크립트를 실행하여 쿠키나 세션 토큰을 직접 가로채지만, CSRF는 공격자가 쿠키를 직접 볼 수는 없으며 로그인된 피해자의 권한과 신뢰된 브라우저를 악용하여 원치 않는 송금이나 비밀번호 변경 요청을 대신 전송하게 만듭니다."
        }
    ],
    "Q-DESC-036": [
        {
            "confused_term_or_misunderstanding": "ServerTokens 지시자의 값을 Full로 설정하는 것이 보안상 안전하다고 오해",
            "explanation": "ServerTokens Full은 아파치 버전, 모듈, OS 배포판 정보까지 모두 응답 헤더에 노출하므로, 정보 노출을 최소화하기 위해서는 'ServerTokens Prod'로 설정하여 최소한의 식별자(Apache)만 출력되도록 해야 합니다."
        }
    ],
    "Q-DESC-037": [
        {
            "confused_term_or_misunderstanding": "XXE 공격 방어를 위해 입력값의 특정 특수문자만 치환하면 된다고 생각",
            "explanation": "외부 엔티티 참조는 다양한 인코딩으로 우회될 수 있으므로, XML 파서 자체의 설정(disallow-doctype-decl 또는 setFeature)에서 DTD(외부 엔티티 선언) 해석 기능을 완전히 비활성화(False)하는 것이 근본 방어책입니다."
        }
    ],
    "Q-DESC-038": [
        {
            "confused_term_or_misunderstanding": "TLS 핸드셰이크 과정에서 실제 대칭 암호화 통신에 사용되는 비밀키를 네트워크로 직접 전송한다고 오해",
            "explanation": "실제 데이터 암호화에 쓰이는 Master Secret은 직접 전송되지 않으며, 양측이 교환한 Random 값들과 공개키로 안전하게 암호화되어 전달된 Pre-Master Secret을 바탕으로 양단에서 각각 독립적으로 유도/계산됩니다."
        }
    ],
    "Q-DESC-039": [
        {
            "confused_term_or_misunderstanding": "Received 헤더의 위조 불가능성을 최상단 헤더 기준으로 오해",
            "explanation": "Received 헤더는 경유하는 각 MTA가 최상단에 덧붙이는 구조이므로 맨 위쪽 헤더는 신뢰받는 최종 수신 서버의 기록이지만, 최초 발신자가 임의로 조작하여 맨 아래에 삽입한 Received 헤더는 위조되었을 가능성을 배제할 수 없습니다."
        }
    ],
    "Q-DESC-040": [
        {
            "confused_term_or_misunderstanding": "교착상태 4대 조건 중 하나만 발생해도 데드락이 발생한다고 오해",
            "explanation": "데드락은 상호배제, 점유와 대기, 비선점, 환형 대기의 4가지 조건이 '동시에 모두 만족'할 때만 발생하며, 이 중 어느 하나라도 사전에 예방(무력화)하면 교착상태가 발생하지 않습니다."
        }
    ],
    "Q-DESC-041": [
        {
            "confused_term_or_misunderstanding": "NTFS의 ADS(Alternate Data Stream) 영역에 숨겨진 악성 파일이 일반 탐색기에서 보인다고 생각",
            "explanation": "ADS 영역에 은닉된 데이터는 Windows 기본 파일 탐색기나 'dir' 명령 실행 시 파일 크기가 0바이트로 표시되거나 은닉 스트림이 보이지 않으므로, 'dir /r' 명령을 통해 추가 데이터 스트림 존재 여부를 점검해야 합니다."
        }
    ],
    "Q-DESC-042": [
        {
            "confused_term_or_misunderstanding": "Windows 파일 공유(SMB) 포트인 445번과 NetBIOS-SSN 139번의 차이 혼동",
            "explanation": "포트 139번은 NetBIOS over TCP/IP 계층 위에서 동작하는 레거시 파일 공유 포트인 반면, 포트 445번은 NetBIOS 없이 TCP 위에서 직접 구동되는 Direct Host SMB 포트입니다."
        }
    ],
    "Q-DESC-043": [
        {
            "confused_term_or_misunderstanding": "IPS를 인라인(In-line) 배치했을 때 장비 장애 시 기본 동작을 무조건 Fail-Close로만 생각",
            "explanation": "보안이 최우선인 환경에서는 Fail-Close(차단)를 적용하지만, 중단 없는 서비스 가용성이 최우선인 비즈니스 환경에서는 하드웨어 바이패스(Bypass) 모듈을 통해 트래픽을 통과시키는 Fail-Open 정책을 적용하기도 합니다."
        }
    ],
    "Q-DESC-044": [
        {
            "confused_term_or_misunderstanding": "Teardrop 공격을 단순 단편화 패킷 대량 플러딩으로 오해",
            "explanation": "Teardrop은 패킷 양이 많은 것이 아니라, IP 헤더 내의 단편화 오프셋(Fragment Offset) 값과 길이를 고의로 중첩되게 조작하여 수신 시스템이 패킷 재조합(Reassembly) 시 내부 버퍼 계산 오류로 충돌/다운되도록 만드는 취약점 공격입니다."
        }
    ]
}

def build_rubric_for_descriptive(q):
    sub_qs = q.get("sub_questions") or []
    rubrics = []
    max_score = q.get("score", 12)

    for sub in sub_qs:
        sub_id = sub.get("sub_id", 1)
        sub_score = sub.get("score", 4)
        sub_prompt = sub.get("prompt", "")
        model_ans = sub.get("model_answer", "")
        rub_data = sub.get("rubric", {})
        kw_groups = rub_data.get("keywords", [])

        # Extract representative keywords from rubric
        required_kws = []
        for g in kw_groups:
            if not g:
                continue
            # Join up to 2 primary synonyms for clear display
            if len(g) >= 2:
                required_kws.append(f"{g[0]} / {g[1]}")
            else:
                required_kws.append(str(g[0]))

        criteria_text = f"소문항 {sub_id}번 ({sub_score}점): {sub_prompt} 핵심 내용 서술"
        if model_ans:
            criteria_text += f" (기준: {model_ans[:60]}...)"

        rubrics.append({
            "points": sub_score,
            "required_keywords": required_kws,
            "criteria": criteria_text
        })

    return {
        "max_score": max_score,
        "rubrics": rubrics
    }

def apply_chunk4(explanations, questions_map):
    applied_count = 0
    rubric_fixed_count = 0
    traps_fixed_count = 0

    for i in range(1, 45):
        qid = f"Q-DESC-{i:03d}"
        if qid not in explanations or qid not in questions_map:
            continue
        exp = explanations[qid]
        q = questions_map[qid]

        # 1. P1-2 Fix: Build authentic rubrics directly from questions.json
        exp["practical_scoring_criteria"] = build_rubric_for_descriptive(q)
        rubric_fixed_count += 1

        # 2. P1-3 Fix: Set precise, context-specific traps
        if qid in DESC_TRAPS:
            exp["why_wrong_common_traps"] = DESC_TRAPS[qid]
            traps_fixed_count += 1

        applied_count += 1

    print(f"Chunk 4 applied: {applied_count} descriptive questions updated.")
    print(f"  - P1-2 rubrics synchronized: {rubric_fixed_count}")
    print(f"  - P1-3 traps updated: {traps_fixed_count}")

if __name__ == "__main__":
    with open("app/data/explanations.json", "r", encoding="utf-8") as f:
        exps = json.load(f)
    with open("app/data/questions.json", "r", encoding="utf-8") as f:
        qs = {q["id"]: q for q in json.load(f)}

    apply_chunk4(exps, qs)

    with open("app/data/explanations.json", "w", encoding="utf-8") as f:
        json.dump(exps, f, indent=2, ensure_ascii=False)
    print("Chunk 4 changes saved successfully to explanations.json")
