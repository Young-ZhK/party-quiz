import json

def check_set_1_tf():
    print('=' * 60)
    print('检查第 1 套题判断题（61-80题）')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 定义用户提供的正确答案（True=正确，False=错误）
    expected_answers = {
        61: True,
        62: True,
        63: True,
        64: True,
        65: False,
        66: True,
        67: True,
        68: True,
        69: False,
        70: True,
        71: False,
        72: True,
        73: True,
        74: True,
        75: False,
        76: True,
        77: True,
        78: True,
        79: True,
        80: True,
    }
    
    # 筛选第1套题并按id排序
    set_1_questions = [q for q in questions if q['set'] == 1]
    sorted_questions = sorted(set_1_questions, key=lambda x: x['id'])
    
    wrong_count = 0
    
    # 打印第61-80题的信息
    for q in sorted_questions:
        if 61 <= q['id'] <= 80:
            actual = q['answer']
            expected = expected_answers.get(q['id'])
            
            actual_str = '正确' if actual else '错误'
            expected_str = '正确' if expected else '错误'
            
            status = '[OK]' if actual == expected else '[!]'
            
            print(f'{status} 第 {q["id"]} 题')
            print(f'  当前答案：{actual_str}')
            if actual != expected:
                print(f'  正确答案：{expected_str}')
                wrong_count += 1
            print(f'  题目：{q["question"][:60]}...')
            print()
    
    print('=' * 60)
    if wrong_count > 0:
        print(f'[!] 发现 {wrong_count} 道错误题目')
    else:
        print('[OK] 所有题目答案正确')
    print('=' * 60)

if __name__ == '__main__':
    check_set_1_tf()
