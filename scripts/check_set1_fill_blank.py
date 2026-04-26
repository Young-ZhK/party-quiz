import json

def check_set1_fill_blank():
    print('=' * 60)
    print('查看第1套题的81-90题填空题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第1套题
    set1_questions = [q for q in questions if q['set'] == 1]
    sorted_questions = sorted(set1_questions, key=lambda x: x['id'])
    
    # 打印81-90题
    for q in sorted_questions:
        if 81 <= q['id'] <= 90:
            q_num = q['id']
            print(f'第 {q_num} 题（id={q["id"]}）')
            print(f'题目：{repr(q["question"])}')
            print(f'答案：{repr(q["answer"])}')
            print('-' * 60)
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    check_set1_fill_blank()
