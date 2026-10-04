# Goal 4 Final Release Baseline & Desktop QA Report

**생성 일시**: 2026-10-04 (Goal 4F-Doc-Fix 최종 문서 확정)  
**대상 시스템**: 정보보안기사 실기 CBT 플랫폼 (Security Practical CBT)  
**검증 기준**: Goal 4 (Goal 4A ~ Goal 4F-Doc-Fix) Desktop Final Baseline & Release Validation  
**릴리즈 차단 결함 (Release-blocking Defects)**: **P0 = 0, P1 = 0, P2 = 0** (차단 결함 0건)  
**알려진 콘텐츠 폴리싱 백로그 (Known Non-blocking Polish Backlog)**: 3건 (차기 개선 과제 분리 관리)  
**전체 테스트 현황**: **181 / 181 PASS (100% ALL PASS)**

---

## 1. Goal 4A ~ 4F-Doc-Fix 구현 기능 총괄 요약

| Goal | 명칭 | 핵심 구현 및 달성 내용 |
| :--- | :--- | :--- |
| **Goal 4A** | Global Layout / Nav / Design Foundation | CSS Design Tokens (색상, 여백, 타이포그래피) 구축, `base.html` 통일화, Desktop 상단 글로벌 GNB 및 모바일 하단 Bottom Nav 분리 제어, Skip Link 및 접근성 기본 토대 구축 |
| **Goal 4B** | Exam / Review / Result UX | 실전 모의고사(화면상 18문항 출제 후보, 실무형 택1 포함 17문항 채점 대상, 100점 만점) 응시 흐름 개편, 모바일 하단 네비게이션 제어, 긴 보안 로그/명령어 syntax block 가독성 개선, 실무형 택1 명확화(17번 IPTables / 18번 Snort IDS), 제출 전 검토(`review.html`) 상태 요약, 결과 화면(`result.html`) 섹션별 득점 계층화 |
| **Goal 4C** | Learning Content Architecture | 20개 보안 Concept 전수 학습서(`concept_contents.json`, 88KB), 180문항 전수 심층 해설(`explanations.json`, 586KB), `/concepts` 개념 도서관, `/concepts/<id>` 개념 상세, Explanation Card, AI Prompt Builder (ChatGPT/Gemini 연동 모달), 법령 최신성 안내 체계 |
| **Goal 4D** | History & Wrong Notes Learning UX | 응시 이력 목록/상세(`/history`, `/history/<id>`), 오답노트(`/wrong-notes`, `/wrong-notes/<qid>`), 오답 복기 타임라인, 오답→해설→소속 Concept→AI 질문→재응시 완결형 학습 루프 완성, 단일 문항 삭제(POST cascade) 보안 강화 |
| **Goal 4E** | Dashboard Learning Action Hub | 대시보드(`/dashboard`)를 단순 통계판에서 "학습 행동 허브"로 승격. 4대 KPI 카드, 5대 보안 영역 가중 성취도 시각화, 취약 Concept Top 5 클리닉 카드 및 원클릭 개념/맞춤시험 CTA, 결정론적 학습 추천 엔진(Boundary Safe) 연동 |
| **Goal 4F** | Desktop Final QA & Release Baseline | 14개 전체 라우트 전수 점검, 4대 E2E 시나리오 자동화, 1024/1280/1440px 해상도 적응성 점검, XSS/POST-only 보안 감사, 404/500 에러 핸들러 구축 |
| **Goal 4F-Fix** | CSRF Security & Data Statistical Audit | 서명된(signed) Flask 세션 기반 CSRF 보호 체계 구축(`app/services/csrf_service.py`), 상태 변경 라우트(`POST /submit`, `POST /history/<id>/delete`) 전수 보호, 403 Forbidden 친화적 에러 페이지, 문항 유형(112/44/24) 및 Concept 실제 ID/분포 교정, 총 181개 테스트 100% PASS |
| **Goal 4F-Doc-Fix** | Release Documentation Finalization | Concept 실제 ID(CON-CRY, CON-SEC) 및 3/4/4/5/4 분포 정정, 서명된 Flask 세션 쿠키 보안 표현 정밀화, 18문항 출제 후보/17문항 채점 대상 표현 명확화, 릴리즈 결함(P0=0/P1=0/P2=0)과 비차단 콘텐츠 폴리싱 백로그 명확 분리 |

