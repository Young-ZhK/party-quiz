import json
from docx import Document

# 读取第十套题目
doc = Document('c:\\Users\\86183\\Desktop\\111\\第十套.docx')

# 读取现有的 questions.json 文件
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 找出最大的 uid
max_uid = max(q['uid'] for q in questions) if questions else 0

# 解析题目
new_questions = []

current_question = None
question_id = 1

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue
    
    # 检查是否是题目开始
    if text.startswith('一、单选题'):
        continue
    elif text.startswith('二、多选题'):
        continue
    elif text.startswith('三、判断题'):
        continue
    elif text.startswith('四、填空题'):
        continue
    
    # 检查是否是题目编号
    if text.startswith('第') and '题' in text:
        # 保存上一个题目
        if current_question:
            new_questions.append(current_question)
        
        # 解析题目类型
        if '单选题' in text:
            q_type = 'single_choice'
        elif '多选题' in text:
            q_type = 'multiple_choice'
        elif '判断题' in text:
            q_type = 'true_false'
        elif '填空题' in text:
            q_type = 'fill_blank'
        else:
            q_type = 'single_choice'  # 默认类型
        
        # 提取题目内容
        q_text = text.split('。', 1)[1].strip() if '。' in text else text
        
        current_question = {
            'id': question_id,
            'set': 10,
            'type': q_type,
            'question': q_text,
            'options': [],
            'answer': '',
            'explanation': '',
            'uid': max_uid + len(new_questions) + 1
        }
        question_id += 1
    
    # 检查是否是选项
    elif current_question and current_question['type'] in ['single_choice', 'multiple_choice']:
        if text.startswith('A.') or text.startswith('B.') or text.startswith('C.') or text.startswith('D.') or text.startswith('E.'):
            current_question['options'].append(text[2:].strip())
    
    # 检查是否是答案
    elif current_question and ('答案：' in text or '答案:' in text):
        answer_part = text.split('答案：')[1].strip() if '答案：' in text else text.split('答案:')[1].strip()
        # 处理判断题答案
        if current_question['type'] == 'true_false':
            current_question['answer'] = answer_part == '对' or answer_part == '正确'
        else:
            current_question['answer'] = answer_part

# 保存最后一个题目
if current_question:
    new_questions.append(current_question)

# 将新题目添加到现有题目中
questions.extend(new_questions)

# 保存更新后的 questions.json 文件
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"成功解析并添加了 {len(new_questions)} 道题目到第十套")
print(f"总题目数: {len(questions)}")
