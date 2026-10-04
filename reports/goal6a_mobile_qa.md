# Goal 6A: Production Mobile QA & Mobile Issue Baseline Report

---

## A. Production Baseline

- **Production Target URL**: `https://web-production-246f1.up.railway.app`
- **Health Check Endpoint**: `https://web-production-246f1.up.railway.app/healthz` (`{"status": "healthy", ...}`)
- **Production Final Commit**: `7fef3efd92d66cf224601135ea1273837fd71019` (`7fef3ef`)
- **Production Final Tag**: `v0.5-production-final`
- **Preceding Tag**: `v0.5-production-ready`
- **Runtime Stack**: Railway + PostgreSQL + Gunicorn + Flask 3.1 + SQLAlchemy 2.0
- **Regression Test Baseline**: 215 tests total (214 PASSED, 1 SKIPPED, 0 FAILURES, 0 ERRORS)
- **Goal 5 Production Closure**: 100% COMPLETE (5 existing Goal 5 P2 items isolated in production backlog)

---

## B. Viewports Tested

The audit conducted automated DOM inspection, bounding client rect evaluations, element hierarchy traversal, touch target auditing, typography verification, and visual regression capture across three standard mobile screen dimensions:

| Viewport Profile | Resolution | Aspect Ratio | Representative Device Class |
|---|:---:|:---:|---|
| **Small Mobile** | **360 × 800 px** | 9:20 | Compact Android devices (Samsung Galaxy A series, budget smartphones) |
| **Standard Mobile** | **390 × 844 px** | 9:19.5 | Mainstream flagship smartphones (Apple iPhone 12 / 13 / 14 / 15 / 16) |
| **Large Mobile** | **430 × 932 px** | 9:20 | Large-screen smartphones (Apple iPhone Pro Max, Samsung Galaxy Plus / Ultra) |

*Desktop baseline reference viewports (1024px, 1280px, 1440px) were continuously monitored to ensure zero desktop layout regression.*

---

## C. Routes Tested (Full Inventory)

All 13 core application routes across Public, Owner (Authenticated), and Error boundaries were inspected under mobile emulation on live Railway production:

### 1. Public Zone (Guest Accessible)
1. **`/`** - Main Home / Portal Landing
2. **`/exam`** - 18-Candidate 실전 모의고사 응시 세션 (Short 12, Descriptive 4, Practical 2택1)
3. **`/review`** - 답안 최종 검토 화면 (POST-only form submission pass-through)
4. **`/result/<attempt_id>`** - 채점 결과 리포트 & AI 질의 프롬프트 모달
5. **`/concepts`** - 20대 핵심 보안 개념 도서관 카탈로그
6. **`/concepts/<concept_id>`** - 개념 심층 학습서 (e.g., `/concepts/CON-NET-01`)
7. **`/admin-login`** - Owner Passphrase 인증 진입 화면

### 2. Protected Zone (Owner Authenticated)
8. **`/dashboard`** - Owner 학습 진단 대시보드 (KPI, 5대 영역 레이더/가중 성취도, 취약 개념 클리닉)
9. **`/history`** - 모의고사 누적 응시 이력 목록 (8컬럼 데이터 테이블)
10. **`/history/<attempt_id>`** - 회차별 채점 상세 복기 리포트 (e.g., `/history/7`)
11. **`/wrong-notes`** - 오답노트 & 취약 문항 복습 목록 (필터 칩, 카드 뷰)
12. **`/wrong-notes/<question_id>`** - 문항 심층 복기 리포트 (e.g., `/wrong-notes/Q-PRAC-001`)

### 3. Error Boundary
13. **Error Pages**: 403 Forbidden (CSRF token verification failure) & 404 Not Found (Invalid route / concept ID)

---

## D. Global Layout QA Findings

1. **Horizontal Viewport Stability**:
   - General containers with standard `.card` and flex wrappers stay within the bounds of 360px, 390px, and 430px viewports without unconstrained horizontal overflow.
   - However, specific unconstrained CSS Grid tracks (`.exam-container`, `.clinic-item`) and flex headers with `flex-shrink: 0` cause layout viewport expansion on narrow devices (detailed in Section T).
