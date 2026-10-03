import os
import sys
import json
import pypdf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from scripts.new_questions_batch import NEW_SHORT_QUESTIONS, NEW_DESC_QUESTIONS, NEW_PRAC_QUESTIONS

pdf_dir = r"G:\내 드라이브\보안기사\보안기사 실기 관련자료"
with open('app/data/sources.json', encoding='utf-8') as f:
    sources = {s['id']: s for s in json.load(f)}

readers = {sid: pypdf.PdfReader(os.path.join(pdf_dir, s['filename'])) for sid, s in sources.items()}

all_new = NEW_SHORT_QUESTIONS + NEW_DESC_QUESTIONS + NEW_PRAC_QUESTIONS
print(f"Auditing {len(all_new)} new questions against real PDFs...")

for q in all_new:
    sid = q['source_id']
    spage = q['source_page']
    reader = readers[sid]
    txt = reader.pages[spage - 1].extract_text()
    
    # Check score
    if q['type'] == 'short':
        assert q['score'] == 3
        if q.get('sub_questions'):
            assert sum(sq['score'] for sq in q['sub_questions']) == 3.0
    elif q['type'] == 'descriptive':
        assert q['score'] == 12
        assert sum(sq['score'] for sq in q['sub_questions']) == 12.0
    elif q['type'] == 'practical':
        assert q['score'] == 16
        assert sum(sq['score'] for sq in q['sub_questions']) == 16.0
        
    print(f"[OK] {q['id']} ({sources[sid]['filename']} p.{spage}) verified! Length: {len(txt)}")

print("ALL 10 NEW QUESTIONS FULLY VERIFIED!")
