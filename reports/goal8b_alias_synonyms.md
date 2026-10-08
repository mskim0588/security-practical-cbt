# Goal 8B Alias / Synonym Knowledge Layer

## Checkpoint

- Status: IN PROGRESS.
- Baseline HEAD: `1f9212cafd46c42aecbf81858a2786647fb72fa8` on clean `master`, equal to `origin/master`.
- Goal 8A: `GOAL_8A_COMPLETE`; Goal 8B entry: `GOAL_8B_READY`.
- Parent Concepts: 20; Topics: 67; Questions: 180.
- Last Safe Step: local implementation, data audit, targeted and full regression, and four-viewport browser QA passed.
- Next Step: final Git review, feature commit, normal push, Railway terminal status, production smoke, and deployment checkpoint.

## A. Baseline — DONE

- Clean `master`; HEAD and `origin/master`: `1f9212cafd46c42aecbf81858a2786647fb72fa8`.
- Goal 7: `GOAL_7_COMPLETE`; Goal 8A: `GOAL_8A_COMPLETE`; Goal 8B entry: `GOAL_8B_READY`.
- Baseline: 20 Parent Concepts, 67 Topics, 180 Questions; 180 mapped, 0 unmapped, 0 zero-question Topics, 0 invalid references, 0 parent mismatches.
- Prior regression: 298 run, 297 passed, 1 skipped, 0 failures, 0 errors.

## B. Alias Architecture — DONE

- `app/data/aliases.json` is separate additive static metadata. Canonical names and IDs remain in existing files. DB schema change: **NO**.
- Each record has `alias_id`, `target_type`, `target_id`, `alias`, `alias_type`, and `language`.
- `DataLoader.load_aliases()` loads the file. `AliasService` validates, groups, audits, and resolves canonical names or aliases to zero, one, or multiple targets.
- Invalid inventory records are rejected. The learning detail service logs an invalid inventory and omits aliases so a bad target does not crash a detail page.
- No global search, ranking, autocomplete, or fuzzy matching was added.

## C. Alias Types — DONE

| Type | Meaning |
|---|---|
| `ko_alt` | Equivalent Korean wording |
| `en_full` | English full expression for the whole target |
| `acronym` | Established abbreviation for the whole target |
| `synonym` | Other equivalent technical wording |

Languages are `ko` and `en`. Existing names remain canonical display names.

## D. Concept Coverage — DONE

- Parent Concepts total: **20**; with one or more aliases: **9**; Concept aliases: **10**.
- Covered IDs: `CON-NET-02`, `CON-APP-01`, `CON-APP-03`, `CON-CRY-01`, `CON-CRY-02`, `CON-MGT-01`, `CON-MGT-04`, `CON-SEC-01`, `CON-SEC-02`.
- Others remain canonical-only where a short term would refer to merely one part of a composite Concept.

## E. Topic Coverage — DONE

