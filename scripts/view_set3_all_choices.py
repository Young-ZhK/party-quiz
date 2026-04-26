import json

def view_set3_all_choices():
    print('=' * 60)
    print('查看第3套题所有选择题（1-60题）')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第3套题
    set3_questions = [q for q in questions if q['set'] == 3]
    sorted_questions = sorted(set3_questions, key=lambda x: x['id'])
    
    # 打印1-60题
    for q in sorted_questions:
        if 201 <= q['id'] <= 260:
            q_num = q['id'] - 200
            print(f'第 {q_num} 题（id={q["id"]}，类型={q["type"]}）')
            print(f'题目：{q["question"]}')
            if q.get('options'):
                print('选项：')
                for i, opt in enumerate(q['options']):
                    print(f'  {chr(65+i)}. {opt}')
            print(f'答案：{q["answer"]}')
            print('-' * 60)
            print()

if __name__ == '__main__':
    view_set3_all_choices()
