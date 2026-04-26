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

# 读取 index.html
with open('c:\\Users\\86183\\Desktop\\111\\111\\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 查找第一道题目的内容在 index.html 中的位置
first_question_text = tenth_set_questions[0]['question'][:20]
print(f"搜索第一道题目内容: {first_question_text}")

if first_question_text in html_content:
    print("找到第一道题目内容在 index.html 中!")
else:
    print("未找到第一道题目内容")

# 查找 uid 1101
uid_search = '"uid":1101'
if uid_search in html_content:
    print("找到 uid:1101 在 index.html 中!")
else:
    print("未找到 uid:1101")

# 查找 set: 10
set_search = '"set": 10'
if set_search in html_content:
    print("找到 set: 10 在 index.html 中!")
else:
    print("未找到 set: 10")
