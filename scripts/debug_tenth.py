from docx import Document

# 读取第十套题目
doc = Document('c:\\Users\\86183\\Desktop\\111\\第十套.docx')

# 打印前20个非空段落
count = 0
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text and count < 20:
        print(f"[{i}] '{text}'")
        count += 1
