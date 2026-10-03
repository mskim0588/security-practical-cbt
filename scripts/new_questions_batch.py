import json
import sys
import os
import pypdf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.expand_questions import EXPANDED_SHORT, EXPANDED_DESC, EXPANDED_PRAC

# 신규 단답형 5문항 (Q-SHORT-037 ~ Q-SHORT-041)
NEW_SHORT_QUESTIONS = [
  {
    "id": "Q-SHORT-037",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-01",
    "source_id": "SRC-01",
    "source_page": 14,
    "question": "접근통제 정책 3가지 모델에 대한 설명이다. ( )에 들어갈 모델명을 기술하시오.\n\n( A ) : 주체나 주체가 속한 그룹의 신분에 근거하여 객체에 대한 접근을 제한하는 사용자 중심의 접근통제 모델 (자유재량 접근통제)\n( B ) : 주체와 객체의 보안등급 및 인가등급을 비교하여 시스템에 부여된 보안 규칙에 따라 접근을 강제하는 모델 (강제적 접근통제)\n( C ) : 조직 내에서 개별 사용자가 맡은 역할 및 직무에 따라 접근 권한을 부여하고 통제하는 모델",
    "sub_questions": [
      {
        "label": "A",
        "score": 1,
        "answer": "DAC",
        "accepted_answers": ["DAC", "임의적 접근통제", "임의적접근통제", "Discretionary Access Control"]
      },
      {
        "label": "B",
        "score": 1,
        "answer": "MAC",
        "accepted_answers": ["MAC", "강제적 접근통제", "강제적접근통제", "Mandatory Access Control"]
      },
      {
        "label": "C",
        "score": 1,
        "answer": "RBAC",
        "accepted_answers": ["RBAC", "역할기반 접근통제", "역할기반접근통제", "Role-Based Access Control"]
      }
    ],
    "explanation": "접근통제 3대 정책: 신분 기반의 임의적 접근통제(DAC), 보안등급 기반의 강제적 접근통제(MAC), 직무 역할 기반의 역할기반 접근통제(RBAC).",
    "difficulty": "low",
    "tags": ["접근통제", "DAC", "MAC", "RBAC"]
  },
  {
    "id": "Q-SHORT-038",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 17,
    "question": "네트워크에 접속을 시도하는 단말기의 무결성을 검증하고(백신 설치 여부, OS 패치 상태 등), 보안 정책을 준수하지 않은 비인가 단말의 사내망 접속을 격리 및 통제하는 네트워크 접근 제어 보안 솔루션의 명칭(영문 약어 또는 풀네임)은 무엇인가?",
    "answer": "NAC",
    "accepted_answers": [
      "NAC",
      "Network Access Control",
      "네트워크 접근 제어",
      "네트워크 접근제어",
      "네트워크접근제어"
    ],
    "sub_questions": None,
    "explanation": "NAC(Network Access Control, 네트워크 접근 제어)은 단말기가 내부망에 접속하기 전 보안 정책 준수 여부를 사전 검증하여 안전한 단말만 접속을 허용하는 솔루션입니다.",
    "difficulty": "low",
    "tags": ["NAC", "네트워크보안", "보안솔루션"]
  },
  {
    "id": "Q-SHORT-039",
    "type": "short",
    "category": "시스템 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-SYS-03",
    "source_id": "SRC-01",
    "source_page": 17,
    "question": "둘 이상의 프로세스가 공용 메모리나 파일 등의 공유 자원에 동시 접근하여 경쟁(Race)하는 과정에서, 자원 상태를 검사하는 시점(Check)과 실제로 사용하는 시점(Use) 사이의 시간차(TOCTOU)를 악용하여 파일 링크를 바꿔치기하고 관리자 권한을 획득하는 시스템 공격 기법의 명칭은 무엇인가?",
    "answer": "레이스 컨디션",
    "accepted_answers": [
      "레이스 컨디션",
      "레이스컨디션",
      "Race Condition",
      "레이스 컨디션 공격",
      "경쟁 상태"
    ],
    "sub_questions": None,
    "explanation": "레이스 컨디션(Race Condition) 공격은 프로세스 간 실행 순서 및 자원 접근 타이밍 경쟁을 이용하여 권한 상승이나 불법 수정을 유발하는 공격입니다.",
    "difficulty": "medium",
    "tags": ["레이스컨디션", "RaceCondition", "TOCTOU", "시스템공격"]
  },
  {
    "id": "Q-SHORT-040",
    "type": "short",
    "category": "네트워크 보안",
    "score": 3,
    "grading_mode": "normalized",
    "concept_id": "CON-NET-01",
    "source_id": "SRC-01",
    "source_page": 17,
    "question": "동일 로컬 네트워크(LAN) 세그먼트 상에서 게이트웨이나 희생자(Victim)의 IP 주소에 해당하는 MAC 주소를 공격자 자신의 MAC 주소로 조작한 위조 ARP Reply 패킷을 주기적으로 브로드캐스트/유니캐스트하여, 희생자의 모든 송수신 패킷을 가로채 도청(스니핑)하는 2계층 공격 기법은 무엇인가?",
    "answer": "ARP 스푸핑",
    "accepted_answers": [
      "ARP 스푸핑",
      "ARP스푸핑",
      "ARP Spoofing",
      "ARP Cache Poisoning",
      "ARP 캐시 포이즈닝"
    ],
    "sub_questions": None,
    "explanation": "ARP 스푸핑(ARP Spoofing)은 2계층 LAN에서 ARP 캐시 테이블을 변조하여 통신 경로를 공격자 PC로 변경하는 공격 기법입니다.",
    "difficulty": "low",
    "tags": ["ARP스푸핑", "ARPSpoofing", "스니핑", "L2공격"]
  },
  {
    "id": "Q-SHORT-041",
    "type": "short",
    "category": "애플리케이션 보안",
    "score": 3,
    "grading_mode": "strict",
    "concept_id": "CON-APP-01",
    "source_id": "SRC-01",
    "source_page": 15,
    "question": "아파치(Apache) 웹서버의 설정 파일(httpd.conf)에서 요청 디렉터리에 index.html 등의 기본 문서가 없을 때 웹 브라우저 화면에 디렉터리 내 전체 파일 목록이 노출되는 디렉터리 리스팅(Directory Listing) 취약점을 제거하기 위해 <Directory> 블록의 Options 지시자에서 삭제하거나 '-' 부호를 붙여 비활성화해야 하는 옵션 키워드는 무엇인가?",
    "answer": "Indexes",
    "accepted_answers": [
      "Indexes",
      "-Indexes",
      "indexes",
      "-indexes"
    ],
    "sub_questions": None,
    "explanation": "Apache 웹서버에서 Options 지시자의 Indexes를 제거하거나 -Indexes로 설정하면 디렉터리 리스팅 취약점을 방지(403 Forbidden 반환)할 수 있습니다.",
    "difficulty": "medium",
    "tags": ["Apache", "Indexes", "디렉터리리스팅", "웹설정"]
  }
]

