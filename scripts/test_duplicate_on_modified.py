import json
import re

with open("test_modified_questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

def get_all_text(q):
    t = q["question"] + " "
    if q.get("answer"):
        t += str(q["answer"]) + " "
    if q.get("sub_questions"):
        for s in q["sub_questions"]:
            t += str(s.get("answer", "")) + " "
            t += str(s.get("model_answer", "")) + " "
    return t

tokens_list = []
for q in questions:
    t = get_all_text(q)
    tokens = set(re.findall(r'[가-힣]{2,}|[a-zA-Z0-9_\-\.]{3,}', t.lower()))
    stopwords = {"설명하시오", "기술하시오", "무엇인가", "대하여", "대해", "다음은", "관련하여", "위한", "있는", "하는", "경우", "각각"}
    tokens_list.append(tokens - stopwords)

pairs = []
for i in range(len(questions)):
    for j in range(i + 1, len(questions)):
        s1 = tokens_list[i]
        s2 = tokens_list[j]
        inter = s1 & s2
        union = s1 | s2
        sim = len(inter) / max(len(union), 1)
        if sim > 0.20:
            pairs.append((sim, questions[i], questions[j], inter))

pairs.sort(key=lambda x: x[0], reverse=True)

print(f"=== TOP SIMILAR QUESTION PAIRS ON MODIFIED (Threshold > 0.20) ===")
print(f"Total pairs found: {len(pairs)}")
for sim, q1, q2, inter in pairs:
    print(f"\nSimilarity: {sim:.2f} | [{q1['id']} ({q1['type']})] vs [{q2['id']} ({q2['type']})]")
    print(f"  Q1: {q1['question'][:60].replace(chr(10), ' ')}... (Src: {q1['source_id']} p.{q1['source_page']})")
    print(f"  Q2: {q2['question'][:60].replace(chr(10), ' ')}... (Src: {q2['source_id']} p.{q2['source_page']})")
    print(f"  Shared tokens ({len(inter)}): {list(inter)[:10]}")
