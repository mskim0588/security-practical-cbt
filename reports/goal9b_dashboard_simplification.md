# Goal 9B — Dashboard Simplification

## Checkpoint

- Status: PARTIAL — finalized `mock_exam` was added to the recent-score mode allowlist and verified locally. Deployment of this fix is pending. Physical Android PENDING; Goal 9C NOT STARTED.
- Baseline HEAD: `faf8ff2981e49e6cf88fec585e441cef8ee72fe1`, clean `master` = `origin/master`; Goal 9A `GOAL_9A_COMPLETE`, Goal 9B `GOAL_9B_READY`; `v0.8-learning-final` unchanged.
- Recovery entry: HEAD `ad633ecd9ed88794fdfae637fb6bb700b6b1a29f` = `origin/master`; unstaged Goal 9B changes in `app/routes/dashboard_routes.py`, `tests/test_goal9b_dashboard.py`, and this report; no staged or untracked files and no unrelated changes. Existing feature commit `13a891c` and checkpoint commit `ad633ec` were preserved.
- Last Safe Step: focused tests 5/5, full regression 327 ran / 326 passed / 1 skipped / 0 failures / 0 errors, and protected hashes 5/5 match after the local fix. Earlier responsive Chrome QA remains applicable because template, CSS, and JavaScript did not change. Earlier public/Guest production smoke and Railway `success` apply only to the already pushed commits.
- Next Step: commit and push the fix, verify Railway `SUCCESS` for the exact new commit, recheck production, then request the user's physical Android verification. Do not finalize Goal 9B or begin Goal 9C until separate closure.

## Recovery classification

| Areas | State | Evidence or next action |
| --- | --- | --- |
| A Baseline verification; B Dashboard inventory; C Old-to-new mapping | DONE | Git recovery, earlier Goal 9A/8 reports, source and layout inspected. |
| D Next action; E deterministic rules; F Weak TOP 3; G canonical VI | DONE | Existing recommendation and analytics retained; attempted positive-VI Concepts and deterministic ID tie-break. |
| H Recent valid score; I empty history; J low data; K detailed analytics; L presentation view-model | DONE | Finalized mock fix and focused tests pass; detailed sections remain below the summary. |
| M Owner authorization; N Guest isolation; O Goal 9A navigation | DONE | Existing protected route, focused authorization test, and unchanged navigation files. |
| P Goal 7; Q Goal 8; U anti-cheat; V targeted tests; W full regression | DONE | Fresh 5/5 focused and 327-test full regression pass. |
| R mobile; S desktop; T accessibility; Y browser QA | DONE | Prior isolated Chrome viewport checks retained; layout and client code did not change in this recovery. Physical Android remains pending. |
| X core data integrity | DONE | Fresh 5/5 SHA-256 match; inventory 20/67/180/39. |
| Z checkpoint report | PARTIAL | Updated for recovery; final deployment result pending. |
| AA feature commit; AB push; AC Railway deployment; AD production smoke | PARTIAL | Earlier feature/checkpoint commits deployed; local mock fix awaits these gates. |
| AE physical Android readiness | TODO | Report ready status only after deployment and smoke; user device check remains pending. |

- Last Safe Completed Step: fresh local test and core-data gates for the recovered fix.
- First Incomplete Step: commit and push the recovered fix.

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
- Recent score uses the latest Owner record from the existing recent trend for supported scored exam modes (`standard`, `random`, `adaptive`, `wrong_review`, finalized `mock_exam`), with a valid 0–100 score, completion date, pass/fail flag, and History detail link. Practice, descriptive training, and active mock attempts remain excluded by the canonical trend service. An empty history shows no completed zero score. The old latest-score, average, highest, pass-rate, score-delta, category, Top 5, recent trend/table, and quick actions remain below the primary summary.
- The actual VI formula remains `(100 - ScoreRate) × ((incorrect + 0.5 × partial) / attempts) × log2(attempts + 1)` in `AnalyticsService`; adaptive selection is unchanged. The existing 60/100 pass threshold and selected-practical grading remain unchanged.

## Authorization and preservation — DONE

