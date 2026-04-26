
import json

def check_question_set(questions, set_number):
    print(f"\n=== 检查第{set_number}套题目 ===")
    
    # 筛选指定套题的题目
    set_questions = [q for q in questions if q['set'] == set_number]
    
    # 按顺序编号1-100
    sorted_questions = sorted(set_questions, key=lambda x: x['id'])
    
    if len(sorted_questions) != 100:
        print(f"[WARNING] 第{set_number}套题目数量异常：{len(sorted_questions)}题（应该100题）")
        return False
    
    print(f"[OK] 题目数量：100题")
    
    # 检查各区间题目类型
    ranges = {
        "1-40题": (1, 40, "single_choice", "单选题"),
        "41-60题": (41, 60, "multiple_choice", "多选题"),
        "61-80题": (61, 80, "true_false", "判断题"),
        "81-100题": (81, 100, "fill_blank", "填空题")
    }
    
    all_correct = True
    
    for name, (start, end, expected_type, expected_name) in ranges.items():
        correct = True
        print(f"\n[CHECK] 检查{name}...")
        
        for i in range(start, end + 1):
            q = sorted_questions[i - 1]
            actual_type = q['type']
            
            if actual_type != expected_type:
                correct = False
                print(f"[ERROR] 第{i}题：期望{expected_name}({expected_type})，实际{actual_type}")
        
        if correct:
            print(f"[OK] {name}全部正确：{expected_name}({expected_type})")
        else:
            all_correct = False
    
    return all_correct

def main():
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"总题目数量：{len(questions)}")
    
    # 检查第2套
    set_2_correct = check_question_set(questions, 2)
    
    # 检查第3套
    set_3_correct = check_question_set(questions, 3)
    
    if set_2_correct and set_3_correct:
        print(f"\n[SUCCESS] 所有检查通过！")
    else:
        print(f"\n[FAILURE] 发现问题，需要修复")

if __name__ == "__main__":
    main()
