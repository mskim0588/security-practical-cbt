# Goal 5E: Production Release Baseline Report

## A. Release Identity
- **Release Version**: `v0.5-production-ready`
- **Release Type**: Production Ready Release Candidate Baseline
- **Release Tag Target**: `v0.5-production-ready` (Annotated Git Tag)
- **Deployment Status**: **READY_FOR_DEPLOYMENT (NOT YET DEPLOYED)**

---

## B. Included Goals & Scope Summary
This release baseline consolidates the verification and hardening across four foundational production preparation milestones:
1. **Goal 5A (Production Architecture & Hardening)**: Gunicorn WSGI multi-worker runtime, ProxyFix reverse proxy integration, HTTP security headers, `/healthz` health check endpoint, PostgreSQL connection pool optimization, and CSRF protection.
2. **Goal 5B & Final Cleanup (Copyright & Source Asset Isolation Gate)**: Full isolation of private learning assets, elimination of raw PDF/OCR binaries, eradication of personal local absolute paths in tracked code, and formalization of `docs/SOURCE_ASSET_POLICY.md`.
3. **Goal 5C (Guest / Owner Data Isolation & Security Boundary)**: Strict data segregation between public guests and the system owner across all models, services, analytics, and wrong answer tracking; session-based result ownership IDOR defense; `@admin_required` route protection; and production fail-closed security.
4. **Goal 5D (Integrated Pre-Deployment QA Gate)**: Full regression evaluation across all 215 tests, E2E journey validations, database migration concurrency review, and release candidate qualification.

---

## C. Architecture & Production Infrastructure
- **Web Framework**: Flask 3.1 & Jinja2 3.1 (Autoescaping enabled)
- **ORM / Database Layer**: SQLAlchemy 2.0 (Declarative Base, Scoped Sessions)
- **Database Engine Support**:
  - Local Development: SQLite (`instance/learning.db` or in-memory)
  - Production Deployment: PostgreSQL (via `psycopg2-binary>=2.9.9` with `pool_pre_ping=True`, `pool_recycle=300`)
  - Dynamic URI Normalization: Automatic conversion of legacy `postgres://` to `postgresql://`
- **Application Server (WSGI)**: Gunicorn 22.0+
  - Worker Model: 2 worker processes with 4 threads each (8 concurrent request workers)
  - Process Timeout: 120 seconds
  - Log Channels: Centralized container stdout/stderr streaming (`--access-logfile - --error-logfile -`)
- **PaaS Target**: Railway Cloud Container Infrastructure
  - Deployment Files: `Procfile`, `runtime.txt` (Python 3.11.9), `requirements.txt`

---

## D. Security & Boundary Architecture
- **Flask Session Architecture**:
  - Implementation: **Flask signed client-side session cookie** (using HMAC-SHA256 signatures with `SECRET_KEY`).
  - Session Lifecycle: `session.clear()` resets authenticated state without relying on server-side session stores, re-establishing permission boundaries cleanly while safely preserving client exam ownership (`submitted_attempts`).
  - Production Cookie Flags: `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, lifetime 24 hours.
- **CSRF Protection (`csrf_token`)**:
  - Cryptographically secure 32-byte hexadecimal token generated per session.
  - Required on all state-altering endpoints: `POST /submit`, `POST /history/<id>/delete`, `POST /admin-login`, `POST /admin-logout`.
  - Missing or invalid tokens fail closed with HTTP 403 Forbidden.
- **Submission Idempotency (`submission_token`)**:
  - Form-level idempotency token persisted in `ExamAttempt.submission_token` with UNIQUE constraint and index.
  - Prevents double submissions, network retries, and browser reload duplication without re-scoring or record duplication.
- **Result Ownership & IDOR Protection**:
  - `/result/<attempt_id>` verifies session ownership or authenticated administrator status.
  - Unauthorized guest cross-session access returns HTTP 403 Forbidden.
  - Injected with `X-Robots-Tag: noindex, nofollow` to prevent search engine indexing of personal/guest exam attempts.
- **Protected Zones & Authentication**:
  - All owner zones (`/dashboard`, `/history`, `/wrong-notes`) guarded by `@admin_required`.
  - Non-authenticated requests redirected with HTTP 302 to `/admin-login` with safe `next` parameter routing.
  - Timing attack defense via `hmac.compare_digest` with brute-force delay.
- **Production Secret Fail-Closed**:
  - `SECRET_KEY` must be explicitly defined in production mode; default dev key triggers immediate `RuntimeError` preventing server startup.
- **Network Hardening & Security Headers**:
  - Werkzeug `ProxyFix(x_for=1, x_proto=1, x_host=1, x_prefix=1)` for single reverse proxy TLS termination.
  - HTTP Headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy`.

---

