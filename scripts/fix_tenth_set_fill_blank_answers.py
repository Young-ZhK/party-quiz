import json
import os

def main():
    # 读取questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 为第十套题的填空题设置具体答案
    # 基于题目内容推断的合理答案
    fill_blank_answers = {
        81: "党的组织",
        82: "消极腐败",
        83: "组织生活",
        84: "入党动机",
        85: "入党自愿",
        86: "共产党宣言",
        87: "全面从严治党",
        88: "理论联系实际",
        89: "改革创新",
        90: "当代中国",
        91: "错误倾向",
        92: "组织生活",
        93: "重要",
        94: "马克思列宁",
        95: "两学一做",
        96: "社会稳定",
        97: "自我批评",
        98: "政治",
        99: "价值观",
        100: "首要"
    }
    
    # 更新填空题的答案
    updated_count = 0
    for q in all_questions:
        if q.get('set') == 10 and q.get('type') == 'fill_blank' and q.get('id') in fill_blank_answers:
            old_answer = q.get('answer')
            q['answer'] = fill_blank_answers[q['id']]
            updated_count += 1
            print(f"更新第{q['id']}题答案: {old_answer} -> {q['answer']}")
    
    # 保存更新后的文件
    with open(questions_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    
    print(f"\n成功更新了 {updated_count} 道填空题的答案")

if __name__ == "__main__":
    main()