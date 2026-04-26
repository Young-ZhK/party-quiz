import json

def update_set_1_answers():
    print('=' * 60)
    print('更新第 1 套题判断题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 定义正确答案映射（True=正确，False=错误）
    answers = {
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
    
    updated_count = 0
    
    # 更新第1套题的判断题答案
    for q in questions:
        if q['set'] == 1 and 61 <= q['id'] <= 80:
            expected_answer = answers.get(q['id'])
            if expected_answer is not None:
                if q['answer'] != expected_answer:
                    old_val = '正确' if q['answer'] else '错误'
                    new_val = '正确' if expected_answer else '错误'
                    print(f'[OK] 第 {q["id"]} 题：{old_val} -> {new_val}')
                    q['answer'] = expected_answer
                    updated_count += 1
    
    print()
    if updated_count > 0:
        # 保存更新后的数据
        with open('data/questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f'[OK] 更新完成！共更新 {updated_count} 道题')
    else:
        print('[OK] 无需更新，答案已经正确')
    print('=' * 60)

if __name__ == '__main__':
    update_set_1_answers()
