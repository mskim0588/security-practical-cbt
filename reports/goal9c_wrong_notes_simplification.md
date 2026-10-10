# Goal 9C — Wrong Notes UI Simplification

## Checkpoint

- Status: Goal 9C COMPLETE. Functional verdict: `GOAL_9C_COMPLETE`. Physical Android: PASS — USER CONFIRMED ("정상 동작 확인했어"); this is user-reported normal operation, not independent automated device testing. Goal 9D readiness: `GOAL_9D_READY`; Goal 9D/9E NOT STARTED.
- Baseline HEAD: `df9b72977969899cb40f29de8c2e93ad0af42db8`; clean `master` = `origin/master`; Goal 9A and 9B COMPLETE; `v0.8-learning-final` remains at `2483cb01928282d6dd3f180b527771191773e59b`.
- Last Safe Step: feature commit `11a74fbb07afca2c34b555915cae7bde79a3889e` pushed with clean `master` = `origin/master`; exact-commit Railway `SUCCESS` and public/Guest production smoke passed. Local Chrome QA passed at four requested viewports. Focused tests passed 21/21; final full regression: 332 ran / 331 passed / 1 skipped / 0 failures / 0 errors; protected hashes 5/5 MATCH.
- Next Step: commit and push this report-only closure; verify Railway `SUCCESS` for the exact closure commit and recheck production health. Do not start Goal 9D automatically.

## Existing architecture and old-to-new mapping

| Existing information | Goal 9C placement |
| --- | --- |
| Three summary counts, wrong-review CTA, type/status/category/sort filters | Retain above the list with existing semantics and defaults. Remove redundant mobile header actions; the review CTA and global exam navigation remain reachable. |
| One grouped card per unresolved Question; ID, type, category, Concept, latest result, failure frequency/rate, attempts | Concise list card with linked question preview, metadata, counts, existing failure rate, date, and detail action. |
| Full submitted answer, model answer, accepted answers, and deep explanation in every card | Existing `/wrong-notes/<question_id>` detail. |
| Source title and page | Existing detail; display only safe title/page, never raw source metadata. |
| Full Question text, canonical answer/rubric, explanation, attempt timeline, Concept link, AI Helper, bookmark control | Retain in existing Owner-only detail route, with light navigation for long content. |

## Canonical behavior to preserve

- `WrongAnswerService.get_wrong_questions()` groups scored Owner `AnswerRecord` rows by Question ID. The newest record determines unresolved `incorrect` or `partial` status; `sufficient` resolves the note. `unselected` practical candidates and learning-only modes are excluded. Existing counts, filters, and latest/frequency sorting remain authoritative; no new scoring or aggregation rules.
- `get_wrong_question_detail()` returns the existing per-Question attempt timeline with dates, answers, status, score, grading feedback, and links to existing History detail. Deleted attempts cascade their answer rows; a valid Question with no remaining history has an existing empty state.
- AI Helper remains local prompt generation on the post-answer detail explanation component. The browser-local bookmark button remains independent of grading-derived Wrong Notes and mock Review Flags. No new endpoint, storage key, schema, or production Owner authentication flow.
- The list now renders one semantic card per Question with a linked two-line preview, type, category, optional Concept, latest score/status, supported failure/attempt counts and rate, and optional date. It no longer renders submitted/model answers or deep explanations repeatedly. The existing detail retains those fields, rubric, timeline, AI Helper, bookmark button, and safe source title/page. Long detail pages gained section links; raw string source metadata is not displayed. Same-timestamp timeline rows now use descending AnswerRecord ID as a stable tie-break. Desktop detail header actions remain; on mobile the in-page navigation and bottom action card avoid overlapping the title.

## Verification ledger

| Area | State | Evidence or next action |
| --- | --- | --- |
| Baseline, Goal 9A/9B, architecture inventory, old-to-new mapping | DONE | Clean parity and source/report inspection. |
| List/detail presentation, accessibility, low-data states | DONE locally | Templates/CSS changed; rendered empty, low-data, aggregation, and detail tests passed. Chrome QA passed. |
| Aggregation, grading, VI, adaptive, Goal 7/8, bookmarks, Review Flags | DONE locally | Service and data rules inventoried; final full regression passed. |
| Owner isolation, AI Helper, private source display | DONE locally | New focused tests cover Guest redirect, Owner scope, detail AI control, bookmark action, and raw source omission. |
| Targeted tests | DONE | New Goal 9C tests 5/5; existing Wrong Notes/history tests 16/16. |
| Full regression, core hashes | DONE | Final post-edit run: 332 ran / 331 passed / 1 skipped / 0 failures / 0 errors. Fresh 5/5 SHA-256 MATCH against Goal 8 release hashes; 20 Concepts / 67 Topics / 180 Questions / 39 Aliases. |
| Browser QA | DONE locally | Headless Chrome DevTools on synthetic authenticated Owner: empty and populated list/detail at 360×740, 390×844, 430×932, 1280×800. Long Question/explanation, multiple attempts, mobile/desktop filter click, reachable bottom actions, no page overflow, no JavaScript errors. Screenshots visually checked. Not physical Android or production Owner QA. |
| Commit, push, Railway, production smoke | DONE for feature commit | `11a74fb` pushed; exact Railway status `success` at 2026-10-10 14:01:40 UTC; production public/Guest smoke passed. |
| Physical Android | DONE — USER CONFIRMED | User reported normal operation ("정상 동작 확인했어"); no independent per-control device observations are claimed. |