2. **Navigation Header & Mobile Bottom Bar**:
   - Header title `정보보안기사 실기시험 CBT` properly scales and wraps cleanly across all tested viewports.
   - Global bottom navigation (`.nav-mobile-bottom`) is rendered on general public and owner views, offering single-tap access to Home, Dashboard, Concepts, Exam, History, and Wrong Notes.
   - On `/exam` and `/review`, the global bottom navigation is cleanly suppressed via `is-exam-session` / `hide_mobile_global_nav: true`, preventing navigation conflicts during active exam sessions.
3. **Safe Area & Footer Padding**:
   - Content bottom padding (`padding-bottom: 72px` on `.has-mobile-nav`) ensures the fixed bottom navigation bar does not overlap bottom card actions or text content.

---

## E. Exam View (`/exam`)

1. **Question Card Stacking**:
   - 12 단답형 cards, 4 서술형 cards, and 2 실무형 cards stack vertically with clean separation.
   - Question badges (`단답형`, `서술형`, `실무형`) and category pills display legibly without clipping.
2. **Input Fields & Textareas**:
   - Short answer inputs (`input[type="text"]`) span 100% width within question rows.
   - Textareas provide adequate vertical height for drafting descriptive answers.
3. **Viewport Inflation Root Cause (MOB-001)**:
   - On `/exam`, the document width expands to 1516px on 360px/390px/430px screens.
   - *Technical Cause*: `.exam-container` uses CSS Grid `grid-template-columns: 1fr` at `@media (max-width: 900px)`. Under CSS Grid specification, grid items default to `min-width: auto`. Because `.exam-main` does not declare `min-width: 0`, and the grid track does not use `minmax(0, 1fr)`, the track stretches to fit the maximum intrinsic content width of its children (1504px).
   - *Consequence*: The browser layout viewport expands to 1440px~1516px. Because the layout viewport exceeds 767px, `@media (max-width: 767px)` rules fail to match, causing `.mobile-exam-action-bar` to render as a 1440px wide bar and displacing `#btn-mobile-sheet-open` off-screen to x=1196px.
   - *Verified Sandbox Resolution*: Applying `.exam-container { grid-template-columns: minmax(0, 1fr); }` and `.exam-main { min-width: 0; }` instantly resolves the inflation, setting document width to exactly 360px and restoring normal mobile action bar behavior.

---

## F. Review View (`/review`)

1. **Access Workflow & Stability**:
   - `/review` is strictly a POST route accepting raw form pass-through data from `/exam`.
   - Direct GET requests yield standard HTTP 405. When reached via the valid POST submission flow, `docWidth` equals exactly 360px, 390px, and 430px with **zero horizontal overflow** (`overflow: false`).
2. **KPI Summary Cards**:
   - `.spec-grid` stacks neatly; response counters (작성 완료, 미완료 문항, 실무형 선택) wrap legibly.
3. **Question Review Table**:
   - The 17-question summary table is enclosed in `<div style="overflow-x: auto; max-width: 100%; -webkit-overflow-scrolling: touch;">`.
   - While horizontally scrollable within the card without breaking the page, the 5-column table structure is dense on 360px screens (cataloged under MOB-005 for card-stack refinement in Goal 6B).
4. **Submission CTA**:
   - Double-submit prevention (`dataset.submitted = 'true'`, button disabling, text change to `채점 및 저장 중...`) functions reliably on mobile touch events.

---

## G. Result View (`/result/<attempt_id>`)

1. **Score Banner & Breakdown**:
   - Total score display, pass/fail badge, and type score grid (`.section-score-grid`) adapt cleanly to mobile viewports.
   - At `@media (max-width: 768px)`, `.section-score-grid` stacks to single-column (`grid-template-columns: 1fr`).
2. **Filter Tabs & Question Cards**:
   - Filter buttons (전체, 단답, 서술, 실무) wrap cleanly.
   - Model answer boxes, rubric listings, and explanations wrap without horizontal overflow.
