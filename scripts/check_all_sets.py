import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

for set_num in [1, 2, 3]:
    print("\n" + "="*50)
    print(f"Checking set {set_num}")
    print("="*50)
    
    set_questions = [q for q in all_questions if q.get('set') == set_num]
    
    # 检查类型为 multiple_choice 但只有两个选项的题目
    problem_count = 0
    for q in set_questions:
        if q['type'] == 'multiple_choice' and len(q.get('options', [])) == 2:
            print(f"PROBLEM id={q['id']}: type={q['type']}, options={q['options']}, answer={q['answer']}")
            problem_count += 1
    
    if problem_count == 0:
        print("OK, no problems found")
    else:
        print(f"\nFound {problem_count} problems")
