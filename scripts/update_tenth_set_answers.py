import json
import os

def main():
    # 读取questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 根据用户提供的正确答案
    correct_answers = {
        81: "党的组织",
        82: "消极腐败",
        83: "组织生活",
        84: "入党动机",
        85: "自愿",
        86: "共产党宣言",
        87: "以党的自我革命引领社会革命",
        88: "批评和自我批评",
        89: "为民服务上",
        90: "当代中国",
        91: "贯彻党的基本路线",
        92: "组织生活",
        93: "专责",
        94: "共产主义",
        95: "一带一路",
        96: "监察",
        97: "自我批评",
        98: "选人用人",
        99: "奢靡之风",
        100: "首要"
    }
    
    # 更新答案
    updated_count = 0
    for q in all_questions:
        if q.get('set') == 10 and q.get('id') in correct_answers:
            old_answer = q.get('answer')
            q['answer'] = correct_answers[q['id']]
            updated_count += 1
            print(f"更新第{q['id']}题答案: {old_answer} -> {q['answer']}")
    
    # 保存更新后的文件
    with open(questions_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n成功更新了 {updated_count} 道题的答案")

if __name__ == "__main__":
    main()