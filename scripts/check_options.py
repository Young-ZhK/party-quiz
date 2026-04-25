import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

problem_count = 0

for q in all_questions:
    if q.get('type') in ['single_choice', 'multiple_choice'] and q.get('options'):
        for opt in q.get('options'):
            if '、' in opt and ('A.' in opt or 'B.' in opt or 'C.' in opt or 'D.' in opt or 'E.' in opt):
                print(f"PROBLEM set={q.get('set')}, id={q.get('id')}, option={opt}")
                problem_count += 1
            if ' E、' in opt or ' D、' in opt or ' C、' in opt or ' B、' in opt or ' A、' in opt:
                print(f"PROBLEM set={q.get('set')}, id={q.get('id')}, option={opt}")
                problem_count += 1

if problem_count == 0:
    print("OK, no problems found")
else:
    print(f"\nFound {problem_count} problems")
