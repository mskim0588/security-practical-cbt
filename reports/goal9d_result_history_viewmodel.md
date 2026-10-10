# Goal 9D — Result / History Shared View Model

## Checkpoint

- Status: LOCAL VERIFIED; deployment pending. Baseline HEAD: `9f1b512f3377f5722daef1ef96ea83053a5c9ac2`.
- Entry gate: clean `master` = `origin/master`; Goal 9A/B/C COMPLETE; Goal 9D READY; `v0.8-learning-final` still points to `2483cb01928282d6dd3f180b527771191773e59b`.
- Last Safe Step: small shared mapper, focused tests, full regression, protected-data checks, and local Chrome QA passed. Fixed fixture projections match the baseline commit exactly.
- Next Step: review and commit the local changes, push `master`, verify exact-commit Railway `SUCCESS`, then run production smoke. Physical Android remains pending.

## Architecture and verified duplication

| Area | State | Baseline behavior |
| --- | --- | --- |
| A Result architecture | DONE | `/submit` grades canonically, saves via `HistoryService`, records session attempt ID, then redirects to `/result/<id>`; failure fallback renders the grading result directly. Result GET checks session/Owner access, obtains enriched `get_attempt_detail`, and rebuilds score summary and per-question feedback. |
| B History architecture | DONE | `/history` and `/history/<id>` are `@admin_required`; list queries Owner non-learning attempts newest first, 15 per page. Detail checks Owner and learning-mode exclusion before loading enriched answers. Delete is CSRF protected. |
| C Proven duplication | DONE | Stored attempt ID/mode, score components, pass flag, created timestamp, and result-detail destination are read and formatted repeatedly in Result and History list/detail. History desktop/mobile also duplicate mode/date/score markup. |
| D Shared contract | DONE | `map_attempt_summary` accepts an authorized `ExamAttempt` or its existing detail dict and copies ID, mode/labels, finalized/scored status, stored score/breakdown, pass flag, selected practical ID, existing local timestamp display, and generated Result/Owner History paths. It never loads answers or recomputes scores. |
| E Result-specific data | DONE | Score percentages, selected practical detail, question feedback, user/model answers, explanation, Concept/Topic, bookmark, AI Helper, and fallback rendering stay in Result. |
| F History-specific data | DONE | Owner pagination/order, incorrect/partial counts, delete action, complete answer timeline, and empty state stay in History. |
| G Existing calculations | DONE | `Grader` owns scoring/pass; `HistoryService` persists canonical values. Result currently computes section percentages only for display. History uses stored values and counts answer statuses. |
| H Ownership/security | DONE | Guest `/result/<id>` requires signed-session submitted ID. Owner can read Owner attempts; session-bound Guest result access remains. `/history` redirects Guest to login; detail rejects Guest-owned/learning attempts. |
| I UI/date behavior | DONE | Result has score, pass/fail, section breakdown and full feedback. History has table/mobile cards, pagination, links, empty state; list uses `created_at` local naive datetime `%Y-%m-%d %H:%M`, detail uses ISO string's first 16 characters. No timezone conversion. |
| J Query/performance | DONE | Baseline list lazily loaded `answers` per attempt. `get_attempts` now uses `selectinload`, preserving the Owner filter, descending order, pagination, and existing answer counts. Focused instrumentation observed at most three SELECTs for a populated two-attempt History list. |

## Verification ledger

| Area | State | Evidence or next step |
| --- | --- | --- |
| H Before/after behavior | DONE | A fixed synthetic fixture was rendered in detached baseline `9f1b512` and current checkout. JSON projections were exactly equal for passing/failing/partial scores, finalized mock, Guest Result, Owner History/detail, dates, links, selected/unselected practical, answers, Guest redirect, and direct IDOR denials. Baseline and after temporary snapshots remained outside the repository. |
| I Guest/Owner authorization | DONE locally | Guest session Result 200; unaffiliated Result 403; signed-session ID cannot grant Guest access to an Owner attempt; Guest History redirects to login; Owner History excludes Guest attempts. |
| J Result ownership | DONE locally | Direct unauthorized Result returns 403; invalid attempt 404; `X-Robots-Tag` retained; Owner and Guest session access checks remain route-side. |
| K Scoring preservation | DONE | Mapper copies canonical stored values. Full regression covers Grader, partial credit, 100-point maximum, 60-point pass threshold, and selected practical rules. No Grader or persistence edits. |
| L Mock compatibility | DONE locally | Finalized `mock_exam` appears in History and renders Result/detail with stored score; active `mock_exam_active` remains excluded and Result GET returns 404. Existing mock-mode tests pass. |
| M Dashboard preservation | DONE | No Dashboard code changed; five Goal 9B focused tests and full regression passed, including finalized mock recent score. |
| N Wrong Notes preservation | DONE | No Wrong Notes code changed; five Goal 9C focused tests and full regression passed. |
| O Anti-cheat and private sources | DONE | Mapper has no answer/rubric/source fields and is called only after Result/History authorization. Active exam/mock/training code was not edited; full regression and raw-source focused assertion passed. |
| P Query/performance | DONE | History list relation eager load; focused populated list assertion at most three SELECTs. No mapper query. |
| Q Responsive QA | DONE locally | Headless local Chrome with isolated SQLite and synthetic signed Owner/Guest sessions: 24 actual route/viewport checks covering empty/populated History, Guest/Owner Result, History detail, and mock Result at 360×740, 390×844, 430×932, 1280×800. Screenshots visually inspected. Document width matched viewport at each size; no JavaScript exceptions. Mobile bottom bar 60px, body clearance 76px; key action links were reachable above the bar after scrolling. |
| R Targeted tests | DONE | `python -m unittest tests.test_goal9d_result_history_viewmodel tests.test_history_persistence tests.test_goal9c_wrong_notes tests.test_goal9b_dashboard tests.test_goal7c_realistic_mock_exam -v`: 38 ran / 38 passed / 0 skipped / 0 failures / 0 errors. Goal 9D contributes six new tests. |
| S Full regression | DONE | `python -m unittest discover tests -v`: 338 ran / 337 passed / 1 skipped (`PRIVATE_SOURCE_DIR` unavailable) / 0 failures / 0 errors. Covers Goal 9A, Goal 7A–D, Goal 8A–D and remaining tests. |
| T Core data integrity | DONE | Fresh 5/5 SHA-256 MATCH against Goal 8 release: Questions `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`; Concepts `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`; Sources `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`; Contents `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171`; Explanations `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696`. Inventory 20 Concepts / 67 Topics / 180 Questions / 39 Aliases / 180 mappings. |
| U Git/deployment | TODO | Local diff reviewed; commit, push, exact final SHA Railway and production smoke pending. |
| V Backlog | DONE | P0 0, P1 0; retain `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, Goal 5 backlog. |
| W Physical Android readiness | TODO | Device testing is pending; set `GOAL_9D_READY_FOR_PHYSICAL_DEVICE_TEST` only after deployment gates pass. |

## Release boundaries

- Production Owner QA: `PRODUCTION_OWNER_NOT_VERIFIED` until separately evidenced.
- DB schema change: NO. Goal 9 release tag: NO. Goal 9E: NOT STARTED.
- P0: 0. P1: 0. Existing P2: `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, Goal 5 backlog.
