import json

def add_uid_to_all():
    print('=' * 60)
    print('为所有题目添加uid字段')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    updated = 0
    
    # 为所有题目添加uid
    for q in questions:
        if 'uid' not in q or q['uid'] is None:
            # uid = set * 100 + id（在套题内的编号）
            q_num_in_set = q['id'] - (q['set'] - 1) * 100
            q['uid'] = q['set'] * 100 + q_num_in_set
            updated += 1
    
    print(f'共为 {updated} 道题添加了uid')
    print()
    
    # 保存更新后的数据
    with open('data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print('[OK] 已保存到 data/questions.json')
    
    # 同时更新index.html
    print()
    print('正在更新 index.html...')
    update_index_html(questions)
    
    print('=' * 60)

def update_index_html(questions_data):
    # 将题目数据转换为单行JSON字符串
    questions_json = json.dumps(questions_data, ensure_ascii=False, separators=(',', ':'))
    
    # 读取 index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 查找并替换题目数据部分
    start_marker = '// ========== 嵌入式题目数据（共800道题）==========\n    const allQuestionsData = '
    end_marker = '\n    \n    // ========== 折叠功能 =========='
    
    start_idx = index_html.find(start_marker)
    if start_idx == -1:
        print('[ERROR] 未找到题目数据起始标记')
        return False
    
    start_idx += len(start_marker)
    end_idx = index_html.find(end_marker, start_idx)
    if end_idx == -1:
        print('[ERROR] 未找到题目数据结束标记')
        return False
    
    # 替换数据
    new_html = index_html[:start_idx] + questions_json + index_html[end_idx:]
    
    # 保存更新后的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print('[OK] 成功更新 index.html')
    return True

if __name__ == '__main__':
    add_uid_to_all()
