import json
import re

# 读取题目数据
with open('questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修复选项
for question in data:
    if question['type'] in ['single_choice', 'multiple_choice']:
        options = question.get('options', [])
        
        # 检查是否只有一个选项，且包含多个选项
        if len(options) == 1 and isinstance(options[0], str):
            option_str = options[0]
            
            # 用正则表达式拆分选项
            # 匹配格式如 "A. xxx B. xxx" 或 "A、xxx B、xxx"
            parts = re.split(r'(?=[A-D][、\.])', option_str)
            
            # 过滤掉空字符串
            parts = [p.strip() for p in parts if p.strip()]
            
            # 如果拆分成功，更新options
            if len(parts) >= 2:
                # 清理每个选项，去掉前面的A. A、等
                cleaned_options = []
                for part in parts:
                    # 去掉开头的A. A、等
                    cleaned = re.sub(r'^[A-D][、\.]\s*', '', part)
                    if cleaned:
                        cleaned_options.append(cleaned)
                
                if cleaned_options:
                    question['options'] = cleaned_options
                    print(f"修复题目: {question['question']}")
                    print(f"  原选项: {option_str}")
                    print(f"  新选项: {cleaned_options}")
                    print()

# 保存修复后的数据
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("修复完成！")
