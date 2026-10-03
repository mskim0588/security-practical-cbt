import json
import re

with open("app/data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Look for overlapping questions
print("=== CROSS QUESTION OVERLAP AUDIT ===")
for i in range(len(questions)):
    for j in range(i + 1, len(questions)):
        q1 = questions[i]
        q2 = questions[j]
        
        # Extract main log or question body
        words1 = set(re.findall(r'[a-zA-Z0-9_\-\./]{4,}', q1["question"]))
        words2 = set(re.findall(r'[a-zA-Z0-9_\-\./]{4,}', q2["question"]))
        common = words1 & words2
        
        # Filter out common stop words
        common = {w for w in common if w.lower() not in {"http", "https", "linux", "server", "access", "다음", "대하여", "설명하시오", "대해"}}
        
        if len(common) >= 3:
            print(f"\nMatch: [{q1['id']}] ({q1['type']}) vs [{q2['id']}] ({q2['type']})")
            print(f"  Common tokens: {common}")
            print(f"  Q1: {q1['question'][:60]}...")
            print(f"  Q2: {q2['question'][:60]}...")
