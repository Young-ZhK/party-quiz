import json
import sys

# 设置标准输出编码为 utf-8
sys.stdout.reconfigure(encoding='utf-8')

# 读取 questions.json 中的第十套题目
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 筛选第十套题目
tenth_set_questions = [q for q in questions if q.get('set') == 10]

print(f"第十套题目数量: {len(tenth_set_questions)}")

# 生成 JavaScript 格式的题目数据
js_content = json.dumps(tenth_set_questions, ensure_ascii=False)

print("\n第十套题目数据长度:", len(js_content))

# 将题目数据写入临时文件，供下一步使用
with open('c:\\Users\\86183\\Desktop\\111\\111\\scripts\\tenth_set_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("\n已将第十套题目数据保存到 tenth_set_data.js")