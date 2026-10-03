import json
import copy

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Create modified copy
modified = copy.deepcopy(questions)

for q in modified:
    if q["id"] == "Q-PRAC-002":
        q["source_page"] = 5
    elif q["id"] == "Q-PRAC-006":
        q["source_page"] = 6
    elif q["id"] == "Q-SHORT-036":
        q["category"] = "네트워크 보안"
        q["concept_id"] = "CON-NET-01"
        q["source_id"] = "SRC-01"
        q["source_page"] = 21
        q["question"] = "DDoS, APT 등 공격 수행 시 악성코드가 C&C(Command and Control) 서버와 통신하기 위해 도메인명을 지속적이고 무작위로 동적 생성하여 보안장비의 도메인 기반 탐지 및 IP/URL 차단을 우회하기 위한 기법(알고리즘)은 무엇인가?"
        q["answer"] = "DGA"
        q["accepted_answers"] = ["DGA", "Domain Generation Algorithm", "도메인 생성 알고리즘", "도메인생성알고리즘"]
        q["grading_mode"] = "normalized"
        q["score"] = 3
        q["explanation"] = "DGA(Domain Generation Algorithm)는 C&C 서버의 IP나 도메인이 차단되는 것을 방지하기 위해 날짜나 시드값을 기반으로 무작위의 도메인 목록을 자동 생성하는 알고리즘으로, 공격자와 봇넷 간의 통신 생존성을 보장하기 위해 사용됩니다."
        q["difficulty"] = "medium"
        q["tags"] = ["DGA", "C&C", "도메인생성알고리즘", "APT", "DDoS"]
    elif q["id"] == "Q-DESC-005":
        q["category"] = "네트워크 보안"
        q["concept_id"] = "CON-NET-01"
        q["source_id"] = "SRC-02"
        q["source_page"] = 13
        q["score"] = 12
        q["question"] = "침입탐지시스템(IDS)에서 사용하는 핵심 침입탐지 방식인 '오용 탐지(Misuse Detection)'와 '이상 탐지(Anomaly Detection)'에 대하여 다음 물음에 답하시오.\n\n1) 오용 탐지(Misuse Detection)의 개념 및 동작 원리를 기술하시오. (3점)\n2) 이상 탐지(Anomaly Detection)의 개념 및 동작 원리를 기술하시오. (3점)\n3) 오용 탐지의 장점을 기술하시오. (3점)\n4) 오용 탐지의 한계점(단점)을 기술하시오. (3점)"
        q["sub_questions"] = [
            {
                "sub_id": 1,
                "score": 3,
                "prompt": "1) 오용 탐지(Misuse Detection)의 개념 및 동작 원리",
                "model_answer": "기존에 이미 알려진 공격 패턴(시그니처)을 룰로 데이터베이스화하여 등록한 후, 수집된 패킷이나 이벤트가 등록된 시그니처와 일치하는지 비교하여 침입 여부를 판단한다.",
                "rubric": {
                    "keywords": [
                        ["알려진 공격", "패턴", "시그니처", "룰"],
                        ["일치", "비교", "매칭"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 2,
                "score": 3,
                "prompt": "2) 이상 탐지(Anomaly Detection)의 개념 및 동작 원리",
                "model_answer": "시스템 및 네트워크의 정상적인 사용자 행위나 트래픽 패턴을 사전에 프로파일링하여 기준(베이스라인)을 확립한 후, 통계적 분석이나 이상치 분석을 통해 이 기준을 유의미하게 벗어나는 비정상 행위를 탐지한다.",
                "rubric": {
                    "keywords": [
                        ["정상", "베이스라인", "프로파일링"],
                        ["비정상", "통계", "벗어나는", "이상 행위", "이상치"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 3,
                "score": 3,
                "prompt": "3) 오용 탐지의 장점",
                "model_answer": "명확하게 정의된 공격 시그니처와 일치하는 경우에만 경보를 발생시키므로, 정상 트래픽을 공격으로 잘못 판단하는 오탐률(False Positive)이 매우 낮고 분석 및 처리가 명확하다.",
                "rubric": {
                    "keywords": [
                        ["오탐률", "오탐", "false positive"],
                        ["낮음", "적음", "감소", "낮다"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            },
            {
                "sub_id": 4,
                "score": 3,
                "prompt": "4) 오용 탐지의 한계점(단점)",
                "model_answer": "시그니처 데이터베이스에 등록되어 있지 않은 새로운 변종 공격이나 제로데이(Zero-day) 공격은 탐지할 수 없으며, 최신 공격을 탐지하기 위해 지속적인 패턴 및 룰 업데이트가 필수적이다.",
                "rubric": {
                    "keywords": [
                        ["새로운 공격", "신종", "제로데이", "미등록", "변종", "미지의"],
                        ["탐지 불가", "탐지할 수 없", "업데이트", "한계"]
                    ],
                    "all_match_points": 3,
                    "partial_match_points": 1.5
                }
            }
        ]
        q["model_answer"] = "1) 알려진 공격 시그니처를 등록하여 유입되는 패킷과 일치 여부를 비교·탐지\n2) 정상 행위의 베이스라인을 프로파일링한 후 통계적 분석을 통해 벗어나는 비정상 행위 탐지\n3) 시그니처 기반으로 정밀 매칭되므로 오탐률(False Positive)이 매우 낮음\n4) 미등록된 신종 공격 및 제로데이 공격 탐지가 불가능하며 지속적 룰 업데이트 필요"
        q["explanation"] = "IDS 침입탐지 기법은 시그니처 기반의 오용 탐지(지식 기반)와 베이스라인 기반의 이상 탐지(행위 기반)로 양분됩니다. 오용 탐지는 낮은 오탐률이 장점이나 제로데이 공격 탐지가 불가능한 한계가 있습니다."
        q["difficulty"] = "medium"
        q["tags"] = ["IDS", "오용탐지", "이상탐지", "시그니처", "침입탐지"]
    elif q["id"] == "Q-PRAC-003":
        q["category"] = "시스템 보안"
        q["concept_id"] = "CON-SYS-03"
        q["source_id"] = "SRC-02"
        q["source_page"] = 41
        q["score"] = 16
        q["question"] = "다음은 리눅스 서버에서 운영 중인 정기 백업 스크립트와 생성된 백업 결과 파일의 권한 설정이다. 내용을 분석하고 각 물음에 답하시오.\n\n[백업 스크립트: /usr/local/bin/backup]\n#!/bin/sh\ndat=`date +%Y%m%d`\ntar -cvzf /data/backup/etc_$dat.tgz /etc/*\ntar -cvzf /data/backup/home_$dat.tgz /home/*\n\n[백업 결과 파일 권한]\n-rw-r--r-- 1 root root 15421038 Oct 01 03:00 /data/backup/etc_20231001.tgz\n-rw-r--r-- 1 root root 89234120 Oct 01 03:05 /data/backup/home_20231001.tgz\n\n1) 생성된 백업 결과 파일의 권한(-rw-r--r--)을 검토하여 발생할 수 있는 보안 문제점을 설명하시오. (5점)\n2) 백업 스크립트 내에서 백업 파일 생성 시 일반 사용자의 접근을 차단하도록 umask를 안전하게 변경한 후, 백업 완료 시 원래의 기본값(022)으로 복원하는 스크립트 수정 방안을 기술하시오. (5점)\n3) operator 사용자 계정만 백업 스크립트(/usr/local/bin/backup)를 단독 실행할 수 있도록 소유자 및 파일 권한을 설정하는 리눅스 명령어 2줄을 기술하시오. (6점)"
        q["sub_questions"] = [
            {
                "sub_id": 1,
                "score": 5,
                "prompt": "1) 백업 결과 파일 권한(-rw-r--r--)의 보안 문제점",
                "model_answer": "백업 파일의 Other 권한이 r--(읽기 허용)로 설정되어 있어 root가 아닌 일반 사용자도 백업 아카이브를 읽고 복사할 수 있다. 특히 /etc 아카이브에는 /etc/passwd, /etc/shadow 등 핵심 인증/설정 파일이 포함되어 있어 기밀성 침해 및 계정 탈취 위험이 존재한다.",
                "rubric": {
                    "keywords": [
                        ["일반 사용자", "other", "다른 계정", "모든 사용자"],
                        ["읽기", "조회", "다운로드", "열람", "접근"],
                        ["shadow", "passwd", "기밀성", "중요 파일", "인증 정보"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 2,
                "score": 5,
                "prompt": "2) umask를 적용한 스크립트 보안 보완 방안",
                "model_answer": "tar 아카이브 생성 전 `umask 027` (또는 `umask 077`)을 설정하여 타인의 읽기 권한이 제거된 파일이 생성되도록 하고, 백업 완료 후 `umask 022`로 기본값을 복원한다.",
                "rubric": {
                    "keywords": [
                        ["umask 027", "umask 077", "umask 266", "umask 007"],
                        ["umask 022", "복원", "원래", "초기화"]
                    ],
                    "all_match_points": 5,
                    "partial_match_points": 2.5
                }
            },
            {
                "sub_id": 3,
                "score": 6,
                "prompt": "3) operator 사용자 전용 실행 권한 설정 명령어",
                "model_answer": "chown operator /usr/local/bin/backup\nchmod 700 /usr/local/bin/backup",
                "rubric": {
                    "keywords": [
                        ["chown operator", "chown operator /usr/local/bin/backup"],
                        ["chmod 700", "chmod 700 /usr/local/bin/backup", "chmod u=rwx"]
                    ],
                    "all_match_points": 6,
                    "partial_match_points": 3
                }
            }
        ]
        q["model_answer"] = "1) 타인(Other)에게 읽기 권한이 부여되어 일반 사용자가 /etc/shadow 등 시스템 중요 설정 및 인증 파일을 열람할 수 있는 위험이 있음\n2) 백업 명령 전 umask 027(또는 077)을 설정하여 권한을 제한하고, 백업 후 umask 022로 복원\n3) chown operator /usr/local/bin/backup\nchmod 700 /usr/local/bin/backup"
        q["explanation"] = "백업 파일은 시스템의 핵심 설정 및 기밀 정보를 포함하므로 타인의 읽기 권한을 제거해야 합니다. 스크립트 내에서 umask 027/077로 권한을 제한하고, 스크립트 자체도 chown 및 chmod 700으로 전용 관리자만 실행할 수 있도록 접근통제해야 합니다."
        q["difficulty"] = "high"
        q["tags"] = ["Linux", "umask", "백업보안", "파일권한", "chown", "chmod"]

# Write to a temporary file and test
with open("test_modified_questions.json", "w", encoding="utf-8") as f:
    json.dump(modified, f, ensure_ascii=False, indent=2)

print("Test questions generated.")