3. **AI Prompt Generator Modal**:
   - Trigger button opens the interactive AI modal.
   - On 390px and 430px viewports, the modal dialog stays centered within the viewport. On 360px viewports, edge margins are narrow (cataloged under MOB-008).

---

## H. Concepts Views (`/concepts`, `/concepts/<id>`)

1. **Concepts Catalog (`/concepts`)**:
   - 20 standard concept cards stack vertically in a clean single-column layout.
   - Category filter pills wrap legibly across multiple lines.
   - Concept cards display category badges, analytics pills, and reading time indicators.
2. **Concept Detail (`/concepts/<concept_id>`)**:
   - Reading line-length and typography provide comfortable readability on 360px~430px screens.
   - Markdown sections (핵심 원리, 메커니즘, 출제 포인트, 실기 대비 핵심 요약) render cleanly.
   - Code blocks (`pre`, `code`) maintain `overflow-x: auto` containment without triggering document-level horizontal scrolling.
   - Related question links at the bottom of the page maintain proper touch targets.

---

## I. Dashboard View (`/dashboard`)

1. **KPI & Quick Action Cards**:
   - Top KPI metric cards (누적 응시 횟수, 최근 점수, 전체 평균 점수, 오답 복습률) wrap and stack predictably.
2. **Two-Column Main Analysis Grid Inflation (MOB-003)**:
   - Line 131 of `dashboard.html` defines:
     `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap: 20px; ...">`
   - Because `minmax(460px, 1fr)` imposes a rigid 460px column minimum, the grid container forces the layout width to 460px+ on screens narrower than 480px, causing the entire dashboard to expand past 360px/390px/430px viewports.
   - *Fix for Goal 6B*: Replace inline grid style with a responsive CSS class that transitions to `grid-template-columns: 1fr` for viewports under 768px.

---

## J. History Views (`/history`, `/history/<id>`)

1. **History List (`/history`)**:
   - Enclosed inside `<div class="card" style="padding: 0; overflow-x: auto;">`.
   - The 8-column table (회차, 응시 일시, 시험 모드, 총점, 합격 여부, 영역별 점수, 복습 필요도, 관리) has a minimum width of ~750px.
   - The table scrolls horizontally inside the card container without breaking the document viewport width (`docWidth = 360px`).
   - However, horizontally scrolling across 8 dense columns on a smartphone degrades usability (cataloged under MOB-005 for card-view transformation in Goal 6B).
2. **History Detail (`/history/<attempt_id>`)**:
   - Displays full retrospective review of past attempt answers, rubrics, and earned scores.
   - Document width conforms strictly to 360px, 390px, and 430px viewports with zero horizontal overflow.

---

## K. Wrong Notes Views (`/wrong-notes`, `/wrong-notes/<id>`)

1. **Wrong Notes List (`/wrong-notes`)**:
   - Summary cards (`.wrong-summary-grid`) stack into single-column cards on 360px viewports.
   - Filter bar and question cards wrap appropriately.
   - On 360px screens, the header actions and bottom nav cause slight width inflation to 376px (MOB-002 / MOB-006).
2. **Wrong Detail View (`/wrong-notes/<question_id>`)**:
   - Deep explanation accordion, model answers, rubric tables, and attempt timeline render completely.
   - *Header Action Inflation (MOB-006)*: The page header contains 3 action buttons (`&larr; 오답노트 목록으로`, `🔥 오답 집중 모의고사`, `새 모의고사 응시`). Because `.header-actions` has `flex-shrink: 0;` and cannot wrap or collapse on mobile, the header expands to 505px, inflating the document viewport on 360px/390px/430px screens.

---

## L. Admin Authentication (`/admin-login`)

1. **Login Card & Passphrase Input**:
   - Login card is centered with `max-width: 440px`.
   - Passphrase input field, submit button (`인증 및 관리자 모드 진입`), and home navigation link fit within 360px viewports (`docWidth = 360px`).
   - CSRF protection token is properly embedded.
2. **Mobile Keyboard Considerations**:
   - On touch focus, the passphrase input triggers the mobile soft keyboard.
   - The login card remains visible above the keyboard fold.

---

## M. Modal QA (AI Prompt Modal)

