
from docx import Document
import json
import re

print("=" * 60)
print("  解析第三套题库")
print("=" * 60)

# 读取文档
doc = Document('第三套.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

print(f"读取到 {len(paragraphs)} 段文本")

# 解析题目
questions = []
current_question = None
i = 0

while i < len(paragraphs):
    text = paragraphs[i]
    
    # 匹配题目
    match = re.match(r'^(\d+)[、.].*', text)
    if match:
        if current_question:
            questions.append(current_question)
        
        num = int(match.group(1))
        
        # 判断题型
        if 1 <= num <= 20:
            q_type = 'single_choice'
        elif 21 <= num <= 60:
            q_type = 'multiple_choice'
        elif 61 <= num <= 80:
            q_type = 'true_false'
        else:
            q_type = 'fill_blank'
        
        current_question = {
            'id': num,
            'set': 3,
            'type': q_type,
            'question': '',
            'options': [],
            'answer': '',
            'explanation': '',
            'uid': 200 + num
        }
        
        # 提取题目文本
        q_text = re.sub(r'^\d+[、.]\s*', '', text)
        current_question['question'] = q_text
        i += 1
        continue
    
    if current_question:
        # 处理选项
        option_match = re.match(r'^([A-D])[、.].*', text)
        if option_match and current_question['type'] in ['single_choice', 'multiple_choice']:
            opt_text = re.sub(r'^[A-D][、.]\s*', '', text)
            current_question['options'].append(opt_text)
            i += 1
            continue
        
        # 处理答案
        if '正确答案' in text:
            ans_match = re.search(r'正确答案[：:]\s*([A-Z（）()正确错误]+)', text)
            if ans_match:
                ans = ans_match.group(1)
                ans = ans.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
                if current_question['type'] == 'true_false':
                    current_question['answer'] = '正确' in ans or 'A' in ans
                else:
                    current_question['answer'] = ans
            i += 1
            continue
        
        # 继续追加题目文本（如果还没找到答案）
        if not current_question['answer']:
            current_question['question'] += ' ' + text
        i += 1
    else:
        i += 1

# 添加最后一道题
if current_question:
    questions.append(current_question)

# 处理填空题 - 尝试从段落中提取
fill_blanks = []
for p in paragraphs:
    match = re.match(r'^(\d+)[、.].*', p)
    if match:
        num = int(match.group(1))
        if 81 <= num <= 100:
            q_text = re.sub(r'^\d+[、.]\s*', '', p)
            # 尝试提取答案
            ans = ''
            ans_match = re.search(r'[（\(]([^）\)]+)[）\)]', q_text)
            if ans_match:
                ans = ans_match.group(1)
                q_text = re.sub(r'[（\(][^）\)]+[）\)]', '____', q_text)
            fill_blanks.append({
                'id': num,
                'set': 3,
                'type': 'fill_blank',
                'question': q_text,
                'options': [],
                'answer': ans,
                'explanation': '',
                'uid': 200 + num
            })

# 合并题目 - 移除旧的填空题，添加新的
questions = [q for q in questions if q['type'] != 'fill_blank']
questions.extend(fill_blanks)

# 按id排序
questions.sort(key=lambda x: x['id'])

print(f"\n解析完成！共 {len(questions)} 题")
print(f"- 单选题: {len([q for q in questions if q['type'] == 'single_choice'])} 题")
print(f"- 多选题: {len([q for q in questions if q['type'] == 'multiple_choice'])} 题")
print(f"- 判断题: {len([q for q in questions if q['type'] == 'true_false'])} 题")
print(f"- 填空题: {len([q for q in questions if q['type'] == 'fill_blank'])} 题")

# 保存第三套题目
with open('第三套.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("\n✅ 已保存到 第三套.json")

# 现在合并到主题库
print("\n" + "=" * 60)
print("  合并到主题库")
print("=" * 60)

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

print(f"当前题库: {len(all_questions)} 题")

# 检查是否已有第三套
existing_set3 = [q for q in all_questions if q.get('set') == 3]
if existing_set3:
    print(f"发现旧的第三套: {len(existing_set3)} 题，正在移除...")
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

print(f"\n✅ 合并成功！")
print(f"题库现在共有: {len(all_questions)} 题")
print(f"- 第一套: {set1} 题")
print(f"- 第二套: {set2} 题")
print(f"- 第三套: {set3} 题")
print("\n完成！刷新浏览器即可使用！")
