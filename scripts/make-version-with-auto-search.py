import json

with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_json = json.dumps(questions, ensure_ascii=False)

console_code = f"""
(function() {{
    const css = `
        #party-search-box {{
            position: fixed !important;
            top: 20px;
            right: 20px;
            width: 400px;
            max-height: 80vh;
            background: white !important;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
            z-index: 2147483647 !important;
            overflow: hidden;
            font-family: 'Microsoft YaHei', Arial, sans-serif !important;
        }}
        #party-search-header {{
            background: #4a90d9 !important;
            color: white !important;
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            cursor: move;
        }}
        #party-search-title {{
            font-weight: bold;
            font-size: 14px;
        }}
        #party-search-btns {{
            display: flex;
            gap: 8px;
        }}
        #party-search-min, #party-search-close {{
            background: rgba(255,255,255,0.25) !important;
            border: none !important;
            color: white !important;
            width: 24px;
            height: 24px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            line-height: 1;
        }}
        #party-search-input {{
            width: 100%;
            padding: 12px 15px;
            border: none !important;
            border-bottom: 1px solid #ddd !important;
            font-size: 14px;
            outline: none;
            box-sizing: border-box;
        }}
        #party-search-btn {{
            width: 100%;
            padding: 12px;
            background: #4a90d9 !important;
            color: white !important;
            border: none !important;
            font-size: 14px;
            cursor: pointer;
            font-weight: bold;
        }}
        #party-search-results {{
            max-height: 55vh;
            overflow-y: auto;
            padding: 10px 15px;
        }}
        .party-result-item {{
            padding: 12px;
            margin: 8px 0;
            background: #f5f5f5 !important;
            border-radius: 4px;
            font-size: 13px;
            line-height: 1.6;
            border-left: 3px solid #4a90d9 !important;
        }}
        .party-result-q {{
            color: #333 !important;
            margin-bottom: 8px;
        }}
        .party-result-a {{
            color: #28a745 !important;
            font-weight: bold;
            font-size: 14px;
        }}
        .party-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            margin-right: 5px;
            font-weight: bold;
        }}
        .party-badge-set {{
            background: #4a90d9 !important;
            color: white !important;
        }}
        .party-badge-type {{
            background: #e74c3c !important;
            color: white !important;
        }}
        #party-search-min-btn {{
            position: fixed !important;
            top: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            background: #4a90d9 !important;
            color: white !important;
            border: none !important;
            border-radius: 50%;
            cursor: pointer;
            font-size: 24px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
            z-index: 2147483647 !important;
            display: none;
        }}
    `;
    
    const existing = document.getElementById('party-search-box');
    const existingMin = document.getElementById('party-search-min-btn');
    const existingStyle = document.getElementById('party-search-style');
    if (existing) existing.remove();
    if (existingMin) existingMin.remove();
    if (existingStyle) existingStyle.remove();
    
    const style = document.createElement('style');
    style.id = 'party-search-style';
    style.textContent = css;
    document.head.appendChild(style);
    
    const minBtn = document.createElement('button');
    minBtn.id = 'party-search-min-btn';
    minBtn.textContent = '📚';
    minBtn.onclick = function() {{
        box.style.display = 'block';
        this.style.display = 'none';
    }};
    document.body.appendChild(minBtn);
    
    const box = document.createElement('div');
    box.id = 'party-search-box';
    box.innerHTML = `
        <div id='party-search-header'>
            <span id='party-search-title'>快速搜题</span>
            <div id='party-search-btns'>
                <button id='party-search-min' title='最小化'>−</button>
                <button id='party-search-close' title='关闭'>×</button>
            </div>
        </div>
        <input type='text' id='party-search-input' placeholder='输入关键词搜索...'>
        <button id='party-search-btn'>搜索</button>
        <div id='party-search-results'></div>
    `;
    document.body.appendChild(box);
    
    function ensureOnTop() {{
        box.style.zIndex = '2147483647';
        minBtn.style.zIndex = '2147483647';
    }}
    setInterval(ensureOnTop, 500);
    
    document.getElementById('party-search-close').onclick = function() {{
        box.remove();
        minBtn.remove();
        style.remove();
    }};
    
    document.getElementById('party-search-min').onclick = function() {{
        const rect = box.getBoundingClientRect();
        minBtn.style.top = rect.top + 'px';
        minBtn.style.right = (window.innerWidth - rect.right) + 'px';
        box.style.display = 'none';
        minBtn.style.display = 'block';
    }};
    
    const header = document.getElementById('party-search-header');
    let isDragging = false;
    let startX, startY, startLeft, startTop;
    
    header.addEventListener('mousedown', function(e) {{
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        const rect = box.getBoundingClientRect();
        startLeft = rect.left;
        startTop = rect.top;
        box.style.right = 'auto';
        box.style.left = startLeft + 'px';
        box.style.top = startTop + 'px';
    }});
    
    document.addEventListener('mousemove', function(e) {{
        if (!isDragging) return;
        const dx = e.clientX - startX;
        const dy = e.clientY - startY;
        box.style.left = (startLeft + dx) + 'px';
        box.style.top = (startTop + dy) + 'px';
    }});
    
    document.addEventListener('mouseup', function() {{
        isDragging = false;
    }});
    
    const allQuestions = {questions_json};
    
    function doSearch() {{
        const keyword = document.getElementById('party-search-input').value.trim().toLowerCase();
        const container = document.getElementById('party-search-results');
        
        if (!keyword) {{
            container.innerHTML = '<p style="text-align:center;color:#999;padding:25px;font-size:14px;">输入关键词搜索</p>';
            return;
        }}
        
        let results = allQuestions.filter(q => {{
            const qText = q.question.toLowerCase();
            const aText = String(q.answer).toLowerCase();
            return qText.includes(keyword) || aText.includes(keyword);
        }});
        
        if (results.length === 0) {{
            container.innerHTML = '<p style="text-align:center;color:#999;padding:25px;font-size:14px;">未找到相关题目</p>';
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
            html += '<div class="party-result-item"><div style="margin-bottom:6px;"><span class="party-badge party-badge-set">' + setName + '</span><span class="party-badge party-badge-type">' + typeName + '</span></div><div class="party-result-q">' + q.question + '</div><div class="party-result-a">答案：' + answerDisplay + '</div></div>';
        }});
        container.innerHTML = html;
    }}
    
    document.getElementById('party-search-btn').onclick = doSearch;
    document.getElementById('party-search-input').addEventListener('keypress', function(e) {{
        if (e.key === 'Enter') doSearch();
    }});
    
    // 自动获取选中的文本搜索
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {{
        document.getElementById('party-search-input').value = selectedText;
        doSearch();
    }} else {{
        document.getElementById('party-search-results').innerHTML = '<p style="text-align:center;color:#999;padding:25px;font-size:14px;">输入关键词搜索，或者选中题目文字再点书签！</p>';
        document.getElementById('party-search-input').focus();
    }}
    
    console.log('✅ 悬浮窗已打开！选中题目再点书签会自动搜索！');
}})();
"""

with open('console-code.txt', 'w', encoding='utf-8') as f:
    f.write(console_code)

print("OK 完成！")
print("已更新：console-code.txt")
print()
print("新功能：")
print("- 选中页面上的题目文字")
print("- 点击书签，自动搜索并显示答案！")
