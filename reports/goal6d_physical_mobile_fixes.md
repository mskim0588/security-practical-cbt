# Goal 6D-PreFix — Physical Mobile Device Findings Fix

## A. Baseline

- Branch: `master`
- Goal 6C documentation baseline: `9fdbe2cbf8c656d9d2564add44709834246b9189`
- Mobile-fix commit: `4c0bfc206e0c2bb56f57e7f2f38f39710e72764e`
- Goal 6A: complete
- Goal 6B: complete and preserved
- Goal 6C: `PASS_WITH_MANUAL_DEVICE_CHECKS`
- Scope remained limited to the five confirmed physical-device findings and regression verification of the named routes.

## B. Physical Device Findings

| ID | Initial Severity | Result |
|---|---:|---|
| MDEV-001 — AI Prompt Clipboard | P2 | `RESOLVED_PENDING_PHYSICAL_DEVICE_RETEST` |
| MDEV-002 — Concept Search Overflow | P2 | `RESOLVED` |
| MDEV-003 — Long Unbroken Text Wrapping | P2 | `RESOLVED` |
| MDEV-004 — Dashboard Heading Wrapping | P2 | `RESOLVED` |
| MDEV-005 — Literal `&rarr;` Display | P2 | `RESOLVED` |

No finding escalated to P1.

## C. MDEV-001

- The existing shared AI Prompt Helper implementation was inspected before modification.
- Copy now attempts `navigator.clipboard.writeText(...)` only in a secure context when the API exists.
- Rejection or API absence falls back to exact textarea selection plus `document.execCommand("copy")`.
- Success feedback is emitted only after the Clipboard API resolves or the fallback returns `true`.
- Complete failure keeps the prompt visible, selects it, and displays: `자동 복사가 지원되지 않습니다. 텍스트를 길게 눌러 복사하세요.`
- Duplicate direct modal includes were removed from history and wrong-note templates because the shared base template already includes the component once.
- Automated Chromium checks confirmed real clipboard content equality, explicit success, fallback failure messaging, retained visibility, and manual selection.
- Physical Android clipboard re-verification remains required.

## D. MDEV-002

- The concept search row now uses `grid-template-columns: minmax(0, 1fr) auto`.
- The field and input use `min-width: 0`; the input uses full available width.
- The search button uses `white-space: nowrap` and remains inside the filter card.
- No page-level clipping or `overflow-x: hidden` workaround was added.
- Local and production viewport checks confirmed that the button remains visible and `검색` stays on one line at 360, 390, and 430 pixels.

## E. MDEV-003

- Normal question, answer, explanation, concept, hint, rubric, and related prose surfaces use local safe wrapping with `min-width: 0`, `overflow-wrap: anywhere`, and `word-break: break-word`.
- Preformatted command/code content retains `white-space: pre`, normal word breaking, and local horizontal scrolling in its existing code container.
- Long-token probes confirmed prose wrapping without page-level horizontal overflow and code scrolling without forced technical-line wrapping.

## F. MDEV-004

- The dashboard heading now uses the dedicated `dashboard-page-title` class.
- The class uses a responsive clamped font size, `word-break: keep-all`, and a mobile-appropriate line height.
- Browser measurement confirmed that `대시보드` remains on one line at 360, 390, and 430 pixels without page overflow.

## G. MDEV-005

- Escaped dynamic dashboard recommendation strings were changed from `&rarr;` to the Unicode arrow `→`.
- No broad Jinja `safe` filter was introduced.
- Browser checks confirmed that the dynamic CTA contains the Unicode arrow and does not display the literal entity text.
- Static template entities remain unchanged because HTML parses those occurrences as arrows rather than literal text.

## H. Admin Route Regression

- Local authenticated browser verification covered `/dashboard`, `/history`, `/history/<id>`, `/wrong-notes`, and `/wrong-notes/<id>`.
- All checked pages returned HTTP 200 locally, fit their viewport, retained the six-item mobile navigation, and kept action controls clear of page-level overflow.
- History and wrong-note screens were not redesigned; changes were limited to safe prose wrapping and removal of duplicate shared-modal includes.
- Production anonymous requests correctly redirected protected list/detail routes to `/admin-login`; authenticated production bodies were not claimed as inspected without credentials.