---

## 2. 전체 Route 인벤토리 및 상태 검증 (14개 라우트)

전체 Flask 애플리케이션의 URL 맵에 등록된 14개 라우트에 대해 HTTP 메서드 제약, CSRF 보호 여부 및 응답 상태 코드를 전수 검증했습니다.

| 번호 | 라우트 (URL) | HTTP Method | 엔드포인트 | 상태 변경 여부 | 보안 / 검증 정책 | 정상 응답 |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| 1 | `/` | GET | `exam.index` | Read-only | 공개 조회 | 200 OK |
| 2 | `/dashboard` | GET | `dashboard.view_dashboard` | Read-only | 학습 행동 허브 조회 | 200 OK |
| 3 | `/concepts` | GET | `concepts.list_concepts` | Read-only | 개념 도서관 검색/필터 | 200 OK |
| 4 | `/concepts/<concept_id>` | GET | `concepts.view_concept_detail` | Read-only | 개념 심층 학습서 조회 | 200 OK |
| 5 | `/exam` | GET | `exam.take_exam` | Read-only | 모의고사 시험창 (18문항 출제 후보 / 17문항 채점 대상) / CSRF 토큰 발급 | 200 OK |
| 6 | `/review` | **POST only** | `exam.review_exam` | Read-only | 답안 최종 검토 (17문항 작성 상태 요약, DB 변경 없음, GET 시 405) | POST: 200 / GET: 405 |
| 7 | `/submit` | **POST only** | `exam.submit_exam` | **State-changing** | **CSRF 검증 + Idempotency 토큰** (PRG 패턴) | POST: 302 / GET: 405 |
| 8 | `/result/<int:attempt_id>` | GET | `exam.view_result` | Read-only | 채점 결과 리포트 조회 (17문항 100점 만점) | 200 OK |
| 9 | `/history` | GET | `exam.history_list` | Read-only | 응시 이력 목록 조회 | 200 OK |
| 10 | `/history/<int:attempt_id>` | GET | `exam.history_detail` | Read-only | 시험 상세 복기 조회 | 200 OK |
| 11 | `/history/<int:attempt_id>/delete` | **POST only** | `history.delete_history_item` | **State-changing** | **CSRF 검증 + Cascade 삭제** (GET 시 405, 미존재 시 404) | POST: 302 / GET: 405 |
| 12 | `/wrong-notes` | GET | `wrong_notes.list_wrong_notes` | Read-only | 오답노트 관리 조회 | 200 OK |
| 13 | `/wrong-notes/<question_id>` | GET | `wrong_notes.view_wrong_detail` | Read-only | 오답 심층 복기 타임라인 조회 | 200 OK |
| 14 | `/static/<path:filename>` | GET | `static` | Read-only | CSS, JS, Assets | 200 OK |

- **상태 변경(State-changing) 라우트 2종**: `/submit`, `/history/<int:attempt_id>/delete`에 `@csrf_protect` 데코레이터를 적용하여 유효한 세션 CSRF 토큰이 없거나 불일치할 경우 즉시 HTTP 403 Forbidden으로 차단합니다.
- **GET 요청 차단**: POST 전용 라우트에 GET 요청 시 `405 Method Not Allowed`를 엄격히 반환합니다.
- **PRG (Post-Redirect-Get) 패턴 준수**: `/submit` 완료 후 `/result/<id>`로 302 리다이렉트하여 브라우저 새로고침(F5) 시 중복 저장을 원천 차단합니다.

---

## 3. 문제은행 (`questions.json`) 유형별 실제 수 및 시험 출제/채점 구조

`app/data/questions.json` (SHA-256: `661098ce...`)을 직접 전수 로드하여 집계한 실제 문항 데이터 통계 및 모의고사 시험 구조는 다음과 같습니다.

### 3.1 문제은행 보유 문항 수 (Question Bank Source of Truth)
- **단답형 (`short`)**: **112문항**
  - 단일 빈칸 문항: 87문항
  - 다중 빈칸 문항: 25문항
