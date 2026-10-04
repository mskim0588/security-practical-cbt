# Goal 5G: Production Smoke, Security & End-to-End QA Report

## A. Production Identity
- **Application**: 정보보안기사 실기 CBT & 학습 플랫폼
- **Production URL**: `https://web-production-246f1.up.railway.app`
- **Release Commit**: `1b5afc355f0b2cadffe543597f3d303ccbc4ae30` (Short: `1b5afc3`)
- **Release Tag**: `v0.5-production-ready`
- **GitHub Repository**: `https://github.com/mskim0588/security-practical-cbt`
- **Railway Project ID**: `6c284a80-7b2a-4194-99b5-cd4af58f4855`
- **Railway Environment ID**: `61d797c9-d157-48b3-915c-021b089824ab` (`production`)
- **QA Execution Date**: 2026-10-04 KST

---

## B. Runtime Architecture
- **Web Service Engine**: Gunicorn 22.0.0
- **Process Model**: 2 workers, 4 threads per worker, 120s worker timeout
- **Python Version**: Python 3.11.9
- **Build System**: Railpack 0.40.1 (`MISE_PYTHON_GITHUB_ATTESTATIONS=false`)
- **Proxy Configuration**: Werkzeug `ProxyFix(x_for=1, x_proto=1, x_host=1, x_prefix=1)` active for reverse proxy edge termination
- **Deployment Status**: Online & Healthy

---

## C. PostgreSQL Persistence
- **Database Engine**: Railway PostgreSQL 16+ (`Postgres` service on private internal network)
- **Database Driver Scheme**: `postgresql+psycopg2://` (psycopg2-binary 2.9.13)
- **Data Persistence**: Backed by persistent volume `postgres-volume`
- **Session Management**: Scoped SQLAlchemy sessions with explicit commit/rollback lifecycle
- **Local Data Isolation**: Zero local SQLite database files transferred; production initialized cleanly with independent schema

---

## D. Guest E2E Workflow
- **Exam Candidate Generation**: Standard exam renders 18 total candidates (12 short, 4 descriptive, 2 practical candidates)
- **Scoring Contract**: 17 scored questions (12 short @ 3 pts = 36 pts, 4 descriptive @ 12 pts = 48 pts, 1 practical @ 16 pts = 16 pts; Total: 100 pts, Pass threshold: 60 pts)
- **Practical Selection Contract**: User selects 1 of 2 practical candidates (e.g., Q-PRAC-001); unselected candidate (Q-PRAC-002) is recorded with status `unselected` and awarded 0 points without penalizing the candidate score
- **Review Page QA**: Real-time summary of answered vs unanswered questions, status badges, and practical selection banner
- **Submission (PRG Pattern)**: POST `/submit` validates CSRF and submission token, executes deterministic grading, persists attempt, and redirects via HTTP 302 to `/result/<attempt_id>`

---

## E. Result Ownership & IDOR Protection
- **Session Ownership Binding**: Each guest submission records the resulting `attempt_id` in the guest's encrypted session cookie
- **Same-Session Result Access**: Guest who submitted attempt accesses `/result/<attempt_id>` -> HTTP 200 OK with full question breakdowns, score, and model answers
- **Cross-Session IDOR Defense**: Separate guest session (Browser B) attempting to access Browser A's `/result/<attempt_id>` is denied with HTTP 403 Forbidden
- **Zero Information Leakage**: IDOR 403 response contains 0 bytes of candidate answers, scores, rubrics, or explanations
- **Search Engine Isolation**: All result views strictly inject header `X-Robots-Tag: noindex, nofollow`
- **Invalid ID Handling**: Direct access to non-existent `/result/<invalid>` denied with HTTP 403 (unauthenticated) or HTTP 404 (authenticated) using clean custom templates with 0 stack trace

---

