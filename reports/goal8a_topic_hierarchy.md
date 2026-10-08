# Goal 8A Topic Hierarchy Checkpoint

## A. Baseline — DONE

- Branch: `master`.
- Baseline HEAD: `a656ea409677cb63d05dc74e9a5d37d0156ce847`.
- Baseline `origin/master`: `a656ea409677cb63d05dc74e9a5d37d0156ce847`.
- Baseline tree: clean.
- Release tag `v0.7-learning-final`: present at `a656ea409677cb63d05dc74e9a5d37d0156ce847`.
- Goal 7: `GOAL_7_COMPLETE`.
- Goal 8A baseline state: `GOAL_8A_READY`.
- Pre-Goal-8A regression: 289 ran, 288 passed, 1 skipped, 0 failures, 0 errors.

## B. Existing 20 Concepts — DONE

- All 20 Concept records and IDs remain unchanged.
- Existing Question-to-Concept mappings remain in protected `questions.json` and are unchanged.
- Parent Concepts remain the only analytics, VI, weakness-aggregation, and adaptive-learning unit.
- Topic is an additive learning/navigation layer only.

## C. Topic Design Rules — DONE

- Topics were derived from all 180 question prompts, types, tags, rubrics/model answers, explanations, and the 20 Concept study packs.
- Every Topic has one primary Parent Concept and uses that Concept's category.
- Every question has one primary Topic; no secondary mappings were needed.
- Closely related exam material is grouped into reusable study units; one-Topic-per-question was avoided except where the bank contains an isolated subject under its stable Parent Concept.
- Goal 8B aliases, acronyms, synonyms, and alternative names were not added.

## D. Topic Inventory — DONE

- `CON-SYS-01` (8): 리눅스 계정 및 인증 관리; 유닉스 로그 및 실행 추적; 리눅스 서비스 접근통제; 시스템 취약점 분석 및 침투 도구; 접근통제 모델과 특수 권한; 모바일 업무환경 보안; Windows 플랫폼 및 저장매체 보호; 운영체제 실행 구조와 자원 교착.
- `CON-SYS-02` (3): Windows 인증과 SID; Windows 이벤트 및 서비스 로그; 호스트 침해 무결성 조사.
- `CON-SYS-03` (3): 리눅스 프로세스와 파일 권한; 메모리 공격과 실행 보호; 리눅스 감사 로그 관리.
- `CON-NET-01` (9): 라우팅과 VLAN 운영; ARP 스푸핑과 LAN 스니핑; DNS 운영과 영역 설정; 패킷 생성·스캔·캡처 분석; 네트워크 접근과 악성 통신 통제; IDS 룰과 탐지 방식; 방화벽과 상태 기반 필터링; 보안 터널과 전송 프로토콜; 반사·증폭 서비스 거부 공격.
- `CON-NET-02` (4): WPA2와 802.1X 무선 인증; Snort 탐지 세부 설정; NAC 배치 방식; IP 단편화와 고전적 DoS.
- `CON-NET-03` (2): 네트워크 서비스 보안 설정; TLS 핸드셰이크.
- `CON-NET-04` (3): VLAN 할당 방식; 라우터 ACL과 증폭 공격 차단; 보안관제 배치와 자동화.
- `CON-APP-01` (8): 웹서버 설정과 로그 분석; SQL 인젝션; 파일 처리 취약점; 브라우저와 세션 기반 공격; HTTP 메시지 및 서버 요청 변조; 애플리케이션 계층 DoS; XML 파서와 질의 인젝션; 애플리케이션 신뢰와 보안 점검.
- `CON-APP-02` (2): 로봇 배제 표준; 메일 서버 및 전송 보안.
- `CON-APP-03` (1): 데이터베이스 암호화와 접근 제한.
- `CON-APP-04` (2): 소프트웨어 컴포넌트 공격과 회피; 소프트웨어 보안 테스트.
- `CON-CRY-01` (5): IPsec 보안 프로토콜; TLS 취약점과 안전성; 대칭키와 공개키 암호 비교; 블록·스트림 암호 알고리즘; 공개키 기반 키 교환.
- `CON-CRY-02` (2): 해시 함수 안전성; 전자서명과 인증서 검증.
- `CON-CRY-03` (1): 인증 프로토콜과 암호 분석 모델.
- `CON-MGT-01` (5): 위험 식별·분석·평가 절차; 위험 분석과 처리 전략; 정량적 위험 분석; 취약점 등급과 보안 평가보증; 침해사고 대응과 정보공유.
- `CON-MGT-02` (3): 가명처리와 가명정보; 개인정보 기술적 보호조치; 개인정보 처리자 법적 의무.
- `CON-MGT-03` (2): ISMS-P와 안전성 확보조치; CISO 정보보호 거버넌스.
- `CON-MGT-04` (1): 업무연속성과 재해복구.
- `CON-SEC-01` (2): 데이터 유출과 엔드포인트 대응; APT와 공격자 전술 분석.
- `CON-SEC-02` (1): 침해 증거와 위기 대응.

## E. Concept → Topic Distribution — DONE

