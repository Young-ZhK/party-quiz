#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 步骤1: 读取完整的questions.json
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
    
    # 步骤2: 读取index.html
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 步骤3: 找到并替换allQuestionsData数组
    # 查找开始和结束标记
    start_str = 'const allQuestionsData ='
    end_str = ']// ========== 折叠功能 =========='
    
    start_idx = html.find(start_str)
    end_idx = html.find(end_str, start_idx)
    
    if start_idx == -1 or end_idx == -1:
        print("错误: 找不到allQuestionsData数组")
        return
    
    # 生成新的题目数组JSON
    questions_json = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 替换题目数据
    # 注意: end_str以']'开始，所以我们保留这个']'
    new_html = (
        html[:start_idx + len(start_str)] + 
        questions_json + 
        html[end_idx:]
    )
    
    # 更新题目总数注释
    new_html = new_html.replace(
        '// ========== 嵌入式题目数据（共1200道题）==========',
        f'// ========== 嵌入式题目数据（共{len(all_questions)}道题）=========='
    )
    
    print(f"\n✓ 已更新题目数据，共 {len(all_questions)} 道")
    
    # 步骤4: 在UI中添加第十套的按钮和选项
    # 1. 题目选择按钮
    btn9 = '<button class="set-btn" id="set-9" onclick="selectSet(\'9\')">第九套</button>'
    btn10 = '\n                        <button class="set-btn" id="set-10" onclick="selectSet(\'10\')">第十套</button>'
    new_html = new_html.replace(btn9, btn9 + btn10)
    
    # 2. 沉浸式学习按钮
    immersive9 = '<button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'9\')">第九套</button>'
    immersive10 = '\n                    <button class="menu-btn feature-btn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" onclick="startImmersive(\'10\')">第十套</button>'
    new_html = new_html.replace(immersive9, immersive9 + immersive10)
    
    # 3. 下拉菜单选项 (需要处理多个位置)
    option9 = '<option value="9">第九套</option>'
    option10 = '\n                        <option value="10">第十套</option>'
    
    # 替换所有出现的下拉菜单选项
    count = 0
    while option9 in new_html:
        new_html = new_html.replace(option9, option9 + option10, 1)
        count += 1
    print(f"✓ 已更新 {count} 个下拉菜单")
    
    # 4. 套数名称映射 (需要处理多个位置)
    map9 = "9: '第九套'"
    map10 = ", 10: '第十套'"
    
    count = 0
    while map9 in new_html:
        # 检查是否已经添加过了
        pos = new_html.find(map9)
        if pos + len(map9) < len(new_html) and new_html[pos + len(map9):pos + len(map9) + len(map10)] == map10:
            # 已经添加过了，跳过
            break
        new_html = new_html.replace(map9, map9 + map10, 1)
        count += 1
    print(f"✓ 已更新 {count} 个套数映射")
    
    # 步骤5: 写入更新后的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("\n✓ index.html已成功更新!")
    
    # 验证
    with open(index_path, 'r', encoding='utf-8') as f:
        final_html = f.read()
    
    print("\n验证结果:")
    print(f"  第十套按钮: {'第十套</button>' in final_html}")
    print(f"  第十套选项: {'第十套</option>' in final_html}")
    print(f"  uid:1101: {'"uid":1101' in final_html}")
    print(f"  set:10: {'"set":10' in final_html or '"set": 10' in final_html}")
    
    # 验证题目数量
    if len(all_questions) == 1000:
        print("\n✓ 题目总数正确: 1000道 (10套×100道)")
    else:
        print(f"\n⚠ 题目总数: {len(all_questions)}道")

if __name__ == '__main__':
    main()
