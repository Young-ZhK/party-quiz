
import json

def main():
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 检查前两套的判断题
    print("=== 检查前两套的判断题 ===")
    
    true_false_questions = []
    
    for q in questions:
        if q['set'] in [1, 2] and q['type'] == 'true_false':
            true_false_questions.append(q)
    
    # 按套和id排序
    true_false_questions.sort(key=lambda x: (x['set'], x['id']))
    
    print(f"找到 {len(true_false_questions)} 道判断题\n")
    
    for q in true_false_questions:
        # 计算题目在套题中的序号
        set_questions = [x for x in questions if x['set'] == q['set']]
        set_questions.sort(key=lambda x: x['id'])
        q_index = next(i+1 for i, x in enumerate(set_questions) if x['id'] == q['id'])
        
        answer_text = "正确" if q['answer'] else "错误"
        print(f"第{q['set']}套 第{q_index}题:")
        print(f"  题目: {q['question']}")
        print(f"  答案: {answer_text} ({q['answer']})")
        print()

if __name__ == "__main__":
    main()
