# Goal 5: Production Architecture & Deployment Report

> **작성 일자**: 2026-10-04  
> **기준 커밋 / 태그**: `v0.5-production-ready` (이전 태그: `v0.4-learning-ui-final`)  
> **테스트 결과**: **187 / 187 ALL PASS** (기존 181개 + 프로덕션 신규 6개 100% 통과)  
> **목표 인프라**: Railway (Nixpacks / Gunicorn) + PostgreSQL (Managed DB)

---

## 1. 개요 및 목적

Goal 5는 로컬 개발 환경(Flask 개발 서버 + SQLite)에서 안정적인 클라우드 운영 환경(Railway PaaS + PostgreSQL)으로의 전환을 위한 프로덕션 아키텍처 수립 및 배포 기반 완성을 목표로 수행되었습니다.

기존 Goal 4 Final Baseline에서 확립된 180개 문제은행, 20개 개념, 180개 해설, 채점 엔진의 무결성을 100% 보존하면서 다음 5대 과제를 완수하였습니다.

1. **데이터 격리 및 Hybrid Portfolio Architecture 구축**
2. **PostgreSQL 드라이버 및 커넥션 풀링 최적화**
3. **프로덕션 WSGI(Gunicorn) 및 컨테이너 런타임 명세 (`Procfile`, `runtime.txt`)**
4. **보안 강화 (Reverse Proxy 지원, HTTPS Secure Cookie, HTTP 보안 응답 헤더)**
5. **헬스체크(`/healthz`) 및 종합 E2E 프로덕션 테스트 슈트 구축**

---

## 2. 핵심 데이터 무결성 검증 (SHA-256)

기존 Final Baseline 핵심 파일의 SHA-256 해시를 검증한 결과, **1바이트의 오차도 없이 100% 일치**함을 확인하였습니다.

| 파일명 | 유형 | 공식 Baseline SHA-256 | 현재 파일 SHA-256 | 일치 여부 |
| :--- | :---: | :--- | :--- | :---: |
| `questions.json` | 문제은행 (180문항) | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` | `661098ce80e957b033fbb1a2b540701815791169ecd57c0f367720b94f3d5dc9` | **MATCH (100%)** |
| `concepts.json` | 개념 레지스트리 (20종) | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` | `d33cdd63824c01c6537dd6f2cb6829b58bf121883a05eb406803bbe58bad5943` | **MATCH (100%)** |
| `sources.json` | 공식 출처 (12문서) | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` | `9ae37ce41f1b3bccf0047474fca8e8332ad18f1ead298ee2f17fe85574049a21` | **MATCH (100%)** |
| `concept_contents.json` | 개념 심층 학습서 (20종) | 전수 구축 완료 확인 (20개 Concept) | 20개 로드 정상 | **MATCH (100%)** |
| `explanations.json` | 문항별 심층 해설 (180문항) | 전수 구축 완료 확인 (180개 Question) | 180개 로드 정상 | **MATCH (100%)** |

---

## 3. 세부 아키텍처 및 구현 결과

### A. Hybrid Portfolio Deployment (데이터 격리 달성)
- **배경**: 현재 DB 스키마에는 `user_id`가 없으므로, 다수의 외부 사용자가 모의고사를 제출하면 단일 테이블에 합산되어 개인 학습 통계 및 오답노트가 오염되는 P0 리스크가 존재했습니다.
- **해결책**:
  - **Public Zone**: 누구나 로그인 없이 180문항 모의고사(표준/랜덤/적응형), 실시간 자동 채점, 결과 리포트(`/result/<id>`), 개념 학습(`/concepts`)을 자유롭게 이용 가능.
  - **Protected Zone**: 개인 데이터 영역인 응시 이력(`/history`), 취약점 오답노트(`/wrong-notes`), 종합 대시보드(`/dashboard`), 이력 삭제 기능은 `ADMIN_ACCESS_KEY` 환경변수로 보호.
  - **유연성**: `ADMIN_ACCESS_KEY`가 미설정된 환경(로컬 개발/기존 테스트)에서는 데코레이터가 즉각 통과하여 기존 181개 테스트의 동작을 100% 보존.
  - **UI/UX**: 미인증 사용자가 보호 영역 접근 시 안내 배너와 패스프레이즈 입력 폼이 제공되는 `admin_login.html`로 자동 이동하며, 인증 후에는 헤더에 깔끔한 '로그아웃' 버튼 제공.

### B. PostgreSQL 호환성 및 커넥션 풀링
- `psycopg2-binary>=2.9.9` 라이브러리를 의존성에 추가.
- `app/models/database.py`에서 비-SQLite 엔진 연결 시 `pool_pre_ping=True`, `pool_recycle=300` 풀링 옵션 적용.
- Railway의 `postgres://` URL을 SQLAlchemy 표준 `postgresql://`로 자동 치환하는 정규화 로직 유지.

