
import json

with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print("="*80)
print("检查所有套题的题型分布")
print("="*80)

for set_num in range(1,9):
    set_qs = [q for q in questions if q['set'] == set_num]
    single = sum(1 for q in set_qs if q['type'] == 'single_choice')
    multi = sum(1 for q in set_qs if q['type'] == 'multiple_choice')
    tf = sum(1 for q in set_qs if q['type'] == 'true_false')
    fill = sum(1 for q in set_qs if q['type'] == 'fill_blank')
    
    print(f"\n第{set_num}套:")
    print(f"  单选题: {single}")
    print(f"  多选题: {multi}")
    print(f"  判断题: {tf}")
    print(f"  填空题: {fill}")
    print(f"  合计: {len(set_qs)}")

print("\n"+"="*80)
print("第1-6套题型分布（作为参考）:")
for set_num in range(1,7):
    set_qs = [q for q in questions if q['set'] == set_num]
    fill = sum(1 for q in set_qs if q['type'] == 'fill_blank')
    print(f"第{set_num}套填空题: {fill}题")