## I. Viewport Regression

Local Chromium checks at `360 × 740`, `390 × 844`, and `430 × 932` covered:

- `/concepts`
- `/dashboard`
- `/result/<session-owned-id>`
- `/history`
- `/history/<id>`
- `/wrong-notes`
- `/wrong-notes/<id>`
- `/concepts/<id>`

Every route had document width equal to viewport width, one shared AI modal, no uncaught page exception, and no failed required resource request. The only console resource message was the existing optional `/favicon.ico` 404.

## J. Desktop Regression

- The same route matrix passed at `1280 × 800`.
- No page-level horizontal overflow occurred.
- Search layout, heading, long prose, code scrolling, and Unicode arrow behavior remained correct.

## K. Tests

- Command: `python -m unittest discover tests -v` using the project-compatible isolated Python environment.
- Ran: 228
- Passed: 227
- Skipped: 1
- Failures: 0
- Errors: 0
- The single skip is the expected `test_sources_match_external_files` skip when `PRIVATE_SOURCE_DIR` is not configured.
- Five stable Goal 6D-PreFix regression tests were added; the increase from the 223-test Goal 6C baseline is legitimate.

## L. Core Hashes

| Dataset | SHA-256 | Result |
|---|---|---|
| `questions.json` | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` | MATCH |
| `concepts.json` | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` | MATCH |
| `sources.json` | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` | MATCH |
| `concept_contents.json` | `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171` | MATCH |
| `explanations.json` | `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696` | MATCH |

Core data result: `5 / 5 MATCH`; no core JSON file changed.

## M. Changed Files

- `app/routes/dashboard_routes.py`
- `app/static/css/style.css`
- `app/templates/components/ai_prompt_modal.html`
- `app/templates/concepts/index.html`
- `app/templates/dashboard.html`
- `app/templates/history_detail.html`
- `app/templates/result.html`
- `app/templates/wrong_detail.html`
- `app/templates/wrong_notes.html`
- `tests/test_goal6d_physical_mobile_fixes.py`
- `reports/goal6d_physical_mobile_fixes.md`

## N. Production Deployment

- `master` was pushed normally; no force push was used.
- Railway auto-deployed the mobile-fix commit.
- `GET /`: HTTP 200.
- `GET /healthz`: HTTP 200 with `status: ok`, `database: healthy`, and `environment: production`.
- Production served the new dashboard title CSS, concept search markup, and clipboard failure fallback text.
- Production `/concepts` passed headless Chromium checks at all four target viewports with no page-level overflow, a visible single-line search button, and no uncaught page exception.
- Protected production routes redirected anonymous requests to `/admin-login`, and `/result/1` denied access with HTTP 403 as designed. No authenticated production content claim is made without an authorized production session.

## O. Remaining Manual Device Checks

- Re-test prompt copy on the original physical Android browser, including the system clipboard contents.
- Confirm manual long-press selection behavior when automatic copying is unavailable.
- Goal 6C physical iOS Safari checks remain separate manual-device requirements: soft keyboard, input zoom, safe area/Home Indicator, touch drawer gesture, and clipboard permission behavior.

## P. P0 / P1 / P2

- P0: 0
- P1: 0
- P2 findings addressed in this task: 5
- Automated resolution: MDEV-002, MDEV-003, MDEV-004, MDEV-005
- Pending physical confirmation: MDEV-001
- Pre-existing known cross-browser P2 `CB-001` remains unchanged and non-blocking.

## Q. Goal 6D Finalization Readiness

Status: `READY_FOR_PHYSICAL_DEVICE_RETEST`

The code, automated regression, core data, deployment, health, and available production smoke criteria pass. Final Goal 6D closure and any `v0.6-mobile-final` tag remain blocked on the requested physical-device re-test. Goal 6D was not finalized, and Goal 7 was not started.
