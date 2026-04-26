from docx import Document
import re

# 读取第十套题目
doc = Document('c:\\Users\\86183\\Desktop\\111\\第十套.docx')

# 查找所有包含"正确答案"的段落
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if '正确答案' in text:
        print(f"[{i}] '{text}'")
        print(f"    编码: {text.encode('utf-8')}")
        print(f"    '正确答案' in text: {'正确答案' in text}")
        print(f"    '正确答案：' in text: {'正确答案：' in text}")
        print(f"    re.search result: {re.search(r'正确答案锛欱([A-Z]+)', text)}")
        break
