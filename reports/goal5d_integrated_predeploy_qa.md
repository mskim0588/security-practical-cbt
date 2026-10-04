# Goal 5D: Integrated Pre-Deployment QA & Release Candidate Gate Report

## A. Baseline Summary
- **Current Version / Target Release**: v0.5-rc (Release Candidate Baseline)
- **Preceding Goals**:
  - Goal 5A (Production Architecture & Security Hardening): COMPLETED
  - Goal 5B & Cleanup (Copyright & Source Asset Isolation): COMPLETED (0 tracked binaries/PDFs/paths)
  - Goal 5C (Guest / Owner Data Isolation & Security Boundary): COMPLETED
- **Evaluation Gate**: Production Readiness for Railway + PostgreSQL deployment.

---

## B. Git State & Working Tree Audit
- **Current Branch**: `master`
- **Current HEAD**: `6988c3e feat: finalize Goal 4 learning UX baseline`
- **Active Git Tags**:
  - `v0.2-question-bank-final`
  - `v0.3-learning-analytics-final`
  - `v0.4-learning-ui-final`
- **Working Tree State**:
  - Goal 5A, 5B, 5C changes remain uncommitted in the working tree as intended.
  - Zero staged files (`git diff --cached` is empty).
  - No auto-commits or tags created during this gate evaluation.
  - Remote repository: Not configured locally (`git remote -v` empty).

---

## C. Copyright & Source Asset Hygiene
- **Raw Document Files in Working Tree**: 0 (No `.pdf`, `.docx`, `.hwp`, `.hwpx`, `.epub`, `.dump` files).
- **Git Tracked Source Binaries**: 0.
- **Static Assets Directory (`app/static/`)**: Only authorized static files (`style.css`, `exam.js`).
- **Production Runtime Dependencies**: Zero PDF/OCR parser dependencies (`pypdf`, `pytesseract`, etc. are strictly absent from `app/`).
- **Personal Paths & Machine Specifics**: 0 occurrences of `C:\Users\`, `G:\`, `OneDrive`, or Google Drive paths across `app/`, `tests/`, and `scripts/`.
- **Source Isolation Tests**: 8 out of 8 tests PASS (`test_source_asset_isolation.py`).

---

## D. Guest / Owner Data Isolation
- **Database Model Isolation**:
  - `ExamAttempt.is_owner` column strictly differentiates owner attempts (`is_owner=True`) from public guest attempts (`is_owner=False`).
- **Service Scope Enforcement**:
  - `HistoryService.get_attempts(is_owner=True)`: Guest attempts are 100% excluded from owner history listings.
  - `WrongAnswerService.get_wrong_questions(is_owner=True)`: Guest failures do not appear in owner wrong notes; guest correct answers never resolve owner wrong items.
  - `AnalyticsService.get_summary_stats(is_owner=True)` & Category/Concept breakdown: Guest attempts do not distort owner metrics (average score, pass rates, VI).
- **Dynamic Exam Generation**:
  - Guest `mode=adaptive` safely falls back to standard random exam (owner VI is not exposed or used).
  - Guest `mode=wrong_review` safely falls back to standard exam (owner wrong notes are protected).

---

## E. Authorization & Protected Routes
- **Route Guarding**:
  - `@admin_required` applied to all owner-restricted endpoints: `/dashboard`, `/history`, `/history/<id>`, `/history/<id>/delete`, `/wrong-notes`, `/wrong-notes/<id>`.
  - Non-authenticated requests are redirected with 302 to `/admin-login` with safe `next` parameter handling.
- **Master Access Key**:
  - Validated via `hmac.compare_digest` to prevent timing attacks.
  - Brute-force delay (`time.sleep(0.3)`) and audit logging on failed authentication.
- **Session Lifecycle & Session Fixation Defense**:
  - Flask utilizes client-side signed cookie sessions (using HMAC with `SECRET_KEY`).
  - Upon successful login: `csrf_token` and `submitted_attempts` (exam ownership) are preserved while sensitive session attributes are reset, preventing session fixation without losing guest attempt access.
  - Upon logout: `session.clear()` removes `is_admin`, revoking protected route access immediately.

---

## F. Result Ownership & IDOR Protection
- **Ownership Verification on `/result/<attempt_id>`**:
  - Accessible ONLY if `is_admin_authenticated()` OR `attempt_id in session.get("submitted_attempts", [])`.
  - Foreign guest attempts accessed across different browser sessions return HTTP 403 Forbidden.
  - Non-existent attempts return HTTP 404 Not Found.
  - Even admin sessions cannot view foreign guest attempts unless explicitly owned in session, preventing accidental privacy leakage.
- **SEO & Search Indexing Defense**:
  - `X-Robots-Tag: noindex, nofollow` response header injected on all result pages.

---

## G. CSRF Protection
- **Session-Based CSRF Service**:
  - Cryptographically secure 32-byte hexadecimal token (`secrets.token_hex(32)`) generated in session.
  - Enforced via `@csrf_protect` decorator across all state-changing POST routes:
    - `POST /submit`
    - `POST /history/<attempt_id>/delete`
    - `POST /admin-login`
    - `POST /admin-logout`
  - Token validated using constant-time comparison (`hmac.compare_digest`).
  - Missing or mismatched tokens abort immediately with HTTP 403 Forbidden.
- **Separation of Concerns**:
  - `csrf_token`: Defends against Cross-Site Request Forgery across user sessions.
  - `submission_token`: Dedicated idempotency token preventing duplicate submission processing.

---

## H. Submission Idempotency & Concurrency
- **Duplicate Submit Protection**:
  - Form submission includes a unique `submission_token`.
  - Database schema defines `ExamAttempt.submission_token` with UNIQUE constraint and index (`uq_exam_attempts_submission_token`).
  - First submission persists attempt and child `AnswerRecord` items (18 records).
  - Rapid double/triple submit, browser reload (F5), or network retry detects the existing token and returns the initial attempt without re-scoring or duplicate database inserts.
  - Handled cleanly even in database-level concurrent INSERT race conditions via `IntegrityError` catch block.

---

## I. PostgreSQL Compatibility
- **Dialect & Syntax Review**:
  - SQLAlchemy 2.0 Declarative mapping with standard cross-database column types (`Integer`, `String(64)`, `Float`, `Boolean`, `DateTime`).
  - Connection pooling configured with `pool_pre_ping=True` and `pool_recycle=300` for remote cloud database resiliency.
  - `postgres://` connection string normalization to `postgresql://` implemented in `app/config.py`.
  - Boolean field `is_owner` mapped via SQLAlchemy `Boolean` type, ensuring proper handling of `TRUE`/`FALSE` across SQLite and PostgreSQL.

