import json

with open('app/data/questions.json', encoding='utf-8') as f:
    qs = json.load(f)

for q in qs:
    if q['source_id'] in ['SRC-02', 'SRC-03']:
        qtext = q['question'].replace('\n', ' ')[:45]
        print(f"{q['id']} ({q['type']}, {q['score']}pt) - {q['source_id']} p.{q['source_page']} [{q['concept_id']}]: {qtext}")