- Topics total: **67**; with one or more aliases: **23**; Topic aliases: **29**.
- SQL Injection / SQLi / SQL 삽입 공격 point only to `TOP-APP-01-02`.
- Robots Exclusion Protocol / REP point only to `TOP-APP-02-01`; the terminology is confirmed by [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html).
- BCDR points to the combined business continuity and disaster recovery Topic `TOP-MGT-04-01`; [IBM defines the combined term](https://www.ibm.com/think/topics/business-continuity-disaster-recovery).
- No Topic relationships changed.

## F. Alias Counts by Type — DONE

| `ko_alt` | `en_full` | `acronym` | `synonym` | Total |
|---:|---:|---:|---:|---:|
| 7 | 28 | 3 | 1 | **39** |

## G. Normalization Rules — DONE

- Unicode NFC, leading/trailing whitespace trim, internal Unicode whitespace collapse, and casefold for case-insensitive English/acronym lookup.
- Punctuation remains meaningful. No stemming, approximate matching, generated normalized storage, or ranking.
- Display values are never normalized or renamed.

## H. Duplicate Audit — DONE

- Duplicate alias IDs: **0**; exact duplicates: **0**; normalized duplicates: **0**; alias equal to own canonical name: **0**.
- Synthetic exact and normalized duplicates are rejected in tests.

## I. Ambiguity / Collision Audit — DONE

- Normalized alias keys: **39 UNIQUE**, **0 AMBIGUOUS**.
- Cross-target collisions: **0**; other-target canonical-name collisions: **0**; invalid targets: **0**.
- `SAFE_DISAMBIGUATION_REQUIRED`: **0**; `INVALID_MAPPING`: **0**.
- A synthetic cross-target collision returns both targets and is classified `SAFE_DISAMBIGUATION_REQUIRED`; an other-target canonical-name collision is rejected as `INVALID_MAPPING`.

## J. Semantic Safety Findings — DONE

- Narrow terms such as IDS, IPS, PKI, ACL, and XSS were not made aliases for broader composite Concepts or Topics.
- IDS versus IPS and authentication versus authorization remain distinct. Tests use current Topic IDs to guard these boundaries.
- `CON-MGT-04`'s existing canonical name embeds BCP; its English alias translates the complete Concept name. No standalone BCP alias was added to that composite target.
- Inventory was derived from Concept and Topic names/summaries, question prompts and rubrics, explanations, and Concept content. Coverage intentionally stays below 100%.

## K. Learner UI — DONE

- Concept and Topic detail headers show a small text block grouped as 영문, 약어, 다른 이름 beneath the canonical heading.
- Overview cards carry no alias lists. No internal IDs, enum names, or raw JSON appear in the alias block.
- Semantic text/list markup and visible acronym text do not rely on color or hover.

## L. Anti-cheat — DONE

- Active `/exam`, `/mock-exam`, and pre-submit `/descriptive-training` render no alias block.
- Goal 7D registry remains **4 VERIFIED**, **9 REVIEW_REQUIRED**; aliases do not affect legal verification.

## M. Goal 8A Preservation — DONE

- 20 Concepts, 67 Topics, 180 Questions, 180 primary mappings, 0 unmapped, 0 zero-question Topics, 0 invalid references, and 0 parent mismatches verified.
- `topics.json`, `question_topics.json`, all Concept/Question IDs, and all Question-to-Concept/Topic mappings are unchanged.
- Alias-to-Concept/Topic is parallel to Concept-to-Topic-to-Question.

## N. Goal 7 Regression — DONE

- Goal 7A, 7B, 7C, 7D, and Goal 8A test modules pass in the full regression.
- Existing tests cover `/exam`, `/practice`, `/descriptive-training`, `/mock-exam`, `/law-freshness`, `/result`, `/history`, `/wrong-notes`, `/concepts`, and `/dashboard`.
- No VI, analytics, adaptive learning, or weakness aggregation implementation changed.

## O. Mobile QA — DONE

- Browser-rendered Concept and Topic detail pages checked at 360×740, 390×844, 430×932, and 1280×800.
- Alias blocks were visible at all eight page/viewport combinations; document width stayed within viewport width.
- Long English text, Korean alternatives, acronym badge, hierarchy, and navigation were visually inspected on representative mobile and desktop screenshots. No page-level horizontal overflow.
- Physical Android: **PENDING**; user verification remains the finalization gate.

## P. Tests — DONE

- Goal 8B focused suite: **8 run, 8 passed**, 0 skipped, 0 failures, 0 errors.
- Full `py -3 -m unittest discover tests -q`: **306 run, 305 passed, 1 skipped**, 0 failures, 0 errors.
- Existing optional `PRIVATE_SOURCE_DIR` comparison is skipped. Python 3.14 emits unclosed SQLite `ResourceWarning` messages; no test failure resulted.

## Q. Core Hashes — DONE

All five protected files match the Goal 8A SHA-256 baseline (5 / 5):

| File | SHA-256 |
|---|---|
| `questions.json` | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` |
| `concepts.json` | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` |
| `sources.json` | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` |
| `concept_contents.json` | `025c54ca679ac3e15ac8f8d98a9bf7ae3f120577e13ee44a5911b6beac335171` |
| `explanations.json` | `e62c2ef4d5ef92c3ec8279ae9f1a8ebe2ad23414bed6560c9fbef4751d322696` |

## R. Goal 8C Readiness — PARTIAL

- Deterministic normalization, multi-target resolution, grouping, and collision audit are ready for later reuse.
- Goal 8C integrated search: **NOT STARTED**. No search route, global bar, fuzzy logic, ranking, or autocomplete exists from this work.
- Feature commit, push, Railway terminal status, and production smoke remain before `GOAL_8B_READY_FOR_PHYSICAL_DEVICE_TEST`.
