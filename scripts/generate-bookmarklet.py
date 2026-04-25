import json

# 读取题目数据
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把题目数据转成JSON字符串，并且处理转义
questions_json = json.dumps(questions, ensure_ascii=False)
# 转义特殊字符，让它能在JavaScript字符串里
questions_json = questions_json.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

# 完整的书签代码
bookmarklet_code = f"""javascript:(function(){{
    const css = `
        #party-search-box {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 420px;
            max-height: 85vh;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 50px rgba(0,0,0,0.35);
            z-index: 2147483647;
            overflow: hidden;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        }}
        #party-search-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }}
        #party-search-close {{
            background: rgba(255,255,255,0.25);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            line-height: 1;
        }}
        #party-search-input {{
            width: 100%;
            padding: 16px 20px;
            border: none;
            border-bottom: 2px solid #eee;
            font-size: 16px;
            outline: none;
            box-sizing: border-box;
        }}
        #party-search-btn {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
        }}
        #party-search-results {{
            max-height: 60vh;
            overflow-y: auto;
            padding: 10px 15px;
        }}
        .party-result-item {{
            padding: 14px;
            margin: 10px 0;
            background: #f8f9ff;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            font-size: 14px;
            line-height: 1.6;
        }}
        .party-result-q {{
            color: #333;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        .party-result-a {{
            color: #2e7d32;
            font-weight: bold;
            font-size: 15px;
        }}
        .party-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 5px;
            font-size: 12px;
            margin-right: 6px;
            font-weight: bold;
        }}
        .party-badge-set {{
            background: #667eea;
            color: white;
        }}
        .party-badge-type {{
            background: #f5576c;
            color: white;
        }}
    `;
    
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    
    const box = document.createElement('div');
    box.id = 'party-search-box';
    box.innerHTML = `
        <div id="party-search-header">
            <span style="font-weight:bold;font-size:15px;">📚 党旗飘飘 - 快速搜题</span>
            <button id="party-search-close">×</button>
        </div>
        <input type="text" id="party-search-input" placeholder="输入题目中的关键词搜索...">
        <button id="party-search-btn">🔍 搜索</button>
        <div id="party-search-results"></div>
    `;
    document.body.appendChild(box);
    
    // 关闭功能
    document.getElementById('party-search-close').onclick = function(){{
        box.remove();
        style.remove();
    }};
    
    // 题目数据
    const allQuestions = {questions_json};
    
    // 搜索函数
    function doSearch() {{
        const keyword = document.getElementById('party-search-input').value.trim().toLowerCase();
        const container = document.getElementById('party-search-results');
        
        if (!keyword) {{
            container.innerHTML = '<p style="text-align:center;color:#999;padding:30px;font-size:15px;">💡 输入题目中的关键词开始搜索</p>';
            return;
        }}
        
        let results = allQuestions.filter(q => {{
            const qText = q.question.toLowerCase();
            const aText = String(q.answer).toLowerCase();
            return qText.includes(keyword) || aText.includes(keyword);
        }});
        
        if (results.length === 0) {{
            container.innerHTML = '<p style="text-align:center;color:#999;padding:30px;font-size:15px;">😔 未找到相关题目，试试其他关键词</p>';
            return;
        }}
        
        let html = '';
        results.slice(0, 15).forEach(q => {{
            let setName = q.set === 1 ? '第一套' : q.set === 2 ? '第二套' : '第三套';
            let typeName = '';
            if (q.type === 'single_choice') typeName = '单选';
            else if (q.type === 'multiple_choice') typeName = '多选';
            else if (q.type === 'true_false') typeName = '判断';
            else if (q.type === 'fill_blank') typeName = '填空';
            
            let answerDisplay = q.type === 'true_false' ? (q.answer ? '正确' : '错误') : q.answer;
            
            html += `
                <div class="party-result-item">
                    <div style="margin-bottom:8px;">
                        <span class="party-badge party-badge-set">${{setName}}</span>
                        <span class="party-badge party-badge-type">${{typeName}}</span>
                    </div>
                    <div class="party-result-q">${{q.question}}</div>
                    <div class="party-result-a">✅ 答案：${{answerDisplay}}</div>
                </div>
            `;
        }});
        
        container.innerHTML = html;
    }}
    
    // 绑定事件
    document.getElementById('party-search-btn').onclick = doSearch;
    document.getElementById('party-search-input').addEventListener('keypress', function(e){{
        if (e.key === 'Enter') doSearch();
    }});
    
    // 初始提示
    document.getElementById('party-search-results').innerHTML = '<p style="text-align:center;color:#999;padding:30px;font-size:15px;">💡 输入题目中的关键词开始搜索</p>';
}})();"""

# 保存书签代码
with open('party-search-bookmarklet.txt', 'w', encoding='utf-8') as f:
    f.write(bookmarklet_code)

# 生成一个简单的HTML安装页
html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>搜题书签 - 安装说明</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 30px;
            margin: 0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 { color: #333; margin-bottom: 20px; text-align: center; }
        .step { margin: 25px 0; padding: 20px; background: #f8f9ff; border-radius: 10px; border-left: 4px solid #667eea; }
        .step h3 { color: #667eea; margin-top: 0; }
        .note { background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px; padding: 15px; margin: 20px 0; }
        .note strong { color: #856404; }
        code { background: #eee; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; }
        textarea { width: 100%; height: 250px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; font-family: Consolas, monospace; font-size: 11px; line-height: 1.4; box-sizing: border-box; }
        button { margin-top: 15px; padding: 12px 35px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 不切屏搜题工具（考试专用）</h1>
        
        <div class="note">
            <strong>⚠️ 说明：</strong> 这是一个浏览器书签工具，可以在任何网页上弹出搜题框，不需要切屏！
        </div>
        
        <div class="step">
            <h3>📋 使用步骤</h3>
            <p>1. 复制下面的完整代码</p>
            <p>2. 在浏览器书签栏右键 → "添加书签"</p>
            <p>3. 名称填：<code>📚 党旗飘飘搜题</code></p>
            <p>4. 网址（URL）栏粘贴刚才复制的代码 → 保存</p>
            <p>5. 考试时，点击书签栏的这个书签，搜题框就会弹出来！</p>
        </div>
        
        <div class="step">
            <h3>👇 复制下面的完整代码</h3>
            <textarea id="codeArea" readonly>""" + bookmarklet_code.replace('\\', '\\\\').replace('`', '\\`') + """</textarea>
            <button onclick="copyCode()">📋 一键复制全部代码</button>
        </div>
        
        <div class="note">
            <strong>💡 提示：</strong> 建议考试前先在普通网页试一下，确保能用！
        </div>
    </div>
    
    <script>
        function copyCode() {
            const textarea = document.getElementById('codeArea');
            textarea.select();
            document.execCommand('copy');
            alert('✅ 代码已复制！现在去浏览器书签栏右键添加书签吧！');
        }
    </script>
</body>
</html>"""

with open('bookmarklet-install.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("OK 书签工具已生成！")
print("   - 完整代码：party-search-bookmarklet.txt")
print("   - 安装页面：bookmarklet-install.html")
print("\n使用方法：")
print("   1. 打开 bookmarklet-install.html")
print("   2. 复制代码，添加到浏览器书签")
print("   3. 考试时点击书签就能用！")
