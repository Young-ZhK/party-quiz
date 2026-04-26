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
    
    # 读取index.html
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 找到脚本开始位置
    script_start = html_content.find('<script>')
    if script_start == -1:
        print("错误: 找不到<script>标签")
        return
    
    # 找到函数定义开始位置
    toggle_start = html_content.find('function toggleCollapse', script_start)
    if toggle_start == -1:
        print("错误: 找不到toggleCollapse函数")
        return
    
    # 生成新的题目数据JSON
    questions_json = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 构建新的脚本内容
    new_script = f'''<script>
    // ========== 嵌入式题目数据（共{len(all_questions)}道题）==========
    const allQuestionsData = {questions_json};
    
    function toggleCollapse(id) {html_content[toggle_start + len('function toggleCollapse'):]}
    '''
    
    # 替换脚本部分
    new_html = html_content[:script_start] + new_script
    
    # 写入更新后的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("✓ 成功修复JavaScript语法错误！")
    print("✓ 数组定义已正确结束")

if __name__ == '__main__':
    main()
