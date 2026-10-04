# -*- coding: utf-8 -*-
"""
Chunk 5 Fixer: Q-PRAC-001 to Q-PRAC-024 (24 Practical questions)
Fixes:
- P1-2: Replaces category boilerplate in practical_scoring_criteria with authentic rubric keywords from questions.json.
  Guarantees rubric points sum to 16.
- P1-3: Replaces concept-inherited traps with question-specific, realistic traps.
"""

import json

PRAC_TRAPS = {
    "Q-PRAC-001": [
        {
            "confused_term_or_misunderstanding": "FORWARD 체인의 검사 대상을 호스트 자신으로 들어오는 패킷으로 혼동",
            "explanation": "방화벽 호스트 자체로 들어오는 인바운드 패킷은 INPUT 체인이 검사하며, FORWARD 체인은 호스트를 단순히 통과(라우팅/포워딩)하여 다른 외부/내부 네트워크로 전달되는 패킷만을 검사합니다."
        },
        {
            "confused_term_or_misunderstanding": "! --syn 옵션의 기술적 의미를 단순 SYN 패킷 차단으로 오해",
            "explanation": "'! --syn'은 TCP 연결 상태가 신규(state NEW)임에도 불구하고 SYN 플래그가 켜져 있지 않은(예: SYN 없이 ACK/FIN만 켜진) 비정상적인 스캔 및 위조 패킷을 정밀 필터링하기 위한 조건입니다."
        }
    ],
    "Q-PRAC-002": [
        {
            "confused_term_or_misunderstanding": "Snort 룰 헤더에서 양방향 트래픽 연산자를 '<-'로 작성",
            "explanation": "Snort 룰 문법에서 허용되는 방향 지시자는 단방향 '->'과 양방향 '<>'뿐이며, 역방향 '<-' 연산자는 유효하지 않은 문법 오류입니다."
        },
        {
            "confused_term_or_misunderstanding": "룰 옵션 작성 시 세미콜론(;) 구분자 누락",
            "explanation": "Snort 룰 바디의 각 옵션(msg, content, sid 등)은 반드시 콜론(:)으로 인자를 구분하고 끝에 세미콜론(;)을 명시해야 정상 로드됩니다."
        }
    ],
    "Q-PRAC-003": [
        {
            "confused_term_or_misunderstanding": "umask 027 적용 시 생성되는 파일의 기본 권한을 750으로 잘못 계산",
            "explanation": "리눅스에서 일반 파일의 최대 생성 기본값은 666이므로 umask 027을 적용하면 '666 - 027 = 640(-rw-r-----)'이 되며, 디렉터리(777 기준 750)와 계산 기준이 다릅니다."
        },
        {
            "confused_term_or_misunderstanding": "operator 계정 전용 파일에 타인(Other) 실행 권한(chmod 705/755)을 남겨두는 실수",
            "explanation": "백업 스크립트 내부의 중요 시스템 파일 접근 권한을 보호하기 위해 소유자를 operator로 변경(chown operator)하고 타인 권한을 전면 차단하는 700(rwx------)으로 설정해야 합니다."
        }
    ],
    "Q-PRAC-004": [
        {
            "confused_term_or_misunderstanding": "Slave 서버 설정에서 원본 동기화 대상을 allow-transfer로 작성",
            "explanation": "Slave 서버가 원본 데이터를 복제해 올 Master 서버의 IP 주소를 지정하는 BIND 설정 지시자는 'masters { 192.168.1.53; };'이며, 영역 전송 허용 호스트를 제한하는 'allow-transfer'와 구분해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "BIND named.conf 설정 시 중괄호 뒤 세미콜론(;) 누락",
            "explanation": "BIND 설정 파일의 지시자 구문은 IP 목록 블록 내부와 끝부분 모두에 세미콜론(예: { 192.168.2.53; };)을 작성해야 문법 오류가 발생하지 않습니다."
        }
    ],
    "Q-PRAC-005": [
        {
            "confused_term_or_misunderstanding": "find 명령어에서 SetUID/SetGID 검색 옵션을 '-perm 4000'으로만 작성",
            "explanation": "정확히 4000 권한만을 찾는 '-perm 4000' 대신, 다른 퍼미션(rwx)이 포함되어도 SetUID(4000) 또는 SetGID(2000) 비트가 켜진 모든 파일을 포괄 검색하기 위해 '-perm -4000 -o -perm -2000' 형태로 하이픈(-)을 붙여야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "SetUID 권한 제거 명령어를 chmod -u 로 잘못 표기",
            "explanation": "특수 권한인 SetUID/SetGID 비트를 기호 모드로 제거하는 올바른 명령어는 'chmod -s <파일명>' 또는 'chmod u-s <파일명>'입니다."
        }
    ],
    "Q-PRAC-006": [
        {
            "confused_term_or_misunderstanding": "Snort offset과 depth 옵션의 시작 기준 혼동",
            "explanation": "offset은 페이로드 시작점으로부터 검사를 건너뛸 바이트 수(오프셋 0: 맨 처음부터)이고, depth는 offset 지점부터 검사할 총 바이트 범위(depth 13: 13바이트 내 검색)를 의미합니다."
        },
        {
            "confused_term_or_misunderstanding": "reject 액션 설정 시 TCP 세션 종료 프로토콜을 ICMP로만 한정 작성",
            "explanation": "Snort에서 TCP 패킷에 대해 reject 액션이 실행되면 클라이언트에게 TCP RST(재설정) 패킷을 전송하여 세션을 즉시 강제 종료하며, UDP 패킷인 경우 ICMP Port Unreachable 메시지를 반환합니다."
        }
    ],
    "Q-PRAC-007": [
        {
            "confused_term_or_misunderstanding": "TCP 플래그 'AP'를 ACK 패킷과 PUSH 패킷이 별도로 2개 전송된 것으로 오해",
            "explanation": "'AP'는 단일 TCP 패킷 헤더 내의 ACK(수신 확인) 비트와 PSH(버퍼링 없이 상위 애플리케이션으로 즉시 전달) 비트가 동시에 1로 설정되어 결합된 상태를 의미합니다."
        },
        {
            "confused_term_or_misunderstanding": "익명 FTP의 위험성을 단순 트래픽 증가로만 서술",
            "explanation": "익명(anonymous) 로그인이 쓰기 권한까지 허용될 경우 외부 공격자가 웹쉘이나 불법 악성코드를 업로드하고 저장소(Warez)로 악용하거나 내부 기밀 파일을 무단 다운로드할 수 있는 중대한 위험이 발생합니다."
        }
    ],
    "Q-PRAC-008": [
        {
            "confused_term_or_misunderstanding": "dig axfr 질의의 위험성을 단순 도메인 IP 노출로 축소 해석",
            "explanation": "일반적인 단일 레코드 질의와 달리 AXFR(Zone Transfer)은 해당 도메인에 등록된 모든 호스트명, 서브도메인, 메일서버, 내부 IP 주소 등 기업 전체 네트워크 자산 맵을 한 번에 공격자에게 유출시키는 치명적인 정찰 취약점입니다."
        },
        {
            "confused_term_or_misunderstanding": "영역 전송 차단 설정을 zone 블록이 아닌 options 전역에만 설정하면 충분하다고 생각",
            "explanation": "보안 강화를 위해 options 블록뿐만 아니라 특정 민감 도메인의 개별 zone 블록에도 'allow-transfer { none; };' 또는 공인된 보조 네임서버 IP만을 명시하여 철저히 통제해야 합니다."
        }
    ],
    "Q-PRAC-009": [
        {
            "confused_term_or_misunderstanding": "AddType text/html 설정 시 웹쉘이 서버에서 여전히 실행된다고 오해",
            "explanation": "PHP 확장자의 MIME 타입을 text/html로 재정의하면 아파치 웹 서버가 PHP 해석 엔진(PHP-FPM/mod_php)으로 스크립트를 전달하지 않고 일반 텍스트 문서로 브라우저에 그대로 출력하므로 서버 측 코드 실행이 원천 무력화됩니다."
        },
        {
            "confused_term_or_misunderstanding": "FilesMatch 지시자의 정규식 문법에서 대소문자 구분 및 파이프(|) 기호 누락",
            "explanation": "다양한 실행 확장자(php, php3, phtml 등)를 모두 차단하기 위해 정규식 패턴 '\\.(php|php3|phtml)$' 형태로 정확히 그룹화하여 작성해야 우회를 차단할 수 있습니다."
        }
    ],
    "Q-PRAC-010": [
        {
            "confused_term_or_misunderstanding": "공격자가 DNS ANY 질의를 사용하는 이유를 단순 응답 속도 향상으로 오해",
            "explanation": "ANY 질의는 도메인에 존재하는 A, MX, NS, TXT, SOA 등 모든 리소스 레코드를 일괄 응답하도록 요구하여, 수십 바이트의 작은 질의 요청으로 수천 바이트의 거대 응답을 유발하는 증폭률(Amplification Factor) 극대화가 목적입니다."
        },
        {
            "confused_term_or_misunderstanding": "공격 증폭 트래픽이 DNS 서버 자신에게 집중된다고 오해",
            "explanation": "공격자가 질의 패킷의 출발지 IP를 피해자(Victim) 서버 IP로 스푸핑하여 전송하므로, 대용량 반사 패킷은 질의를 수신한 DNS 서버가 아니라 위조된 피해자 서버로 집중되어 대역폭을 고갈시킵니다."
        }
    ],
    "Q-PRAC-011": [
        {
            "confused_term_or_misunderstanding": "SPF(Sender Policy Framework) 검증을 수신자 메일함 암호 검증으로 오해",
            "explanation": "SPF는 메일 수신 서버가 발신 도메인의 DNS TXT 레코드에 등록된 정당한 메일 발송 서버 IP 대역과 실제 SMTP 연결을 시도한 송신 서버 IP가 일치하는지 대조하여 발신 도메인 위조를 방어하는 기법입니다."
        },
        {
            "confused_term_or_misunderstanding": "DKIM 전자서명 검증 시 발신자의 개인키를 DNS에서 조회한다고 오해",
            "explanation": "발신 서버는 자신의 '개인키(비밀키)'로 메일 헤더를 서명하고, 수신 서버는 발신 도메인의 DNS TXT 레코드에 공개된 '공개키'를 조회하여 서명 무결성을 검증합니다."
        }
    ],
    "Q-PRAC-012": [
        {
            "confused_term_or_misunderstanding": "/etc/shadow 파일의 권한을 644(rw-r--r--)로 완화 설정하는 실수",
            "explanation": "/etc/shadow 파일은 일반 사용자가 열람할 경우 암호화된 해시를 복사하여 오프라인 크랙을 시도할 수 있으므로, 반드시 소유자를 root로 하고 권한을 400(r--------) 또는 000으로 극소화해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "LimitRequestBody 설정 단위(바이트)를 메가바이트(MB) 단위로 오해",
            "explanation": "아파치 LimitRequestBody 지시자의 설정값은 바이트 단위이므로, 약 5MB 제한을 위해서는 '5000000'(또는 5242880)과 같이 바이트 정수형으로 정확히 기재해야 합니다."
        }
    ],
    "Q-PRAC-013": [
        {
            "confused_term_or_misunderstanding": "TCP Wrapper에서 hosts.deny가 hosts.allow보다 우선 적용된다고 혼동",
            "explanation": "TCP Wrapper 적용 우선순위는 1단계: hosts.allow에 매칭되면 즉시 접속 허용, 2단계: hosts.deny에 매칭되면 접속 차단, 3단계: 두 파일 모두 매칭되지 않으면 기본 허용(Allow) 순으로 처리됩니다."
        },
        {
            "confused_term_or_misunderstanding": "xinetd cps 설정값의 앞뒤 숫자 단위 혼동",
            "explanation": "'cps 50 10'에서 첫 번째 인자(50)는 초당 허용할 최대 연결 요청 수이고, 두 번째 인자(10)는 해당 한도를 초과했을 때 서비스를 일시 중단(대기)시킬 초(sec) 단위 시간입니다."
        }
    ],
    "Q-PRAC-014": [
        {
            "confused_term_or_misunderstanding": "Event ID 4624와 4625의 성공/실패 의미 반대 작성",
            "explanation": "Windows 보안 감사 로그에서 Event ID 4624는 '계정 로그온 성공(An account was successfully logged on)'이며, 4625는 '계정 로그온 실패(An account failed to log on)' 이벤트입니다."
        },
        {
            "confused_term_or_misunderstanding": "Logon Type 3을 콘솔 키보드 대화형 로그인으로 혼동",
            "explanation": "Logon Type 2는 컴퓨터 콘솔 키보드에 직접 앉아서 로그인하는 대화형(Interactive) 로그온이며, Logon Type 3은 네트워크를 통해 공유 폴더나 원격 서비스에 접근한 네트워크(Network) 로그온입니다."
        }
    ],
    "Q-PRAC-015": [
        {
            "confused_term_or_misunderstanding": "tcpdump의 IP ID(95)를 프로세스 PID나 포트 번호로 오해",
            "explanation": "IP 헤더의 식별자(ID) 필드는 송신 호스트가 분할된 단편들이 원래 동일한 하나의 IP 데이터그램에 속해 있음을 수신 측에서 재조합할 수 있도록 부여한 고유 번호입니다."
        },
        {
            "confused_term_or_misunderstanding": "'+' 기호를 패킷 전송 성공 플래그로 오해",
            "explanation": "tcpdump 단편화 출력에서 '+' 기호는 IP 헤더의 플래그 중 MF(More Fragments) 플래그가 1로 설정되어 있어 뒤에 추가 단편 패킷이 더 존재함을 의미하며, 마지막 단편에서는 '+' 기호가 표시되지 않습니다."
        }
    ],
    "Q-PRAC-016": [
        {
            "confused_term_or_misunderstanding": "Heartbleed 탐지 룰에서 depth 옵션을 페이로드 건너뛰기 오프셋으로 혼동",
            "explanation": "특정 바이트를 건너뛰는 옵션은 offset/distance이며, depth는 페이로드 시작점(0)부터 패턴 검사를 제한할 검색 깊이 바이트 수를 의미합니다."
        },
        {
            "confused_term_or_misunderstanding": "within 옵션과 distance 옵션의 차이 혼동",
            "explanation": "distance는 직전 content 매칭 성공 위치로부터 몇 바이트 건너뛸 것인가(상대적 오프셋)이며, within은 그 위치부터 몇 바이트 범위 내에서 다음 패턴을 검사할 것인가(상대적 깊이)를 지정합니다."
        }
    ],
    "Q-PRAC-017": [
        {
            "confused_term_or_misunderstanding": "Slow HTTP POST 공격을 단순 SYN 플러딩 공격으로 혼동",
            "explanation": "SYN Flood는 L4 계층 연결을 방해하지만, Slow HTTP POST(RUDY)는 정상 3-Way Handshake 완료 후 대용량 Content-Length를 선언하고 본문 데이터를 장시간 지연 전송하여 웹 애플리케이션 연결 슬롯을 고갈시킵니다."
        },
        {
            "confused_term_or_misunderstanding": "웹 서버 차원의 방어 모듈로 mod_rewrite만을 제시하는 오류",
            "explanation": "저전송 DoS 방어의 핵심은 HTTP 요청 헤더 및 본문의 최소 수신 전송률을 강제하는 'mod_reqtimeout(RequestReadTimeout)' 모듈 설정과 클라이언트 타임아웃(Timeout) 값의 합리적 축소입니다."
        }
    ],
    "Q-PRAC-018": [
        {
            "confused_term_or_misunderstanding": "보안 대책 순이익 계산 시 SLE 감소액 대신 ALE를 직접 차감하는 계산 오류",
            "explanation": "보안 대책의 연간 순이익(CBA)은 '대책 적용 전 ALE - 대책 적용 후 ALE - 연간 대책 비용'으로 산출되며, 감소된 연간 손실액에서 대책 비용을 차감해야 합니다."
        },
        {
            "confused_term_or_misunderstanding": "단일예상손실액(SLE) 산정 시 연간발생률(ARO)을 곱하는 실수",
            "explanation": "SLE는 1회 사고 시의 손실액이므로 '자산가치(AV) * 노출계수(EF)'로 계산하며, 여기에 ARO를 곱한 결과는 연간예상손실액(ALE)입니다."
        }
    ],
    "Q-PRAC-019": [
        {
            "confused_term_or_misunderstanding": "만 14세 미만 아동의 법정대리인 동의 기준 연령을 만 19세나 만 12세로 혼동",
            "explanation": "개인정보보호법 제22조의2에 따라 아동의 개인정보 처리를 위해 법정대리인의 동의를 받아야 하는 법정 연령 기준은 '만 14세 미만'입니다."
        },
        {
            "confused_term_or_misunderstanding": "선택항목 미동의 시 부가 서비스 거부가 정당하다고 오해",
            "explanation": "개인정보보호법 제16조 제3항에 따라 정보주체가 선택항목에 동의하지 않는다는 이유로 기본 서비스(헬스장 이용 등)의 제공을 거부하거나 불이익을 주는 행위는 명백한 법률 위반입니다."
        }
    ],
    "Q-PRAC-020": [
        {
            "confused_term_or_misunderstanding": "SQL Injection 주석 기호(--)의 역할을 단순 문자열 검색 조건으로 오해",
            "explanation": "공격 쿼리 끝에 삽입된 '--'(또는 /* */)는 SQL 인터프리터에서 이후의 모든 조건(예: AND password='...')을 주석으로 처리하여 무력화함으로써 패스워드 검증 없이 최고관리자(admin) 계정으로 로그인을 성공시킵니다."
        },
        {
            "confused_term_or_misunderstanding": "시큐어 코딩 대응 방안으로 단순 프론트엔드 유효성 검사만을 작성",
            "explanation": "클라이언트 자바스크립트 검증은 프록시로 쉽게 우회되므로, 반드시 서버 소스코드 레벨에서 파라미터화된 쿼리(Prepared Statement)를 적용하고 특수문자 화이트리스트 검증을 수행해야 합니다."
        }
    ],
    "Q-PRAC-021": [
        {
            "confused_term_or_misunderstanding": "rpm -V 플래그 'S'와 '5'의 기술적 의미 혼동",
            "explanation": "rpm -V 검증 출력에서 'S'는 파일의 크기(File Size)가 패키지 원본과 다르게 변경되었음을 나타내고, '5'는 MD5 체크섬 해시값이 변경되어 파일 내용이 악의적으로 변조되었음을 의미합니다."
        },
        {
            "confused_term_or_misunderstanding": "immutable(i) 속성 파일을 일반 rm -f 명령어로 삭제 가능하다고 오해",
            "explanation": "chattr +i(불변 속성)가 설정된 파일은 root 관리자라 하더라도 삭제나 덮어쓰기가 거부되므로, 반드시 'chattr -i' 명령으로 불변 속성을 먼저 해제한 후에야 재설치나 삭제가 가능합니다."
        }
    ],
    "Q-PRAC-022": [
        {
            "confused_term_or_misunderstanding": "logrotate의 postrotate 스크립트가 누락되어도 로그 기록에 영향이 없다고 오해",
            "explanation": "아파치 등 웹 서버 프로세스는 파일의 inode를 열고 있으므로, 파일 이동(순환) 후 웹 데몬에게 HUP 시그널(systemctl reload httpd)을 주지 않으면 이전 파일 디스크립터에 로그를 계속 쓰게 되어 새로 생성된 로그 파일에 로그가 기록되지 않는 장애가 발생합니다."
        },
        {
            "confused_term_or_misunderstanding": "logrotate dry-run 테스트 옵션을 -f로 혼동",
            "explanation": "'-f'는 순환 주기가 도래하지 않았더라도 강제로 로그 순환을 실행(force)하는 옵션이며, 실제 순환하지 않고 설정 구문의 이상 유무만 시뮬레이션 테스트하는 옵션은 '-d'(--debug)입니다."
        }
    ],
    "Q-PRAC-023": [
        {
            "confused_term_or_misunderstanding": "스머프 공격의 희생자 서버를 ICMP 패킷의 목적지 IP로 착각",
            "explanation": "스머프 공격에서 공격자는 패킷의 목적지 IP를 내부 네트워크의 서브넷 브로드캐스트 주소로 지정하고, 출발지 IP(Source IP)를 피해자 서버로 위조(Spoofing)하여 모든 호스트의 응답(Reply)이 피해자에게 집중되도록 합니다."
        },
        {
            "confused_term_or_misunderstanding": "directed-broadcast 차단 설정을 라우터 전역 설정 모드에 적용하는 실수",
            "explanation": "'no ip directed-broadcast' 명령어는 라우터 글로벌 모드가 아니라, 서브넷 트래픽이 유입/출입하는 개별 네트워크 인터페이스(예: FastEthernet0/0) 설정 모드에 직접 진입하여 적용해야 합니다."
        }
    ],
    "Q-PRAC-024": [
        {
            "confused_term_or_misunderstanding": "DNS 증폭 반사 공격의 수신 서비스 포트를 80번 웹 포트로 혼동",
            "explanation": "DNS 질의 및 응답 서비스는 전송 계층 프로토콜 UDP와 전용 서비스 포트 53번을 기반으로 동작합니다."
        },
        {
            "confused_term_or_misunderstanding": "라우터 ACL에서 증폭 트래픽 차단 시 프로토콜을 TCP로만 지정",
            "explanation": "DNS 반사 증폭 DRDoS 공격은 출발지 IP 스푸핑이 용이하고 3-Way Handshake가 불필요한 비연결형 UDP 프로토콜을 집중 악용하므로, ACL 필터링 시 'udp' 프로토콜과 53번 포트를 정확히 지정해야 합니다."
        }
    ]
}

