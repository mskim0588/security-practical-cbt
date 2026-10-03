# -*- coding: utf-8 -*-
"""
Batch 3 - Chunk 3: SRC-06 System Security (10 questions)
Q-SHORT-101 ~ Q-SHORT-106 (6 short)
Q-DESC-040 ~ Q-DESC-042 (3 desc)
Q-PRAC-022 (1 prac)
"""

CHUNK_3_QUESTIONS = [
    {
        "id": "Q-SHORT-101",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "리눅스 및 유닉스 시스템에서 사용자가 로그인한 시점부터 로그아웃할 때까지 실행한 모든 명령어의 이름, 실행한 사용자 계정, 소요된 CPU 시간, 터미널 정보 등을 기록하는 `acct` 또는 `pacct` 로그 파일의 내용을 확인·조회하기 위해 사용하는 명령어의 명칭을 쓰시오.",
        "answer": "lastcomm",
        "accepted_answers": ["lastcomm"],
        "grading_mode": "strict",
        "explanation": "lastcomm 명령어는 acct/pacct 프로세스 회계 로그 파일의 내용을 확인하여 사용자가 입력한 명령어 기록을 추적합니다 (SRC-06 p.213, 29회 기출).",
        "source_id": "SRC-06",
        "source_page": 213,
        "concept_id": "CON-SYS-03",
        "difficulty": "medium",
        "tags": ["lastcomm", "pacct", "acct", "시스템로그", "명령어추적"]
    },
    {
        "id": "Q-SHORT-102",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "리눅스 시스템에서 시스템 로그 파일이 무한정 비대해져 디스크 저장 공간을 고갈시키는 장애를 방지하기 위해, 설정 파일(`/etc/logrotate.conf`)에 정의된 주기에 따라 로그 파일을 자동으로 순환(Rotate), 압축(Compress) 및 신규 생성해 주는 로그 관리 데몬 유틸리티의 명칭을 쓰시오.",
        "answer": "logrotate",
        "accepted_answers": ["logrotate"],
        "grading_mode": "strict",
        "explanation": "logrotate는 주기적으로 로그 파일을 순환, 백업, 압축하고 빈 로그 파일을 새로 생성해 주는 로그 관리 도구입니다 (SRC-06 p.207, 12회 기출).",
        "source_id": "SRC-06",
        "source_page": 207,
        "concept_id": "CON-SYS-03",
        "difficulty": "easy",
        "tags": ["logrotate", "로그순환", "시스템관리", "로그백업"]
    },
    {
        "id": "Q-SHORT-103",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "마이크로소프트 윈도우 운영체제(Windows Vista 이상)에서 노트북 분실이나 저장매체 도난으로 인한 기밀 데이터 유출을 방지하기 위해 하드 디스크 볼륨 전체에 대해 투명 암호화를 제공하는 볼륨 단위 암호화 기능의 명칭을 영문 또는 국문으로 쓰시오.",
        "answer": "비트락커",
        "accepted_answers": ["비트락커", "비트 락커", "BitLocker", "Bit Locker"],
        "grading_mode": "normalized",
        "explanation": "비트 락커(BitLocker)는 윈도우 운영체제에서 제공하는 볼륨 단위 데이터 암호화 기능으로 볼륨에 저장된 파일과 폴더를 자동으로 암호화합니다 (SRC-06 p.61).",
        "source_id": "SRC-06",
        "source_page": 61,
        "concept_id": "CON-SYS-01",
        "difficulty": "easy",
        "tags": ["비트락커", "BitLocker", "볼륨암호화", "윈도우보안", "전체디스크암호화"]
    },
    {
        "id": "Q-SHORT-104",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "윈도우 운영체제에서 악성 소프트웨어가 관리자 모르게 시스템 설정을 무단 변경하거나 악성 프로그램을 설치하는 것을 차단하기 위해, 관리자 권한이 필요한 작업 수행 시 동의 대화상자(프롬프트)를 띄워 사용자의 승인을 확인하는 계정 접근 통제 기술의 영문 약어를 쓰시오.",
        "answer": "UAC",
        "accepted_answers": ["UAC", "User Account Control", "사용자 계정 컨트롤", "사용자계정컨트롤"],
        "grading_mode": "normalized",
        "explanation": "UAC(User Account Control; 사용자 계정 컨트롤)는 관리자 권한 승격 시 프롬프트를 통해 사용자 동의를 확인하는 윈도우 계정 접근통제 기능입니다 (SRC-06 p.51).",
        "source_id": "SRC-06",
        "source_page": 51,
        "concept_id": "CON-SYS-01",
        "difficulty": "easy",
        "tags": ["UAC", "UserAccountControl", "사용자계정컨트롤", "윈도우보안", "권한승격"]
    },
    {
        "id": "Q-SHORT-105",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "마이크로소프트 윈도우 운영체제에서 사용되는 실행 파일(EXE), 동적 링크 라이브러리(DLL) 등의 표준 32비트/64비트 실행 파일 형식 구조로서, DOS 헤더, NT 헤더, 섹션 헤더 및 코드/데이터 섹션 등으로 구성된 포맷의 영문 약어를 쓰시오.",
        "answer": "PE",
        "accepted_answers": ["PE", "Portable Executable", "PE 포맷", "PE 파일"],
        "grading_mode": "normalized",
        "explanation": "PE(Portable Executable) 포맷은 윈도우의 표준 실행 파일 형식으로 DOS Header, NT Header, Section Header 등으로 구성됩니다 (SRC-06 p.81).",
        "source_id": "SRC-06",
        "source_page": 81,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["PE", "PortableExecutable", "PE포맷", "PE파일", "윈도우실행파일"]
    },
    {
        "id": "Q-SHORT-106",
        "type": "short",
        "category": "시스템 보안",
        "score": 3,
        "question": "운영체제에서 둘 이상의 프로세스가 더 이상 진행하지 못하고 영구 대기하는 교착상태(Deadlock)의 4대 발생 조건 중, 둘 이상의 프로세스가 순환 형태로 자원을 점유하면서 다음 프로세스가 점유한 자원을 요구하여 자원 할당 그래프 상에서 사이클(Cycle)을 형성하는 조건의 명칭을 국문 또는 영문으로 쓰시오.",
        "answer": "환형 대기",
        "accepted_answers": ["환형 대기", "환형대기", "Circular Wait", "원형 대기", "순환 대기"],
        "grading_mode": "normalized",
        "explanation": "환형 대기(Circular Wait)는 두 개 이상의 프로세스 간 자원의 점유와 대기가 하나의 원형 고리를 구성하는 교착상태 발생 조건입니다 (SRC-06 p.18).",
        "source_id": "SRC-06",
        "source_page": 18,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["교착상태", "Deadlock", "환형대기", "CircularWait", "운영체제"]
    },
    {
        "id": "Q-DESC-040",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "question": "운영체제 환경에서 둘 이상의 프로세스가 자원을 점유한 채 서로 상대방의 자원을 무한정 대기하는 교착상태(Deadlock)에 대하여 다음 물음에 답하시오.\n\n1) 교착상태가 발생하기 위해 동시에 충족되어야 하는 4대 필요조건의 명칭과 각각의 기술적 의미를 서술하시오. (6점)\n2) 교착상태를 사전에 예방(Prevention)하기 위한 접근 방법과, 시스템 성능 관점에서 발생하는 한계점을 서술하시오. (3점)\n3) 교착상태 회피(Avoidance) 기법의 개념과 대표적인 알고리즘의 명칭을 쓰시오. (3점)",
        "model_answer": "1) 4대 발생 조건:\n- 상호 배제 (Mutual Exclusion): 자원은 한 번에 하나의 프로세스만이 독점적으로 사용할 수 있음\n- 점유와 대기 (Hold and Wait): 프로세스가 최소 하나의 자원을 점유한 상태에서 다른 프로세스에 할당된 자원을 요청하여 대기함\n- 비선점 (Non-preemption): 다른 프로세스가 점유한 자원은 강제로 빼앗을 수 없고, 점유한 프로세스가 작업을 마치고 스스로 해제할 때까지 기다려야 함\n- 환형 대기 (Circular Wait): 프로세스 간 자원 점유와 요구 관계가 순환 형태로 원형 고리를 형성함\n2) 예방 기법 및 한계점: 4가지 발생 조건 중 최소 하나를 사전에 부정(배제)하여 교착상태 발생 가능성을 원천 차단하는 방식이다. 그러나 모든 자원을 한 번에 할당하거나 자원 요청 순서를 강제해야 하므로 심각한 시스템 자원 낭비와 프로세스 기아(Starvation) 현상이 발생한다.\n3) 회피 기법 및 대표 알고리즘: 교착상태 발생을 배제하지 않고 시스템이 안전 상태(Safe State)를 유지할 수 있는 범위 내에서만 자원을 동적으로 할당하는 방식으로, 대표적으로 다익스트라(Dijkstra)의 '은행원 알고리즘(Banker's Algorithm)'이 있다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 6,
                "prompt": "1) 교착상태 4대 발생 조건의 명칭 및 기술적 의미",
                "model_answer": "상호 배제(독점 점유), 점유와 대기(자원 보유 후 추가 대기), 비선점(강제 회수 불가), 환형 대기(순환 대기 고리 형성)",
                "rubric": {
                    "keywords": [
                        ["상호 배제", "mutual exclusion", "독점"],
                        ["점유와 대기", "hold and wait", "점유 및 대기"],
                        ["비선점", "non-preemption"],
                        ["환형 대기", "circular wait", "원형"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 교착상태 예방 기법의 접근 방식 및 자원 관점의 한계점",
                "model_answer": "4대 조건 중 하나를 배제하여 원천 차단하며, 심각한 자원 낭비와 비효율이 발생한다.",
                "rubric": {
                    "keywords": [
                        ["조건 부정", "조건 방지", "배제", "조건 중"],
                        ["자원 낭비", "비효율", "낭비"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 교착상태 회피 기법의 개념 및 대표 알고리즘",
                "model_answer": "안전 상태를 유지하도록 자원을 동적으로 할당하며 대표적으로 은행원 알고리즘이 있다.",
                "rubric": {
                    "keywords": [
                        ["은행원", "은행가", "banker", "은행원 알고리즘"],
                        ["안전 상태", "회피", "동적 할당"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ],
        "explanation": "교착상태 4대 조건은 상호배제, 점유대기, 비선점, 환형대기이며, 예방/회피(은행원 알고리즘)/탐지/회복으로 다룹니다 (SRC-06 p.17, 18).",
        "source_id": "SRC-06",
        "source_page": 17,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["교착상태", "Deadlock", "상호배제", "점유대기", "비선점", "환형대기", "은행원알고리즘"]
    },
    {
        "id": "Q-DESC-041",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "question": "마이크로소프트 윈도우 운영체제의 대표적인 파일 시스템인 NTFS(New Technology File System)와 이전 FAT32 파일 시스템을 비교하고, NTFS가 제공하는 핵심 보안 기능에 대하여 다음 물음에 답하시오.\n\n1) FAT32 파일 시스템과 비교하여 NTFS가 보안 및 파일 권한 제어 관점에서 가지는 기술적 차이점을 서술하시오. (4점)\n2) NTFS 환경에서 파일 및 폴더 레벨로 기밀성을 보장하기 위해 운영체제 차원에서 자체 제공하는 암호화 기능의 명칭과 동작 방식을 서술하시오. (4점)\n3) 시스템 비정상 종료나 전원 장애 발생 시 데이터 손상을 방지하고 빠른 복구를 지원하는 NTFS의 트랜잭션 저널링(Journaling) 기능의 역할을 서술하시오. (4점)",
        "model_answer": "1) 파일 권한 제어 차이점: FAT32는 파일 및 디렉터리 레벨에서 사용자별 접근 권한(ACL)을 설정할 수 없어 모든 로컬 사용자가 파일에 자유롭게 접근할 수 있으나, NTFS는 세분화된 접근제어목록(ACL/ACE)을 지원하여 사용자 및 그룹별로 개별적인 읽기, 쓰기, 실행, 수정 권한을 차등 부여하여 인가된 사용자만 접근하도록 통제할 수 있다.\n2) EFS 암호화 기능 및 동작 방식: EFS(Encrypting File System; 파일 암호화 시스템)이다. 사용자가 파일이나 폴더를 암호화하도록 지정하면 대칭키(FEK; File Encryption Key)로 파일 내용을 암호화하고, 해당 FEK를 사용자의 공개키로 암호화하여 파일 헤더에 저장함으로써 해당 인증서를 보유한 사용자 본인만이 투명하게 복호화하여 열람할 수 있도록 한다.\n3) 트랜잭션 저널링 역할: 파일 시스템 메타데이터 변경 내역을 실제 디스크 블록에 반영하기 전에 트랜잭션 로그 파일($LogFile)에 사전 기록(저널링)함으로써, 급작스러운 정전이나 시스템 크래시 발생 시 로그를 기반으로 롤백(Rollback)하거나 재수행(Redo)하여 디스크 전체를 검사하지 않고도 파일 시스템의 일관성과 무결성을 신속하게 복구한다.",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) FAT32 대비 NTFS의 파일 권한 제어 및 보안 차이점",
                "model_answer": "FAT32는 파일별 권한 설정이 불가능하나, NTFS는 ACL을 통해 사용자별 세부 접근 권한 통제가 가능하다.",
                "rubric": {
                    "keywords": [
                        ["acl", "접근제어", "접근 권한", "권한 설정"],
                        ["사용자별", "차등", "보안 기능", "통제"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) NTFS 자체 파일 암호화 기능 명칭 및 동작 방식",
                "model_answer": "EFS(Encrypting File System)로, 대칭키(FEK)와 사용자 공개키를 결합하여 파일 단위 투명 암호화를 제공한다.",
                "rubric": {
                    "keywords": [
                        ["efs", "encrypting file system", "파일 암호화 시스템"],
                        ["공개키", "대칭키", "fek", "투명", "인증서"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) NTFS 저널링 기능의 장애 복구 및 무결성 역할",
                "model_answer": "트랜잭션 로그를 사전 기록하여 정전 등 장애 시 일관성을 신속하게 복구한다.",
                "rubric": {
                    "keywords": [
                        ["저널링", "로그", "트랜잭션", "journaling"],
                        ["복구", "일관성", "무결성", "정전", "크래시"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "NTFS는 ACL 권한 관리, EFS 암호화, 저널링 로그 복구 등 강력한 엔터프라이즈 보안 및 안정성 기능을 제공합니다 (SRC-06 p.79).",
        "source_id": "SRC-06",
        "source_page": 79,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["NTFS", "FAT32", "EFS", "ACL", "저널링", "파일시스템보안"]
    },
    {
        "id": "Q-DESC-042",
        "type": "descriptive",
        "category": "시스템 보안",
        "score": 12,
        "question": "윈도우(Windows) 운영체제에서 기본적으로 활성화되어 네트워크 공유 등을 지원하는 NetBIOS 바인딩 서비스와 관련하여 다음 물음에 답하시오.\n\n1) Windows에서 NetBIOS 바인딩 서비스(NetBIOS over TCP/IP)를 활성화해 둘 경우 외부 또는 내부 네트워크 공격자에게 노출될 수 있는 보안상 취약점 이유를 서술하시오. (4점)\n2) 윈도우 네트워크 연결 제어판 실행 명령어인 `ncpa.cpl`을 활용하여 해당 NetBIOS 바인딩 취약점을 해결하기 위한 구체적인 보안 설정 절차를 서술하시오. (4점)\n3) 제어판 네트워크 속성 변경 외에, 윈도우 서비스 관리자(`services.msc`)에서 NetBIOS 관련 보안 위험을 원천 차단하기 위해 중지 및 사용 안 함으로 설정해야 하는 서비스의 명칭을 쓰시오. (4점)",
        "model_answer": "1) 보안 취약점 이유: NetBIOS over TCP/IP(포트 137~139, 445) 서비스가 외부 또는 비인가 네트워크에 노출될 경우, Null Session 접속 등을 악용하여 시스템의 사용자 계정 목록, 공유 폴더 목록, 도메인 정보 및 시스템 설정 정보가 무단 유출될 수 있으며, SMB 취약점을 통한 원격 코드 실행 및 랜섬웨어 전파 경로로 악용될 수 있다.\n2) ncpa.cpl 설정 절차:\n- `ncpa.cpl` 실행 후 현재 활성화된 '이더넷(로컬 영역 연결)'의 속성 창을 연다.\n- '인터넷 프로토콜 버전 4(TCP/IPv4)'를 선택하고 [속성] 버튼을 클릭한다.\n- [고급] 버튼을 클릭한 후 [WINS] 탭으로 이동한다.\n- 하단의 NetBIOS 설정 항목에서 'NetBIOS over TCP/IP 사용 안 함' 라디오 버튼을 선택하고 확인을 눌러 적용한다.\n3) 중지해야 하는 윈도우 서비스 명칭: TCP/IP NetBIOS Helper (서비스명: lmhosts)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 4,
                "prompt": "1) NetBIOS 바인딩 서비스 활성화 시 보안상 취약한 이유",
                "model_answer": "계정 목록, 공유 폴더, 시스템 정보가 비인가자에게 유출되고 SMB 침해 공격에 노출될 수 있다.",
                "rubric": {
                    "keywords": [
                        ["정보 유출", "공유 폴더", "계정 목록", "계정 정보", "시스템 정보"],
                        ["null session", "smb", "139", "445", "랜섬웨어", "공격"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) ncpa.cpl을 통한 NetBIOS over TCP/IP 비활성화 설정 절차",
                "model_answer": "ncpa.cpl 실행 -> 네트워크 어댑터 속성 -> IPv4 속성 -> 고급 -> WINS 탭 -> 'NetBIOS over TCP/IP 사용 안 함' 선택",
                "rubric": {
                    "keywords": [
                        ["ipv4", "tcp/ipv4", "속성"],
                        ["wins", "wins 탭", "고급"],
                        ["사용 안 함", "netbios over tcp/ip 사용 안 함"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) NetBIOS 관련 윈도우 서비스 명칭",
                "model_answer": "TCP/IP NetBIOS Helper (lmhosts)",
                "rubric": {
                    "keywords": [
                        ["tcp/ip netbios helper", "netbios helper", "lmhosts"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "NetBIOS over TCP/IP는 계정 및 시스템 정보 유출에 취약하므로 ncpa.cpl의 WINS 탭에서 비활성화하고 TCP/IP NetBIOS Helper 서비스를 중지합니다 (SRC-06 p.299, 23회 기출).",
        "source_id": "SRC-06",
        "source_page": 299,
        "concept_id": "CON-SYS-01",
        "difficulty": "medium",
        "tags": ["NetBIOS", "ncpa.cpl", "WINS", "TCP/IP_NetBIOS_Helper", "윈도우보안설정"]
    },
    {
        "id": "Q-PRAC-022",
        "type": "practical",
        "category": "시스템 보안",
        "score": 16,
        "question": "다음은 리눅스 서버에서 아파치 웹 서버의 접근 로그(`/var/log/httpd/access_log`)를 관리하기 위해 작성된 logrotate 설정 파일(`/etc/logrotate.d/httpd`)의 내용이다. 설정을 분석하고 각 질문에 답하시오.\n\n[logrotate 설정 파일 내용]\n/var/log/httpd/*log {\n    weekly\n    rotate 4\n    create 0640 root adm\n    compress\n    missingok\n    notifempty\n    sharedscripts\n    postrotate\n        /bin/systemctl reload httpd.service > /dev/null 2>/dev/null || true\n    endscript\n}\n\n1) 위 설정 파일에서 지정된 `weekly`, `rotate 4`, `create 0640 root adm`, `compress` 지시자의 기술적 역할을 각각 서술하시오. (8점)\n2) 관리자가 `compress` 옵션을 적용했을 때 생성되는 순환 로그 파일의 확장자 형태와, 만약 `postrotate` 스크립트를 정의하지 않았을 경우 웹 데몬(`httpd`)에서 발생할 수 있는 로그 기록 장애 현상을 서술하시오. (4점)\n3) 관리자가 수정한 logrotate 설정 파일의 문법 오류 여부를 실제 로그 파일 순환을 수행하지 않고 테스트(Dry-run)해 보는 점검 명령어 옵션과, 주기에 도달하지 않았더라도 강제로 순환을 즉시 실행하는 명령어 옵션을 각각 쓰시오. (4점)",
        "model_answer": "1) 지시자 기술적 역할:\n- weekly: 로그 파일을 1주일(주 단위) 주기로 순환(Rotate)한다.\n- rotate 4: 순환된 백업 로그 파일을 최대 4개까지 보관하며, 4개를 초과하는 가장 오래된 로그 파일은 자동 삭제한다.\n- create 0640 root adm: 기존 로그 파일 순환(이동) 직후 새로운 빈 로그 파일을 생성할 때, 퍼미션을 0640(소유자 rw-, 그룹 r--, 기타 ---), 소유자를 root, 소유 그룹을 adm으로 지정하여 생성한다.\n- compress: 순환되어 보관되는 이전 로그 파일들을 디스크 절약을 위해 gzip 형식(.gz)으로 압축하여 저장한다.\n2) 확장자 및 장애 원인:\n- 확장자 형태: `access_log-YYYYMMDD.gz` 또는 `access_log.1.gz` 형태의 gzip 압축 파일\n- 로그 기록 장애 현상: 리눅스는 파일명 기반이 아닌 파일 디스크립터(Inode)를 기준으로 파일을 기록하므로, 기존 로그 파일이 다른 이름으로 이동(Rename)된 후에도 아파치 프로세스가 여전히 이동된 이전 로그 파일의 파일 디스크립터를 물고 있어, 새로운 로그 파일이 생성되었음에도 새로운 파일에 로그가 기록되지 않고 순환된 과거 파일에 로그가 계속 기록되거나 로그 유실이 발생한다. 이를 방지하기 위해 postrotate에서 데몬을 리로드(reload)하여 파일 디스크립터를 새로 갱신해 주어야 한다.\n3) 점검 명령어 옵션:\n- 사전 테스트(Dry-run) 옵션: `logrotate -d /etc/logrotate.d/httpd` (또는 `--debug`)\n- 강제 즉시 실행 옵션: `logrotate -f /etc/logrotate.d/httpd` (또는 `--force`)",
        "sub_questions": [
            {
                "sub_id": 1,
                "score": 8,
                "prompt": "1) weekly, rotate 4, create 0640 root adm, compress의 각 역할",
                "model_answer": "weekly(주 단위 순환), rotate 4(4개 보관 후 삭제), create(권한 0640 소유자 root adm으로 빈 파일 생성), compress(gzip 압축 저장)",
                "rubric": {
                    "keywords": [
                        ["주 단위", "weekly", "1주일"],
                        ["4개", "rotate 4", "보관"],
                        ["0640", "새로 생성", "root", "adm", "생성"],
                        ["압축", "compress", "gzip"]
                    ],
                    "all_match_points": 8,
                    "partial_match_points": 4
                }
            },
            {
                "sub_id": 2,
                "score": 4,
                "prompt": "2) compress 확장자 및 postrotate 누락 시 로그 장애 현상",
                "model_answer": ".gz 확장자로 압축되며, reload를 하지 않으면 데몬이 기존 파일 디스크립터를 유지하여 새 파일에 로그가 기록되지 않는다.",
                "rubric": {
                    "keywords": [
                        ["gz", ".gz", "gzip"],
                        ["파일 디스크립터", "inode", "기록되지 않음", "새 파일", "reload", "리로드"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            },
            {
                "sub_id": 3,
                "score": 4,
                "prompt": "3) logrotate dry-run 테스트 옵션 및 강제 실행 옵션",
                "model_answer": "테스트(Dry-run)는 `-d` (또는 `--debug`), 강제 실행은 `-f` (또는 `--force`) 옵션을 사용한다.",
                "rubric": {
                    "keywords": [
                        ["-d", "--debug", "debug"],
                        ["-f", "--force", "force"]
                    ],
                    "all_match_points": 4,
                    "partial_match_points": 2
                }
            }
        ],
        "explanation": "logrotate는 weekly, rotate, create, compress 옵션으로 로그를 순환하고, postrotate를 통해 데몬을 reload하여 파일 디스크립터를 갱신하며, -d(테스트), -f(강제) 옵션을 제공합니다 (SRC-06 p.207, 12회 기출).",
        "source_id": "SRC-06",
        "source_page": 207,
        "concept_id": "CON-SYS-03",
        "difficulty": "hard",
        "tags": ["logrotate", "로그순환", "rotate", "compress", "create", "postrotate", "아파치로그"]
    }
]
