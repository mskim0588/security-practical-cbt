# 정보보안기사 실기시험 실전 CBT 웹 애플리케이션 (MVP)

정보보안기사 실기시험을 실제 시험 환경과 유사하게 연습하고 자동 평가받을 수 있는 CBT(Computer Based Test) 웹 애플리케이션입니다.

---

## 🎯 시험 규격 및 구성

- **총 문항 수**: 18개 후보 문항 제시 / **17문항 채점**
- **총점**: **100점 만점** (합격 기준: 60점 이상)

| 시험 영역 | 제시 문항 | 채점 문항 | 배점 | 채점 방식 |
|---|:---:|:---:|:---:|---|
| **제1영역 (단답형)** | 12문제 | 12문제 | 문제당 3점 (총 36점) | 대소문자/공백 정규화, accepted_answers 복수 정답 자동채점 |
| **제2영역 (서술형)** | 4문제 | 4문제 | 문제당 12점 (총 48점) | 핵심 키워드군 매칭 기반 루브릭 부분점수 채점 |
| **제3영역 (실무형)** | 2문제 | **1문제 선택** | 선택 문제 16점 (총 16점) | 텍스트/루브릭 기반 부분점수 채점 (미선택 문항 제외) |
| **합계** | **18문제** | **17문제** | **총 100점** | 합격 여부(60점) 판정 |

---

## 🚀 빠른 시작

### 1. 패키지 설치
Python 3.10 이상 환경에서 Flask를 설치합니다:
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python run.py
```
브라우저에서 `http://127.0.0.1:5000`으로 접속합니다.

### 3. 자동화 테스트 실행
```bash
python -m unittest discover tests
```

---

## 📁 프로젝트 구조

```
security-practical-cbt/
├── app/
│   ├── config.py                 # 환경설정
│   ├── data/                     # JSON 데이터베이스
│   │   ├── questions.json        # 18개 문항 (단답 12, 서술 4, 실무 2)
│   │   ├── sources.json          # PDF 출처 메타데이터
│   │   └── concepts.json         # 핵심 보안 개념 메타데이터
│   ├── routes/
│   │   ├── main_routes.py        # 홈 화면 (/)
│   │   └── exam_routes.py        # 응시(/exam), 검토(/review), 채점/결과(/submit)
│   ├── services/
│   │   ├── data_loader.py        # JSON 데이터 로더 및 정합성 검증
│   │   ├── exam_service.py       # 시험 세션 및 폼 데이터 파싱
│   │   └── grader.py             # 3대 채점 엔진 (단답 정규화, 서술 루브릭, 실무 택1)
│   ├── static/
│   │   ├── css/style.css         # 모던 CBT 스타일시트
│   │   └── js/exam.js            # 실무형 택1 인터랙션 및 문항 네비게이터
│   └── templates/
│       ├── base.html             # 기본 레이아웃
│       ├── index.html            # 홈 화면
│       ├── exam.html             # 시험 응시 화면
│       ├── review.html           # 제출 전 답안 검토 화면
│       └── result.html           # 결과 리포트 및 출처/해설 화면
├── tests/
│   ├── test_data.py              # 데이터 무결성 및 배점(100점) 테스트
│   ├── test_grader.py            # 채점 엔진 단위 테스트
│   └── test_routes.py            # E2E 웹 라우트 테스트
├── requirements.txt
├── run.py
└── README.md
```

---

## 📖 출처 인용 및 원천 자산 격리 정책 (Source Asset Policy)

본 프로젝트는 원본 자료의 저장소/배포 격리 및 기술적 위생 기준을 엄격히 준수합니다.

- **외부 원본 문서 격리**: 원본 PDF, 상용 교재, 수험 요약본 등 원문 바이너리 문서는 본 저장소 및 프로덕션 환경에 절대 포함되지 않습니다 (Zero Raw Asset Tracking).
- **서지 인용 메타데이터**: 애플리케이션 내의 출처 표기(`sources.json`)는 검증을 위한 서지 정보(파일명, 인용 페이지 번호)만을 포함하며, 원문 텍스트나 바이너리를 내포하지 않습니다.
- **콘텐츠 분류 (Provenance)**: 180문항에 대한 해설(`explanations.json`)과 20개 개념서(`concept_contents.json`)는 공개 기술 표준(RFC, NIST, OWASP, KISA 가이드라인)을 바탕으로 프로젝트 전용으로 작성되었습니다.

> **[참고]** 본 검증은 원본 Source Asset의 Repository/Production 격리 여부와 콘텐츠 provenance를 기술적으로 검증한 것이며, 개별 콘텐츠의 법적 이용 허가 또는 공정이용 해당 여부를 확정하는 법률 검토를 의미하지 않습니다.

상세 격리 정책 및 기술 감사 결과는 [docs/SOURCE_ASSET_POLICY.md](docs/SOURCE_ASSET_POLICY.md)를 참조하십시오.
