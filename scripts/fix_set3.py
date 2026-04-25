import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

fixed_count = 0

for q in all_questions:
    # 只修复第三套的题目
    if q.get('set') == 3:
        if q['type'] == 'multiple_choice' and len(q['options']) == 2:
            # 把类型改为 true_false
            q['type'] = 'true_false'
            # 移除 options 字段（判断题不需要）
            if 'options' in q:
                del q['options']
            # 解析答案
            answer = q['answer']
            if 'A' in answer or '正确' in answer:
                q['answer'] = True
            elif 'B' in answer or '错误' in answer:
                q['answer'] = False
            fixed_count += 1
            print(f"Fixed id={q['id']}: answer={q['answer']}")

# 保存修复后的文件
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"\n共修复了 {fixed_count} 道题目")