1. **Dialog Presentation**:
   - The modal overlay covers the full viewport (`position: fixed; inset: 0`).
   - Modal header, close button (`✕`), textarea for customizable prompt, copy button (`📋 프롬프트 복사`), and external AI shortcuts (ChatGPT, Claude) render properly.
2. **Mobile Constraints (MOB-008)**:
   - On 360px viewports, horizontal margin is constrained (padding leaves ~8px gutter on narrow screens).
   - Textarea auto-sizing needs minimum touch height and scrolling clearance when virtual keyboard is active.

---

## N. Touch Targets & Typography QA

1. **Touch Target Size Violations (MOB-007)**:
   - Interactive elements with touch dimensions < 44×44px were audited:
     - Radio buttons (`#radio-Q-PRAC-001`, `#radio-Q-PRAC-002`): 13 × 13 px (requires tap area expansion via parent label padding).
     - Breadcrumb navigation links: height ~16px.
     - History table delete buttons: height ~32px.
     - Filter type buttons (`.filter-type-btn`): height ~28px.
     - Secondary header buttons: height ~32-36px.
2. **Form Input Typography & iOS Auto-Zoom (MOB-004)**:
   - Form inputs (`input[type="text"]`, `input[type="password"]`, `textarea`) currently declare `font-size: 12px ~ 15px`.
   - On iOS Safari / WebKit browsers, tapping any form control with `font-size < 16px` automatically triggers an involuntary page zoom that throws off layout centering and requires manual pinch-to-zoom reset.
   - Setting `font-size: 16px` on text inputs and textareas below 768px is required in Goal 6B.

---

## O. Accessibility Mobile QA

1. **Semantic HTML & Headings**:
   - Heading hierarchy (`h1` -> `h2` -> `h3`) is preserved across all views.
   - Color contrast on text badges (`단답형`, `서술형`, `실무형`, `합격`, `불합격`) meets WCAG 2.1 AA requirements.
2. **Screen Reader & Keyboard Accessibility**:
   - Skip link (`본문 바로가기`) is present at the top of every page.
   - Form controls have matching `id` and `label` associations.
   - Interactive drawers and modals declare appropriate `aria-hidden` attributes.

---

## P. Performance Sanity

- **Page Load Speed**: All 13 routes load under 1.2s on standard mobile 4G network emulation.
- **Asset Size**: Single consolidated CSS bundle (`style.css`, 69KB uncompressed, ~14KB gzip). No heavy external client-side JavaScript frameworks or fonts.
- **Layout Shift (CLS)**: Zero disruptive Cumulative Layout Shifts observed during standard rendering passes.

---

## Q. Real Device Manual Checklist

The following items involve physical device hardware, virtual keyboard view transitions, touch gesture dynamics, and WebKit-specific engine behaviors that require manual verification on real physical devices (iOS & Android):

- [ ] **DEV-001: Soft Keyboard Viewport Resize & Focus Jump**
  - *Device*: Physical iPhone (Safari) & Android (Chrome)
  - *Action*: On `/exam`, tap into descriptive question textarea.
  - *Verification*: Confirm virtual keyboard opens smoothly, active textarea is not obscured behind the keyboard, and the page does not jump erratically.
- [ ] **DEV-002: iOS Input Auto-Zoom Immunity**
  - *Device*: Physical iPhone (Safari)
  - *Action*: Tap into short answer input on `/exam` and passphrase input on `/admin-login`.
  - *Verification*: Confirm Safari does NOT involuntarily zoom in and break horizontal boundaries.
- [ ] **DEV-003: Bottom Action Bar & iOS Home Indicator Safe Area**
  - *Device*: Physical iPhone with Home Bar (iPhone 12/13/14/15/16)
  - *Action*: Scroll to bottom of `/exam` and `/review`.
  - *Verification*: Confirm `.mobile-exam-action-bar` and `.nav-mobile-bottom` respect `env(safe-area-inset-bottom)` and do not collide with the system swipe bar.