# 신규 서술형 3문항 (Q-DESC-013 ~ Q-DESC-015)
NEW_DESC_QUESTIONS = [
  {
    "id": "Q-DESC-013",
    "type": "descriptive",
    "category": "정보보호 관리 및 법규",
    "score": 12,
    "concept_id": "CON-MGT-01",
    "source_id": "SRC-02",
    "source_page": 10,
    "question": "조직의 정보자산 위험 분석(Risk Analysis) 방법론 중 다음 두 가지 접근법에 대하여 개념과 장단점을 각각 설명하시오.\n\n1) 기준선(베이스라인) 접근법의 개념과 장·단점 (6점)\n2) 상세 위험 분석법의 개념과 장·단점 (6점)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 6,
        "prompt": "기준선(베이스라인) 접근법의 개념 및 장단점",
        "model_answer": "개념: 표준화된 체크리스트를 기반으로 모든 시스템에 기본적인 보호대책 수준을 적용하는 방식. 장점: 시간과 비용을 절약하여 간단히 수행 가능. 단점: 조직별 특성이 반영되지 않아 과보호 또는 보안 미흡이 발생할 수 있음.",
        "rubric": {
          "keywords": [
            ["체크리스트", "표준", "기본 수준", "보호대책"],
            ["시간", "비용", "절약", "간단"],
            ["과보호", "미흡", "특성 미반영", "변화 미반영"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      },
      {
        "sub_id": 2,
        "score": 6,
        "prompt": "상세 위험 분석법의 개념 및 장단점",
        "model_answer": "개념: 자산, 위협, 취약점의 세부 평가를 통해 위험 수준을 정확히 정량/정성적으로 분석하는 방식. 장점: 조직에 가장 적합한 최적의 보안 대책을 도출할 수 있음. 단점: 전문 인력과 많은 시간, 높은 비용이 소요됨.",
        "rubric": {
          "keywords": [
            ["자산", "위협", "취약점", "세부", "정밀"],
            ["최적", "적합", "정확"],
            ["시간", "비용", "전문 인력", "노력"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      }
    ],
    "model_answer": "1) 기준선 접근법: 표준 체크리스트 기반 기본 대책 적용 방식. 장점은 시간/비용 절약, 단점은 조직 특성 미반영으로 인한 과보호/보호미흡.\n2) 상세 위험분석: 자산/위협/취약점 전수 식별 방식. 장점은 최적화된 맞춤 통제 수립, 단점은 과도한 시간과 비용 소요.",
    "explanation": "기준선 접근법은 체크리스트 기반으로 신속하나 획일적이며, 상세 위험분석은 정밀하나 비용이 크므로, 통상 복합 접근법(Combined Approach)을 적용합니다.",
    "difficulty": "medium",
    "tags": ["위험분석", "기준선접근법", "상세위험분석"]
  },
  {
    "id": "Q-DESC-014",
    "type": "descriptive",
    "category": "네트워크 보안",
    "score": 12,
    "concept_id": "CON-NET-01",
    "source_id": "SRC-02",
    "source_page": 11,
    "question": "DDoS 공격 유형 중 하나인 DNS 증폭(DNS Amplification) 공격에 대하여 다음 물음에 답하시오.\n\n1) DNS 증폭 공격 시 출발지 IP 위조 및 증폭을 달성하기 위한 구체적인 동작 원리를 설명하시오. (6점)\n2) 공격자가 일반 DDoS 대신 DNS 증폭 반사 공격을 수행하는 주된 이유 2가지를 설명하시오. (6점)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 6,
        "prompt": "DNS 증폭 공격의 출발지 IP 위조 및 증폭 동작 원리",
        "model_answer": "공격자가 출발지 IP를 희생자(공격 대상)의 IP로 위조(IP Spoofing)한 후, 오픈 리졸버 DNS 서버에 요청 크기가 작고 응답 크기가 매우 큰 ANY 타입 쿼리를 대량 전송하여, 증폭된 대용량 응답 트래픽이 모두 희생자 서버로 쏟아지게 함",
        "rubric": {
          "keywords": [
            ["스푸핑", "IP 위조", "출발지"],
            ["ANY", "대용량", "레코드", "크기"],
            ["응답", "증폭", "반사", "희생자"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      },
      {
        "sub_id": 2,
        "score": 6,
        "prompt": "DNS 증폭 반사 공격을 수행하는 주된 이유 2가지",
        "model_answer": "첫째, 비연결성 프로토콜인 UDP의 특성상 인증이 없어 출발지 IP 스푸핑이 용이하고 반사 서버를 거쳐 공격 근원지 추적이 매우 어려움. 둘째, 소수의 좀비 PC나 작은 대역폭으로도 수십 배에 달하는 대용량 증폭 트래픽을 생성할 수 있어 공격 효율이 매우 높음.",
        "rubric": {
          "keywords": [
            ["추적", "은닉", "근원지", "UDP"],
            ["효율", "소수", "작은", "대용량", "트래픽"]
          ],
          "all_match_points": 6,
          "partial_match_points": 3
        }
      }
    ],
    "model_answer": "1) 원리: 출발지 IP를 피해자 IP로 위조하고 ANY 질의를 오픈 DNS에 전송하여 작은 요청 대비 수십 배 큰 응답을 피해자에게 반사 전달함.\n2) 이유: 근원지 역추적이 불가능하여 은닉성이 높고, 적은 자원으로 대규모 공격 트래픽을 유발할 수 있어 공격 효율이 극대화됨.",
    "explanation": "DNS Amplification은 대표적인 반사 DDoS(DrDoS) 공격으로, UDP 비연결성 특성과 오픈 리졸버(Open Resolver)의 대규모 TXT/ANY 응답 특성을 악용합니다.",
    "difficulty": "medium",
    "tags": ["DNS", "증폭공격", "DrDoS", "반사공격"]
  },
  {
    "id": "Q-DESC-015",
    "type": "descriptive",
    "category": "정보보호 관리 및 법규",
    "score": 12,
    "concept_id": "CON-MGT-03",
    "source_id": "SRC-02",
    "source_page": 12,
    "question": "개인정보보호법에 따른 '개인정보의 안전성 확보조치 기준'에서 요구하는 핵심 기술적 보호조치 중 다음 3가지 항목의 구체적 이행 방안을 설명하시오.\n\n1) 접근통제 이행 방안 (4점)\n2) 접속기록의 보관 및 위·변조 방지 방안 (4점)\n3) 개인정보의 안전한 암호화 적용 방안 (4점)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 4,
        "prompt": "접근통제 이행 방안",
        "model_answer": "개인정보처리시스템에 대한 접속 권한을 IP 주소 등으로 제한하여 인가받지 않은 접근을 차단하고, 불법 접근 및 유출 시도를 실시간 탐지·차단함",
        "rubric": {
          "keywords": [
            ["IP", "접속 권한", "제한", "인가", "차단"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 2,
        "score": 4,
        "prompt": "접속기록 보관 및 위변조 방지 방안",
        "model_answer": "개인정보 취급자의 접속기록을 1년(또는 2년) 이상 보관·관리하고, 접속기록의 위·변조 방지를 위해 정기적 백업 및 별도의 물리적/논리적 매체에 안전하게 보관함",
        "rubric": {
          "keywords": [
            ["접속기록", "1년", "2년", "보관", "백업", "위변조"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      },
      {
        "sub_id": 3,
        "score": 4,
        "prompt": "개인정보 암호화 적용 방안",
        "model_answer": "비밀번호는 복호화가 불가능한 일방향 암호화(단방향 해시 함수)로 저장하고, 주민등록번호 등 고유식별정보와 계좌정보 등은 안전한 암호 알고리즘으로 양방향 암호화하여 저장 및 전송함",
        "rubric": {
          "keywords": [
            ["일방향", "단방향", "해시", "비밀번호"],
            ["양방향", "고유식별정보", "주민등록번호", "암호화"]
          ],
          "all_match_points": 4,
          "partial_match_points": 2
        }
      }
    ],
    "model_answer": "1) 접근통제: IP 제한 및 접속 권한 관리를 통해 비인가 접근 차단.\n2) 접속기록: 1년(고유식별 2년) 이상 보관 및 월 1회 점검, 위변조 방지 백업.\n3) 암호화: 비밀번호는 일방향 해시, 고유식별정보/계좌정보는 양방향 암호화 저장 및 전송 구간 암호화.",
    "explanation": "안전성 확보조치 기준의 3대 기술 통제는 인가된 자만 접근하는 접근통제, 사후 추적성을 확보하는 접속기록 관리, 데이터 유출 시 무력화하는 암호화입니다.",
    "difficulty": "medium",
    "tags": ["안전성확보조치", "접근통제", "접속기록", "암호화"]
  }
]

# 신규 실무형 2문항 (Q-PRAC-007, Q-PRAC-008)
NEW_PRAC_QUESTIONS = [
  {
    "id": "Q-PRAC-007",
    "type": "practical",
    "category": "네트워크 보안",
    "score": 16,
    "concept_id": "CON-NET-01",
    "source_id": "SRC-02",
    "source_page": 16,
    "question": "[실무형] 다음은 사내 FTP 서버(포트 21)에서 침입탐지시스템(Snort)에 탐지된 로그와 패킷 헤더 정보이다. 물음에 답하시오.\n\n[Snort Rule]\nalert tcp any any -> any 21 (content:\"anonymous\"; nocase; msg:\"Anonymous FTP attempt\"; sid:1000012;)\n\n[탐지 패킷 로그]\nTCP TTL:64 TOS:0x10 ID:5450 IpLen:20 DgmLen:68 DF\n***AP*** Seq: 0xE95B8593 Ack: 0x7D3F3893 Win:0x1D TcpLen:32\nPayload: anonymous\\r\\n\n\n1) 등록된 Snort 룰의 탐지 조건(프로토콜, 포트, 옵션 등)의 의미를 설명하시오. (8점)\n2) 패킷 헤더의 '***AP***' 플래그가 나타내는 의미와, 공격자가 anonymous 계정 접근을 시도하는 보안상의 위협을 설명하시오. (8점)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 8,
        "prompt": "Snort 룰의 상세 분석",
        "model_answer": "모든 송신지 IP/포트에서 목적지 포트 21번(FTP)으로 전송되는 TCP 트래픽 중, 페이로드에 대소문자 구분 없이(nocase) 'anonymous' 문자열이 포함된 패킷을 탐지하여 alert을 발생시키고 'Anonymous FTP attempt' 메시지와 SID 1000012를 부여하는 룰",
        "rubric": {
          "keywords": [
            ["21", "FTP", "포트"],
            ["TCP"],
            ["anonymous", "익명"],
            ["nocase", "대소문자"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      },
      {
        "sub_id": 2,
        "score": 8,
        "prompt": "TCP 플래그 분석 및 익명 FTP 공격 위협",
        "model_answer": "AP 플래그는 ACK(수신확인)와 PSH(데이터 즉시 상위 계층 전송) 플래그가 동시에 설정된 것으로 실제 애플리케이션 데이터가 전송 중임을 의미함. anonymous FTP 접근 시도는 인증 없이 서버에 로그인하여 시스템 정보 수집, 악성코드 업로드, 민감 파일 다운로드 등의 침해사고를 유발할 수 있음",
        "rubric": {
          "keywords": [
            ["ACK", "PSH", "푸시"],
            ["인증 없이", "익명", "업로드", "다운로드", "정보 유출"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      }
    ],
    "model_answer": "1) TCP 21번 FTP 포트로 향하는 패킷 중 'anonymous'가 대소문자 무관하게 포함된 트래픽을 탐지하여 경보를 발생시킴.\n2) AP는 ACK+PSH 플래그 조합으로 데이터 버퍼링 없이 즉시 전송함을 뜻하며, 익명 FTP 접근 허용 시 불법 파일 업로드 및 정보 유출 위험이 발생함.",
    "explanation": "FTP 서비스의 익명 접근 허용은 초기 침투의 주요 경로입니다. PSH 플래그는 데이터를 즉시 수신 애플리케이션에 전달하도록 요구합니다.",
    "difficulty": "high",
    "tags": ["Snort", "FTP", "TCP플래그", "AP플래그", "실무형"]
  },
  {
    "id": "Q-PRAC-008",
    "type": "practical",
    "category": "네트워크 보안",
    "score": 16,
    "concept_id": "CON-NET-03",
    "source_id": "SRC-03",
    "source_page": 35,
    "question": "[실무형] DNS 서버(BIND)를 운용 중인 시스템에서 DNS Zone Transfer(영역 전송) 취약점이 발견되었다. 다음 물음에 답하시오.\n\n[외부 공격자의 질의 명령]\n$ dig @ns.test.co.kr test.co.kr AXFR\n\n1) 공격자가 'AXFR' 질의를 통해 노출시킬 수 있는 정보와 이로 인한 보안 위협을 설명하시오. (8점)\n2) BIND DNS 설정 파일(/etc/named.conf)에서 비인가된 외부 호스트의 영역 전송을 원천 차단하기 위한 'allow-transfer' 지시자 설정 구문을 작성하시오. (단, 신뢰하는 2차 네임서버 192.168.10.2에서만 허용하거나 전체 차단하는 구문 기술) (8점)",
    "sub_questions": [
      {
        "sub_id": 1,
        "score": 8,
        "prompt": "Zone Transfer(AXFR) 취약점 및 보안 위협 분석",
        "model_answer": "AXFR은 해당 도메인에 등록된 모든 호스트 이름, 서브도메인, IP 주소 매핑 등 전체 DNS 영역(Zone) 데이터를 일괄 전송받는 명령으로, 공격자에게 조직 내부의 네트워크 토폴로지, 주요 서버 목록 및 공격 타깃 정보를 고스란히 노출하는 정찰 위협을 초래함",
        "rubric": {
          "keywords": [
            ["전체", "영역", "Zone", "호스트"],
            ["서브도메인", "IP", "매핑"],
            ["정찰", "정보 노출", "토폴로지", "서버 목록"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      },
      {
        "sub_id": 2,
        "score": 8,
        "prompt": "named.conf allow-transfer 차단 설정 구문",
        "model_answer": "allow-transfer { none; }; 또는 특정 슬레이브 IP만 지정: allow-transfer { 192.168.10.2; };",
        "rubric": {
          "keywords": [
            ["allow-transfer"],
            ["none;", "192.168.10.2;"]
          ],
          "all_match_points": 8,
          "partial_match_points": 4
        }
      }
    ],
    "model_answer": "1) AXFR은 전체 Zone 데이터를 덤프하는 명령으로 내부 호스트, IP, 서브도메인 등 전체 네트워크 자산 구조가 공격자에게 노출됩니다.\n2) 설정: allow-transfer { 192.168.10.2; }; 또는 allow-transfer { none; };",
    "explanation": "DNS Zone Transfer는 원칙적으로 Primary와 Secondary 네임서버 간 동기화에만 사용되어야 하며, allow-transfer 지시자로 엄격히 IP를 제한해야 합니다.",
    "difficulty": "high",
    "tags": ["DNS", "ZoneTransfer", "AXFR", "allow-transfer", "named.conf", "실무형"]
  }
]

print("Script defined successfully!")
