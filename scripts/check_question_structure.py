import json

def check_question_structure():
    print('=' * 60)
    print('检查题目数据结构')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 打印前几道题的信息
    for i, q in enumerate(questions[:10]):
        print(f'题目 {i+1}:')
        print(f'  id: {q.get("id")}')
        print(f'  uid: {q.get("uid")}')
        print(f'  set: {q.get("set")}')
        print(f'  type: {q.get("type")}')
        print(f'  answer: {q.get("answer")}')
        print(f'  question: {q.get("question")[:30]}...')
        print()
    
    print('=' * 60)

if __name__ == '__main__':
    check_question_structure()
