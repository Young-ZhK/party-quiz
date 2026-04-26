import json

def check_all_fill_blank():
    print('=' * 60)
    print('检查所有套题的填空题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    wrong_count = 0
    
    # 检查每套题的81-100题（填空题）
    for set_num in range(1, 9):
        print(f'第 {set_num} 套题：')
        
        set_questions = [q for q in questions if q['set'] == set_num]
        sorted_questions = sorted(set_questions, key=lambda x: x['id'])
        
        for q in sorted_questions:
            if q['type'] == 'fill_blank':
                q_num = q['id'] - (set_num - 1) * 100
                if q['answer'] is False or q['answer'] is True:
                    print(f'  [ERROR] 第 {q_num} 题（id={q["id"]}）：答案错误（{q["answer"]}）')
                    print(f'     题目：{q["question"]}')
                    wrong_count += 1
                else:
                    print(f'  [OK] 第 {q_num} 题（id={q["id"]}）：答案正确（{q["answer"]}）')
        
        print()
    
    print('=' * 60)
    print(f'共发现 {wrong_count} 道错误的填空题答案')
    print('=' * 60)

if __name__ == '__main__':
    check_all_fill_blank()
