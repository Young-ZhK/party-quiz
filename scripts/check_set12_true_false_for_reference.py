import json

def check_set12_true_false_for_reference():
    print('=' * 60)
    print('检查第1套和第2套的判断题作为参考')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 查看第69、75、78题
    target_ids = {
        1: [69, 75, 78],  # 第1套题的69、75、78题
        2: [169, 175, 178]  # 第2套题的69、75、78题
    }
    
    for set_num in [1, 2]:
        print(f'--- 第 {set_num} 套题 ---')
        for q in questions:
            if q['set'] == set_num and q['id'] in target_ids[set_num]:
                q_num = q['id'] - (set_num - 1) * 100
                answer_str = '正确' if q['answer'] else '错误'
                print(f'第 {q_num} 题：{answer_str}')
                print(f'题目：{q["question"]}')
                print()
        print()
    
    print('=' * 60)

if __name__ == '__main__':
    check_set12_true_false_for_reference()
