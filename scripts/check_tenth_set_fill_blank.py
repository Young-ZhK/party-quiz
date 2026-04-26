import json
import os
import sys

# 设置编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 读取questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 筛选第十套题的81-100题
    tenth_set_81_100 = [q for q in all_questions if q.get('set') == 10 and q.get('id', 0) >= 81 and q.get('id', 0) <= 100]
    
    print(f"第十套题81-100题共有 {len(tenth_set_81_100)} 道")
    
    # 显示这些题的详细信息
    print("\n81-100题详情：")
    for q in tenth_set_81_100:
        question_num = q.get('id', '未知')
        question = q.get('question', '无题目')
        answer = q.get('answer', '无答案')
        q_type = q.get('type', '未知')
        print(f"第{question_num}题 (类型: {q_type}): {question}")
        print(f"答案: {answer}")
        print("-" * 50)

if __name__ == "__main__":
    main()