
import json

def verify_ninth_set():
    print('=' * 60)
    print('验证第九套题库')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json'), 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"总题目数：{len(questions)}")
    print()
    
    # 统计每套题的数量
    set_counts = {}
    for q in questions:
        s = q.get('set')
        set_counts[s] = set_counts.get(s, 0) + 1
    
    print('每套题数量：')
    for s in sorted(set_counts.keys()):
        print(f"  第{s}套：{set_counts[s]}题")
    print()
    
    # 验证第九套题
    print('验证第九套题：')
    ninth_questions = [q for q in questions if q['set'] == 9]
    if len(ninth_questions) != 100:
        print(f"  [ERROR] 第九套题应该有100道，但实际有{len(ninth_questions)}道")
    else:
        print("  [OK] 第九套题有100道题")
    
    # 验证题型分布
    type_counts = {}
    for q in ninth_questions:
        t = q['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print('第九套题题型分布：')
    type_names = {
        'single_choice': '单选题',
        'multiple_choice': '多选题',
        'true_false': '判断题',
        'fill_blank': '填空题'
    }
    
    expected = {
        'single_choice': 40,
        'multiple_choice': 20,
        'true_false': 20,
        'fill_blank': 20
    }
    
    for t in sorted(type_counts.keys()):
        name = type_names.get(t, t)
        e = expected.get(t, 0)
        a = type_counts[t]
        if e == a:
            print(f"  {name}：{a}题 [OK]")
        else:
            print(f"  {name}：{a}题（应该是{e}题）[ERROR]")
    
    # 验证uid
    uid_ok = True
    for q in ninth_questions:
        if q['uid'] is None:
            uid_ok = False
            break
    
    print()
    if uid_ok:
        print("[OK] 第九套题的uid都已正确设置")
    else:
        print("[ERROR] 第九套题的uid有问题")
    
    print()
    print('=' * 60)

import os
if __name__ == '__main__':
    verify_ninth_set()
