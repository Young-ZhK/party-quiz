import json

def fix_set_2_65():
    print('=' * 60)
    print('检查并修复第 2 套题第 65 题（id=165）')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 查找第2套题第65题（id=165）
    found = False
    for q in questions:
        if q['set'] == 2 and q['id'] == 165:
            found = True
            current_answer = q['answer']
            current_str = '正确' if current_answer else '错误'
            expected_str = '错误'
            
            print(f'第 2 套题第 65 题（id=165）')
            print(f'题目：{q["question"]}')
            print(f'当前答案：{current_str}')
            print(f'应该是：{expected_str}')
            print()
            
            if current_answer is not False:
                q['answer'] = False
                print('[OK] 已将答案更新为：错误')
                
                # 保存更新后的数据
                with open('data/questions.json', 'w', encoding='utf-8') as f:
                    json.dump(questions, f, ensure_ascii=False, indent=2)
                
                print('[OK] 已保存到 data/questions.json')
                
                # 现在更新 index.html
                print()
                print('正在更新 index.html...')
                update_index_html()
            else:
                print('[OK] 答案已经是正确的了')
            break
    
    if not found:
        print('[!] 未找到第 2 套题第 65 题（id=165）')
    
    print('=' * 60)

def update_index_html():
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 将题目数据转换为单行JSON字符串
    questions_json = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))
    
    # 读取 index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 查找并替换题目数据部分
    start_marker = '// ========== 嵌入式题目数据（共800道题）==========\n    const allQuestionsData = '
    end_marker = '\n    \n    // ========== 折叠功能 =========='
    
    start_idx = index_html.find(start_marker)
    if start_idx == -1:
        print('[!] 未找到题目数据起始标记')
        return False
    
    start_idx += len(start_marker)
    end_idx = index_html.find(end_marker, start_idx)
    if end_idx == -1:
        print('[!] 未找到题目数据结束标记')
        return False
    
    # 替换数据
    new_html = index_html[:start_idx] + questions_json + index_html[end_idx:]
    
    # 保存更新后的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f'[OK] 成功更新 index.html，共 {len(questions)} 道题')
    return True

if __name__ == '__main__':
    fix_set_2_65()
