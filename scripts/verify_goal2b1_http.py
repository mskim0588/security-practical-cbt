import urllib.request
import urllib.parse
import json

def test_http_flows():
    # 1. 홈 화면 확인
    req_home = urllib.request.Request('http://127.0.0.1:5000/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_home) as resp:
        assert resp.status == 200
        html = resp.read().decode('utf-8')
        assert "12개" in html
        assert "18문제" in html or "18개" in html
        print("[HTTP] Home page OK (12 sources, 18 questions)")

    # 2. 시험 화면 확인
    req_exam = urllib.request.Request('http://127.0.0.1:5000/exam', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_exam) as resp:
        assert resp.status == 200
        html = resp.read().decode('utf-8')
        assert "Q-SHORT-001" in html
        assert "Q-SHORT-012" in html
        assert "Q-DESC-001" in html
        assert "Q-PRAC-001" in html
        print("[HTTP] Exam page OK")

    # 3. 제출 및 채점 플로우 확인 (strict 및 normalized 동작 확인)
    post_data = urllib.parse.urlencode({
        'selected_practical_id': 'Q-PRAC-001',
        # Q-SHORT-001 (normalized): "위험도 = 자산가치 + (발생가능성 * 법적준거성 * 2)"
        'ans_Q-SHORT-001_A': '침해요인 발생 가능성',
        'ans_Q-SHORT-001_B': '법적 준거성',
        'ans_Q-SHORT-001_C': '2',
        # Q-SHORT-005 (strict): "robots.txt"
        'ans_Q-SHORT-005': 'robots.txt',
        # Q-SHORT-008 (strict): "/proc"
        'ans_Q-SHORT-008': '  /proc  ',  # trim 허용 확인
        # Q-SHORT-011 (strict): HTTPERR, DHCP
        'ans_Q-SHORT-011_A': 'HTTPERR',
        'ans_Q-SHORT-011_B': 'DHCP',
    }).encode('utf-8')

    req_submit = urllib.request.Request('http://127.0.0.1:5000/submit', data=post_data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_submit) as resp:
        assert resp.status == 200
        html = resp.read().decode('utf-8')
        assert "채점 결과" in html
        assert "100" in html
        print("[HTTP] Submit & Scoring flow OK")

if __name__ == '__main__':
    test_http_flows()
    print("ALL HTTP FLOWS VERIFIED SUCCESSFULLY!")
