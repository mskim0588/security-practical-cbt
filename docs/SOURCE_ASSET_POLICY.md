# Source Asset & Technical Isolation Policy

- **Project**: Security Practical CBT (`security-practical-cbt`)
- **Version**: 1.1 (Goal 5B Final Cleanup)
- **Effective Date**: 2026-10-04
- **Scope**: All repository code, data assets, deployment configurations, and public repositories

---

## 1. Overview & Purpose (개요 및 목적)

본 문서는 `security-practical-cbt` 프로젝트의 외부 출처 자산 격리(Source Asset Isolation), 저장소 위생(Repository Hygiene), 및 기술적 배포 안전 기준을 정의한다.

> [!IMPORTANT]
> **법률적 효력에 관한 고지 (Legal Notice)**
> 본 감사는 원본 Source Asset의 Repository/Production 격리 여부와 콘텐츠 provenance를 기술적으로 검증한다.
> 개별 콘텐츠의 법적 이용 허가 또는 공정이용 해당 여부를 확정하는 법률 검토를 의미하지 않는다.
> (This audit verifies technical repository/production isolation and content provenance; it does NOT constitute legal clearance, legal approval, or a guarantee of fair use.)

본 애플리케이션은 국가기술자격검정(정보보안기사 실기) 수험생을 위한 교육용 실전 CBT(Computer-Based Test) 시스템이다. 본 문서는 수험 기술 표준과 공개 기출 동향을 학습용 소프트웨어로 구현함에 있어, **상용 출판물 및 원본 수험 자료가 저장소 및 배포 아티팩트에 유입되는 것을 기술적으로 원천 차단**하는 것을 목적으로 한다.

---

## 2. Asset Classification (자산 분류 체계)

프로젝트 자산은 **Public Assets (공개 가능 자산)** 과 **Private Assets (비공개 격리 자산)** 으로 엄격히 분리된다.

```
+-----------------------------------------------------------------------------------+
|                            Security Practical CBT System                          |
+-----------------------------------------------------------------------------------+
                                         |
         +-------------------------------+-------------------------------+
         |                                                               |
         v                                                               v
+----------------------------------+            +----------------------------------+
|      PUBLIC ASSETS (Repo/Web)    |            |     PRIVATE ASSETS (External)    |
+----------------------------------+            +----------------------------------+
| - CBT Web Engine (Flask/SQLAlchemy)           | - External Raw Reference PDFs    |
| - Standard CSS / JavaScript UI   |            | - Commercial Textbooks & Scans   |
| - Normalized Question Bank (JSON)|            | - Proprietary Study Notes        |
| - Original Rubric & Grader Logic |            | - OCR Text / Raw Source Dumps    |
| - Original Explanations (180개)  |            | - Local Workspaces / Drives      |
| - Original Concept Guides (20개) |            |                                  |
| - Bibliographic Citations (Meta) |            |                                  |
+----------------------------------+            +----------------------------------+
                 |                                               |
                 | (Deployed / Tracked)                          | (NEVER Committed)
                 v                                               v
        [Production Platform]                           [Local Offline Only]
```

### A. Public Assets (공개 자산)
1. **애플리케이션 소스 코드**: Flask 3.1 라우트, 서비스 계층, 채점 알고리즘(Grader), 취약점 분석기(Analytics), 뷰 템플릿.
2. **CBT 문항 데이터베이스 (`questions.json`)**: 국가기술자격 출제기준에 맞춰 CBT 인터랙션(단답형 정규화, 서술형 루브릭, 실무형 택1)으로 재구성 및 구조화된 180문항 (`TRANSFORMED` / `ADAPTED`).
3. **학습 콘텐츠 (`explanations.json`, `concept_contents.json`)**: 핵심 원리, 오답 함정 분석, 채점 포인트, 비교 표, AI 프롬프트 템플릿 등으로 작성된 교육용 해설 및 개념 가이드 (`ORIGINAL`).
4. **서지 인용 메타데이터 (`sources.json`)**: 문항의 학술적·시험적 출처 검증을 위한 도서명, 출처 유형, 인용 페이지 번호 메타데이터 (`CITATIONAL METADATA`).

### B. Private Assets (비공개 격리 자산)
1. **외부 원본 PDF 문서**: 기출 모음집 PDF, 상용 기본서 교안, 수험용 요약 PDF 등 원문 파일.
2. **원문 추출 및 OCR 텍스트**: PDF 또는 종이 문서에서 추출된 raw text, OCR 스캔본, 대량 발췌문.
3. **개인 드라이브 및 로컬 작업 경로**: 개발자의 로컬 디스크 및 개인 클라우드 드라이브 등 (오프라인 참조 전용).

---

## 3. Strict Technical Isolation Policy (기술적 격리 원칙)