---

## J. Runtime Migration Risk Analysis
- **Migration Strategy Evaluation (`_migrate_schema`)**:
  - Fresh Production Database: On an empty PostgreSQL database, `Base.metadata.create_all()` creates all tables with current columns (`submission_token`, `is_owner`) and indices directly.
  - Runtime Inspector: `_migrate_schema()` checks `inspector.get_columns("exam_attempts")`. Because columns already exist on fresh DBs, runtime DDL execution is completely bypassed.
  - Multi-Worker Concurrency: Gunicorn spawns 2 workers. Both workers initialize the app. If tables are already up to date, no ALTER TABLE executes. If an older database requires column additions, duplicate DDL exceptions are caught safely via `try...except Exception: pass`.
  - Risk Classification: Zero blocker for empty production deployment.

---

## K. Gunicorn Server Configuration
- **Procfile Command**:
  `web: gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile -`
- **Parameter Validation**:
  - Target: `"app:create_app()"` factory callable verified and imported successfully.
  - Concurrency: 2 worker processes with 4 threads each (8 concurrent request handlers), ideal for Railway container CPU allocations.
  - Timeout: 120 seconds, accommodating complex grading computations and cold startup DB handshakes.
  - Logging: Access and error logs redirected to standard output/error (`-`) for centralized container log aggregation.

---

## L. Railway Configuration & Runtime Files
- **Procfile**: Present and syntactically valid.
- **runtime.txt**: Specifies `python-3.11.9`.
- **requirements.txt**:
  - Production web packages: `Flask>=3.0.0`, `Jinja2>=3.1.0`, `SQLAlchemy>=2.0.0`, `gunicorn>=22.0.0`, `psycopg2-binary>=2.9.9`.
  - Offline audit packages: `pypdf>=5.0.0` (used for offline source verification scripts, zero runtime import in `app/`).
