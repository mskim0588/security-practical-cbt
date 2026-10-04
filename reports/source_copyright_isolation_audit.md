# Source Asset & Technical Isolation Audit Report

- **Goal**: Goal 5B Copyright / Source Asset Isolation Gate (Final Cleanup)
- **Audit Date**: 2026-10-04
- **Auditor**: Security CBT Engineering QA
- **Status**: PASSED (Technical & Asset Isolation Gate Approved)

---

## 1. Executive Summary & Legal Disclaimer

본 감사는 `security-practical-cbt` 프로젝트의 공개 배포(GitHub Public Repository 및 Railway Production 배포)에 앞서, 외부 원본 저작물(PDF, 교재 교안, 수험 요약집 등)의 기술적 격리 상태와 프로젝트 내 콘텐츠의 provenance(출처 및 변형 이력)를 전수 조사한 기술 감사 보고서이다.

> [!IMPORTANT]
> **법률적 효력에 관한 고지 (Legal Notice)**
> 본 감사는 원본 Source Asset의 Repository/Production 격리 여부와 콘텐츠 provenance를 기술적으로 검증한다.
> 개별 콘텐츠의 법적 이용 허가 또는 공정이용 해당 여부를 확정하는 법률 검토를 의미하지 않는다.
> (This audit verifies technical repository/production isolation and content provenance; it does NOT constitute legal clearance, legal approval, or a guarantee of fair use.)

감사 결과, **저장소 작업 트리 및 Git 이력 전체에 원본 바이너리 문서(PDF 등)가 단 한 건도 존재하지 않음**을 확인하였으며, 프로덕션 런타임 애플리케이션(`app/`)은 외부 소스 파일이나 파서 라이브러리에 전혀 의존하지 않는 완전한 독립형 아키텍처임이 검증되었다.

또한, 이전 오프라인 개발 스크립트 및 테스트에 남아있던 개인 로컬 절대경로(`G:\내 드라이브\...`)를 전수 조사하여 환경변수(`PRIVATE_SOURCE_DIR`) 및 generic placeholder로 일반화 완료함으로써, **Public Repository 추적 코드 내 개인 로컬 절대경로 = 0건**을 달성하였다.

---

## 2. Gate Verification Summary (게이트 검증 요약)

| Gate 항목 | 기준 | 감사 결과 | 판정 |
|---|---|---|:---:|
| **Gate 1: Raw Asset Git Tracking** | Git 추적 원본 소스 바이너리 = 0 | `git ls-files` 전수 조사 결과 PDF/문서 바이너리 0건 | **PASS** |
| **Gate 2: Repository File Presence** | 작업 트리 내 원본 소스 문서 = 0 | `.pdf`, `.hwp`, `.docx`, `.ocr` 등 금지 확장자 0건 | **PASS** |
| **Gate 3: Git History Cleanliness** | Git 커밋 이력 내 원본 문서 유입 = 0 | 3개 전체 커밋(`2cc1063`, `64c9019`, `6988c3e`) 이력 내 0건 | **PASS** |
| **Gate 4: Static Asset Exposure** | 정적 서빙 경로 문서 노출 = 0 | `app/static/` 내 프론트엔드 코드(`style.css`, `exam.js`)만 존재 | **PASS** |
| **Gate 5: Runtime Dependency** | 프로덕션 런타임 소스 파서 의존 = 0 | `app/` 내 `pypdf`, `pytesseract` 등 임포트 0건 | **PASS** |
| **Gate 6: Local Path Leakage in Code** | 추적 코드 내 개인 절대경로 노출 = 0 | `app/`, `tests/`, `scripts/` 전수 일반화 (`PRIVATE_SOURCE_DIR`) | **PASS** |
| **Gate 7: Metadata Integrity** | `sources.json` 원문 덤프 배제 = 0 | 12개 항목 모두 순수 서지 인용 메타데이터만 보유 | **PASS** |
| **Gate 8: Isolation Protection Rules** | `.gitignore` 격리 규칙 탑재 | `*.pdf`, `private_sources/`, `source_materials/` 등 명시 | **PASS** |
| **Gate 9: Automated CI Test** | 자동화 격리 테스트 통과 | `tests/test_source_asset_isolation.py` 8/8 PASS | **PASS** |

