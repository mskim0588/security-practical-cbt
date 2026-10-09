# Goal 9A — Lean Navigation Simplification

## Checkpoint

- Status: PARTIAL — implementation commit deployed and production checked; this checkpoint update still needs commit/push and exact-commit deployment verification.
- Last Safe Step: implementation commit `2f74fd8cd0c9833dd89cb6b050631f597f740211` pushed with clean parity; Railway reported `SUCCESS` for that exact commit; production Guest smoke and `/healthz` passed at 2026-10-09 14:46 UTC.
- Next Step: commit and push this report update, wait for its exact Railway deployment result, then report Goal 9A ready for physical Android testing if healthy.

## Baseline — DONE

- Goal 7 and Goal 8 are COMPLETE. Entry tree clean; no baseline changes or protected-data edits.
- Previous regression: 318 ran / 317 passed / 1 skipped / 0 failures / 0 errors. This is retained baseline evidence, not a fresh Goal 9A run.
- Fresh loader count: 20 Concepts / 67 Topics / 180 Questions / 39 Aliases. Bookmark persistence remains browser-local with separate Guest/Owner keys. No database schema change; `v0.8-learning-final` remains unchanged.

## Existing navigation inventory — DONE

- Desktop: Home, Dashboard, Concepts, Exam, History, Wrong Notes, conditional Bookmarks; Owner law queue and logout live in an overridable header-actions block.
- Mobile: six bottom items, plus a seventh conditional Bookmark item. Dashboard, History, and Wrong Notes links render for Guests even though direct routes protect their data.
- No existing overflow menu. Home already links to ordinary exams, Practice, Descriptive Training, and Mock Exam. Search is reachable through existing pages but absent from the global navigation.

## Old-to-new mapping — DONE

| Existing destination | Goal 9A placement |
| --- | --- |
| Home `/` | Guest/Owner primary |
| Exam `/exam` | Guest/Owner primary `문제풀기` |
| Concepts `/concepts` | Guest/Owner primary `개념정리` |
| Dashboard `/dashboard` | Owner `내 학습` |
| History `/history` | Owner `내 학습` |
| Wrong Notes `/wrong-notes` | Owner `내 학습` |
| Bookmarks `/bookmarks` | Owner `내 학습`; Guest `더보기` |
| Search `/search` | Guest/Owner `더보기` |
| Practice, Descriptive Training, Mock Exam | Existing Home links and `더보기` learning-mode links |
| Law freshness, login/logout | Relevant Guest/Owner `더보기` utility links |

## Implementation — DONE

- Shared primary links: Home, Problem Solving, Concepts. Owner `내 학습` groups Dashboard, History, Wrong Notes, and Bookmarks. Guest Bookmarks and both users' Search remain in `더보기`.
- `더보기` also exposes Practice, Descriptive Training, and Mock Exam; Owner law queue and CSRF-protected logout or Guest login appear only in the applicable state.
- Mobile uses four Guest or five Owner bottom destinations; active learning/exam states and assessment restrictions remain conditional. Native `details` menus support click/touch/keyboard, with Escape, outside-click closing, and `aria-expanded` synchronization.

## Verification — DONE locally

- Targeted Goal 9A and current navigation, learning-label, and mobile layout tests: 31 ran / 31 passed / 0 skipped / 0 failures / 0 errors.
- Guest/Owner destinations, direct URL protection, logout CSRF, active state, and active exam utility exclusion passed targeted tests.
- Full `python -m unittest discover tests -v`: 322 ran / 321 passed / 1 skipped / 0 failures / 0 errors. The first run exposed one stale `개념학습` navigation-label assertion; after updating the test to `개념정리`, the full rerun passed. Goal 7A–7D and Goal 8A–8D tests remain green.
- Isolated local Chrome QA with a temporary SQLite database and synthetic Owner login: Guest Home, Exam, Concepts, Search, Bookmarks, Practice, Descriptive Training, and Mock Exam; Owner Home, Exam, Concepts, Search, Bookmarks, Dashboard, History, and Wrong Notes checked at 360×740, 390×844, 430×932, and 1280×800. No page-level horizontal overflow on the checked routes.
- Guest mobile `더보기` opened by click; Search/Bookmarks links were present and reachable. Owner desktop `내 학습` opened with its four correct destinations; Owner mobile menu opened above the bottom bar. Escape returned focus to the summary, outside click closed the menu, `aria-expanded` synchronized, and Chrome reported no JavaScript errors during completed checks. An additional keyboard Enter check timed out in browser automation and is not claimed as verified.
- Mobile bottom bar was 60px high with 76px body bottom padding in the 360×740 inspection; menu panel ended above the bar. Active Exam had no mobile bar, Bookmark link, Search link, or new navigation script. Practice and pre-submit Descriptive Training retained the restricted three-item mobile bar.
- Protected JSON hashes: `questions.json` `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`; `concepts.json` `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`; `sources.json` `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`; `concept_contents.json` `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171`; `explanations.json` `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696`. All 5/5 match the protected baseline.

## Deployment — PARTIAL (implementation commit verified)

- Implementation commit `2f74fd8cd0c9833dd89cb6b050631f597f740211` pushed to `master`; local HEAD = `origin/master`, working tree clean before this checkpoint edit. Existing `v0.8-learning-final` still targets `2483cb01928282d6dd3f180b527771191773e59b`. No Goal 9 tag.
- Railway GitHub commit status for `2f74fd8`: `security-practical-cbt - web` = `success`, updated 2026-10-09 14:44:02 UTC. This verifies the new implementation deployment, not an older build.
- Production checks at 2026-10-09 14:46 UTC: `/` 200 with new Guest primary navigation and Search/Bookmark utility links; `/healthz` 200 with `database=healthy`, `environment=production`; `/static/js/navigation.js` 200. Guest browser clicked `더보기` → `/search` and `더보기` → `/bookmarks`; Bookmark empty state loaded without JavaScript errors.
- Guest HTTP smoke: `/exam`, `/practice`, `/descriptive-training`, `/mock-exam`, `/concepts`, a Concept detail, a Topic detail, `/search?q=SQLi`, and `/bookmarks` all returned 200. `/dashboard`, `/history`, `/wrong-notes`, and `/law-freshness` redirected Guest to `/admin-login`. Active `/exam` lacked new Search/Bookmark utility controls.
- Production Owner navigation was not exercised with real credentials. Isolated local Owner browser and direct-route tests passed; no production Owner data was altered. Physical Android remains PENDING. Goal 9A must stop at `GOAL_9A_READY_FOR_PHYSICAL_DEVICE_TEST` after the checkpoint commit deploys successfully.

## Outstanding issues — DONE (documented)

- P0: 0. P1: 0. Existing non-blocking backlog: `/favicon.ico` 404, nine `REVIEW_REQUIRED` legal records, Goal 5 operational/security backlog. Goal 9B is NOT STARTED.