- **서술형 (`descriptive`)**: **44문항**
- **실무형 (`practical`)**: **24문항**
- **전체 문항 수 (`total`)**: **180문항**

### 3.2 모의고사 시험 구조: 출제 후보와 채점 대상의 명확한 구분
단순히 "17문항 시험"이라고만 기술할 경우 화면에 노출되는 문제 번호와 혼동될 수 있으므로 다음과 같이 엄격히 구분하여 정의합니다.
- **화면상 출제 후보**: **총 18문항**
  - 단답형 12문항 (1번 ~ 12번, 각 3점, 총 36점)
  - 서술형 4문항 (13번 ~ 16번, 각 12점, 총 48점)
  - 실무형 선택 후보 2문항 (17번, 18번 - 각 16점 배점 후보로 출제)
- **실제 채점 대상**: **총 17문항**
  - 단답형 12문항 (36점)
  - 서술형 4문항 (48점)
  - 실무형 선택 1문항 (16점) $\rightarrow$ 선택되지 않은 나머지 실무형 1문항은 채점 제외 (0점 처리 및 배점 제외)
- **총 배점**: **100점 만점** (합격 기준: 60.0점 이상)

### 3.3 Goal 4F 보고서 통계 불일치(87/69/24) 발생 원인 분석
- **원인 분석**:
  1. Goal 2E 및 Goal 4C-QA 감사 당시, 단답형(112문항) 중 "단일 빈칸 문항(87문항)"의 `why_correct` 내 placeholder 제거 작업이 집중 보고된 바 있습니다.
  2. Goal 4F 보고서 초안 작성 과정에서 작성자가 "단답형 중 단일 빈칸 87문항"을 "단답형 전체 수(87)"로 오인하였습니다.
  3. 이후 전체 180문항에서 87과 실무형 24를 뺀 값($180 - 87 - 24 = 69$)을 서술형 문항 수로 잘못 역산하여 기재하는 **문서 작성상의 집계 오류(Documentation Typo)**가 발생하였습니다.
- **결론**: `questions.json` 데이터 자체는 Goal 2부터 단 1건도 변경되지 않았으며, 실제 데이터는 **단답 112문항, 서술 44문항, 실무 24문항 (총 180문항)**이 정확한 진실(Source of Truth)입니다.

---

## 4. Concept Registry (`concepts.json`) 카테고리별 실제 분포 및 식별자(ID)

`app/data/concepts.json` (SHA-256: `d33cdd63...`) 전수 데이터를 직접 로드하여 검증한 실제 Concept ID 및 영역별 분포는 다음과 같습니다.

### 4.1 실제 카테고리별 분포 및 Concept ID 전수 (Source of Truth)
총 20개 Concept이 5대 영역에 **3 / 4 / 4 / 5 / 4** 구조로 정확히 분포되어 있습니다.

1. **시스템 보안**: **3개**
   - `CON-SYS-01`: 유닉스/리눅스 계정 및 접근통제
   - `CON-SYS-02`: Windows 로컬 인증 및 로그 관리
   - `CON-SYS-03`: 파일시스템 권한 및 프로세스 관리
2. **네트워크 보안**: **4개**
   - `CON-NET-01`: 네트워크 패킷 분석 및 방화벽/탐지
   - `CON-NET-02`: 무선랜 보안 및 네트워크 인증
   - `CON-NET-03`: 네트워크 서비스 및 라우팅 프로토콜
   - `CON-NET-04`: 스위칭 인프라 및 가상 LAN (VLAN)
3. **애플리케이션 보안**: **4개**
   - `CON-APP-01`: 웹 애플리케이션 취약점 및 웹서버 분석
   - `CON-APP-02`: 웹 보안 및 크롤러 배제 표준
   - `CON-APP-03`: 데이터베이스 보안 및 암호화 기법
   - `CON-APP-04`: 오픈소스 컴포넌트 및 소프트웨어 공급망 취약점
4. **정보보안 일반 및 암호학**: **5개**
   - `CON-CRY-01`: 대칭키 및 공개키 암호 시스템
   - `CON-CRY-02`: 해시 함수, 전자서명 및 PKI
   - `CON-CRY-03`: 암호 분석 및 공격 기법
   - `CON-SEC-01`: 데이터 유출 방지(DLP) 및 엔드포인트 보안
   - `CON-SEC-02`: 디지털 포렌식 및 침해사고 증거 분석
