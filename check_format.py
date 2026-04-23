
from docx import Document

doc = Document('第三套.docx')
paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

print("=" * 80)
print("前 50 段内容预览：")
print("=" * 80)
for i, p in enumerate(paragraphs[:50]):
    print(f"{i:2d}. {p}")
print("\n" + "=" * 80)
print("后 20 段内容预览：")
print("=" * 80)
for i, p in enumerate(paragraphs[-20:], start=len(paragraphs)-20):
    print(f"{i:2d}. {p}")
