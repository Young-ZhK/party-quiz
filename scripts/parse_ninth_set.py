
from docx import Document
import json
import os
import re

def parse_ninth_set():
    print('=' * 60)
    print('解析第九套题库')
    print('=' * 60)
    print()
    
    # 读取第九套题库
    doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '第九套.docx')
    doc = Document(doc_path)
    
    # 提取所有段落文本
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            lines.append(text)
    
    # 解析题目
    questions = []
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i]
        
        # 匹配题目格式："1. 【单选题】题目内容"
        match = re.match(r'^(\d+)\.\s*【([^】]+)】\s*(.+)$', line)
        
        if match:
            q_num = int(match.group(1))
            q_type_str = match.group(2)
            q_text = match.group(3)
            
            # 转换题目类型
            if q_type_str == '单选题':
                q_type = 'single_choice'
            elif q_type_str == '多选题':
                q_type = 'multiple_choice'
            elif q_type_str == '判断题':
                q_type = 'true_false'
            elif q_type_str == '填空题':
                q_type = 'fill_blank'
            else:
                q_type = 'single_choice'
            
            # 创建题目对象
            q = {
                'id': 800 + q_num,
                'set': 9,
                'type': q_type,
                'question': q_text,
                'options': [],
                'answer': '',
                'explanation': '',
                'uid': 900 + q_num
            }
            
            i += 1
            
            # 解析选项和答案
            if q_type == 'true_false':
                # 判断题
                # 应该有A、正确和B、错误
                while i < n:
                    line_i = lines[i]
                    if line_i.startswith('A、') or line_i.startswith('A.'):
                        pass  # 正确选项
                    elif line_i.startswith('B、') or line_i.startswith('B.'):
                        pass  # 错误选项
                    elif line_i.startswith('正确答案：'):
                        # 解析答案
                        answer_match = re.search(r'正确答案：([AB])', line_i)
                        if answer_match:
                            ans_char = answer_match.group(1)
                            q['answer'] = (ans_char == 'A')
                        break
                    i += 1
            
            elif q_type == 'fill_blank':
                # 填空题
                while i < n:
                    line_i = lines[i]
                    if line_i.startswith('正确答案：'):
                        q['answer'] = line_i[5:].strip()
                        break
                    i += 1
            
            else:
                # 单选题或多选题
                options = []
                
                while i < n:
                    line_i = lines[i]
                    
                    # 解析选项
                    opt_match = re.match(r'^([A-H])[、.](.+)$', line_i)
                    if opt_match:
                        options.append(opt_match.group(2).strip())
                    elif line_i.startswith('正确答案：'):
                        # 解析答案
                        answer_match = re.search(r'正确答案：([A-H]+)', line_i)
                        if answer_match:
                            q['answer'] = answer_match.group(1)
                        break
                    
                    i += 1
                
                q['options'] = options
            
            questions.append(q)
            print(f"已解析第{q_num}题 ({q_type_str})")
        
        i += 1
    
    print()
    print(f"共解析 {len(questions)} 道题")
    print()
    
    # 读取现有题目
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json'), 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 添加第九套题
    all_questions.extend(questions)
    
    # 保存更新后的题目
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json'), 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print("[OK] 已保存到 data/questions.json")
    
    # 同时更新index.html
    print()
    print('正在更新 index.html...')
    update_index_html(all_questions)
    
    print('=' * 60)

def update_index_html(questions_data):
    # 将题目数据转换为单行JSON字符串
    questions_json = json.dumps(questions_data, ensure_ascii=False, separators=(',', ':'))
    
    # 读取 index.html
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html'), 'r', encoding='utf-8') as f:
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
    
    # 更新注释
    new_html = new_html.replace('// ========== 嵌入式题目数据（共800道题）==========',
                                 '// ========== 嵌入式题目数据（共900道题）==========')
    
    # 保存更新后的 index.html
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'index.html'), 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print('[OK] 成功更新 index.html')
    return True

if __name__ == '__main__':
    parse_ninth_set()
