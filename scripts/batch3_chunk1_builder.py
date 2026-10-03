# -*- coding: utf-8 -*-
"""
Batch 3 - Chunk 1: SRC-08 Application Security (10 questions)
Q-SHORT-088 ~ Q-SHORT-093 (6 short)
Q-DESC-035 ~ Q-DESC-037 (3 desc)
Q-PRAC-020 (1 prac)
"""

CHUNK_1_QUESTIONS = [
    {
        "id": "Q-SHORT-088",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "웹 브라우저와 웹 서버 사이의 HTTP/HTTPS 트래픽을 중간에서 가로채어 패킷의 요청 및 응답 헤더와 본문을 실시간으로 확인·수정·재전송할 수 있으며, 웹 취약점 분석 및 모의해킹에 필수적으로 사용되는 Burp Suite, Paros, OWASP ZAP 등의 보안 점검 도구 유형을 의미하는 용어를 쓰시오.",
        "answer": "웹 프록시",
        "accepted_answers": ["웹 프록시", "웹프록시", "웹 프록시 도구", "Web Proxy", "HTTP 프록시", "프록시 도구", "웹 프록시도구"],
        "grading_mode": "normalized",
        "explanation": "Burp Suite, Paros, OWASP ZAP 등은 브라우저와 서버 간 통신을 인터셉트하여 분석하는 웹 프록시 도구입니다 (SRC-08 p.95, p.161 25회 기출).",
        "source_id": "SRC-08",
        "source_page": 95,
        "concept_id": "CON-APP-01",
        "difficulty": "easy",
        "tags": ["웹보안", "웹프록시", "BurpSuite", "OWASP_ZAP", "모의해킹"]
    },
    {
        "id": "Q-SHORT-089",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "웹 애플리케이션에서 파일 경로나 이름을 다루는 매개변수에 `../` 또는 `..\\`와 같은 상위 디렉터리 참조 문자를 조작 삽입하여, 웹 루트 디렉터리를 벗어나 시스템의 비인가된 디렉터리나 민감한 시스템 설정 파일(예: `/etc/passwd`)에 접근하는 웹 취약점 공격 기법의 명칭을 영문 또는 국문으로 쓰시오.",
        "answer": "디렉터리 접근",
        "accepted_answers": [
            "디렉터리 접근",
            "경로 조작",
            "디렉터리 접근 취약점",
            "경로조작",
            "디렉터리 트래버설",
            "디렉터리 순회",
            "Directory Traversal",
            "Path Traversal",
            "디렉토리 접근",
            "디렉토리 트래버설"
        ],
        "grading_mode": "normalized",
        "explanation": "경로 조작(Directory Traversal / Path Traversal; 디렉터리 접근)은 상대 경로 문자(..)를 이용해 비인가 파일에 접근하는 공격입니다 (SRC-08 p.118).",
        "source_id": "SRC-08",
        "source_page": 118,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["디렉터리접근", "경로조작", "DirectoryTraversal", "PathTraversal"]
    },
    {
        "id": "Q-SHORT-090",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "XML 문서를 파싱하는 웹 애플리케이션에서 DTD(Document Type Definition)의 외부 엔티티(External Entity) 선언을 악용하여, 공격자가 `<!ENTITY xxe SYSTEM \"file:///etc/passwd\">`와 같은 구문을 삽입함으로써 서버 내부 파일 열람, 내부 네트워크 스캔, SSRF 등을 유발하는 취약점 공격의 영문 약어를 쓰시오.",
        "answer": "XXE",
        "accepted_answers": ["XXE", "XML External Entity", "XXE Injection", "XML 외부 엔티티", "XML 외부 개체 삽입"],
        "grading_mode": "normalized",
        "explanation": "XXE(XML External Entity Injection)는 XML 파서가 DTD 외부 엔티티를 부적절하게 처리할 때 발생하는 취약점입니다 (SRC-08 p.137, 169, 16회 기출).",
        "source_id": "SRC-08",
        "source_page": 137,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["XXE", "XML", "취약점", "SSRF", "외부엔티티"]
    },
    {
        "id": "Q-SHORT-091",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "서버 간 처리되는 요청에 검증되지 않은 외부 입력값을 허용하여, 공격자가 조작한 URI나 요청을 통해 취약한 웹 서버가 공격자가 의도한 내부망 시스템이나 외부 서버로 비인가 요청을 대신 전송하게 만드는 서버 측 웹 취약점 공격의 영문 약어를 쓰시오.",
        "answer": "SSRF",
        "accepted_answers": ["SSRF", "Server-Side Request Forgery", "Server Side Request Forgery", "서버 사이드 요청 위조", "서버 측 요청 위조", "서버사이드 요청위조", "서버사이드요청위조"],
        "grading_mode": "normalized",
        "explanation": "SSRF(Server-Side Request Forgery; 서버 사이드 요청 위조)는 서버 간 요청 시 입력값을 조작하여 서버가 공격자의 의도대로 내부 시스템 등에 요청을 보내게 만드는 취약점입니다 (SRC-08 p.112, p.162 28회 기출).",
        "source_id": "SRC-08",
        "source_page": 112,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["SSRF", "ServerSideRequestForgery", "웹취약점", "서버요청위조"]
    },
    {
        "id": "Q-SHORT-092",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "HTML 문서 내에서 새 창이나 새 탭을 여는 링크(`target=\"_blank\"`)를 사용자가 클릭했을 때, 새롭게 열린 페이지가 `window.opener.location` 객체를 조작하여 기존 부모 탭의 URL을 피싱 사이트로 몰래 변경함으로써 사용자의 계정 정보를 탈취하는 웹 공격 기술을 영문 또는 국문으로 쓰시오.",
        "answer": "탭내빙",
        "accepted_answers": ["탭내빙", "Tabnabbing", "탭 내빙", "리버스 탭내빙", "Reverse Tabnabbing"],
        "grading_mode": "normalized",
        "explanation": "탭내빙(Tabnabbing)은 target=\"_blank\" 링크를 클릭했을 때 새 창이 부모 탭의 location을 피싱 사이트로 변경하는 공격이며, rel=\"noopener\" 또는 rel=\"noreferrer\" 속성을 적용하여 방어합니다 (SRC-08 p.145).",
        "source_id": "SRC-08",
        "source_page": 145,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["탭내빙", "Tabnabbing", "웹보안", "피싱", "noopener"]
    },
    {
        "id": "Q-SHORT-093",
        "type": "short",
        "category": "애플리케이션 보안",
        "score": 3,
        "question": "MySQL 데이터베이스 설정 파일(`/etc/mysql/my.cnf`)에서 데이터베이스 서버 데몬(`mysqld`)이 특정 IP 인터페이스의 접속 요청만을 수신하도록 바인딩하는 지시자로서, 로컬 루프백(`127.0.0.1`)으로 설정될 경우 외부 네트워크로부터의 접근이 차단되는 지시자의 명칭을 쓰시오.",
        "answer": "bind-address",
        "accepted_answers": ["bind-address", "bind_address", "bindaddress"],
        "grading_mode": "strict",
        "explanation": "bind-address 설정은 MySQL 서버가 수신할 네트워크 주소를 바인딩하며, 127.0.0.1 설정 시 외부 접근이 차단됩니다 (SRC-08 p.244, 8회 기출).",
        "source_id": "SRC-08",
        "source_page": 244,
        "concept_id": "CON-APP-03",
        "difficulty": "easy",
        "tags": ["MySQL", "my.cnf", "bind-address", "DB보안"]
    },
    {
        "id": "Q-DESC-035",
        "type": "descriptive",
        "category": "애플리케이션 보안",
        "score": 12,
        "question": "웹 애플리케이션 취약점 중 크로스 사이트 요청 변조(CSRF; Cross-Site Request Forgery) 공격과 이에 대응하기 위한 보안 대책에 대하여 다음 물음에 답하시오.\n\n1) CSRF 공격의 개념과, 공격자가 피해자 브라우저의 어떤 인증 상태 메커니즘을 악용하는지 서술하시오. (4점)\n2) CSRF 공격을 방어하기 위한 대표적인 기법인 'CSRF 토큰(Token)' 검증 방식의 동작 원리를 서술하시오. (4점)\n3) CSRF 토큰 외에 웹 애플리케이션 및 브라우저 레벨에서 적용할 수 있는 추가적인 대응 방안 2가지를 서술하시오. (4점)",
        "model_answer": "1) CSRF 개념 및 메커니즘: 사용자가 로그인하여 유효한 세션 인증 쿠키를 브라우저에 보유한 상태에서, 공격자가 유도한 악성 페이지를 방문할 때 브라우저가 대상 웹사이트로 요청을 보낼 때 쿠키를 자동으로 포함시키는 특성을 악용하여, 사용자의 의도와 무관하게 공격자가 원하는 악의적 요청(비밀번호 변경, 이체 등)을 서버로 전송하여 실행시키는 공격이다.\n2) CSRF 토큰 원리: 서버는 사용자의 세션마다 예측 불가능한 임의의 고유 난수(CSRF 토큰)를 생성하여 폼(Hidden 필드)에 담아 전달하고, 클라이언트가 데이터 변경 요청을 전송할 때 제출된 토큰과 서버 세션에 저장된 토큰이 일치하는지 비교 검증하여 위조 요청을 차단한다.\n3) 추가 대응 방안:\n- 쿠키에 `SameSite` 속성(Strict 또는 Lax)을 설정하여 타 사이트로부터 시작된 요청 시 쿠키 전송 제한\n- HTTP 요청 헤더의 `Referer` 또는 `Origin` 헤더를 검증하여 신뢰된 도메인에서 발생한 요청인지 확인\n- 비밀번호 변경, 자금 이체 등 민감한 기능 수행 시 기존 패스워드 재입력(재인증) 또는 2차 인증 요구",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) CSRF 공격의 개념 및 브라우저 인증 악용 메커니즘",
                "model_answer": "로그인된 사용자의 브라우저가 요청 시 인증 쿠키를 자동 전송하는 점을 악용하여, 사용자 의지와 무관하게 공격자의 악의적 요청을 수행하게 만드는 공격이다.",
                "rubric": {
                    "keywords": [
                        ["의지와 무관", "의도와 무관", "자신의 의지"],
                        ["쿠키", "세션", "자동 첨부", "자동 전송", "인증 상태"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) CSRF 토큰 검증 메커니즘의 동작 원리",
                "model_answer": "서버 세션에 생성된 난수 토큰을 폼에 삽입하여 전달하고, 요청 시 전달된 토큰과 세션의 토큰이 일치하는지 비교 검증한다.",
                "rubric": {
                    "keywords": [
                        ["난수", "토큰", "csrf 토큰"],
                        ["세션", "hidden", "비교", "검증", "일치"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) CSRF 방어를 위한 추가 대응 대책 2가지",
                "model_answer": "SameSite 쿠키 속성 설정, Referer/Origin 헤더 검증, 중요 기능 재인증을 적용한다.",
                "rubric": {
                    "keywords": [
                        ["samesite", "samesite 속성", "쿠키 속성"],
                        ["referer", "origin", "재인증", "2차 인증", "도메인 검증"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "CSRF는 인증 쿠키 자동 전송을 악용하는 공격으로, CSRF 토큰, SameSite 쿠키, Referer 검증, 재인증으로 방어합니다 (SRC-08 p.110, 111).",
        "source_id": "SRC-08",
        "source_page": 110,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["CSRF", "SameSite", "CSRF토큰", "Referer", "웹보안"]
    },
    {
        "id": "Q-DESC-036",
        "type": "descriptive",
        "category": "애플리케이션 보안",
        "score": 12,
        "question": "리눅스 환경의 대표적인 웹 서버인 Apache의 설정 파일(`httpd.conf`)에 포함된 다음 4가지 핵심 지시자(Directive)의 기술적 의미와 역할을 각각 서술하시오.\n\n1) `Timeout 300`의 기술적 의미 (3점)\n2) `MaxKeepAliveRequests 100`의 기술적 의미 (3점)\n3) `DirectoryIndex index.htm index.html index.php`의 역할 (3점)\n4) `ErrorLog \"logs/error_log\"`의 역할 (3점)",
        "model_answer": "1) Timeout 300: 클라이언트와의 연결 수립 후 요청 메시지 수신 및 응답 전송 과정에서 패킷 송수신 간 서버가 기다리는 최대 대기 시간(초)을 설정하며, 300초(5분) 동안 패킷 송수신이 없으면 연결을 강제 종료한다.\n2) MaxKeepAliveRequests 100: HTTP 지속 연결(Keep-Alive) 세션이 활성화된 상태에서 동일한 연결을 재사용하여 처리할 수 있는 최대 요청 횟수를 100회로 제한한다.\n3) DirectoryIndex: 클라이언트가 특정 파일명이 아닌 디렉터리 경로 URL을 요청했을 때, 웹 서버가 우선순위에 따라 찾아 자동으로 반환할 기본 인덱스 문서 파일 목록을 지정한다.\n4) ErrorLog: 웹 서버 구동 중 발생하는 오류 메시지, 경고 및 진단 정보를 기록할 에러 로그 파일의 저장 경로를 지정한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) Timeout 지시자의 기술적 의미",
                "model_answer": "클라이언트 요청 및 응답 송수신 시 서버가 대기하는 최대 대기 시간(초)",
                "rubric": {
                    "keywords": [
                        ["대기 시간", "타임아웃", "송수신 대기", "최대 대기", "초"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) MaxKeepAliveRequests 지시자의 기술적 의미",
                "model_answer": "Keep-Alive 연결 유지 상태에서 하나의 연결로 처리할 수 있는 최대 요청 수",
                "rubric": {
                    "keywords": [
                        ["keep-alive", "지속 연결", "하나의 연결", "최대 요청", "100"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) DirectoryIndex 지시자의 역할",
                "model_answer": "디렉터리 요청 시 기본으로 반환할 인덱스 문서 파일 목록 및 우선순위 지정",
                "rubric": {
                    "keywords": [
                        ["디렉터리", "인덱스", "기본 문서", "우선순위", "반환"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) ErrorLog 지시자의 역할",
                "model_answer": "웹 서버의 에러 및 진단 메시지를 기록하는 로그 파일 경로 지정",
                "rubric": {
                    "keywords": [
                        ["에러 로그", "오류", "로그 파일", "경로"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "Apache 웹 서버의 핵심 설정 지시자(Timeout, MaxKeepAliveRequests, DirectoryIndex, ErrorLog)의 의미와 역할입니다 (SRC-08 p.168, 14회 기출).",
        "source_id": "SRC-08",
        "source_page": 168,
        "concept_id": "CON-APP-01",
        "difficulty": "medium",
        "tags": ["Apache", "httpd.conf", "Timeout", "KeepAlive", "웹서버설정"]
    },
    {
        "id": "Q-DESC-037",
        "type": "descriptive",
        "category": "애플리케이션 보안",
        "score": 12,
        "question": "다음은 웹 서버로 전송된 비정상적인 XML 요청 데이터이다. [XML 요청 데이터]를 분석하고 각 물음에 답하시오.\n\n[XML 요청 데이터]\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE foo [\n  <!ENTITY xxe SYSTEM \"file:///etc/passwd\">\n]>\n<foo>&xxe;</foo>\n\n1) 수행 중인 보안 취약점 공격의 명칭과 DTD 구문의 동작 원리를 서술하시오. (4점)\n2) 이 공격이 성공할 경우 발생할 수 있는 주요 보안 위협 2가지를 서술하시오. (4점)\n3) 애플리케이션 및 XML 파서 차원에서 이 공격을 원천 방어하기 위한 설정 대책을 서술하시오. (4점)",
        "model_answer": "1) 공격 명칭 및 동작 원리: XML 외부 개체 삽입(XXE; XML External Entity) 공격이다. XML 파서가 DTD를 해석할 때 `SYSTEM \"file:///etc/passwd\"` 지시자를 통해 로컬 시스템의 `/etc/passwd` 파일을 읽어들여 `xxe` 엔티티에 치환하고, 본문의 `&xxe;` 참조를 통해 파일 내용을 화면에 노출시킨다.\n2) 주요 보안 위협:\n- 서버 내부 중요 로컬 파일(설정 파일, 계정 정보, 소스코드 등)의 비인가 열람 및 유출\n- 서버를 경유하여 방화벽 내부의 다른 시스템을 스캔하거나 공격하는 서버 측 요청 위조(SSRF)\n- `http://` 스키마 등을 통한 내부망 포트 스캐닝 및 DoS(Billion Laughs XML 폭탄 공격)\n3) 방어 대책: 웹 애플리케이션에서 사용하는 XML 파서의 설정에서 외부 DTD 선언 및 외부 엔티티 파싱 기능(DPA / DTD 로딩)을 비활성화한다. (예: Java XML 파서에서 `disallow-doctype-decl` 속성을 true로 설정하거나 `external-general-entities`, `external-parameter-entities`를 false로 설정)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 공격 명칭 및 DTD 구문 동작 원리",
                "model_answer": "XXE 공격으로, DTD 외부 엔티티(SYSTEM) 선언을 통해 /etc/passwd 파일을 읽어 본문에 치환한다.",
                "rubric": {
                    "keywords": [
                        ["xxe", "xml 외부 엔티티", "xml external entity"],
                        ["외부 엔티티", "system", "/etc/passwd", "치환", "파싱"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) XXE 성공 시 발생 가능한 보안 위협 2가지",
                "model_answer": "서버 내부 파일 유출, 내부망 스캔 및 SSRF 공격, 서비스 거부(DoS) 유발",
                "rubric": {
                    "keywords": [
                        ["파일 유출", "파일 열람", "내부 파일"],
                        ["ssrf", "내부망 스캔", "포트 스캔", "dos"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) XML 파서 레벨의 원천 방어 대책",
                "model_answer": "XML 파서의 외부 DTD 및 외부 엔티티 참조 기능을 비활성화한다.",
                "rubric": {
                    "keywords": [
                        ["외부 dtd", "외부 엔티티", "dtd 비활성화", "비활성화", "disallow-doctype-decl"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "XXE 취약점은 DTD 외부 엔티티를 악용하여 파일을 유출하며, XML 파서의 외부 DTD 참조 기능을 비활성화하여 방어합니다 (SRC-08 p.137, 169, 16회 기출).",
        "source_id": "SRC-08",
        "source_page": 169,
        "concept_id": "CON-APP-01",
        "difficulty": "hard",
        "tags": ["XXE", "XML", "취약점", "SSRF", "파서보안"]
    },
    {
        "id": "Q-PRAC-020",
        "type": "practical",
        "category": "애플리케이션 보안",
        "score": 16,
        "question": "다음은 웹 서버로 유입된 특정 요청 URL과 이에 대응하는 [IIS 웹로그]의 일부이다. 로그를 분석하고 각 질문에 답하시오.\n\n[요청 URL]\nhttp://test.com/login.asp?password='orid='admin';--\n\n[IIS 웹로그]\n#Fields: date time cs-method cs-uri-stem cs-uri-query s-port c-ip cs(User-Agent) sc-status sc-substatus sc-win32-status time-taken\n2025-01-01 12:00:00 GET /login.asp password='or id='admin';-- 80 192.168.1.10 Mozilla/5.0 200 0 0 141\n\n1) 로그에서 시도된 웹 해킹 공격 기법의 명칭을 쓰시오. (4점)\n2) 공격자가 전달한 쿼리 파라미터 `password='or id='admin';--`가 백엔드 데이터베이스에서 인증을 우회시키는 원리를 쿼리 로직 관점에서 구체적으로 서술하시오. (6점)\n3) 이 취약점을 소스코드 레벨에서 원천 방어하기 위한 개발 보안 구현 원칙 2가지를 서술하시오. (6점)",
        "model_answer": "1) 공격 기법 명칭: SQL 인젝션 (SQL Injection; SQL 삽입)\n2) 인증 우회 원리:\n- 백엔드에서 `SELECT * FROM users WHERE id='$id' AND password='$password'`와 같이 동적으로 문자열을 연결하여 SQL 문을 생성하는 경우\n- 입력값 `password`에 `' or id='admin';--`가 삽입되면 WHERE 절이 `WHERE id='...' AND password='' or id='admin';--'` 형태로 변조된다.\n- `--` 이후의 구문은 주석으로 처리되어 비밀번호 검증 조건이 무효화되고, `OR id='admin'` 조건이 참이 되면서 패스워드 일치 여부와 상관없이 최고관리자(admin) 계정으로 인증이 우회된다.\n3) 개발 보안 구현 원칙:\n- 정적 파라미터화된 쿼리(Prepared Statement)를 사용하여 사용자 입력값이 쿼리 구조(문법)를 변경하지 못하고 순수 데이터 파라미터로만 바인딩되도록 구현\n- 사용자 입력값에 대해 특수문자(', \", ;, --, # 등) 및 SQL 예약어를 필터링하거나 화이트리스트 기반의 유효성 검증(Validation) 수행\n- 웹방화벽(WAF)을 적용하여 SQL 구문 조작 패턴 차단 및 DB 계정의 권한 최소화 적용",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) 시도된 웹 해킹 공격 기법의 명칭",
                "model_answer": "SQL 인젝션 (SQL Injection; SQL 삽입)",
                "rubric": {
                    "keywords": [
                        ["sql 인젝션", "sql injection", "sql 삽입", "sqli"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 6,
                "prompt": "2) SQL 쿼리 로직 관점에서의 인증 우회 원리",
                "model_answer": "OR 조건으로 인해 password 검증이 무력화되고 주석문(--)으로 뒷부분이 무시되어 admin으로 인증 우회된다.",
                "rubric": {
                    "keywords": [
                        ["or 조건", "or id='admin'", "or id"],
                        ["주석", "--", "비밀번호 검증 무력화", "패스워드 검증 무력화", "인증 우회"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 3,
                "score": 6,
                "prompt": "3) 소스코드 레벨 원천 방어를 위한 개발 보안 원칙 2가지",
                "model_answer": "Prepared Statement(파라미터화된 쿼리) 적용, 특수문자 입력값 검증(화이트리스트 필터링)",
                "rubric": {
                    "keywords": [
                        ["prepared statement", "파라미터화된 쿼리", "바인딩", "preparedStatement"],
                        ["입력값 검증", "특수문자 필터링", "화이트리스트", "waf", "최소 권한"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ],
        "explanation": "IIS 웹로그의 `password='or id='admin';--`는 SQL Injection을 통한 관리자 로그인 우회 시도이며, Prepared Statement로 방어합니다 (SRC-08 p.163, 2회 기출).",
        "source_id": "SRC-08",
        "source_page": 163,
        "concept_id": "CON-APP-01",
        "difficulty": "hard",
        "tags": ["SQL인젝션", "로그분석", "IIS로그", "PreparedStatement", "인증우회"]
    }
]
