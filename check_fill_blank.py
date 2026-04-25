
import json

with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print("="*80)
print("检查第七套和第八套的填空题")
print("="*80)

for q in questions:
    if q['set'] in [7,8] and q['type'] == 'fill_blank':
        print(f"\n第{q['set']}套 - 第{q['id']}题")
        print(f"题目: {q['question']}")
        print(f"答案: {q['answer']}")
        print(f"选项: {q['options']}")
        print("-"*80)

# 统计一下
count_7 = sum(1 for q in questions if q['set'] == 7 and q['type'] == 'fill_blank')
count_8 = sum(1 for q in questions if q['set'] == 8 and q['type'] == 'fill_blank')
print(f"\n第七套填空题数量: {count_7}")
print(f"第八套填空题数量: {count_8}")
print(f"合计: {count_7 + count_8}")
