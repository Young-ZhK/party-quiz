#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 读取完整的questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    print(f"✓ 从questions.json读取到 {len(all_questions)} 道题目")
    
    # 统计每套题目数量
    set_counts = {}
    for q in all_questions:
        s = q['set']
        set_counts[s] = set_counts.get(s, 0) + 1
    
    print("\n每套题目数量:")
    for s in sorted(set_counts.keys()):
        print(f"  第{s}套: {set_counts[s]}道")
    
    # 读取index.html
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 找到allQuestionsData数组的开始和结束位置
    start_marker = 'const allQuestionsData ='
    end_marker = ']// ========== 折叠功能 =========='
    
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("错误: 找不到allQuestionsData数组")
        return
    
    # 生成新的题目数据JSON
    # 注意：我们需要确保格式与原有一致（没有空格）
    questions_json = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 替换题目数据
    # 注意：end_marker以']'开始，所以我们保留这个']'
    new_html = (
        html_content[:start_idx + len(start_marker)] + 
        questions_json + 
        html_content[end_idx:]
    )
    
    # 更新题目总数注释
    new_html = new_html.replace(
        '// ========== 嵌入式题目数据（共1200道题）==========',
        f'// ========== 嵌入式题目数据（共{len(all_questions)}道题）=========='
    )
    
    # 写入更新后的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"\n✓ index.html已成功更新！")
    print(f"✓ 题目总数: {len(all_questions)}道 (10套×100道)")
    
    # 验证
    print(f"\n验证结果:")
    if f'"set":10' in new_html or f'"set": 10' in new_html:
        print(f"  ✓ 第十套题目存在")
    
    if f'"uid":1101' in new_html:
        print(f"  ✓ uid:1101 存在")

if __name__ == '__main__':
    main()
