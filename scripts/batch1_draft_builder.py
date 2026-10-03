import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Batch 1: 36 new questions (21 short, 9 descriptive, 6 practical)
# Total will be 64 + 36 = 100 questions

BATCH1_SHORT = [
    {
        "id": "Q-SHORT-042",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "concept_id": "CON-APP-01",
        "source_id": "SRC-01",
        "source_page": 21,
        "question": "HTTP 관련 공격 중 헤더의 개행문자(CRLF) 필드 끝을 고의로 전송하지 않고 조작된 불완전한 HTTP 헤더를 지속적으로 천천히 전송하여 웹서버의 동시 연결 자원(Connection Pool)을 고갈시키는 서비스 거부 공격의 명칭은 무엇인가?",
        "answer": "Slowloris",
        "accepted_answers": ["Slowloris", "Slow HTTP Header DoS", "Slow HTTP Header DoS 공격", "슬로우리더", "Slowloris 공격"],
        "grading_mode": "normalized",
        "explanation": "Slowloris(Slow HTTP Header DoS)는 HTTP 요청 헤더의 끝을 알리는 빈 줄(CRLF CRLF)을 보내지 않고 불필요한 헤더 필드를 지속적으로 지연 전송하여 웹서버가 연결을 유지하도록 강제함으로써 가용성을 침해하는 공격입니다.",
        "difficulty": "medium",
        "tags": ["Slowloris", "Slow_HTTP_Header_DoS", "DoS", "CRLF", "웹서버"]
    },
    {
        "id": "Q-SHORT-043",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "concept_id": "CON-APP-01",
        "source_id": "SRC-01",
        "source_page": 22,
        "question": "공격자가 사전에 이미 유출된 사용자들의 계정 및 패스워드 목록(Credential)을 확보한 후, 사용자들이 여러 웹사이트에 동일한 계정정보를 재사용한다는 점을 악용하여 다른 웹사이트들에 무작위로 자동 대입하여 인증 로그인을 시도하는 공격 기법은 무엇인가?",
        "answer": "크리덴셜 스터핑",
        "accepted_answers": ["크리덴셜 스터핑", "Credential Stuffing", "크리덴셜스터핑"],
        "grading_mode": "normalized",
        "explanation": "크리덴셜 스터핑(Credential Stuffing)은 이미 유출된 사용자 인증정보(ID/PW 쌍)를 다른 서비스들에 대입하여 인증을 시도하는 공격으로, CAPTCHA 및 다중인증(MFA) 도입으로 대응할 수 있습니다.",
        "difficulty": "medium",
        "tags": ["Credential_Stuffing", "크리덴셜스터핑", "계정탈취", "인증공격"]
    },
    {
        "id": "Q-SHORT-044",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-02",
        "source_id": "SRC-01",
        "source_page": 22,
        "question": "공격자가 Mimikatz 등 도구를 활용하여 윈도우 시스템 메모리에서 평문 암호 대신 탈취한 NTLM 또는 LanMan 해시 값을 원격 서버에 그대로 전송하여 인증을 통과하는 공격 기법의 명칭은 무엇인가?",
        "answer": "Pass the Hash",
        "accepted_answers": ["Pass the Hash", "Pass the hash", "패스 더 해시", "패스더해시", "PtH"],
        "grading_mode": "normalized",
        "explanation": "Pass the Hash(PtH)는 공격자가 패스워드를 평문으로 크래킹하지 않고 탈취한 해시(NTLM 등) 값을 그대로 사용하여 원격 서비스 인증을 획득하는 공격 기법입니다.",
        "difficulty": "medium",
        "tags": ["Pass_the_Hash", "NTLM", "Mimikatz", "윈도우인증", "해시탈취"]
    },
    {
        "id": "Q-SHORT-045",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "concept_id": "CON-NET-03",
        "source_id": "SRC-01",
        "source_page": 22,
        "question": "DNS 서버의 캐시에 위조된 도메인 IP 질의 응답 레코드를 주입하여, 사용자가 정상적인 도메인 이름으로 접속하더라도 공격자가 의도한 피싱 및 파밍 사이트로 유도되도록 만드는 공격은 무엇인가?",
        "answer": "DNS 캐시 포이즈닝",
        "accepted_answers": ["DNS 캐시 포이즈닝", "DNS 캐시포이즈닝", "DNS Cache Poisoning", "DNS Spoofing", "DNS 스푸핑"],
        "grading_mode": "normalized",
        "explanation": "DNS 캐시 포이즈닝은 DNS 해석기(Resolver)의 캐시에 조작된 주소 매핑을 저장시켜 사용자를 위조 사이트로 접속시키는 공격으로, DNSSEC 도입을 통해 방어합니다.",
        "difficulty": "medium",
        "tags": ["DNS", "DNS_Cache_Poisoning", "DNSSEC", "파밍", "위조"]
    },
    {
        "id": "Q-SHORT-046",
        "type": "short",
        "category": "정보보안 일반 및 암호학",
        "score": 3,
        "concept_id": "CON-SEC-01",
        "source_id": "SRC-01",
        "source_page": 22,
        "question": "사이버 킬체인 모델을 실무적으로 확장하여 공격자의 침해 전술(Tactics), 기술(Techniques), 절차(Procedures)를 총 14개 전술 단계의 매트릭스 형태로 체계화한 지식 베이스 프레임워크의 명칭은 무엇인가?",
        "answer": "MITRE ATT&CK",
        "accepted_answers": ["MITRE ATT&CK", "MITRE ATTACK", "ATT&CK", "마이터 어택", "마이트레 어택"],
        "grading_mode": "normalized",
        "explanation": "MITRE ATT&CK(Adversarial Tactics, Techniques, and Common Knowledge)은 사이버 공격자의 실제 행위 및 위협 전술·기법을 14대 전술 매트릭스로 분류한 글로벌 표준 보안 프레임워크입니다.",
        "difficulty": "medium",
        "tags": ["MITRE_ATTACK", "TTPs", "사이버킬체인", "위협분석", "프레임워크"]
    },
    {
        "id": "Q-SHORT-047",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "concept_id": "CON-MGT-01",
        "source_id": "SRC-01",
        "source_page": 23,
        "question": "보안 취약점의 기본 지표(공격 벡터, 복잡도, 인증 등), 시간성 지표, 환경적 지표를 종합적으로 고려하여 취약점의 심각도를 0~10점 사이의 수치로 표준화하여 평가하는 기준 체계의 영문 약어는 무엇인가?",
        "answer": "CVSS",
        "accepted_answers": ["CVSS", "Common Vulnerability Scoring System", "공통 취약점 등급 시스템"],
        "grading_mode": "normalized",
        "explanation": "CVSS(Common Vulnerability Scoring System)는 소프트웨어 보안 취약점의 특성과 심각도를 객관적인 정량 수치(0.0~10.0)로 산정하는 국제 공개 표준입니다.",
        "difficulty": "medium",
        "tags": ["CVSS", "취약점평가", "보안표준", "위험분석"]
    },
    {
        "id": "Q-SHORT-048",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "concept_id": "CON-MGT-01",
        "source_id": "SRC-01",
        "source_page": 23,
        "question": "침해사고 대응 7단계 절차 중 다음 ( 괄호 )에 들어갈 단계명은 무엇인가?\n[사고 전 준비] → [사고 탐지] → [ ( 괄호 ) ] → [대응 전략 체계화] → [사고 조사] → [보고서 작성] → [해결]",
        "answer": "초기 대응",
        "accepted_answers": ["초기 대응", "초기대응", "초기 조치", "Initial Response"],
        "grading_mode": "normalized",
        "explanation": "침해사고 대응 7단계는 준비 → 탐지 → 초기대응 → 대응전략체계화 → 사고조사 → 보고서작성 → 해결 순으로 진행되며, 초기대응 단계에서 피해 확산 방지 및 초기 증거 확보가 이루어집니다.",
        "difficulty": "medium",
        "tags": ["침해사고대응", "7단계", "초기대응", "사고조사"]
    },
    {
        "id": "Q-SHORT-049",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "concept_id": "CON-MGT-01",
        "source_id": "SRC-01",
        "source_page": 24,
        "question": "ISO 27005 위험평가(Risk Assessment)의 3단계 중, 잠재적인 손해 발생의 근원을 밝혀내기 위하여 자산, 위협, 기존 보안대책, 취약점을 식별하는 첫 번째 단계의 명칭은 무엇인가?",
        "answer": "위험식별",
        "accepted_answers": ["위험식별", "위험 식별", "Risk Identification", "Risk identification"],
        "grading_mode": "normalized",
        "explanation": "ISO 27005에 따른 위험평가는 '위험식별(Risk Identification) → 위험분석(Risk Analysis) → 위험수준평가(Risk Evaluation)'의 3단계로 구성됩니다.",
        "difficulty": "medium",
        "tags": ["ISO27005", "위험식별", "위험평가", "위험관리"]
    },
    {
        "id": "Q-SHORT-050",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-01",
        "source_page": 29,
        "question": "마이크로소프트와 3Com 등이 공동 개발한 대표적인 2계층(데이터 링크 계층) VPN 터널링 프로토콜로, PPP(Point-to-Point Protocol) 패킷을 IP 데이터그램에 캡슐화하여 인터넷을 통한 보안 터널을 생성하는 프로토콜의 영문 약어는 무엇인가?",
        "answer": "PPTP",
        "accepted_answers": ["PPTP", "Point-to-Point Tunneling Protocol", "Point to Point Tunneling Protocol"],
        "grading_mode": "normalized",
        "explanation": "PPTP(Point-to-Point Tunneling Protocol)는 데이터 링크 계층에서 동작하는 VPN 터널링 프로토콜로, TCP 1723번 포트를 통해 제어 연결을 맺고 GRE(IP 프로토콜 47)를 사용하여 PPP 데이터를 캡슐화합니다.",
        "difficulty": "medium",
        "tags": ["VPN", "PPTP", "터널링", "2계층", "네트워크보안"]
    },
    {
        "id": "Q-SHORT-051",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-01",
        "source_page": 24,
        "question": "리눅스 /etc/shadow 파일의 두 번째 필드(패스워드 암호화 필드: $id$salt$encrypted)에서 해시 알고리즘 식별자 ID가 '6'으로 설정되어 있을 때, 사용된 일방향 암호화 해시 알고리즘은 무엇인가?",
        "answer": "SHA-512",
        "accepted_answers": ["SHA-512", "SHA512", "sha512", "sha-512"],
        "grading_mode": "strict",
        "explanation": "shadow 파일의 암호화 알고리즘 ID: 1은 MD5, 2a는 Blowfish, 5는 SHA-256, 6은 SHA-512를 의미합니다. 현재 대부분의 리눅스 배포판은 SHA-512($6$)를 기본값으로 사용합니다.",
        "difficulty": "medium",
        "tags": ["shadow", "해시알고리즘", "SHA512", "리눅스계정"]
    },
    {
        "id": "Q-SHORT-052",
        "type": "short",
        "category": "정보보호 관리 및 법규",
        "score": 3,
        "concept_id": "CON-MGT-03",
        "source_id": "SRC-01",
        "source_page": 25,
        "question": "정보통신망 이용촉진 및 정보보호 등에 관한 법률에 따라 정보보호관리체계의 수립, 취약점 분석·개선, 침해사고 예방·대응 등 기업의 정보보호 관리 업무를 총괄 지휘하는 임원급 책임자의 명칭(직책)은 무엇인가?",
        "answer": "CISO",
        "accepted_answers": ["CISO", "정보보호최고책임자", "정보보호 최고책임자", "Chief Information Security Officer"],
        "grading_mode": "normalized",
        "explanation": "CISO(정보보호최고책임자)는 기업 내 정보통신시스템의 안전성 확보 및 정보보호 관리체계 수립·운영을 총괄하는 임원급 지위의 책임자입니다.",
        "difficulty": "low",
        "tags": ["CISO", "정보보호최고책임자", "정보통신망법", "관리체계"]
    },
    {
        "id": "Q-SHORT-053",
        "type": "short",
        "category": "정보보안 일반 및 암호학",
        "score": 3,
        "concept_id": "CON-SEC-01",
        "source_id": "SRC-01",
        "source_page": 25,
        "question": "사용자 엔드포인트(단말기) 영역에 대한 지속적인 모니터링을 통해 행위 기반의 이상 위협을 탐지하고, 공격 유입 경로를 추적·분석하여 즉각적인 격리 및 침해 대응 기능을 제공하는 보안 솔루션의 영문 약어는 무엇인가?",
        "answer": "EDR",
        "accepted_answers": ["EDR", "Endpoint Detection and Response", "Endpoint Detection & Response"],
        "grading_mode": "normalized",
        "explanation": "EDR(Endpoint Detection & Response)은 PC 및 서버 등 엔드포인트에서 발생하는 프로세스, 네트워크, 파일 행위 로그를 실시간 수집·분석하여 알려지지 않은 지능형 위협을 탐지·대응하는 기술입니다.",
        "difficulty": "medium",
        "tags": ["EDR", "엔드포인트보안", "보안솔루션", "행위탐지"]
    },
    {
        "id": "Q-SHORT-054",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-01",
        "source_page": 26,
        "question": "리눅스 시스템에서 특정 프로그램이나 프로세스가 실행 중에 호출하는 시스템 콜(System Call)과 수신하는 시그널을 실시간으로 추적·기록하여 트로이목마 감염 파일이나 비인가 동작을 분석할 때 사용하는 명령어는 무엇인가?",
        "answer": "strace",
        "accepted_answers": ["strace"],
        "grading_mode": "strict",
        "explanation": "strace는 바이너리 실행 파일이 커널에 요청하는 시스템 콜(open, read, write, connect 등)을 모니터링하여 악성 행위나 설정 오류를 디버깅하는 시스템 명령어입니다.",
        "difficulty": "medium",
        "tags": ["strace", "시스템콜", "프로세스추적", "리눅스명령어"]
    },
    {
        "id": "Q-SHORT-055",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-01",
        "source_page": 27,
        "question": "비연결형 전송 계층 프로토콜인 UDP 환경에서 스트리밍 및 음성/영상 통신 시 패킷 도청과 변조를 방지하기 위해 TLS와 유사한 기밀성, 무결성, 인증 기능을 제공하는 보안 프로토콜의 영문 약어는 무엇인가?",
        "answer": "DTLS",
        "accepted_answers": ["DTLS", "Datagram Transport Layer Security", "Datagram TLS"],
        "grading_mode": "normalized",
        "explanation": "DTLS(Datagram Transport Layer Security)는 패킷 유실과 재정렬이 발생할 수 있는 UDP 데이터그램 환경에서 TLS 암호화 보안을 제공하기 위해 설계된 통신 표준 프로토콜입니다.",
        "difficulty": "medium",
        "tags": ["DTLS", "UDP", "TLS", "네트워크보안", "암호프로토콜"]
    },
    {
        "id": "Q-SHORT-056",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-01",
        "source_page": 28,
        "question": "IoT 기기나 가정용 공유기 등에서 네트워크 장치 탐색에 사용되는 UDP 1900번 포트를 악용하여, 공격자가 출발지 IP를 피해자 IP로 위조한 M-SEARCH 요청을 전송해 대량의 반사 패킷을 유발하는 DRDoS 공격의 명칭은 무엇인가?",
        "answer": "SSDP DRDoS",
        "accepted_answers": ["SSDP DRDoS", "SSDP DRDoS 공격", "SSDP 증폭 공격", "SSDP Amplification Attack", "SSDP 반사 공격"],
        "grading_mode": "normalized",
        "explanation": "SSDP(Simple Service Discovery Protocol) DRDoS는 UPnP 장치가 사용하는 UDP 1900 포트에 질의를 보내 정상 응답 크기보다 수십 배 증폭된 반사 응답을 피해자에게 집중시키는 DDoS 공격입니다.",
        "difficulty": "medium",
        "tags": ["SSDP", "DRDoS", "반사공격", "증폭공격", "UDP_1900"]
    },
    {
        "id": "Q-SHORT-057",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-01",
        "source_page": 28,
        "question": "Snort의 시그니처 룰 체계를 수용하면서도 멀티스레드(Multi-threading) 아키텍처와 하드웨어 가속을 지원하여 기가비트급 고속 대용량 트래픽 환경에서 실시간 패킷 탐지 및 차단에 특화된 오픈소스 NIDS/IPS 소프트웨어 명칭은 무엇인가?",
        "answer": "Suricata",
        "accepted_answers": ["Suricata", "수리카타", "suricata"],
        "grading_mode": "normalized",
        "explanation": "Suricata(수리카타)는 Snort와 호환되는 룰 문법을 사용하면서 멀티스레딩을 완벽 지원하여 대규모 엔터프라이즈 트래픽 환경에서 높은 처리 성능을 보이는 대표적 차세대 오픈소스 IDS/IPS입니다.",
        "difficulty": "medium",
        "tags": ["Suricata", "수리카타", "NIDS", "IPS", "멀티스레드"]
    },
    {
        "id": "Q-SHORT-058",
        "type": "short",
        "category": "정보보안 일반 및 암호학",
        "score": 3,
        "concept_id": "CON-CRY-01",
        "source_id": "SRC-01",
        "source_page": 29,
        "question": "TLS 암호화 통신 시 핸드셰이크 협상 과정을 강제로 SSL 3.0 레거시 버전으로 다운그레이드 유도한 후, CBC 암호 모드의 패딩 검증 오류를 악용하여 암호문을 해독하는 공격 기법의 명칭은 무엇인가?",
        "answer": "POODLE",
        "accepted_answers": ["POODLE", "푸들", "푸들 공격", "POODLE 공격", "Padding Oracle On Downgraded Legacy Encryption"],
        "grading_mode": "normalized",
        "explanation": "POODLE 공격은 안전하지 않은 SSL 3.0으로의 다운그레이드를 유도하고 패딩 바이트 오라클을 통해 웹 쿠키나 세션 토큰 등의 암호화된 데이터를 바이트 단위로 복호화하는 공격입니다.",
        "difficulty": "medium",
        "tags": ["POODLE", "SSL3.0", "패딩오라클", "암호공격", "다운그레이드"]
    },
    {
        "id": "Q-SHORT-059",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-02",
        "source_id": "SRC-05",
        "source_page": 3,
        "question": "Windows 로컬 인증의 3대 핵심 구성요소(LSA, SAM, SRM) 중, 커널 모드에서 실행되며 인증된 사용자에게 고유한 SID를 부여하고 자원에 대한 접근 권한(ACL) 검사 및 감사 로그 생성을 담당하는 보안 서브시스템의 명칭은 무엇인가?",
        "answer": "SRM",
        "accepted_answers": ["SRM", "Security Reference Monitor", "보안 참조 모니터"],
        "grading_mode": "normalized",
        "explanation": "SRM(Security Reference Monitor)은 윈도우 커널 내에서 실행되며 사용자가 객체(파일, 프로세스 등)에 접근할 때 토큰의 SID와 객체의 ACL을 비교하여 접근 승인 여부를 최종 결정합니다.",
        "difficulty": "medium",
        "tags": ["SRM", "LSA", "SAM", "Windows인증", "SID"]
    },
    {
        "id": "Q-SHORT-060",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-05",
        "source_page": 9,
        "question": "리눅스 시스템에서 일반 사용자의 crontab 명령어 사용을 통제하기 위해 접근 허용 목록을 지정하는 파일의 절대 경로는 무엇인가?",
        "answer": "/etc/cron.allow",
        "accepted_answers": ["/etc/cron.allow"],
        "grading_mode": "strict",
        "explanation": "crontab 접근제어: /etc/cron.allow 파일이 존재하면 이 파일에 등록된 사용자만 cron 작업 등록이 가능하며, 존재하지 않으면 /etc/cron.deny 파일에 등록되지 않은 사용자만 작업 등록이 허용됩니다.",
        "difficulty": "low",
        "tags": ["crontab", "cron.allow", "cron.deny", "접근통제", "리눅스경로"]
    },
    {
        "id": "Q-SHORT-061",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-05",
        "source_page": 10,
        "question": "리눅스 PAM(Pluggable Authentication Modules) 설정 파일에서 모듈의 동작 성격을 규정하는 4대 모듈 타입(Module Type)을 모두 기술하시오.",
        "answer": "auth, account, password, session",
        "accepted_answers": ["auth, account, password, session", "auth,account,password,session", "auth, account, session, password"],
        "grading_mode": "normalized",
        "explanation": "PAM의 4대 모듈 타입: auth(사용자 신원 확인 및 인증), account(계정 유효성 및 권한 만료 점검), password(패스워드 변경 및 복잡도 검증), session(로그인 전후 환경설정 및 세션 감사).",
        "difficulty": "medium",
        "tags": ["PAM", "auth", "account", "password", "session"]
    },
    {
        "id": "Q-SHORT-062",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-05",
        "source_page": 10,
        "question": "리눅스 시스템에서 사용자의 잘못된 로그인 시도나 5회 이상 인증 실패 등 실패한 로그인 기록을 바이너리 형태로 누적 저장하는 로그 파일의 절대 경로는 무엇인가? (lastb 명령어로 확인 가능)",
        "answer": "/var/log/btmp",
        "accepted_answers": ["/var/log/btmp"],
        "grading_mode": "strict",
        "explanation": "리눅스 로그 파일: /var/log/wtmp(성공한 로그인/로그아웃, last), /var/log/btmp(실패한 로그인, lastb), /var/run/utmp(현재 접속자, who/w).",
        "difficulty": "low",
        "tags": ["btmp", "lastb", "로그파일", "실패기록", "리눅스경로"]
    }
]

