import json
import os

def main():
    base_path = r'c:\Users\86183\Desktop\111\111'
    data_path = os.path.join(base_path, 'data')
    
    # 1. 读取原来的完整题库
    print('读取现有题库...')
    with open(os.path.join(data_path, 'questions.json'), 'r', encoding='utf-8') as f:
        old_questions = json.load(f)
    
    # 2. 解析第七套和第八套
    print('解析第七套和第八套...')
    
    def parse_file(filepath, set_num):
        import re
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        questions = []
        qid = 1
        
        pattern = r'(【.*?题】.*?)(?=\n\d+、【|$)'
        parts = re.findall(pattern, content, re.DOTALL)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            qtype = 'single_choice'
            if '【多选题】' in part:
                qtype = 'multiple_choice'
            elif '【判断题】' in part:
                qtype = 'true_false'
            elif '【填空题】' in part:
                qtype = 'fill_blank'
            
            q_text = part
            q_text = re.sub(r'【.*?题】\s*', '', q_text)
            q_text = re.sub(r'^\d+、\s*', '', q_text)
            
            answer_idx = part.find('正确答案：')
            if answer_idx == -1:
                continue
            
            question_before_answer = part[:answer_idx].strip()
            
            options = []
            opt_pattern = r'\n\s*([A-Z])、\s*(.*?)(?=\n\s*[A-Z]、|$|\n\s*正确答案)'
            opts = re.findall(opt_pattern, question_before_answer, re.DOTALL)
            
            if opts:
                for label, opt_text in opts:
                    options.append(opt_text.strip())
                first_opt_idx = question_before_answer.find(opts[0][0] + '、')
                if first_opt_idx != -1:
                    q_text = question_before_answer[:first_opt_idx].strip()
            else:
                first_ans_idx = question_before_answer.find('正确答案：')
                if first_ans_idx == -1:
                    first_ans_idx = len(question_before_answer)
                q_text = question_before_answer[:first_ans_idx].strip()
            
            ans_text = part[answer_idx + 5:].strip()
            if '易错率' in ans_text:
                ans_text = ans_text.split('易错率')[0].strip()
            
            final_answer = ans_text
            if qtype == 'true_false':
                if '正确' in ans_text or '对' in ans_text or '√' in ans_text:
                    final_answer = True
                elif '错误' in ans_text or '错' in ans_text or '×' in ans_text or 'X' in ans_text:
                    final_answer = False
            
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
    
    set7 = parse_file(r'c:\Users\86183\Desktop\111\第七套', 7)
    set8 = parse_file(r'c:\Users\86183\Desktop\111\第八套', 8)
    
    print(f'第七套: {len(set7)}题')
    print(f'第八套: {len(set8)}题')
    
    # 3. 合并所有题目
    new_questions = old_questions + set7 + set8
    
    # 重新编号
    for i, q in enumerate(new_questions):
        q['id'] = i + 1
    
    # 4. 保存
    print(f'保存完整题库（共 {len(new_questions)} 题）')
    with open(os.path.join(data_path, 'questions.json'), 'w', encoding='utf-8') as f:
        json.dump(new_questions, f, ensure_ascii=False, indent=4)
    
    print('✅ 合并完成！')
    
    # 验证
    print('\n=== 验证 ===')
    for s in range(1, 9):
        cnt = sum(1 for q in new_questions if q['set'] == s)
        print(f'第{s}套: {cnt}题')
        # 检查是否有answer缺失
        missing = [q for q in new_questions if q['set'] == s and ('answer' not in q or q['answer'] is None)]
        if missing:
            print(f'  ❌ {len(missing)}题缺少答案')

if __name__ == '__main__':
    main()
