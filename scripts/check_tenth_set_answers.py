import json
import os

def main():
    # 读取questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 筛选第十套题
    tenth_set = [q for q in all_questions if q.get('set') == 10]
    
    print(f"第十套题共有 {len(tenth_set)} 道题")
    
    # 检查61-100题的答案
    missing_answers = []
    for i, q in enumerate(tenth_set, 1):
        if i >= 61 and i <= 100:
            if 'answer' not in q or not q['answer']:
                missing_answers.append(i)
    
    if missing_answers:
        print(f"第61-100题中，以下题目缺少答案：{missing_answers}")
    else:
        print("第61-100题都有答案")
    
    # 检查所有题目的答案情况
    all_missing = []
    for i, q in enumerate(tenth_set, 1):
        if 'answer' not in q or not q['answer']:
            all_missing.append(i)
    
    if all_missing:
        print(f"第十套题中，以下题目缺少答案：{all_missing}")
    else:
        print("第十套题所有题目都有答案")

if __name__ == "__main__":
    main()