import json

def check_all_sets_debug():
    print('=' * 60)
    print('调试：检查所有套题')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f'总题目数：{len(questions)}')
    print()
    
    # 统计每套题的数量
    set_counts = {}
    for q in questions:
        s = q.get('set')
        set_counts[s] = set_counts.get(s, 0) + 1
    
    print('每套题数量：')
    for s in sorted(set_counts.keys()):
        print(f'  第 {s} 套：{set_counts[s]} 题')
    print()
    
    # 查看第2套题
    print('查看第 2 套题前10题：')
    set_2 = [q for q in questions if q.get('set') == 2]
    for i, q in enumerate(set_2[:10]):
        print(f'  {i+1}. id={q.get("id")}, type={q.get("type")}')
        print(f'     {q.get("question", "")[:30]}...')
    print()
    
    print('=' * 60)

if __name__ == '__main__':
    check_all_sets_debug()
