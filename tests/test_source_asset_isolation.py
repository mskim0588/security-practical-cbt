import unittest
import os
import json
import subprocess
from app.services.data_loader import DataLoader

class TestSourceAssetIsolation(unittest.TestCase):
    """Goal 5B: Automated Copyright & Source Asset Isolation Gate Tests"""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.forbidden_exts = {'.pdf', '.hwp', '.hwpx', '.doc', '.docx', '.ppt', '.pptx', '.epub', '.ocr', '.dump'}

    def test_01_no_raw_source_documents_in_repository(self):
        """1. 저장소 작업 트리 내 원본 소스 문서(PDF, HWP, DOCX 등)가 존재하지 않는지 전수 검증"""
        found_forbidden = []
        for root, dirs, files in os.walk(self.repo_root):
            if any(ignored in root for ignored in ['.git', '.venv', 'venv', '__pycache__']):
                continue
            for f in files:
                _, ext = os.path.splitext(f.lower())
                if ext in self.forbidden_exts:
                    found_forbidden.append(os.path.join(root, f))
        
        self.assertEqual(len(found_forbidden), 0,
                         f"저장소 내에 비인가 원본 문서가 발견되었습니다: {found_forbidden}")

    def test_02_git_tracked_files_have_zero_source_binaries(self):
        """2. Git에 추적(tracked)되는 파일 중 소스 바이너리 문서가 0건인지 검증"""
        try:
            res = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            tracked_files = res.stdout.splitlines()
            tracked_forbidden = [f for f in tracked_files if os.path.splitext(f.lower())[1] in self.forbidden_exts]
            self.assertEqual(len(tracked_forbidden), 0,
                             f"Git에 추적 중인 원본 문서 바이너리가 발견되었습니다: {tracked_forbidden}")
        except FileNotFoundError:
            self.skipTest("git command not available in test environment")

    def test_03_static_directory_isolation(self):
        """3. app/static/ 정적 디렉토리에 원본 문서 및 비인가 텍스트 덤프가 노출되지 않는지 검증"""
        static_dir = os.path.join(self.repo_root, 'app', 'static')
        allowed_static_exts = {'.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.ico', '.woff', '.woff2'}
        
        unauthorized_static = []
        for root, dirs, files in os.walk(static_dir):
            for f in files:
                ext = os.path.splitext(f.lower())[1]
                if ext not in allowed_static_exts or ext in self.forbidden_exts:
                    unauthorized_static.append(os.path.join(root, f))
        
        self.assertEqual(len(unauthorized_static), 0,
                         f"정적 서빙 디렉토리에 비인가 파일이 노출되었습니다: {unauthorized_static}")

    def test_04_app_runtime_zero_pdf_ocr_dependency(self):
        """4. app/ 프로덕션 런타임 코드 내 PDF/OCR 패키지 의존성(pypdf, pytesseract 등)이 0건인지 검증"""
        app_dir = os.path.join(self.repo_root, 'app')
        disallowed_imports = ['pypdf', 'pdfminer', 'fitz', 'pytesseract', 'easyocr']
        
        found_dependencies = []
        for root, dirs, files in os.walk(app_dir):
            for f in files:
                if f.endswith('.py'):
                    fp = os.path.join(root, f)
                    with open(fp, 'r', encoding='utf-8') as fh:
                        for idx, line in enumerate(fh, 1):
                            line_strip = line.strip()
                            for pkg in disallowed_imports:
                                if line_strip.startswith(f'import {pkg}') or line_strip.startswith(f'from {pkg}'):
                                    found_dependencies.append(f"{f}:{idx} -> {line_strip}")
        
        self.assertEqual(len(found_dependencies), 0,
                         f"프로덕션 앱 코드 내 비인가 소스 파서 의존성이 발견되었습니다: {found_dependencies}")

    def test_05_sources_json_pure_bibliographic_metadata(self):
        """5. sources.json이 원문 덤프나 개인 로컬 절대 경로 없이 순수 서지 인용 메타데이터만 보유하는지 검증"""
        loader = DataLoader()
        sources = loader.load_sources()
        self.assertEqual(len(sources), 12, "sources.json에는 12개 출처 메타데이터가 등록되어야 합니다.")

        forbidden_path_substrings = ['g:\\', 'g:/', 'c:\\users', '내 드라이브']
        allowed_keys = {"id", "filename", "title", "source_type", "subject", "role", "group", "priority", "total_pages", "description"}

        for s in sources:
            self.assertTrue(set(s.keys()).issubset(allowed_keys),
                            f"Source {s.get('id')}에 비인가 필드가 존재합니다: {set(s.keys()) - allowed_keys}")
            
            # 필드 값 내 로컬 경로 포함 여부 검증
            for k, v in s.items():
                if isinstance(v, str):
                    for sub in forbidden_path_substrings:
                        self.assertNotIn(sub, v.lower(),
                                         f"Source {s.get('id')} 필드 '{k}'에 로컬 절대 경로가 누설되었습니다: {v}")
                    # 원문 대량 덤프 방지 (개별 필드 길이 500자 이하 검증)
                    self.assertLess(len(v), 500,
                                    f"Source {s.get('id')} 필드 '{k}'의 길이가 비정상적으로 깁니다 ({len(v)}자).")

    def test_06_gitignore_rules_enforce_isolation(self):
        """6. .gitignore에 원본 문서 격리 규칙(*.pdf, private_sources/ 등)이 명시되어 있는지 검증"""
        gitignore_path = os.path.join(self.repo_root, '.gitignore')
        self.assertTrue(os.path.exists(gitignore_path), ".gitignore 파일이 존재해야 합니다.")

        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_patterns = ['*.pdf', 'private_sources/', 'source_materials/', 'local_references/']
        for pattern in required_patterns:
            self.assertIn(pattern, content, f".gitignore에 필수 격리 패턴 '{pattern}'이 누락되었습니다.")

    def test_07_learning_content_integrity_and_isolation(self):
        """7. 180문항, 180해설, 20개념서의 구조적 완결성 및 독자 창작 메타데이터 검증"""
        loader = DataLoader()
        questions = loader.load_questions()
        explanations = loader.load_explanations()
        concepts = loader.load_concepts()
        concept_contents = loader.load_concept_contents()

        self.assertEqual(len(questions), 180, "문제 수는 180이어야 합니다.")
        self.assertEqual(len(explanations), 180, "해설 수는 180이어야 합니다.")
        self.assertEqual(len(concepts), 20, "개념 메타 수는 20이어야 합니다.")
        self.assertEqual(len(concept_contents), 20, "개념 콘텐츠 수는 20이어야 합니다.")

        # 모든 질문에 대응하는 해설이 정확히 1:1 매핑되는지 검증
        for q in questions:
            self.assertIn(q['id'], explanations, f"문제 {q['id']}에 대응하는 해설이 누락되었습니다.")

        # 모든 개념에 대응하는 콘텐츠가 정확히 1:1 매핑되는지 검증
        for c in concepts:
            self.assertIn(c['id'], concept_contents, f"개념 {c['id']}에 대응하는 콘텐츠가 누락되었습니다.")

    def test_08_no_hardcoded_personal_paths_in_tracked_code(self):
        """8. app/, tests/, scripts/ 내 파이썬 코드에 개인 로컬 절대경로가 하드코딩되지 않았는지 전수 검증"""
        target_dirs = ['app', 'tests', 'scripts']
        forbidden_substrings = ['g:\\내 드라이브', 'g:/내 드라이브', 'c:\\users\\mskim']

        found_leaks = []
        for tdir in target_dirs:
            full_dir = os.path.join(self.repo_root, tdir)
            if not os.path.exists(full_dir):
                continue
            for root, dirs, files in os.walk(full_dir):
                if any(ignored in root for ignored in ['__pycache__']):
                    continue
                for f in files:
                    if f.endswith('.py') and f != 'test_source_asset_isolation.py':
                        fp = os.path.join(root, f)
                        with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                            for idx, line in enumerate(fh, 1):
                                line_lower = line.lower()
                                for sub in forbidden_substrings:
                                    if sub in line_lower:
                                        found_leaks.append(f"{f}:{idx} -> {line.strip()}")

        self.assertEqual(len(found_leaks), 0,
                         f"추적 파이썬 코드 내 개인 절대경로가 발견되었습니다: {found_leaks}")

if __name__ == '__main__':
    unittest.main()
