import unittest
import json
from flask import Flask, session
from app import create_app
from app.config import Config
from app.models.database import close_db

class TestGoal5ProductionArchitecture(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        close_db()

    def test_healthz_endpoint(self):
        """1. /healthz 엔드포인트가 200 OK와 DB 상태 healthy를 반환하는지 검증"""
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("database"), "healthy")

    def test_security_response_headers(self):
        """2. 모든 HTTP 응답에 보안 헤더가 올바르게 주입되는지 검증"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(response.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")
        self.assertIn("default-src 'self'", response.headers.get("Content-Security-Policy", ""))

    def test_public_routes_accessible_without_auth(self):
        """3. 공개 모의고사 및 개념 영역은 인증 없이 누구나 접근 가능한지 검증"""
        # 홈
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        # 개념 목록
        res = self.client.get("/concepts")
        self.assertEqual(res.status_code, 200)
        # 개념 상세
        res = self.client.get("/concepts/CON-NET-01")
        self.assertEqual(res.status_code, 200)
        # 표준 모의고사
        res = self.client.get("/exam?mode=standard")
        self.assertEqual(res.status_code, 200)
        # 랜덤 모의고사
        res = self.client.get("/exam?mode=random")
        self.assertEqual(res.status_code, 200)

    def test_hybrid_mode_when_admin_key_configured(self):
        """4. ADMIN_ACCESS_KEY 설정 시 개인 학습 영역 보호 및 로그인/로그아웃 라이프사이클 검증"""
        # ADMIN_ACCESS_KEY가 활성화된 별도 앱 인스턴스 생성
        class ProtectedConfig(Config):
            TESTING = True
            ADMIN_ACCESS_KEY = "test-master-passphrase-2026"

        p_app = create_app(ProtectedConfig)
        p_client = p_app.test_client()

        try:
            # A. 비인증 상태에서 /history, /wrong-notes, /dashboard 접근 시 리다이렉트
            res = p_client.get("/history")
            self.assertEqual(res.status_code, 302)
            self.assertIn("/admin-login", res.headers.get("Location"))

            res = p_client.get("/wrong-notes")
            self.assertEqual(res.status_code, 302)
            self.assertIn("/admin-login", res.headers.get("Location"))

            res = p_client.get("/dashboard")
            self.assertEqual(res.status_code, 302)
            self.assertIn("/admin-login", res.headers.get("Location"))

            # B. 로그인 페이지 렌더링 검증
            login_page = p_client.get("/admin-login")
            self.assertEqual(login_page.status_code, 200)
            self.assertIn("관리자 / 개인 학습 데이터", login_page.get_data(as_text=True))

            # CSRF 토큰 추출
            with p_client.session_transaction() as sess:
                csrf_token = sess.get("csrf_token")

            # C. 잘못된 패스프레이즈 입력 시 실패
            fail_res = p_client.post("/admin-login", data={
                "access_key": "wrong-password",
                "csrf_token": csrf_token,
                "next": "/dashboard"
            })
            self.assertEqual(fail_res.status_code, 200)
            self.assertIn("일치하지 않습니다", fail_res.get_data(as_text=True))

            # D. 올바른 패스프레이즈 입력 시 로그인 성공
            success_res = p_client.post("/admin-login", data={
                "access_key": "test-master-passphrase-2026",
                "csrf_token": csrf_token,
                "next": "/dashboard"
            })
            self.assertEqual(success_res.status_code, 302)
            self.assertIn("/dashboard", success_res.headers.get("Location"))

            # E. 로그인 완료 후 보호 영역 정상 접근 확인
            res_history = p_client.get("/history")
            self.assertEqual(res_history.status_code, 200)

            res_wrong = p_client.get("/wrong-notes")
            self.assertEqual(res_wrong.status_code, 200)

            res_dashboard = p_client.get("/dashboard")
            self.assertEqual(res_dashboard.status_code, 200)

            # F. 로그아웃 수행
            logout_res = p_client.post("/admin-logout", data={"csrf_token": csrf_token})
            self.assertEqual(logout_res.status_code, 302)

            # G. 로그아웃 후 다시 접근 차단 확인
            after_logout = p_client.get("/dashboard")
            self.assertEqual(after_logout.status_code, 302)
            self.assertIn("/admin-login", after_logout.headers.get("Location"))

        finally:
            close_db()

    def test_postgres_url_normalization(self):
        """5. Railway의 postgres:// URL이 SQLAlchemy 표준 postgresql:// 로 안전하게 치환되는지 검증"""
        import os
        orig = os.environ.get("DATABASE_URL")
        try:
            os.environ["DATABASE_URL"] = "postgres://user:pass@host:5432/dbname"
            from importlib import reload
            import app.config
            reload(app.config)
            self.assertTrue(app.config.Config.SQLALCHEMY_DATABASE_URI.startswith("postgresql://"))
        finally:
            if orig is not None:
                os.environ["DATABASE_URL"] = orig
            else:
                os.environ.pop("DATABASE_URL", None)
            from importlib import reload
            import app.config
            reload(app.config)

    def test_production_cookie_and_proxyfix_configuration(self):
        """6. 프로덕션 환경 플래그 활성화 시 쿠키 보안 플래그와 ProxyFix가 정상 적용되는지 검증"""
        class ProdConfig(Config):
            TESTING = True
            FLASK_ENV = "production"
            IS_PRODUCTION = True
            USE_PROXYFIX = True
            SESSION_COOKIE_SECURE = True
            SESSION_COOKIE_HTTPONLY = True
            SESSION_COOKIE_SAMESITE = "Lax"

        prod_app = create_app(ProdConfig)
        self.assertTrue(prod_app.config["SESSION_COOKIE_SECURE"])
        self.assertTrue(prod_app.config["SESSION_COOKIE_HTTPONLY"])
        self.assertEqual(prod_app.config["SESSION_COOKIE_SAMESITE"], "Lax")
        close_db()

if __name__ == "__main__":
    unittest.main()