## Known boundaries

- Production Owner QA: `PRODUCTION_OWNER_NOT_VERIFIED` unless separately authorized. P0 0; P1 0. Existing P2 backlog: `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, and Goal 5 items.
- Expected DB schema change: NO. Protected JSON files must stay unchanged. No Goal 9 release tag and no Goal 9D/9E work.

## Deployment and production smoke

- Feature commit `11a74fbb07afca2c34b555915cae7bde79a3889e` reached exact-SHA Railway GitHub status `security-practical-cbt - web: success` at 2026-10-10 14:01:40 UTC. Local `master` and `origin/master` matched with a clean working tree after the feature push.
- HTTP smoke at 2026-10-10 14:02 UTC: `/`, `/healthz`, `/concepts`, `/search`, `/bookmarks`, `/practice`, `/descriptive-training`, `/mock-exam`, and `/exam` returned 200. `/healthz` reported `database=healthy`, `environment=production`, `status=ok`.
- Guest `/wrong-notes` and `/dashboard` returned 302 to `/admin-login` with the expected next path. Authenticated production Owner Wrong Notes and Dashboard remain `PRODUCTION_OWNER_NOT_VERIFIED`; local Owner fixtures cover functional QA without bypassing production login.
- Physical Android: PASS — USER CONFIRMED. Final functional verdict: `GOAL_9C_COMPLETE`; Goal 9D READY but NOT STARTED. Separate production Owner QA remains `PRODUCTION_OWNER_NOT_VERIFIED`.

## Final closure — user confirmation and retained evidence

| Area | Final status | Evidence boundary |
| --- | --- | --- |
| Wrong Notes list simplification and per-Question summary | PASS | One concise card per unresolved Question; existing short preview, type, category, Concept, latest outcome, supported mistake count/rate, and optional date. |
| Existing aggregation, wrong/partial rules, unselected practical exclusion, filters, sorting | PRESERVED | Prior focused and full regression evidence; no implementation changes in this closure. |
| Owner-only detail, submitted answers, canonical answers/rubrics, explanations, attempt timeline, related learning information | PASS / PRESERVED | Existing detail route and prior rendered-output tests; timeline remains accessible. |
| AI Helper, browser-local Bookmark separation, temporary mock Review Flag separation | PRESERVED / PASS | Prior focused and regression evidence; no storage or behavior changes. |
| Owner authorization and private source safety | PASS — LOCAL VERIFIED | Prior local Owner/Guest tests and raw-source omission test. Production authenticated Owner QA remains `PRODUCTION_OWNER_NOT_VERIFIED`. |
| Goal 9A navigation, Goal 9B Dashboard, Goal 7/8 behavior, anti-cheat | PASS | Previously executed full regression; no application or test files changed for closure. |
| Mobile and desktop browser QA | PASS | Previously executed local Chrome checks at 360×740, 390×844, 430×932, and 1280×800; details retained in the ledger above. |
| Targeted tests | 21 passed — RETAINED | Previously executed Goal 9C and Wrong Notes/history tests, not rerun for this report-only closure. |
| Full regression | 332 ran / 331 passed / 1 skipped / 0 failures / 0 errors — RETAINED | Previously executed after the final application edit; not rerun for this closure. |
| Protected core data | 5/5 SHA-256 MATCH | Read-only hash recheck at closure against the established Goal 8 values; 20 Concepts / 67 Topics / 180 Questions / 39 Aliases retained. |
| DB schema change | NO | No models, migrations, application code, or tests changed in this closure. |
| Physical Android | PASS — USER CONFIRMED | Overall user-reported normal operation; no independent automated Android or individual-control claims. |
| P0 / P1 | 0 / 0 | Existing P2 backlog remains `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, and Goal 5 operational/security items. |

- Closure commit Railway deployment: PENDING exact-commit verification after push. The earlier feature/checkpoint deployment success above is historical evidence and does not verify this closure commit.
- Release policy: keep `v0.8-learning-final` unchanged; create no Goal 9 tag. Goal 9D (Result / History Shared View Model) is READY but NOT STARTED; Goal 9E is NOT STARTED.
