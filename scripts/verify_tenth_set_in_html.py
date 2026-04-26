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
    
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("找不到allQuestionsData数组")
        return
    
    # 提取数组内容
    array_content = html_content[start_idx + len(start_marker):end_idx + 1]
    
    print(f"数组内容长度: {len(array_content)}")
    print(f"前100个字符: {array_content[:100]}")
    
    # 检查第十套的标记
    print("\n检查第十套...")
    if 'set":10' in array_content or 'set": 10' in array_content:
        print("✓ 第十套存在！")
    else:
        print("✗ 第十套不存在")
    
    # 检查uid:1101
    if '"uid":1101' in array_content:
        print("✓ uid:1101 存在！")
    else:
        print("✗ uid:1101 不存在")
    
    # 检查题目数量
    # 计算有多少个题目对象
    # 粗略统计
    count = array_content.count('{"id":')
    print(f"\n粗略统计题目数量: {count}")
    
    # 统计每套题目
    print("\n每套题目数量:")
    for set_num in range(1, 11):
        count_set = array_content.count(f'"set":{set_num}')
        if count_set == 0:
            count_set = array_content.count(f'"set": {set_num}')
        print(f"  第{set_num}套: {count_set}")
    
    print("\n验证完成！")

if __name__ == '__main__':
    main()
