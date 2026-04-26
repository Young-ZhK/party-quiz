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
    # 将所有题目转换为JavaScript格式
    questions_js = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 替换原有的allQuestionsData数组
    new_html = (
        html_content[:start_pos + len(start_marker)] + 
        questions_js + 
        html_content[end_pos:]
    )
    
    # 更新题目总数注释
    new_html = new_html.replace(
        '// ========== 嵌入式题目数据（共1200道题）==========',
        f'// ========== 嵌入式题目数据（共{len(all_questions)}道题）=========='
    )
    
    # 写入更新后的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"\n成功更新index.html，包含 {len(all_questions)} 道题目")
    
    # 现在更新UI部分，添加第十套的按钮和选项
    # 1. 更新题目选择按钮
    set_buttons_marker = '<button class="set-btn" id="set-9" onclick="selectSet(\'9\')">第九套</button>'
    new_set_buttons = set_buttons_marker + '\n                        <button class="set-btn" id="set-10" onclick="selectSet(\'10\')">第十套</button>'
    
    # 2. 更新沉浸式学习按钮
    immersive_buttons_marker = '<button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'9\')">第九套</button>'
    new_immersive_buttons = immersive_buttons_marker + '\n                    <button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'10\')">第十套</button>'
    
    # 3. 更新选择下拉菜单1
    select1_marker = '<option value="9">第九套</option>'
    new_select1 = select1_marker + '\n                        <option value="10">第十套</option>'
    
    # 4. 更新选择下拉菜单2
    select2_marker = '<option value="9">第九套</option>'
    new_select2 = select2_marker + '\n                        <option value="10">第十套</option>'
    
    # 5. 更新题目套数映射1
    set_map1_marker = "9: '第九套'"
    new_set_map1 = "9: '第九套', 10: '第十套'"
    
    # 6. 更新题目套数映射2
    set_map2_marker = "9: '第九套'"
    new_set_map2 = "9: '第九套', 10: '第十套'"
    
    # 7. 更新题目套数映射3
    set_map3_marker = "9: '第九套'"
    new_set_map3 = "9: '第九套', 10: '第十套'"
    
    # 应用所有替换
    new_html = new_html.replace(set_buttons_marker, new_set_buttons)
    new_html = new_html.replace(immersive_buttons_marker, new_immersive_buttons)
    new_html = new_html.replace(select1_marker, new_select1)
    
    # 需要处理第二个下拉菜单，它可能在不同位置
    # 先替换第一个，然后查找第二个
    parts = new_html.split(select2_marker)
    if len(parts) > 2:
        # 有多个匹配项，只替换第二个
        new_html = parts[0] + select2_marker + parts[1] + new_select2 + parts[2]
    
    # 更新套数映射
    # 查找所有三个映射
    map_positions = []
    search_pos = 0
    while True:
        pos = new_html.find(set_map1_marker, search_pos)
        if pos == -1:
            break
        map_positions.append(pos)
        search_pos = pos + len(set_map1_marker)
    
    print(f"\n找到 {len(map_positions)} 个套数映射位置")
    
    # 依次替换
    for i, pos in enumerate(map_positions):
        before = new_html[:pos]
        after = new_html[pos + len(set_map1_marker):]
        new_html = before + new_set_map1 + after
        # 因为替换后长度变化，需要重新查找位置
        if i < len(map_positions) - 1:
            map_positions = []
            search_pos = 0
            while True:
                pos = new_html.find(set_map1_marker, search_pos)
                if pos == -1:
                    break
                map_positions.append(pos)
                search_pos = pos + len(set_map1_marker)
    
    # 写入最终的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("\n成功更新UI，添加第十套按钮和选项!")
    
    # 验证结果
    with open(index_path, 'r', encoding='utf-8') as f:
        final_html = f.read()
    
    print("\n验证结果:")
    print(f"  第十套按钮: {'第十套</button>' in final_html}")
    print(f"  第十套选项: {'第十套</option>' in final_html}")
    print(f"  uid:1101: {'"uid":1101' in final_html}")
    print(f"  set:10: {'"set":10' in final_html}")

if __name__ == '__main__':
    main()
