import json

def fix_set_1():
    print('=' * 60)
    print('修复第 1 套题标注')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 修复第1套题21-40题的类型
    fixed_count = 0
    for q in questions:
        if q['set'] == 1 and 21 <= q['id'] <= 40:
            if q['type'] == 'multiple_choice':
                q['type'] = 'single_choice'
                fixed_count += 1
                print(f'[OK] 第 {q["id"]} 题：multiple_choice -> single_choice')
    
    print()
    if fixed_count > 0:
        # 保存修复后的数据
        with open('data/questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f'[OK] 修复完成！共修复 {fixed_count} 道题')
    else:
        print('[OK] 无需修复，第 1 套题已经正确标注')
    print('=' * 60)

if __name__ == '__main__':
    fix_set_1()
