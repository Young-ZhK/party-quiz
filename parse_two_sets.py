
from docx import Document
import json
import re

doc = Document('党旗飘飘题库.docx')

# 读取所有段落文本
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# 检测分隔两套题的位置
split_index = None
for i, p in enumerate(paragraphs):
    if '入党积极分子' in p and '第二套' not in p and i > 100:
        split_index = i
        break

# 分割两套题
set1_paragraphs = paragraphs[:split_index] if split_index else paragraphs[:len(paragraphs)//2]
set2_paragraphs = paragraphs[split_index:] if split_index else paragraphs[len(paragraphs)//2:]

def parse_set(paragraphs, set_name):
    questions = []
    current_question = None
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
                'set': set_name,
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
                    'set': set_name,
                    'type': 'fill_blank',
                    'question': q_text,
                    'options': [],
                    'answer': answer,
                    'explanation': ''
                })
    
    questions = [q for q in questions if q['type'] != 'fill_blank']
    questions.extend(fill_blanks)
    questions.sort(key=lambda x: x['id'])
    return questions

set1 = parse_set(set1_paragraphs, 1)
set2 = parse_set(set2_paragraphs, 2)

# 给题目唯一ID
all_questions = []
uid = 1
for q in set1:
    q['uid'] = uid
    all_questions.append(q)
    uid += 1
for q in set2:
    q['uid'] = uid
    all_questions.append(q)
    uid += 1

with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f'第一套题: {len(set1)} 题')
print(f'第二套题: {len(set2)} 题')
print(f'总共: {len(all_questions)} 题')
