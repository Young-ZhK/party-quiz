import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

# 检查第二套的题目
set2_questions = [q for q in all_questions if q.get('set') == 2]

print("Checking set 2...\n")

problem_count = 0
for q in set2_questions:
    # 检查：类型为 fill_blank，但题目中没有空白字符（____），且答案为空
    if q['type'] == 'fill_blank':
        if '____' not in q['question'] and q.get('answer') == '':
            print(f"PROBLEM id={q['id']}: type={q['type']}, question={q['question']}")
            problem_count += 1

if problem_count == 0:
    print("OK, no problems found")
else:
    print(f"\nFound {problem_count} problems")
