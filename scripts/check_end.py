import json
import sys

# 设置标准输出编码为 utf-8
sys.stdout.reconfigure(encoding='utf-8')

# 读取 index.html
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 查找数据结束标记
data_end_marker = ']]// ========== 折叠功能 =========='
data_end_pos = html_content.find(data_end_marker)
if data_end_pos != -1:
    print(f"找到数据结束标记在位置: {data_end_pos}")

    # 打印数据结束标记之前 500 字符的内容
    start_pos = max(0, data_end_pos - 500)
    content_before_end = html_content[start_pos:data_end_pos]

    print(f"\n=== 数据结束标记之前 500 字符 ===")
    print(content_before_end[-500:])
else:
    print("未找到数据结束标记")