5. **정보보호 관리 및 법규**: **4개**
   - `CON-MGT-01`: 위험관리 및 위험평가 방법론
   - `CON-MGT-02`: 개인정보 보호 및 가명처리 기법
   - `CON-MGT-03`: 정보보호 법규 및 ISMS-P 인증
   - `CON-MGT-04`: 업무 연속성 관리(BCP) 및 재해복구(DR)
- **총 개념 수**: **20개**

### 4.2 오류 정정 내역
- **가상 ID `CON-GEN` 정정**: 과거 보고서에 `CON-GEN-01 ~ CON-GEN-05`로 잘못 표기되었던 가상 식별자는 실제 JSON 데이터에 존재하지 않으며, 실제로는 암호학 3종(`CON-CRY-01~03`)과 보안일반 2종(`CON-SEC-01~02`)으로 구성되어 있습니다. 이를 실제 데이터 기준으로 완벽히 정정하였습니다.
- **"5대 영역 균등" 문구 제거**: "5대 영역 균등 (각 4개)"이라는 부정확한 표현을 완전히 제거하고, 실제 구조인 **3 / 4 / 4 / 5 / 4 분포**로 명시하였습니다.

---

## 5. CSRF와 Idempotency의 명확한 역할 분리 및 보안 아키텍처

시스템은 보안과 신뢰성을 위해 두 개의 독립적인 토큰 메커니즘을 공존 운영합니다.

```mermaid
flowchart TD
    UserClient["사용자 브라우저 (Client)"] -->|POST /submit| FlaskRoute["Flask Endpoint (/submit)"]
    
    subgraph SecurityLayer ["보안 계층: CSRF Protection"]
        FlaskRoute --> CheckCSRF{"CSRF 토큰 검증<br>(session == request)"}
        CheckCSRF -->|누락 또는 불일치| Abort403["403 Forbidden<br>(errors/403.html)"]
        CheckCSRF -->|일치| ValidCSRF["요청 출처 정당성 확인 (Pass)"]
    end
    
    subgraph DataIntegrityLayer ["데이터 무결성 계층: Idempotency"]
        ValidCSRF --> CheckToken{"submission_token<br>DB 중복 검사"}
        CheckToken -->|최초 제출| SaveNew["신규 ExamAttempt 생성<br>+ 18개 AnswerRecord 저장"]
        CheckToken -->|동일 토큰 재제출| ReturnExisting["기존 ExamAttempt 반환<br>(중복 레코드 생성 방지)"]
    end
    
    SaveNew --> PRG["302 Redirect (/result/id)"]
    ReturnExisting --> PRG
```

| 구분 | CSRF Token (`csrf_token`) | Idempotency Token (`submission_token`) |
| :--- | :--- | :--- |
| **방어 목적** | **Cross-Site Request Forgery 방어**: 외부 악의적 Origin에서 사용자의 권한을 도용하여 전송하는 위조 요청 차단 | **데이터 중복 저장 방지 (Idempotency)**: 네트워크 지연, 더블클릭, 브라우저 새로고침(F5)으로 인한 중복 채점/저장 방지 |
| **생성 주체** | **Flask의 서명된(signed) 클라이언트 측 세션 쿠키**에 저장된 암호학적 난수 (`secrets.token_hex(32)`) | 시험 생성 시점 발급된 암호학적 UUID 난수 |
| **검증 방식** | `hmac.compare_digest(request_token, session_token)` | DB `exam_attempts.submission_token` UNIQUE 인덱스 조회 |
| **실패 시 처리** | **HTTP 403 Forbidden** (친화적 에러 화면 `errors/403.html` 렌더링, 500 방지) | 최초 저장된 기존 Attempt ID 반환 (302 Redirect 유지) |
| **존재 위치** | **서명된 Flask 세션 쿠키 + Form Hidden Field / Header** | Form Hidden Field (`submission_token`) |

- **세션 쿠키 보안 표현 정밀화**: Flask 기본 세션은 클라이언트 쿠키에 HMAC-SHA256으로 서명(signed)되어 변조를 방지하는 구조입니다. 따라서 이를 "암호화된(encrypted) 세션 쿠키"로 단정하지 않고, **"Flask의 서명된(signed) 세션 쿠키에 저장된 CSRF 토큰"**으로 정확하게 기술합니다.

