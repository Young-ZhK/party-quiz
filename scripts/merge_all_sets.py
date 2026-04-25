
import json
import re
import os

def parse_file(filepath, set_num):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    qid = 1
    
    # 按题目分隔（"【单选题】"、"【多选题】"、"【判断题】"、"【填空题】"开头）
    pattern = r'(【.*?题】.*?)(?=\n\d+、【|$)'
    parts = re.findall(pattern, content, re.DOTALL)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # 1. 确定题目类型
        qtype = 'single_choice'
        if '【多选题】' in part:
            qtype = 'multiple_choice'
        elif '【判断题】' in part:
            qtype = 'true_false'
        elif '【填空题】' in part:
            qtype = 'fill_blank'
        
        # 2. 提取题目文本（去掉前面的类型和序号）
        q_text = part
        # 去掉"【单选题】 "或类似
        q_text = re.sub(r'【.*?题】\s*', '', q_text)
        # 去掉前面的"1、 "等序号
        q_text = re.sub(r'^\d+、\s*', '', q_text)
        
        # 3. 分割题目和选项及答案
        # 查找"正确答案："的位置
        answer_idx = part.find('正确答案：')
        if answer_idx == -1:
            continue
        
        question_before_answer = part[:answer_idx].strip()
        
        # 提取选项
        options = []
        # 查找选项（A、B、C、D...）
        opt_pattern = r'\n\s*([A-Z])、\s*(.*?)(?=\n\s*[A-Z]、|$|\n\s*正确答案)'
        opts = re.findall(opt_pattern, question_before_answer, re.DOTALL)
        
        if opts:
            for label, opt_text in opts:
                options.append(opt_text.strip())
            # 提取题目主体（在选项之前的部分）
            first_opt_idx = question_before_answer.find(opts[0][0] + '、')
            if first_opt_idx != -1:
                q_text = question_before_answer[:first_opt_idx].strip()
        else:
            # 判断题、填空题，没有选项，提取题目
            first_ans_idx = question_before_answer.find('正确答案：')
            if first_ans_idx == -1:
                first_ans_idx = len(question_before_answer)
            q_text = question_before_answer[:first_ans_idx].strip()
        
        # 4. 提取正确答案
        ans_text = part[answer_idx + 5:].strip()
        # 去掉后面的"易错率：..."
        if '易错率' in ans_text:
            ans_text = ans_text.split('易错率')[0].strip()
        
        final_answer = ans_text
        if qtype == 'true_false':
            if '正确' in ans_text or '对' in ans_text or '√' in ans_text:
                final_answer = True
            elif '错误' in ans_text or '错' in ans_text or '×' in ans_text or 'X' in ans_text:
                final_answer = False
        
        # 5. 构建题目对象
        q_obj = {
            'id': qid,
            'set': set_num,
            'type': qtype,
            'question': q_text.strip(),
            'answer': final_answer,
            'options': options
        }
        questions.append(q_obj)
        qid += 1
    
    return questions

def main():
    base_path = r'c:\Users\86183\Desktop\111'
    data_path = os.path.join(os.path.dirname(base_path), '111', 'data')
    
    print('=== 开始合并所有套题 ===')
    
    # 读取原有的第1-3套
    print('读取第1-3套...')
    with open(r'c:\Users\86183\Desktop\111\111\backups\questions.json.backup_20260423_161505', 'r', encoding='utf-8') as f:
        old_123 = json.load(f)
    
    # 读取第4-6套
    print('读取第4-6套...')
    with open(r'c:\Users\86183\Desktop\111\111\data\第四套-第六套.json', 'r', encoding='utf-8') as f:
        set456 = json.load(f)
    
    # 解析第7-8套
    print('解析第7套...')
    set7 = parse_file(os.path.join(base_path, '第七套'), 7)
    print(f'第7套: {len(set7)}题')
    
    print('解析第8套...')
    set8 = parse_file(os.path.join(base_path, '第八套'), 8)
    print(f'第8套: {len(set8)}题')
    
    # 合并所有题目
    all_questions = old_123 + set456 + set7 + set8
    
    # 重新编号
    for i, q in enumerate(all_questions):
        q['id'] = i + 1
    
    # 保存
    print(f'保存完整题库（共 {len(all_questions)} 题）')
    with open(r'c:\Users\86183\Desktop\111\111\data\questions.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)
    
    print('合并完成！')
    
    # 验证
    print('\n=== 验证 ===')
    for set_num in range(1,9):
        count = sum(1 for q in all_questions if q['set'] == set_num)
        fill = sum(1 for q in all_questions if q['set'] == set_num and q['type'] == 'fill_blank')
        print(f'第{set_num}套: {count}题，填空题: {fill}题')

if __name__ == '__main__':
    main()