BATCH1_DESC = [
    {
        "id": "Q-DESC-016",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-02",
        "source_page": 18,
        "question": "네트워크 관리자가 시스템 모니터링 중 'device eth0 entered Promiscuous mode' 로그를 확인하였다. 이와 관련하여 다음 물음에 답하시오.\n\n1) Promiscuous mode(무차별 모드)의 동작 개념을 기술하시오. (4점)\n2) 공격자가 해당 모드로 진입 시 수행할 수 있는 대표적 보안 위협은 무엇인가? (4점)\n3) 해당 보안 위협에 대응할 수 있는 기술적 방안 2가지를 설명하시오. (4점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) Promiscuous mode(무차별 모드)의 동작 개념",
                "model_answer": "NIC(네트워크 인터페이스 카드)의 필터링 기능을 해제하여, 자신의 MAC 주소가 목적지가 아닌 패킷이라도 버리지 않고 모두 수신하여 상위 계층으로 전달하는 모드이다.",
                "rubric": {
                    "keywords": [
                        ["목적지", "자신의 mac", "자신", "목적지 주소"],
                        ["버리지 않고", "모두 수신", "모든 패킷", "전부 수신"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 무차별 모드 진입 시 수행 가능한 대표적 공격",
                "model_answer": "네트워크 패킷 스니핑(Sniffing) 공격으로, 평문으로 전송되는 계정 정보, 패스워드, 세션 토큰 등 기밀 데이터를 도청할 수 있다.",
                "rubric": {
                    "keywords": [
                        ["스니핑", "패킷 스니핑", "sniffing", "도청", "패킷 도청"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 스니핑 위협 대응 기술적 방안 2가지",
                "model_answer": "1) SSH, HTTPS, IPsec 등 종단 간 암호화 프로토콜을 적용하여 데이터 기밀성 보장\n2) 더미 허브 대신 지능형 스위치(Switch)를 사용하여 불필요한 브로드캐스팅 패킷 유입을 차단하고, ifconfig promisc 해제 설정",
                "rubric": {
                    "keywords": [
                        ["암호화", "ssh", "https", "ipsec", "tls"],
                        ["스위치", "지능형 스위치", "arp 감시", "-promisc"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "model_answer": "1) 무차별 모드는 자신에게 오지 않은 패킷도 Drop하지 않고 모두 수신하는 모드\n2) 패킷 스니핑(도청) 공격\n3) 암호화 통신(SSH, HTTPS 등) 적용 및 지능형 스위치 사용",
        "explanation": "Promiscuous 모드는 Wireshark 등 패킷 분석을 위해 사용되나, 공격자가 침투하여 활성화할 경우 내부망의 평문 통신을 도청하는 스니핑 공격에 악용됩니다.",
        "difficulty": "medium",
        "tags": ["Promiscuous", "무차별모드", "스니핑", "스위치", "암호화"]
    },
    {
        "id": "Q-DESC-017",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-02",
        "source_page": 25,
        "question": "분산 반사 서비스 거부 공격인 DRDoS(Distributed Reflection DoS)에 대하여 다음 물음에 답하시오.\n\n1) DRDoS의 핵심 공격 동작 원리를 기술하시오. (4점)\n2) 기존의 일반 DoS/DDoS 공격과 비교했을 때 DRDoS가 갖는 공격자 측면의 주요 특징 2가지를 기술하시오. (4점)\n3) 네트워크 라우터에서 IP 스푸핑 공격을 차단하기 위해 사용하는 Unicast RPF(Reverse Path Forwarding)의 원리를 설명하시오. (4점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) DRDoS의 핵심 공격 동작 원리",
                "model_answer": "공격자가 출발지 IP 주소를 피해자(공격대상)의 IP로 위조(스푸핑)하여 다수의 반사 서버(DNS, NTP 등)로 요청을 전송하고, 반사 서버들이 대량의 응답 패킷을 피해자에게 일제히 집중 전송하여 서비스 거부를 유발한다.",
                "rubric": {
                    "keywords": [
                        ["출발지 ip", "소스 ip", "ip 스푸핑", "위조"],
                        ["반사 서버", "반사", "증폭", "응답"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 일반 DoS와 대비되는 DRDoS의 주요 특징 2가지",
                "model_answer": "1) 출발지 IP가 위조되고 정상 반사 서버를 경유하므로 실제 공격자의 위치 추적이 극히 어렵다.\n2) 좀비 PC를 대량으로 장악하지 않고도 반사 서버의 증폭 효과(Amplification)를 통해 대규모 공격 트래픽을 손쉽게 생성할 수 있다.",
                "rubric": {
                    "keywords": [
                        ["추적", "역추적", "출처", "어려움", "은닉"],
                        ["증폭", "좀비", "효율", "트래픽"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) Unicast RPF의 동작 원리",
                "model_answer": "라우터 인터페이스로 유입되는 패킷의 출발지 IP 주소를 라우팅 테이블과 대조하여, 해당 IP로 되돌아가는 최적의 경로(Reverse Path)가 패킷이 들어온 인터페이스와 일치하면 통과시키고 일치하지 않으면 위조된 IP로 판단하여 패킷을 차단(Drop)한다.",
                "rubric": {
                    "keywords": [
                        ["출발지 ip", "라우팅 테이블", "인터페이스"],
                        ["일치", "역경로", "reverse path", "차단", "drop"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "model_answer": "1) 출발지 IP를 위조하여 반사서버로 요청 후 반사 응답이 피해자에게 집중\n2) 공격자 추적 곤란 및 좀비PC 없이도 대규모 증폭 트래픽 생성\n3) 수신 인터페이스와 라우팅 역경로가 일치하지 않는 위조 패킷 차단",
        "explanation": "DRDoS는 TCP 3-Way Handshake가 없는 UDP 프로토콜의 특성과 반사 서버를 악용하며, 라우터 경계단에서 uRPF(Unicast Reverse Path Forwarding) 및 Ingress 필터링을 통해 출발지 위조 패킷을 차단해야 합니다.",
        "difficulty": "medium",
        "tags": ["DRDoS", "반사공격", "uRPF", "IP스푸핑", "라우팅"]
    },
    {
        "id": "Q-DESC-018",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-02",
        "source_page": 26,
        "question": "패킷 필터링 방화벽 기술과 관련하여 다음 물음에 답하시오.\n\n1) 인터넷 상에서 사용되지 않는 사설 IP나 미할당 IP를 출발지로 하는 스푸핑 공격을 막기 위한 방화벽 필터링 기술 명칭과 원리를 기술하시오. (3점)\n2) 공격자가 패킷을 아주 잘게 쪼개어 전송하는 Tiny Fragment(미세 단편화) 공격을 수행하는 목적(이유)을 기술하시오. (3점)\n3) Tiny Fragment 공격에 대응하기 위한 보안 방안을 기술하시오. (3점)\n4) Stateful Inspection(상태 추적) 패킷 필터링 방화벽이 기존 정적 패킷 필터링 방화벽과 구별되는 핵심 차이점을 설명하시오. (3점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 외부 IP 스푸핑 차단 필터링 기술명 및 원리",
                "model_answer": "Ingress 필터링: 외부에서 유입되는 패킷 중 출발지 IP 주소가 사설 IP 대역이거나 인터넷에서 유효하지 않은 비정상 IP인 경우 경계 라우터나 방화벽에서 즉각 차단한다.",
                "rubric": {
                    "keywords": [
                        ["ingress", "인그레스", "수신 필터링"],
                        ["사설 ip", "미할당", "비정상", "차단"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) Tiny Fragment 공격을 수행하는 목적",
                "model_answer": "첫 번째 조각(Fragment)의 크기를 매우 작게 만들어 TCP 헤더의 포트 번호 정보가 첫 번째 조각에 포함되지 않고 다음 조각으로 넘어가도록 분할함으로써, 포트 기반 필터링 룰을 우회하기 위함이다.",
                "rubric": {
                    "keywords": [
                        ["포트 번호", "헤더", "포트"],
                        ["우회", "필터링 우회", "검사 우회", "분할"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) Tiny Fragment 공격 대응 방안",
                "model_answer": "1) 단편화된 패킷을 즉시 통과시키지 않고 메모리에 수집하여 온전히 재조합(Reassembly)한 후 룰을 검사하거나,\n2) 포트 번호가 포함될 수 없을 정도로 지나치게 작은 크기의 단편 패킷은 방화벽에서 즉시 폐기(Drop)한다.",
                "rubric": {
                    "keywords": [
                        ["재조합", "reassembly", "단편 결합"],
                        ["폐기", "drop", "차단", "작은 크기"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) Stateful Inspection 방화벽의 핵심 차이점",
                "model_answer": "단순 패킷 헤더의 IP/포트만을 정적으로 비교하는 1세대와 달리, 통신 세션의 상태 테이블(State Table)을 유지하여 정상적인 3-Way Handshake를 거친 유효한 세션의 패킷만 통과시키며 비정상 패킷을 지능적으로 차단한다.",
                "rubric": {
                    "keywords": [
                        ["상태 테이블", "state table", "세션 상태", "연결 상태"],
                        ["핸드셰이크", "handshake", "추적", "정상 세션"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "model_answer": "1) Ingress 필터링: 유효하지 않은 외부 유입 IP 차단\n2) 헤더의 포트 정보를 분할하여 방화벽 룰 우회 목적\n3) 단편화 패킷 재조합 후 검사 및 미세 패킷 Drop\n4) 상태 테이블을 통한 세션 연속성 및 정당성 추적",
        "explanation": "네트워크 패킷 필터링은 단순 헤더 매칭의 한계를 극복하기 위해 Ingress/Egress 필터링, 패킷 재조합, Stateful Inspection 세션 추적 기법을 통합적으로 운용해야 합니다.",
        "difficulty": "medium",
        "tags": ["방화벽", "Ingress", "TinyFragment", "StatefulInspection", "패킷필터링"]
    },
    {
        "id": "Q-DESC-019",
        "type": "descriptive",
        "category": "정보보호 관리 및 법규",
        "score": 12,
        "concept_id": "CON-MGT-02",
        "source_id": "SRC-02",
        "source_page": 30,
        "question": "개인정보보호법에 규정된 가명정보(Pseudonymized Data)의 처리 및 활용과 관련하여 다음 물음에 답하시오.\n\n1) 개인정보보호법상 '가명처리'의 법적 정의를 기술하시오. (3점)\n2) 개인정보 가명처리 4단계 절차 중 3번째 단계의 명칭을 기술하시오. (3점)\n3) 가명정보를 정보주체의 동의 없이도 처리 및 활용할 수 있도록 법률로 허용된 3대 목적을 모두 기술하시오. (3점)\n4) 가명정보와 달리 더 이상 다른 정보를 사용하여도 특정 개인을 알아볼 수 없는 정보로 개인정보보호법의 적용 대상에서 완전히 제외되는 정보의 명칭을 기술하시오. (3점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 가명처리의 법적 정의",
                "model_answer": "개인정보의 일부를 삭제하거나 일부 또는 전부를 대체하는 등의 방법으로 추가 정보가 없이는 특정 개인을 알아볼 수 없도록 처리하는 것을 말한다.",
                "rubric": {
                    "keywords": [
                        ["삭제", "대체", "일부"],
                        ["추가 정보", "알아볼 수 없도록", "특정 개인"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 가명처리 4단계 중 3번째 단계명",
                "model_answer": "적정성 검토 및 추가 가명처리 (사전준비 → 가명처리 → 적정성 검토 및 추가 가명처리 → 사후관리)",
                "rubric": {
                    "keywords": [
                        ["적정성 검토", "적정성", "추가 가명처리"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 정보주체 동의 없이 가명정보 처리가 허용되는 3대 목적",
                "model_answer": "1) 통계작성(상업적 통계 포함), 2) 과학적 연구(산업적 연구 개발 포함), 3) 공익적 기록보존",
                "rubric": {
                    "keywords": [
                        ["통계", "통계작성"],
                        ["과학적 연구", "연구"],
                        ["공익적 기록보존", "기록보존"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 법 적용에서 제외되는 정보 명칭",
                "model_answer": "익명정보 (Anonymous Data)",
                "rubric": {
                    "keywords": [
                        ["익명정보", "익명화 정보", "anonymous"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "model_answer": "1) 추가 정보 없이는 특정 개인을 식별할 수 없도록 처리한 정보\n2) 적정성 검토 및 추가 가명처리\n3) 통계작성, 과학적 연구, 공익적 기록보존\n4) 익명정보",
        "explanation": "가명정보는 데이터 경제 활성화를 위해 3대 목적(통계, 연구, 기록보존)에 한해 동의 없이 활용 가능하며, 추가 식별이 원천 불가능한 익명정보는 개인정보보호법 적용이 배제됩니다.",
        "difficulty": "medium",
        "tags": ["가명처리", "가명정보", "익명정보", "개인정보보호법", "적정성검토"]
    },
    {
        "id": "Q-DESC-020",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "concept_id": "CON-NET-02",
        "source_id": "SRC-02",
        "source_page": 31,
        "question": "내부망 단말 보안 강화를 위해 도입하는 NAC(Network Access Control, 네트워크 접근제어)의 물리적 구성 방식인 인라인(In-Line) 방식과 아웃오브밴드(Out-of-Band) 방식에 대하여 다음 물음에 답하시오.\n\n1) 인라인(In-Line) 방식의 배치 구성 및 장단점을 기술하시오. (6점)\n2) 아웃오브밴드(Out-of-Band) 방식의 배치 구성 및 장단점을 기술하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) 인라인(In-Line) 방식의 구성 및 장단점",
                "model_answer": "- 구성: 트래픽이 통과하는 네트워크 전송 경로(주로 엑세스 스위치와 분배 스위치 사이)에 직접 직렬로 배치\n- 장점: 비인가 단말의 트래픽을 실시간으로 직접 차단 및 제어할 수 있어 통제력이 매우 우수함\n- 단점: 장비 장애 시 네트워크 전체가 단절되는 단일장애점(SPOF) 문제가 있으며, 고성능 패킷 처리가 요구되고 네트워크 물리 재구성이 필요함",
                "rubric": {
                    "keywords": [
                        ["직렬", "전송 경로", "경로에 배치", "통과 경로"],
                        ["실시간 차단", "차단", "통제력"],
                        ["spof", "단일장애점", "장애", "성능 부하"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) 아웃오브밴드(Out-of-Band) 방식의 구성 및 장단점",
                "model_answer": "- 구성: 스위치의 일반 포트나 미러링(SPAN) 포트에 별도로 병렬 연결하여 제어 트래픽을 송수신\n- 장점: 기존 네트워크 물리 구조 변경이 필요 없고 장애가 발생해도 실제 데이터 전송에 영향을 주지 않음\n- 단점: ARP Spoofing이나 802.1X 기반으로 간접 차단하므로 인라인 방식에 비해 차단의 실시간성이 떨어지고 우회 가능성이 존재함",
                "rubric": {
                    "keywords": [
                        ["미러링", "스위치 포트", "병렬", "일반 포트"],
                        ["네트워크 영향 없음", "spof 없음", "구축 용이"],
                        ["실시간성 저하", "지연", "간접 차단"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) 인라인: 트래픽 경로상 직렬 배치, 실시간 직접 차단 가능하나 장애 시 SPOF 위험 및 고성능 요구\n2) 아웃오브밴드: 스위치 포트에 병렬 배치, 서비스 영향 없으나 차단 실시간성 및 신뢰도 다소 저하",
        "explanation": "NAC 솔루션 도입 시 가용성이 최우선인 망은 아웃오브밴드 방식을 선호하며, 완벽한 비인가 단말 격리가 요구되는 폐쇄망은 인라인 방식을 채택합니다.",
        "difficulty": "medium",
        "tags": ["NAC", "인라인", "아웃오브밴드", "SPOF", "접근제어"]
    },
    {
        "id": "Q-DESC-021",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "concept_id": "CON-SYS-02",
        "source_id": "SRC-05",
        "source_page": 3,
        "question": "Windows 로컬 보안 서브시스템 및 인증 체계와 관련하여 다음 물음에 답하시오.\n\n1) Windows 인증을 구성하는 LSA, SAM, SRM 세 구성요소의 핵심 역할을 각각 설명하시오. (6점)\n2) Windows에서 인증된 사용자나 그룹에 부여되는 보안 식별자(SID)의 개념과 일반적인 문자열 구조(예: S-1-5-21-...)의 주요 구성요소를 설명하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) LSA, SAM, SRM 세 구성요소의 역할",
                "model_answer": "- LSA(Local Security Authority): 로컬 및 원격 로그인 검증, 시스템 보안 정책 적용, SRM이 전달한 보안 감사 로그를 기록하는 중앙 보안 서브시스템\n- SAM(Security Account Manager): 사용자 및 그룹 계정 정보와 해시 암호화된 패스워드 정보를 SAM 파일 DB에 안전하게 보관 및 관리\n- SRM(Security Reference Monitor): 커널 모드에서 실행되며 사용자에게 SID가 포함된 액세스 토큰을 부여하고, 객체 접근 시 ACL을 비교하여 권한을 검사",
                "rubric": {
                    "keywords": [
                        ["lsa", "로그인 검증", "감사 로그", "보안 정책"],
                        ["sam", "계정 정보", "패스워드", "db"],
                        ["srm", "커널", "sid", "acl", "접근 검사"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) SID 개념 및 구조 설명",
                "model_answer": "- 개념: Windows에서 사용자 계정, 그룹, 컴퓨터를 고유하게 식별하기 위해 발급하는 불변의 고유 문자열\n- 구조: S-1-5-21-A-B-C-500 형태\n  1) S: SID를 식별하는 접두사\n  2) 1: 리비전(버전) 번호\n  3) 5: 식별자 권한 기관 (5는 NT Authority)\n  4) 21-A-B-C: 도메인 또는 로컬 컴퓨터 고유 서브 어소리티 값\n  5) 500(마지막 숫자): 상대 식별자(RID, 500은 관리자 Administrator, 501은 Guest, 1000 이상은 일반사용자)",
                "rubric": {
                    "keywords": [
                        ["보안 식별자", "고유 식별", "사용자 계정"],
                        ["rid", "상대 식별자", "500", "administrator", "리비전"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) LSA(로그인 검증/감사기록), SAM(계정/해시DB 관리), SRM(커널 권한검사/SID 토큰 발급)\n2) SID는 윈도우 고유 식별자로 S(접두사)-버전-기관-도메인ID-RID(상대ID: 500 관리자 등)로 구성",
        "explanation": "윈도우는 계정 이름이 변경되더라도 내부적으로는 고유한 SID를 기반으로 권한을 관리하므로, SRM이 토큰 내 SID와 파일 ACL을 비교하여 접근을 제어합니다.",
        "difficulty": "medium",
        "tags": ["Windows인증", "LSA", "SAM", "SRM", "SID", "RID"]
    },
    {
        "id": "Q-DESC-022",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-05",
        "source_page": 6,
        "question": "리눅스 계정 보안의 핵심 파일인 /etc/shadow의 구조 및 설정과 관련하여 다음 물음에 답하시오.\n\n1) /etc/shadow 파일의 한 행은 총 9개 필드로 콜론(:)으로 구분된다. 다음 형식에서 각 필드의 의미를 설명하시오. (6점)\n`user:$6$salt$encrypted:19000:0:90:7:30:19500:`\n\n2) 위 설정 값을 분석하여 패스워드 최소/최대 사용 기간, 변경 경고 기간, 만료 후 유예 기간의 구체적인 설정 의미를 기술하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) /etc/shadow 파일 필드 의미 설명",
                "model_answer": "1필드: 사용자 계정명(user)\n2필드: 암호화된 패스워드($6$은 SHA-512)\n3필드: 최종 패스워드 변경일(1970-01-01부터 경과한 일수)\n4필드: 패스워드 최소 사용 일수(변경 금지 기간)\n5필드: 패스워드 최대 사용 일수(유효 기간)\n6필드: 패스워드 만료 전 경고 일수\n7필드: 패스워드 만료 후 계정 잠금 전 유예 일수(비활성 기간)\n8필드: 계정 만료일(1970-01-01부터 경과 일수)\n9필드: 예약 필드",
                "rubric": {
                    "keywords": [
                        ["계정명", "사용자"],
                        ["암호화", "패스워드", "해시"],
                        ["최소 사용", "최대 사용", "경고", "유예", "만료"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) 제시된 설정값의 보안 정책 의미",
                "model_answer": "- 0 (4필드): 패스워드 변경 후 즉시 재변경 가능(최소 사용기간 없음)\n- 90 (5필드): 패스워드 최대 사용기간 90일 (90일마다 의무적으로 패스워드 변경 필요)\n- 7 (6필드): 패스워드 만료 7일 전부터 로그인 시 변경 경고 메시지 출력\n- 30 (7필드): 패스워드 만료 후 30일 동안 변경하지 않으면 계정 영구 비활성화(잠금)",
                "rubric": {
                    "keywords": [
                        ["최대 90일", "90일", "유효기간"],
                        ["경고 7일", "7일 전", "경고"],
                        ["유예 30일", "비활성화", "계정 잠금", "30일"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) shadow 9필드: 계정명:암호화패스워드:최종변경일:최소일수:최대일수:경고일수:유예일수:만료일:예약\n2) 90일마다 변경 의무, 만료 7일 전 경고 시작, 만료 후 30일 미변경 시 계정 잠금 처리",
        "explanation": "/etc/shadow 파일은 root 전용(0400 또는 0000 권한)으로 관리되며, 주기적인 패스워드 변경(최대 90일 이하) 및 경고 정책을 강제하는 패스워드 에이징의 핵심 파일입니다.",
        "difficulty": "medium",
        "tags": ["shadow", "패스워드에이징", "리눅스계정", "계정보안"]
    },
    {
        "id": "Q-DESC-023",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "concept_id": "CON-SYS-03",
        "source_id": "SRC-05",
        "source_page": 11,
        "question": "시스템 소프트웨어의 메모리 취약점인 버퍼 오버플로우(Buffer Overflow) 공격과 방어 기술에 대하여 다음 물음에 답하시오.\n\n1) 스택 버퍼 오버플로우(Stack BOF) 공격의 발생 원리와 프로세스의 실행 흐름(EIP/RIP)을 변조하는 과정을 설명하시오. (6점)\n2) 운영체제 및 컴파일러 수준에서 버퍼 오버플로우를 무력화하기 위해 적용하는 3대 대표적 방어 기술(ASLR, DEP/NX, Stack Canary)의 동작 원리를 각각 기술하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) 스택 BOF 원리 및 실행 흐름 변조 과정",
                "model_answer": "프로그램에서 입력값의 크기를 검증하지 않는 함수(strcpy, gets 등)를 사용할 때 할당된 버퍼보다 큰 데이터를 입력하면, 버퍼 뒤에 위치한 SFP(Saved Frame Pointer)와 RET(Return Address)를 덮어쓰게 된다. 함수 종료 시 변조된 RET 주소로 점프하여 공격자가 주입한 쉘코드(Shellcode)를 실행하게 된다.",
                "rubric": {
                    "keywords": [
                        ["경계 검사", "크기 검증", "strcpy", "버퍼 크기"],
                        ["ret", "return address", "복귀 주소", "반환 주소"],
                        ["쉘코드", "점프", "실행 흐름", "eip"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) ASLR, DEP/NX, Stack Canary 동작 원리",
                "model_answer": "- ASLR(Address Space Layout Randomization): 프로그램 실행 시마다 스택, 힙, 라이브러리 메모리 주소를 무작위로 배치하여 공격자가 쉘코드 주소를 예측하지 못하게 방어\n- DEP/NX(Data Execution Prevention / Never eXecute): 스택과 힙 등 데이터 영역에 실행(Execute) 권한을 제거하여 악성 쉘코드가 주입되어도 실행되지 않고 크래시 발생\n- Stack Canary: 스택 버퍼와 복귀주소(RET) 사이에 특정한 랜덤 값(Canary)을 삽입해 두고, 함수 종료 전 이 값이 변조되었는지 검사하여 변조 시 실행을 즉시 중단",
                "rubric": {
                    "keywords": [
                        ["aslr", "주소 무작위", "랜덤", "예측 방지"],
                        ["dep", "nx", "실행 권한 제거", "실행 방지"],
                        ["카나리", "canary", "랜덤 값", "ret 변조 검사"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) 버퍼 경계 미검증으로 RET(복귀주소)를 덮어써 악성 쉘코드로 실행 흐름 탈취\n2) ASLR(메모리 주소 무작위화), DEP/NX(데이터 영역 실행 권한 차단), Canary(RET 앞 무결성 검증값 삽입)",
        "explanation": "버퍼 오버플로우 방어를 위해 안전한 함수(strncpy, fgets) 사용뿐만 아니라 커널 차원의 ASLR, CPU 레벨의 DEP(NX bit), 컴파일러 레벨의 Stack Shield/Canary를 복합 적용합니다.",
        "difficulty": "medium",
        "tags": ["BOF", "버퍼오버플로우", "ASLR", "DEP", "NX", "Canary"]
    },
    {
        "id": "Q-DESC-024",
        "type": "descriptive",
        "category": "정보보안 일반 및 암호학",
        "score": 12,
        "concept_id": "CON-CRY-01",
        "source_id": "SRC-09",
        "source_page": 30,
        "question": "암호 시스템의 양대 축인 대칭키 암호화(비밀키) 방식과 비대칭키 암호화(공개키) 방식에 대하여 다음 물음에 답하시오.\n\n1) 대칭키 암호화 방식과 비대칭키 암호화 방식의 기본 개념 및 키(Key) 사용 구조의 차이점을 설명하시오. (6점)\n2) 두 암호화 방식을 1) 암·복호화 처리 속도, 2) 키 분배 및 관리(n명 참여 시 필요한 키 개수), 3) 전자서명/부인방지 제공 여부의 3가지 측면에서 상호 비교하여 서술하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) 대칭키 vs 비대칭키 기본 개념 및 키 구조",
                "model_answer": "- 대칭키(비밀키): 암호화할 때 사용하는 키와 복호화할 때 사용하는 키가 동일한 단일 키 방식 (예: AES, DES, ARIA, SEED)\n- 비대칭키(공개키): 암호화 키(공개키, Public Key)와 복호화 키(개인키, Private Key)가 수학적으로 연결된 서로 다른 키 쌍(Key Pair)을 사용하는 방식 (예: RSA, ECC, ElGamal)",
                "rubric": {
                    "keywords": [
                        ["대칭키", "동일한 키", "하나의 키", "비밀키"],
                        ["비대칭키", "공개키", "개인키", "서로 다른 키", "쌍"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) 세 가지 비교 기준별 상세 비교",
                "model_answer": "1) 처리 속도: 대칭키는 단순 블록/스트림 연산으로 처리 속도가 매우 빠른 반면, 비대칭키는 복잡한 수학적 연산으로 인해 상대적으로 연산 속도가 느림\n2) 키 관리 개수: n명의 참여자 통신 시 대칭키는 n(n-1)/2개의 키가 필요하여 관리가 어렵고 안전한 키 분배가 난제이나, 비대칭키는 각자 공개키/개인키 쌍(총 2n개)만 관리하면 되어 키 분배가 용이함\n3) 전자서명/부인방지: 대칭키는 키를 양자가 공유하므로 부인방지가 불가하나, 비대칭키는 송신자 본인의 비밀키로 전자서명을 생성하여 무결성 및 부인방지 기능을 완벽히 제공함",
                "rubric": {
                    "keywords": [
                        ["속도", "대칭키 빠름", "비대칭키 느림"],
                        ["n(n-1)/2", "2n", "키 관리", "키 분배"],
                        ["부인방지", "전자서명", "개인키 서명"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) 대칭키는 암복호화에 동일한 키 사용, 비대칭키는 공개키와 개인키 한 쌍 사용\n2) 대칭키: 빠른 속도, n(n-1)/2 키 관리 난제, 부인방지 불가 / 비대칭키: 느린 속도, 2n개 키 분배 용이, 전자서명/부인방지 가능",
        "explanation": "실제 인터넷 보안 통신(HTTPS/TLS, IPsec)은 비대칭키 방식으로 세션키를 안전하게 교환한 후, 대용량 데이터는 대칭키 방식으로 암호화하는 하이브리드 암호 방식을 채택합니다.",
        "difficulty": "medium",
        "tags": ["암호학", "대칭키", "비대칭키", "공개키", "부인방지", "키관리"]
    }
]

BATCH1_PRAC = [
    {
        "id": "Q-PRAC-009",
        "type": "practical",
        "category": "애플리케이션 보안",
        "score": 16,
        "concept_id": "CON-APP-01",
        "source_id": "SRC-02",
        "source_page": 21,
        "question": "다음은 아파치(Apache) 웹서버의 특정 업로드 디렉토리(/var/www/html/uploads)에 적용된 보안 설정 파일(.htaccess)의 내용이다. 내용을 분석하고 각 물음에 답하시오.\n\n[.htaccess 파일 내용]\n<FilesMatch \"\\.(ph|php|phtml|sh|cgi|pl)$\">\n    Order Allow,Deny\n    Deny from all\n</FilesMatch>\n\nAddType text/html .php .php3 .phtml\n\n1) `<FilesMatch \"\\.(ph|php|phtml|sh|cgi|pl)$\">` 지시자와 하위 `Deny from all` 설정이 방어하고자 하는 구체적인 보안 취약점과 동작 원리를 설명하시오. (8점)\n2) `AddType text/html .php .php3 .phtml` 설정이 공격자의 웹쉘(WebShell) 악용 공격을 무력화하는 원리를 MIME 타입 처리 관점에서 설명하시오. (8점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 8,
                "prompt": "1) FilesMatch 및 Deny from all의 방어 목적 및 동작 원리",
                "model_answer": "파일 업로드 취약점을 통해 업로드된 악성 서버사이드 스크립트(웹쉘) 파일에 대해 웹 브라우저나 외부 클라이언트가 직접 URL 호출을 수행하는 것을 전면 차단(HTTP 403 Forbidden)함으로써, 공격자가 웹쉘을 원격 실행하여 서버 권한을 획득하는 것을 방지한다.",
                "rubric": {
                    "keywords": [
                        ["웹쉘", "webshell", "악성 스크립트", "서버사이드"],
                        ["직접 호출", "url 호출", "접근 차단", "실행 방지", "403"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            },
            {
                "sub_id": 2,
                "score": 8,
                "prompt": "2) AddType text/html 재조정의 웹쉘 무력화 원리",
                "model_answer": "PHP 등 서버사이드 스크립트 확장자에 대한 MIME 타입을 아파치 해석 엔진(PHP Handler)이 실행하는 타입이 아닌 단순 텍스트/HTML(text/html)로 재정의함으로써, 설령 파일이 호출되더라도 웹서버가 스크립트를 서버 측에서 실행하지 않고 일반 텍스트 문서로 브라우저에 단순 출력하도록 만들어 웹쉘 실행을 무력화한다.",
                "rubric": {
                    "keywords": [
                        ["text/html", "mime 타입", "마임 타입", "일반 텍스트"],
                        ["서버 실행 방지", "실행되지 않", "단순 출력", "스크립트 미실행"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            }
        ],
        "model_answer": "1) 업로드된 PHP/스크립트 웹쉘에 대한 외부 직접 URL 호출 및 실행을 원천 차단\n2) PHP 확장자의 MIME 타입을 text/html로 변경하여 서버 측 스크립트 실행 엔진이 실행하지 않고 일반 텍스트로 단순 출력하도록 강제",
        "explanation": "업로드 디렉토리 보안은 파일 실행 권한 제거, 확장자 검증, URL 직접 호출 차단(FilesMatch), MIME 타입 재지정(AddType)의 다중 방어 체계로 구축해야 합니다.",
        "difficulty": "medium",
        "tags": ["아파치설정", "htaccess", "파일업로드", "웹쉘", "MIME"]
    },
    {
        "id": "Q-PRAC-010",
        "type": "practical",
        "category": "네트워크 보안",
        "score": 16,
        "concept_id": "CON-NET-01",
        "source_id": "SRC-02",
        "source_page": 27,
        "question": "다음은 보안관제 센터에서 탐지된 DNS 서버 대상의 패킷 덤프 로그 기록이다. 로그를 분석하고 각 물음에 답하시오.\n\n[DNS 패킷 분석 로그]\nDNS standard query 0x2872 ANY cpsc.gov (출발지: 211.234.11.88:49152, 목적지: 168.126.63.1:53)\nDNS standard query 0x3914 ANY cpsc.gov (출발지: 211.234.11.88:49153, 목적지: 168.126.63.1:53)\nDNS standard query 0x712a ANY cpsc.gov (출발지: 211.234.11.88:49154, 목적지: 168.126.63.1:53)\n\n1) 수행 중인 구체적인 서비스 거부 공격의 명칭을 기술하시오. (4점)\n2) 패킷 로그에서 질의 타입(Query Type)을 'ANY'로 지정한 공격자의 기술적 의도를 설명하시오. (4점)\n3) 이 공격에서 공격자가 소스 IP(211.234.11.88)를 위조하여 발생하는 공격 증폭(Amplification) 메커니즘을 설명하시오. (4점)\n4) 공격에 악용되는 공개 DNS 리졸버의 보안 강화를 위한 named.conf 설정 방안 1가지를 기술하시오. (4점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 구체적인 서비스 거부 공격 명칭",
                "model_answer": "DNS 증폭 DRDoS 공격 (DNS Amplification DRDoS Attack)",
                "rubric": {
                    "keywords": [
                        ["dns 증폭", "dns amplification", "drdos", "dns 반사"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 질의 타입을 ANY로 지정한 기술적 의도",
                "model_answer": "ANY 타입 질의는 해당 도메인의 모든 DNS 레코드(A, MX, NS, TXT, SOA 등)를 한꺼번에 응답하도록 요구하므로, 약 50~90 바이트의 작은 질의 요청으로 수천 바이트(약 3,000 바이트 이상)의 방대한 응답을 유발하여 증폭률(약 30~50배)을 극대화하기 위함이다.",
                "rubric": {
                    "keywords": [
                        ["모든 레코드", "전체 레코드", "a, mx, txt"],
                        ["증폭", "큰 응답", "응답 크기", "수천 바이트"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) IP 위조를 통한 공격 증폭 메커니즘",
                "model_answer": "공격자가 출발지 IP를 피해 대상 서버(211.234.11.88)로 스푸핑하여 정상 오픈 DNS 서버들로 질의를 전송하면, DNS 서버들이 생성한 대규모의 증폭된 응답 패킷이 위조된 출발지 IP인 피해자 서버로 일제히 반사되어 네트워크 대역폭을 고갈시킨다.",
                "rubric": {
                    "keywords": [
                        ["출발지 ip 위조", "피해자 ip", "스푸핑"],
                        ["반사", "피해자에게 전달", "대역폭 고갈"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 4,
                "score": 4,
                "prompt": "4) DNS 서버 named.conf 보안 설정 방안",
                "model_answer": "외부 불특정 다수의 재귀 질의(Recursion)를 차단하기 위해 `recursion no;`로 설정하거나, `allow-recursion { 내부IP대역; };`을 설정하여 신뢰할 수 있는 내부 클라이언트에게만 재귀 질의를 허용한다.",
                "rubric": {
                    "keywords": [
                        ["recursion no", "allow-recursion", "재귀 질의 차단", "재귀 쿼리"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "model_answer": "1) DNS 증폭 DRDoS 공격\n2) ANY 질의로 모든 레코드를 응답받아 패킷 증폭률 극대화\n3) 출발지 IP를 피해자로 위조하여 대용량 반사 패킷이 피해자에게 집중\n4) named.conf에서 recursion no; 또는 allow-recursion 제한 설정",
        "explanation": "DNS 증폭 DRDoS는 오픈 리졸버(Open Resolver) 취약점을 이용하므로, 공용 DNS 서버에서 recursion no 설정 및 응답 속도 제한(RRL: Response Rate Limiting)을 적용해야 합니다.",
        "difficulty": "medium",
        "tags": ["DNS증폭", "DRDoS", "ANY질의", "OpenResolver", "recursion"]
    },
    {
        "id": "Q-PRAC-011",
        "type": "practical",
        "category": "애플리케이션 보안",
        "score": 16,
        "concept_id": "CON-APP-01",
        "source_id": "SRC-02",
        "source_page": 28,
        "question": "다음은 메일 수신 서버(mx.google.com)에 기록된 수신 이메일의 헤더 및 인증 분석 로그이다. 내용을 분석하고 각 물음에 답하시오.\n\n[이메일 수신 헤더 로그]\n1 Delivered-To: victim@company.com\n2 Received: by 10.36.47.149 with SMTP id j143;\n3 Return-Path: <sender.notice@partner.com>\n4 Received: from mail.partner.com (mail.partner.com. [203.248.55.10])\n5     by mx.google.com with ESMTPS id u123si\n6     (version=TLSv1.2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);\n7 Received-SPF: pass (partner.com designates 203.248.55.10 as permitted sender) client-ip=203.248.55.10;\n8 Authentication-Results: mx.google.com;\n9     dkim=pass header.i=@partner.com header.s=s2023;\n\n1) 6행의 암호 스위트(Cipher Suite) 설정에서 'RSA'가 수행하는 보안 역할(용도)을 기술하시오. (5점)\n2) 7행의 'Received-SPF: pass' 결과가 판정된 기술적 원리와 DNS 레코드 검증 메커니즘을 설명하시오. (5점)\n3) 9행의 'dkim=pass'가 메일의 위변조 방지 및 송신자 신원 보증을 수행하는 기술적 동작 원리를 설명하시오. (6점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 5,
                "prompt": "1) TLS 통신에서 RSA의 역할",
                "model_answer": "서버 인증서(공개키)의 정당성을 검증하여 메일 서버의 신원을 인증하고, 중간자 공격(MITM)을 방지하기 위한 디지털 서명 검증 역할을 수행한다.",
                "rubric": {
                    "keywords": [
                        ["서버 인증", "인증서", "신원 확인", "인증"],
                        ["중간자 공격", "mitm", "서명 검증", "전자서명"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 2,
                "score": 5,
                "prompt": "2) SPF pass 판정 원리 및 DNS 메커니즘",
                "model_answer": "수신 서버가 발신자 도메인(partner.com)의 DNS 서버에 등록된 TXT 레코드(SPF 정책)를 조회하여, 실제 메일을 발송한 클라이언트 IP(203.248.55.10)가 허용된 정당한 메일 발송 서버 목록에 포함되어 있음을 확인했기 때문이다.",
                "rubric": {
                    "keywords": [
                        ["dns", "txt 레코드", "spf"],
                        ["송신 ip", "203.248.55.10", "발송 서버 ip", "허용"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 3,
                "score": 6,
                "prompt": "3) DKIM 동작 원리",
                "model_answer": "송신 메일 서버가 메일 헤더 및 본문의 해시값을 자신의 개인키(Private Key)로 전자서명하여 메일에 첨부하고, 수신 서버는 발신 도메인 DNS TXT 레코드에 공개된 공개키(Public Key)로 서명을 복호화/검증함으로써 메일 내용이 전송 도중 위변조되지 않았음을 확인한다.",
                "rubric": {
                    "keywords": [
                        ["개인키", "전자서명", "헤더 서명", "비밀키"],
                        ["공개키", "dns", "검증", "위변조 방지"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "model_answer": "1) 서버 인증서 검증을 통한 메일 서버 신원 인증 및 중간자 공격 차단\n2) 발신 도메인 DNS TXT 레코드에 지정된 정당한 송신 서버 IP와 실제 송신 IP 일치 검증\n3) 송신자 개인키로 이메일 헤더를 전자서명하고, 도메인 DNS 공개키로 서명 검증하여 위변조 방지",
        "explanation": "이메일 스푸핑 방어는 발송 서버 IP를 검증하는 SPF와 메일 본문/헤더의 전자서명 무결성을 검증하는 DKIM, 그리고 검증 실패 시 차단 정책을 정의하는 DMARC를 복합 적용합니다.",
        "difficulty": "medium",
        "tags": ["이메일보안", "SPF", "DKIM", "TLS", "DNS_TXT"]
    },
    {
        "id": "Q-PRAC-012",
        "type": "practical",
        "category": "시스템 보안",
        "score": 16,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-02",
        "source_page": 29,
        "question": "다음은 리눅스 및 웹 서버의 4가지 주요 보안 설정 점검 항목이다. 각 물음에 답하시오.\n\n[항목 1] 패스워드 무차별 대입 공격을 방어하기 위한 PAM 계정 잠금 설정\nauth required pam_tally2.so ( A )=5 unlock_time=600\n\n[항목 2] 특정 비인가 호스트(192.168.10.50)로부터의 FTP(21번) 접속을 차단하는 IPTables 룰\niptables -A INPUT -p tcp -s 192.168.10.50 --dport 21 -j ( B )\n\n[항목 3] /etc/shadow 파일의 소유자를 root로 변경하고 소유자에게만 읽기 권한을 부여하는 명령어\n\n[항목 4] 웹서버 업로드 디렉토리(/var/www/uploads)에서 대용량 악성 웹쉘 업로드를 억제하기 위한 설정\nLimitRequestBody 5000000\n\n1) [항목 1]의 ( A )에 들어갈 PAM 모듈 설정 옵션명을 기술하시오. (4점)\n2) [항목 2]의 ( B )에 들어갈 패킷 차단 타깃(Target) 옵션을 기술하시오. (4점)\n3) [항목 3]의 보안 조치를 수행하기 위한 정확한 리눅스 명령어 2줄을 작성하시오. (4점)\n4) [항목 4]의 아파치 지시자 `LimitRequestBody 5000000`의 구체적인 동작 의미와 수치 단위를 설명하시오. (4점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) ( A )에 들어갈 PAM 옵션명",
                "model_answer": "deny (또는 onerr=fail deny)",
                "rubric": {
                    "keywords": [
                        ["deny"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) ( B )에 들어갈 차단 타깃",
                "model_answer": "DROP (또는 REJECT)",
                "rubric": {
                    "keywords": [
                        ["DROP", "REJECT"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) /etc/shadow 소유자 변경 및 권한 설정 명령어 2줄",
                "model_answer": "chown root /etc/shadow\nchmod 400 /etc/shadow (또는 chmod 000 /etc/shadow)",
                "rubric": {
                    "keywords": [
                        ["chown root /etc/shadow", "chown root:root /etc/shadow"],
                        ["chmod 400 /etc/shadow", "chmod 000 /etc/shadow", "chmod 600 /etc/shadow"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 4,
                "score": 4,
                "prompt": "4) LimitRequestBody 5000000의 동작 의미 및 단위",
                "model_answer": "클라이언트가 HTTP 요청 본문(Request Body)으로 웹서버에 업로드할 수 있는 파일의 최대 허용 크기를 5,000,000 바이트(Byte, 약 5MB)로 제한하는 설정이다.",
                "rubric": {
                    "keywords": [
                        ["바이트", "byte", "5mb"],
                        ["업로드 크기 제한", "본문 크기 제한", "최대 크기", "5000000"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "model_answer": "1) deny\n2) DROP\n3) chown root /etc/shadow\nchmod 400 /etc/shadow\n4) 클라이언트 요청 본문(업로드) 크기를 최대 5,000,000 바이트(약 5MB)로 제한",
        "explanation": "리눅스 시스템 및 웹서버 보안 점검의 표준 항목으로 계정 잠금(deny=5), 방화벽 차단(DROP), 중요 계정 파일 권한(chmod 400), 웹서버 업로드 본문 크기 통제(LimitRequestBody)를 검증합니다.",
        "difficulty": "medium",
        "tags": ["리눅스보안점검", "PAM", "iptables", "shadow", "LimitRequestBody"]
    },
    {
        "id": "Q-PRAC-013",
        "type": "practical",
        "category": "시스템 보안",
        "score": 16,
        "concept_id": "CON-SYS-01",
        "source_id": "SRC-05",
        "source_page": 10,
        "question": "다음은 리눅스 서버에서 슈퍼 데몬(xinetd) 및 TCP Wrapper를 이용하여 원격 접속 서비스를 보호하기 위한 설정 내용이다. 물음에 답하시오.\n\n[설정 1: TCP Wrapper 설정 파일]\n/etc/hosts.allow\n/etc/hosts.deny\n\n[설정 2: /etc/xinetd.d/telnet 설정]\nservice telnet\n{\n    disable = no\n    flags = REUSE\n    socket_type = stream\n    wait = no\n    user = root\n    server = /usr/sbin/in.telnetd\n    ( A ) = 192.168.1.0/24 10.0.0.5\n    ( B ) = 192.168.1.100\n    ( C ) = 50 10\n}\n\n1) TCP Wrapper에서 `/etc/hosts.allow` 파일과 `/etc/hosts.deny` 파일이 동시에 존재할 때 클라이언트 접속 요청에 대한 접근 통제 적용 우선순위 규칙을 3단계로 설명하시오. (8점)\n2) [설정 2]의 텔넷 xinetd 설정에서 ( A ), ( B ), ( C )에 들어갈 지시자의 이름을 각각 작성하고, ( C ) 지시자의 구체적인 동작 의미를 설명하시오. (8점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 8,
                "prompt": "1) TCP Wrapper의 접근 통제 적용 우선순위 3단계",
                "model_answer": "1단계: /etc/hosts.allow 파일을 검사하여 일치하는 규칙이 있으면 즉시 접속을 허용한다.\n2단계: hosts.allow에 일치하지 않으면 /etc/hosts.deny 파일을 검사하여 일치하는 규칙이 있으면 접속을 차단(거부)한다.\n3단계: 두 파일 모두에 매칭되는 규칙이 없으면 기본적으로 접속을 허용(Allow)한다.",
                "rubric": {
                    "keywords": [
                        ["hosts.allow", "먼저 검사", "허용"],
                        ["hosts.deny", "차단", "거부"],
                        ["기본 허용", "둘 다 없으면"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            },
            {
                "sub_id": 2,
                "score": 8,
                "prompt": "2) xinetd (A), (B), (C) 지시자 및 (C)의 동작 의미",
                "model_answer": "- (A): only_from (접속을 허용할 IP/대역)\n- (B): no_access (접속을 차단할 IP)\n- (C): cps (Connections Per Second)\n- (C) 동작 의미: 초당 연결 요청 수가 50개를 초과하는 경우 서비스 거부 공격 방어를 위해 해당 서비스를 10초 동안 일시적으로 비활성화(접속 중단)한다.",
                "rubric": {
                    "keywords": [
                        ["only_from"],
                        ["no_access"],
                        ["cps"],
                        ["초당 50개", "10초 동안 중지", "비활성화"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            }
        ],
        "model_answer": "1) hosts.allow 우선 허용 -> hosts.deny 차단 -> 둘 다 매칭 없으면 기본 허용\n2) (A) only_from, (B) no_access, (C) cps\n- cps 50 10: 초당 50개 이상 접속 시 10초간 서비스 일시 중단",
        "explanation": "xinetd는 슈퍼 데몬으로서 TCP Wrapper의 호스트 기반 접근제어와 자체 지시자(only_from, no_access, cps 자원 제한)를 통해 네트워크 서비스에 대한 다층 방어를 제공합니다.",
        "difficulty": "medium",
        "tags": ["xinetd", "TCP_Wrapper", "hosts.allow", "hosts.deny", "cps", "only_from"]
    },
    {
        "id": "Q-PRAC-014",
        "type": "practical",
        "category": "시스템 보안",
        "score": 16,
        "concept_id": "CON-SYS-02",
        "source_id": "SRC-05",
        "source_page": 4,
        "question": "다음은 Windows 서버의 보안 이벤트 로그(Security Event Log)를 분석한 기록이다. 각 물음에 답하시오.\n\n[이벤트 로그 A]\n- 이벤트 ID: 4625\n- 계정 이름: Administrator\n- 로그온 유형(Logon Type): 3\n- 실패 사유: 0xC000006A (잘못된 패스워드)\n- 발생 빈도: 10초 동안 동일 IP(192.168.1.200)로부터 500회 연속 발생\n\n[이벤트 로그 B]\n- 이벤트 ID: 4624\n- 계정 이름: Administrator\n- 로그온 유형(Logon Type): 2\n- 원본 네트워크 주소: 127.0.0.1\n\n1) [이벤트 로그 A]의 Event ID '4625'와 [이벤트 로그 B]의 Event ID '4624'의 의미를 각각 기술하시오. (4점)\n2) [이벤트 로그 A]의 발생 패턴(10초 동안 500회 4625)을 바탕으로 공격자가 시도한 구체적인 사이버 공격 명칭을 기술하시오. (4점)\n3) [이벤트 로그 A]의 Logon Type '3'과 [이벤트 로그 B]의 Logon Type '2'가 의미하는 로그온 방식의 차이점을 각각 설명하시오. (4점)\n4) 관리자 계정에 대한 이러한 무작위 공격을 차단하기 위해 Windows 보안 정책에서 설정해야 하는 필수 보안 정책 항목 1가지를 기술하시오. (4점)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) Event ID 4624 및 4625의 의미",
                "model_answer": "- 4624: 계정 로그온 성공 (Successful Logon)\n- 4625: 계정 로그온 실패 (Failed Logon)",
                "rubric": {
                    "keywords": [
                        ["4624", "로그온 성공", "성공"],
                        ["4625", "로그온 실패", "실패"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) 이벤트 로그 A의 공격 명칭",
                "model_answer": "패스워드 무차별 대입 공격 (Brute Force Attack) 또는 사전 공격 (Dictionary Attack)",
                "rubric": {
                    "keywords": [
                        ["무차별 대입", "brute force", "사전 대입", "패스워드 무차별"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) Logon Type 2 vs Logon Type 3 차이점",
                "model_answer": "- Logon Type 2 (Interactive): 사용자가 콘솔 키보드/모니터를 통해 컴퓨터에 직접 물리적으로 로그인한 대화형 로그온\n- Logon Type 3 (Network): 공유 폴더, IIS 웹서비스 등 네트워크를 통해 원격 컴퓨터에서 접근한 네트워크 로그온",
                "rubric": {
                    "keywords": [
                        ["type 2", "대화형", "로컬", "콘솔", "키보드"],
                        ["type 3", "네트워크", "원격", "공유 폴더"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 4,
                "score": 4,
                "prompt": "4) 무차별 대입 공격 차단을 위한 윈도우 보안 정책 항목",
                "model_answer": "계정 잠금 임계값 (Account Lockout Threshold) 설정 (예: 5회 실패 시 계정 잠금) 및 계정 잠금 기간 설정",
                "rubric": {
                    "keywords": [
                        ["계정 잠금", "계정 잠금 임계값", "임계값", "lockout threshold"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "model_answer": "1) 4624: 로그온 성공, 4625: 로그온 실패\n2) 패스워드 무차별 대입 공격 (Brute Force Attack)\n3) Type 2: 로컬 대화형 콘솔 로그온, Type 3: 네트워크 원격 로그온\n4) 계정 잠금 임계값(Account Lockout Threshold) 정책 설정",
        "explanation": "윈도우 보안 감사 로그는 Event ID 4624(성공), 4625(실패) 및 Logon Type(2:대화형, 3:네트워크, 10:원격데스크톱 RDP)을 분석하여 무차별 대입 공격을 식별합니다.",
        "difficulty": "medium",
        "tags": ["Windows로그", "4624", "4625", "LogonType", "계정잠금"]
    }
]

print(f"Batch 1 Short: {len(BATCH1_SHORT)}")
print(f"Batch 1 Descriptive: {len(BATCH1_DESC)}")
print(f"Batch 1 Practical: {len(BATCH1_PRAC)}")
print(f"Total Batch 1 New Questions: {len(BATCH1_SHORT) + len(BATCH1_DESC) + len(BATCH1_PRAC)}")
