import json
import os

EXPANDED_SHORT = [
  {
    "id": "Q-SHORT-013",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-MGT-01",
    "source_id": "SRC-01",
    "source_page": 7,
    "question": "위험관리 3단계에 대한 설명이다. ( )에 들어갈 단계명을 기술하시오.\n\n( A ) : 자산의 위협과 취약점을 분석하여 보안 위험의 종류와 규모를 결정하는 과정\n( B ) : 식별된 자산, 위협 및 취약점을 기준으로 위험도를 산출하여 기존의 보호대책을 파악하고 위험의 대응 여부와 우선순위를 결정하기 위한 평가 과정\n(대책 선정) : 허용가능 수준으로 위험을 줄이기 위해 적절하고 정당한 정보보호 대책을 선정하고 이행 계획을 수립하는 과정",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "위험분석",
        "accepted_answers": ["위험분석", "위험 분석", "Risk Analysis"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "위험평가",
        "accepted_answers": ["위험평가", "위험 평가", "Risk Evaluation"]
      }
    ],
    "explanation": "위험관리의 핵심 3단계는 자산의 위협/취약점을 식별하는 위험분석(Risk Analysis), 위험도를 산출하고 우선순위를 결정하는 위험평가(Risk Evaluation), 그리고 적절한 보호대책을 수립하는 대책선정 단계로 구성됩니다.",
    "difficulty": "medium",
    "tags": ["위험관리", "위험분석", "위험평가"]
  },
  {
    "id": "Q-SHORT-014",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 7,
    "question": "라우팅 프로토콜에 대한 설명이다. ( )에 들어갈 프로토콜명을 기술하시오.\n\n( A ) : 거리 벡터(Distance Vector) 알고리즘을 사용하며, Bellman-Ford 기반의 가장 오래되고 널리 사용되는 내부 라우팅 프로토콜\n( B ) : 링크 상태(Link State) 알고리즘을 사용하며, 다익스트라(Dijkstra) 기반으로 변화시에만 라우팅 정보를 교환하는 내부 라우팅 프로토콜\n( C ) : 시스코에서 제안하였으며 거리벡터와 링크상태의 장점을 수용한 고급 거리벡터(하이브리드) 라우팅 프로토콜",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "RIP",
        "accepted_answers": ["RIP", "Routing Information Protocol"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "OSPF",
        "accepted_answers": ["OSPF", "Open Shortest Path First"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "EIGRP",
        "accepted_answers": ["EIGRP", "Enhanced Interior Gateway Routing Protocol"]
      }
    ],
    "explanation": "내부 라우팅 프로토콜(IGP) 중 거리벡터 방식은 RIP, 링크상태 방식은 OSPF, 시스코 독자의 하이브리드(고급 거리벡터) 방식은 EIGRP입니다.",
    "difficulty": "low",
    "tags": ["라우팅", "RIP", "OSPF", "EIGRP"]
  },
  {
    "id": "Q-SHORT-015",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 7,
    "question": "유닉스/리눅스의 주요 로그 파일에 대한 설명이다. ( )에 들어갈 로그 파일명을 기술하시오 (경로는 생략 가능).\n\n( A ) : 사용자의 가장 최근 로그인 시각 및 접속 호스트 정보가 바이너리 형태로 기록되는 로그 파일\n( B ) : su(Switch User) 명령어를 통한 사용자 계정 권한 변경(성공 및 실패) 내역이 기록되는 로그 파일\n( C ) : 시스템에 로그인한 모든 사용자가 실행한 명령어, 시작 시간, CPU 사용량 정보가 기록되는 프로세스 계정 로그 파일",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "lastlog",
        "accepted_answers": ["lastlog", "/var/log/lastlog"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "sulog",
        "accepted_answers": ["sulog", "/var/log/sulog"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "pacct",
        "accepted_answers": ["pacct", "acct", "acct/pacct", "/var/account/pacct"]
      }
    ],
    "explanation": "유닉스 시스템 로그: lastlog(최근 로그인), sulog(su 변경 내역), pacct/acct(사용자가 실행한 명령어 추적).",
    "difficulty": "medium",
    "tags": ["로그분석", "lastlog", "sulog", "pacct"]
  },
  {
    "id": "Q-SHORT-016",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 8,
    "question": "리눅스 /etc/passwd 파일에 등록된 한 줄의 설정이다. 각 필드가 의미하는 바를 기술하시오.\n\ntest01:x:100:1000:/home/exam:/bin/bash\n\n1) 1000 : ( A )\n2) /home/exam : ( B )\n3) /bin/bash : ( C )",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "GID",
        "accepted_answers": ["GID", "그룹 ID", "그룹ID", "기본 그룹 ID", "그룹 식별자"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "홈 디렉터리",
        "accepted_answers": ["홈 디렉터리", "홈 디렉토리", "홈디렉터리", "사용자 홈 디렉터리", "홈디렉토리"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "로그인 셸",
        "accepted_answers": ["로그인 셸", "로그인 쉘", "로그인쉘", "기본 셸", "기본 쉘"]
      }
    ],
    "explanation": "/etc/passwd의 7개 필드는 '사용자명:패스워드(x):UID:GID:코멘트(GECOS):홈디렉터리:기본로그인셸' 순서로 정의됩니다.",
    "difficulty": "low",
    "tags": ["리눅스", "passwd", "계정관리"]
  },
  {
    "id": "Q-SHORT-017",
    "type": "short",
    "category": "애플리케이션 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-APP-01",
    "source_id": "SRC-01",
    "source_page": 8,
    "question": "HTTP Request 입력값에 개행 문자가 포함되어 서버의 HTTP 응답 헤더가 2개 이상으로 분리되는 HTTP 응답 분할(HTTP Response Splitting) 취약점이 발생한다. 공격자가 사용하는 대표적인 2가지 개행 문자의 영문 약어(또는 이스케이프 문자)를 기술하시오.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "CR",
        "accepted_answers": ["CR", "\\r", "%0D", "Carriage Return", "CarriageReturn"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "LF",
        "accepted_answers": ["LF", "\\n", "%0A", "Line Feed", "LineFeed"]
      }
    ],
    "explanation": "HTTP 프로토콜 헤더는 CRLF(\\r\\n, %0D%0A)로 헤더와 바디 또는 각 헤더 필드를 구분하므로, 입력값에 CR과 LF가 필터링되지 않으면 응답 분할 공격에 노출됩니다.",
    "difficulty": "medium",
    "tags": ["HTTP", "CRLF", "개행문자", "웹보안"]
  },
  {
    "id": "Q-SHORT-018",
    "type": "short",
    "category": "애플리케이션 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-APP-01",
    "source_id": "SRC-01",
    "source_page": 8,
    "question": "PHP 기반 원격 파일 삽입(RFI/LFI) 취약점을 예방하기 위한 조치이다. ( )에 들어갈 적절한 값을 기술하시오.\n\n1) 소스코드 내 외부 입력값이 직접 전달되는 ( A ) 계열 함수 호출 검증\n2) PHP 환경설정 파일인 ( B )에서 원격 파일 include를 차단하기 위해 allow_url_fopen 및 allow_url_include 지시자 값을 ( C )로 설정",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "include",
        "accepted_answers": ["include", "require", "include_once", "require_once"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "php.ini",
        "accepted_answers": ["php.ini", "PHP.ini"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "Off",
        "accepted_answers": ["Off", "off", "OFF"]
      }
    ],
    "explanation": "PHP 파일 삽입 취약점은 include/require 함수에 동적 파라미터가 바인딩될 때 발생하며, php.ini에서 allow_url_fopen = Off, allow_url_include = Off 설정을 통해 원격 파일 삽입(RFI)을 원천 방어합니다.",
    "difficulty": "medium",
    "tags": ["PHP", "RFI", "php.ini", "allow_url_fopen"]
  },
  {
    "id": "Q-SHORT-019",
    "type": "short",
    "category": "네트워크/보안운영",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-NET-02",
    "source_id": "SRC-01",
    "source_page": 8,
    "question": "Snort IDS에서 대량의 패킷 로그를 제어하기 위해 사용하는 threshold 옵션의 세부 type 3가지를 기술하시오.\n\n구문 형식: threshold: type < (A) | (B) | (C) >, track <by_src | by_dst>, count <c>, seconds <s>",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "threshold",
        "accepted_answers": ["threshold"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "limit",
        "accepted_answers": ["limit"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "both",
        "accepted_answers": ["both"]
      }
    ],
    "explanation": "Snort threshold type: limit(s초 동안 c번째까지 액션 수행), threshold(s초 동안 c번째마다 액션 반복), both(s초 동안 c번째 발생 시 1회만 액션 수행).",
    "difficulty": "medium",
    "tags": ["Snort", "Threshold", "침입탐지"]
  },
  {
    "id": "Q-SHORT-020",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "strict",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 9,
    "question": "이더넷 환경에서 상대방의 IP 주소는 알지만 MAC 주소를 모를 때 전송하는 ARP Request 브로드캐스트 프레임의 목적지 MAC(Hardware) 주소를 표준 형식으로 기술하시오.",
    "answer": "FF:FF:FF:FF:FF:FF",
    "accepted_answers": ["FF:FF:FF:FF:FF:FF", "ff:ff:ff:ff:ff:ff", "FF-FF-FF-FF-FF-FF"],
    "sub_questions": None,
    "explanation": "ARP 요청은 동일 서브넷의 모든 호스트에 전파되어야 하므로 이더넷 브로드캐스트 MAC 주소인 FF:FF:FF:FF:FF:FF를 목적지 주소로 사용합니다.",
    "difficulty": "low",
    "tags": ["ARP", "MAC", "브로드캐스트"]
  },
  {
    "id": "Q-SHORT-021",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 9,
    "question": "DNS(Domain Name System) 서비스의 특성에 대한 설명이다. ( )에 들어갈 용어를 기술하시오.\n\n1) DNS는 53번 포트를 기본 사용하며 일반 질의에는 주로 ( A ) 전송 계층 프로토콜을 사용한다.\n2) DNS 서버는 반복적인 외부 질의 부하를 줄이기 위해 조회된 레코드를 로컬의 ( B )에 임시 저장한다.\n3) ( B )에 저장된 정보가 소멸되지 않고 유지되는 유효 기간을 의미하는 헤더 필드는 ( C )이다.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "UDP",
        "accepted_answers": ["UDP", "UDP/TCP", "UDP 53"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "캐시",
        "accepted_answers": ["캐시", "Cache", "DNS 캐시", "DNS Cache"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "TTL",
        "accepted_answers": ["TTL", "Time To Live", "Time-To-Live"]
      }
    ],
    "explanation": "DNS는 포트 53번으로 동작하며 일반 질의는 빠른 응답의 UDP를 사용하고, 캐시(Cache)에 저장하여 재사용하며, 이 캐시의 생존 시간은 TTL(Time To Live)에 의해 관리됩니다.",
    "difficulty": "low",
    "tags": ["DNS", "UDP", "TTL", "캐시"]
  },
  {
    "id": "Q-SHORT-022",
    "type": "short",
    "category": "애플리케이션 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-APP-04",
    "source_id": "SRC-01",
    "source_page": 33,
    "question": "소프트웨어 보안 취약점 점검 방식에 대한 설명이다. ( )에 들어갈 테스트 명칭을 기술하시오.\n\n( A ) : 애플리케이션의 소스코드를 보지 않고, 외부 인터페이스 및 입력값에 따른 응답 결과를 분석하여 취약점을 점검하는 동적/블라인드 분석 방식\n( B ) : 개발된 소스코드를 직접 열람하고 제어 흐름 및 데이터 흐름을 추적하여 코딩 상의 보안 약점을 찾아내는 정적 분석 방식",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "블랙박스 테스트",
        "accepted_answers": ["블랙박스 테스트", "Blackbox", "Black-box", "블랙박스", "블랙박스 점검"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "화이트박스 테스트",
        "accepted_answers": ["화이트박스 테스트", "Whitebox", "White-box", "화이트박스", "화이트박스 점검"]
      }
    ],
    "explanation": "내부 코드를 보지 않는 인터페이스/동적 점검은 블랙박스 테스트(Blackbox Testing), 내부 소스코드를 분석하는 정적 점검은 화이트박스 테스트(Whitebox Testing)입니다.",
    "difficulty": "low",
    "tags": ["시큐어코딩", "블랙박스", "화이트박스"]
  },
  {
    "id": "Q-SHORT-023",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-LAW-01",
    "source_id": "SRC-01",
    "source_page": 10,
    "question": "개인정보의 안전성 확보조치 기준에 따른 접속기록 보관 기준이다. ( )에 들어갈 기준치를 기술하시오.\n\n개인정보처리자는 개인정보취급자가 개인정보처리시스템에 접속한 기록을 ( A ) 이상 보관·관리하여야 한다. 다만, ( B ) 이상의 정보주체에 관하여 개인정보를 처리하거나, 고유식별정보 또는 ( C )를 처리하는 시스템의 경우에는 2년 이상 보관·관리하여야 한다.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "1년",
        "accepted_answers": ["1년", "1년 이상", "1 년"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "5만명",
        "accepted_answers": ["5만명", "5만 명", "50000명", "50,000명", "5만"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "민감정보",
        "accepted_answers": ["민감정보", "민감 정보"]
      }
    ],
    "explanation": "개인정보보호법상 접속기록은 기본 1년 이상 보관해야 하며, 5만 명 이상의 정보주체 정보를 처리하거나 고유식별정보/민감정보를 처리하는 시스템은 2년 이상 보관해야 합니다.",
    "difficulty": "medium",
    "tags": ["개인정보보호법", "접속기록", "민감정보"]
  },
  {
    "id": "Q-SHORT-024",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-MGT-01",
    "source_id": "SRC-01",
    "source_page": 10,
    "question": "위험관리 및 정보보호 대책과 관련된 용어 설명이다. ( )에 들어갈 용어를 기술하시오.\n\n( A ) : 자산에 존재하는 위협과 취약성으로 인해 발생할 수 있는 손실을 줄이기 위해 적용하는 관리적, 물리적, 기술적 수단\n( B ) : ( A )를 적용하고 통제한 후에도 완전히 제거되지 않고 여전히 남아있는 위험\n( C ) : 조직이 감당할 수 있다고 경영진이 공식적으로 승인한 허용 가능한 위험 수준(Degree of Assurance)",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "보호대책",
        "accepted_answers": ["보호대책", "보호 대책", "정보보호대책", "보안대책"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "잔여 위험",
        "accepted_answers": ["잔여 위험", "잔여위험", "Residual Risk", "잔존위험"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "DoA",
        "accepted_answers": ["DoA", "DOA", "허용 가능한 위험 수준", "위험수용수준"]
      }
    ],
    "explanation": "보호대책을 적용한 후에도 남는 위험을 잔여 위험(Residual Risk)이라 하며, 이 잔여 위험이 조직의 허용 위험 수준(DoA) 이하가 되도록 관리해야 합니다.",
    "difficulty": "medium",
    "tags": ["위험관리", "잔여위험", "DoA", "보호대책"]
  },
  {
    "id": "Q-SHORT-025",
    "type": "short",
    "category": "애플리케이션 보안",
    "score": 3,
    "grading_mode": "strict",
    "concept_id": "CON-APP-02",
    "source_id": "SRC-01",
    "source_page": 10,
    "question": "Sendmail 메일 서버에서 스팸 릴레이 방지를 위해 텍스트 파일인 /etc/mail/access를 바이너리 DB 형태인 access.db로 변환 생성하는 명령어의 ( A )와 ( B )에 들어갈 키워드를 기술하시오.\n\n# ( A ) ( B ) /etc/mail/access.db < /etc/mail/access",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "makemap",
        "accepted_answers": ["makemap"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "hash",
        "accepted_answers": ["hash"]
      }
    ],
    "explanation": "Sendmail의 access 제어 파일은 Berkeley DB 해시 형식으로 컴파일되어야 적용되므로 'makemap hash /etc/mail/access.db < /etc/mail/access' 명령을 사용합니다.",
    "difficulty": "high",
    "tags": ["Sendmail", "makemap", "access.db", "메일보안"]
  },
  {
    "id": "Q-SHORT-026",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-MGT-01",
    "source_id": "SRC-01",
    "source_page": 11,
    "question": "업무 연속성 계획(BCP) 5단계 중 조직의 핵심 비즈니스 기능이 중단되었을 때 발생할 재정적·운영적 손실 규모를 정량적/정성적으로 분석하고 목표 복구 시간(RTO)과 목표 복구 시점(RPO)을 도출하는 2단계의 영문 약어(또는 명칭)를 기술하시오.",
    "answer": "BIA",
    "accepted_answers": ["BIA", "Business Impact Analysis", "비즈니스 영향 분석", "업무 영향 분석", "업무영향분석"],
    "sub_questions": None,
    "explanation": "BIA(Business Impact Analysis)는 재해 발생 시 각 비즈니스 프로세스 중단이 미치는 영향을 평가하여 핵심 복구 우선순위와 RTO/RPO를 산정하는 BCP의 핵심 단계입니다.",
    "difficulty": "low",
    "tags": ["BCP", "BIA", "RTO", "RPO"]
  },
  {
    "id": "Q-SHORT-027",
    "type": "short",
    "category": "정보보안 일반 및 암호학",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SEC-01",
    "source_id": "SRC-01",
    "source_page": 11,
    "question": "특정 기업이나 정부 조직 등 명확한 대상을 표적으로 삼아 제로데이 취약점, 스피어 피싱, 소셜 엔지니어링 등 다양한 기법을 동원하여 은밀하게 장기간에 걸쳐 지속적으로 침투 및 정보 탈취를 수행하는 고도화된 사이버 공격 형태를 무엇이라 하는가?",
    "answer": "APT",
    "accepted_answers": ["APT", "Advanced Persistent Threat", "지능형 지속 위협", "지능형지속위협"],
    "sub_questions": None,
    "explanation": "APT(Advanced Persistent Threat)는 명확한 대상을 지정하고 지속적(Persistent)으로 다양한 지능형(Advanced) 공격 기법을 결합하여 침투하는 위협입니다.",
    "difficulty": "low",
    "tags": ["APT", "지능형지속위협", "사이버공격"]
  },
  {
    "id": "Q-SHORT-028",
    "type": "short",
    "category": "정보보안 일반 및 암호학",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-CRY-01",
    "source_id": "SRC-01",
    "source_page": 12,
    "question": "네트워크 3계층(IP 계층)에서 종단 간 안전한 통신을 제공하는 표준 VPN 프로토콜인 IPSec의 구성 요소에 대한 설명이다. ( )에 들어갈 프로토콜 약어를 기술하시오.\n\n1) ( A ) : IP 계층 보안 표준 프로토콜 전체 체계\n2) ( B ) : 패킷의 송신처 인증과 데이터 무결성만을 제공하며, 데이터 자체의 암호화(기밀성)는 제공하지 않는 프로토콜 헤더\n3) ( C ) : 데이터 암호화(기밀성), 송신처 인증, 데이터 무결성을 모두 제공하는 프로토콜 헤더",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "IPSec",
        "accepted_answers": ["IPSec", "IPsec", "IP Security"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "AH",
        "accepted_answers": ["AH", "Authentication Header"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "ESP",
        "accepted_answers": ["ESP", "Encapsulating Security Payload"]
      }
    ],
    "explanation": "IPSec에서 AH는 인증/무결성(기밀성 제외)을 제공하고, ESP는 기밀성(암호화)+인증+무결성을 모두 지원합니다.",
    "difficulty": "medium",
    "tags": ["IPSec", "AH", "ESP", "VPN", "암호학"]
  },
  {
    "id": "Q-SHORT-029",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 12,
    "question": "버퍼 오버플로우(Buffer Overflow) 공격 기법과 관련된 설명이다. ( )에 들어갈 용어를 기술하시오.\n\n( A ) : 공격자가 메모리에 주입하여 관리자 셸 권한을 획득하도록 기계어로 작성된 명령 코드 집합\n( B ) : CPU가 아무런 동작도 수행하지 않고 다음 명령어로 넘어가도록 하는 x86 어셈블리 1바이트 기계어 코드(Hex)\n( C ) : 스택 포인터 레지스터(ESP)에 담긴 셸코드로 실행 제어권을 넘기기 위해 반환 주소(RET)에 덮어쓰는 대표적인 간접 점프 명령어",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "셸코드",
        "accepted_answers": ["셸코드", "쉘코드", "Shellcode", "Shell code"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "0x90",
        "accepted_answers": ["0x90", "0X90", "NOP", "nop"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "JMP ESP",
        "accepted_answers": ["JMP ESP", "CALL ESP", "jmp esp", "call esp"]
      }
    ],
    "explanation": "버퍼 오버플로우는 RET 주소를 'JMP ESP'와 같은 명령어 주소로 덮어쓰고, NOP Sled(0x90)를 타고 내려와 셸코드(Shellcode)를 실행시키는 기법을 사용합니다.",
    "difficulty": "medium",
    "tags": ["BoF", "셸코드", "0x90", "JMP ESP"]
  },
  {
    "id": "Q-SHORT-030",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "strict",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 6,
    "question": "Salvatore Sanfilippo가 개발한 네트워크 보안 진단 툴로 TCP, UDP, ICMP 등 다양한 프로토콜의 패킷을 조작하여 방화벽 룰 테스트 및 대량의 DDoS 공격 트래픽 생성 훈련에 사용하는 도구의 명칭은 무엇인가?",
    "answer": "hping3",
    "accepted_answers": ["hping3", "hping"],
    "sub_questions": None,
    "explanation": "hping3은 패킷 생성 및 분석 도구로, 임의의 플래그를 설정한 SYN 패킷을 초당 수만 개 생성하여 SYN Flooding 등 방화벽 성능 테스트에 자주 활용됩니다.",
    "difficulty": "low",
    "tags": ["hping3", "DDoS", "패킷도구"]
  },
  {
    "id": "Q-SHORT-031",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 6,
    "question": "시스템 보안 진단 도구에 대한 설명이다. ( )에 들어갈 도구명 또는 보안 특성을 기술하시오.\n\n1) Tripwire는 주요 시스템 파일의 해시값을 미리 생성하여 변경 여부를 감시하는 ( A ) 점검 도구이다.\n2) Tenable사에서 개발한 ( B )는 네트워크에 연결된 다양한 호스트와 포트를 자동으로 스캔하고 방대한 취약점 DB를 기반으로 점검 리포트를 제공하는 대표적인 취약점 스캐너이다.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "무결성",
        "accepted_answers": ["무결성", "파일 무결성", "무결성 검증", "Integrity"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "Nessus",
        "accepted_answers": ["Nessus", "NESSUS", "네서스"]
      }
    ],
    "explanation": "Tripwire는 파일 무결성(Integrity) 모니터링 도구이며, Nessus는 종합 자동 취약점 진단 스캐너입니다.",
    "difficulty": "low",
    "tags": ["Tripwire", "Nessus", "무결성", "취약점스캔"]
  },
  {
    "id": "Q-SHORT-032",
    "type": "short",
    "category": "정보보안 일반 및 암호학",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-CRY-01",
    "source_id": "SRC-01",
    "source_page": 6,
    "question": "OpenSSL의 TLS 하트비트(Heartbeat) 확장 규격에서 요청 메시지의 페이로드 길이 검증 누락으로 인해, 서버 메모리에 존재하는 최대 64KB의 개인키, 세션 쿠키, 계정 정보가 평문으로 유출되는 심각한 취약점(CVE-2014-0160)의 명칭은 무엇인가?",
    "answer": "하트블리드",
    "accepted_answers": ["하트블리드", "하트 블리드", "Heartbleed", "HeartBleed"],
    "sub_questions": None,
    "explanation": "Heartbleed(하트블리드, CVE-2014-0160)는 OpenSSL 라이브러리에서 발생한 바운드 검사 누락으로 메모리 중요 정보가 유출되는 대표적 취약점입니다.",
    "difficulty": "low",
    "tags": ["하트블리드", "Heartbleed", "OpenSSL", "CVE-2014-0160"]
  },
  {
    "id": "Q-SHORT-033",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 5,
    "question": "리눅스 ELF 바이너리의 동적 링킹(Dynamic Linking) 메커니즘에 대한 설명이다. ( )에 들어갈 테이블 명칭을 기술하시오.\n\n프로그램 실행 시 외부 공유 라이브러리 함수의 실제 메모리 주소를 연결하기 위해 함수 호출 시 거치는 점프 테이블인 ( A )를 참조하고, ( A )는 실제 함수의 절대 주소가 런타임에 동적으로 바인딩되어 저장되는 테이블인 ( B )를 참조하여 실행한다.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1.5,
        "answer": "PLT",
        "accepted_answers": ["PLT", "Procedure Linkage Table"]
      },
      {
        "label": "B",
        "score": 1.5,
        "answer": "GOT",
        "accepted_answers": ["GOT", "Global Offset Table"]
      }
    ],
    "explanation": "리눅스 동적 바이너리는 PLT(Procedure Linkage Table)를 호출하고, PLT는 GOT(Global Offset Table)에 적재된 동적 링커가 해결한 실제 라이브러리 함수 주소로 점프합니다.",
    "difficulty": "medium",
    "tags": ["리눅스", "PLT", "GOT", "동적링킹"]
  },
  {
    "id": "Q-SHORT-034",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-LAW-01",
    "source_id": "SRC-01",
    "source_page": 5,
    "question": "정보보호 및 개인정보보호 관리체계(ISMS-P) 인증 기준의 3개 영역 명칭을 기술하시오.",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "관리체계 수립 및 운영",
        "accepted_answers": ["관리체계 수립 및 운영", "관리체계수립및운영", "관리체계 수립 운영"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "보호대책 요구사항",
        "accepted_answers": ["보호대책 요구사항", "보호대책요구사항", "보호대책"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "개인정보 처리 단계별 요구사항",
        "accepted_answers": ["개인정보 처리 단계별 요구사항", "개인정보처리단계별요구사항", "개인정보 처리단계별 요구사항"]
      }
    ],
    "explanation": "ISMS-P 인증 기준은 1. 관리체계 수립 및 운영(16개), 2. 보호대책 요구사항(64개), 3. 개인정보 처리 단계별 요구사항(22개) 총 102개 항목으로 구성됩니다.",
    "difficulty": "medium",
    "tags": ["ISMS-P", "인증기준", "보호대책"]
  },
  {
    "id": "Q-SHORT-035",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "strict",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 4,
    "question": "리눅스 xinetd 수퍼데몬 서비스 설정 파일(/etc/xinetd.d/telnet 등)의 지시자이다. ( )에 들어갈 정확한 지시자명을 기술하시오.\n\n1) ( A ) = 10.0.0.0/8 # 특정 IP/네트워크의 접근을 차단하는 지시자\n2) ( B ) = 192.168.10.0/24 # 특정 IP/네트워크의 접근만을 허용하는 지시자\n3) ( C ) = 3 # 동시에 실행될 수 있는 최대 데몬 인스턴스(세션) 수를 제한하는 지시자",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "no_access",
        "accepted_answers": ["no_access"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "only_from",
        "accepted_answers": ["only_from"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "instances",
        "accepted_answers": ["instances"]
      }
    ],
    "explanation": "xinetd 설정 지시자: no_access(접근 금지 호스트 목록), only_from(접근 허용 호스트 목록), instances(동시 접속 가능한 최대 데몬 세션 수).",
    "difficulty": "medium",
    "tags": ["xinetd", "no_access", "only_from", "instances"]
  },
  {
    "id": "Q-SHORT-036",
    "type": "short",
    "category": "정보보호 관리 및 법규",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-LAW-01",
    "source_id": "SRC-01",
    "source_page": 3,
    "question": "개인정보 가명·익명처리 기법 중 나이, 소득 등의 수치형 데이터를 올림이나 내림을 적용할 때 정해진 규칙 대신 무작위 난수나 확률적 기준을 적용하여 편향을 줄이고 원래 값을 유추하기 어렵게 만드는 기법의 명칭은 무엇인가?",
    "answer": "랜덤 라운딩",
    "accepted_answers": ["랜덤 라운딩", "랜덤라운딩", "Random Rounding", "확률적 라운딩"],
    "sub_questions": None,
    "explanation": "랜덤 라운딩(Random Rounding)은 통계적 왜곡을 방지하면서 특정 레코드의 실제 수치를 식별하지 못하도록 확률적으로 자리올림/내림을 처리하는 가명처리 기법입니다.",
    "difficulty": "medium",
    "tags": ["가명처리", "익명처리", "랜덤라운딩"]
  }
]