- [ ] **DEV-004: Question Drawer Touch Gestures & Scroll Locking**
  - *Device*: Physical Android & iOS smartphone
  - *Action*: On `/exam`, tap `문항 목록 (18)`, scroll the question drawer list, tap backdrop to dismiss.
  - *Verification*: Confirm body background scrolling is locked while drawer is open, and tapping a question smoothly scrolls to the target question card.
- [ ] **DEV-005: Practical 2-Choice Radio Selection Touch Sensitivity**
  - *Device*: Physical smartphone with small screen (360px)
  - *Action*: Select between Q-PRAC-001 and Q-PRAC-002.
  - *Verification*: Confirm entire card/label area responds reliably to thumb taps without false miss-clicks.
- [ ] **DEV-006: AI Prompt Modal Copy to Clipboard**
  - *Device*: Physical iOS & Android device
  - *Action*: On `/result/<id>`, tap AI prompt button, then tap `📋 프롬프트 복사`.
  - *Verification*: Confirm system clipboard toast displays and prompt is successfully copied.

---

## R. Mobile Issue Matrix (Consolidated & Deduplicated)

| ID | Route(s) | Viewport(s) | Component | Severity | Problem Summary | Reproduction | Expected | Actual | Recommended Fix | Target Goal |
|---|---|:---:|---|:---:|---|---|---|---|---|:---:|
| **MOB-001** | `/exam` | 360, 390, 430 | Layout Grid / Action Bar | **P1** | CSS Grid track min-width expansion inflates document to 1516px; breaks media query and displaces mobile bottom action bar | Load `/exam` at 360px width | `docWidth <= 360px`, action bar visible at bottom | `docWidth = 1516px`, viewport inflates, action bar button displaced to x=1196px | Add `.exam-container { grid-template-columns: minmax(0, 1fr); }` and `.exam-main { min-width: 0; }` | **Goal 6B** |
| **MOB-002** | `/`, `/concepts`, `/wrong-notes` | 360 | Global Bottom Nav | **P2** | Bottom navigation grid column count mismatch (6 items vs 5-col grid template) causes 12px overflow on 360px screens | Load `/concepts` at 360px width | `docWidth <= 360px` | `docWidth = 372px` (12px horizontal expansion) | Update `.nav-mobile-grid` to `grid-template-columns: repeat(6, 1fr)` and adjust icon/label sizing | **Goal 6B** |
| **MOB-003** | `/dashboard` | 360, 390, 430 | Analysis Grid | **P1** | Inline style `minmax(460px, 1fr)` on 2-column analysis grid enforces 460px min-width, inflating dashboard layout on screens < 480px | Load `/dashboard` at 360px or 390px | `docWidth <= viewport width` | `docWidth = 472px` (horizontal overflow on mobile) | Move inline style to responsive class stacking to `1fr` below 768px | **Goal 6B** |
| **MOB-004** | `/exam`, `/admin-login`, Modal | 360, 390, 430 | Form Inputs & Textareas | **P2** | Text inputs and textareas have `font-size: 12px ~ 15px`, which triggers involuntary page zoom on iOS Safari | Tap input on iOS Safari | Page remains at 100% scale without zoom | iOS Safari auto-zooms into input, disrupting viewport scale | Set `font-size: 16px` on text inputs and textareas for mobile viewports below 768px | **Goal 6B** |
| **MOB-005** | `/history`, `/review` | 360, 390 | Data Tables | **P2** | Dense multi-column desktop tables (8 cols on `/history`, 5 cols on `/review`) require extensive horizontal scrolling on mobile | Load `/history` at 360px width | Mobile-friendly stacked card layout | Wide table contained in `overflow-x: auto` requiring panning | Transform table into responsive stacked summary cards for viewports < 768px | **Goal 6B** |
| **MOB-006** | `/wrong-notes/<id>`, Detail Pages | 360, 390, 430 | Header Actions | **P1** | Multiple action buttons in `.header-actions` with `flex-shrink: 0` inflate `.header-content` to 505px | Load `/wrong-notes/Q-PRAC-001` at 360px | `docWidth <= 360px` | `docWidth = 505px` (inflates layout viewport) | On viewports < 768px, hide secondary action buttons from header or wrap into action toolbar | **Goal 6B** |
| **MOB-007** | Global, `/exam`, `/history` | 360, 390, 430 | Interactive Elements | **P2** | Interactive controls (radio buttons: 13x13px, filter buttons: 28px height, delete buttons: 32px) fall below recommended 44px touch target | Inspect touch targets on 360px | Touch targets >= 44×44px | Touch targets between 13px and 36px | Increase tap padding, min-height: 44px, min-width: 44px on mobile interactive elements | **Goal 6B** |
| **MOB-008** | `/result/<id>` | 360 | AI Prompt Modal | **P2** | AI modal dialog edge gutters are narrow on 360px screens and lack virtual keyboard scrolling offset | Open AI modal on 360px width | Modal centered with 16px side margins | Modal edges sit tight against viewport boundary | Adjust modal max-width: `calc(100vw - 32px)` and add safe scrolling clearance | **Goal 6B** |

