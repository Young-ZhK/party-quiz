
import json
import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
with open(path, 'r', encoding='utf-8') as f:
    qs = json.load(f)

print(f'总题数: {len(qs)}')

count = {}
for i, q in enumerate(qs):
    s = q['set']
    count[s] = count.get(s, 0) + 1
    if i < 5 or i > len(qs)-6:
        print(f'第{i+1}题: set={s}, type={q["type"]}, answer={q.get("answer")}')

print('\n各套题数:')
for s in sorted(count.keys()):
    print(f'第{s}套: {count[s]}题')
