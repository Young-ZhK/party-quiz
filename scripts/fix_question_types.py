import json

# 读取questions.json文件
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 修复第一套题的第21-40题，将类型从multiple_choice改为single_choice
for q in questions:
    if q['set'] == 1 and 21 <= q['id'] <= 40:
        q['type'] = 'single_choice'

# 保存修复后的文件
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("修复完成！第一套题第21-40题已从多选题改为单选题。")
