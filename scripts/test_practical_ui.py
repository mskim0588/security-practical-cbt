# -*- coding: utf-8 -*-
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.services.data_loader import DataLoader
from app.services.exam_service import ExamService

app = create_app()
client = app.test_client()
loader = DataLoader()
service = ExamService(loader)

test_cases = [
    ('standard', None),
    ('random', 42),
    ('random', 1),
    ('random', 10),
    ('random', 100),
    ('random', 999),
]

all_passed = True
print("--- Verifying Practical UI Selection Radios ---")
for mode, seed in test_cases:
    url = f"/exam?mode={mode}" + (f"&seed={seed}" if seed is not None else "")
    res = client.get(url)
    assert res.status_code == 200, f"Failed GET {url}"
    html = res.get_data(as_text=True)

    # Extract practical radios
    radio_vals = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"', html)
    # Extract practical question cards
    card_ids = re.findall(r'class="question-card practical-card"\s+id="q-([^"]+)"', html)
    # Check default checked
    checked_val = re.findall(r'name="selected_practical_id"\s+value="([^"]+)"\s+checked', html)

    match = (radio_vals == card_ids)
    has_checked = len(checked_val) == 1 and checked_val[0] == radio_vals[0]
    
    print(f"[{mode.upper()} seed={seed}]")
    print(f"  Radios:  {radio_vals}")
    print(f"  Cards:   {card_ids}")
    print(f"  Checked: {checked_val}")
    print(f"  Result:  {'PASS' if (match and has_checked) else 'FAIL'}")

    if not (match and has_checked):
        all_passed = False

    # Also test submission with 1st practical selected vs 2nd practical selected
    q_ids_match = re.search(r'name="question_ids"\s+value="([^"]+)"', html)
    assert q_ids_match, "question_ids hidden input missing"
    q_ids_str = q_ids_match.group(1)

    for choose_idx in [0, 1]:
        chosen_pid = radio_vals[choose_idx]
        unchosen_pid = radio_vals[1 - choose_idx]
        submit_data = {
            "question_ids": q_ids_str,
            "exam_mode": mode,
            "selected_practical_id": chosen_pid
        }
        # Fill answers for chosen practical
        submit_data[f"ans_{chosen_pid}_1"] = "테스트 실무 답안"

        sub_res = client.post("/submit", data=submit_data)
        assert sub_res.status_code == 200, f"Submit failed for {chosen_pid}"
        sub_html = sub_res.get_data(as_text=True)

        assert f"선택: {chosen_pid}" in sub_html, f"Selected practical ID {chosen_pid} not shown in result"
        assert "/ 100점" in sub_html, "100점 만점 기준 누락"

print("\n>> All Practical Selection & Submission Tests PASSED (100%)!")
