#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

def main():
    # 读取index.html
    html_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到脚本开始位置
    script_start = content.find('<script>\n    // ========== 嵌入式题目数据（共1000道题）==========')
    if script_start == -1:
        print('未找到脚本开始位置')
        return
    
    # 找到脚本结束位置
    script_end = content.find('</script>', script_start)
    if script_end == -1:
        print('未找到脚本结束位置')
        return
    script_end += len('</script>')
    
    # 替换脚本部分
    new_content = content[:script_start] + '<script type="module" src="js/main.js"></script>' + content[script_end:]
    
    # 保存修改后的文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('成功更新index.html，使用模块化JavaScript文件')

if __name__ == '__main__':
    main()
