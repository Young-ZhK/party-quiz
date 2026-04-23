
from PIL import Image
import pytesseract
import sys

try:
    print("正在加载图片...")
    img = Image.open('第三套.png')
    
    print("正在使用OCR识别文字...")
    text = pytesseract.image_to_string(img, lang='chi_sim')
    
    print("\n识别成功！识别到的文字内容：")
    print("=" * 80)
    print(text)
    print("=" * 80)
    
    with open('第三套_ocr.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("\n文本已保存到：第三套_ocr.txt")
    
except ImportError as e:
    print(f"错误: {e}")
    print("\n提示：")
    print("OCR可能需要安装以下库：")
    print("pip install pillow pytesseract")
    print("\n同时还需要安装Tesseract OCR引擎：")
    print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    print("配置tesseract路径可能需要指定路径")

