
from docx import Document
import json
import re

doc = Document('党旗飘飘题库.docx')

questions = []
current_question = None

# 读取所有段落文本
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

i = 0
while i < len(paragraphs):
    text = paragraphs[i]
    
    # 匹配题目开头："1、..." 或 "1. "
    match = re.match(r'^(\d+)[、.].*', text)
    if match:
        if current_question:
            questions.append(current_question)
        
        # 确定题型
        num = int(match.group(1))
        if 1 &lt;= num &lt;= 20:
            question_type = 'single_choice'
        elif 21 &lt;= num &lt;= 60:
            question_type = 'multiple_choice'
        elif 61 &lt;= num &lt;= 80:
            question_type = 'true_false'
        else:
            question_type = 'fill_blank'
        
        current_question = {
            'id': num,
            'type': question_type,
            'question': '',
            'options': [],
            'answer': '',
            'explanation': ''
        }
        
        # 提取题目文本（去除题号）
        q_text = re.sub(r'^\d+[、.]\s*', '', text)
        current_question['question'] = q_text
        
        i += 1
        continue
    
    if current_question:
        # 检查是否是选项（A、B、C、D开头）
        option_match = re.match(r'^([A-D])[、.].*', text)
        if option_match and current_question['type'] in ['single_choice', 'multiple_choice']:
            opt = re.sub(r'^[A-D][、.\s]+', '', text)
            current_question['options'].append(opt)
            i += 1
            continue
        
        # 检查是否是正确答案
        if '正确答案' in text:
            ans_match = re.search(r'正确答案[：:]\s*([A-Z（）()]+)', text)
            if ans_match:
                ans = ans_match.group(1)
                # 处理判断题的答案
                if current_question['type'] == 'true_false':
                    current_question['answer'] = 'A' in ans or '正确' in text
                else:
                    current_question['answer'] = ans.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
            i += 1
            continue
        
        # 如果不是选项和答案都不是，可能是题目继续
        if not current_question['answer']:
            current_question['question'] += ' ' + text
        i += 1
    else:
        i += 1

# 添加最后一个题目
if current_question:
    questions.append(current_question)

# 处理填空题（从段落中提取）
fill_blank = []
for p in paragraphs:
    match = re.match(r'^(\d+)[、.].*', p)
    if match:
        num = int(match.group(1))
        if 81 &lt;= num &lt;= 100:
            q_text = re.sub(r'^\d+[、.]\s*', '', p)
            # 寻找答案（括号中的内容）
            ans_match = re.search(r'[（\(]([^）\)]+)[）\)]', q_text)
            answer = ''
            if ans_match:
                answer = ans_match.group(1)
                # 把答案替换为空白
                q_text = re.sub(r'[（\(][^）\)]+[）\)]', '____', q_text)
            fill_blank.append({
                'id': num,
                'type': 'fill_blank',
                'question': q_text,
                'options': [],
                'answer': answer,
                'explanation': ''
            })

# 更新填空题替换原来的填空题
questions = [q for q in questions if q['type'] != 'fill_blank']
questions.extend(fill_blank)

# 按ID排序
questions.sort(key=lambda x: x['id'])

# 保存为JSON
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f'成功解析 {len(questions)} 道题目')
print(f'单选题: {len([q for q in questions if q["type"] == "single_choice"])}')
print(f'多选题: {len([q for q in questions if q["type"] == "multiple_choice"])}')
print(f'判断题: {len([q for q in questions if q["type"] == "true_false"])}')
print(f'填空题: {len([q for q in questions if q["type"] == "fill_blank"])}')
