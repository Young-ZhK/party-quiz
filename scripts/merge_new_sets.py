
import json
import os

# 读取原来的
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json') as f:
    old_questions = json.load(f)

# 读取新解析的
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', '第四套-第六套.json') as f:
    new_questions = json.load(f)

# 合并
all_questions = old_questions + new_questions

# 重新编号
for i, q in enumerate(all_questions):
    q['id'] = i + 1

# 统计
count_by_set = {}
for q in all_questions:
    s = q['set']
    count_by_set[s] = count_by_set.get(s, 0) + 1

print(f"合并完成！统计：")
for set_num in sorted(count_by_set.keys()):
    print(f"第{set_num}套: {count_by_set[set_num]}题")
print(f"总题数: {len(all_questions)}题")

# 保存
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"已保存到: {output_path}")
