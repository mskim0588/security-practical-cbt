# Goal 7A — 회독 / 반복 학습 모드

## Baseline

- Branch: `master`
- Baseline HEAD: `5969c7b565b1fbad6399b43c9b552d6679cbd557`
- Release baseline: `v0.6-mobile-final`
- Goal 6 status: COMPLETE

## Architecture reused

- Canonical `Grader`, `ExamService.parse_submission`, explanation/concept mappings, and Goal 6 local AI prompt helper are reused.
- One existing `ExamAttempt` represents a practice session. An internal metadata `AnswerRecord` stores the fixed shuffled question set and progress; each submitted question/round adds one normal answer record.
- Practice records are excluded from normal exam history, wrong-note, and dashboard aggregates.
- No DB schema change or production migration is required.

## Practice workflow and persistence

- Entry: `/practice`; session: `/practice/<attempt_id>`.
- Supports 1/2/3 rounds and existing all/category/type scopes.
- One question is shown at a time. Answers, explanations, concepts, and AI helper remain hidden until submission.
- Immediate results use `correct`, `partial`, and `wrong` presentation mapped from existing achievement states.
- Progress tracks current round, answered count, correct/partial/wrong counts, per-question attempts, and latest result.
- The question order is shuffled once and persisted for every configured round.
- POST/Redirect/GET, CSRF, phase-based idempotency, row locking, and owner/session authorization protect refresh and duplicate actions.
- Guest access remains session-bound; authenticated owner sessions are persisted and resumable from the setup page.

## Tests

- Goal 7A targeted: 14 passed, 0 failed, 0 errors.
- Related targeted regression: 51 passed, 0 failed, 0 errors.
- Full regression: 248 ran, 247 passed, 1 skipped, 0 failures, 0 errors.
- Intentional skip: external source filename comparison when `PRIVATE_SOURCE_DIR` is unset.

## Mobile regression

- Chromium rendered checks passed at 360×740, 390×844, 430×932, and 1280×800.
- No page-level horizontal overflow; answer controls and next action were reachable; the AI modal fit and scrolled correctly.
- One-round practical sessions completed at each viewport with no uncaught JavaScript errors and no AI-provider requests.
- Normal `/exam` remained loadable, overflow-free, and free of AI helper controls.

## Core data integrity

- Protected datasets: 5 / 5 SHA-256 MATCH.
- `questions.json`, `concepts.json`, `sources.json`, `concept_contents.json`, and `explanations.json` were not modified.

## Production result

- Functional commit: `e33d2481688b7c4d5e61e9c99ce978a2a5701abd`.
- GitHub push: PASS; `master` synchronized with `origin/master`.
- Railway deployment: SUCCESS.
- `GET /`: 200; `GET /healthz`: 200; database `healthy`; environment `production`.
- Production guest smoke: setup, 1-round start, immediate grading, explanation, concept, next question, and round completion PASS.
- Normal `/exam` → `/review` smoke PASS; no uncaught JavaScript errors, page overflow, raw source metadata, or AI-provider requests.

## Known limitations

- Physical-device practice-mode testing has not been performed; automated viewport coverage only.
- Goal 7B, Goal 7C, and Goal 7D are out of scope and were not started.

## Checkpoint

- DONE: baseline recovery, architecture inspection, implementation, targeted tests, full regression, data integrity, local browser QA, functional commit/push, Railway deployment, production smoke.
- PARTIAL: documentation-only closure push.
- TODO: verify Railway health after the documentation-only commit.
- BLOCKED: none.
- Last Safe Step: production smoke passed on functional commit `e33d248`.
- Next Step: commit and push this final production verification record, then recheck `/healthz`.