## E. Copyright & Source Asset Policy
- **Tracked Binary Documents**: **0** (`*.pdf`, `*.hwp`, `*.docx`, etc.)
- **Static Directory (`app/static/`)**: Authoritative CSS and JS only; zero private documents or raw dumps.
- **Runtime Dependency**: Zero import or usage of document parsing libraries (`pypdf`, `pytesseract`) in application code.
- **Path Hygiene**: Zero occurrences of developer absolute paths (`C:\Users\`, `G:\`, `OneDrive`, Google Drive) in tracked code.
- **Policy Documentation**: Codified in `docs/SOURCE_ASSET_POLICY.md`.

---

## F. Exam Contract & Content Integrity
- **Question Bank**: 180 total verified questions
  - Short-answer: 112 questions
  - Descriptive: 44 questions
  - Practical candidates: 24 questions
- **Learning Content**:
  - 20 Concepts (`concepts.json` & `concept_contents.json`)
  - 180 Deep Explanations (`explanations.json`)
- **Exam Session Contract**:
  - Rendered: 18 candidate questions (12 Short, 4 Descriptive, 2 Practical Candidates)
  - Scored: 17 questions (12 Short × 3 pts = 36 pts; 4 Descriptive × 12 pts = 48 pts; 1 Selected Practical × 16 pts = 16 pts)
  - Total Points: 100.0 pts
  - Passing Score: 60.0 pts
  - Unselected Practical: `achievement_status = "unselected"` (0 points, excluded from scoring)

---

## G. Full Test Suite Verification
- **Test Command**: `python -m unittest discover tests -v`
- **Total Tests Executed**: 215
- **Passed**: 214
- **Failures**: 0
- **Errors**: 0
- **Skipped**: 1
  - Skipped Test: `test_sources_match_external_files` in `tests/test_sources_registry.py`
  - Reason: Normal behavior when external `PRIVATE_SOURCE_DIR` is not exported in local environment.

---

## H. Core Data Hashes (Exact SHA-256 Match)
- `app/data/questions.json`:
  `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` (MATCH)
- `app/data/concepts.json`:
  `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` (MATCH)
- `app/data/sources.json`:
  `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` (MATCH)

---

## I. Production Environment Variables Contract
| Variable Name | Environment | Required | Default Allowed | Description / Format |
|---|:---:|:---:|:---:|---|
| `SECRET_KEY` | Production | **YES** | **NO** (Fail-Closed) | 64-char random hex key for session signing and CSRF tokens |
| `ADMIN_ACCESS_KEY` | Production | **YES** | YES (Unprotected) | Master passphrase for personal/admin data zones |
| `DATABASE_URL` | Production | **YES** | SQLite Fallback | PostgreSQL connection string (provided by Railway) |
| `FLASK_ENV` | Production | YES | `development` | Set to `production` |
| `DEBUG` | Production | YES | `False` | Set to `False` |
| `USE_PROXYFIX` | Production | Optional | Auto (`True` in prod) | Reverse proxy header trust flag |

---

## J. Known Backlog (P2 Non-Blockers)
- **P2-1 (Offline Script Polish)**: Offline verification scripts in `scripts/` contain legacy analysis notes (zero production impact).
- **P2-2 (CSP Nonce Hardening)**: Replace `'unsafe-inline'` with dynamic cryptographic nonces for script and style tags.
- **P2-3 (Guest Data Retention Policy)**: Periodic batch cleanup or TTL policy for anonymous guest attempts in long-term deployment.
- **P2-4 (Alembic Migration Support)**: Adopt formal Alembic migrations if complex future schema alterations occur.
- **P2-5 (Structured JSON Logging)**: Format Gunicorn and Flask application logs into structured JSON for observability APMs.

### Future Roadmap Separation:
- **Future Goal 7**: Practice/Drill mode, structured descriptive answer training, 180-minute simulation, Review flags, Law freshness UX.
- **Future Goal 8**: 20 Parent Concepts + 50~70 Topics, Aliases, Integrated search, Bookmarking.
- **Future Goal 9**: Navigation/Dashboard slimming, wrong note slimming, Result/History UI consolidation, JSON deduplication.
*(Print functionality permanently excluded from roadmap)*.

---

## K. Rollback Points & Recovery Strategy
- **Previous Known Stable Baseline**: Tag `v0.4-learning-ui-final` (Commit `6988c3e`)
- **Current Production Release Candidate**: Tag `v0.5-production-ready`
- **Application Rollback Procedure**: Checkout `v0.4-learning-ui-final` or redeploy prior commit via Railway deployment dashboard.
- **Database Safety**: All schema additions are additive (`is_owner`, `submission_token`); no destructive DDL rollbacks required.

---

## L. Deployment Gate Summary
- **P0 Defects**: **0**
- **P1 Defects**: **0**
- **Goal 5A Gate**: **PASS**
- **Goal 5B Gate**: **PASS**
- **Goal 5C Gate**: **PASS**
- **Goal 5D Gate**: **PASS**
- **Goal 5E Gate**: **PASS**
- **Action**: Commit and tag baseline locally. Remote push and Railway deployment remain pending Goal 5F.
