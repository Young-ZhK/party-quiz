import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

# 检查第三套的题目
set3_questions = [q for q in all_questions if q.get('set') == 3]

print(f"第三套共有 {len(set3_questions)} 道题\n")

print("检查第三套中类型为 multiple_choice 但只有两个选项的题目：")
problem_questions = []
for q in set3_questions:
    if q['type'] == 'multiple_choice' and len(q['options']) == 2:
        problem_questions.append(q)
        print(f"id={q['id']}, type={q['type']}, options={q['options']}, answer={q['answer']}")

print(f"\n共发现 {len(problem_questions)} 道有问题的题目")
