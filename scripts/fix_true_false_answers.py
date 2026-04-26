
import json

def fix_true_false_answers():
    print('=' * 60)
    print('修复判断题答案格式')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    fixed_count = 0
    
    # 修复所有判断题答案
    for q in questions:
        if q.get('type') == 'true_false':
            answer = q.get('answer')
            if isinstance(answer, str):
                # 如果是字符串格式，转换为布尔值
                if '正确' in answer or answer.upper() == 'A':
                    q['answer'] = True
                    fixed_count += 1
                    print(f'修复 uid={q["uid"]}: "{answer}" -> true')
                elif '错误' in answer or answer.upper() == 'B':
                    q['answer'] = False
                    fixed_count += 1
                    print(f'修复 uid={q["uid"]}: "{answer}" -> false')
    
    print()
    print(f'共修复 {fixed_count} 道题')
    print()
    
    # 保存修复后的数据
    with open('data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print('[OK] 已保存到 data/questions.json')
    
    # 同时更新index.html
    print()
    print('正在更新 index.html...')
    
    # 将题目数据转换为单行JSON字符串
    questions_json = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))
    
    # 读取 index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 查找并替换题目数据部分
    start_marker = '// ========== 嵌入式题目数据（共'
    end_marker = '// ========== 折叠功能 =========='
    
    start_idx = index_html.find(start_marker)
    if start_idx == -1:
        print('[ERROR] 未找到题目数据起始标记')
        return False
    
    # 找到题目数据开始的地方（在const allQuestionsData =之后）
    data_start_idx = index_html.find('const allQuestionsData =', start_idx)
    if data_start_idx == -1:
        print('[ERROR] 未找到 allQuestionsData 定义')
        return False
    
    data_start_idx += len('const allQuestionsData =')
    end_idx = index_html.find(end_marker, data_start_idx)
    if end_idx == -1:
        print('[ERROR] 未找到题目数据结束标记')
        return False
    
    # 替换数据
    new_html = index_html[:data_start_idx] + questions_json + index_html[end_idx:]
    
    # 保存更新后的 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print('[OK] 成功更新 index.html')
    print('=' * 60)

if __name__ == '__main__':
    fix_true_false_answers()
