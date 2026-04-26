#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    print(f"总共 {len(all_questions)} 道题目")
    
    # 统计每套题目数量
    set_counts = {}
    for q in all_questions:
        s = q['set']
        set_counts[s] = set_counts.get(s, 0) + 1
    
    print("\n每套题目数量:")
    total = 0
    for s in sorted(set_counts.keys()):
        count = set_counts[s]
        total += count
        print(f"  第{s}套: {count}道")
    
    print(f"\n总计: {total}道")
    
    # 检查uid
    print("\n检查uid...")
    uids = []
    duplicate_uids = []
    for q in all_questions:
        uid = q.get('uid', q.get('id'))
        if uid in uids:
            duplicate_uids.append(uid)
        uids.append(uid)
    
    print(f"uid范围: {min(uids)} - {max(uids)}")
    if duplicate_uids:
        print(f"重复uid: {duplicate_uids}")
    else:
        print("没有重复uid")

if __name__ == '__main__':
    main()
