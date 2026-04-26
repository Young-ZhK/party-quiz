import json

def check_all_sets():
    print('=' * 60)
    print('检查所有题库（8套题）标注')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    all_correct = True
    
    # 检查每一套题
    for set_num in range(1, 9):
        print('=' * 60)
        print(f'检查第 {set_num} 套题')
        print('=' * 60)
        
        # 筛选当前套题
        set_questions = [q for q in questions if q['set'] == set_num]
        
        # 按 id 排序
        sorted_questions = sorted(set_questions, key=lambda x: x['id'])
        
        if len(sorted_questions) != 100:
            print(f'[!] 题目数量异常：{len(sorted_questions)} 题（应该 100 题）')
            all_correct = False
            print()
            continue
        
        print('[OK] 题目数量：100 题')
        print()
        
        # 检查各区间
        ranges = [
            (1, 40, 'single_choice', '单选题'),
            (41, 60, 'multiple_choice', '多选题'),
            (61, 80, 'true_false', '判断题'),
            (81, 100, 'fill_blank', '填空题'),
        ]
        
        set_correct = True
        
        for start, end, expected_type, expected_name in ranges:
            print(f'[*] 检查 {start}-{end} 题（{expected_name}）...')
            
            range_correct = True
            wrong_questions = []
            
            for i in range(start, end + 1):
                q = sorted_questions[i - 1]
                actual_type = q['type']
                
                if actual_type != expected_type:
                    range_correct = False
                    set_correct = False
                    all_correct = False
                    wrong_questions.append({
                        'num': i,
                        'question': q['question'],
                        'expected': expected_name,
                        'actual': actual_type
                    })
            
            if range_correct:
                print(f'[OK] {start}-{end} 题全部正确')
            else:
                print(f'[!] 发现 {len(wrong_questions)} 道错误标注的题目：')
                for q in wrong_questions:
                    print(f'    第 {q["num"]} 题：期望 {q["expected"]}，实际 {q["actual"]}')
                    print(f'    题目：{q["question"][:30]}...')
            print()
        
        if set_correct:
            print(f'[OK] 第 {set_num} 套题标注正确！')
        else:
            print(f'[!] 第 {set_num} 套题标注存在问题！')
        print()
    
    print('=' * 60)
    if all_correct:
        print('[OK] 所有 8 套题标注检查完成！全部正确！')
    else:
        print('[!] 存在标注问题的套题！')
    print('=' * 60)
    
    return all_correct

if __name__ == '__main__':
    check_all_sets()
