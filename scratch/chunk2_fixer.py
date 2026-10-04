# -*- coding: utf-8 -*-
"""
Chunk 2 Fixer: Q-SHORT-031 to Q-SHORT-060
Fixes:
- P1-1: Eliminates "표준 정답" placeholder in why_correct and embeds the official representative answer.
- P1-3: Replaces concept-inherited traps with question-specific, realistic traps.
"""

import json

CHUNK2_FIXES = {
    "Q-SHORT-031": {
        # Tripwire (무결성), Nessus (취약점 점검)
        "traps": [
            {
                "confused_term_or_misunderstanding": "Tripwire를 네트워크 침입차단시스템(방화벽)으로 혼동",
                "explanation": "Tripwire는 시스템 내부 주요 바이너리 및 설정 파일의 해시값(MD5/SHA)을 DB에 저장하고 주기적으로 대조하여 무단 변조를 탐지하는 무결성 검증 도구입니다."
            },
            {
                "confused_term_or_misunderstanding": "Nessus를 수동 패킷 스니핑 도구(Wireshark/tcpdump)로 혼동",
                "explanation": "Nessus는 원격 호스트의 오픈 포트, 실행 서비스 및 알려진 CVE 보안 취약점을 종합적으로 자동 스캔하고 리포트를 생성하는 취약점 진단 솔루션입니다."
            }
        ]
    },
    "Q-SHORT-032": {
        # 하트블리드 (Heartbleed)
        "ans_replace": "하트블리드",
        "traps": [
            {
                "confused_term_or_misunderstanding": "하트블리드를 단순 서비스 거부(DoS) 공격으로만 오해",
                "explanation": "하트블리드는 OpenSSL의 TLS Heartbeat 확장에서 요청 페이로드 길이 검증 누락으로 발생하며, 서버 프로세스 메모리에 상주하는 비밀키, 세션 쿠키, 사용자 패스워드 등 최대 64KB의 기밀 데이터가 외부로 유출되는 치명적인 정보 유출 취약점입니다."
            }
        ]
    },
    "Q-SHORT-033": {
        # PLT, GOT
        "traps": [
            {
                "confused_term_or_misunderstanding": "PLT(Procedure Linkage Table)와 GOT(Global Offset Table)의 역할 반대 서술",
                "explanation": "PLT는 동적 라이브러리 함수 호출을 연결하는 점프 코드 영역이며, 동적 링커가 해석한 실제 함수의 메모리 절대 주소를 최종 저장하고 캐싱하는 테이블은 GOT입니다."
            }
        ]
    },
    "Q-SHORT-034": {
        # ISMS-P 3개 영역: 관리체계 수립 및 운영, 보호대책 요구사항, 개인정보 처리 단계별 요구사항
        "traps": [
            {
                "confused_term_or_misunderstanding": "구 ISMS의 5단계(정책수립, 범위설정, 위험관리, 구현, 사후관리) 명칭을 기재",
                "explanation": "통합 ISMS-P 인증 기준의 3개 대영역은 '1. 관리체계 수립 및 운영(16개)', '2. 보호대책 요구사항(64개)', '3. 개인정보 처리 단계별 요구사항(22개)'입니다."
            }
        ]
    },
    "Q-SHORT-035": {
        # xinetd: no_access, only_from, instances
        "traps": [
            {
                "confused_term_or_misunderstanding": "xinetd 지시자 명칭을 TCP Wrapper의 hosts.allow/deny와 혼동",
                "explanation": "TCP Wrapper는 설정 파일(/etc/hosts.allow, /etc/hosts.deny)을 사용하는 반면, xinetd는 개별 서비스 설정 블록 내부의 'only_from', 'no_access', 'instances' 지시자를 통해 접근 통제 및 동시 접속 제한을 수행합니다."
            }
        ]
    },
    "Q-SHORT-036": {
        # DGA (Domain Generation Algorithm)
        "ans_replace": "DGA",
        "traps": [
            {
                "confused_term_or_misunderstanding": "DGA를 Fast Flux 기술과 혼동",
                "explanation": "Fast Flux는 단일 도메인에 수많은 IP 주소를 TTL을 극도로 짧게 하여 빠르게 순환시키는 기술이며, DGA는 C&C IP/도메인 블랙리스트 차단을 우회하기 위해 날짜나 시드값을 기반으로 매일 수백~수천 개의 도메인을 동적으로 무작위 생성하는 알고리즘입니다."
            }
        ]
    },
    "Q-SHORT-037": {
        # DAC, MAC, RBAC
        "traps": [
            {
                "confused_term_or_misunderstanding": "보안 등급 기반 강제적 접근통제(MAC)와 역할 기반 접근통제(RBAC) 혼동",
                "explanation": "MAC은 객체의 보안 레이블과 주체의 인가 등급을 시스템이 강제로 비교하여 통제하는 모델이며, RBAC은 조직 내 사용자의 직무 역할(Role)에 권한을 할당하고 사용자는 해당 역할을 부여받아 접근하는 모델입니다."
            }
        ]
    },
    "Q-SHORT-038": {
        # NAC (Network Access Control)
        "ans_replace": "NAC",
        "traps": [
            {
                "confused_term_or_misunderstanding": "NAC를 단순 IP/Port 기반 네트워크 방화벽으로 오해",
                "explanation": "NAC(Network Access Control)는 패킷을 단순히 허용/차단하는 방화벽과 달리, 네트워크에 접속하려는 엔드포인트 단말(PC, 모바일)의 백신 설치, OS 보안 패치, 무결성 상태를 검증하여 격리 또는 정책 준수 후에만 내부망 접속을 승인하는 솔루션입니다."
            }
        ]
    },
    "Q-SHORT-039": {
        # 레이스 컨디션 (Race Condition, TOCTOU)
        "ans_replace": "레이스 컨디션",
        "traps": [
            {
                "confused_term_or_misunderstanding": "경쟁 상태(Race Condition)를 단순 데드락(Deadlock, 교착상태)으로 혼동",
                "explanation": "데드락은 자원을 상호 점유한 채 무한 대기하는 교착 현상인 반면, 레이스 컨디션은 자원의 검사 시점(Time of Check)과 사용 시점(Time of Use) 사이의 시간차(TOCTOU)를 공격자가 악용하여 심볼릭 링크 변경 등으로 권한을 상승시키는 취약점입니다."
            }
        ]
    },
    "Q-SHORT-040": {
        # ARP 스푸핑 (ARP Spoofing)
        "ans_replace": "ARP 스푸핑",
        "traps": [
            {
                "confused_term_or_misunderstanding": "ARP 스푸핑 공격이 라우터를 넘어 외부 인터넷(WAN)까지 도달 가능하다고 오해",
                "explanation": "ARP는 2계층 데이터 링크 프로토콜이므로, ARP 스푸핑(ARP 캐시 변조) 공격은 반드시 동일한 브로드캐스트 도메인(동일 서브넷/LAN 세그먼트) 내부에서만 동작합니다."
            }
        ]
    },
    "Q-SHORT-041": {
        # Indexes (디렉터리 리스팅 방지)
        "ans_replace": "Indexes",
        "traps": [
            {
                "confused_term_or_misunderstanding": "디렉터리 리스팅 차단 지시자를 ServerTokens나 ServerSignature로 오해",
                "explanation": "ServerTokens는 HTTP 응답 헤더의 아파치 버전 정보 노출을 제어하는 지시자이며, 인덱스 파일(index.html 등)이 없을 때 디렉터리 내 파일 목록 출력을 차단하는 지시자는 'Options -Indexes'입니다."
            }
        ]
    },
    "Q-SHORT-042": {
        # Slowloris (Slow HTTP Header DoS)
        "ans_replace": "Slowloris",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Slowloris를 대용량 트래픽을 유발하는 HTTP GET 플러딩과 혼동",
                "explanation": "Slowloris는 대역폭을 소모하는 대용량 플러딩이 아니라, HTTP 요청 헤더의 끝(\\r\\n\\r\\n)을 전송하지 않고 불완전한 헤더를 극도로 느린 주기로 지속 전송하여 웹 서버의 가용 연결 세션을 고갈시키는 저전송 DoS 공격입니다."
            },
            {
                "confused_term_or_misunderstanding": "본문을 지연 전송하는 Slow HTTP POST(RUDY)와 혼동",
                "explanation": "Slow HTTP POST는 Content-Length를 크게 선언하고 Body 본문을 천천히 보내는 반면, Slowloris는 Header 영역의 미완료 유지를 통해 세션을 점유합니다."
            }
        ]
    },
    "Q-SHORT-043": {
        # 크리덴셜 스터핑 (Credential Stuffing)
        "ans_replace": "크리덴셜 스터핑",
        "traps": [
            {
                "confused_term_or_misunderstanding": "크리덴셜 스터핑을 무작위 문자열을 대입하는 단순 무차별 대입(Brute Force)으로 오해",
                "explanation": "크리덴셜 스터핑은 무작위 패스워드 생성이 아니라, 다른 사이트에서 이미 유출된 대량의 '유효한 아이디/비밀번호 쌍(Credential)' 데이터베이스를 그대로 타깃 웹사이트에 자동화 도구로 자동 대입하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-044": {
        # Pass the Hash (PtH)
        "ans_replace": "Pass the Hash",
        "traps": [
            {
                "confused_term_or_misunderstanding": "공격자가 NTLM 해시값을 평문 암호로 먼저 크랙(복호화)해야 인증할 수 있다고 오해",
                "explanation": "Pass-the-Hash 공격은 윈도우의 NTLM 인증 구조상 평문 암호를 알 필요 없이 메모리(LSASS)에서 추출한 NTLM 해시값 자체를 세션 협상 메시지에 그대로 주입하여 원격 인증을 통과하는 기법입니다."
            }
        ]
    },
    "Q-SHORT-045": {
        # DNS 캐시 포이즈닝 (DNS Cache Poisoning)
        "ans_replace": "DNS 캐시 포이즈닝",
        "traps": [
            {
                "confused_term_or_misunderstanding": "DNS 캐시 포이즈닝을 도메인 등록 기관 정보를 변경하는 DNS Hijacking과 혼동",
                "explanation": "DNS 하이재킹은 등록기관(Registrar) 계정을 탈취하여 네임서버 주소를 변경하는 것이며, 캐시 포이즈닝은 DNS 리커시브 리졸버의 트랜잭션 ID(TXID)와 UDP 포트를 예측하여 위조된 응답 레코드를 리졸버 캐시에 주입하는 공격입니다."
            }
        ]
    },
    "Q-SHORT-046": {
        # MITRE ATT&CK
        "ans_replace": "MITRE ATT&CK",
        "traps": [
            {
                "confused_term_or_misunderstanding": "MITRE ATT&CK을 단순 소프트웨어 취약점 목록인 CVE/NVD와 동일시",
                "explanation": "CVE는 개별 소프트웨어 결함(버그)을 식별하는 체계인 반면, MITRE ATT&CK은 실제 공격자들의 침해 행위 전술(Tactics), 기법(Techniques), 절차(Procedures)인 TTP를 행렬 매트릭스 형태로 체계화한 지식 베이스입니다."
            }
        ]
    },
    "Q-SHORT-047": {
        # CVSS (Common Vulnerability Scoring System)
        "ans_replace": "CVSS",
        "traps": [
            {
                "confused_term_or_misunderstanding": "CVSS 점수를 자산 가치까지 반영된 조직의 최종 위험 수준으로 오해",
                "explanation": "CVSS 기본 점수(Base Score)는 취약점 자체의 기술적 심각도(공격 난이도, 권한, 영향도 등)만을 측정한 점수(0.0~10.0)이며, 조직의 특정 비즈니스 환경과 자산 가치가 반영된 것은 환경 지표(Environmental Metric)가 결합되어야 합니다."
            }
        ]
    },
    "Q-SHORT-048": {
        # 초기 대응 (Initial Response)
        "ans_replace": "초기 대응",
        "traps": [
            {
                "confused_term_or_misunderstanding": "사고 인지 직후 단계를 침해사고 '복구(Recovery)' 또는 '보고' 단계로 혼동",
                "explanation": "KISA 침해사고 대응 절차는 '사고 탐지 -> 초기 대응(사고 인지 및 전파, 피해 최소화) -> 전략 수립 -> 조사 및 분석 -> 억제 및 제거 -> 복구 -> 사후 관리' 순으로 진행됩니다."
            }
        ]
    },
    "Q-SHORT-049": {
        # 위험식별 (Risk Identification)
        "ans_replace": "위험식별",
        "traps": [
            {
                "confused_term_or_misunderstanding": "위험식별(Risk Identification)을 위험분석(Risk Analysis)과 혼동",
                "explanation": "위험평가의 첫 단계는 보호 대상 자산과 위협, 취약성을 찾아내고 분류하는 '위험식별' 단계이며, 식별된 위험의 발생 가능성과 영향을 결합하여 위험의 수준을 수치화하는 것은 '위험분석' 단계입니다."
            }
        ]
    },
    "Q-SHORT-050": {
        # PPTP (Point-to-Point Tunneling Protocol)
        "ans_replace": "PPTP",
        "traps": [
            {
                "confused_term_or_misunderstanding": "PPTP를 3계층(네트워크 계층) VPN 프로토콜인 IPSec과 혼동",
                "explanation": "PPTP는 PPP 프레임을 IP 패킷으로 캡슐화(GRE)하여 사용하는 데이터 링크 계층(2계층) 기반의 터널링 프로토콜입니다."
            },
            {
                "confused_term_or_misunderstanding": "PPTP의 제어 포트와 프로토콜 번호 혼동",
                "explanation": "PPTP는 제어 세션에 TCP 1723 포트를 사용하고, 데이터 터널링 캡슐화에는 IP 프로토콜 47번(GRE)을 사용합니다."
            }
        ]
    },
    "Q-SHORT-051": {
        # SHA-512 ($6$)
        "ans_replace": "SHA-512",
        "traps": [
            {
                "confused_term_or_misunderstanding": "$6$ 해시 식별자를 MD5($1$)나 SHA-256($5$)과 혼동",
                "explanation": "리눅스 shadow 파일에서 $1$은 MD5, $2a$는 Blowfish, $5$는 SHA-256, $6$은 SHA-512(솔트와 함께 최소 5,000회 이상 해싱)를 나타내는 표준 매직 ID입니다."
            }
        ]
    },
    "Q-SHORT-052": {
        # CISO (정보보호최고책임자)
        "ans_replace": "CISO",
        "traps": [
            {
                "confused_term_or_misunderstanding": "CISO(정보보호최고책임자)를 CPO(개인정보보호책임자)와 혼동",
                "explanation": "CISO는 정보통신망법 등에 따라 시스템, 네트워크 및 정보보호 관리체계 전반의 보안 대책 수립을 총괄하며, CPO는 개인정보보호법에 따라 개인정보의 수집, 이용, 파기 등 프라이버시 보호 업무를 총괄합니다."
            }
        ]
    },
    "Q-SHORT-053": {
        # EDR (Endpoint Detection and Response)
        "ans_replace": "EDR",
        "traps": [
            {
                "confused_term_or_misunderstanding": "EDR을 시그니처 기반의 전통적 백신(Anti-Virus)과 동일시",
                "explanation": "전통 백신은 알려진 악성코드 해시/시그니처를 사전 차단하는 정적 검역 도구인 반면, EDR은 엔드포인트에서 발생하는 프로세스 생성, 네트워크 통신, 레지스트리 변조 등 모든 행위 로그를 실시간 수집하여 파일리스 악성코드나 이상 행위를 사후 탐지/대응하는 솔루션입니다."
            }
        ]
    },
    "Q-SHORT-054": {
        # strace (System Call Tracer)
        "ans_replace": "strace",
        "traps": [
            {
                "confused_term_or_misunderstanding": "strace를 공유 라이브러리 함수 호출을 추적하는 ltrace와 혼동",
                "explanation": "ltrace는 사용자 공간 라이브러리(libc 등)의 함수 호출을 추적하고, strace는 프로세스가 커널 영역에 요청하는 시스템 콜(open, read, write, connect 등)과 시그널을 가로채어 추적하는 도구입니다."
            }
        ]
    },
    "Q-SHORT-055": {
        # DTLS (Datagram Transport Layer Security)
        "ans_replace": "DTLS",
        "traps": [
            {
                "confused_term_or_misunderstanding": "UDP 환경에서 표준 TLS/SSL을 그대로 적용 가능하다고 오해",
                "explanation": "표준 TLS는 신뢰성 있는 TCP 스트림을 전제로 동작하므로 패킷 손실, 순서 변경이 발생하는 UDP 환경에서는 정상 동작하지 않으며, UDP의 비신뢰성 특성을 수용하기 위해 재전송 및 순서 번호 메커니즘을 추가한 규격이 DTLS(RFC 6347)입니다."
            }
        ]
    },
    "Q-SHORT-056": {
        # SSDP DRDoS (Simple Service Discovery Protocol)
        "ans_replace": "SSDP DRDoS",
        "traps": [
            {
                "confused_term_or_misunderstanding": "SSDP 프로토콜의 기본 포트를 NTP(123)나 SNMP(161)로 혼동",
                "explanation": "SSDP는 UPnP(Universal Plug and Play) 환경에서 네트워크 디바이스 자동 탐색을 위해 UDP 1900 포트(M-SEARCH 멀티캐스트)를 사용하며, 대용량 반사 응답을 유발하는 증폭 공격에 악용됩니다."
            }
        ]
    },
    "Q-SHORT-057": {
        # Suricata
        "ans_replace": "Suricata",
        "traps": [
            {
                "confused_term_or_misunderstanding": "Suricata가 Snort와 완전히 다른 독자 시그니처 문법만 지원한다고 오해",
                "explanation": "Suricata는 Snort 룰 문법과 호환성을 제공하면서도, 고속 네트워크 환경을 위해 멀티스레딩(Multi-threading) 아키텍처와 하드웨어 가속, HTTP/TLS 내장 파서를 지원하는 고성능 NIDS/IPS 엔진입니다."
            }
        ]
    },
    "Q-SHORT-058": {
        # POODLE (Padding Oracle On Downgraded Legacy Encryption)
        "ans_replace": "POODLE",
        "traps": [
            {
                "confused_term_or_misunderstanding": "POODLE 취약점의 근본 원인을 최신 TLS 1.2/1.3 프로토콜의 취약점으로 오해",
                "explanation": "POODLE은 공격자가 통신 오류를 고의로 유발하여 브라우저와 서버가 레거시 SSL 3.0 프로토콜로 다운그레이드 협상하도록 강제한 후, SSL 3.0의 CBC 모드 블록 암호 패딩 검증 결함을 악용하여 평문 데이터를 한 바이트씩 복원하는 취약점입니다."
            }
        ]
    },
    "Q-SHORT-059": {
        # SRM (Security Reference Monitor)
        "ans_replace": "SRM",
        "traps": [
            {
                "confused_term_or_misunderstanding": "SRM의 역할을 사용자 로그인 인증을 직접 수행하는 LSA(Local Security Authority)로 혼동",
                "explanation": "사용자 계정 인증과 액세스 토큰 생성을 주관하는 것은 LSA이며, 생성된 액세스 토큰과 객체의 보안 디스크립터(DACL)를 대조하여 실제 파일이나 레지스트리에 대한 읽기/쓰기 접근 허용 여부를 커널 모드에서 최종 판정하는 것은 SRM입니다."
            }
        ]
    },
    "Q-SHORT-060": {
        # /etc/cron.allow
        "ans_replace": "/etc/cron.allow",
        "traps": [
            {
                "confused_term_or_misunderstanding": "cron.allow와 cron.deny 파일 간의 적용 우선순위 혼동",
                "explanation": "리눅스 cron 접근 통제는 'cron.allow' 파일이 존재하면 오직 여기에 명시된 사용자만 cron을 사용할 수 있고 cron.deny는 무시되며, cron.allow가 없을 때만 cron.deny에 명시되지 않은 모든 사용자에게 기본 허용됩니다."
            }
        ]
    }
}

def apply_chunk2(explanations, questions_map):
    applied_count = 0
    ph_fixed_count = 0
    traps_fixed_count = 0

    for qid, fixes in CHUNK2_FIXES.items():
        if qid not in explanations:
            continue
        exp = explanations[qid]
        q = questions_map[qid]

        # 1. P1-1 Fix: Placeholder removal in why_correct
        if "ans_replace" in fixes:
            ans = fixes["ans_replace"]
            wc = exp.get("why_correct", "")
            if "표준 정답" in wc:
                old_ph_sent1 = "본 문항에서 요구하는 정확한 용어는 표준 정답입니다."
                old_ph_sent2 = "본 문항에서 요구하는 정확한 용어는 표준 정답입니다. 실기 시험 채점 특성상 표준 지침 및 관련 법령에 명시된 공식 명칭을 작성해야 만점이 인정됩니다."
                
                new_sent = f"본 문항에서 요구하는 정확한 정답은 '{ans}'입니다. 실기 시험 채점 특성상 관련 규정 및 표준 지침에 명시된 정식 명칭을 정확히 작성해야 정답으로 인정됩니다."
                
                if old_ph_sent2 in wc:
                    exp["why_correct"] = wc.replace(old_ph_sent2, new_sent)
                elif old_ph_sent1 in wc:
                    exp["why_correct"] = wc.replace(old_ph_sent1, new_sent)
                else:
                    exp["why_correct"] = wc.replace("표준 정답", f"'{ans}'")
                ph_fixed_count += 1

        # 2. P1-3 Fix: Question-specific traps
        if "traps" in fixes:
            exp["why_wrong_common_traps"] = fixes["traps"]
            traps_fixed_count += 1

        applied_count += 1

    print(f"Chunk 2 applied: {applied_count} questions updated.")
    print(f"  - P1-1 placeholders fixed: {ph_fixed_count}")
    print(f"  - P1-3 traps updated: {traps_fixed_count}")

if __name__ == "__main__":
    with open("app/data/explanations.json", "r", encoding="utf-8") as f:
        exps = json.load(f)
    with open("app/data/questions.json", "r", encoding="utf-8") as f:
        qs = {q["id"]: q for q in json.load(f)}

    apply_chunk2(exps, qs)

    with open("app/data/explanations.json", "w", encoding="utf-8") as f:
        json.dump(exps, f, indent=2, ensure_ascii=False)
    print("Chunk 2 changes saved successfully to explanations.json")
