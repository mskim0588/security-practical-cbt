import os
import sys
import json
import pypdf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.expand_questions import EXPANDED_SHORT, EXPANDED_DESC, EXPANDED_PRAC

with open('app/data/sources.json', encoding='utf-8') as f:
    sources = json.load(f)
source_map = {s['id']: s for s in sources}

pdf_dir = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"

# Load all PDF readers
readers = {}
for sid, sinfo in source_map.items():
    fn = sinfo['filename']
    fp = os.path.join(pdf_dir, fn)
    if os.path.exists(fp):
        readers[sid] = pypdf.PdfReader(fp)
    else:
        print(f"File not found: {fp}")

def audit_question(q):
    qid = q['id']
    sid = q['source_id']
    spage = q['source_page']
    
    if sid not in readers:
        return False, f"Reader not found for {sid}"
    
    reader = readers[sid]
    total_pages = len(reader.pages)
    if spage < 1 or spage > total_pages:
        return False, f"Invalid page {spage} (total {total_pages})"
    
    # 0-indexed page in pypdf
    page_text = reader.pages[spage - 1].extract_text() or ""
    
    # Find key tokens from question / answer
    if q.get('answer'):
        ans_tokens = [q['answer']]
    elif q.get('sub_questions'):
        ans_tokens = [sq.get('answer') or sq.get('model_answer', '')[:10] for sq in q['sub_questions'] if sq.get('answer') or sq.get('model_answer')]
    else:
        ans_tokens = []
        
    # Check if any answer token or distinctive question phrase appears on page
    found_on_page = False
    matched_token = None
    for token in ans_tokens:
        if token and len(token) >= 2 and token.lower() in page_text.lower():
            found_on_page = True
            matched_token = token
            break
            
    if not found_on_page:
        # Check title / tags / question keywords
        tags = q.get('tags', [])
        for tag in tags:
            if tag and len(tag) >= 2 and tag.lower() in page_text.lower():
                found_on_page = True
                matched_token = f"tag:{tag}"
                break

    if found_on_page:
        return True, f"Matched on page {spage}: {matched_token}"
    else:
        # Search nearby pages (+- 5 pages)
        nearby_found = []
        for offset in range(-5, 6):
            if offset == 0:
                continue
            target_p = spage + offset
            if 1 <= target_p <= total_pages:
                t_text = reader.pages[target_p - 1].extract_text() or ""
                for token in ans_tokens:
                    if token and len(token) >= 2 and token.lower() in t_text.lower():
                        nearby_found.append((target_p, token))
                        break
        return False, f"Not on page {spage}. Nearby candidates: {nearby_found}"

print("=== Auditing Expanded Questions ===")
all_expanded = EXPANDED_SHORT + EXPANDED_DESC + EXPANDED_PRAC
success_count = 0
fail_list = []

for q in all_expanded:
    ok, msg = audit_question(q)
    if ok:
        success_count += 1
        print(f"[OK] {q['id']} ({q['source_id']} p.{q['source_page']}) -> {msg}")
    else:
        fail_list.append((q, msg))
        print(f"[FAIL] {q['id']} ({q['source_id']} p.{q['source_page']}) -> {msg}")

print(f"\nTotal: {len(all_expanded)}, Verified OK: {success_count}, Needs Correction: {len(fail_list)}")
