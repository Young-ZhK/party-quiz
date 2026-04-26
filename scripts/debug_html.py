import json
import re

# 读取 index.html
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"index.html 文件大小: {len(html_content)} 字符")

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

# 找到 allQuestionsData 的起始位置
array_start = html_content.find('const allQuestionsData =[', data_start)
if array_start == -1:
    print("错误：无法找到 allQuestionsData 的起始位置")
    exit(1)

print(f"找到数组起始位置: {array_start}")

# 找到下一个 function 的位置
next_function = html_content.find('\n    function ', array_start)
if next_function == -1:
    print("错误：无法找到下一个 function")
    exit(1)

print(f"找到下一个 function 位置: {next_function}")

# 计算数据范围
data_length = next_function - array_start
print(f"数据长度: {data_length} 字符")

# 查找是否包含 uid":1101
if '"uid":1101' in html_content:
    print("找到 uid:1101")
else:
    print("未找到 uid:1101")

# 查找是否包含 "set": 10
if '"set": 10' in html_content:
    print("找到 set: 10")
else:
    print("未找到 set: 10")

# 查找 "set":10 (无空格)
if '"set":10' in html_content:
    print("找到 set:10 (无空格)")
else:
    print("未找到 set:10 (无空格)")

# 查找数据结束标记
data_end_marker = ']]// ========== 折叠功能 =========='
data_end_pos = html_content.find(data_end_marker)
if data_end_pos != -1:
    print(f"找到数据结束标记在位置: {data_end_pos}")
else:
    print("未找到数据结束标记")

# 查找所有 ] 后面跟换行和 // 的位置
for i in range(next_function - 500, next_function):
    if html_content[i] == ']':
        if i + 1 < next_function and html_content[i+1:i+3] == '\n//':
            print(f"找到可能的数组结束位置: {i}")
            print(f"上下文: {repr(html_content[i-30:i+50])}")