---

## 3. Detailed Technical Audit Findings

### A. Repository Source Material Scan
- **검사 대상**: 프로젝트 전체 디렉토리 (가상환경 및 Git 내부 메타데이터 제외)
- **검사 확장자**: `.pdf`, `.hwp`, `.hwpx`, `.doc`, `.docx`, `.ppt`, `.pptx`, `.epub`, `.ocr`, `.dump`
- **결과**: **0건 발견 (Clean)**
- **소견**: 개발 과정에서 참조된 원본 PDF 자료들은 개발자 외부 오프라인 저장소에만 보관되었으며, 프로젝트 저장소 내부로는 일절 유입되지 않았음.

### B. Git Tracking & Git History Audit
- **Git Tracked Files (`git ls-files`)**: 총 158개 파일 추적 중.
  - 원본 소스 문서 바이너리: **0건 (0.0%)**
- **Git History (전체 커밋 이력)**:
  1. `2cc1063` (Goal 2 Question Bank Baseline)
  2. `64c9019` (Goal 3 Learning Analytics Baseline)
  3. `6988c3e` (Goal 4 Learning UX Baseline)
  - 3개 커밋 전체에서 원본 바이너리가 추가된 이력이 전무함.
  - **History Rewrite (`git filter-repo`, `git filter-branch`) 필요성: 불필요 (Risk Level: ZERO)**.

### C. Static & Deployment Packaging Audit
- **`app/static/` 검사**:
  - `app/static/css/style.css` (CBT 스타일시트)
  - `app/static/js/exam.js` (문항 인터랙션 스크립트)
  - 외부로 서빙 가능한 비인가 텍스트나 PDF 파일 없음 (Clean).
- **배포 설정 파일 검사**:
  - `Procfile`, `runtime.txt`, `.env.example` 등 배포 아티팩트 내 소스 누설 0건.

### D. Private Local Path Leakage Removal (Public Hygiene)
- **초기 검색 결과**:
  - `tests/test_sources_registry.py` (1건)
  - `scripts/*.py` (27건)
  - `app/templates/index.html` (2건, "Google Drive" 문구 노출)
  - `reports/question_bank_audit.md` (1건)
- **조치 내용**:
  1. `tests/test_sources_registry.py`: `PRIVATE_SOURCE_DIR = os.environ.get("PRIVATE_SOURCE_DIR")`로 변경 및 미설정 시 안전한 skipTest 구현.
  2. `scripts/*.py` 27개 스크립트: `os.environ.get("PRIVATE_SOURCE_DIR", "")`로 일반화 완료.
  3. `app/templates/index.html`: "Google Drive" 문구를 "공식 서지 메타데이터 12종 전권"으로 UI 텍스트 정제 완료.
  4. `reports/question_bank_audit.md`: `[PRIVATE_SOURCE_DIR]` generic placeholder로 대체 완료.
- **최종 결과**:
  - **Public Repository 추적 코드 및 스크립트 내 개인 로컬 절대경로: 0건 (Clean)**.

### E. Production Runtime Source Dependency Audit
- **의존성 검사**: `app/` 패키지 내 모든 `.py` 파일 대상 `pypdf`, `pdfminer`, `fitz`, `pytesseract` 등 소스 문서 파서 임포트 여부 검사.
- **결과**: **0건 (의존성 없음)**
- **소견**: `DataLoader`는 파일시스템 상의 정적 JSON만을 디코딩하여 메모리에 적재하므로, 프로덕션 서버에 어떠한 PDF 엔진이나 외부 소스 파일이 없어도 완벽히 독립 구동됨.

