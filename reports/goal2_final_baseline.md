# 정보보안기사 실기 CBT — Goal 2: 문제은행 최종 확정 보고서 (Final Baseline Report)

- **마일스톤**: Goal 2F (Final Question Bank Baseline 확정)
- **보고서 확정 일자**: 2026-10-03
- **프로젝트 명**: 정보보안기사 실기 CBT 웹 애플리케이션
- **문제은행 저장소**: `app/data/questions.json`
- **Goal 2 상태**: **COMPLETE (최종 확정 및 고정 완료)**

---

## 1. Executive Summary (총괄 요약)

본 문서는 정보보안기사 실기 CBT 시스템의 **Goal 2: 문제은행 구축 및 품질 고도화** 단계의 최종 성과물과 확정된 데이터베이스 기준선(Final Baseline)을 공식 기록하는 보고서이다.

초기 18문항의 검증용 CBT 프로토타입(Goal 1)에서 시작하여, 12개 PDF 기출문제 및 이론서 전수 분석(Goal 2A), 64문항 기반 구축(Goal 2B), ExamGenerator 랜덤 출제 엔진 및 Seed 제어 구현(Goal 2C), 3단계 점진적 대규모 확장(Goal 2D Batch 1~3), 전수 품질 감사(Goal 2E), 그리고 발견된 결함에 대한 완벽한 수정(Goal 2E-Fix)을 거쳐 **최종 180문항의 고품질 실전 문제은행을 확정**하였다.

---

## 2. 문제은행 확정 지표 (Final Baseline Metrics)

### 2.1 문항 유형별 분포 (180문항 100% 확정)

| 문항 유형 | 문항 수 | 문항당 배점 | 회당 출제 수 | 영역 총점 | 배점 및 루브릭 무결성 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **단답형 (Short Answer)** | **112문항** | 3점 | 12문항 | 36점 | 100% 정규화 채점 지원 (다중빈칸 소문항 합계 3점) |
| **서술형 (Descriptive)** | **44문항** | 12점 | 4문항 | 48점 | 100% 단계별 부분점수 루브릭 완비 (소문항 합계 12점) |
| **실무형 (Practical)** | **24문항** | 16점 | 2문항 (택1) | 16점 | 100% 명령어/로그/룰 기술검증 완료 (소문항 합계 16점) |
| **총계** | **180문항** | - | **18문항 (17응시)** | **100점** | **무결성 100% 달성** |

### 2.2 5대 표준 카테고리별 문항 분포

| 표준 카테고리 | 단답형 | 서술형 | 실무형 | 카테고리 총계 | 비율 |
|:---|:---:|:---:|:---:|:---:|:---:|
| **시스템 보안** | 29문항 | 9문항 | 7문항 | **45문항** | 25.0% |
| **네트워크 보안** | 24문항 | 11문항 | 11문항 | **46문항** | 25.6% |
| **애플리케이션 보안** | 19문항 | 10문항 | 4문항 | **33문항** | 18.3% |
| **정보보안 일반 및 암호학** | 21문항 | 6문항 | 0문항 | **27문항** | 15.0% |
| **정보보호 관리 및 법규** | 19문항 | 8문항 | 2문항 | **29문항** | 16.1% |
| **총계** | **112문항** | **44문항** | **24문항** | **180문항** | **100.0%** |

### 2.3 Concept 및 Source Registry 현황
- **활성 Concept 수**: **20개 전수 매핑** (`app/data/concepts.json`)
  - 시스템 보안: 3개 (`CON-SYS-01` ~ `03`)
  - 네트워크 보안: 4개 (`CON-NET-01` ~ `04`)
  - 애플리케이션 보안: 4개 (`CON-APP-01` ~ `04`)
  - 정보보안 일반 및 암호학: 5개 (`CON-SEC-01` ~ `02`, `CON-CRY-01` ~ `03`)
  - 정보보호 관리 및 법규: 4개 (`CON-MGT-01` ~ `04`)
  - *미등록 Concept 참조 오류: 0건 (100% 유효)*
- **활성 PDF Source 수**: **12개 전수 Active** (`app/data/sources.json`)
  - 기출문제집 (3종): `SRC-01`(단답 1~28회), `SRC-02`(서술 1~28회), `SRC-03`(서술 TOP20)
  - 이론/교안/단권화 (9종): `SRC-04` ~ `SRC-12` (총 2,457페이지 전수 대조 완료)
  - *PDF 원본 근거 매핑율: 100% (180/180문항)*

