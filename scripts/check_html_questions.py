#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os
import re

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 找到allQuestionsData数组
    start_marker = 'const allQuestionsData ='
    end_marker = ']// ========== 折叠功能 =========='
    
    start_pos = html_content.find(start_marker)
    end_pos = html_content.find(end_marker, start_pos)
    
    if start_pos == -1 or end_pos == -1:
        print("找不到allQuestionsData数组")
        return
    
    # 提取数组内容，注意要包含最后的']'
    array_content = html_content[start_pos + len(start_marker):end_pos + 1]
    
    print(f"数组内容长度: {len(array_content)} 字符")
    print(f"前200个字符: {array_content[:200]}")
    print(f"\n后200个字符: {array_content[-200:]}")
    
    # 尝试解析JSON
    try:
        questions = json.loads(array_content)
        print(f"\n成功解析 {len(questions)} 道题目")
        
        # 统计每套题目
        set_counts = {}
        for q in questions:
            s = q['set']
            set_counts[s] = set_counts.get(s, 0) + 1
        
        print("\n每套题目数量:")
        for s in sorted(set_counts.keys()):
            print(f"  第{s}套: {set_counts[s]}道")
        
        # 查找第10套的前几道题
        print("\n第10套的前5道题:")
        count = 0
        for q in questions:
            if q['set'] == 10:
                print(f"  uid:{q['uid']}, id:{q['id']}, {q['question'][:30]}...")
                count += 1
                if count >= 5:
                    break
        
    except Exception as e:
        print(f"\n解析失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