## F. Authorization & Protected Routes
- **Unauthenticated Access Control**:
  - `GET /dashboard` -> HTTP 302 Redirect to `/admin-login?next=/dashboard`
  - `GET /history` -> HTTP 302 Redirect to `/admin-login?next=/history`
  - `GET /wrong-notes` -> HTTP 302 Redirect to `/admin-login?next=/wrong-notes`
  - `GET /history/<id>` -> HTTP 302 Redirect to `/admin-login`
  - `GET /wrong-notes/<id>` -> HTTP 302 Redirect to `/admin-login`
  - `GET /history/<id>/delete` -> HTTP 405 Method Not Allowed
  - `POST /history/<id>/delete` (unauthenticated) -> HTTP 302 / 403 Forbidden
- **Information Boundary**: Unauthenticated requests to protected endpoints expose exactly 0 bytes of Owner learning data

---

## G. Owner Authentication & E2E Loop
- **Passphrase Verification**: Admin authentication uses constant-time `hmac.compare_digest` against `ADMIN_ACCESS_KEY`
- **Brute-Force Mitigation**: Failed login introduces artificial 300ms timing delay and logs security warning (`Failed admin login attempt`) without logging the secret
- **Session Fixation Defense**: Successful login resets session state while preserving CSRF token and guest ownership list
- **Cookie Hardening**: Production session cookies configured with `Secure; HttpOnly; SameSite=Lax`
- **Dashboard Integrity**: Owner KPI cards, category achievement radar, weak concept list, and score trends render dynamically from Owner database attempts
- **Guest / Owner Isolation**: Guest attempts are strictly excluded from Owner History and Dashboard analytics (`is_owner = False`)
- **Direct Access Isolation**: Authenticated Owner accessing guest attempt `/history/<guest_attempt_id>` receives clean HTTP 404 Not Found

---

## H. Wrong Notes Management
- **Automated Detection**: Incorrect and partial answers in Owner exams are automatically registered into Owner Wrong Notes
- **State Transition**: Unresolved questions remain in wrong notes; upon answering correctly in a subsequent exam, the note transitions to `resolved`
- **Status Filter**: Wrong notes dashboard accurately filters by unresolved vs resolved questions

---

## I. Adaptive & Wrong Review Modes
- **Owner Wrong Review (`/exam?mode=wrong_review`)**: Prioritizes questions currently registered as unresolved wrong notes
- **Owner Adaptive Mode (`/exam?mode=adaptive`)**: Analyzes Owner weak categories and concepts, dynamically applying weighted probability distribution
- **Guest Safe Fallback**: Unauthenticated requests to `/exam?mode=wrong_review` and `/exam?mode=adaptive` safely fall back to standard or random exams without exposing Owner wrong notes or throwing runtime exceptions

---

## J. Concept Library & 180 Explanations
- **Concept Catalog (`/concepts`)**: Displays all 20 standardized concepts classified under 5 domains:
  1. 시스템 보안 (System Security: CON-SYS-01 ~ 03)
  2. 네트워크 보안 (Network Security: CON-NET-01 ~ 04)
  3. 애플리케이션 보안 (Application Security: CON-APP-01 ~ 04)
  4. 암호학 및 정보보안 일반 (Cryptography & InfoSec: CON-CRY-01 ~ 03)
  5. 정보보안 관리 및 법규 (Security Management & Laws: CON-MGT-01 ~ 04, CON-SEC-01 ~ 02)
- **Concept Detail Pages**: Verified all 20 individual URLs (`/concepts/<concept_id>`); all return HTTP 200 OK with key takeaways, summaries, and related question links
- **Invalid Concept**: `/concepts/CON-INVALID-999` returns clean HTTP 404 Not Found
- **Deep Explanations**: 180 questions mapped to structured explanations with `why_correct`, `wrong_traps`, scoring rubrics, and source citations

---

## K. AI Prompt Helper
- **Permitted Views**: AI prompt helper modal is active and verified on:
  - Result Page (`/result/<attempt_id>`)
  - History Detail Page (`/history/<attempt_id>`)
  - Wrong Notes Detail Page (`/wrong-notes/<question_id>`)
