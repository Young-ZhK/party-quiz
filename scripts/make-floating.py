import json

# 读取题目
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把题目转成JSON字符串
questions_json = json.dumps(questions, ensure_ascii=False)

# 完整的悬浮窗代码
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>党旗飘飘 - 悬浮窗搜题</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 30px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .card {{
            background: white;
            border-radius: 15px;
            padding: 35px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }}
        .card h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.4em;
        }}
        .btn {{
            display: block;
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
            text-decoration: none;
            text-align: center;
            margin-bottom: 15px;
        }}
        .btn:hover {{
            transform: translateY(-2px);
        }}
        .btn-secondary {{
            background: #e7e7e7;
            color: #333;
        }}
        .note {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .note strong {{ color: #856404; }}
        code {{
            background: #eee;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        
        /* 悬浮窗样式 */
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
            font-family: 'Microsoft YaHei','Segoe UI', sans-serif;
            display: none;
        }}
        #party-search-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            cursor: move;
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 党旗飘飘 - 悬浮窗搜题</h1>
            <p>包含300道题，点开就能用！</p>
        </div>
        
        <div class="card">
            <h2>📋 使用方法</h2>
            <button class="btn" onclick="openSearchBox()">🚀 打开悬浮窗搜题</button>
            <p style="color: #666; margin-top: 15px; line-height: 1.8;">
                💡 说明：点击上面按钮，会在右上角弹出搜题框！
            </p>
            <p style="color: #666; line-height: 1.8;">
                悬浮窗可以拖动位置，点击×关闭。
            </p>
        </div>
        
        <div class="card">
            <h2>👀 或者直接搜索</h2>
            <input type="text" id="direct-search" class="search-input" placeholder="输入关键词直接搜索..." style="width: 100%; padding: 15px; border: 2px solid #eee; border-radius: 8px; font-size: 16px;">
            <button class="btn btn-secondary" onclick="directSearch()" style="margin-top: 12px;">🔍 搜索</button>
            <div id="direct-results"></div>
        </div>
        
        <div class="note">
            <strong>提示：</strong> 也可以把这个文件发给别人，直接双击就能用！
        </div>
    </div>
    
    <!-- 悬浮窗 -->
    <div id="party-search-box">
        <div id="party-search-header">
            <span style="font-weight:bold;font-size:15px;">📚 党旗飘飘 - 快速搜题</span>
            <button id="party-search-close" onclick="closeSearchBox()">×</button>
        </div>
        <input type="text" id="party-search-input" placeholder="输入题目中的关键词搜索...">
        <button id="party-search-btn" onclick="doSearch()">🔍 搜索</button>
        <div id="party-search-results"></div>
    </div>
    
    <script>
        const allQuestions = {questions_json};
        
        // 直接搜索功能
        function directSearch() {{
            const keyword = document.getElementById('direct-search').value.trim().toLowerCase();
            const container = document.getElementById('direct-results');
            
            if (!keyword) {{
                container.innerHTML = '';
                return;
            }}
            
            let results = allQuestions.filter(q => {{
                const qText = q.question.toLowerCase();
                const aText = String(q.answer).toLowerCase();
                return qText.includes(keyword) || aText.includes(keyword);
            }});
            
            if (results.length === 0) {{
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 30px; font-size: 16px;">未找到相关题目</p>';
                return;
            }}
            
            let html = '<h3 style="margin:20px 0 10px;color:#333;">搜索结果 (共 ' + results.length + ' 道)</h3>';
            results.slice(0, 20).forEach(q => {{
                let setName = q.set === 1 ? '第一套' : q.set === 2 ? '第二套' : '第三套';
                let typeName = '';
                if (q.type === 'single_choice') typeName = '单选';
                else if (q.type === 'multiple_choice') typeName = '多选';
                else if (q.type === 'true_false') typeName = '判断';
                else if (q.type === 'fill_blank') typeName = '填空';
                
                let answerDisplay = q.type === 'true_false' ? (q.answer ? '正确' : '错误') : q.answer;
                
                html += `
                    <div style='background:#f8f9ff;padding:15px;border-radius:8px;margin-bottom:12px;border-left:4px solid #667eea;'>
                        <div style='margin-bottom:8px;'>
                            <span style='background:#667eea;color:white;padding:2px 8px;border-radius:4px;font-size:12px;margin-right:6px;'>${setName}</span>
                            <span style='background:#f5576c;color:white;padding:2px 8px;border-radius:4px;font-size:12px;'>${typeName}</span>
                        </div>
                        <p style='color:#333;margin-bottom:10px;line-height:1.7;'>${q.question}</p>
                        <p style='color:#2e7d32;font-weight:bold;font-size:16px;'>✅ 答案：${answerDisplay}</p>
                    </div>
                `;
            }});
            container.innerHTML = html;
        }}
        
        // 悬浮窗功能
        function openSearchBox() {{
            document.getElementById('party-search-box').style.display = 'block';
            document.getElementById('party-search-input').focus();
            document.getElementById('party-search-results').innerHTML = '<p style=\"text-align:center;color:#999;padding:30px;font-size:15px;\">💡 输入题目中的关键词开始搜索</p>';
        }}
        
        function closeSearchBox() {{
            document.getElementById('party-search-box').style.display = 'none';
        }}
        
        function doSearch() {{
            const keyword = document.getElementById('party-search-input').value.trim().toLowerCase();
            const container = document.getElementById('party-search-results');
            
            if (!keyword) {{
                container.innerHTML = '<p style=\"text-align:center;color:#999;padding:30px;font-size:15px;\">💡 输入题目中的关键词开始搜索</p>';
                return;
            }}
            
            let results = allQuestions.filter(q => {{
                const qText = q.question.toLowerCase();
                const aText = String(q.answer).toLowerCase();
                return qText.includes(keyword) || aText.includes(keyword);
            }});
            
            if (results.length === 0) {{
                container.innerHTML = '<p style=\"text-align:center;color:#999;padding:30px;font-size:15px;\">😔 未找到相关题目，试试其他关键词</p>';
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
                    <div class='party-result-item'>
                        <div style='margin-bottom:8px;'>
                            <span class='party-badge party-badge-set'>${setName}</span>
                            <span class='party-badge party-badge-type'>${typeName}</span>
                        </div>
                        <div class='party-result-q'>${q.question}</div>
                        <div class='party-result-a'>✅ 答案：${answerDisplay}</div>
                    </div>
                `;
            }});
            container.innerHTML = html;
        }}
        
        // 回车搜索
        document.getElementById('party-search-input').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') doSearch();
        }});
        
        document.getElementById('direct-search').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') directSearch();
        }});
    </script>
</body>
</html>"""

# 保存
with open('floating-search.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("OK 完成！")
print("已生成：floating-search.html")
print("直接双击打开就能用！")
