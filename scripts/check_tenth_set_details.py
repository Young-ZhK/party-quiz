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
    
    # 检查61-100题的详细信息
    print("\n第61-100题的答案情况：")
    for i, q in enumerate(tenth_set, 1):
        if i >= 61 and i <= 100:
            answer = q.get('answer', '无')
            q_type = q.get('type', '未知')
            print(f"第{i}题 (类型: {q_type}): 答案 = {answer}")

if __name__ == "__main__":
    main()