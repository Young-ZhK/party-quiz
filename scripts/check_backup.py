
import json
import os

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups', 'questions.json.backup_20260423_161505')
with open(path, 'r', encoding='utf-8') as f:
    qs = json.load(f)

count = {}
for q in qs:
    s = q.get('set', '?')
    count[s] = count.get(s, 0) + 1

print(f'备份文件题数: {len(qs)}')
print('各套题数:', count)
