import json

# 读取 questions.json 中的第十套题目
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 筛选第十套题目
tenth_set_questions = [q for q in questions if q.get('set') == 10]

print(f"第十套题目数量: {len(tenth_set_questions)}")

# 显示前5道题目的 uid
for i, q in enumerate(tenth_set_questions[:5]):
    print(f"题目 {i+1}: uid={q['uid']}, id={q['id']}, set={q['set']}")

# 显示最后5道题目的 uid
for i, q in enumerate(tenth_set_questions[-5:]):
    print(f"最后题目 {len(tenth_set_questions)-4+i}: uid={q['uid']}, id={q['id']}, set={q['set']}")

# 检查 uid 的范围
uids = [q['uid'] for q in tenth_set_questions]
print(f"\nUID 范围: {min(uids)} - {max(uids)}")