### C. 프로덕션 WSGI 및 컨테이너 명세
- `Procfile` 생성:
  ```text
  web: gunicorn "app:create_app()" --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile -
  ```
- `runtime.txt` 생성: `python-3.11.9`
- `.env.example` 템플릿 생성: 필수 환경변수(`SECRET_KEY`, `ADMIN_ACCESS_KEY`, `DATABASE_URL` 등) 가이드 제공.

### D. 프로덕션 보안 강화
- **Reverse Proxy 지원**: `USE_PROXYFIX=True` 시 Werkzeug `ProxyFix` 미들웨어 적용 (`x_for=1, x_proto=1, x_host=1, x_prefix=1`).
- **Cookie Security Flags**: 프로덕션 모드에서 `SESSION_COOKIE_SECURE=True`, `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"` 강제.
- **HTTP Security Response Headers**: 모든 응답에 `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy` 주입.
- **CSRF 데코레이터 표준화**: GET/HEAD 등 안전한 HTTP 메서드는 통과시키고, POST/PUT/DELETE 등 상태 변경 요청만 엄격히 CSRF 토큰을 검증하도록 보강.

### E. 시스템 헬스체크 (`/healthz`)
- Railway 및 업타임 모니터링을 위한 `/healthz` 엔드포인트 구현:
  - 데이터베이스에 `SELECT 1`을 실행하여 DB 연결 건전성 실시간 확인.
  - 정상 시 `{"status": "ok", "database": "healthy", "environment": "production", "version": "0.5.0"}` (200 OK) 반환.

---

## 4. 테스트 결과 보고

```text
Ran 187 tests in 10.636s

OK
```

- **기존 Goal 1~4 회귀 테스트**: 181 / 181 PASS
- **신규 Goal 5 프로덕션 테스트 (`test_goal5_production.py`)**: 6 / 6 PASS
  1. `test_healthz_endpoint`: 200 OK & DB healthy 확인 (PASS)
  2. `test_security_response_headers`: nosniff, SAMEORIGIN, CSP 헤더 확인 (PASS)
  3. `test_public_routes_accessible_without_auth`: 홈, 개념목록, 개념상세, 표준/랜덤 모의고사 공개 접근 확인 (PASS)
  4. `test_hybrid_mode_when_admin_key_configured`: 패스프레이즈 미인증 시 차단, 오입력 차단, 정답 로그인 성공, 보호영역 정상 조회, 로그아웃 차단 전 라이프사이클 확인 (PASS)
  5. `test_postgres_url_normalization`: postgres:// -> postgresql:// 치환 확인 (PASS)
  6. `test_production_cookie_and_proxyfix_configuration`: 프로덕션 쿠키 및 프록시픽스 설정 확인 (PASS)

---

## 5. Railway 배포 매뉴얼

1. **Railway 프로젝트 생성**:
   - Railway 콘솔 접속 -> "New Project" -> "Deploy from GitHub repo" -> `security-practical-cbt` 선택.
2. **PostgreSQL 추가**:
   - "+ New" -> "Database" -> "Add PostgreSQL" 선택.
   - Web Service의 변수에 `DATABASE_URL`이 자동으로 연결됩니다.
3. **환경변수(Variables) 설정**:
   - `FLASK_ENV`: `production`
   - `DEBUG`: `False`
   - `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"` 실행 결과값
   - `ADMIN_ACCESS_KEY`: 관리자 개인 패스프레이즈
   - `USE_PROXYFIX`: `True`
   - `SESSION_COOKIE_SECURE`: `True`
4. **배포 확인**:
   - 배포 로그에서 `Gunicorn` 워커 2개 및 스레드 4개 기동 확인.
   - `https://<your-app>.up.railway.app/healthz` 접속하여 `status: ok` 확인.
