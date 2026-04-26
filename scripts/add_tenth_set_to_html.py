import json
import re

# 读取 questions.json 中的第十套题目
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 筛选第十套题目
tenth_set_questions = [q for q in questions if q.get('set') == 10]

# 生成 JavaScript 格式的题目数据
tenth_set_js = json.dumps(tenth_set_questions, ensure_ascii=False)

print(f"第十套题目数量: {len(tenth_set_questions)}")
print(f"第十套题目数据长度: {len(tenth_set_js)}")

# 读取 index.html
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到嵌入式数据的起始位置
marker = '// ========== 嵌入式题目数据'
data_start = html_content.find(marker)
if data_start == -1:
    print("错误：无法找到嵌入式题目数据的起始位置")
    exit(1)

# 用正则表达式提取当前题目数量
count_match = re.search(r'嵌入式题目数据（共(\d+)道题）', html_content[data_start:data_start+100])
if count_match:
    current_count = int(count_match.group(1))
    print(f"当前题目数量: {current_count}")
else:
    print("错误：无法解析当前题目数量")
    exit(1)

# 找到数据结束位置
data_end_marker = ']]// ========== 折叠功能 =========='
data_end_pos = html_content.find(data_end_marker)
if data_end_pos == -1:
    print("错误：无法找到数据的结束位置")
    exit(1)

print(f"找到数据结束位置: {data_end_pos}")

# 在数据结束标记之前插入第十套题目的数据
# 数据格式是 [...}...]，我们需要插入为 [...}, {第十套数据}...]
# 所以应该在 ]] 之前插入 ,tenth_set_js
insert_pos = data_end_pos  # 在 ]] 之前

new_html = html_content[:insert_pos] + ',' + tenth_set_js + html_content[insert_pos:]

# 更新注释中的题目数量
new_count = current_count + len(tenth_set_questions)
new_html = new_html.replace(
    f'// ========== 嵌入式题目数据（共{current_count}道题）==========',
    f'// ========== 嵌入式题目数据（共{new_count}道题）=========='
)

# 保存更新后的 index.html
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"\n已成功将第十套题目添加到 index.html")
print(f"题目总数已更新为 {new_count} 道")

# 验证
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'r', encoding='utf-8') as f:
    verify_content = f.read()

if '"uid":1101' in verify_content:
    print("验证成功：第十套题目已添加到 index.html")
else:
    print("验证失败：第十套题目未找到")
