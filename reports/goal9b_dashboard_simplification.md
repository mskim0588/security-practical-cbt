# Goal 9B — Dashboard Simplification

## Checkpoint

- Status: PARTIAL — implementation, local tests, protected hashes, and responsive browser QA pass; commit/deployment pending.
- Baseline HEAD: `faf8ff2981e49e6cf88fec585e441cef8ee72fe1`, clean `master` = `origin/master`; Goal 9A `GOAL_9A_COMPLETE`, Goal 9B `GOAL_9B_READY`; `v0.8-learning-final` unchanged.
- Last Safe Step: focused tests 4/4 and full regression 326 ran / 325 passed / 1 skipped / 0 failures / 0 errors; isolated Owner Chrome QA completed at four viewports; protected hashes 5/5 match.
- Next Step: review and commit Goal 9B changes, push master, verify exact-commit Railway SUCCESS and production public/Guest smoke. Physical Android remains pending.

## Existing Dashboard inventory — DONE

| Existing element or metric | Data source | Goal 9B placement |
| --- | --- | --- |
| Page heading; Wrong Notes and History links | Dashboard template, `wrong_count` | Header, retained |
| Next learning recommendation and two actions | Existing deterministic `get_learning_recommendation` | First summary section with one visually primary action |
| Total exam attempts; latest score, result, and score delta | `AnalyticsService.get_summary_stats`, recent trend | Detailed KPI section below primary summary |
| Average and highest score | `get_summary_stats` | Detailed KPI section; empty state shown as unavailable instead of a completed zero score |
| Pass rate, passed/failed counts | `get_summary_stats` | Detailed KPI section |
| Unresolved Wrong Note count and link | `WrongAnswerService` | Header and detailed KPI section |
| Five category weighted score, grade, answer counts, progress | `get_category_analytics` | Detailed analysis section, unchanged |
| Existing Top 5 clinic, VI, score rate, answer counts, links, adaptive CTA | `get_top_vulnerable_concepts(limit=5)` | Detailed analysis section, unchanged |
| Recent five-attempt trend, score delta, table, mode, dates, breakdown, detail links | `get_recent_performance_trend(limit=5)` | Detailed history section, unchanged |
| Standard, random, adaptive, and Wrong Review exam links | Existing routes | Detailed quick actions, unchanged |

## Primary summary — DONE

- First: `다음 추천 학습`, reusing the existing deterministic recommendation policy and valid existing route.
- Second: up to three attempted Concepts with positive VI from the existing ranked Top 5; tie break by canonical Concept ID. Zero attempts and missing weak evidence show an honest empty state.
- Third: the latest canonical Owner scored-attempt trend record, with score out of 100, date, pass/fail text, and existing History detail link. No completed record shows `아직 완료한 시험 기록이 없습니다.` and an existing exam link.
- No new analytics query, VI formula, scoring calculation, adaptive logic, data model, or database schema. Existing detailed cards and sections remain lower on the page.

## Recommendation and recent score rules — DONE

- The existing deterministic recommendation remains authoritative: no Owner exam history → standard exam; unresolved grading-derived Wrong Notes → wrong-review exam; positive ranked VI → adaptive exam and Concept detail; otherwise random exam. The fallback message no longer implies a passing performance without evidence. The first action is visually primary; the existing secondary action remains.
- Weak TOP 3 uses the already-computed Top 5 service result, keeps only attempted Concepts with positive VI, and sorts equal VI by canonical Concept ID. The existing detailed Top 5 still includes its established unattempted fallback, with its explicit `미응시` label; no unattempted Concept appears in the new weak summary.
- Recent score uses the latest Owner record from the existing recent trend for supported scored exam modes (`standard`, `random`, `adaptive`, `wrong_review`), with a valid 0–100 score, completion date, pass/fail flag, and History detail link. Practice, descriptive training, and active mock attempts remain excluded by the canonical trend service. An empty history shows no completed zero score. The old latest-score, average, highest, pass-rate, score-delta, category, Top 5, recent trend/table, and quick actions remain below the primary summary.
- The actual VI formula remains `(100 - ScoreRate) × ((incorrect + 0.5 × partial) / attempts) × log2(attempts + 1)` in `AnalyticsService`; adaptive selection is unchanged. The existing 60/100 pass threshold and selected-practical grading remain unchanged.

## Authorization and preservation — DONE

- `/dashboard` remains protected by `@admin_required`; local synthetic Guest received 302 to `/admin-login`, while authenticated synthetic Owner received 200. No new endpoint, authentication path, database schema, or data model was added.
- Goal 9A navigation was not edited and Owner `내 학습` still marked Dashboard active in Chrome. Goal 7A–7D and Goal 8A–8D implementation files were not changed. Full regression covers existing scoring, analytics, VI, adaptive, history, Wrong Notes, search, bookmarks, and anti-cheat behavior. No active exam, mock exam, or descriptive training template was edited.

## Tests and browser QA — DONE

- Focused `python -m unittest tests.test_goal9b_dashboard -v`: 4 ran, 4 passed, 0 skipped/failures/errors. Cases cover Owner/Guest access, rendered empty/low-data states, recommendation target, canonical VI and tie ordering, exclusion of unattempted/unselected practical data, latest valid Owner scored exam, training-mode isolation, detail link, and read-only attempt/answer counts.
- Fresh `python -m unittest discover tests -v`: 326 ran, 325 passed, 1 skipped (`PRIVATE_SOURCE_DIR` absent), 0 failures, 0 errors. This includes existing Goal 7/8/9A tests.
- Isolated local Chrome at 2026-10-09 15:13 UTC used a temporary SQLite database and a synthetic Owner login. Empty and populated Owner Dashboard checked at 360×740, 390×844, 430×932, 1280×800. Document widths were 345, 375, 415, and 1265 CSS pixels respectively, below viewport widths. New cards stacked on mobile and sat side by side on desktop; TOP 3 names, VI/sample metadata, recent score and result link, existing detailed sections, and long scrolling were readable. The 44px recent-result action and bottom-of-page exam actions remained reachable above the fixed 60px mobile navigation; no JavaScript error was reported. Existing detailed trend table retained its internal horizontal scrolling. Physical Android: PENDING.

## Data and deployment — PARTIAL

- Protected SHA-256 files: `questions.json` `661098CE80E957B033FBB1A2B540701815791169ECD57C0F367720B94F3D5DC9`; `concepts.json` `D33CDD63824C01C6537DD6F2CB6829B58BF121883A05EB406803BBE58BAD5943`; `sources.json` `9AE37CE41F1B3BCCF0047474FCA8E8332AD18F1EAD298EE2F17FE85574049A21`; `concept_contents.json` `025C54CA679AC3E15AC8F8D98A9BF7AE3F120577E13EE44A5911B6BEAC335171`; `explanations.json` `E62C2EF4D5EF92C3EC8279AE9F1A8EBE2AD23414BED6560C9FBEF4751D322696`. All 5 MATCH the Goal 8 release report. Concepts 20; Topics 67; Questions 180; Aliases 39 (taxonomy/alias files unchanged).
- Feature commit/push: TODO. Railway exact-commit terminal status: TODO. Production public health/Guest smoke: TODO. Production authenticated Owner: NOT_VERIFIED; no authorized production Owner session used.

## Remaining release gates — TODO

- Commit/push, exact-commit Railway terminal result, production public/Guest smoke. Authenticated production Owner QA remains NOT_VERIFIED unless authorized access is actually available. Physical Android: PENDING.

## Existing non-blocking backlog — DONE (documented)

- `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, existing Goal 5 operational/security items. Goal 9C/9D/9E: NOT STARTED.
