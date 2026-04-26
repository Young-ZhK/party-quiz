# 题库系统目录结构

## 整理说明

此目录结构已进行整理，移除了临时文件和重复文件，保持了清晰的组织结构。

## 目录结构

```
111/
├── data/                 # 题目数据目录
│   └── questions.json    # 完整题目数据库（包含所有套题）
├── scripts/              # 脚本工具目录
│   ├── build-standalone.py        # 构建独立版本
│   ├── check_all_sets.py          # 检查所有套题
│   ├── check_backup.py            # 检查备份
│   ├── check_format.py            # 检查格式
│   ├── check_options.py           # 检查选项
│   ├── check_questions.py         # 检查题目
│   ├── check_set2.py              # 检查第二套
│   ├── check_set3.py              # 检查第三套
│   ├── do_merge.py                # 执行合并
│   ├── final-gen.py               # 最终生成
│   ├── fix-second-set.py          # 修复第二套
│   ├── fix_options.py             # 修复选项
│   ├── fix_question_types.py      # 修复题目类型
│   ├── fix_set3.py                # 修复第三套
│   ├── fix_set3_81_90.py          # 修复第三套81-90题
│   ├── generate-bookmarklet.py    # 生成书签工具
│   ├── generate-github-page.py    # 生成GitHub页面
│   ├── generate_static.py         # 生成静态版本
│   ├── make-bookmarklet-final.py  # 制作最终书签工具
│   ├── make-console-code.py       # 制作控制台代码
│   ├── make-final-version.py      # 制作最终版本
│   ├── make-floating-v2.py        # 制作浮动版本v2
│   ├── make-floating.py           # 制作浮动版本
│   ├── make-simple-floating.py    # 制作简单浮动版本
│   ├── make-version-with-auto-search.py  # 制作自动搜索版本
│   ├── merge_all_sets.py          # 合并所有套题
│   ├── merge_new_sets.py          # 合并新套题
│   ├── merge_set3.py              # 合并第三套
│   ├── merge_sets78.py            # 合并第七、八套
│   ├── ocr_parse.py               # OCR解析
│   ├── parse_new_sets.py          # 解析新套题
│   ├── parse_questions.py         # 解析题目
│   ├── parse_set3.py              # 解析第三套
│   ├── parse_set3_fixed.py        # 解析修复后的第三套
│   ├── parse_sets78.py            # 解析第七、八套
│   ├── parse_simple.py            # 简单解析
│   ├── parse_two_sets.py          # 解析两套题
│   ├── read_docx.py               # 读取docx文件
│   ├── read_new_docs.py           # 读取新文档
│   ├── simple-github-gen.py       # 简单GitHub生成
│   └── verify_questions.py        # 验证题目
├── tools/                # 工具目录
│   ├── bookmarklet-install.html      # 书签工具安装
│   ├── complete-search.html          # 完整搜索
│   ├── console-code.txt              # 控制台代码
│   ├── drag-drop-install.html        # 拖放安装
│   ├── floating-search.html          # 浮动搜索
│   ├── how-to-use.html               # 使用说明
│   ├── input_questions.html          # 输入题目
│   ├── party-search-bookmarklet.txt  # 派对搜索书签
│   ├── search-bookmarklet.html       # 搜索书签
│   ├── search-static.html            # 静态搜索
│   ├── search.html                   # 搜索
│   ├── simple-install.html           # 简单安装
│   └── standalone-search.html        # 独立搜索
├── backups/              # 备份目录
│   ├── questions.json.backup_20260423_161505  # 备份文件
│   ├── questions_backup.json                 # 备份文件
│   ├── 第三套.json                           # 第三套备份
│   └── 第四套-第六套.json                     # 第四-六套备份
├── .gitignore            # Git忽略文件
├── app.py                # 主应用程序
├── index.html            # 主页面
└── requirements.txt      # 依赖项
```

## 主要文件说明

### 核心文件
- **index.html**：主页面，包含题库系统的所有功能
- **data/questions.json**：完整的题目数据库，包含所有套题的题目
- **app.py**：主应用程序，可能用于本地服务器或其他功能

### 备份文件
- **backups/** 目录：存储各种备份文件，包括题目数据备份

### 脚本工具
- **scripts/** 目录：包含各种用于处理题目数据的脚本，如解析、合并、修复等

### 工具文件
- **tools/** 目录：包含各种辅助工具，如搜索页面、安装说明等

## 使用说明

1. **访问题库**：直接打开 `index.html` 文件即可使用题库系统
2. **修改题目**：编辑 `data/questions.json` 文件来修改题目数据
3. **使用脚本**：运行 `scripts/` 目录下的脚本来处理题目数据
4. **使用工具**：访问 `tools/` 目录下的工具页面来使用辅助功能

## 注意事项

- 请勿删除 `data/questions.json` 文件，这是题库系统的核心数据文件
- 重要修改前请先备份题目数据
- 如需添加新题目，请确保格式正确
