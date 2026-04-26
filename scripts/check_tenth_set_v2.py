from docx import Document
import sys

# 设置标准输出编码为 utf-8
sys.stdout.reconfigure(encoding='utf-8')

# 读取第十套题目
doc = Document('c:\\Users\\86183\\Desktop\\111\\第十套.docx')

print("=== 文档内容（前100个段落）===")

# 打印前100个段落，了解文档结构
for i, para in enumerate(doc.paragraphs[:100]):
    if para.text.strip():
        print(f"[{i}] {para.text}")