- **.env.example**: Well-documented template with all required keys, default configurations, and security advisories.

---

## M. Health Check (`/healthz`)
- **Normal Operation**: Returns HTTP 200 OK with JSON `{"status": "ok", "database": "healthy", "environment": "production", "version": "0.5.0"}`.
- **Database Failure**: Performs active connection test (`SELECT 1`). Returns generic HTTP 503 Service Unavailable with `{"status": "error", "database": "unhealthy"}`.
- **Information Leakage**: Zero internal connection strings, credentials, DB hostnames, or SQL tracebacks exposed to callers.

---

## N. Security Headers & Proxy Configuration
- **ProxyFix**:
  - Configured with `x_for=1, x_proto=1, x_host=1, x_prefix=1`.
  - Correctly evaluates `request.scheme == 'https'` and client remote address behind Railway's single TLS termination proxy.
- **HTTP Security Headers**:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: SAMEORIGIN`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';`
  - `X-Robots-Tag: noindex, nofollow` on exam result pages.
- **Cookie Security**:
  - `SESSION_COOKIE_SECURE = True` in production mode.
  - `SESSION_COOKIE_HTTPONLY = True`.
  - `SESSION_COOKIE_SAMESITE = "Lax"`.

---

## O. Four Core E2E Journeys Verification
1. **Journey A — Guest Standard Flow**:
   - Guest loads home (`/`) -> opens standard exam (`/exam?mode=standard`) -> inputs answers -> reviews (`/review`) -> submits (`/submit`) -> redirects via PRG pattern to `/result/<attempt_id>` -> 200 OK.
2. **Journey B — Guest Data Isolation**:
   - Guest completes exam -> DB record saved with `is_owner=False` -> Owner logs in via `/admin-login` -> Owner examines `/history`, `/dashboard`, and `/wrong-notes` -> Zero guest attempt records or statistics visible.
3. **Journey C — Owner Learning Loop**:
   - Owner logs in -> takes exam and fails Q-SHORT-001 -> wrong item appears in `/wrong-notes` -> loads `/exam?mode=wrong_review` (displays "오답 다시 풀기 모의고사") -> submits correct answer -> wrong note marked resolved.
4. **Journey D — Owner Adaptive Mode**:
   - Owner logs in -> requests `/exam?mode=adaptive` -> dynamically weights vulnerable concepts based on owner VI metrics (displays "취약 Concept 집중 모의고사") -> submits exam -> analytics updated.

---

## P. Test Suite Verification
- **Execution Command**: `python -m unittest discover tests -v`
- **Execution Time**: 23.521s
- **Total Tests Executed**: 215
- **Passed**: 214
- **Failures**: 0
- **Errors**: 0
- **Skipped**: 1 (`test_sources_match_external_files` - skipped as intended when local `PRIVATE_SOURCE_DIR` is not set).
- **Result**: ALL TESTS GREEN.

---

## Q. Core Data Hash Verification
- `app/data/questions.json`:
  - Expected: `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`
  - Actual: `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9`
  - Status: **MATCH (100% Intact)**
- `app/data/concepts.json`:
  - Expected: `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`
  - Actual: `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943`
  - Status: **MATCH (100% Intact)**
- `app/data/sources.json`:
  - Expected: `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`
  - Actual: `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21`
  - Status: **MATCH (100% Intact)**

---

## R. Remaining Backlog & Non-Blockers (P2 Items)
- **P2-1**: Offline audit scripts in `scripts/` contain historical analysis routines; isolated from production runtime.
- **P2-2**: CSP policy uses `'unsafe-inline'` for vanilla inline script/style handlers; nonces recommended for future hardening.
- **P2-3**: Guest attempt retention policy / periodic cleanup job for high-traffic public installations.
- **P2-4**: Future database migrations should adopt Alembic if complex DDL transformations become necessary.
- **P2-5**: Enhanced structured JSON logging for enterprise APM integration.

---

## S. Deployment Decision
- **P0 Defects**: 0
- **P1 Defects**: 0
- **Goal 5B Copyright Gate**: PASS
- **Goal 5C Isolation Gate**: PASS
- **Release Candidate Gate**: **PASS (APPROVED FOR PRODUCTION RELEASE BASELINE)**
- **Recommendation**: Proceed to Goal 5E (Production Release Baseline) upon user review and approval.