---

## 3. 품질 감사 및 결함 조치 결과 (P0 / P1 / P2 Status)

| 결함 등급 | 초기 감사 결과 | Goal 2E-Fix 조치 결과 | 최종 잔여 건수 | 최종 상태 및 처리 |
|:---:|:---:|:---:|:---:|:---|
| **FAIL (P0)** | 1건 (Web UI) | 완료 | **0건** | `exam.html` 실무형 선택 라디오 동적 렌더링 수정 완료 |
| **WARNING (P1)** | 11건 (Data/Script) | 완료 | **0건** | 단답형 주정답 동기화, 카테고리 정상 일원화 완료 |
| **WARNING (P2)** | 13건 (Advisory) | 분리 관리 | **13건** | 기능 결함 없음. [`reports/goal2_p2_backlog.md`](goal2_p2_backlog.md)로 이관 |

---

## 4. 핵심 파일 무결성 해시 (Cryptographic Integrity Hashes)

문제은행의 불변성을 보증하기 위해 확정된 핵심 데이터 및 템플릿 파일의 SHA-256 해시값을 영구 보존합니다.

| 파일 경로 | 파일 설명 | 파일 크기 | SHA-256 Checksum |
|:---|:---|:---:|:---|
| [`app/data/questions.json`](../app/data/questions.json) | 180문항 문제은행 데이터베이스 | 432,363 bytes | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` |
| [`app/data/concepts.json`](../app/data/concepts.json) | 20개 표준 Concept 레지스트리 | 11,678 bytes | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` |
| [`app/data/sources.json`](../app/data/sources.json) | 12개 PDF Source 레지스트리 | 5,093 bytes | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` |
| [`app/templates/exam.html`](../app/templates/exam.html) | 시험 응시 및 실무형 선택 UI 템플릿 | 9,493 bytes | `255b75ba959f1030410ef08c4be20ff4194e89e4a95fafab4761379de45e50bf` |

---

## 5. 최종 자동 테스트 및 회귀 검증 결과

### 5.1 단위 테스트 스위트 (Unit Test Suite)
- **실행 명령**: `python -m unittest discover tests -v`
- **테스트 케이스 수**: **57개 전수 통과 (57 / 57 PASS)**
- **실행 시간**: **1.078초**
- **주요 검증 항목**:
  - `test_data.py`: 데이터 로더 및 소스 매핑 정상
  - `test_exam_generator.py`: 표준 시험 불변성, 500회 시뮬레이션 전체 풀 100% 커버리지, 카테고리 Round-Robin 정상
  - `test_grader.py`: 단답형/서술형/실무형 채점 엔진 및 100점 만점 구조 정상
  - `test_grading_modes.py`: normalized 및 strict 모드 동작, 5대 카테고리 및 Concept 참조 정합성 정상
  - `test_question_bank.py`: 180문항 메트릭스(112/44/24), 기존 18문항 보존, 소문항 배점 합계(12/16점) 정상
  - `test_question_status.py`: 작성 상태 감지 및 내비게이터 연동 정상
  - `test_routes.py`: 실무형 라디오 동적 렌더링, Standard/Random 모드, Seed 결정론적 재현성, 장애 Fallback 정상
  - `test_sources_registry.py`: 12개 교재 1:1 매핑 및 요약 정보 정상

### 5.2 ExamGenerator 1,000회 시뮬레이션 검증
- **총 실행 횟수**: 1,000회 무작위 시험 생성
- **발생 예외**: **0건 (100% 무중단 안정성)**
- **회당 시험 구성**: 정확히 단답 12, 서술 4, 실무 2 (총 18문항, 100점 만점)
- **시험 내 ID 중복**: **0건**
- **문항 생존율 (Dead Questions)**: **0건 (180개 전 문항 1회 이상 출제 확인)**

### 5.3 Web QA 검증
- Standard 모드 및 5개 이상의 Random Seed(seed=1, 10, 42, 100, 999)에 대해 시험 렌더링, 라디오 ID 일치, 검토 화면(`/review`), 최종 제출(`/submit`), 채점 성적표(`/result`), 출처 뱃지 표시 전 과정 100% 정상 동작 확인.

---

## 6. 개발 산출물 정리 감사 (Artifact Audit)

Goal 2D~2E 과정에서 생성된 스크립트 및 백업 파일들을 체계적으로 분류하였습니다. (원칙에 따라 파일 삭제는 수행하지 않음)

### 6.1 KEEP (향후 회귀 테스트 및 감사 운영에 영구 유지)
- [`scripts/verify_goal2e_fix.py`](../scripts/verify_goal2e_fix.py): Data QA, Web QA, 1,000회 시뮬레이션 통합 검증 스크립트
- [`scripts/deep_audit_180.py`](../scripts/deep_audit_180.py): 180문항 12개 PDF 대조 전수 감사 스크립트
- [`scripts/test_practical_ui.py`](../scripts/test_practical_ui.py): 실무형 라디오 UI 및 채점 회귀 테스트 스크립트
- [`scripts/test_web_rendering.py`](../scripts/test_web_rendering.py): Flask 템플릿 웹 렌더링 검증 스크립트
- [`scripts/audit_24_practical.py`](../scripts/audit_24_practical.py): 24개 실무형 문항 정밀 검사 스크립트
- [`reports/goal2_final_baseline.md`](goal2_final_baseline.md): Final Baseline 보고서
- [`reports/goal2_p2_backlog.md`](goal2_p2_backlog.md): P2 개선 권고 백로그 보고서
- [`reports/goal2e_final_audit.md`](goal2e_final_audit.md): Goal 2E 최종 품질 감사 보고서

### 6.2 ARCHIVE (개발 히스토리 보존용, 런타임 비의존)
- 중간 단계 빌더 및 머지 스크립트: `batch1_draft_builder.py`, `batch2_chunk1~4_builder.py`, `batch3_chunk1~4_builder.py`, `merge_batch2.py`, `merge_batch3.py`, `apply_batch1.py`, `apply_goal2e_fixes.py` 등
- 중간 단계 백업 파일: `questions.json.goal2e_fix_pre_bak`, `questions.json.goal2e_pre_bak`, `questions.json.batch3_pre_bak`, `questions.json.batch2_pre_bak`, `questions.json.batch1_bak`, `questions.json.bak` 등

### 6.3 REMOVE_CANDIDATE (향후 정리 가능한 일회성 디버그 스크립트)
- `find_pam_page.py`, `search_pam.py`, `search_practical.py`, `search_src08_db.py`, `search_src10_src11.py`, `search_src5_src9.py`
- `dump_batch1_src1.py`, `dump_batch1_src5.py`, `dump_candidates.py`, `dump_src2_part2.py`, `dump_src2_part3.py`, `dump_toc.py`
- `inspect_exact_pages.py`, `inspect_src05.py`, `inspect_candidates.py`, `inspect_all_pdfs.py`, `inspect_audit.py`, `list_src2_src3.py`
- `compare_desc1_prac3.py`, `test_duplicate_on_modified.py`, `generate_test_modified.py`, `format_details.py`, `check_strict.py`, `check_short_overlaps.py`

---

## 7. Git Baseline 준비 및 권고

- **현재 Working Tree 상태**: 작업 디렉터리에 `.git` 저장소가 아직 초기화되지 않은 상태임 (`fatal: not a git repository`).
- **권장 조치 방안**:
  1. Git 저장소 초기화: `git init`
  2. `.gitignore` 생성: 중간 백업본(`*.bak`) 및 임시 스크립트 제외 설정
  3. Final Baseline 커밋 및 태그 생성:
     - 커밋 메시지: `feat: finalize Goal 2 Question Bank Baseline (180 questions, 100 points, 20 concepts, 12 sources)`
     - 권장 태그명: `goal2-final-baseline` 또는 `v0.2-question-bank-final`

---

## 8. Goal 2 종료 승인 결론

1. 180문항 전수 PDF 근거 검증 완료
2. P0 결함 0건 / P1 불일치 0건 완료
3. 전체 자동 단위 테스트 57/57 PASS 달성
4. Standard / Random 모의고사 및 100점 만점 구조 100% 안정성 확인
5. **Goal 2의 모든 마일스톤(2A, 2B, 2C, 2D, 2E, 2F)이 성공적으로 종료되었음을 선언함.**
