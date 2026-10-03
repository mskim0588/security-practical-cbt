# -*- coding: utf-8 -*-
"""
Batch 3 - Chunk 4: SRC-07 Network Security (10 questions)
Q-SHORT-107 ~ Q-SHORT-112 (6 short)
Q-DESC-043 ~ Q-DESC-044 (2 desc)
Q-PRAC-023 ~ Q-PRAC-024 (2 prac)
"""

CHUNK_4_QUESTIONS = [
    {
        "id": "Q-SHORT-107",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "다양한 이기종 보안 솔루션과 관제 시스템을 단일 인터페이스로 통합 연계하여 오케스트레이션하고, 사전 정의된 플레이북(Playbook)에 따라 반복적인 보안 침해 대응 작업을 자동화함으로써 보안팀의 대응 속도와 효율성을 극대화하는 지능형 보안 플랫폼의 영문 약어를 쓰시오.",
        "answer": "SOAR",
        "accepted_answers": ["SOAR", "Security Orchestration, Automation and Response", "보안 오케스트레이션"],
        "grading_mode": "normalized",
        "explanation": "SOAR는 보안 도구를 통합 및 조정하고 반복적인 작업을 자동화하여 위협에 더 빠르고 효율적으로 대응하도록 지원하는 플랫폼입니다 (SRC-07 p.368, p.382 25회 기출).",
        "source_id": "SRC-07",
        "source_page": 368,
        "concept_id": "CON-NET-04",
        "difficulty": "medium",
        "tags": ["SOAR", "보안관제", "자동화", "플레이북", "네트워크보안솔루션"]
    },
    {
        "id": "Q-SHORT-108",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "IP 패킷이 전송될 때 단편화(Fragmentation) 과정에서 발생하는 취약점을 악용한 서비스 거부(DoS) 공격으로서, 패킷의 단편 오프셋(Fragment Offset) 값을 서로 중첩되도록 조작하여 전송함으로써 이를 수신한 대상 시스템이 패킷 재조합 시 커널 오류나 시스템 다운을 일으키도록 유도하는 공격의 명칭을 영문 또는 국문으로 쓰시오.",
        "answer": "티어드롭",
        "accepted_answers": ["티어드롭", "티어드롭 공격", "Teardrop", "Teardrop Attack", "티어 드롭"],
        "grading_mode": "normalized",
        "explanation": "티어드롭(Teardrop) 공격은 IP 패킷 재조합 과정에서 Fragment 오프셋 값을 서로 중첩되도록 조작하여 수신 시스템 오류를 유발하는 DoS 공격입니다 (SRC-07 p.150).",
        "source_id": "SRC-07",
        "source_page": 150,
        "concept_id": "CON-NET-02",
        "difficulty": "medium",
        "tags": ["티어드롭", "Teardrop", "DoS", "단편화", "오프셋중첩"]
    },
    {
        "id": "Q-SHORT-109",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "네트워크 서비스 거부(DoS) 공격 기법 중, 공격자가 전송하는 TCP SYN 패킷의 출발지 IP 주소와 목적지 IP 주소를 피해자 서버의 IP 주소와 동일하게 변조하여 전송함으로써, 패킷을 수신한 피해 서버가 자기 자신에게 SYN/ACK 응답을 전송하여 무한 루프에 빠지고 시스템 자원을 고갈시키는 공격의 명칭을 영문 또는 국문으로 쓰시오.",
        "answer": "랜드 어택",
        "accepted_answers": ["랜드 어택", "랜드어택", "Land Attack", "LAND", "랜드 공격"],
        "grading_mode": "normalized",
        "explanation": "랜드 어택(Land Attack)은 출발지 IP와 목적지 IP를 피해자 주소로 동일하게 만들어 전송함으로써 수신자가 자기 자신에게 응답하게 만들어 자원을 고갈시키는 DoS 공격입니다 (SRC-07 p.144).",
        "source_id": "SRC-07",
        "source_page": 144,
        "concept_id": "CON-NET-02",
        "difficulty": "easy",
        "tags": ["랜드어택", "LandAttack", "DoS", "IP변조", "네트워크공격"]
    },
    {
        "id": "Q-SHORT-110",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "시스코(Cisco) 라우터에서 외부에서 특정 서브넷으로 유입된 유니캐스트 패킷이 로컬 링크-레이어 브로드캐스트로 전환되는 것을 차단하여, 스머프(Smurf) 증폭 반사 서비스 거부 공격의 매개체로 악용되는 것을 방지하기 위해 인터페이스 설정 모드에서 입력하는 명령어 구문을 쓰시오.",
        "answer": "no ip directed-broadcast",
        "accepted_answers": [
            "no ip directed-broadcast",
            "Directed-broadcast",
            "IP Directed-Broadcast",
            "directed-broadcast"
        ],
        "grading_mode": "strict",
        "explanation": "no ip directed-broadcast 명령은 유니캐스트 IP 패킷이 서브넷 브로드캐스트로 전환되는 것을 차단하여 Smurf 공격 등을 방지합니다 (SRC-07 p.441, p.449 20회 기출).",
        "source_id": "SRC-07",
        "source_page": 441,
        "concept_id": "CON-NET-04",
        "difficulty": "medium",
        "tags": ["directed-broadcast", "Smurf", "라우터보안", "브로드캐스트차단", "시스코"]
    },
    {
        "id": "Q-SHORT-111",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "가상 근거리 통신망(VLAN)을 구성하는 방식 중 네트워크 관리자가 스위치의 물리적 포트 번호에 특정 VLAN ID를 수동으로 일대일 매핑하여 논리적인 브로드캐스트 도메인을 분리하는 방식으로, 구성이 단순하고 가장 널리 사용되는 정적 VLAN 구성 방식의 명칭을 쓰시오.",
        "answer": "포트 기반 VLAN",
        "accepted_answers": [
            "포트 기반 VLAN",
            "포트기반 VLAN",
            "포트 기반 vlan",
            "Port-based VLAN",
            "Port based VLAN",
            "정적 VLAN",
            "포트"
        ],
        "grading_mode": "normalized",
        "explanation": "포트 기반 VLAN(Port-based VLAN; 정적 VLAN)은 관리자가 스위치의 각 물리적 포트에 VLAN 번호를 직접 설정하는 가장 보편적인 방식입니다 (SRC-07 p.135 27회 기출, p.447 28회 기출).",
        "source_id": "SRC-07",
        "source_page": 135,
        "concept_id": "CON-NET-01",
        "difficulty": "easy",
        "tags": ["VLAN", "포트기반VLAN", "Port-based", "스위치", "네트워크분할"]
    },
    {
        "id": "Q-SHORT-112",
        "type": "short",
        "category": "네트워크 보안",
        "score": 3,
        "question": "시스코(Cisco) 스위치 장비의 관리자 모드(특권 EXEC 모드)에서 스위치에 현재 생성된 VLAN 목록, VLAN 번호 및 이름, 동작 상태(Status), 각 VLAN에 할당된 스위치 포트 목록 정보를 종합적으로 조회·확인하기 위해 입력하는 기본 명령어 구문을 쓰시오.",
        "answer": "show vlan",
        "accepted_answers": ["show vlan", "show vlan brief", "sh vlan"],
        "grading_mode": "strict",
        "explanation": "show vlan 명령어는 Cisco 스위치에서 구성된 VLAN 정보와 포트 할당 상태를 조회하는 명령어입니다 (SRC-07 p.409, p.447 28회 기출).",
        "source_id": "SRC-07",
        "source_page": 409,
        "concept_id": "CON-NET-01",
        "difficulty": "easy",
        "tags": ["showvlan", "Cisco", "VLAN조회", "스위치명령어", "네트워크관리"]
    },
    {
        "id": "Q-DESC-043",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "question": "네트워크 보안 솔루션을 구축할 때 침입탐지시스템(IDS)과 침입차단시스템(IPS)의 배치 모드 및 장애 대응 방식에 대하여 다음 물음에 답하시오.\n\n1) IDS를 네트워크에 구축할 때 SPAN(포트 미러링) 또는 TAP 장비를 이용한 '미러링 모드(Mirroring Mode)'로 구축하는 기술적 원리와 이점을 서술하시오. (4점)\n2) IPS를 네트워크에 구축할 때 실제 트래픽 경로상에 직렬로 배치하는 '인라인 모드(In-line Mode)'로 구축하는 이유와 동작 메커니즘을 서술하시오. (4점)\n3) 인라인 모드로 동작하는 IPS 장비 자체에 하드웨어 결함이나 전원 장애(Crash)가 발생할 경우 네트워크 전체 통신이 단절되는 것을 방지하기 위해 적용되는 하드웨어 기능의 명칭과 동작 원리를 서술하시오. (4점)",
        "model_answer": "1) IDS 미러링 모드 원리 및 이점: 스위치의 특정 포트나 네트워크 회선에 흐르는 패킷을 SPAN(Port Mirroring) 또는 광/전기적 TAP 장비를 통해 복사(Mirroring)하여 IDS로 전달하는 방식이다. 실제 서비스 통신 패킷 흐름에 전혀 영향을 주지 않으므로 네트워크 전송 지연(Latency)이 발생하지 않으며, IDS 장비 장애 시에도 기존 네트워크 서비스 통신에 아무런 장애를 유발하지 않는 무중단 안정성의 이점이 있다.\n2) IPS 인라인 모드 원리 및 이유: 인라인 모드는 IPS 장비가 방화벽과 스위치 사이의 실제 데이터 전송 통로 상에 직렬로 위치하여, 모든 유출입 패킷이 반드시 IPS를 통과하도록 구성하는 방식이다. 패킷을 실시간으로 전수 검사하여 악의적인 침입이나 취약점 공격 패턴이 탐지되는 즉시 해당 세션을 차단(Drop)하거나 리셋(RST) 패킷을 보내 공격을 즉각 방어할 수 있다.\n3) 하드웨어 장애 대응 기능(Fail-Open / Bypass): 바이패스(Bypass) 또는 페일 오픈(Fail-Open) 기능이다. IPS 장비에 전원 차단, 하드웨어 고장, 소프트웨어 커널 패닉 등이 발생할 경우, 내장된 물리적 릴레이 스위치가 기계적으로 바이패스 회선으로 자동 전환되어 패킷 검사 없이 입력 포트와 출력 포트를 직결 연결함으로써 네트워크 트래픽 단절 없이 지속적인 통신을 보장한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) IDS 미러링 모드의 기술적 원리 및 장점",
                "model_answer": "패킷을 복사하여 전달하므로 네트워크 전송 지연이 없고 장비 장애 시에도 서비스에 영향을 주지 않는다.",
                "rubric": {
                    "keywords": [
                        ["복사", "미러링", "tap", "span"],
                        ["지연 없음", "영향 없음", "무중단", "안정성"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) IPS 인라인 모드의 구축 이유 및 실시간 차단 동작 메커니즘",
                "model_answer": "트래픽 경로 상에 직렬 배치되어 모든 패킷을 통과시키며 악성 패킷 탐지 즉시 실시간 차단(Drop)한다.",
                "rubric": {
                    "keywords": [
                        ["직렬", "경로 상", "인라인"],
                        ["실시간 차단", "drop", "차단", "즉각"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) IPS 장애 시 통신 유지를 위한 하드웨어 기능 명칭 및 원리",
                "model_answer": "Bypass(Fail-Open) 기능으로, 장비 장애 시 물리적 릴레이를 통해 입력과 출력을 직결하여 통신을 유지한다.",
                "rubric": {
                    "keywords": [
                        ["bypass", "바이패스", "fail-open", "페일 오픈"],
                        ["직결", "릴레이", "단절 방지", "통신 유지", "무중단"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "IDS는 서비스 영향 없는 미러링 모드를, IPS는 실시간 차단을 위한 인라인 모드를 사용하며, 장애 시 바이패스(Fail-Open)로 가용성을 유지합니다 (SRC-07 p.383, 13회 기출).",
        "source_id": "SRC-07",
        "source_page": 383,
        "concept_id": "CON-NET-04",
        "difficulty": "medium",
        "tags": ["IDS", "IPS", "미러링", "인라인", "Bypass", "Fail-Open", "보안장비배치"]
    },
    {
        "id": "Q-DESC-044",
        "type": "descriptive",
        "category": "네트워크 보안",
        "score": 12,
        "question": "IP 패킷의 단편화(Fragmentation) 처리 메커니즘을 악용한 대표적인 서비스 거부(DoS) 공격 기법과 방어 대책에 대하여 다음 물음에 답하시오.\n\n1) 티어드롭(Teardrop) 공격이 단편화 패킷의 오프셋(Fragment Offset) 값을 조작하여 수신 시스템의 장애를 유발하는 구체적인 원리를 서술하시오. (4점)\n2) 초소형 단편화(Tiny Fragment) 공격의 개념과, 이 공격이 패킷 필터링 방화벽의 접근 제어 정책을 우회하는 원리를 서술하시오. (4점)\n3) 단편화 기반 DoS 및 우회 공격에 대응하기 위한 운영체제 및 네트워크 방화벽 차원의 방어 대책 2가지를 서술하시오. (4점)",
        "model_answer": "1) 티어드롭 공격 원리: 송신 측에서 대용량 IP 패킷을 단편화할 때 각 단편의 시작 지점(Fragment Offset)과 데이터 길이를 고의로 왜곡하여, 다음 단편의 시작 위치가 이전 단편의 끝 위치보다 앞서게(오프셋 중첩) 조작하여 전송한다. 이를 수신한 대상 시스템이 재조합하는 과정에서 메모리 복사 버퍼 크기 계산에 음수나 언더플로우가 발생하여 운영체제가 충돌(Crash)하거나 재부팅된다.\n2) Tiny Fragment 우회 원리: 최초의 단편(Fragment 0)을 최소 크기로 잘게 쪼개어 TCP 헤더의 출발지/목적지 포트 번호 정보가 첫 번째 단편에 포함되지 못하고 두 번째 단편으로 넘어가도록 조작한다. 포트 번호 기반으로 패킷을 필터링하는 방화벽은 첫 번째 단편에서 포트 정보를 확인할 수 없어 필터링 규칙을 적용하지 못하고 패킷을 통과시키게 되며, 내부 호스트에서 재조합되어 비인가 접속이 허용된다.\n3) 방어 대책:\n- 방화벽에서 단편화된 패킷에 대해 첫 번째 단편이 최소 TCP 헤더 크기(20바이트) 이상을 포함하지 않는 비정상 초소형 단편 패킷을 즉시 차단\n- 방화벽이 단편화된 패킷을 통과시키기 전에 상태 추적 메모리에서 모든 단편을 임시 저장 및 오프셋 중첩 여부를 검증한 후 정상 조립된 패킷만을 내부로 포워딩\n- 운영체제의 최신 보안 패치를 적용하여 비정상 오프셋 패킷 수신 시 오류 없이 안전하게 폐기하도록 조치",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 티어드롭 공격의 오프셋 조작 및 장애 유발 원리",
                "model_answer": "Fragment 오프셋을 서로 중첩되도록 조작하여 수신 시스템이 재조합 시 오류로 충돌하게 만든다.",
                "rubric": {
                    "keywords": [
                        ["오프셋", "offset", "fragment offset"],
                        ["중첩", "겹치", "재조합 오류", "크래시", "다운"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) Tiny Fragment 공격의 개념 및 방화벽 필터링 우회 원리",
                "model_answer": "첫 번째 단편을 작게 분할하여 포트 정보가 두 번째 단편으로 넘어가게 만들어 방화벽 포트 검사를 우회한다.",
                "rubric": {
                    "keywords": [
                        ["포트 정보", "포트 번호", "헤더 분할"],
                        ["두 번째 단편", "우회", "필터링 통과", "확인 불가"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) 단편화 공격 대응을 위한 방화벽 및 시스템 방어 대책 2가지",
                "model_answer": "비정상 초소형 단편 차단, 방화벽 레벨 재조합 검증 후 통과, 최신 OS 패치 적용",
                "rubric": {
                    "keywords": [
                        ["패치", "최신 패치", "os 패치"],
                        ["초소형 단편 차단", "재조합 검증", "오프셋 검증", "단편화 검사"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "티어드롭은 오프셋 중첩으로 시스템 충돌을, Tiny Fragment는 포트 헤더 분할로 방화벽 우회를 노리며, 방화벽 재조합 검사 및 OS 패치로 대응합니다 (SRC-07 p.150).",
        "source_id": "SRC-07",
        "source_page": 150,
        "concept_id": "CON-NET-02",
        "difficulty": "hard",
        "tags": ["티어드롭", "TinyFragment", "단편화공격", "오프셋중첩", "방화벽우회", "DoS"]
    },
    {
        "id": "Q-PRAC-023",
        "type": "practical",
        "category": "네트워크 보안",
        "score": 16,
        "question": "다음은 기업 내부 네트워크를 보호하는 시스코(Cisco) 라우터에서 스머프(Smurf) 증폭 반사 공격을 차단하기 위해 수행하는 보안 설정 시나리오이다. [설정 요구조건]과 [라우터 설정 프롬프트]를 분석하고 각 질문에 답하시오.\n\n[설정 요구조건]\n- 외부 인터넷과 연결된 인터페이스: FastEthernet0/0\n- 내부 신뢰 네트워크 대역: 192.168.1.0/24\n- 외부 인터넷에서 내부 신뢰 네트워크(192.168.1.0/24) 대역을 출발지 IP로 사칭하여 유입되는 모든 비인가 ICMP 패킷을 차단하고, 그 외의 일반 IP 트래픽은 모두 허용하는 확장 Access-List(번호 100)를 생성하여 FastEthernet0/0 유입(inbound) 방향에 적용할 것\n- 유니캐스트 패킷이 로컬 서브넷의 링크 브로드캐스트로 전환되는 것을 차단할 것\n\n[라우터 설정 프롬프트]\nRouter(config)# ( ① )\nRouter(config)# access-list 100 permit ip any any\nRouter(config)# ( ② )\nRouter(config-if)# ip access-group 100 in\nRouter(config-if)# ( ③ )\n\n1) 공격자가 스머프(Smurf) 공격을 수행할 때 피해자 서버에 대량의 트래픽을 유발시키는 공격 동작 메커니즘을 출발지 IP 및 대상 주소 관점에서 서술하시오. (6점)\n2) 라우터 설정의 빈칸 ( ① )에 들어갈 확장 Access-List 차단 규칙 명령어와 ( ② )에 들어갈 인터페이스 진입 명령어를 쓰시오. (5점)\n3) 빈칸 ( ③ )에 들어갈 명령어 구문과, 이 설정이 스머프 공격을 무력화시키는 원리를 서술하시오. (5점)",
        "model_answer": "1) 스머프 공격 메커니즘: 공격자가 패킷의 출발지 IP(Source IP)를 공격 대상(피해자)의 IP 주소로 위조(IP Spoofing)한 후, 목적지 IP(Destination IP)를 특정 네트워크의 브로드캐스트 주소(예: 192.168.1.255)로 설정한 ICMP Echo Request(Ping) 패킷을 다량 전송한다. 해당 서브넷의 모든 활성 호스트들이 일제히 위조된 출발지 IP(피해자 서버)로 대량의 ICMP Echo Reply 응답을 일시에 반사 전송함으로써 피해자의 네트워크 대역폭과 시스템 자원을 고갈시킨다.\n2) ( ① ), ( ② ) 명령어:\n- ( ① ): `access-list 100 deny icmp 192.168.1.0 0.0.0.255 any` (또는 `deny ip 192.168.1.0 0.0.0.255 any`)\n- ( ② ): `interface FastEthernet0/0` (또는 `int fa0/0`)\n3) ( ③ ) 명령어 및 원리:\n- 명령어: `no ip directed-broadcast`\n- 원리: 외부에서 라우터로 유입된 특정 서브넷 대상의 유니캐스트 패킷이 해당 인터페이스의 로컬 브로드캐스트로 전환되는 것을 차단함으로써, 브로드캐스트 대역으로 전송된 패킷이 서브넷 내부의 수많은 호스트들에게 일제히 증폭 전달되는 현상을 원천 방지한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) 스머프 공격의 IP 변조 및 브로드캐스트 반사 메커니즘",
                "model_answer": "출발지 IP를 피해자로 위조하고 목적지를 브로드캐스트로 설정하여 다수의 호스트가 피해자에게 동시 응답하게 만든다.",
                "rubric": {
                    "keywords": [
                        ["출발지 ip", "피해자", "위조", "스푸핑"],
                        ["브로드캐스트", "목적지"],
                        ["icmp echo reply", "응답", "반사", "증폭"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 5,
                "prompt": "2) 라우터 설정 ( ① )의 ACL 차단 구문 및 ( ② ) 인터페이스 명령",
                "model_answer": "( ① ) access-list 100 deny icmp 192.168.1.0 0.0.0.255 any, ( ② ) interface FastEthernet0/0",
                "rubric": {
                    "keywords": [
                        ["access-list 100 deny", "192.168.1.0", "0.0.0.255"],
                        ["interface fastethernet0/0", "interface", "fastethernet0/0"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 3,
                "score": 5,
                "prompt": "3) ( ③ )의 directed-broadcast 차단 명령어 및 무력화 원리",
                "model_answer": "`no ip directed-broadcast`로, 유니캐스트가 서브넷 브로드캐스트로 변환되는 것을 막아 증폭 반사를 차단한다.",
                "rubric": {
                    "keywords": [
                        ["no ip directed-broadcast"],
                        ["브로드캐스트 변환 차단", "브로드캐스트 전환", "증폭 차단"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            }
        ],
        "explanation": "스머프 공격은 위조된 ICMP 요청을 브로드캐스트로 보내 다량의 Echo Reply를 유발하며, ACL 차단 및 no ip directed-broadcast로 방어합니다 (SRC-07 p.441, p.449 20회 기출).",
        "source_id": "SRC-07",
        "source_page": 449,
        "concept_id": "CON-NET-04",
        "difficulty": "hard",
        "tags": ["Smurf", "라우터ACL", "directed-broadcast", "Cisco", "DDoS방어"]
    },
    {
        "id": "Q-PRAC-024",
        "type": "practical",
        "category": "네트워크 보안",
        "score": 16,
        "question": "다음은 보안 관리자가 내부 DNS 서버(192.168.159.133)로 유입되는 비정상적인 대량 트래픽을 패킷 캡처 도구로 수집한 결과 중 일부이다. [패킷 캡처 로그]를 분석하고 각 질문에 답하시오.\n\n[패킷 캡처 로그]\nNo  Timestamp    SourceIP        SRCPort  DestinationIP    DSTPort  Protocol\n49  40.043491    33.228.79.82    2235     192.168.159.133  53       DNS\n50  40.144564    170.91.141.31   2236     192.168.159.133  53       DNS\n51  40.245563    170.203.168.176 2237     192.168.159.133  53       DNS\n52  40.346658    171.102.103.175 2238     192.168.159.133  53       DNS\n53  40.447705    6.133.62.251    2239     192.168.159.133  53       DNS\n54  40.548938    62.42.23.216    2240     192.168.159.133  53       DNS\n55  40.650258    71.56.58.54     2241     192.168.159.133  53       DNS\n56  40.750777    33.160.34.38    2242     192.168.159.133  53       DNS\n\n1) 패킷 로그를 분석하여 공격 대상이 되고 있는 피해자 시스템의 IP 주소와 수신 포트 번호, 그리고 공격자가 악용하고 있는 서비스 프로토콜 명칭을 쓰시오. (4점)\n2) 공격자가 공격 효율을 극대화하기 위해 다수의 외부 DNS 서버를 경유하여 유발하는 분산 반사 서비스 거부(DRDoS) 공격의 구체적인 명칭을 쓰고, 공격자가 DNS 질의 시 응답 데이터 크기를 비약적으로 증폭시키기 위해 사용하는 질의 레코드 타입(Record Type)의 명칭을 쓰시오. (6점)\n3) 네트워크 게이트웨이 시스코 라우터에서 위와 같이 외부에서 DNS 서버로 유입되는 비정상 대량 UDP 트래픽을 차단하기 위한 확장 Access-List(번호 110) 명령어를 빈칸 [ ① ], [ ② ]를 채워 완성하시오. (6점)\n   Router(config)# access-list 110 deny [ ① ] any any eq [ ② ]",
        "model_answer": "1) 로그 분석 결과:\n- 공격 대상(피해자) IP: 192.168.159.133\n- 수신 포트 번호: 53\n- 서비스 프로토콜: DNS (Domain Name System / UDP)\n2) 공격 명칭 및 레코드 타입:\n- 공격 명칭: DNS 증폭 공격 (DNS Amplification Attack; DNS 반사 증폭 DRDoS)\n- 질의 레코드 타입: ANY 레코드 (또는 TXT 레코드)\n  (작은 크기의 질의 요청을 보내고 도메인의 모든 존 정보를 담은 수십 배 이상의 대용량 응답을 유발하여 트래픽을 증폭시킴)\n3) 라우터 ACL 빈칸 완성:\n- [ ① ]: `udp`\n- [ ② ]: `53` (또는 `domain`)\n  완성된 구문: `access-list 110 deny udp any any eq 53`",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 로그에 나타난 공격 대상 IP, 수신 포트 및 서비스 프로토콜",
                "model_answer": "피해자 IP는 192.168.159.133, 수신 포트는 53, 프로토콜은 DNS(UDP)이다.",
                "rubric": {
                    "keywords": [
                        ["192.168.159.133"],
                        ["53"],
                        ["dns", "udp"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) DRDoS 공격 명칭 및 트래픽 증폭 질의 레코드 타입",
                "model_answer": "DNS 증폭(Amplification) 공격이며, 대용량 응답을 유발하는 ANY(또는 TXT) 레코드를 사용한다.",
                "rubric": {
                    "keywords": [
                        ["dns 증폭", "dns amplification", "증폭 공격", "dns 반사 증폭"],
                        ["any", "any 레코드", "txt", "txt 레코드"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 3,
                "score": 6,
                "prompt": "3) 라우터 Access-List 110 빈칸 [ ① ], [ ② ]",
                "model_answer": "[ ① ] udp, [ ② ] 53 (access-list 110 deny udp any any eq 53)",
                "rubric": {
                    "keywords": [
                        ["udp"],
                        ["53", "domain"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "explanation": "DNS Amplification 공격은 ANY 레코드 질의를 통해 대량의 증폭 응답을 유발하며, 라우터에서 `access-list 110 deny udp any any eq 53`으로 차단합니다 (SRC-07 p.445, 6회 기출).",
        "source_id": "SRC-07",
        "source_page": 445,
        "concept_id": "CON-NET-04",
        "difficulty": "hard",
        "tags": ["DNS증폭공격", "DNS_Amplification", "DRDoS", "라우터ACL", "트래픽분석"]
    }
]