EXPANDED_DESC = [
  {
    "id": "Q-DESC-005",
    "type": "descriptive",
    "category": "네트워크 보안",
    "score": 12,
    "concept_id": "CON-NET-01",
    "source_id": "SRC-02",
    "source_page": 3,
    "question": "네트워크 장비 모니터링을 위해 SNMP(Simple Network Management Protocol) 서비스를 운영할 때 반드시 적용해야 하는 보안 강화 조치 4가지를 서술하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 3,
        "prompt": "1) 커뮤니티 스트링(Community String) 보안 설정 방안을 서술하시오.",
        "model_answer": "공장 출하 시 설정된 public, private 등 기본(Default) 커뮤니티 스트링을 유추하기 어려운 복잡한 문자열로 변경한다.",
        "rubric": {
          "keywords": [
            ["기본값", "default", "초기값", "공장", "public", "private"],
            ["변경", "수정", "유추", "복잡도", "강화"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 2,
        "score": 3,
        "prompt": "2) SNMP 프로토콜 버전 선택 관점에서의 보안 권장사항을 서술하시오.",
        "model_answer": "평문 전송되는 SNMPv1, v2c 대신 사용자 인증과 패킷 암호화가 기본 지원되는 SNMPv3을 사용한다.",
        "rubric": {
          "keywords": [
            ["snmpv3", "snmp v3", "v3"],
            ["암호화", "인증", "보안"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 3,
        "score": 3,
        "prompt": "3) 네트워크 접근통제 관점에서의 설정 방안을 서술하시오.",
        "model_answer": "ACL(Access Control List)이나 방화벽 정책을 적용하여 사전에 인가된 NMS(관리 서버) IP에서만 SNMP 포트(UDP 161/162)로 접근할 수 있도록 제한한다.",
        "rubric": {
          "keywords": [
            ["acl", "access control list", "접근제어", "방화벽"],
            ["nms", "관리 서버", "관리자", "ip 제한", "호스트 제한"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 4,
        "score": 3,
        "prompt": "4) SNMP 권한(모드) 부여 관점에서의 보안 설정 방안을 서술하시오.",
        "model_answer": "원격 장비 설정 변경이 가능한 RW(Read-Write) 모드를 비활성화 또는 삭제하고 모니터링만 가능한 RO(Read-Only) 모드로 운영한다.",
        "rubric": {
          "keywords": [
            ["ro", "read-only", "읽기 전용", "읽기전용"],
            ["rw", "read-write", "쓰기", "비활성화", "삭제", "제거"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      }
    ],
    "explanation": "SNMP 보안의 4대 원칙은 1) Community String 복잡화, 2) 암호화 지원 SNMPv3 도입, 3) ACL을 통한 NMS IP 제한, 4) RO 모드 전용 운용입니다.",
    "difficulty": "medium",
    "tags": ["SNMP", "네트워크보안", "ACL", "SNMPv3"]
  },
  {
    "id": "Q-DESC-006",
    "type": "descriptive",
    "category": "네트워크 보안",
    "score": 12,
    "concept_id": "CON-NET-01",
    "source_id": "SRC-02",
    "source_page": 3,
    "question": "TCP 헤더의 제어 비트(Control Flag)는 통신 세션 제어에 사용된다. 다음 4개 플래그의 명칭과 동작 역할을 각각 서술하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 3,
        "prompt": "1) SYN(Synchronize) 플래그의 역할",
        "model_answer": "TCP 3-Way Handshake 시 최초 연결 수립을 요청하며 송수신자 간의 초기 시퀀스 번호(ISN)를 동기화하기 위해 사용된다.",
        "rubric": {
          "keywords": [
            ["연결 수립", "연결 요청", "handshake", "세션 수립", "연결시작"],
            ["시퀀스", "sequence", "순서 번호", "동기화", "isn"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 2,
        "score": 3,
        "prompt": "2) ACK(Acknowledgment) 플래그의 역할",
        "model_answer": "상대방으로부터 패킷을 정상 수신했음을 확인해주는 응답 플래그로 일반적으로 수신한 시퀀스 번호에 +1한 값을 승인 번호로 전송한다.",
        "rubric": {
          "keywords": [
            ["수신 확인", "수신", "패킷 확인", "정상 수신", "도착"],
            ["응답", "+1", "승인", "확인 번호"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 3,
        "score": 3,
        "prompt": "3) FIN(Finish) 플래그의 역할",
        "model_answer": "더 이상 전송할 데이터가 없어 정상적으로 TCP 세션 연결 종료를 요청할 때 사용된다(4-Way Handshake).",
        "rubric": {
          "keywords": [
            ["종료", "연결 종료", "세션 종료", "연결 해제"],
            ["정상", "데이터 전송 완료", "요청"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      },
      {
        "sub_id": 4,
        "score": 3,
        "prompt": "4) RST(Reset) 플래그의 역할",
        "model_answer": "연결 상의 오류가 발생하거나 수신 대기 포트가 닫혀있을 때 비정상적인 세션을 즉시 강제 종료하고 리셋할 때 사용된다.",
        "rubric": {
          "keywords": [
            ["강제 종료", "강제 리셋", "리셋", "reset", "재설정"],
            ["비정상", "오류", "즉시 끊기", "강제"]
          ],
          "all_match_points": 3,
          "partial_match_points": 1.5
        }
      }
    ],
    "explanation": "TCP 6비트 제어 플래그 중 SYN(연결수립), ACK(수신확인), FIN(정상종료), RST(비정상 강제리셋)의 핵심 메커니즘을 묻는 정통 기출입니다.",
    "difficulty": "low",
    "tags": ["TCP", "플래그", "SYN", "ACK", "FIN", "RST"]
  },
  {
    "id": "Q-DESC-007",
    "type": "descriptive",
    "category": "애플리케이션 보안",
    "score": 12,
    "concept_id": "CON-APP-01",
    "source_id": "SRC-02",
    "source_page": 4,
    "question": "웹 애플리케이션의 파일 업로드 취약점에 대한 질문이다. 각 물음에 답하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) 파일 업로드 취약점의 정의와 공격자가 업로드 성공 시 초래되는 보안 위협을 서술하시오.",
        "model_answer": "서버 측 확장자 및 실행 검증 미흡으로 공격자가 웹셸(Webshell) 등 서버 측 실행 스크립트 파일을 업로드하여 원격에서 시스템 명령 실행 및 내부망 침투 권한을 탈취하는 취약점이다.",
        "rubric": {
          "keywords": [
            ["웹셸", "webshell", "악성 스크립트", "실행 파일", "실행 스크립트"],
            ["명령어 실행", "원격 실행", "권한 탈취", "시스템 제어"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) 클라이언트 단 확장자 검증을 우회하기 위해 공격자가 사용하는 대표적인 기법 2가지를 서술하시오.",
        "model_answer": "1. 웹 프록시 도구를 이용한 Content-Type 변조 (예: image/jpeg로 조작)\n2. 파일명 뒤에 Null 바이트(%00)를 삽입하는 Null Byte Injection (예: test.php%00.jpg)",
        "rubric": {
          "keywords": [
            ["content-type", "파일 타입", "mime type", "프록시"],
            ["null 바이트", "%00", "null", "널 바이트", "확장자 변조"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) 서버 측에서 파일 업로드 공격을 원천 차단하기 위한 기술적 대응 대책 2가지를 서술하시오.",
        "model_answer": "1. 업로드 파일의 확장자를 서버 단에서 화이트리스트 방식으로 엄격히 검증\n2. 업로드 디렉터리를 웹 루트 외부에 두거나 웹 서버 설정에서 스크립트 실행 권한을 완전히 제거",
        "rubric": {
          "keywords": [
            ["화이트리스트", "whitelist", "서버 측 검증", "확장자 제한"],
            ["실행 권한 제거", "실행 제한", "웹 루트 외부", "실행 차단"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "파일 업로드 취약점 대응은 클라이언트 검증이 아닌 서버 측 확장자 화이트리스트, 실행 권한 박탈, 웹 루트 분리가 필수적입니다.",
    "difficulty": "medium",
    "tags": ["파일업로드", "웹셸", "Content-Type", "Null바이트"]
  },
  {
    "id": "Q-DESC-008",
    "type": "descriptive",
    "category": "애플리케이션 보안",
    "score": 12,
    "concept_id": "CON-APP-01",
    "source_id": "SRC-02",
    "source_page": 5,
    "question": "웹서버 보안 로그 분석 중 1초에 1,000건 이상의 비정상 HTTP GET 요청이 유입되는 현상이 식별되었다. 다음 HTTP 헤더 샘플을 보고 물음에 답하시오.\n\n[HTTP Request]\nGET /test.jsp HTTP/1.1\nHost: webserver.com\nUser-Agent: Mozilla/5.0\nReferer: http://www.attacker-site.com/default.jsp\nCache-Control: max-age=0",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) 해당 공격의 정확한 명칭을 기술하시오.",
        "model_answer": "HTTP GET Flooding with Cache-Control (또는 CC Attack, Cache-Control 기반 웹 부하 공격)",
        "rubric": {
          "keywords": [
            ["http get flooding", "get flooding", "겟 플러딩", "cc attack", "cache control"],
            ["flooding", "플러딩", "공격", "부하"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) 헤더 중 'Cache-Control: max-age=0' 설정이 서버에 미치는 기술적 영향을 서술하시오.",
        "model_answer": "중간 프록시 서버나 CDN의 캐시 응답을 무력화(no-cache와 유사)하여 모든 대량 요청이 백엔드 원본 웹 서버로 직접 전달되게 함으로써 서버의 CPU 및 자원 고갈을 유발한다.",
        "rubric": {
          "keywords": [
            ["캐시 우회", "no-cache", "캐시 무력화", "캐시 서버"],
            ["원본 웹서버", "웹서버", "직접", "부하 가중", "자원 고갈"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) 'Referer' 헤더를 통해 파악할 수 있는 공격 트래픽의 이상 징후를 서술하시오.",
        "model_answer": "요청된 Host(webserver.com)와 무관한 제3의 외부 도메인(attacker-site.com)이 Referer로 설정되어 있어 악의적인 외부 사이트 링크나 자동화 스크립트에 의해 대량 호출되었음을 나타낸다.",
        "rubric": {
          "keywords": [
            ["외부", "제3", "다른 사이트", "타 도메인", "불일치"],
            ["자동화", "스크립트", "유입", "링크"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "Cache-Control: max-age=0 옵션은 캐시 서버를 우회하여 원본 웹 서버로 직접 부하를 유발하는 대표적 웹 DDoS 공격(CC Attack) 기법입니다.",
    "difficulty": "medium",
    "tags": ["HTTP_GET_Flooding", "Cache-Control", "CC_Attack", "DDoS"]
  },
  {
    "id": "Q-DESC-009",
    "type": "descriptive",
    "category": "시스템 보안",
    "score": 12,
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-02",
    "source_page": 9,
    "question": "기업 내 BYOD(Bring Your Own Device) 모바일 오피스 환경에서 업무 데이터 유출을 방지하기 위한 핵심 보안 기술 3가지의 개념을 서술하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) MDM(Mobile Device Management)의 개념과 주요 보안 기능을 서술하시오.",
        "model_answer": "모바일 단말기를 중앙에서 관리·통제하는 기술로, 분실/도난 시 원격 데이터 삭제(Remote Wipe), 화면 캡처 방지, 카메라 차단, 루팅/탈옥 탐지 등의 보안 정책을 강제 적용한다.",
        "rubric": {
          "keywords": [
            ["단말 관리", "중앙 관리", "모바일 관리", "원격 제어"],
            ["원격 삭제", "wipe", "정책 강제", "분실", "도난"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) 컨테이너화(Containerization) 기술의 원리와 프라이버시 보호 방안을 서술하시오.",
        "model_answer": "단일 모바일 기기 내에 암호화된 독립적인 업무 전용 가상 공간(컨테이너)을 생성하여 개인 영역과 업무 데이터를 격리함으로써 회사 데이터 보호와 개인 프라이버시를 동시에 보장한다.",
        "rubric": {
          "keywords": [
            ["업무", "업무용", "회사"],
            ["개인", "개인용", "프라이버시"],
            ["격리", "분리", "암호화 공간", "컨테이너"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) 모바일 가상화(Mobile Virtualization) 기술의 개념을 서술하시오.",
        "model_answer": "하이퍼바이저 등 가상화 기술을 이용하여 하나의 하드웨어 위에 개인용 OS와 업무용 OS를 물리적 수준으로 완전 분리하여 독립 구동하는 기술이다.",
        "rubric": {
          "keywords": [
            ["가상화", "하이퍼바이저", "vm"],
            ["os 분리", "운영체제 분리", "듀얼 os", "물리적 수준 분리"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "BYOD 보안의 삼총사는 단말 자체를 제어하는 MDM, 앱/데이터를 분리하는 컨테이너화, OS 수준을 분리하는 모바일 가상화입니다.",
    "difficulty": "medium",
    "tags": ["BYOD", "MDM", "컨테이너화", "모바일가상화"]
  },
  {
    "id": "Q-DESC-010",
    "type": "descriptive",
    "category": "애플리케이션 보안",
    "score": 12,
    "concept_id": "CON-APP-01",
    "source_id": "SRC-03",
    "source_page": 4,
    "question": "XSS(Cross-Site Scripting) 취약점에 대한 질문이다. 제공된 자료를 바탕으로 각 물음에 답하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) Stored XSS와 Reflected XSS의 결정적인 차이점을 '악성 스크립트 저장 위치' 및 '피해 대상 범위' 관점에서 비교 서술하시오.",
        "model_answer": "Stored XSS는 악성 스크립트가 웹 서버의 DB에 영구 저장되어 페이지를 열람하는 불특정 다수에게 피해를 주며, Reflected XSS는 스크립트가 DB에 저장되지 않고 URL 파라미터를 통해 즉시 반사되어 조작된 링크를 클릭한 특정 사용자에게만 피해를 준다.",
        "rubric": {
          "keywords": [
            ["db 저장", "데이터베이스 저장", "영구", "불특정 다수"],
            ["url 파라미터", "즉시 반사", "미저장", "링크 클릭"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) XSS를 통한 세션 탈취를 방지하기 위해 Set-Cookie 헤더에 설정하는 'HttpOnly' 속성의 방어 원리를 서술하시오.",
        "model_answer": "브라우저 자바스크립트(document.cookie)를 통한 해당 쿠키의 접근을 원천 차단하여, 악성 스크립트가 실행되더라도 사용자의 세션 쿠키를 외부로 유출할 수 없도록 방어한다.",
        "rubric": {
          "keywords": [
            ["document.cookie", "자바스크립트", "javascript", "스크립트 접근 차단"],
            ["세션 탈취", "쿠키 유출", "탈취 방지", "보호"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) 출력값 검증을 위해 특수문자를 HTML Entity로 치환하는 원리를 서술하고, 치환 대상 특수문자 3가지를 예시로 드시오.",
        "model_answer": "브라우저가 특수문자를 실행 코드가 아닌 단순 문자열로 렌더링하도록 치환하는 기법이며, 주요 대상 문자는 '<' (&lt;), '>' (&gt;), '&' (&amp;), '\"' (&quot;) 등이다.",
        "rubric": {
          "keywords": [
            ["단순 문자열", "실행 방지", "코드 인식 방지", "치환"],
            ["&lt;", "<", "&gt;", ">", "&amp;", "&"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "XSS 방어의 2대 축은 출력값 HTML Entity 인코딩과 쿠키 탈취를 방어하는 HttpOnly 속성 부여입니다.",
    "difficulty": "medium",
    "tags": ["XSS", "HttpOnly", "HTML_Entity", "Stored_XSS", "Reflected_XSS"]
  },
  {
    "id": "Q-DESC-011",
    "type": "descriptive",
    "category": "정보보호 관리 및 법규",
    "score": 12,
    "concept_id": "CON-LAW-01",
    "source_id": "SRC-03",
    "source_page": 1,
    "question": "법적 증거 능력을 인정받기 위한 디지털 포렌식(Digital Forensics)의 5대 원칙에 대한 질문이다. 각 물음에 답하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) '정당성의 원칙'과 '신속성의 원칙'의 개념을 각각 서술하시오.",
        "model_answer": "정당성의 원칙: 증거 수집 과정이 적법한 법적 절차(적법절차 준수, 영장주의 등)를 거쳐 획득되어야 한다.\n신속성의 원칙: 휘발성 메모리 데이터 등 디지털 증거가 손실·소멸되기 전에 지체 없이 신속하게 수집되어야 한다.",
        "rubric": {
          "keywords": [
            ["적법 절차", "영장", "정당성", "법적 절차"],
            ["휘발성", "신속성", "지체 없이", "소멸 방지"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) '무결성의 원칙'과 '재현성의 원칙'의 개념을 각각 서술하시오.",
        "model_answer": "무결성의 원칙: 수집된 원본 증거가 법정에 제출될 때까지 위조·변조되지 않았음을 해시(Hash)값 일치를 통해 입증해야 한다.\n재현성의 원칙: 동일한 조건과 도구를 사용하여 분석했을 때 언제나 동일한 결과가 도출되어야 한다.",
        "rubric": {
          "keywords": [
            ["무결성", "해시", "위변조", "해시값"],
            ["재현성", "동일한 결과", "동일 조건", "검증"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) '연계보관성의 원칙(Chain of Custody)'의 개념을 서술하시오.",
        "model_answer": "증거 획득 시점부터 법정 제출에 이르기까지 증거를 취급한 모든 담당자, 시간, 장소, 보관 상태가 연속적으로 추적 가능하도록 투명하게 기록·관리되어야 한다는 원칙이다.",
        "rubric": {
          "keywords": [
            ["연계보관성", "chain of custody", "연계 보관성"],
            ["담당자", "이동", "보관", "추적성", "기록"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "디지털 포렌식 5대 기본 원칙: 정당성, 신속성, 무결성, 재현성, 연계보관성(Chain of Custody)은 실기 단골 빈출 주제입니다.",
    "difficulty": "medium",
    "tags": ["포렌식", "5대원칙", "무결성", "연계보관성"]
  },
  {
    "id": "Q-DESC-012",
    "type": "descriptive",
    "category": "정보보호 관리 및 법규",
    "score": 12,
    "concept_id": "CON-MGT-01",
    "source_id": "SRC-03",
    "source_page": 1,
    "question": "정량적 위험분석(Quantitative Risk Analysis)에서 연간 예상 손실액을 산출하는 주요 지표와 공식에 대한 질문이다. 각 물음에 답하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "1) SLE(Single Loss Expectancy, 단일 예상 손실액)의 정의와 산출 공식을 자산가치(AV) 및 노출계수(EF)를 사용하여 기술하시오.",
        "model_answer": "정의: 특정 위협이 1회 발생했을 때 조직의 자산이 입게 되는 단일 손실 규모\n공식: SLE = 자산가치(AV, Asset Value) × 노출계수(EF, Exposure Factor)",
        "rubric": {
          "keywords": [
            ["av", "자산가치", "asset value"],
            ["ef", "노출계수", "exposure factor"],
            ["1회", "단일 손실", "단일 예상"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "2) ARO(Annual Rate of Occurrence, 연간 발생률)의 개념을 기술하시오.",
        "model_answer": "특정 보안 위협이 1년 동안 발생할 것으로 예상되는 빈도(횟수)를 나타내는 확률적 수치이다 (예: 10년에 1회면 0.1, 1년에 2회면 2.0).",
        "rubric": {
          "keywords": [
            ["1년", "연간", "연간 발생"],
            ["빈도", "횟수", "발생률", "확률"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "3) ALE(Annualized Loss Expectancy, 연간 예상 손실액)의 산출 공식을 기술하고, 조직이 정보보호 대책을 도입할 때의 비용 대비 효과성(Cost-Benefit Analysis) 판단 기준을 서술하시오.",
        "model_answer": "공식: ALE = SLE × ARO\n판단 기준: 보안 대책 도입에 소요되는 연간 비용이 대책 적용을 통해 감소되는 위험 손실액(ALE 감소분)보다 적어야 대책 도입의 타당성이 인정된다 (보호대책 비용 < 통제 전 ALE - 통제 후 ALE).",
        "rubric": {
          "keywords": [
            ["sle * aro", "sle × aro", "sle*aro", "연간 예상 손실액"],
            ["비용", "대책 비용", "손실 감소", "비용효과", "ale 감소"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "explanation": "정량적 위험분석 공식: SLE = AV * EF, ALE = SLE * ARO. 보안 대책의 비용 효과성은 연간 대책 비용이 줄어든 위험 손실액(ALE)보다 작아야 합니다.",
    "difficulty": "medium",
    "tags": ["위험분석", "ALE", "SLE", "ARO", "비용효과분석"]
  }
]

EXPANDED_PRAC = [
  {
    "id": "Q-PRAC-003",
    "type": "practical",
    "category": "애플리케이션 보안",
    "score": 16,
    "concept_id": "CON-APP-01",
    "source_id": "SRC-02",
    "source_page": 1,
    "question": "다음 아파치(Apache) 웹서버의 access.log 포맷 기록을 분석하고 물음에 답하시오.\n\n[웹서버 접근 로그 기록]\n200.3.1.4 - - [30/May/2023:01:20:01 +09:00] \"GET /bulletin/read.php?no=101&item=book HTTP/1.1\" 200 3549 \"http://test.co.kr/main.php\" \"Mozilla/5.0 (Windows NT 10.0; WOW64)\"",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 5,
        "prompt": "1) 요청 URI의 파라미터인 'no=101&item=book'이 웹 애플리케이션 관점에서 의미하는 바를 구체적으로 서술하시오.",
        "model_answer": "클라이언트가 /bulletin/read.php 스크립트를 GET 메서드로 호출하면서 no 변수에 101, item 변수에 book이라는 두 개의 매개변수 값을 각각 전달하여 해당 게시물을 조회 요청하고 있다.",
        "rubric": {
          "keywords": [
            ["get", "get 방식", "get 메서드"],
            ["no=101", "no 101", "매개변수"],
            ["item=book", "item book", "파라미터", "조회"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 2,
        "score": 5,
        "prompt": "2) 로그에 기록된 HTTP 상태 코드 '200'과 전송 크기 '3549'의 의미를 서술하시오.",
        "model_answer": "상태 코드 200은 웹서버가 클라이언트의 요청을 에러 없이 성공적으로 처리(OK)했음을 의미하며, 3549는 클라이언트에게 전송한 응답 HTTP 본문(페이로드) 크기가 3,549 바이트임을 의미한다.",
        "rubric": {
          "keywords": [
            ["200", "정상", "성공", "ok"],
            ["3549", "바이트", "전송 크기", "응답 크기"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 3,
        "score": 6,
        "prompt": "3) 로그 필드 중 \"http://test.co.kr/main.php\"의 의미를 HTTP 요청 헤더 관점에서 서술하시오.",
        "model_answer": "Referer(참조자) 헤더 필드로, 사용자가 test.co.kr/main.php 페이지에 위치한 링크나 기능을 클릭하여 현재 요청 URL(/bulletin/read.php)로 이동(경유)해 왔음을 나타낸다.",
        "rubric": {
          "keywords": [
            ["referer", "리퍼러", "참조자"],
            ["경유", "이전 페이지", "호출한 페이지", "링크"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      }
    ],
    "explanation": "Combined Log Format 분석: 클라이언트 IP - - [일시] \"메서드 URI 프로토콜\" 상태코드 전송바이트 \"Referer\" \"User-Agent\"",
    "difficulty": "medium",
    "tags": ["로그분석", "Apache", "HTTP_200", "Referer"]
  },
  {
    "id": "Q-PRAC-004",
    "type": "practical",
    "category": "네트워크 보안",
    "score": 16,
    "concept_id": "CON-NET-01",
    "source_id": "SRC-02",
    "source_page": 8,
    "question": "Korea.co.kr 도메인에 대한 DNS Master와 Slave 서버 구축을 진행하려고 한다. Master 네임서버 IP는 192.168.1.53, Slave 네임서버 IP는 192.168.2.53일 때 BIND 설정 파일(/etc/named.conf)을 완성하시오.",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 8,
        "prompt": "1) Master DNS 서버의 named.conf 설정에서 zone \"korea.co.kr\" 블록의 type 및 Slave 서버로만 영역 전송(zone transfer)을 허용하는 allow-transfer(또는 allow-update) 지시자 설정을 작성하시오.",
        "model_answer": "zone \"korea.co.kr\" IN {\n    type master;\n    file \"korea.co.kr.zone\";\n    allow-transfer { 192.168.2.53; };\n};",
        "rubric": {
          "keywords": [
            ["type master", "master"],
            ["allow-transfer", "allow-update", "192.168.2.53"],
            ["korea.co.kr.zone", "zone"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      },
      {
        "sub_id": 2,
        "score": 8,
        "prompt": "2) Slave DNS 서버의 named.conf 설정에서 zone \"korea.co.kr\" 블록의 type, 원본 데이터를 동기화받을 Master IP 지정 masters 지시자, 그리고 다른 호스트로의 영역 전송을 차단하는 설정을 작성하시오.",
        "model_answer": "zone \"korea.co.kr\" IN {\n    type slave;\n    file \"slaves/korea.co.kr.zone\";\n    masters { 192.168.1.53; };\n    allow-transfer { none; };\n};",
        "rubric": {
          "keywords": [
            ["type slave", "slave"],
            ["masters", "192.168.1.53"],
            ["allow-transfer", "none"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      }
    ],
    "explanation": "DNS 보안 설정의 핵심은 불필요한 도메인 정보 유출(Zone Transfer)을 방지하기 위해 Master에서는 지정된 Slave IP만 허용하고, Slave에서는 allow-transfer { none; }으로 차단하는 것입니다.",
    "difficulty": "high",
    "tags": ["DNS", "named.conf", "Zone_Transfer", "BIND"]
  },
  {
    "id": "Q-PRAC-005",
    "type": "practical",
    "category": "시스템 보안",
    "score": 16,
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-02",
    "source_page": 1,
    "question": "서버 보안 진단원이 리눅스 시스템 점검 중 다음과 같은 특수 권한 제거 조치 및 검색 명령을 수행하였다. 각 물음에 답하시오.\n\n[조치 명령 1] chmod -s /usr/bin/newgrp\n[조치 명령 2] find / -user root -type f \\( -perm -4000 -o -perm -2000 \\) -exec ls -al {} \\;",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 5,
        "prompt": "1) [조치 명령 1]의 'chmod -s' 명령어가 시스템 파일에 적용하는 구체적인 동작을 서술하시오.",
        "model_answer": "지정된 실행 파일에 설정되어 있던 특수 권한 비트인 SetUID 및 SetGID 권한을 제거하여, 일반 사용자가 해당 명령 실행 시 소유자(root) 권한으로 전환되지 못하도록 방지한다.",
        "rubric": {
          "keywords": [
            ["setuid", "setgid", "특수 권한", "특수 비트"],
            ["제거", "해제", "박탈", "삭제"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 2,
        "score": 5,
        "prompt": "2) [조치 명령 2]의 find 명령어에서 '-perm -4000 -o -perm -2000' 옵션이 검색하는 대상의 조건을 서술하시오.",
        "model_answer": "최상위(/) 디렉터리 하위의 일반 파일 중 root가 소유주이면서 SetUID 비트(4000)가 설정되어 있거나 또는(-o) SetGID 비트(2000)가 설정되어 있는 모든 파일을 검색한다.",
        "rubric": {
          "keywords": [
            ["root", "소유주", "소유자"],
            ["4000", "setuid", "2000", "setgid", "-perm"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 3,
        "score": 6,
        "prompt": "3) root 소유의 실행 파일에 불필요한 SetUID 비트가 설정되어 있을 때 발생할 수 있는 보안 위협을 권한 상승 관점에서 서술하시오.",
        "model_answer": "SetUID가 설정된 파일은 일반 사용자가 실행하더라도 프로세스가 실행되는 동안 파일 소유자(root) 권한으로 동작하므로, 해당 프로그램에 취약점이 존재할 경우 일반 사용자가 비인가 root 관리자 권한을 획득(Privilege Escalation)하는 심각한 보안 위협이 발생한다.",
        "rubric": {
          "keywords": [
            ["일반 사용자", "누구나", "사용자"],
            ["root 권한", "관리자 권한", "소유자 권한"],
            ["권한 상승", "privilege escalation", "악용", "침해"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      }
    ],
    "explanation": "SetUID(4000)는 실행 순간 소유자 권한으로 실행되므로 불필요한 SetUID 바이너리는 'chmod -s'로 제거해야 시스템 권한 상승 공격을 차단할 수 있습니다.",
    "difficulty": "medium",
    "tags": ["SetUID", "SetGID", "chmod", "권한상승", "find"]
  },
  {
    "id": "Q-PRAC-006",
    "type": "practical",
    "category": "네트워크/보안운영",
    "score": 16,
    "concept_id": "CON-NET-02",
    "source_id": "SRC-03",
    "source_page": 5,
    "question": "다음은 특정 공격 트래픽을 탐지·차단하기 위해 작성된 Snort NIDS 룰의 일부이다. 각 물음에 답하시오.\n\nalert tcp $EXTERNAL_NET any -> $HOME_NET 80 (msg:\"HTTP GET Flooding Detect\"; content:\"GET / HTTP/1.1\"; ( A ); nocase; threshold:type ( B ), track ( C ), count 100, seconds 1; sid:1000999;)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 5,
        "prompt": "1) content 매칭 대상을 페이로드의 첫 바이트(오프셋 0)부터 시작하여 13바이트 범위 내에서만 탐지하도록 제한하고자 할 때, ( A )에 들어갈 Snort 바디 옵션을 문법에 맞게 작성하시오.",
        "model_answer": "depth:13 (또는 offset:0; depth:13)",
        "rubric": {
          "keywords": [
            ["depth:13", "depth : 13", "depth: 13", "depth"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 2,
        "score": 5,
        "prompt": "2) 매 1초 동안 동일한 출발지 IP에서 100번째 이벤트가 발생할 때마다 알람을 발생시키고자 한다. ( B )와 ( C )에 들어갈 옵션 값을 기술하시오.",
        "model_answer": "(B): threshold\n(C): by_src",
        "rubric": {
          "keywords": [
            ["threshold", "type threshold"],
            ["by_src", "track by_src", "by_dst"]
          ],
          "all_match_points": 5,
          "partial_match_points": 2.5
        }
      },
      {
        "sub_id": 3,
        "score": 6,
        "prompt": "3) 만약 이 룰의 액션을 alert에서 'reject'로 변경할 경우, Snort는 탐지된 악성 패킷을 차단한 후 TCP 세션을 강제 종료하기 위해 공격자에게 어떤 프로토콜 응답 패킷을 전송하는지 기술하시오.",
        "model_answer": "TCP 프로토콜의 RST(Reset) 플래그 패킷(TCP RST 패킷)을 송신자에게 전송하여 세션을 즉시 강제 리셋·종료시킨다.",
        "rubric": {
          "keywords": [
            ["tcp rst", "rst", "reset", "리셋 패킷"],
            ["강제 종료", "세션 종료", "차단", "연결 리셋"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      }
    ],
    "explanation": "Snort 룰 바디 옵션: depth는 시작점부터의 탐지 범위, threshold는 조건 만족 시마다 알람, reject 액션은 TCP의 경우 RST 패킷을 전송하여 능동 세션 차단을 수행합니다.",
    "difficulty": "medium",
    "tags": ["Snort", "depth", "threshold", "reject", "TCP_RST"]
  }
]

def main():
    target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data", "questions.json")
    with open(target_path, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # 18개 표준 문항 보존
    existing_ids = set(q["id"] for q in existing)
    new_questions = []

    for q in EXPANDED_SHORT:
        if q["id"] not in existing_ids:
            new_questions.append(q)

    for q in EXPANDED_DESC:
        if q["id"] not in existing_ids:
            new_questions.append(q)

    for q in EXPANDED_PRAC:
        if q["id"] not in existing_ids:
            new_questions.append(q)

    combined = existing + new_questions

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"Successfully added {len(new_questions)} questions! Total question bank count: {len(combined)}")

if __name__ == "__main__":
    main()