---

## 4. Content Provenance & Classification

본 프로젝트는 콘텐츠의 출처와 가공 방식을 다음과 같이 기술적으로 분류하여 관리한다.

### A. Question Bank (`questions.json`, 180문항)
- **기출 기반 문항 (91문항)**:
  - 국가기술자격검정 실기 출제기준을 기반으로, CBT 자동 채점(Accepted answers, Rubrics) 규격으로 구조화된 `TRANSFORMED / ADAPTED` 저작물.
- **이론/교안 기반 문항 (89문항)**:
  - 보안 운영 도구 및 이론 표준을 평가하기 위해 독자 출제된 CBT 문항 (`TRANSFORMED / ADAPTED`).
- **단순 상용 복제본 (Verbatim copy)**: **0문항**.

### B. Explanations (`explanations.json`, 180개 해설)
- Goal 4C에서 직접 개발된 핵심 원리, 오답 함정 분석, 루브릭 채점 팁, AI 프롬프트 템플릿으로 구성된 `ORIGINAL (독자 창작물)`.

### C. Concept Contents (`concept_contents.json`, 20개 개념서)
- RFC, NIST SP 800, OWASP, KISA 가이드라인 등 공개 기술 표준을 기반으로 프로젝트 전용으로 종합 정리된 `ORIGINAL (독자 저작물)`.

### D. Sources Registry (`sources.json`, 12개 서지 메타데이터)
- 도서명, 출처 유형, 인용 페이지 번호 등 서지 인용 메타데이터 10개 필드만 포함 (`CITATIONAL METADATA ONLY`).

---

## 5. Automated CI/CD Test Validation

- **기존 테스트 통과 수**: 187 / 187 PASS
- **신규 격리 테스트 수**: 8 / 8 PASS (`tests/test_source_asset_isolation.py`)
- **총 테스트 수**: **195 / 195 PASS (100% OK)**
- **핵심 데이터 SHA-256 검증**:
  - `app/data/questions.json`: `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` (**MATCH**)
  - `app/data/concepts.json`: `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` (**MATCH**)
  - `app/data/sources.json`: `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` (**MATCH**)
- **결함 수**:
  - **P0**: 0
  - **P1**: 0
  - **P2**: 0

---

## 6. Final Decision & Gate Determination (최종 판정)

본 감사의 최종 판정은 기술적 격리와 법률적 영역을 엄격히 구분하여 다음과 같이 확정한다.

```
+-----------------------------------------------------------------------------------+
|                        GOAL 5B FINAL GATE DETERMINATION                           |
+-----------------------------------------------------------------------------------+
| 1. Technical Source Isolation      : PASS                                         |
|    - Raw source documents in repo  : 0건 (Clean)                                  |
|    - Git history source leakage    : 0건 (Clean)                                  |
|    - Static asset source exposure  : 0건 (Clean)                                  |
|    - Production runtime dependency : 0건 (Clean)                                  |
|                                                                                   |
| 2. Public Repository Asset Hygiene : PASS                                         |
|    - Hardcoded local paths in code : 0건 (Clean, PRIVATE_SOURCE_DIR 일반화 완료)  |
|    - Metadata purity               : 100% Bibliographic Citation Only             |
|    - Automated CI isolation tests  : 8/8 PASS                                     |
|                                                                                   |
| 3. Legal Copyright Clearance       : NOT DETERMINED BY THIS AUDIT                 |
|    - 본 감사는 기술적 격리 및 provenance 검증에 한하며, 법률적 clearance를           |
|      확정하지 않음.                                                               |
+-----------------------------------------------------------------------------------+
| TECHNICAL VERDICT: APPROVED FOR GITHUB PUBLIC REPO & RAILWAY PRODUCTION DEPLOYMENT|
+-----------------------------------------------------------------------------------+
```
