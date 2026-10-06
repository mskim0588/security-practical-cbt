# Goal 7B Structured Descriptive Answer Training

## Baseline Gate

- Branch: `master`.
- Baseline HEAD: `a58af18b6f6267ba159f30504df1dd53b2ca0525`.
- Baseline `origin/master`: `a58af18b6f6267ba159f30504df1dd53b2ca0525`.
- Working tree at gate: clean.
- Goal 7A report: `GOAL_7A_COMPLETE`, `GOAL_7B_READY`, Physical Android `PASS`.
- Railway status for baseline commit: `SUCCESS` (GitHub commit status `security-practical-cbt - web`, production service).

## Architecture Decision

- Reuse `ExamAttempt` and `AnswerRecord` with a dedicated training `exam_mode` and metadata answer record.
- Reuse canonical descriptive questions, model answers, rubrics, explanations, concepts, and the Goal 6 local-only AI Helper.
- No DB schema change or production migration is required.
- Keep training attempts isolated from normal history, analytics, and wrong-note aggregates.

## Implemented Workflow

- Entry: `/descriptive-training`.
- Session: `/descriptive-training/<attempt_id>`.
- State-changing routes: `/descriptive-training/start`, `/descriptive-training/<attempt_id>/answer`, and `/descriptive-training/<attempt_id>/next`.
- Each canonical descriptive sub-question becomes a separate answer field with a prompt-sensitive structure hint.
- Structure evaluation reports `충족`, `부분 충족`, or `미충족` from required-field completion.
- Keyword feedback reports matched core keywords and missing canonical rubric groups.
- False-positive controls apply Unicode normalization, independent ASCII token boundaries, standalone-symbol handling, and direct negation rejection. An exact canonical model-answer match remains authoritative.
- Model answer, per-field rubric result, explanation, related concept, and Goal 6 local-only AI Helper appear only after submission.
- CSRF, POST/Redirect/GET, phase-based idempotency, row locking, and owner/session authorization are reused.

## Validation So Far

- Goal 7B targeted tests: 12 passed, 0 failures, 0 errors.
- Related targeted regression including all Goal 7A `/practice` tests: 39 passed, 0 failures, 0 errors.
- Canonical answer compatibility: 44 / 44 descriptive model-answer sets evaluated as fully sufficient.
- Chromium rendered QA: PASS at 360x740, 390x844, 430x932, and 1280x800.
- Chromium findings: no horizontal overflow; primary actions 52px high; pre-submit answers/AI hidden; result, explanation, concept link, next action, and local AI prompt available after submission.
- AI Helper browser check: modal fit and scrolled at every viewport; fixed provider home URLs; clipboard success and manual-selection fallback passed; zero AI-provider requests.
- Goal 7A browser regression: `/practice` question submission and immediate learning result passed at all four viewports.
- Browser console/runtime errors: 0. Required-resource failures: 0. A non-functional `/favicon.ico` 404 remains unchanged.
- Full regression: 260 ran, 259 passed, 1 skipped, 0 failures, 0 errors.
- Intentional skip: external source filename comparison when `PRIVATE_SOURCE_DIR` is unset.
- Protected core data: 5 / 5 SHA-256 MATCH; no protected dataset appears in the Git diff.

## Protected Core Data Baseline

- `questions.json`: `661098CE80E957B033FBB1A2B540701815791169ECD57C0F367720B94F3D5DC9`
- `concepts.json`: `D33CDD63824C01C6537DD6F2CB6829B58BF121883A05EB406803BBE58BAD5943`
- `sources.json`: `9AE37CE41F1B3BCCF0047474FCA8E8332AD18F1EAD298EE2F17FE85574049A21`
- `concept_contents.json`: `025C54CA679AC3E15AC8F8D98A9BF7AE3F120577E13EE44A5911B6BEAC335171`
- `explanations.json`: `E62C2EF4D5EF92C3EC8279AE9F1A8EBE2AD23414BED6560C9FBEF4751D322696`

## Checkpoint

- DONE: baseline Git/report parity, baseline Railway terminal success, architecture inspection, protected-data baseline hashes, routes, service, structured UI, evaluation feedback, isolation filters, targeted tests, Goal 7A regression, and mobile/desktop Chromium QA.
- PARTIAL: release handoff.
- TODO: commit, push, Railway terminal deployment result, and production smoke.
- BLOCKED: none.
- Last Safe Step: full regression and protected-data integrity gates passed.
- Next Step: commit as `feat: add structured descriptive answer training`, push `master`, wait for Railway, and run production smoke.

## Release State

- Goal 7B is not marked complete.
- Expected final state after successful deployment and smoke: `GOAL_7B_READY_FOR_PHYSICAL_DEVICE_TEST`.
