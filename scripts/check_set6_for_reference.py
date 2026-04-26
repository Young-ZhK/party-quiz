import json

def check_set6_for_reference():
    print('=' * 60)
    print('查看第6套题的81-90题作为参考')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第6套题
    set6_questions = [q for q in questions if q['set'] == 6]
    sorted_questions = sorted(set6_questions, key=lambda x: x['id'])
    
    # 打印81-90题
    for q in sorted_questions:
        if 581 <= q['id'] <= 590:
            q_num = q['id'] - 500
            print(f'第 {q_num} 题（id={q["id"]}）')
            print(f'题目：{q["question"]}')
            print(f'答案：{q["answer"]}')
            print('-' * 60)
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    check_set6_for_reference()
