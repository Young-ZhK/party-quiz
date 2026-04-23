
from flask import Flask, jsonify, send_from_directory, request
import json
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 读取题目数据
with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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
    
    for uid, user_answer in answers.items():
        q = next((x for x in all_questions if str(x.get('uid', x['id'])) == str(uid)), None)
        if q:
            correct = False
            if q['type'] == 'true_false':
                correct = str(user_answer).lower() == str(q['answer']).lower()
            elif q['type'] == 'fill_blank':
                correct = str(user_answer).strip() == str(q['answer']).strip()
            else:
                correct = str(user_answer).upper() == str(q['answer']).upper()
            
            if correct:
                score += 1
            
            results.append({
                'id': q.get('uid', q['id']),
                'original_id': q['id'],
                'set': q.get('set', 1),
                'correct': correct,
                'user_answer': user_answer,
                'correct_answer': q['answer']
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
    print(f'第一套: {set1_count} 题, 第二套: {set2_count} 题, 第三套: {set3_count} 题')
    app.run(debug=True, host='0.0.0.0', port=5000)
