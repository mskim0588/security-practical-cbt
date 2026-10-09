# Goal 8D — Persistent Question Bookmark / 다시 볼 문제

## Checkpoint

- Status: `GOAL_8D_COMPLETE`; functional PASS; physical Android PASS — USER CONFIRMED.
- Last Safe Step: feature commit `d682531` and deployment checkpoint commit `85b775a` were pushed; Railway reached terminal `SUCCESS`, production health and real-browser bookmark smoke passed, the retained full regression passed, protected core hashes matched, and the user confirmed normal operation on a physical Android device.
- Next Step: separate Goal 8 Integration QA & Release Closure. Do not create a Goal 8 release tag or start Goal 9 in this closure.

## Final Closure — COMPLETE

- Final Verdict: `GOAL_8D_COMPLETE`. Goal 8 Integration Readiness: `GOAL_8_INTEGRATION_READY`. Goal 9: NOT STARTED.
- Persistence: browser `localStorage`; bookmark target: canonical `question_id`; guest and owner use separate browser-local keys. Cross-device synchronization: NOT SUPPORTED. Database schema change: NO.
- Dedicated route: `/bookmarks`. Manual add/remove: PASS. Reload persistence: PASS in prior browser QA. A separate browser-restart test was not recorded; no independent restart result is claimed.
- Wrong Notes separation: PASS. Goal 7C Review Flag separation: PASS. Analytics/VI/adaptive preservation: PASS. Anti-cheat: PASS. Mobile browser QA: PASS.
- Retained regression, not rerun for this documentation-only closure: 318 ran / 317 passed / 1 skipped / 0 failures / 0 errors. Core data: 5 / 5 SHA-256 MATCH.
- P0: 0. P1: 0. Remaining P2: `/favicon.ico` 404, 9 `REVIEW_REQUIRED` law-freshness records, and the existing Goal 5 operational/security backlog.

## A. Baseline — DONE

- Goal 7, Goal 8A, Goal 8B, and Goal 8C are complete; Goal 8D entry state is `GOAL_8D_READY`.
- 20 Concepts, 67 Topics, 180 Questions, 39 aliases; prior regression 312 ran / 311 passed / 1 skipped / 0 failures / 0 errors.
- Branch `master`, clean at entry; HEAD and `origin/master` both `b023e97e6d8d78fa223c15e76ab01e394910d42e`.

## B. Persistence Architecture — DONE

- Existing SQLAlchemy persistence stores `ExamAttempt` and `AnswerRecord` only. Neither is an appropriate manual saved-item store.
- Goal 8D uses `localStorage` with separate `goal8d.question_bookmarks.v1.guest` and `.owner` keys. Each value is a JSON array of canonical Question IDs only. Bookmarks are stored on this browser/device; no account, browser, or device synchronization.
- The current catalog is served from canonical Questions and Topic mappings; saved IDs are validated and deduplicated against it on load. Invalid or stale IDs are cleaned. Canonical bank order controls list sorting; no timestamps are stored.

## C. DB Schema Decision — DONE

- No DB schema change. No `create_all`, startup migration, or production `ALTER TABLE` change for Goal 8D.

## D. Bookmark Semantics — DONE

- Manual add/remove only, independent of correctness, partial credit, Wrong Notes, attempts, and scores. No implicit conversion from review flags.
- Target is `question_id` only. No Concept, Topic, alias, query, or attempt bookmarks.
- Controls show `☆ 다시 볼 문제에 추가` or `★ 저장됨 · 제거` with an accessible state label; color is not the sole state signal.

## E. Wrong Notes Separation — DONE

- Wrong Notes continue to derive from graded owner history. Bookmark actions only change the browser's scoped ID list. A Question can exist in both; removing either record does not remove the other.

## F. Review Flag Separation — DONE

- Goal 7C Review Flag remains attempt-local mock state. Bookmark JS reads/writes no review-flag data; finishing a mock does not create bookmarks.

## G. Bookmarkable Surfaces — DONE

- Shared control partial: Search Question results, Topic and Parent Concept related-question lists, post-submit result detail, history detail, Wrong Note detail, graded Practice feedback, and graded Descriptive Training feedback.
- No control on active Exam, active Mock Exam, pre-submit Descriptive Training, or pre-answer Practice.

## H. Dedicated Bookmark Page — DONE

- `GET /bookmarks` renders `다시 볼 문제`; `GET /bookmarks/catalog` supplies answer-free canonical display metadata for 180 Questions. The list renders saved Questions only.
- Each card shows ID, type, category, Parent Concept, Topic, concise preview, open/study link to Topic Question anchor, and remove action. No model answer in cards.
- Empty and filtered-empty states are explicit. Filters: All, Short, Descriptive, Practical. Canonical question order is deterministic.

## I. Guest / Owner Behavior — DONE

- Guest and owner each have same-browser/device persistence under separate keys. Neither has account synchronization. No owner attempt, Wrong Note, or history data enters the guest bookmark catalog.

