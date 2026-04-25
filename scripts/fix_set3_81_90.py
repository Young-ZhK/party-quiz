import json

with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

# 修复数据
fix_data = {
    81: {
        "question": "“三会一课”制度是指：定期召开支部党员大会、支部委员会、____，按时上好党课。",
        "answer": "党小组会"
    },
    82: {
        "question": "“四个意识”：是指政治意识、____、核心意识、看齐意识。这“四个意识”是2016年1月29日中共中央政治局会议最早提出来的。",
        "answer": "大局意识"
    },
    83: {
        "question": "要求入党的同志要能够经受住____的考验。",
        "answer": "党组织"
    },
    84: {
        "question": "按照党的思想建设的要求，党员不仅要在组织上入党，而且要在____上入党。",
        "answer": "思想"
    },
    85: {
        "question": "党的二十届四中全会指出，要严守____，全面推进以国家公园为主体的自然保护地体系建设，有序设立新的国家公园。",
        "answer": "生态保护红线"
    },
    86: {
        "question": "党的二十届四中全会指出，弘扬全人类共同价值，推动建设持久和平、普遍安全、共同繁荣、开放包容、清洁美丽的世界，为构建____作出中国贡献。",
        "answer": "人类命运共同体"
    },
    87: {
        "question": "党的二十届四中全会指出，全党全军全国各族人民要更加紧密地团结在以习近平同志为核心的党中央周围，为基本实现社会主义现代化而共同奋斗，不断开创以中国式现代化全面推进____伟业新局面。",
        "answer": "强国建设、民族复兴"
    },
    88: {
        "question": "各级党委（党组）原则上每____年组织开展1次党史学习教育工作情况综合评估，充分运用评估结果，不断改进党史学习教育工作。",
        "answer": "5|五"
    },
    89: {
        "question": "深入推进党风廉政建设和反腐败斗争，以____态度惩治腐败，构建不敢腐、不能腐、不想腐的有效机制。",
        "answer": "零容忍"
    },
    90: {
        "question": "党章总纲指出，要抓紧时机，加快发展，实施科教兴国战略、人才强国战略、创新驱动发展战略、____战略、区域协调发展战略、可持续发展战略、军民融合发展战略，充分发挥科学技术作为第一生产力的作用，依靠科技进步，提高劳动者素质，促进国民经济又好又快发展。",
        "answer": "乡村振兴"
    }
}

fixed_count = 0

for q in all_questions:
    if q.get('set') == 3 and q.get('id') in fix_data:
        q['type'] = 'fill_blank'
        q['question'] = fix_data[q['id']]['question']
        q['answer'] = fix_data[q['id']]['answer']
        if 'options' in q:
            del q['options']
        fixed_count += 1
        print(f"Fixed set 3, id {q['id']}")

# 保存
with open('questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"\nTotal fixed: {fixed_count}")
