"""Goal 9A navigation destinations, visibility, and preserved access controls."""

import re
import unittest

from app import create_app
from app.config import Config
from app.models.database import close_db


class NavigationConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    ADMIN_ACCESS_KEY = "navigation-test-owner-key"


def nav_html(html, class_name):
    start = html.index(f'<nav class="{class_name}"')
    return html[start:html.index('</nav>', start)]


class Goal9ANavigationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(NavigationConfig)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            close_db()

    def owner(self):
        with self.client.session_transaction() as session:
            session['is_admin'] = True

    def test_guest_primary_and_utility_destinations(self):
        html = self.client.get('/').get_data(as_text=True)
        desktop = nav_html(html, 'nav-desktop')
        mobile = nav_html(html, 'nav-mobile-bottom')
        self.assertEqual(re.findall(r'<a href="([^"]+)" class="nav-desktop-link', desktop),
                         ['/', '/exam', '/concepts'])
        self.assertEqual(re.findall(r'<a href="([^"]+)" class="nav-mobile-item', mobile),
                         ['/', '/exam', '/concepts'])
        self.assertNotIn('>내 학습</summary>', desktop + mobile)
        for path in ('/search', '/bookmarks', '/practice', '/descriptive-training',
                     '/mock-exam', '/admin-login'):
            self.assertIn(f'href="{path}"', desktop)
            self.assertIn(f'href="{path}"', mobile)
            self.assertEqual(self.client.get(path).status_code, 200, path)
        for path in ('/dashboard', '/history', '/wrong-notes', '/law-freshness'):
            self.assertNotIn(f'href="{path}"', desktop + mobile)
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302, path)
            self.assertIn('/admin-login', response.headers['Location'])

    def test_owner_my_learning_destinations_and_logout(self):
        self.owner()
        html = self.client.get('/').get_data(as_text=True)
        desktop = nav_html(html, 'nav-desktop')
        mobile = nav_html(html, 'nav-mobile-bottom')
        self.assertEqual(re.findall(r'<a href="([^"]+)" class="nav-desktop-link', desktop),
                         ['/', '/exam', '/concepts'])
        self.assertIn('>내 학습</summary>', desktop)
        self.assertIn('내 학습</span>', mobile)
        for nav in (desktop, mobile):
            for path in ('/dashboard', '/history', '/wrong-notes', '/bookmarks'):
                self.assertIn(f'href="{path}"', nav)
            self.assertIn('href="/search"', nav)
            self.assertIn('href="/law-freshness"', nav)
            self.assertIn('action="/admin-logout"', nav)
            self.assertNotIn('href="/admin-login"', nav)
        for path in ('/dashboard', '/history', '/wrong-notes', '/bookmarks', '/law-freshness'):
            self.assertEqual(self.client.get(path).status_code, 200, path)
        self.assertEqual(self.client.post('/admin-logout').status_code, 403)
        with self.client.session_transaction() as session:
            token = session['csrf_token']
        self.assertEqual(self.client.post('/admin-logout', data={'csrf_token': token}).status_code, 302)
        self.assertEqual(self.client.get('/history').status_code, 302)

    def test_active_state_on_primary_and_grouped_destinations(self):
        self.owner()
        for path, snippet in (
            ('/', 'href="/" class="nav-desktop-link is-active" aria-current="page"'),
            ('/exam', 'href="/exam" class="nav-desktop-link is-active" aria-current="page"'),
            ('/concepts', 'href="/concepts" class="nav-desktop-link is-active" aria-current="page"'),
            ('/history', 'href="/history" class="nav-menu-link is-active" aria-current="page"'),
            ('/bookmarks', 'href="/bookmarks" class="nav-menu-link is-active" aria-current="page"'),
            ('/search', 'href="/search" class="nav-menu-link is-active" aria-current="page"'),
        ):
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                self.assertIn(snippet, nav_html(html, 'nav-desktop'))
        guest = self.app.test_client().get('/bookmarks').get_data(as_text=True)
        self.assertIn('class="nav-desktop-link is-active" aria-expanded="false">더보기',
                      nav_html(guest, 'nav-desktop'))

    def test_active_exam_navigation_does_not_expose_learning_utilities(self):
        self.owner()
        html = self.client.get('/exam').get_data(as_text=True)
        desktop = nav_html(html, 'nav-desktop')
        self.assertNotIn('href="/search"', desktop)
        self.assertNotIn('href="/bookmarks"', desktop)
        self.assertNotIn('>내 학습</summary>', desktop)
        self.assertNotIn('nav-mobile-bottom', html)
        self.assertNotIn('js/navigation.js', html)


if __name__ == '__main__':
    unittest.main()
