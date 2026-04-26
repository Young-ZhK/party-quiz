
import json

def check_set_1():
    print('=== 检查第一套题目标注 ===\n')
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 筛选第一套题目
    set_1_questions = [q for q in questions if q['set'] == 1]
    
    # 按 id 排序
    sorted_questions = sorted(set_1_questions, key=lambda x: x['id'])
    
    if len(sorted_questions) != 100:
        print(f'⚠️ 第一套题目数量异常：{len(sorted_questions)}题（应该100题）\n')
        return False
    
    print('✅ 第一套题目数量：100题\n')
    
    # 检查各区间
    ranges = [
        (1, 40, 'single_choice', '单选题'),
        (41, 60, 'multiple_choice', '多选题'),
        (61, 80, 'true_false', '判断题'),
        (81, 100, 'fill_blank', '填空题'),
    ]
    
    all_correct = True
    
    for start, end, expected_type, expected_name in ranges:
        print(f'📋 检查{start}-{end}题（{expected_name}）...')
        
        correct = True
        wrong_questions = []
        
        for i in range(start, end + 1):
            q = sorted_questions[i - 1]
            actual_type = q['type']
            
            if actual_type != expected_type:
                correct = False
                all_correct = False
                wrong_questions.append({
                    'num': i,
                    'question': q['question'],
                    'expected': expected_name,
                    'actual': actual_type
                })
        
        if correct:
            print(f'✅ {start}-{end}题全部正确！\n')
        else:
            print(f'❌ 发现{len(wrong_questions)}道错误标注的题目：')
            for q in wrong_questions:
                print(f'   第{q["num"]}题：期望{q["expected"]}，实际{q["actual"]}')
                print(f'   题目：{q["question"]}')
            print()
    
    if all_correct:
        print('🎉 第一套题目标注检查完成！全部正确！')
    else:
        print('⚠️ 第一套题目标注存在问题！')
    
    return all_correct

if __name__ == '__main__':
    check_set_1()
