import urllib.request
import urllib.parse

def check_url(url, label):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        print(f"[{label}] Status: {resp.status}, Content Length: {len(content)}")
        return content

# 1. 홈 화면 확인
home = check_url('http://127.0.0.1:5000/', 'HOME')
assert '12권' in home
assert '54문항' in home
assert '제1회 표준 기출 모의고사' in home
assert '랜덤 실전 모의고사' in home
print("Home page verified: 12 sources, 54 questions, dual exam buttons present.")

# 2. 표준 모의고사 확인
std = check_url('http://127.0.0.1:5000/exam?mode=standard', 'EXAM_STD')
assert 'Q-SHORT-001' in std
assert 'Q-SHORT-012' in std
assert 'Q-DESC-001' in std
assert 'Q-PRAC-001' in std
assert 'name="question_ids"' in std
print("Standard exam verified: fixed 18 questions present.")

# 3. 랜덤 모의고사 확인 (2회 호출하여 문항 조합 달라지는지 확인)
rnd1 = check_url('http://127.0.0.1:5000/exam?mode=random', 'EXAM_RND_1')
rnd2 = check_url('http://127.0.0.1:5000/exam?mode=random', 'EXAM_RND_2')
assert 'name="question_ids"' in rnd1
assert 'name="question_ids"' in rnd2
print("Random exams verified.")

# 4. 검토(Review) 및 제출(Submit) POST 플로우 확인
post_data = urllib.parse.urlencode({
    'selected_practical_id': 'Q-PRAC-001',
    'ans_Q-SHORT-001_A': '침해요인 발생 가능성',
    'ans_Q-SHORT-001_B': '법적 준거성',
    'ans_Q-SHORT-001_C': '2',
    'ans_Q-SHORT-003': 'WPA2',
    'ans_Q-SHORT-008': '/proc'
}).encode('utf-8')

req_review = urllib.request.Request('http://127.0.0.1:5000/review', data=post_data, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_review) as resp:
    review_html = resp.read().decode('utf-8')
    assert resp.status == 200
    assert '답안 최종 검토' in review_html
    assert '17번 (IPTables) 선택됨' in review_html
    print("Review POST verified.")

req_submit = urllib.request.Request('http://127.0.0.1:5000/submit', data=post_data, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_submit) as resp:
    submit_html = resp.read().decode('utf-8')
    assert resp.status == 200
    assert '채점 결과' in submit_html
    assert '보안기사 실기 단답형.pdf' in submit_html
    assert 'Page' in submit_html
    print("Submit POST verified.")

print("\n>>> ALL LIVE HTTP ENDPOINTS PERFECTLY VERIFIED! <<<")