1. **Zero Raw Asset Tracking (저장소 유입 절대 금지)**:
   - 어떠한 PDF, HWP, DOCX, PPTX, EPUB, 이미지 스캔 파일도 Git 저장소에 추가하거나 커밋하지 않는다.
   - `.gitignore`에 파일 확장자(`*.pdf`, `*.hwp`, `*.docx` 등)와 격리 디렉토리(`private_sources/`, `source_materials/`, `local_references/` 등)를 명시하여 실수로 인한 추적을 원천 차단한다.

2. **Zero Static Exposure (정적 디렉토리 노출 금지)**:
   - `app/static/`, `public/`, `assets/` 등 웹 서버가 직접 정적 서빙하는 경로에는 프론트엔드 UI 자산(`style.css`, `exam.js`) 외에 어떠한 문서나 원문 데이터도 위치할 수 없다.

3. **Zero Production Runtime Dependency (런타임 의존성 배제)**:
   - 프로덕션 런타임 애플리케이션(`app/`)은 구동 시 PDF 파서(`pypdf`, `pdfminer` 등)나 OCR 도구(`pytesseract` 등), 외부 파일 저장소에 의존하지 않는다.
   - 모든 런타임 데이터는 검증 완료된 내부 정형 JSON 데이터셋(`app/data/`)만을 참조한다.

4. **Zero Raw Text Excerpt in Metadata (메타데이터 순수성)**:
   - `sources.json` 및 `questions.json`의 출처 필드는 **학술적 인용 목적의 서지 정보(Bibliographic Citation)** 만을 포함한다.
   - 원문의 긴 단락, 책의 목차 전체, 본문 스캔 내용 등 원문 텍스트는 메타데이터에 일절 포함하지 않는다.

5. **Zero Hardcoded Local Paths (개인 로컬 절대경로 배제)**:
   - 저장소 내 모든 코드, 테스트, 스크립트, 리포트에서 개인 로컬 절대경로(`G:\`, `C:\Users\`, `내 드라이브` 등)를 하드코딩하지 않는다.
   - 필요한 경우 환경변수(`PRIVATE_SOURCE_DIR`) 또는 generic placeholder를 사용하며, 해당 환경변수가 없을 경우 테스트는 안전하게 skip 처리된다.

---

## 4. Content Provenance & Classification (콘텐츠 출처 및 변형 분류)

본 프로젝트는 콘텐츠의 출처와 가공 방식을 다음과 같이 기술적으로 분류하여 관리한다.

1. **TRANSFORMED / ADAPTED (기출 변형 문항)**:
   - 국가기술자격검정 시험 출제기준에 기초하여, 자동화 채점 모델(Accepted answers) 및 루브릭(Rubrics) 구조로 재구성된 문항.
2. **ORIGINAL (창작 교육 콘텐츠)**:
   - 공개 기술 표준(RFC, NIST, OWASP, KISA 가이드라인)을 기반으로 본 프로젝트를 위해 독자 작성된 해설 및 개념 가이드.
3. **CITATIONAL METADATA (서지 메타데이터)**:
   - 출처 명시 의무를 위한 도서명 및 페이지 정보.

> [!NOTE]
> 위의 분류는 콘텐츠의 provenance(작성 및 출처 이력)를 설명하는 기술적 분류이며, 공정이용의 법적 성립 여부나 무제한 배포(unrestricted redistribution) 권리를 보증하는 법적 판정이 아님을 유의한다.

---

## 5. Automated CI/CD Isolation Gate (자동화 검증 게이트)

본 격리 정책을 보장하기 위해 자동화 테스트(`tests/test_source_asset_isolation.py`)가 구축되어 있으며, 배포 전 필수 통과해야 한다.

- **Gate 1**: Git 추적 파일 중 비허가 문서/바이너리(`*.pdf`, `*.docx` 등) 0건 검증.
- **Gate 2**: 작업 디렉토리 내 비허가 소스 바이너리 노출 0건 검증.
- **Gate 3**: `app/static/` 내 비인가 문서 노출 0건 검증.
- **Gate 4**: `app/` 런타임 코드 내 PDF/OCR 패키지 임포트 0건 검증.
- **Gate 5**: `sources.json` 내 로컬 절대 경로 및 원문 덤프 부재 검증.
- **Gate 6**: `.gitignore` 격리 규칙 완전성 검증.
- **Gate 7**: 런타임/테스트/스크립트 내 개인 절대경로 하드코딩 0건 검증.

---

## 6. Incident Response & Contact (권리 침해 대응 절차)

본 프로젝트의 콘텐츠와 관련하여 정당한 권리자의 문의 또는 권리 침해 주장이 접수될 경우, 프로젝트 관리자는 다음 절차에 따라 즉각 대응한다.

1. **접수 및 검토**: 해당 문항 ID 또는 콘텐츠 식별 및 기술적 출처 즉시 검토.
2. **임시 조치**: 사실 확인 기간 동안 해당 문항의 출제 및 노출 즉시 비활성화.
3. **수정 또는 대체**: 필요 시 대체 문항으로 교체 또는 수정 반영.
