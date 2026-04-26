import json

def check_set1_54():
    print('=' * 60)
    print('查看第1套题第54题作为参考')
    print('=' * 60)
    print()
    
    # 读取题目数据
    with open('data/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # 查找第1套题第54题
    for q in questions:
        if q['set'] == 1 and q['id'] == 54:
            print(f'第 54 题（id=54）')
            print(f'题目：{q["question"]}')
            print('选项：')
            for i, opt in enumerate(q['options']):
                print(f'  {chr(65+i)}. {opt}')
            print(f'答案：{q["answer"]}')
            break
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    check_set1_54()
