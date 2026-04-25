import json
data = json.load(open('questions.json', 'r', encoding='utf-8'))
sets = set(q.get('set') for q in data)
print('题目集:', sets)
print('总数:', len(data))
for s in sorted(sets):
    count = len([q for q in data if q.get('set') == s])
    print(f'第{s}套: {count}题')