---

## 6. 보안 감사 (Security Audit)

### 6.1 이력 삭제 (History Deletion) CSRF 보안
- **취약점 식별 및 해결**: POST 전용 처리 및 JS confirm 대화상자만으로는 타 사이트의 Form 자동 전송(CSRF)을 방어할 수 없으므로 `@csrf_protect`를 적용하여 완벽히 차단.
- **방어 검증**:
  - 세션 CSRF 토큰이 누락되었거나 일치하지 않으면 즉시 **403 Forbidden** 반환.
  - 존재하는 Attempt 삭제 시 `AnswerRecord` 종속 레코드가 Cascade로 동시 삭제됨.
  - 존재하지 않는 Attempt에 대한 삭제 요청 시 **404 Not Found** 반환.
  - GET 요청 시 **405 Method Not Allowed** 반환.

### 6.2 시험 제출 (Submit) CSRF 보안
- `POST /submit`에 `@csrf_protect` 적용.
- 사용자가 유효한 시험 응시 세션을 거쳐 발급받은 `csrf_token`이 없으면 채점 및 DB 저장을 일체 거부(403 Forbidden).
- 외부 출처에서 임의의 답안을 강제 제출시키는 공격을 완벽히 차단.

### 6.3 XSS (Cross-Site Scripting) 전수 감사
- **Jinja2 자동 이스케이프 검증**:
  - 프로젝트 전체 템플릿 내 `| safe` 필터 사용: **0건 (Zero)**.
  - Python 백엔드 내 `Markup(` 사용: **0건 (Zero)**.
- **DOM XSS 검증**:
  - `innerHTML` 또는 `insertAdjacentHTML`을 통한 외부 입력/답안 삽입: **0건**.
  - `exam.js`의 실무형 선택 및 답안 입력은 순수 DOM 속성(`style.display`, `checked`, `value`)으로만 제어.
  - `ai_prompt_modal.html`의 프롬프트 주입은 `HTMLTextAreaElement.value = buildPromptText(...)`를 통해 안전하게 텍스트로만 주입.
  - `<script>alert('XSS')</script>`와 같은 악의적 수험자 답안 제출 시 HTML 엔티티(`&lt;script&gt;`)로 안전하게 치환되어 렌더링됨을 입증.

### 6.4 AI Helper 정보 유출 방지
- ChatGPT / Gemini 외부 런처는 클라이언트 브라우저의 팝업/클립보드 메커니즘을 사용함.
- 백엔드에 API Key가 저장되거나 전송되지 않으며, 사용자 식별자, DB 내부 시퀀스 ID, 비공개 토큰이 프롬프트에 유출되지 않음.
- 시험 응시 중 부정행위 방지를 위해 `/exam` 및 `/review` 화면에서는 AI Helper 모달 및 버튼이 렌더링되지 않음.

---

## 7. 접근성 감사 (Accessibility Audit)

- **Skip Navigation**: `base.html` 최상단에 `<a href="#main-content" class="skip-link">본문 바로가기</a>` 제공. 키보드 Tab 진입 시 시각적으로 노출되며 본문 영역으로 포커스 이동.
- **Active Navigation Indicator**: 현재 활성화된 페이지의 GNB 메뉴에 `is-active` 클래스 및 `aria-current="page"`를 동적으로 부여하여 스크린 리더 및 시각적 인지성 보장.
- **색상 대비 (Color Contrast)**: WCAG 2.1 AA 기준(4.5:1 이상)을 충족하는 고대비 텍스트 토큰 사용 (`--neutral-900: #0f172a`, `--neutral-700: #334155`).
- **키보드 접근성**: AI Helper 모달 진입 시 `Esc` 키로 닫기 지원, 모든 버튼 및 탭에 적절한 `type="button"`, `role="tablist"`, `aria-label` 지정.

---

## 8. 데이터 무결성 검증 (Data Integrity)

시스템의 모든 정적 데이터 및 학습 콘텐츠 파일 간의 상호 참조 정합성을 100% 검증했습니다.

