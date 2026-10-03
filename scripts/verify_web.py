import urllib.request
import urllib.parse
import re

base_url = "http://127.0.0.1:5000"

# 1. Index
html = urllib.request.urlopen(base_url + "/").read().decode("utf-8")
summary_boxes = re.findall(r'<div style="font-size: 22px; font-weight: 800;[^>]*>(.*?)</div>', html)
print("Index Summary numbers:", summary_boxes)

# 2. Random mode with seed=123 (reproducible)
res1 = urllib.request.urlopen(base_url + "/exam?mode=random&seed=123").read().decode("utf-8")
res2 = urllib.request.urlopen(base_url + "/exam?mode=random&seed=123").read().decode("utf-8")
qids1 = re.search(r'name="question_ids" value="([^"]+)"', res1).group(1)
qids2 = re.search(r'name="question_ids" value="([^"]+)"', res2).group(1)
print("Seed=123 deterministic match:", qids1 == qids2)
print("Contains seed badge '시험 Seed: 123':", "시험 Seed: 123" in res1)

# 3. Random mode with seed=456 (different)
res3 = urllib.request.urlopen(base_url + "/exam?mode=random&seed=456").read().decode("utf-8")
qids3 = re.search(r'name="question_ids" value="([^"]+)"', res3).group(1)
print("Seed=123 vs Seed=456 different:", qids1 != qids3)

# 4. Random mode with invalid seed (fallback, no 500)
res_inv = urllib.request.urlopen(base_url + "/exam?mode=random&seed=invalid_abc").read().decode("utf-8")
print("Invalid seed handled safely (status 200, no seed badge):", "시험 Seed:" not in res_inv and "랜덤 실전 모의고사" in res_inv)

# 5. Submit random exam
random_qids = qids1.split(",")
print("Random exam questions count:", len(random_qids))
prac_id = random_qids[-1] # pick last practical question
submit_data = urllib.parse.urlencode({
    "question_ids": qids1,
    "exam_mode": "random",
    "selected_practical_id": prac_id,
    f"ans_{random_qids[0]}": "테스트답안"
}).encode("utf-8")

req = urllib.request.Request(base_url + "/submit", data=submit_data)
submit_html = urllib.request.urlopen(req).read().decode("utf-8")
print("Random exam submit status: Success, score card rendered:", "정보보안기사 실기 모의고사 채점 결과" in submit_html)
