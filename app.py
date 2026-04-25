
from flask import Flask, jsonify, send_from_directory, request
import json
import random
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 读取题目数据
with open('data/questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    q_set = request.args.get('set', 'all')
    q_type = request.args.get('type', 'all')
    
    filtered = all_questions
    
    if q_set != 'all':
        filtered = [q for q in filtered if q.get('set') == int(q_set)]
    
    if q_type != 'all':
        filtered = [q for q in filtered if q['type'] == q_type]
    
    return jsonify(filtered)

@app.route('/api/random', methods=['GET'])
def get_random():
    count = int(request.args.get('count', 10))
    q_set = request.args.get('set', 'all')
    
    pool = all_questions
    if q_set != 'all':
        pool = [q for q in pool if q.get('set') == int(q_set)]
    
    random_questions = random.sample(pool, min(count, len(pool)))
    return jsonify(random_questions)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    answers = data.get('answers', {})
    results = []
    score = 0
    
    # 前端会传递 questions 参数吗？不，我们需要前端把当前 quiz 的题目列表也传过来
    # 但现在的实现没有传，所以我们需要另一种方式
    # 让我们先确保能正确匹配和处理所有已有的答案
    for uid, user_answer in answers.items():
        # 先尝试用 uid 匹配
        q = next((x for x in all_questions if str(x.get('uid')) == str(uid)), None)
        # 如果没找到，再用 id 匹配
        if not q:
            q = next((x for x in all_questions if str(x.get('id')) == str(uid)), None)
            
        if q:
            correct = False
            display_user_answer = user_answer
            display_correct_answer = q['answer']
            
            if q['type'] == 'true_false':
                # 处理判断题的布尔值和字符串情况
                user_bool = user_answer if isinstance(user_answer, bool) else str(user_answer).lower() in ('true', '1', 'yes', '正确')
                correct = user_bool == q['answer']
                display_user_answer = '正确' if user_bool else '错误'
                display_correct_answer = '正确' if q['answer'] else '错误'
            elif q['type'] == 'fill_blank':
                correct = str(user_answer).strip() == str(q['answer']).strip()
            elif q['type'] == 'multiple_choice':
                # 多选题：将用户答案和正确答案都排序后比较
                if isinstance(user_answer, list):
                    user_answer_str = ''.join(sorted(user_answer)).upper()
                    display_user_answer = ''.join(user_answer)
                else:
                    user_answer_str = str(user_answer).upper()
                correct_answer_str = ''.join(sorted(str(q['answer']).upper()))
                correct = user_answer_str == correct_answer_str
            else:
                # 单选题
                correct = str(user_answer).upper() == str(q['answer']).upper()
            
            if correct:
                score += 1
            
            results.append({
                'id': q.get('uid', q['id']),
                'original_id': q['id'],
                'set': q.get('set', 1),
                'correct': correct,
                'user_answer': display_user_answer,
                'correct_answer': display_correct_answer
            })
    
    return jsonify({
        'score': score,
        'total': len(results),
        'results': results
    })

if __name__ == '__main__':
    print(f'Loaded {len(all_questions)} questions total')
    set1_count = len([q for q in all_questions if q.get('set') == 1])
    set2_count = len([q for q in all_questions if q.get('set') == 2])
    set3_count = len([q for q in all_questions if q.get('set') == 3])
    set4_count = len([q for q in all_questions if q.get('set') == 4])
    set5_count = len([q for q in all_questions if q.get('set') == 5])
    set6_count = len([q for q in all_questions if q.get('set') == 6])
    print(f'第一套: {set1_count} 题, 第二套: {set2_count} 题, 第三套: {set3_count} 题, 第四套: {set4_count} 题, 第五套: {set5_count} 题, 第六套: {set6_count} 题')
    app.run(debug=True, host='0.0.0.0', port=5000)