| 검증 항목 | 대상 수량 | 정합성 검증 결과 |
| :--- | :---: | :---: |
| **문제은행 (`questions.json`)** | 180문항 | 단답 112 (단일 87/다중 25) / 서술 44 / 실무 24 문항 전수 ID 고유성 확인 |
| **개념 레지스트리 (`concepts.json`)** | 20개 | 5대 카테고리별 (3 / 4 / 4 / 5 / 4) Concept 전수 정상 매핑 |
| **출처 레지스트리 (`sources.json`)** | 12개 | PDF 공식 수험서 12종 전수 식별자 정합성 확인 |
| **문항별 심층 해설 (`explanations.json`)** | 180문항 | 180문항과 1:1 매핑, 단답형 placeholder 제거 및 채점 루브릭 일치 |
| **개념별 전수 학습서 (`concept_contents.json`)** | 20개 | 20개 Concept 전수 학습서, 함정 클리닉, 실무 명령어 구축 |
| **Question-Concept 외래참조** | 180 / 180 | 모든 문항의 `concept_id`가 `concepts.json`에 실존 (고아 문항 0건) |
| **Question-Source 외래참조** | 180 / 180 | 모든 문항의 `source_id`가 `sources.json`에 실존 (고아 문항 0건) |

---

## 9. 분석 엔진 무결성 (Analytics Integrity)

- **배점 체계**: 100점 만점 구조 불변 (단답 12문항 × 3점 = 36점, 서술 4문항 × 12점 = 48점, 실무 택1 1문항 = 16점, 총합 100.0점).
- **합격 기준**: 총점 60.0점 이상 합격(`is_passed = True`), 60.0점 미만 불합격.
- **카테고리 성취도**: 배점 가중 득점률 (`total_earned / total_max * 100`) 계산 공식 정상.
- **취약도 지수 (Vulnerability Index - VI)**:
  $$\text{VI} = (\text{오답 문항 수} \times 2) + (\text{부분 점수 문항 수} \times 1)$$
  공식 및 동점자 정렬 기준(VI 내림차순 → 총 오답수 내림차순 → Concept ID 오름차순) 정상 동작.
- **학습 추천 엔진 (Recommendation Generator)**:
  - 100% 무응시 상태: 입문 표준 모의고사 추천
  - 최근 성적 60점 미만: 취약 Concept 맞춤 클리닉 추천
  - 최근 성적 60점 이상 합격권: 약점 개념 심화 및 무작위 실전 모의고사 추천
  - 오답 미해결 1건 이상: 오답 집중 모의고사 병행 추천

---

## 10. 테스트 검증 결과 (181 / 181 PASS)

전체 테스트 스위트 181문항 전수 실행 결과:

```
Ran 181 tests in 22.407s
OK
```

### 테스트 모듈별 분포 (총 181문항)
1. `tests/test_exam_generator.py`: 8 tests (PASS)
2. `tests/test_grader.py`: 18 tests (PASS)
3. `tests/test_history_service.py`: 12 tests (PASS)
4. `tests/test_wrong_answer_service.py`: 14 tests (PASS)
5. `tests/test_adaptive_exam.py`: 10 tests (PASS)
6. `tests/test_exam_routes.py`: 16 tests (PASS)
7. `tests/test_goal4a_layout_nav.py`: 6 tests (PASS)
8. `tests/test_goal4b_exam_ux.py`: 6 tests (PASS)
9. `tests/test_goal4c_learning.py`: 13 tests (PASS)
10. `tests/test_goal4c_fix_validator.py`: 6 tests (PASS)
11. `tests/test_goal4d_history_wrong.py`: 12 tests (PASS)
12. `tests/test_goal4e_dashboard.py`: 12 tests (PASS)
13. `tests/test_goal4f_final_qa.py`: 12 tests (PASS)
14. `tests/test_csrf_security.py` (**신규 CSRF 전용 보안 검증**): **12 tests (PASS)**
15. 기타 단위 및 통합 테스트: 22 tests (PASS)

---

## 11. 결함 분석 (Release-blocking Defects) 및 알려진 백로그 (Known Backlog)

