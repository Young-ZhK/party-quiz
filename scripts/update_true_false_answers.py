
import json

def main():
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 定义需要修改的题目
    # 格式：(套号, 题目序号, 正确答案)
    updates = [
        # 第一套
        (1, 65, False),
        (1, 69, False),
        (1, 71, False),
        (1, 75, False),
        # 第二套
        (2, 65, False),
        (2, 75, False),
        (2, 76, False),
    ]
    
    modified_count = 0
    
    # 处理每一道需要修改的题目
    for set_num, q_num_in_set, correct_answer in updates:
        # 找到该套的题目
        set_questions = [q for q in questions if q['set'] == set_num]
        set_questions.sort(key=lambda x: x['id'])
        
        if q_num_in_set > len(set_questions):
            print('第{}套第{}题不存在'.format(set_num, q_num_in_set))
            continue
        
        # 找到题目
        q = set_questions[q_num_in_set - 1]
        
        # 更新答案
        if q['answer'] != correct_answer:
            q['answer'] = correct_answer
            modified_count += 1
            answer_text = '正确' if correct_answer else '错误'
            print('第{}套第{}题已更新为：{}'.format(set_num, q_num_in_set, answer_text))
            print('  题目：{}'.format(q['question']))
    
    # 保存更新后的数据
    with open('data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print('\n共修改了{}道题'.format(modified_count))

if __name__ == "__main__":
    main()