def build_rubric_for_practical(q):
    sub_qs = q.get("sub_questions") or []
    rubrics = []
    max_score = q.get("score", 16)

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
            if len(g) >= 2:
                required_kws.append(f"{g[0]} / {g[1]}")
            else:
                required_kws.append(str(g[0]))

        criteria_text = f"소문항 {sub_id}번 ({sub_score}점): {sub_prompt}"
        if model_ans:
            criteria_text += f" (기준: {model_ans[:70]}...)"

        rubrics.append({
            "points": sub_score,
            "required_keywords": required_kws,
            "criteria": criteria_text
        })

    return {
        "max_score": max_score,
        "rubrics": rubrics
    }

def apply_chunk5(explanations, questions_map):
    applied_count = 0
    rubric_fixed_count = 0
    traps_fixed_count = 0

    for i in range(1, 25):
        qid = f"Q-PRAC-{i:03d}"
        if qid not in explanations or qid not in questions_map:
            continue
        exp = explanations[qid]
        q = questions_map[qid]

        # 1. P1-2 Fix: Build authentic rubrics directly from questions.json
        exp["practical_scoring_criteria"] = build_rubric_for_practical(q)
        rubric_fixed_count += 1

        # 2. P1-3 Fix: Set precise, context-specific traps
        if qid in PRAC_TRAPS:
            exp["why_wrong_common_traps"] = PRAC_TRAPS[qid]
            traps_fixed_count += 1

        applied_count += 1

    print(f"Chunk 5 applied: {applied_count} practical questions updated.")
    print(f"  - P1-2 rubrics synchronized: {rubric_fixed_count}")
    print(f"  - P1-3 traps updated: {traps_fixed_count}")

if __name__ == "__main__":
    with open("app/data/explanations.json", "r", encoding="utf-8") as f:
        exps = json.load(f)
    with open("app/data/questions.json", "r", encoding="utf-8") as f:
        qs = {q["id"]: q for q in json.load(f)}

    apply_chunk5(exps, qs)

    with open("app/data/explanations.json", "w", encoding="utf-8") as f:
        json.dump(exps, f, indent=2, ensure_ascii=False)
    print("Chunk 5 changes saved successfully to explanations.json")
