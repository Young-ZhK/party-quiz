import json

def check_set3_answers():
    print('=' * 60)
    print('检查第三套题 61-90 题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第三套题
    set3_questions = [q for q in questions if q['set'] == 3]
    sorted_questions = sorted(set3_questions, key=lambda x: x['id'])
    
    # 打印 61-90 题（id=261-290）
    for q in sorted_questions:
        if 261 <= q['id'] <= 290:
            q_num = q['id'] - 200
            print(f'第 {q_num} 题（id={q["id"]}）')
            print(f'类型：{q["type"]}')
            print(f'题目：{q["question"]}')
            if q.get('options'):
                print('选项：')
                for i, opt in enumerate(q['options']):
                    print(f'  {chr(65+i)}. {opt}')
            print(f'答案：{q["answer"]}')
            print('-' * 60)
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    check_set3_answers()