- `/dashboard` remains protected by `@admin_required`; local synthetic Guest received 302 to `/admin-login`, while authenticated synthetic Owner received 200. No new endpoint, authentication path, database schema, or data model was added.
- Goal 9A navigation was not edited and Owner `내 학습` still marked Dashboard active in Chrome. Goal 7A–7D and Goal 8A–8D implementation files were not changed. Full regression covers existing scoring, analytics, VI, adaptive, history, Wrong Notes, search, bookmarks, and anti-cheat behavior. No active exam, mock exam, or descriptive training template was edited.

## Tests and browser QA — DONE

- Fresh focused `python -m unittest tests.test_goal9b_dashboard -v`: 5 ran, 5 passed, 0 skipped/failures/errors. The added case checks finalized mock-exam score and History link. The existing cases cover Owner/Guest access, rendered empty/low-data states, recommendation target, canonical VI and tie ordering, exclusion of unattempted/unselected practical data, latest valid Owner scored exam, training-mode isolation, detail link, and read-only attempt/answer counts.
- Fresh `python -m unittest discover tests -v`: 327 ran, 326 passed, 1 skipped (`PRIVATE_SOURCE_DIR` absent), 0 failures, 0 errors. This includes existing Goal 7/8/9A tests.
- Isolated local Chrome at 2026-10-09 15:13 UTC used a temporary SQLite database and a synthetic Owner login. Empty and populated Owner Dashboard checked at 360×740, 390×844, 430×932, 1280×800. Document widths were 345, 375, 415, and 1265 CSS pixels respectively, below viewport widths. New cards stacked on mobile and sat side by side on desktop; TOP 3 names, VI/sample metadata, recent score and result link, existing detailed sections, and long scrolling were readable. The 44px recent-result action and bottom-of-page exam actions remained reachable above the fixed 60px mobile navigation; no JavaScript error was reported. Existing detailed trend table retained its internal horizontal scrolling. Physical Android: PENDING.

## Data and deployment — PARTIAL for recovered fix

- Protected SHA-256 files: `questions.json` `661098CE80E957B033FBB1A2B540701815791169ECD57C0F367720B94F3D5DC9`; `concepts.json` `D33CDD63824C01C6537DD6F2CB6829B58BF121883A05EB406803BBE58BAD5943`; `sources.json` `9AE37CE41F1B3BCCF0047474FCA8E8332AD18F1EAD298EE2F17FE85574049A21`; `concept_contents.json` `025C54CA679AC3E15AC8F8D98A9BF7AE3F120577E13EE44A5911B6BEAC335171`; `explanations.json` `E62C2EF4D5EF92C3EC8279AE9F1A8EBE2AD23414BED6560C9FBEF4751D322696`. All 5 MATCH the Goal 8 release report. Fresh JSON counts: Concepts 20; Topics 67; Questions 180; Aliases 39; Question-to-Topic mappings 180.
- Feature commit `13a891c8d6acc2299a0dce43a3e3c295eeff1d86` pushed to `origin/master`. Exact SHA Railway GitHub commit status `security-practical-cbt - web` = `success`, updated 2026-10-09 15:15:14 UTC. This confirms the feature build, not an older deployment.
- Production HTTP checks at 2026-10-09 15:15 UTC: `/`, `/healthz`, `/concepts`, `/search`, `/bookmarks`, `/practice`, `/descriptive-training`, `/mock-exam`, and `/exam` returned 200. `/healthz`: `status=ok`, `database=healthy`, `environment=production`. Root HTML retained `/`, `/exam`, `/concepts`, `/search`, and `/bookmarks` links. Guest `/dashboard` returned 302 to `/admin-login?next=/dashboard`.
- Production authenticated Owner Dashboard: `NOT_VERIFIED`; no authorized production Owner session was used. Physical Android: PENDING.

## Remaining release gates — TODO

- Recovered fix commit/push, exact-commit Railway `SUCCESS`, and fresh public/Guest production smoke; user physical Android verification. Authenticated production Owner QA remains `PRODUCTION_OWNER_NOT_VERIFIED` unless authorized access is actually available.

## Existing non-blocking backlog — DONE (documented)

- `/favicon.ico` 404, nine `REVIEW_REQUIRED` law records, existing Goal 5 operational/security items. Goal 9C/9D/9E: NOT STARTED.
