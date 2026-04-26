#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

print("正在读取题目数据...")

# 读取questions.json文件
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print("正在修改第二套21-40题的类型...")

# 找到第二套的21-40题（id 121-140）并修改类型
modified_count = 0
for q in questions:
    if q['set'] == 2 and 121 <= q['id'] <= 140:
        if q['type'] == 'multiple_choice':
            q['type'] = 'single_choice'
            modified_count += 1
            print(f"已修改第{q['id']}题（第二套第{q['id']-100}题）的类型为单选题")

print(f"\n共修改了{modified_count}道题")

# 保存修改后的数据
with open('c:\\Users\\86183\\Desktop\\111\\111\\data\\questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print("修改完成！")
