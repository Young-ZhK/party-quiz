import json

def check_set_2_answers():
    print('=' * 60)
    print('检查第 2 套题判断题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第2套题并按id排序
    set_2_questions = [q for q in questions if q['set'] == 2]
    sorted_questions = sorted(set_2_questions, key=lambda x: x['id'])
    
    # 打印第61-80题的信息
    for q in sorted_questions:
        if 61 <= q['id'] <= 80:
            answer_str = '正确' if q['answer'] else '错误'
            print(f'第 {q["id"]} 题：{answer_str}')
            print(f'  题目：{q["question"][:40]}...')
            print()
    
    print('=' * 60)

if __name__ == '__main__':
    check_set_2_answers()
