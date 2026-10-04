# Goal 5F: GitHub Remote & Railway PostgreSQL Production Deployment Report

## A. Local Release Baseline
- **Release Commit**: `1b5afc355f0b2cadffe543597f3d303ccbc4ae30` (Short: `1b5afc3`)
- **Commit Message**: `feat: finalize Goal 5 production-ready baseline`
- **Release Tag**: `v0.5-production-ready`
- **Pre-Push Test Status**: Ran 215 tests in 21.768s (214 Passed, 1 Skipped `test_sources_match_external_files`, 0 Failures, 0 Errors)
- **Local Working Tree**: Clean

---

## B. GitHub Remote Configuration
- **Repository Name**: `security-practical-cbt`
- **Repository Visibility**: `public`
- **Public Web URL**: `https://github.com/mskim0588/security-practical-cbt`
- **Clone URL**: `https://github.com/mskim0588/security-practical-cbt.git`
- **Remote Tracking**: `origin/master -> master`
- **Remote Commit**: `1b5afc355f0b2cadffe543597f3d303ccbc4ae30`
- **Remote Tag**: `v0.5-production-ready` verified pointing directly to commit `1b5afc3`

---

## C. Public Repository Safety Audit
- **Tracked Binary Documents**: **0** (No `.pdf`, `.docx`, `.hwp`, `.hwpx`, `.epub`, `.dump` files tracked)
- **Sensitive Configuration**: Zero `.env` files tracked (enforced by `.gitignore`)
- **Personal Local Paths**: Zero developer machine absolute paths (`C:\Users\`, `G:\`, `OneDrive`, Google Drive) in tracked code
- **Credentials & API Keys**: Zero private secrets or passphrases committed
- **Source Asset Policy**: Fully codified and published in `docs/SOURCE_ASSET_POLICY.md`

---

## D. Railway Project Infrastructure
- **Project Name**: `security-practical-cbt`
- **Project ID**: `6c284a80-7b2a-4194-99b5-cd4af58f4855`
- **Environment**: `production` (`61d797c9-d157-48b3-915c-021b089824ab`)
- **Web Service**: `web` (`99b83c04-5088-4a12-8efe-28dc0b5ee9a7`)
  - Continuous Delivery: Connected to GitHub repository `mskim0588/security-practical-cbt`
  - Production Branch: `master`
  - Builder: Railpack 0.40.1 / mise / Python 3.11.9

---

## E. PostgreSQL Database Service
- **Service Name**: `Postgres`
- **Service ID**: `f3dbeb09-2389-48c7-9cec-808824d85627`
- **Database Engine**: PostgreSQL
- **Connection Isolation**: Internal private network (`postgres.railway.internal:5432`)
- **Database Origin**: Clean empty production database (zero local dev SQLite records or personal history copied)

---

## F. Production Environment Variables
All production variables are configured securely on Railway without exposing values in repository or reports:
- `DATABASE_URL`: Set (internal connection URI reference to `Postgres` service)
- `SECRET_KEY`: Set (Cryptographically secure 64-char random hexadecimal key)
- `ADMIN_ACCESS_KEY`: Set (Production administrator passphrase)
- `FLASK_ENV`: Set to `production`
- `DEBUG`: Set to `False`
- `USE_PROXYFIX`: Set to `True`
- `MISE_PYTHON_GITHUB_ATTESTATIONS`: Set to `false` (Railpack mise package build compatibility)

---

## G. Build Execution
- **Deployment ID**: `d2bdffb8-a45d-478b-b81c-05ba1375faef`
- **Python Version**: CPython 3.11.9
- **Package Installation**: Successfully installed `Flask-3.1.3`, `Jinja2-3.1.6`, `SQLAlchemy-2.1.3`, `gunicorn-26.2.0`, `psycopg2-binary-2.9.13`, etc.
- **Container Image Digest**: `sha256:a5069d762f7191d86a7edc7f265a79521af1b8cfaa3b359957782e2b4f173395`
- **Build Status**: **SUCCESS**

---

## H. Gunicorn Runtime Status
- **Process Model**: Gunicorn 26.2.0 with `gthread` worker class
- **Concurrency**: 2 worker processes with 4 threads each (8 concurrent request handlers)
- **Port Binding**: Listening on `0.0.0.0:8080` (Railway `$PORT` mapping)
- **Worker Status**: Worker 2 (PID 2) and Worker 3 (PID 3) booted and active
- **Server Health**: Steady-state execution, zero worker crashes or restart loops

---

## I. Production Schema Initialization
- **Table Creation**: `Base.metadata.create_all()` executed cleanly against empty PostgreSQL instance.
- **Database Tables**:
  - `exam_attempts` (including `is_owner`, `submission_token`, and unique index)
  - `answer_records`
  - `wrong_answer_items`
- **Data Persistence**: Verified by executing live exam submission flow on production; attempt and answers written to PostgreSQL successfully.

---

## J. Production URL & HTTPS
- **Public Domain**: `https://web-production-246f1.up.railway.app`
- **Protocol**: HTTPS / TLS 1.3 enforced at Railway Edge Proxy
- **Availability**: Live worldwide

---

## K. Health Check (`/healthz`)
- **Request**: `GET https://web-production-246f1.up.railway.app/healthz`
- **Status Code**: `200 OK`
- **Response Payload**:
  ```json
  {
    "database": "healthy",
    "environment": "production",
    "status": "ok",
    "version": "0.5.0"
  }
  ```
- **Information Leakage**: Zero internal hostnames, passwords, connection URIs, or SQL details exposed.

---

## L. Startup Smoke Verification
| Endpoint | Expected | Actual | Smoke Test Result |
|---|:---:|:---:|:---:|
| `GET /` (Home) | 200 | 200 | PASS |
| `GET /concepts` (Concepts Catalog) | 200 | 200 | PASS |
| `GET /concepts/CON-NET-01` (Concept Detail) | 200 | 200 | PASS |
| `GET /static/css/style.css` (CSS) | 200 | 200 | PASS |
| `GET /static/js/exam.js` (JS) | 200 | 200 | PASS |
| `GET /admin-login` (Admin Login Form) | 200 | 200 | PASS |
| `GET /exam?mode=standard` (Standard Exam) | 200 | 200 | PASS |
| `GET /history` (Guest Protected Route) | 302 | 302 | PASS (Redirects to `/admin-login`) |
| `GET /dashboard` (Guest Protected Route) | 302 | 302 | PASS (Redirects to `/admin-login`) |
| `POST /admin-login` (Valid Passphrase) | 302 | 302 | PASS (Redirects to `/dashboard`) |
| `GET /dashboard` (Authenticated Session) | 200 | 200 | PASS (Owner Dashboard Rendered) |
| `POST /submit` (Standard Guest Exam) | 302 | 302 | PASS (Persisted in PostgreSQL) |
| `GET /result/1` (Exam Result Report) | 200 | 200 | PASS (Result Rendered) |

---

## M. Cookie Security
Live HTTP response headers verified on production session cookie:
- **`Secure`**: `True` (Cookie restricted to HTTPS)
- **`HttpOnly`**: `True` (Cookie inaccessible to JavaScript `document.cookie`)
- **`SameSite`**: `Lax` (Cross-site request forgery protection)
- **`Path`**: `/`

---

## N. Security Headers Verification
Verified live on production responses:
- `Content-Security-Policy`: `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';`
- `X-Content-Type-Options`: `nosniff`
- `X-Frame-Options`: `SAMEORIGIN`
- `Referrer-Policy`: `strict-origin-when-cross-origin`

---

## O. Logging & Secret Scrubbing
- **Access Logs**: Streaming correctly to stdout with client IPs, timestamps, HTTP verbs, status codes, and request durations.
- **Secret Scrubbing**: Zero instances of `SECRET_KEY`, `ADMIN_ACCESS_KEY`, `DATABASE_URL`, or database passwords in Railway deployment or runtime logs.

---

## P. Rollback Readiness
- **Production Baseline Tag**: `v0.5-production-ready` (Commit `1b5afc3`)
- **Prior Stable Tag**: `v0.4-learning-ui-final`
- **Rollback Option**: 1-click redeploy of prior deployment in Railway UI or checkout of `v0.4-learning-ui-final`.
- **Database Safety**: Additive schema design allows rollbacks without destructive data loss.

---

## Q. Known Backlog (P2 Items)
- **P2-1**: Offline audit script docstring polish in `scripts/`.
- **P2-2**: Implementation of CSP Nonces to phase out `'unsafe-inline'`.
- **P2-3**: Guest attempt data retention / TTL policy.
- **P2-4**: Transition to Alembic for complex future migrations.
- **P2-5**: Structured JSON logging format for enterprise APM ingestion.

---

## R. Release Decision
- **Goal 5F Deployment Gate**: **PASS (LIVE ON PRODUCTION)**
- **System Status**: Fully operational on Railway + PostgreSQL.
- **Recommendation**: Proceed to Goal 5G (Production Smoke & Comprehensive Security QA) upon user review.
