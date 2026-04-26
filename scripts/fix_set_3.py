
import json

def fix_set_3(questions):
    print("=== 修复第3套题目 ===")
    
    # 筛选第3套题目
    set_3_questions = [q for q in questions if q['set'] == 3]
    
    # 按顺序排序
    sorted_questions = sorted(set_3_questions, key=lambda x: x['id'])
    
    fixed_count = 0
    
    # 修复61-80题：将multiple_choice改为true_false
    for i in range(61, 81):
        q = sorted_questions[i - 1]
        if q['type'] == 'multiple_choice':
            q['type'] = 'true_false'
            fixed_count += 1
            print(f"[FIX] 第{i}题：multiple_choice -&gt; true_false")
    
    # 修复81-100题：将true_false改为fill_blank
    for i in range(81, 101):
        q = sorted_questions[i - 1]
        if q['type'] == 'true_false':
            q['type'] = 'fill_blank'
            fixed_count += 1
            print(f"[FIX] 第{i}题：true_false -&gt; fill_blank")
    
    print(f"\n[SUCCESS] 共修复{fixed_count}题")
    
    return questions

def main():
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 修复第3套
    questions = fix_set_3(questions)
    
    # 保存修改后的数据
    with open('data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print("\n[SUCCESS] 数据已保存！")

if __name__ == "__main__":
    main()
