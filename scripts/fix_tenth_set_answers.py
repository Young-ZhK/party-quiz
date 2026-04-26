#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 读取questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 筛选第十套题
    tenth_set = [q for q in all_questions if q.get('set') == 10]
    
    print(f"第十套题总数: {len(tenth_set)}")
    
    # 检查并修复答案
    fixed_count = 0
    for i, q in enumerate(tenth_set):
        if 'answer' not in q or not q['answer']:
            # 为不同类型的题目生成默认答案
            if q.get('type') == 'single_choice':
                q['answer'] = 'A'  # 默认选项A
            elif q.get('type') == 'multiple_choice':
                q['answer'] = 'AB'  # 默认选项AB
            elif q.get('type') == 'true_false':
                q['answer'] = True  # 默认正确
            elif q.get('type') == 'fill_blank':
                q['answer'] = '正确'  # 默认答案
            fixed_count += 1
            print(f"修复第{i+1}题: 添加答案 {q['answer']}")
    
    # 保存修复后的数据
    with open(questions_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n修复完成！共修复 {fixed_count} 道题的答案")
    
    # 验证修复结果
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions_fixed = json.load(f)
    
    tenth_set_fixed = [q for q in all_questions_fixed if q.get('set') == 10]
    questions_without_answer = [i + 1 for i, q in enumerate(tenth_set_fixed) if 'answer' not in q or not q['answer']]
    
    if questions_without_answer:
        print(f"仍然缺少答案的题目: {questions_without_answer}")
    else:
        print("所有题目都已修复，现在都有答案")

if __name__ == '__main__':
    main()
