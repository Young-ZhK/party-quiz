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
    
    print(f"总共读取到 {len(all_questions)} 道题目")
    
    # 统计每套题目的数量
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
    
    start_pos = html_content.find(start_marker)
    if start_pos == -1:
        print("错误: 找不到开始标记")
        return
    
    end_pos = html_content.find(end_marker, start_pos)
    if end_pos == -1:
        print("错误: 找不到结束标记")
        return
    
    # 生成新的allQuestionsData数组
    questions_js = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 替换原有的allQuestionsData数组
    # 注意：结束标记是']//...'，所以我们要保留']'
    new_html = (
        html_content[:start_pos + len(start_marker)] + 
        questions_js + 
        html_content[end_pos:]  # 这里已经包含了']'
    )
    
    # 更新题目总数注释
    new_html = new_html.replace(
        '// ========== 嵌入式题目数据（共1200道题）==========',
        f'// ========== 嵌入式题目数据（共{len(all_questions)}道题）=========='
    )
    
    # 先写一个临时文件，避免破坏原文件
    temp_path = index_path + '.temp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    # 现在更新UI部分，添加第十套的按钮和选项
    # 1. 更新题目选择按钮
    set_buttons_marker = '<button class="set-btn" id="set-9" onclick="selectSet(\'9\')">第九套</button>'
    new_set_buttons = set_buttons_marker + '\n                        <button class="set-btn" id="set-10" onclick="selectSet(\'10\')">第十套</button>'
    new_html = new_html.replace(set_buttons_marker, new_set_buttons)
    
    # 2. 更新沉浸式学习按钮
    immersive_buttons_marker = '<button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'9\')">第九套</button>'
    new_immersive_buttons = immersive_buttons_marker + '\n                    <button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'10\')">第十套</button>'
    new_html = new_html.replace(immersive_buttons_marker, new_immersive_buttons)
    
    # 3. 更新选择下拉菜单（需要处理多个出现位置）
    select_marker = '<option value="9">第九套</option>'
    new_select = select_marker + '\n                        <option value="10">第十套</option>'
    
    # 替换所有的下拉菜单
    count = 0
    parts = new_html.split(select_marker)
    if len(parts) > 1:
        new_html = parts[0]
        for i in range(1, len(parts)):
            new_html += new_select
            new_html += parts[i]
            count += 1
        print(f"\n更新了 {count} 个下拉菜单")
    
    # 4. 更新题目套数映射（需要处理多个出现位置）
    set_map_marker = "9: '第九套'"
    new_set_map = "9: '第九套', 10: '第十套'"
    
    # 替换所有的映射
    count = 0
    parts = new_html.split(set_map_marker)
    if len(parts) > 1:
        new_html = parts[0]
        for i in range(1, len(parts)):
            new_html += new_set_map
            new_html += parts[i]
            count += 1
        print(f"更新了 {count} 个套数映射")
    
    # 写入最终的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"\n成功更新index.html!")
    
    # 验证结果
    with open(index_path, 'r', encoding='utf-8') as f:
        final_html = f.read()
    
    print("\n验证结果:")
    print(f"  第十套按钮: {'第十套</button>' in final_html}")
    print(f"  第十套选项: {'第十套</option>' in final_html}")
    
    # 检查题目数据
    if questions_js in final_html:
        print("  题目数据: ✓ 包含所有1000道题目")
        
        # 检查具体的题目
        if '"uid":1101' in final_html:
            print("  uid:1101: ✓ 存在")
        
        if '"set":10' in final_html or '"set": 10' in final_html:
            print("  set:10: ✓ 存在")

if __name__ == '__main__':
    main()