---

## S. P0 Issue Count: 0

- **P0 Count**: **0**
- No mobile data loss, session contamination, authentication bypass, CSRF token invalidation, or cross-tenant data exposure defects exist on mobile.

---

## T. P1 Issue Count: 3

- **P1 Count**: **3**
  1. **MOB-001**: `/exam` CSS Grid layout track expansion inflating viewport to 1516px and breaking mobile bottom action bar positioning.
  2. **MOB-003**: `/dashboard` inline style `minmax(460px, 1fr)` enforcing 460px minimum width and causing horizontal overflow on all mobile screens < 480px.
  3. **MOB-006**: Header action buttons with `flex-shrink: 0` inflating header to 505px on `/wrong-notes/<id>` and multi-button detail views.

*All 3 P1 issues are layout / CSS constraint defects; none break core server-side functionality or cause data integrity failure.*

---

## U. P2 Issue Count: 5

- **P2 Count**: **5**
  1. **MOB-002**: Mobile bottom navigation 6-item column mismatch causing 12px expansion on 360px screens.
  2. **MOB-004**: Form inputs font-size < 16px triggering iOS WebKit auto-zoom behavior.
  3. **MOB-005**: Dense multi-column data tables requiring horizontal scrolling on `/history` and `/review`.
  4. **MOB-007**: Interactive touch target sizing below 44×44px on buttons, pills, and radio controls.
  5. **MOB-008**: AI prompt modal dialog sizing margins and keyboard clearance on compact 360px viewports.

---

## V. Goal 6B Scope Recommendation

Based on the empirical findings of Goal 6A, the scope for **Goal 6B (Mobile UI Polish)** is clearly fixed to the following targeted improvements:

1. **Fix Layout Viewport Inflation (P1)**:
   - Update `.exam-container` in `style.css` to use `grid-template-columns: minmax(0, 1fr)` and apply `min-width: 0` to `.exam-main`.
   - Replace inline `minmax(460px, 1fr)` on `dashboard.html` with responsive CSS class that transitions to `1fr` below 768px.
   - Refactor `.header-actions` to allow wrapping or collapse secondary buttons into page action bars on mobile.
2. **Polish Navigation & Alignment (P2)**:
   - Update `.nav-mobile-grid` to accommodate all 6 navigation items cleanly on 360px screens.
   - Set `font-size: 16px` on text inputs and textareas for mobile viewports to prevent iOS auto-zoom.
   - Provide card-based responsive views for `/history` and `/review` on viewports < 768px.
   - Expand touch target tap areas to meet 44×44px standards for radio buttons, action pills, and filter controls.
   - Refine AI prompt modal dialog max-width and margin for compact mobile displays.

---

## W. Preserved Production P2 Backlog (Non-Mobile)

The 5 existing Goal 5 production backlog items remain completely preserved and distinct from mobile UI polish:
- **P2-1**: Scripts & tool cleanup (scripts/ cleanup completed in Goal 5B-Final, generic source path)
- **P2-2**: Strict CSP & HSTS header enhancements for production reverse proxy
- **P2-3**: Guest session & attempt retention TTL cleanup cron job
- **P2-4**: Database Alembic migration workflow for future schema updates
- **P2-5**: Structured JSON logging & centralized monitoring integration
