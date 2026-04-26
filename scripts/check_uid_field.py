import json

def check_uid_field():
    print('=' * 60)
    print('检查题目数据中的uid字段')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 统计uid的情况
    has_uid = 0
    no_uid = 0
    
    for q in questions:
        if 'uid' in q and q['uid'] is not None:
            has_uid += 1
        else:
            no_uid += 1
            # 输出前几个没有uid的题目
            if no_uid <= 5:
                print(f'[缺少uid] id={q["id"]}, set={q["set"]}, 题={q["question"][:20]}...')
    
    print()
    print(f'有uid: {has_uid} 题')
    print(f'无uid: {no_uid} 题')
    print()
    
    # 检查第4-5套题
    print('检查第4-5套题：')
    for set_num in [4, 5]:
        set_questions = [q for q in questions if q['set'] == set_num]
        set_has_uid = sum(1 for q in set_questions if 'uid' in q and q['uid'] is not None)
        print(f'  第{set_num}套: {set_has_uid}/{len(set_questions)} 题有uid')
    
    print('=' * 60)

if __name__ == '__main__':
    check_uid_field()
