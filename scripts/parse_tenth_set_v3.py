import json
from docx import Document
import re

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

    # 检查是否是题目开始 - 格式: 1、【单选题】 或 1、【多选题】 等
    if '、【单选题】' in text or '、【多选题】' in text or '、【判断题】' in text or '、【填空题】' in text:
        # 保存上一个题目
        if current_question:
            new_questions.append(current_question)

        # 解析题目类型
        if '【单选题】' in text:
            q_type = 'single_choice'
        elif '【多选题】' in text:
            q_type = 'multiple_choice'
        elif '【判断题】' in text:
            q_type = 'true_false'
        elif '【填空题】' in text:
            q_type = 'fill_blank'
        else:
            q_type = 'single_choice'  # 默认类型

        # 提取题目内容 - 去掉题号和类型标记
        if '【单选题】' in text:
            q_text = text.split('【单选题】')[1].strip()
        elif '【多选题】' in text:
            q_text = text.split('【多选题】')[1].strip()
        elif '【判断题】' in text:
            q_text = text.split('【判断题】')[1].strip()
        elif '【填空题】' in text:
            q_text = text.split('【填空题】')[1].strip()
        else:
            q_text = text

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
        continue

    # 检查是否是选项
    if current_question and current_question['type'] in ['single_choice', 'multiple_choice']:
        if text.startswith('A、') or text.startswith('B、') or text.startswith('C、') or text.startswith('D、') or text.startswith('E、'):
            # 提取选项内容（去掉开头的 A、B、C、D、E 和、）
            opt_text = text[2:].strip() if len(text) > 2 else text
            current_question['options'].append(opt_text)
            continue

    # 检查是否是答案 (格式: 正确答案：B易错率：15.25%)
    # 注意：这里的冒号是全角冒号
    if current_question and '正确答案' in text:
        # 提取答案字母
        answer_match = re.search(r'正确答案：([A-Z]+)', text)
        if answer_match:
            current_question['answer'] = answer_match.group(1)
        continue

# 保存最后一个题目
if current_question:
    new_questions.append(current_question)

# 更新 questions.json 中的第十套题目
# 先删除旧的第十套题目
questions = [q for q in questions if q.get('set') != 10]

# 添加新的第十套题目
questions.extend(new_questions)

# 保存更新后的 questions.json 文件
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"成功解析并添加了 {len(new_questions)} 道题目到第十套")
print(f"总题目数: {len(questions)}")

# 显示前5道题目的答案，确认解析正确
for i, q in enumerate(new_questions[:5]):
    print(f"\n题目 {i+1}: {q['question'][:50]}...")
    print(f"答案: {q['answer']}")
    print(f"选项数: {len(q['options'])}")