| Parent Concept | Topics | Questions |
|---|---:|---:|
| CON-SYS-01 | 8 | 31 |
| CON-SYS-02 | 3 | 6 |
| CON-SYS-03 | 3 | 8 |
| CON-NET-01 | 9 | 27 |
| CON-NET-02 | 4 | 8 |
| CON-NET-03 | 2 | 4 |
| CON-NET-04 | 3 | 7 |
| CON-APP-01 | 8 | 25 |
| CON-APP-02 | 2 | 3 |
| CON-APP-03 | 1 | 2 |
| CON-APP-04 | 2 | 3 |
| CON-CRY-01 | 5 | 13 |
| CON-CRY-02 | 2 | 6 |
| CON-CRY-03 | 1 | 2 |
| CON-MGT-01 | 5 | 15 |
| CON-MGT-02 | 3 | 7 |
| CON-MGT-03 | 2 | 5 |
| CON-MGT-04 | 1 | 2 |
| CON-SEC-01 | 2 | 4 |
| CON-SEC-02 | 1 | 2 |
| **Total** | **67** | **180** |

## F. Question → Topic Coverage — DONE

- Total questions: 180.
- Mapped questions: 180.
- Duplicate mappings: 0.
- Primary Topics per question: exactly 1.

## G. Unmapped Questions — DONE

- Unmapped: 0.
- Unresolved question IDs: none.

## H. Validation Findings — DONE

- Duplicate Topic IDs: 0.
- Duplicate Topic names: 0.
- Invalid Parent Concept IDs: 0.
- Invalid Question IDs: 0.
- Invalid Topic references: 0.
- Parent mismatches: 0.
- Zero-question Topics: 0.
- Single-question Topics: 10 (`TOP-SYS-01-06`, `TOP-SYS-02-03`, `TOP-NET-02-01`, `TOP-NET-02-03`, `TOP-NET-03-02`, `TOP-NET-04-01`, `TOP-APP-02-01`, `TOP-APP-04-02`, `TOP-CRY-01-01`, `TOP-CRY-01-03`). These correspond to isolated bank subjects under immutable Parent Concepts and were retained rather than merged across parents.
- Largest Topic size: 6 questions (3.3% of the bank); no Topic contains an excessive share.

## I. UI Integration — DONE

- `/concepts` remains the existing Concept library and now shows Topic counts.
- Parent Concept detail retains all existing content and adds a responsive Topic-card section.
- `/topics/<topic_id>` shows Topic name, Parent Concept, category, summary, and related questions.
- Related-question links return to stable question anchors on the Parent Concept page.
- Invalid Topic IDs use the existing HTML 404 handler; raw JSON/dict data is not rendered.
- Active exam, mock-exam setup, and pre-submit descriptive-training surfaces contain no Topic links or summaries.

## J. Goal 7 Regression — DONE

- Goal 7A targeted suite: PASS.
- Goal 7B targeted suite: PASS.
- Goal 7C targeted suite: PASS.
- Goal 7D targeted suite: PASS; freshness registry remains separate from Topic metadata.
- Combined Goal 4C + Goal 7A–7D + Goal 8A targeted run: 77 passed, 0 failures, 0 errors.
- Full regression: PASS — 298 ran, 297 passed, 1 skipped, 0 failures, 0 errors.
- Existing Concept-based analytics, VI, adaptive selection, practice, descriptive training, mock exam, and law-freshness regressions all passed.

## K. Mobile QA — DONE

- Browser-rendered viewport matrix passed at 360×740, 390×844, 430×932, and 1280×800.
- Topic cards fit the viewport; long names wrap or fit; hierarchy breadcrumbs and related-question rows remain readable.
- No page-level horizontal overflow remains on the Parent Concept or Topic detail views.
- Mobile bottom-navigation clearance passed; desktop bottom navigation remains hidden.
- Browser console errors: 0.
- A narrow-screen overflow found in existing Concept question rows was corrected with scoped responsive CSS and the complete matrix was rerun successfully.

## L. Tests — DONE

- Goal 8A focused tests: 9 ran, 9 passed, 0 skipped, 0 failures, 0 errors.
- Expanded targeted suite: 77 ran, 77 passed, 0 skipped, 0 failures, 0 errors.
- Full `python -m unittest discover tests -v`: 298 ran, 297 passed, 1 skipped, 0 failures, 0 errors.
- The single skip is the existing optional private-source file comparison when `PRIVATE_SOURCE_DIR` is not configured.

## M. Core Hashes — DONE

- Protected data result: 5 / 5 SHA-256 MATCH.
- `questions.json`: `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`.
- `concepts.json`: `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`.
- `sources.json`: `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`.
- `concept_contents.json`: `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171`.
- `explanations.json`: `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696`.

## N. Limitations — PARTIAL

- Topic metadata is intentionally static and has no learner-specific Topic analytics.
- No DB schema change is required or introduced.
- Physical Android verification remains pending by policy.
- Deployment and production smoke remain pending at this checkpoint.

## O. Goal 8B Readiness — TODO

- Goal 8B is not started.
- No alternative names, English aliases, acronyms, synonyms, or global search were implemented.
- Readiness will be reported only after Goal 8A deployment and production smoke complete.

## Checkpoint State

- Current status: `PARTIAL`.
- Last Safe Step: additive taxonomy, UI integration, 5/5 hash validation, 77-test targeted regression, 298-test full regression, and four-viewport browser QA all pass.
- Next Step: complete Git review, commit, push, Railway terminal deployment, and production smoke.
