import json

def fix_set3_true_false():
    print('=' * 60)
    print('修复第3套题61-80题判断题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 定义需要修改的题目
    fixes = {
        269: False,  # 第69题：选举采用无记名投票，不是记名
        275: False,  # 第75题：质量很重要
        278: False   # 第78题：党是领导一切的，不是人民
    }
    
    updated_count = 0
    
    # 更新题目
    for q in questions:
        if q['id'] in fixes:
            old_answer = q['answer']
            new_answer = fixes[q['id']]
            
            if old_answer != new_answer:
                q_num = q['id'] - 200
                old_str = '正确' if old_answer else '错误'
                new_str = '正确' if new_answer else '错误'
                print(f'第 {q_num} 题（id={q["id"]}）：{old_str} -> {new_str}')
                q['answer'] = new_answer
                updated_count += 1
    
    print()
    
    if updated_count > 0:
        # 保存更新后的数据
        with open('data/questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] 修复完成！共更新 {updated_count} 道题')
        
        # 同时更新index.html
        print()
        print('正在更新 index.html...')
        update_index_html(questions)
    else:
        print('[OK] 无需修复，答案已经正确')
    
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
    fix_set3_true_false()
