
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
    
    # 匹配题目开头
    match = re.match(r'^(\d+)[、.].*', text)
    if match:
        if current_question:
            questions.append(current_question)
        
        num = int(match.group(1))
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
            'type': q_type,
            'question': '',
            'options': [],
            'answer': '',
            'explanation': ''
        }
        
        q_text = re.sub(r'^\d+[、.]\s*', '', text)
        current_question['question'] = q_text
        i += 1
        continue
    
    if current_question:
        # 检查选项
        option_match = re.match(r'^([A-D])[、.].*', text)
        if option_match and current_question['type'] in ['single_choice', 'multiple_choice']:
            opt = re.sub(r'^[A-D][、.\s]+', '', text)
            current_question['options'].append(opt)
            i += 1
            continue
        
        # 检查答案
        if '正确答案' in text:
            ans_match = re.search(r'正确答案[：:]\s*([A-Z（）()]+)', text)
            if ans_match:
                ans = ans_match.group(1)
                if current_question['type'] == 'true_false':
                    current_question['answer'] = 'A' in ans or '正确' in text
                else:
                    current_question['answer'] = ans.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
            i += 1
            continue
        
        if not current_question['answer']:
            current_question['question'] += ' ' + text
        i += 1
    else:
        i += 1

if current_question:
    questions.append(current_question)

# 处理填空题
fill_blanks = []
for p in paragraphs:
    match = re.match(r'^(\d+)[、.].*', p)
    if match:
        num = int(match.group(1))
        if 81 <= num <= 100:
            q_text = re.sub(r'^\d+[、.]\s*', '', p)
            ans_match = re.search(r'[（\(]([^）\)]+)[）\)]', q_text)
            answer = ''
            if ans_match:
                answer = ans_match.group(1)
                q_text = re.sub(r'[（\(][^）\)]+[）\)]', '____', q_text)
            fill_blanks.append({
                'id': num,
                'type': 'fill_blank',
                'question': q_text,
                'options': [],
                'answer': answer,
                'explanation': ''
            })

questions = [q for q in questions if q['type'] != 'fill_blank']
questions.extend(fill_blanks)
questions.sort(key=lambda x: x['id'])

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print('Successfully parsed', len(questions), 'questions')
print('Single choice:', len([q for q in questions if q['type'] == 'single_choice']))
print('Multiple choice:', len([q for q in questions if q['type'] == 'multiple_choice']))
print('True/false:', len([q for q in questions if q['type'] == 'true_false']))
print('Fill blank:', len([q for q in questions if q['type'] == 'fill_blank']))
