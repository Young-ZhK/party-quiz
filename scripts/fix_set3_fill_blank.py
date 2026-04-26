import json

def fix_set3_fill_blank():
    print('=' * 60)
    print('修复第3套题81-90题填空题答案')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 定义正确答案
    correct_answers = {
        281: '党小组会',
        282: '大局意识',
        283: '党组织',
        284: '思想',
        285: '生态保护红线',
        286: '人类命运共同体',
        287: '中华民族伟大复兴',
        288: '5|五',
        289: '零容忍',
        290: '乡村振兴'
    }
    
    updated_count = 0
    
    # 更新第3套题81-90题
    for q in questions:
        if q['id'] in correct_answers:
            old_answer = q['answer']
            new_answer = correct_answers[q['id']]
            
            if old_answer != new_answer:
                q_num = q['id'] - 200
                print(f'第 {q_num} 题（id={q["id"]}）：{old_answer} -> {new_answer}')
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
    fix_set3_fill_blank()
