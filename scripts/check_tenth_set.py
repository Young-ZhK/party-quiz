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
    
    # 检查答案字段
    questions_without_answer = []
    for i, q in enumerate(tenth_set):
        if 'answer' not in q or not q['answer']:
            questions_without_answer.append(i + 1)
    
    if questions_without_answer:
        print(f"缺少答案的题目: {questions_without_answer}")
    else:
        print("所有题目都有答案")
    
    # 检查前几个题目
    print("\n前5道题的结构:")
    for i, q in enumerate(tenth_set[:5]):
        print(f"\n第{i+1}题:")
        print(f"  id: {q.get('id')}")
        print(f"  set: {q.get('set')}")
        print(f"  type: {q.get('type')}")
        print(f"  question: {q.get('question')[:50]}...")
        print(f"  answer: {q.get('answer')}")
        if 'options' in q:
            print(f"  options: {len(q['options'])}个选项")

if __name__ == '__main__':
    main()
