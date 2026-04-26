import json

def check_set3_choices():
    print('=' * 60)
    print('检查第3套题选择题（1-60题）')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第3套题
    set3_questions = [q for q in questions if q['set'] == 3]
    sorted_questions = sorted(set3_questions, key=lambda x: x['id'])
    
    wrong_count = 0
    
    # 检查1-60题
    for q in sorted_questions:
        if 201 <= q['id'] <= 260:
            q_num = q['id'] - 200
            answer = q['answer']
            
            # 检查答案是否是布尔值或者格式不正确
            if isinstance(answer, bool) or answer is None:
                print(f'[ERROR] 第 {q_num} 题（id={q["id"]}）')
                print(f'  题目：{q["question"][:50]}...')
                print(f'  答案：{answer}（类型：{type(answer)}）')
                if q.get('options'):
                    print('  选项：')
                    for i, opt in enumerate(q['options']):
                        print(f'    {chr(65+i)}. {opt}')
                print()
                wrong_count += 1
    
    print('=' * 60)
    print(f'共发现 {wrong_count} 道错误的选择题')
    print('=' * 60)

if __name__ == '__main__':
    check_set3_choices()