## J. Security — DONE

- Browser storage contains Question IDs only; no answers, scores, source metadata, secrets, or personal data. Catalog is derived from trusted application records and contains no model answers/rubrics.
- Invalid IDs are ignored/cleaned. The browser renders canonical catalog text using `textContent`, never stored HTML. The catalog is GET-only with `Cache-Control: no-store`; bookmark mutation has no server POST or database write.

## K. Anti-cheat — DONE

- No persistent bookmark control, script, or navigation entry in active Exam/Mock or pre-submit Descriptive Training. Practice exposes its control only after feedback.

## L. Goal 8A Preservation — DONE

- 20 Concepts, 67 Topics, 180 Questions; 180 mappings, 0 unmapped, 0 zero-question Topics, 0 invalid references, 0 parent mismatches. Taxonomy files and Question-to-Concept/Topic mappings unchanged.

## M. Goal 8B Preservation — DONE

- 39 aliases unchanged; audit finds 0 exact/normalized duplicates, cross-target collisions, ambiguous aliases, or invalid targets. Bookmarks use Question IDs only.

## N. Goal 8C Preservation — DONE

- `GET /search`, matching, normalization, ranking, filters, keywords, commands, aliases, and deduplication remain unchanged. The Question card only adds a manual bookmark control. Existing Goal 8C tests pass in the full regression.

## O. Goal 7 Regression — DONE

- Goal 7A/7B/7C/7D suites pass in the full regression. No VI, adaptive, analytics, weakness, grading, dashboard, or Wrong Note service changes.
- Law freshness remains 4 `VERIFIED` / 9 `REVIEW_REQUIRED`.

## P. Mobile QA — DONE (browser and user-confirmed physical Android)

- Chrome checks at 360×740, 390×844, 430×932, and 1280×800. Cards, previews, filters, add/remove actions, and empty state fit; no horizontal overflow. At mobile widths, open/remove controls remain visible above the bottom navigation.
- Real-browser add, navigation, reload persistence, type filter, Question destination, remove, and removed-state reload passed. Keyboard Enter activated filter and removal. Physical Android: PASS — USER CONFIRMED. The user confirmed normal operation without reporting separate detailed device observations.

## Q. Tests — DONE

- Goal 8D targeted Python: 6 ran / 6 passed / 0 skipped / 0 failures / 0 errors. JavaScript storage tests: 3 passed, including stale/duplicate cleanup and guest/owner key separation.
- Full `py -3 -m unittest discover tests -v`: 318 ran / 317 passed / 1 skipped / 0 failures / 0 errors. The skip is the existing optional private-source comparison.

## R. Core Hashes — DONE

- `questions.json` `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`
- `concepts.json` `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`
- `sources.json` `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`
- `concept_contents.json` `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171`
- `explanations.json` `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696`
- Result: 5 / 5 SHA-256 MATCH. Protected files unchanged.

## S. Production Smoke — DONE

- Feature commit `d682531deab9ab867d6a28f35f1c4760e6d3fd1f` pushed to `master` normally; local HEAD matched `origin/master`. Railway deployment `6938332853` reached terminal `success`.
- `GET /` and `/healthz` returned 200; health JSON reported `status=ok`, `database=healthy`, `environment=production`.
- `GET /bookmarks` and `/bookmarks/catalog` returned 200; catalog contains 180 Questions. `/search?q=lastb`, `/search?q=SQLi`, and `/search?q=iptables` returned 200. `/practice`, `/concepts`, `/exam`, `/mock-exam`, and `/descriptive-training` returned 200.
- In a real Chrome guest browser on production: empty state, add `Q-SHORT-062` from Search, saved card, reload persistence, Topic Question navigation, remove, and removed-state reload all passed. Stored state remained browser-local.
- Production `/exam`, mock setup, and descriptive setup contained 0 Question bookmark controls. The active Mock session/Review Flag boundary was verified locally by targeted and full regression tests; no synthetic attempt was created in production.
- Guest access to owner `/dashboard`, `/history`, `/wrong-notes`, and `/law-freshness` retained the expected login redirect. Bookmark actions do not touch Wrong Notes or Review Flag server data.
- P0: 0. P1: 0. Remaining P2: `/favicon.ico` 404, 9 `REVIEW_REQUIRED` law-freshness records, existing Goal 5 operational/security backlog.

## T. Goal 8 Integration Readiness — DONE

- Goal 8A, Goal 8B, Goal 8C, and Goal 8D are complete. Goal 8D functional status: PASS; physical Android: PASS — USER CONFIRMED.
- Goal 8 Integration status: `GOAL_8_INTEGRATION_READY`.
- Goal 8 Integration QA and Release Closure are a separate next task; only that task may create `v0.8-learning-final` after its release gates pass. Goal 9 is NOT STARTED. Existing `v0.7-learning-final` is unchanged.
