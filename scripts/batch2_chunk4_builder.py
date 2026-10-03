# -*- coding: utf-8 -*-
"""
Batch 2 - Chunk 4: Descriptive (2 questions) & Practical (5 questions)
Q-DESC-033 ~ Q-DESC-034
Q-PRAC-015 ~ Q-PRAC-019
"""

CHUNK_4_QUESTIONS = [
    {
        "id": "Q-DESC-033",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "question": "대표적인 오픈소스 침투 테스트 프레임워크인 Metasploit의 주요 모듈 4가지에 대하여 각 물음에 답하시오.\n\n1) 대상 시스템의 알려진 취약점(RCE, 버퍼 오버플로우 등)을 공격하여 침투하기 위해 사용되는 코드 모듈의 명칭을 쓰시오. (3점)\n2) 익스플로잇 성공 후 대상 시스템에서 공격자가 원하는 원격 쉘 획득 등의 행위를 실행하는 코드 모듈의 명칭을 쓰시오. (3점)\n3) 침투 전 포트 스캐닝, 서비스 버전 확인, 취약점 탐색 등 정보 수집 및 보조 작업을 수행하는 모듈의 명칭을 쓰시오. (3점)\n4) 안티바이러스나 IDS/IPS 등 보안 솔루션의 시그니처 탐지를 우회하기 위해 페이로드를 난독화하는 모듈의 명칭을 쓰시오. (3점)",
        "model_answer": "1) 익스플로잇 (Exploit): 시스템의 특정 취약점을 공격하여 비정상적인 동작이나 권한을 획득하기 위한 공격 코드이다.\n2) 페이로드 (Payload): 익스플로잇 성공 후 대상 시스템에서 공격자가 원격 제어, 쉘 실행(리버스 쉘 등)을 수행하는 악성 코드이다.\n3) 보조 모듈 (Auxiliary Module): 공격 실행 전 대상 시스템의 포트 스캔, 서비스 식별, 취약점 탐색 등 정보 수집을 수행하는 모듈이다.\n4) 인코더 (Encoder): 시그니처 기반 보안 솔루션(백신, IDS/IPS)의 탐지를 우회하기 위해 페이로드를 암호화 또는 난독화하여 포장하는 모듈이다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 취약점을 공격하여 침투하는 코드 모듈의 명칭",
                "model_answer": "익스플로잇 (Exploit)",
                "rubric": {
                    "keywords": [
                        ["익스플로잇", "exploit", "취약점 공격"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 익스플로잇 성공 후 대상 시스템에서 실행되는 코드 모듈의 명칭",
                "model_answer": "페이로드 (Payload)",
                "rubric": {
                    "keywords": [
                        ["페이로드", "payload", "쉘코드", "원격 제어"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 정보 수집 및 스캐닝을 수행하는 보조 모듈의 명칭",
                "model_answer": "보조 모듈 (Auxiliary Module)",
                "rubric": {
                    "keywords": [
                        ["보조 모듈", "보조모듈", "auxiliary", "auxiliary module"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 보안 솔루션 탐지 우회를 위해 페이로드를 난독화하는 모듈의 명칭",
                "model_answer": "인코더 (Encoder)",
                "rubric": {
                    "keywords": [
                        ["인코더", "encoder", "난독화", "탐지 우회"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "Metasploit의 4대 주요 구성요소는 Exploit, Payload, Auxiliary, Encoder입니다 (SRC-04 p.63).",
        "source_id": "SRC-04",
        "source_page": 63,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["Metasploit", "Exploit", "Payload", "Auxiliary", "Encoder"]
    },
    {
        "id": "Q-DESC-034",
        "type": "descriptive",
        "category": "애플리케이션 보안",
        "score": 12,
        "question": "대표적인 저대역폭 애플리케이션 계층 DoS 공격인 Slowloris와 RUDY(Slow HTTP POST)의 공격 원리와 이에 대응하기 위한 웹 서버 보안 대책에 대하여 다음 물음에 답하시오.\n\n1) Slowloris 공격의 헤더 전송 방식과 공격 원리를 서술하시오. (3점)\n2) RUDY(Slow HTTP POST) 공격의 Content-Length 및 본문 전송 방식과 공격 원리를 서술하시오. (3점)\n3) 두 공격이 공통적으로 노리는 웹 서버의 구조적 취약점(자원 고갈 대상)을 서술하시오. (3점)\n4) Apache 웹 서버 등에서 두 공격을 방어하기 위한 설정 및 대응 대책 2가지를 서술하시오. (3점)",
        "model_answer": "1) Slowloris: HTTP 요청 헤더의 끝을 알리는 개행문자(\\r\\n\\r\\n)를 완성하지 않고, 지속적으로 비정상적인 헤더(예: X-a: b\\r\\n)를 극도로 지연 전송하여 웹 서버의 연결 세션을 지속 점유하는 공격이다.\n2) RUDY: HTTP POST 요청 시 헤더의 Content-Length를 매우 크게 설정한 후, 메시지 본문(Body)을 1바이트씩 장시간에 걸쳐 지연 전송하여 웹 서버의 수신 버퍼와 연결을 장시간 고갈시키는 공격이다.\n3) 공통 타깃: 웹 서버가 클라이언트 요청마다 할당하는 동시 연결 수(Connection Pool/Worker Thread)와 연결 세션 자원을 고갈시켜 정상 사용자의 신규 접속을 차단한다.\n4) 대응 대책:\n- 웹 서버의 요청 타임아웃(Timeout) 시간을 짧게 축소 설정\n- Apache의 mod_reqtimeout 모듈 활성화(헤더/바디 최소 수신 속도 및 제한 시간 설정)\n- 동일 IP당 최대 동시 연결 수(MaxKeepAliveRequests, mod_evasive) 제한",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) Slowloris 공격의 헤더 전송 방식 및 원리",
                "model_answer": "개행문자(\\r\\n\\r\\n)를 완성하지 않고 미완성 헤더를 지연 전송하여 연결을 유지한다.",
                "rubric": {
                    "keywords": [
                        ["\\r\\n\\r\\n", "개행문자", "헤더 끝", "미완성"],
                        ["지연 전송", "연결 유지", "세션 점유"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) RUDY 공격의 Content-Length 및 본문 지연 전송 원리",
                "model_answer": "Content-Length를 크게 설정한 후 본문을 1바이트씩 지연 전송하여 수신 버퍼를 고갈시킨다.",
                "rubric": {
                    "keywords": [
                        ["content-length", "크게 설정", "큰 값"],
                        ["본문", "body", "1바이트", "지연 전송", "고갈"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 두 공격이 공통적으로 노리는 웹 서버의 고갈 대상",
                "model_answer": "웹 서버의 동시 연결 세션 수(커넥션 풀, 워커 스레드)를 고갈시켜 정상 접속을 방해한다.",
                "rubric": {
                    "keywords": [
                        ["연결 세션", "동시 연결", "커넥션", "worker", "스레드", "소진", "고갈"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 웹 서버 차원의 대응 방안 2가지",
                "model_answer": "타임아웃 시간 단축, mod_reqtimeout 모듈 설정, 동일 IP 동시 연결 수 제한을 적용한다.",
                "rubric": {
                    "keywords": [
                        ["타임아웃", "timeout", "mod_reqtimeout", "동시 연결 제한", "연결 수 제한"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "Slow HTTP DoS 공격(Slowloris, RUDY)은 소량 트래픽으로 웹서버 연결 자원을 고갈시키며, mod_reqtimeout 및 Timeout 단축으로 대응합니다 (SRC-04 p.150, 152).",
        "source_id": "SRC-04",
        "source_page": 150,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["DoS", "Slowloris", "RUDY", "mod_reqtimeout", "SlowHTTP"]
    },
    {
        "id": "Q-PRAC-015",
        "type": "practical",
        "category": "네트워크 보안",
        "score": 16,
        "question": "다음은 네트워크 패킷 캡처 도구인 `tcpdump`의 실행 결과에 출력된 IP 패킷 단편화(Fragmentation) 정보이다. 출력된 정보의 각 항목 ①~④의 정확한 기술적 의미를 서술하시오.\n\n[tcpdump 단편화 출력]\nfrag 95:1480@ 2920+\n     ①   ②    ③  ④\n\n1) ① '95'의 의미를 서술하시오. (4점)\n2) ② '1480'의 의미를 서술하시오. (4점)\n3) ③ '2920'의 의미를 서술하시오. (4점)\n4) ④ '+' 기호의 의미를 서술하시오. (4점)",
        "model_answer": "1) ① 95: 단편화된 패킷들이 원래 동일한 IP 데이터그램에 속함을 식별하기 위한 IP 헤더의 식별자(Identification, ID) 번호이다.\n2) ② 1480: 현재 단편화된 패킷에 포함된 IP 페이로드(데이터)의 크기가 1480 바이트임을 나타낸다.\n3) ③ 2920: 원본 IP 데이터그램 내에서 현재 단편 데이터가 시작하는 오프셋(Fragment Offset) 위치로, 2920번째 바이트부터 시작됨을 의미한다.\n4) ④ +: More Fragments (MF) 플래그가 1로 설정되어 있음을 의미하며, 현재 패킷 뒤에 추가 단편화 패킷이 더 전송될 것임을 나타낸다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) ① '95'의 기술적 의미",
                "model_answer": "동일 IP 데이터그램임을 식별하는 IP 패킷 식별자(Identification / IP ID)",
                "rubric": {
                    "keywords": [
                        ["식별자", "id", "identification", "ip id", "식별 번호"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) ② '1480'의 기술적 의미",
                "model_answer": "현재 단편에 포함된 데이터(페이로드) 크기 (1480 바이트)",
                "rubric": {
                    "keywords": [
                        ["페이로드", "데이터 크기", "데이터 길이", "1480 바이트", "1480byte"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) ③ '2920'의 기술적 의미",
                "model_answer": "원본 데이터그램 내에서 현재 단편의 시작 위치를 나타내는 단편화 오프셋(Fragment Offset, 2920 바이트)",
                "rubric": {
                    "keywords": [
                        ["단편화 오프셋", "오프셋", "fragment offset", "시작 위치", "2920"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 4,
                "score": 4,
                "prompt": "4) ④ '+' 기호의 기술적 의미",
                "model_answer": "More Fragments(MF) 플래그가 설정되어 뒤에 단편이 더 남아있음을 표시 (MF=1)",
                "rubric": {
                    "keywords": [
                        ["more fragments", "mf", "mf 플래그", "단편이 더", "추가 단편"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "tcpdump 단편화 출력 'frag id:size@offset+'는 ID, 데이터크기, 오프셋, MF플래그(+)를 나타냅니다 (SRC-04 p.88, 9회 기출).",
        "source_id": "SRC-04",
        "source_page": 88,
        "concept_id": "CON-NET-01",
        "difficulty": "hard",
        "tags": ["tcpdump", "단편화", "Fragmentation", "Offset", "MF"]
    },
    {
        "id": "Q-PRAC-016",
        "type": "practical",
        "category": "네트워크 보안",
        "score": 16,
        "question": "다음은 OpenSSL 라이브러리의 하트비트(HeartBeat) 확장 모듈의 버그로 인해 발생하는 하트블리드(Heartbleed) 취약점(CVE-2014-0160) 탐지를 위한 Snort Rule이다. 설정된 규칙의 각 항목 ①~④의 기술적 의미를 서술하시오.\n\n[Snort Rule]\nalert tcp any any <> any [443,465,523] (\n    content:\"|18 03 00|\"; depth: 3;\n    content:\"|01|\"; distance: 2; within: 1;\n    content:!\"|00|\"; within: 1;\n    msg: \"Heartbleed attack (CVE-2014-0160)\"; sid: 1;\n)\n\n1) `[443,465,523]` 포트 지정의 의미를 서술하시오. (4점)\n2) `content:\"|18 03 00|\"; depth: 3;` 옵션의 의미를 서술하시오. (4점)\n3) `content:\"|01|\"; distance: 2; within: 1;` 옵션의 의미를 서술하시오. (4점)\n4) `content:!\"|00|\"; within: 1;` 옵션의 의미를 서술하시오. (4점)",
        "model_answer": "1) [443,465,523]: HTTPS(443), SMTPS(465) 등 SSL/TLS 보안 통신 프로토콜이 적용되는 주요 서비스 포트를 대상으로 트래픽을 검사함을 의미한다.\n2) content:\"|18 03 00|\"; depth: 3;: 패킷 페이로드의 최초 3바이트(depth: 3) 내에서 TLS Heartbeat 메시지 유형(0x18)과 SSL 3.0/TLS 1.0 프로토콜 버전(0x03 0x00) 바이트 패턴을 검사한다.\n3) content:\"|01|\"; distance: 2; within: 1;: 이전 일치 패턴 이후 2바이트를 건너뛴(distance: 2) 바로 다음 1바이트(within: 1)가 Heartbeat Request(0x01) 메시지 유형인지 검사한다.\n4) content:!\"|00|\"; within: 1;: 뒤따르는 1바이트(within: 1)의 페이로드 길이 상위 바이트가 0x00이 아닌 경우(!\"|00|\"), 즉 요청 데이터 길이가 비정상적으로 큰 악성 요청을 탐지한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) [443,465,523] 포트 지정의 의미",
                "model_answer": "HTTPS(443), SMTPS(465) 등 SSL/TLS 보안 통신 포트를 지정",
                "rubric": {
                    "keywords": [
                        ["ssl", "tls", "https", "smtps", "보안 통신", "포트"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) content:\"|18 03 00|\"; depth: 3; 의 의미",
                "model_answer": "페이로드 시작 3바이트 내에서 Heartbeat 메시지 타입(0x18) 및 SSL/TLS 버전(0x03 0x00) 검사",
                "rubric": {
                    "keywords": [
                        ["heartbeat", "하트비트", "0x18", "타입"],
                        ["3바이트", "depth: 3", "depth", "ssl", "tls"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) content:\"|01|\"; distance: 2; within: 1; 의 의미",
                "model_answer": "이전 패턴에서 2바이트 떨어진 위치의 1바이트가 Heartbeat Request(0x01)인지 검사",
                "rubric": {
                    "keywords": [
                        ["distance", "2바이트", "건너뛰"],
                        ["within", "1바이트", "0x01", "request", "요청"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 4,
                "score": 4,
                "prompt": "4) content:!\"|00|\"; within: 1; 의 의미",
                "model_answer": "길이 필드가 0이 아닌 비정상적으로 큰 페이로드 요청을 탐지",
                "rubric": {
                    "keywords": [
                        ["길이 필드", "길이", "페이로드 길이"],
                        ["!\"|00|\"", "0이 아닌", "비정상", "탐지"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "Heartbleed Snort 룰은 TLS Heartbeat(0x18) Request(0x01) 패킷의 비정상 길이 요청을 탐지합니다 (SRC-04 p.174, 13회 기출).",
        "source_id": "SRC-04",
        "source_page": 174,
        "concept_id": "CON-NET-02",
        "difficulty": "hard",
        "tags": ["Heartbleed", "Snort", "SnortRule", "CVE-2014-0160", "침해사고"]
    },
    {
        "id": "Q-PRAC-017",
        "type": "practical",
        "category": "애플리케이션 보안",
        "score": 16,
        "question": "다음은 웹 서버로 유입된 비정상적인 HTTP 트래픽 패킷 캡처 화면이다. [패킷 캡처 화면]을 분석하고 다음 각 질문에 답하시오.\n\n[1번 패킷 캡처 화면]\nPOST /zb41p16/index.html HTTP/1.1\nHost: 192.16.0.80\nConnection: keep-alive\nContent-Length: 100000000\nUser-Agent: soojebi\npage=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n\n[2번 패킷 캡처 화면]\nHTTP/1.1 200 OK\nDate: Mon, 9 Dec 2019 12:00:00 GMT\nServer: Apache/2.0.52 (CentOS)\nContent-Length: 2\nConnection: close\nContent-Type: text/html; charset=EUC-KR\n\n1) 수행 중인 웹 애플리케이션 서비스 거부(DoS) 공격 기법의 정확한 명칭을 쓰시오. (4점)\n2) 해당 공격이라고 판단한 구체적인 근거를 패킷 캡처 헤더 필드를 인용하여 서술하시오. (6점)\n3) 대상 웹 서버(Apache 등)에서 이 공격을 차단하고 방어하기 위한 실무적인 대응 방안 2가지를 서술하시오. (6점)",
        "model_answer": "1) 공격 명칭: Slow HTTP POST DoS (또는 RUDY, R-U-Dead-Yet)\n2) 판단 근거: POST 요청 시 헤더의 `Content-Length`를 `100000000`(약 100MB)이라는 비정상적으로 매우 큰 값으로 선언한 후, 실제 본문(page=AAAA...)을 한 번에 전송하지 않고 극소량씩 지연 전송하여 웹 서버의 연결 세션을 지속 점유하려 하기 때문이다.\n3) 대응 방안:\n- Apache 웹 서버의 `mod_reqtimeout` 모듈을 활성화하여 요청 바디의 최소 수신 전송률 및 타임아웃 제한 설정 (예: RequestReadTimeout body=10,MinRate=500)\n- Apache `httpd.conf`에서 `Timeout` 디렉티브 설정값을 축소 (예: Timeout 10~30)\n- 방화벽이나 웹방화벽(WAF)에서 동일 IP당 동시 연결 수(Connection Limit) 제한",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 수행 중인 DoS 공격 기법의 명칭",
                "model_answer": "Slow HTTP POST DoS (RUDY; R-U-Dead-Yet)",
                "rubric": {
                    "keywords": [
                        ["slow http post", "slow http post dos", "rudy", "r-u-dead-yet", "슬로우 http post"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) 해당 공격으로 판단한 구체적 근거",
                "model_answer": "Content-Length를 100000000으로 비정상적으로 크게 설정하고 본문을 소량씩 지연 전송하기 때문",
                "rubric": {
                    "keywords": [
                        ["content-length", "100000000", "비정상적으로 큰"],
                        ["지연 전송", "소량씩", "본문", "바디"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 3,
                "score": 6,
                "prompt": "3) 웹 서버 차원의 실무 대응 방안 2가지",
                "model_answer": "mod_reqtimeout 모듈 설정(RequestReadTimeout), Timeout 축소, 동일 IP 동시 연결 수 제한",
                "rubric": {
                    "keywords": [
                        ["mod_reqtimeout", "requestreadtimeout"],
                        ["timeout", "타임아웃 단축", "타임아웃 축소", "동시 연결 제한", "waf"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "explanation": "Slow HTTP POST DoS는 비정상적인 Content-Length(100000000)를 설정 후 지연 전송하며, mod_reqtimeout 및 Timeout 단축으로 방어합니다 (SRC-04 p.176, 15회 기출).",
        "source_id": "SRC-04",
        "source_page": 176,
        "concept_id": "CON-APP-01",
        "difficulty": "hard",
        "tags": ["SlowHTTP", "RUDY", "Content-Length", "mod_reqtimeout", "패킷분석"]
    },
    {
        "id": "Q-PRAC-018",
        "type": "practical",
        "category": "정보보호 관리 및 법규",
        "score": 16,
        "question": "다음은 특정 정보자산에 대한 정량적 위험 분석(Quantitative Risk Analysis) 및 보안 대책 평가 자료이다. [표]를 참고하여 각 물음에 답하시오.\n\n[정량적 위험 분석 표]\n| 구분 | A 대책 | B 대책 |\n| :--- | :--- | :--- |\n| 자산가치(AV) | 100,000만원 | 100,000만원 |\n| 노출계수(EF) | 20% | 80% |\n| 단일 예상 손실액(SLE) | ( ① ) 만원 | ( ② ) 만원 |\n| 연간 발생률(ARO) | 50% | 25% |\n| 연간 예상 손실액(ALE) | ( ③ ) 만원 | ( ④ ) 만원 |\n| 대책 적용 시 ALE 감소액 | 30,000만원 | 20,000만원 |\n| 연간 대책 비용 | 17,000만원 | 4,000만원 |\n| 대책 적용 시 순이익(CBA) | ( ⑤ ) 만원 | ( ⑥ ) 만원 |\n\n1) 표의 빈칸 ①~⑥에 들어갈 금액(숫자)을 각각 계산하여 쓰시오. (8점)\n2) A 대책과 B 대책 중 비용 대비 효과(순이익) 관점에서 최종 선택해야 하는 보안 대책을 제시하고, 그 근거를 수치와 함께 서술하시오. (8점)",
        "model_answer": "1) 표의 빈칸 금액 계산:\n- ① SLE(A) = 100,000만원 * 20% = 20,000만원\n- ② SLE(B) = 100,000만원 * 80% = 80,000만원\n- ③ ALE(A) = 20,000만원 * 50% = 10,000만원\n- ④ ALE(B) = 80,000만원 * 25% = 20,000만원\n- ⑤ A 대책 순이익 = ALE 감소(30,000) - 대책비용(17,000) = 13,000만원\n- ⑥ B 대책 순이익 = ALE 감소(20,000) - 대책비용(4,000) = 16,000만원\n\n2) 최종 대책 선택 및 근거:\n- 선택 대책: B 대책\n- 선택 근거: 비용 대비 편익 분석(Cost-Benefit Analysis) 결과, A 대책 적용 시 연간 순이익은 13,000만원인 반면, B 대책 적용 시 연간 순이익은 16,000만원으로 B 대책이 3,000만원 더 높은 순이익(경제적 타당성)을 제공하므로 B 대책을 선택해야 한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 8,
                "prompt": "1) 표의 빈칸 ①~⑥ 금액 계산 (①~⑥ 순서대로 기재)",
                "model_answer": "① 20,000, ② 80,000, ③ 10,000, ④ 20,000, ⑤ 13,000, ⑥ 16,000",
                "rubric": {
                    "keywords": [
                        ["20000", "20,000"],
                        ["80000", "80,000"],
                        ["10000", "10,000"],
                        ["13000", "13,000"],
                        ["16000", "16,000"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            },
            {
                "sub_id": 2,
                "score": 8,
                "prompt": "2) 최종 선택해야 하는 보안 대책 및 선정 근거",
                "model_answer": "B 대책 선택. B 대책의 순이익(16,000만원)이 A 대책(13,000만원)보다 크므로 경제적 타당성이 더 높다.",
                "rubric": {
                    "keywords": [
                        ["b 대책", "b대책", "b 선택"],
                        ["순이익", "16,000", "16000", "13,000", "13000", "비용 대비 효과", "더 크"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            }
        ],
        "explanation": "정량적 위험 분석에서 SLE=AV*EF, ALE=SLE*ARO이며 순이익(ALE감소-비용)이 더 큰 B대책(16,000만원)을 선정합니다 (SRC-10 p.110, 16회 기출).",
        "source_id": "SRC-10",
        "source_page": 110,
        "concept_id": "CON-MGT-01",
        "difficulty": "hard",
        "tags": ["정량적위험분석", "SLE", "ALE", "ARO", "비용편익분석"]
    },
    {
        "id": "Q-PRAC-019",
        "type": "practical",
        "category": "정보보호 관리 및 법규",
        "score": 16,
        "question": "다음은 모 피트니스 센터의 [헬스클럽 가입신청서] 양식이다. 개인정보보호법에 근거하여 법률 위반 사항 2가지를 지적하고, 각각에 대한 올바른 법적 개선 방안을 서술하시오.\n\n[헬스클럽 가입신청서]\n< 필수항목 수집·이용 동의 >\n수집목적: 회원관리\n수집항목: 이름, 성별, 생년월일, 연락처\n보유기간: 회원탈퇴 시까지\n안내: 해당 내용을 거부할 수 있으며 거부 시 불이익이 있을 수 있습니다.\n[ ] 동의합니다   [ ] 동의하지 않습니다\n이름: 수제비 / 생년월일: 2010. 10. 20 / 성별: 남 / 연락처: 010-0000-0000\n\n< 선택항목 수집·이용 동의 >\n수집목적: 최신정보제공, 맞춤형 헬스케어\n수집항목: 키, 몸무게, 질병(해당 시에만), 이메일\n보유기간: 회원탈퇴 시까지\n안내: 선택정보는 동의하지 않아도 되나 동의하지 않을 경우 PT(개인트레이닝) 서비스를 받으시는데 불이익이 있을 수 있습니다.\n[ ] 동의합니다   [ ] 동의하지 않습니다\n신청일: 2017. 01. 10  신청자: 수제비 (서명)\n\n1) 첫 번째 법률 위반 사항과 개선 방안을 서술하시오. (8점)\n2) 두 번째 법률 위반 사항과 개선 방안을 서술하시오. (8점)",
        "model_answer": "1) 위반 사항 1: 만 14세 미만 아동의 개인정보 수집 시 법정대리인 동의 미획득\n- 위반 내용: 신청자의 생년월일이 2010년 10월 20일로 신청일(2017년) 기준 만 6세(만 14세 미만) 아동임에도 불구하고 법정대리인의 동의 절차나 법정대리인의 서명이 누락되어 있다. (법 제22조의2 위반)\n- 개선 방안: 만 14세 미만 아동의 개인정보를 처리하기 위해서는 법정대리인의 성명·연락처 등 최소한의 정보를 수집하고 반드시 법정대리인의 동의를 별도로 받아야 한다.\n\n2) 위반 사항 2: 선택항목 미동의를 이유로 한 서비스 제공 거부(불이익 제공) 금지 위반\n- 위반 내용: 선택항목(키, 몸무게, 질병, 이메일)에 동의하지 않는다는 이유로 기본 부가서비스인 PT(개인트레이닝) 서비스 제공에 불이익이 있을 수 있다고 명시하여 동의를 강제하였다. (법 제16조 제3항 위반)\n- 개선 방안: 선택항목은 정보주체가 동의를 거부하더라도 기본 헬스클럽 서비스 및 PT 서비스 등 재화나 서비스의 제공을 거부하거나 불이익을 주어서는 안 되며, 선택항목 미동의 시에도 정상적인 서비스 이용이 가능함을 고지하여야 한다.\n(추가 위반 가능 사항: 필수항목 거부 시 구체적인 불이익 내용 미고지 - '거부 시 회원가입 및 시설 이용 불가' 등 구체적 불이익 내용 명시 필요)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 8,
                "prompt": "1) 만 14세 미만 아동 관련 법률 위반 사항 및 개선 방안",
                "model_answer": "신청자가 만 14세 미만 아동이므로 법정대리인 동의를 받아야 하나 누락됨. 법정대리인 동의 절차를 추가해야 함.",
                "rubric": {
                    "keywords": [
                        ["만 14세 미만", "14세 미만", "법정대리인"],
                        ["법정대리인 동의", "법정대리인의 동의", "동의 누락", "동의 절차"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            },
            {
                "sub_id": 2,
                "score": 8,
                "prompt": "2) 선택항목 미동의 관련 법률 위반 사항 및 개선 방안",
                "model_answer": "선택항목 미동의 시 PT 서비스 불이익을 명시한 것은 법 제16조 위반임. 선택항목 거부 시에도 서비스 제공을 거부하지 않아야 함.",
                "rubric": {
                    "keywords": [
                        ["선택항목", "선택 정보", "미동의", "거부"],
                        ["서비스 제공 거부", "불이익", "pt 서비스", "거부할 수 없", "제공 거부 금지"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            }
        ],
        "explanation": "개인정보보호법상 만 14세 미만 아동은 법정대리인 동의가 필수이며, 선택항목 미동의를 이유로 재화·서비스 제공을 거부할 수 없습니다 (SRC-11 p.173, 9회 기출).",
        "source_id": "SRC-11",
        "source_page": 173,
        "concept_id": "CON-MGT-02",
        "difficulty": "hard",
        "tags": ["개인정보보호법", "법정대리인", "선택항목", "동의서", "위반분석"]
    }
]
