# -*- coding: utf-8 -*-
import sys
import pypdf
import re

sys.stdout.reconfigure(encoding='utf-8')

reader = pypdf.PdfReader(r'G:\내 드라이브\보안기사\보안기사 실기 관련자료\3과목.pdf')

def search(term, start=1, end=len(reader.pages)):
    found = []
    term_clean = term.lower().replace(' ', '')
    for i in range(start - 1, min(end, len(reader.pages))):
        txt = reader.pages[i].extract_text() or ''
        txt_clean = txt.lower().replace(' ', '')
        if term_clean in txt_clean:
            found.append(i + 1)
    return found

print("프록시도구:", search("프록시도구", 80, 180))
print("추론:", search("추론", 230, 250))
print("aggregation:", search("aggregation", 230, 250))
print("부정조작:", search("부정조작", 230, 250))
print("자료변조:", search("자료변조", 230, 250))
print("데이터베이스 보안 위협:", search("위협", 235, 245))

# Let's inspect page 235, 241, 242 text
for p in [235, 241, 242, 243]:
    txt = reader.pages[p - 1].extract_text() or ""
    print(f"\n--- PAGE {p} ---")
    print(txt[:600])
