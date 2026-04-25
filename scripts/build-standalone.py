import json

# 读取题目
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把题目转成JSON字符串
questions_json = json.dumps(questions, ensure_ascii=False)

# 读取模板
with open('standalone-search.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替换占位符
final_html = html_content.replace('[QUESTIONS_DATA_HERE]', questions_json)

# 保存最终版本
with open('complete-search.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("OK 完成！")
print("已生成：complete-search.html")
print("直接双击这个文件就能用！")
