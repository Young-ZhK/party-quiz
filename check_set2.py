import json

# 读取题目数据
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查第二套的单选和多选
set2_questions = [q for q in data if q.get('set') == 2]
print(f"第二套共有 {len(set2_questions)} 题")

problem_count = 0
for q in set2_questions:
    if q['type'] in ['single_choice', 'multiple_choice']:
        options = q.get('options', [])
        if len(options) == 1 and isinstance(options[0], str):
            # 检查是否还包含其他选项
            opt_str = options[0]
            if '、' in opt_str and (('A' in opt_str and 'B' in opt_str) or ('A、' in opt_str)):
                problem_count += 1
                print(f"\n发现问题：{q['id']} - {q['question']}")
                print(f"  选项：{opt_str}")

print(f"\n共发现 {problem_count} 道有问题的题目")
