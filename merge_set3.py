
import json

print("=" * 60)
print("  第三套题目合并工具")
print("=" * 60)

# 读取现有题库
with open('questions.json', 'r', encoding='utf-8') as f:
    all_questions = json.load(f)

print(f"当前题库共有 {len(all_questions)} 题")

# 检查是否已经有第三套
set3_existing = [q for q in all_questions if q.get('set') == 3]
if set3_existing:
    print(f"\n警告：题库中已有 {len(set3_existing)} 道第三套题目！")
    confirm = input("是否覆盖？(y/n): ").strip().lower()
    if confirm != 'y':
        print("操作取消。")
        exit()
    else:
        all_questions = [q for q in all_questions if q.get('set') != 3]
        print("已移除旧的第三套题目")

print("\n" + "=" * 60)
print("  请准备好第三套题目的JSON文件，或者我们创建一个模板")
print("=" * 60)

# 创建一个示例模板
print("\n正在创建第三套题目的模板文件...")
template_data = []
for i in range(1, 101):
    if i <= 20:
        q_type = 'single_choice'
    elif i <= 60:
        q_type = 'multiple_choice'
    elif i <= 80:
        q_type = 'true_false'
    else:
        q_type = 'fill_blank'
    
    question = {
        "id": i,
        "set": 3,
        "type": q_type,
        "question": f"第{i}题题目内容",
        "options": ["选项A", "选项B", "选项C", "选项D"] if q_type != 'true_false' and q_type != 'fill_blank' else [],
        "answer": "A",
        "explanation": "",
        "uid": 200 + i
    }
    template_data.append(question)

with open('第三套_模板.json', 'w', encoding='utf-8') as f:
    json.dump(template_data, f, ensure_ascii=False, indent=2)

print("\n✅ 已创建 '第三套_模板.json' 文件！")
print("\n你有两个选择：")
print("1. 直接在网页界面输入（推荐）: http://127.0.0.1:5000/input")
print("2. 编辑 '第三套_模板.json' 文件，填入题目内容后运行合并")
print("\n如果你已经有第三套题目的JSON文件，请将它重命名为 '第三套.json' 然后按提示合并")

choice = input("\n\n你是否已经有准备好的 '第三套.json' 文件？(y/n): ").strip().lower()

if choice == 'y':
    try:
        with open('第三套.json', 'r', encoding='utf-8') as f:
            set3_data = json.load(f)
        
        print(f"\n读取到 {len(set3_data)} 道第三套题目")
        
        # 合并
        for q in set3_data:
            q['set'] = 3
            if 'uid' not in q:
                q['uid'] = 200 + q['id']
        
        all_questions.extend(set3_data)
        
        # 按set和id排序
        all_questions.sort(key=lambda x: (x.get('set', 1), x.get('id', 0)))
        
        # 重新分配uid
        uid = 1
        for q in all_questions:
            q['uid'] = uid
            uid += 1
        
        # 备份旧文件
        import os
        import shutil
        if os.path.exists('questions_backup.json'):
            os.remove('questions_backup.json')
        shutil.copy('questions.json', 'questions_backup.json')
        print("\n已备份旧题库到 questions_backup.json")
        
        # 保存新文件
        with open('questions.json', 'w', encoding='utf-8') as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 合并成功！现在题库共有 {len(all_questions)} 题")
        set1 = len([q for q in all_questions if q.get('set') == 1])
        set2 = len([q for q in all_questions if q.get('set') == 2])
        set3 = len([q for q in all_questions if q.get('set') == 3])
        print(f"第一套: {set1}, 第二套: {set2}, 第三套: {set3}")
        
    except FileNotFoundError:
        print("\n未找到 '第三套.json' 文件！")
        print("请先通过网页界面输入题目并导出，或者手动创建JSON文件。")
else:
    print("\n好的，请使用网页界面输入题目！")
    print("访问 http://127.0.0.1:5000/input")
