import json

def check_set3_true_false():
    print('=' * 60)
    print('检查第三套题 61-80 题（判断题）')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第三套题
    set3_questions = [q for q in questions if q['set'] == 3]
    sorted_questions = sorted(set3_questions, key=lambda x: x['id'])
    
    # 打印 61-80 题（id=261-280）
    for q in sorted_questions:
        if 261 <= q['id'] <= 280:
            q_num = q['id'] - 200
            answer_str = '正确' if q['answer'] else '错误'
            print(f'第 {q_num} 题（id={q["id"]}）：{answer_str}')
            print(f'题目：{q["question"]}')
            print('-' * 60)
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    check_set3_true_false()
