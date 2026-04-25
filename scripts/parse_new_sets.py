
from docx import Document
import json
import os

doc_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '第四套-第六套.docx')
doc = Document(doc_path)

questions = []

currentSet = None
currentQuestion = None
currentOptions = []

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue
    
    # 检测新的套数
    if text == '第四套':
        currentSet = 4
        print("正在解析 第四套...")
        continue
    elif text == '第五套':
        currentSet = 5
        print("正在解析 第五套...")
        continue
    elif text == '第六套':
        currentSet = 6
        print("正在解析 第六套...")
        continue
    
    # 检测新题目：以数字开头，后面有【
    if ('【单选题】' in text or '【多选题】' in text or '【判断题】' in text or '【填空题】' in text) and (text[0].isdigit()):
        # 保存上一个题目
        if currentQuestion:
            if currentQuestion['type'] in ['single_choice', 'multiple_choice']:
                currentQuestion['options'] = currentOptions
            questions.append(currentQuestion)
        
        # 开始新题目
        currentOptions = []
        qType = None
        if '【单选题】' in text:
            qType = 'single_choice'
            text = text.replace('【单选题】', '')
        elif '【多选题】' in text:
            qType = 'multiple_choice'
            text = text.replace('【多选题】', '')
        elif '【判断题】' in text:
            qType = 'true_false'
            text = text.replace('【判断题】', '')
        elif '【填空题】' in text:
            qType = 'fill_blank'
            text = text.replace('【填空题】', '')
        
        # 去掉题目前面的数字和、
        if '、' in text:
            text = text.split('、', 1)[1]
        
        currentQuestion = {
            'id': len(questions) + 1,
            'set': currentSet,
            'type': qType,
            'question': text.strip()
        }
    
    # 检测选项
    elif (text.startswith('A、') or text.startswith('B、') or 
          text.startswith('C、') or text.startswith('D、') or 
          text.startswith('E、') or text.startswith('F、') or 
          text.startswith('G、') or text.startswith('H、')):
        currentOptions.append(text[2:].strip())
    
    # 检测答案（包含"正确答案："）
    elif '正确答案：' in text:
        if currentQuestion:
            # 找到正确答案
            idx = text.find('正确答案：')
            ansText = text[idx + 5:].strip()
            # 去掉后面的"易错率：..."
            if '易错率' in ansText:
                ansText = ansText.split('易错率')[0].strip()
            
            if currentQuestion['type'] == 'true_false':
                currentQuestion['answer'] = ansText in ['正确', '对', '√', 'A']
            else:
                currentQuestion['answer'] = ansText
    
    # 跳过"知识点："
    elif text == '知识点：':
        continue

# 保存最后一个题目
if currentQuestion:
    if currentQuestion['type'] in ['single_choice', 'multiple_choice']:
        currentQuestion['options'] = currentOptions
    questions.append(currentQuestion)

print(f"\n解析完成！共 {len(questions)} 题！")

# 按套数统计
countBySet = {}
for q in questions:
    s = q['set']
    countBySet[s] = countBySet.get(s, 0) + 1

for setNum in sorted(countBySet.keys()):
    print(f"第{setNum}套: {countBySet[setNum]} 题")

# 保存为JSON
outputPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '第四套-第六套.json')
with open(outputPath, 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"\n已保存到：{outputPath}")
