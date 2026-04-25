
import json
import os

# 读取原来的前三套（来自完整备份）
backupPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups', 'questions.json.backup_20260423_161505')
with open(backupPath, 'r', encoding='utf-8') as f:
    oldQs = json.load(f)

# 读取新解析的第四-第六套
newPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '第四套-第六套.json')
with open(newPath, 'r', encoding='utf-8') as f:
    newQs = json.load(f)

# 合并
allQs = oldQs + newQs

# 重新编号
for i in range(len(allQs)):
    allQs[i]['id'] = i + 1

# 保存
outputPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
with open(outputPath, 'w', encoding='utf-8') as f:
    json.dump(allQs, f, ensure_ascii=False, indent=2)

# 统计
count = {}
for q in allQs:
    s = q['set']
    count[s] = count.get(s, 0) + 1

print('合并成功！')
for s in sorted(count.keys()):
    print(f'第{s}套: {count[s]}题')
print(f'总计: {len(allQs)}题')
