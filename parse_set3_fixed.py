
from docx import Document
import json
import re

print("=" * 60)
print("  解析第三套题库（修正版）")
print("=" * 60)

doc = Document('第三套.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

questions = []
i = 0

while i < len(paragraphs):
    text = paragraphs[i]
    
    # 匹配题目
    match = re.match(r'^(\d+)\.\s+(.+)$', text)
    if match:
        num = int(match.group(1))
        q_text = match.group(2)
        
        # 确定题型
        if 1 <= num <= 40:
            q_type = 'single_choice'
        elif 41 <= num <= 80:
            q_type = 'multiple_choice'
        elif 81 <= num <= 90:
            q_type = 'true_false'
        else:
            q_type = 'fill_blank'
        
        question = {
            'id': num,
            'set': 3,
            'type': q_type,
            'question': q_text,
            'options': [],
            'answer': '',
            'explanation': '',
            'uid': 200 + num
        }
        
        i += 1
        
        # 读取选项（如果是选择题）
        if q_type in ['single_choice', 'multiple_choice'] and i < len(paragraphs):
            option_line = paragraphs[i]
            if re.match(r'^[A-D]、', option_line):
                # 分割选项
                options = re.split(r'[A-D]、', option_line)[1:]  # 去掉开头的空字符串
                question['options'] = [opt.strip() for opt in options]
                i += 1
        
        # 读取答案
        if i < len(paragraphs) and '答案' in paragraphs[i]:
            ans_match = re.search(r'答案[：:]\s*(.+)', paragraphs[i])
            if ans_match:
                ans = ans_match.group(1).strip()
                if q_type == 'true_false':
                    question['answer'] = '正确' in ans or ans == 'A'
                else:
                    question['answer'] = ans
            i += 1
        
        questions.append(question)
        continue
    
    i += 1

print(f"\n解析完成！共 {len(questions)} 题")
print(f"- 单选题: {len([q for q in questions if q['type'] == 'single_choice'])} 题")
print(f"- 多选题: {len([q for q in questions if q['type'] == 'multiple_choice'])} 题")
print(f"- 判断题: {len([q for q in questions if q['type'] == 'true_false'])} 题")
print(f"- 填空题: {len([q for q in questions if q['type'] == 'fill_blank'])} 题")

# 保存第三套题目
with open('第三套.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("\n已保存到 第三套.json")

# 合并到主题库
print("\n" + "=" * 60)
print("  合并到主题库")
print("=" * 60)

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

print(f"当前题库: {len(all_questions)} 题")

# 移除旧的第三套
all_questions = [q for q in all_questions if q.get('set') != 3]

# 添加新的第三套
all_questions.extend(questions)

# 排序
all_questions.sort(key=lambda x: (x.get('set', 1), x.get('id', 0)))

# 重新分配uid
uid = 1
for q in all_questions:
    q['uid'] = uid
    uid += 1

# 备份旧文件
import os
import shutil
if os.path.exists('questions_backup.json'):
    os.remove('questions_backup.json')
shutil.copy('questions.json', 'questions_backup.json')
print("已备份到 questions_backup.json")

# 保存新题库
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

set1 = len([q for q in all_questions if q.get('set') == 1])
set2 = len([q for q in all_questions if q.get('set') == 2])
set3 = len([q for q in all_questions if q.get('set') == 3])

print(f"\n合并成功！")
print(f"题库现在共有: {len(all_questions)} 题")
print(f"- 第一套: {set1} 题")
print(f"- 第二套: {set2} 题")
print(f"- 第三套: {set3} 题")
print("\n完成！")