- **Anti-Cheat Enforcement**: AI prompt modal is strictly suppressed and completely absent from:
  - Exam View (`/exam`)
  - Review View (`/review`)
- **Template Functions**: Generates structured AI prompts for ChatGPT / Gemini with 1-click clipboard copy

---

## L. CSRF & State-Changing Integrity
- **Protection**: Session-backed CSRF token validation enforced on all POST endpoints (`/submit`, `/review`, `/admin-login`, `/admin-logout`, `/history/<id>/delete`) via `session["csrf_token"]`, form/header transmission, and constant-time `hmac.compare_digest`
- **Rejection**: POST requests missing `csrf_token` or with mismatched tokens return HTTP 403 Forbidden
- **Idempotency Multi-Worker Safety**: Resubmitting the same exam submission with identical `submission_token` returns HTTP 302 to the existing attempt without creating duplicate records or causing race condition database locks

---

## M. Security Headers & Network Hygiene
- **Content-Security-Policy (CSP)**: Active across all endpoints
- **X-Content-Type-Options**: `nosniff`
- **X-Frame-Options**: `SAMEORIGIN`
- **Referrer-Policy**: `strict-origin-when-cross-origin`
- **HTTPS Enforcement**: 100% TLS/HTTPS enforced by Railway Edge proxy; explicit `Strict-Transport-Security` (HSTS) response header is not injected by Railway Edge by default (cataloged in P2 hardening backlog)
- **Mixed Content**: 0 mixed content resources detected

---

## N. Error Handling & Leakage Prevention
- **HTTP 403 / 404 / 405**: Handled by custom Jinja templates with consistent styling
- **Stack Trace Suppression**: `DEBUG=False` verified; zero Flask debug tracebacks or Python exceptions rendered to clients
- **Credential Protection**: Zero database connection strings, passwords, or access keys exposed in HTTP bodies or headers

---

## O. Runtime Logs Review
- **Gunicorn Workers**: Running steadily without crashes, worker recycles, or restart loops
- **Log Hygiene**: Verified zero occurrences of `SECRET_KEY`, `ADMIN_ACCESS_KEY`, or `DATABASE_URL` passwords in Railway deployment or runtime logs
- **Error Count**: 0 unhandled exceptions, 0 database disconnects, 0 transaction leaks

---

## P. Automated Regression & Core Hashes
- **Local Unit Suite**: Ran 215 tests, Passed 214, Skipped 1 (`test_sources_match_external_files`), Failures 0, Errors 0
- **Live Production E2E Suite**: 58 automated live HTTP assertions executed against `https://web-production-246f1.up.railway.app`:
  - Total Passed: 58
  - Total Failed: 0
  - Total Warnings: 0
- **Core Data SHA-256 Hashes**:
  - `app/data/questions.json`: `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` (MATCH)
  - `app/data/concepts.json`: `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` (MATCH)
  - `app/data/sources.json`: `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` (MATCH)

---

## Q. Severity Classification & Findings
- **P0 (Critical Vulnerabilities / Exposures)**: 0
- **P1 (Core Functional / Isolation Defects)**: 0
- **New P2 Findings**: 0
- **Known P2 Backlog (Total: 5)**:
  1. `P2-1`: Legacy script comment polish
  2. `P2-2`: CSP nonce / inline script-style hardening & explicit HSTS header
  3. `P2-3`: Guest attempt retention / TTL policy
  4. `P2-4`: Alembic migration framework
  5. `P2-5`: Structured production logging
- **Post-Production Architecture Backlog**:
  - `POST-PRODUCTION ACCESS POLICY`: Railway Private Network or site-wide access gate retained as future operational option

---

## R. Final QA Verdict
- **Goal 5G Result**: **PASS (ALL 41 GATES SATISFIED)**
- **Release Baseline Status**: `v0.5-production-ready` verified on live Railway PostgreSQL production environment
- **Production Final Tag**: Awaiting user approval per Section 50 protocol (no automatic tag created)
