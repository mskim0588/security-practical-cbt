import os
import sys
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.data_loader import DataLoader

def run_verification():
    loader = DataLoader()
    sources = loader.load_sources()
    questions = loader.load_questions()
    summary = loader.get_sources_summary()

    print("=== [1. Data Layer Verification] ===")
    print(f"Total Sources in sources.json: {len(sources)}")
    assert len(sources) == 12, "sources.json should contain exactly 12 sources."

    source_ids = [s["id"] for s in sources]
    assert len(source_ids) == len(set(source_ids)), "Source IDs must be unique."
    print(f"Source IDs: {source_ids}")

    print(f"Total Questions in questions.json: {len(questions)}")
    assert len(questions) == 18, "questions.json should contain exactly 18 questions."

    usage = loader.get_source_usage_counts()
    print(f"Source Usage Counts: {usage}")
    assert usage.get("SRC-01") == 12, f"Expected 12 for SRC-01, got {usage.get('SRC-01')}"
    assert usage.get("SRC-02") == 4, f"Expected 4 for SRC-02, got {usage.get('SRC-02')}"
    assert usage.get("SRC-03") == 2, f"Expected 2 for SRC-03, got {usage.get('SRC-03')}"
    assert usage.get("SRC-04", 0) == 0, f"Expected 0 for SRC-04, got {usage.get('SRC-04')}"

    assert summary["total_sources"] == 12
    assert summary["active_sources_count"] == 3
    assert summary["total_questions_count"] == 18

    # Check individual status text
    by_id = {s["id"]: s for s in summary["all_sources"]}
    assert by_id["SRC-01"]["status_text"] == "사용 중 · 12문제"
    assert by_id["SRC-02"]["status_text"] == "사용 중 · 4문제"
    assert by_id["SRC-03"]["status_text"] == "사용 중 · 2문제"
    assert by_id["SRC-04"]["status_text"] == "등록됨 · 현재 미사용"
    assert by_id["SRC-05"]["status_text"] == "등록됨 · 현재 미사용"
    print("Data Layer Verification PASSED!")

    print("\n=== [2. Live HTTP Endpoint Verification] ===")
    req = urllib.request.Request("http://127.0.0.1:5000/", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        home_html = resp.read().decode("utf-8")
        assert resp.status == 200

        # Check Summary Metrics
        assert "등록된 학습자료" in home_html
        assert "12개" in home_html
        assert "현재 문제 출처로 사용 중" in home_html
        assert "3개" in home_html
        assert "등록 문제" in home_html
        assert "18개" in home_html

        # Check Collapsible Details Table
        assert "<details" in home_html
        assert "<summary" in home_html
        assert "보안기사 실기 단답형.pdf" in home_html
        assert "사용 중 · 12문제" in home_html
        assert "보안기사 실기 서술형.pdf" in home_html
        assert "사용 중 · 4문제" in home_html
        assert "정보보안기사 실기 서술형 TOP 20.pdf" in home_html
        assert "사용 중 · 2문제" in home_html
        assert "4과목.pdf" in home_html
        assert "등록됨 · 현재 미사용" in home_html
        assert "00. 정보보안기사_실기_요약_v1.0.pdf" in home_html
        assert "정보보안기사 정리_260214.pdf" in home_html
        print("Home Page UI Verification PASSED!")

    # Check Exam & Scoring Flow
    post_data = urllib.parse.urlencode({
        "selected_practical_id": "Q-PRAC-001",
        "ans_Q-SHORT-001_A": "침해요인 발생 가능성",
        "ans_Q-SHORT-001_B": "법적 준거성",
        "ans_Q-SHORT-001_C": "2"
    }).encode("utf-8")

    req_review = urllib.request.Request("http://127.0.0.1:5000/review", data=post_data, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req_review) as resp:
        review_html = resp.read().decode("utf-8")
        assert resp.status == 200
        assert "17번 (IPTables) 선택됨" in review_html
        print("Review Page Verification PASSED!")

    req_submit = urllib.request.Request("http://127.0.0.1:5000/submit", data=post_data, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req_submit) as resp:
        submit_html = resp.read().decode("utf-8")
        assert resp.status == 200
        assert "/ 100점" in submit_html
        assert "출처:" in submit_html
        print("Submit Scoring Verification PASSED!")

    print("\n==========================================")
    print(">>> GOAL 2A ALL 10 CRITERIA FULLY VERIFIED! <<<")
    print("==========================================")

if __name__ == "__main__":
    run_verification()