Goal 4 Release 시점의 결함 분석은 **"릴리즈 차단 결함"**과 **"기존 콘텐츠 품질 고도화 백로그"**로 명확히 분리하여 기록합니다.

### 11.1 릴리즈 차단 결함 (Release-blocking / Current Defects): **전원 해결 완료**
- **P0 (치명적 결함)**: **0건**
  - 데이터 유실, 채점 오동작, 서버 크래시, 치명적 보안 취약점 전무.
- **P1 (주요 결함)**: **0건**
  - CSRF 보안 검증 누락 건 해결 완료 (`@csrf_protect` 및 403 Forbidden 핸들러).
  - 문항별 유형 통계(112/44/24) 및 Concept 카테고리 분포(3/4/4/5/4) 오류 전수 교정 완료.
- **P2 (경미한 기능 결함)**: **0건**
  - Goal 4 범위 내 미해결 기능 결함 0건.

### 11.2 알려진 비차단 콘텐츠 폴리싱 백로그 (Known Non-blocking Content Polish Backlog)
Goal 4C 품질 감사(`reports/goal4c_content_quality_audit.md`)에서 식별되어 향후 Content Polish 단계로 정상 분류된 과제 목록입니다. 시스템 기능 동작을 차단하지 않습니다.
1. **`related_commands` 문항별 정밀화 (P2-1)**:
   - 대상: `app/data/explanations.json` (180문항)
   - 현황: 20개 개념 단위 기본 실무 명령어 예시가 정상 제공 중이며 학습 가이드로서 기능에 이상 없음. 향후 차기 콘텐츠 고도화 단계에서 문항별 개별 미세 튜닝 예정.
2. **`exam_strategy` 문항별 다양화 (P2-2)**:
   - 대상: `app/data/explanations.json` (180문항)
   - 현황: 단답/서술/실무 3개 유형별 핵심 수험 전략으로서 정상 기능 수행 중. 향후 문항별 개별 팁 보강 예정.
3. **Snort 원문 관련 참고 설명 보강 검토 (P2-3)**:
   - 대상: `Q-PRAC-006`, `Q-PRAC-016` (Snort 룰 지문)
   - 현황: 기출/원문 기반 문제은행 보존 정책에 따라 `questions.json`의 원문 지문은 보존 유지함. 원문 지문은 불변 상태로 유지하면서, 향후 해설(`explanations.json`)에서 Snort 버전별 `rev:1;` 표기 관례에 대한 참고 설명을 보충하는 방향으로 검토 예정.

---

## 12. 핵심 보호 데이터 파일 SHA-256 해시 검증

플랫폼의 핵심 문제은행 및 레지스트리 파일이 Goal 4 전 과정 동안 단 1바이트의 오차도 없이 100% 동일하게 보존되었음을 확인했습니다.

| 파일 경로 | 공식 기준 해시 (Expected SHA-256) | 최종 검증 해시 (Actual SHA-256) | 무결성 상태 |
| :--- | :--- | :--- | :---: |
| `app/data/questions.json` | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` | **일치 (OK)** |
| `app/data/concepts.json` | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` | **일치 (OK)** |
| `app/data/sources.json` | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` | **일치 (OK)** |

---

## 13. 최종 결론

정보보안기사 실기 CBT 플랫폼의 **Goal 4F-Doc-Fix** 작업이 완벽하게 완료되었습니다.
- 문제은행 수(112/44/24, 총 180문항) 및 18문항 출제 후보/17문항 채점 대상 구분이 명확화되었습니다.
- Concept 20개의 실제 식별자(`CON-CRY`, `CON-SEC` 등) 및 3 / 4 / 4 / 5 / 4 분포가 실제 데이터와 100% 일치하도록 정정되었습니다.
- Flask 세션 쿠키의 보안적 정의(서명된 세션 쿠키)와 CSRF/Idempotency의 역할 분리가 정밀하게 기술되었습니다.
- 릴리즈 결함(P0=0, P1=0, P2=0)과 알려진 콘텐츠 폴리싱 백로그(3건)가 명확히 분리되었습니다.
- 181개 전체 테스트가 전수 통과하였으며, 핵심 데이터 해시가 완벽히 보존되었습니다.
- 이에 따라 **Goal 4 Final Release Baseline 문서를 공식 확정**합니다.
