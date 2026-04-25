import json

# 读取题目
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把题目转成JSON字符串
questions_json = json.dumps(questions, ensure_ascii=False)

# 完整的控制台代码
console_code = f"""
// 复制这段代码，在浏览器控制台（按F12）里粘贴，然后按回车！

(function() {{
    const css = `#party-search-box{{position:fixed;top:20px;right:20px;width:420px;max-height:85vh;background:white;border-radius:15px;box-shadow:0 10px 50px rgba(0,0,0,0.35);z-index:2147483647;overflow:hidden;font-family:'Microsoft YaHei','Segoe UI',sans-serif}}#party-search-header{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px 20px;display:flex;justify-content:space-between;align-items:center;user-select:none}}#party-search-close{{background:rgba(255,255,255,0.25);border:none;color:white;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:20px;line-height:1}}#party-search-input{{width:100%;padding:16px 20px;border:none;border-bottom:2px solid #eee;font-size:16px;outline:none;box-sizing:border-box}}#party-search-btn{{width:100%;padding:14px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;font-size:16px;cursor:pointer;font-weight:bold}}#party-search-results{{max-height:60vh;overflow-y:auto;padding:10px 15px}}.party-result-item{{padding:14px;margin:10px 0;background:#f8f9ff;border-radius:10px;border-left:4px solid #667eea;font-size:14px;line-height:1.6}}.party-result-q{{color:#333;margin-bottom:10px;font-weight:500}}.party-result-a{{color:#2e7d32;font-weight:bold;font-size:15px}}.party-badge{{display:inline-block;padding:3px 10px;border-radius:5px;font-size:12px;margin-right:6px;font-weight:bold}}.party-badge-set{{background:#667eea;color:white}}.party-badge-type{{background:#f5576c;color:white}}`;
    
    const style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);
    
    const box = document.createElement('div');
    box.id = 'party-search-box';
    box.innerHTML = `<div id='party-search-header'><span style='font-weight:bold;font-size:15px;'>📚 党旗飘飘 - 快速搜题</span><button id='party-search-close'>×</button></div><input type='text' id='party-search-input' placeholder='输入题目中的关键词搜索...'><button id='party-search-btn'>🔍 搜索</button><div id='party-search-results'></div>`;
    document.body.appendChild(box);
    
    document.getElementById('party-search-close').onclick = function() {{
        box.remove();
        style.remove();
    }};
    
    const allQuestions = {questions_json};
    
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
            container.innerHTML = '<p style="text-align:center;color:#999;padding:30px;font-size:15px;">😔 未找到相关题目</p>';
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
            html += '<div class="party-result-item"><div style="margin-bottom:8px;"><span class="party-badge party-badge-set">' + setName + '</span><span class="party-badge party-badge-type">' + typeName + '</span></div><div class="party-result-q">' + q.question + '</div><div class="party-result-a">✅ 答案：' + answerDisplay + '</div></div>';
        }});
        container.innerHTML = html;
    }}
    
    document.getElementById('party-search-btn').onclick = doSearch;
    document.getElementById('party-search-input').addEventListener('keypress', function(e) {{ if (e.key === 'Enter') doSearch(); }});
    document.getElementById('party-search-results').innerHTML = '<p style="text-align:center;color:#999;padding:30px;font-size:15px;">💡 输入题目中的关键词开始搜索</p>';
    
    console.log('✅ 搜题悬浮窗已打开！');
}})();
"""

# 保存到文件
with open('console-code.txt', 'w', encoding='utf-8') as f:
    f.write(console_code)

print("OK 完成！")
print("已生成：console-code.txt")
print()
print("用法：")
print("1. 打开考试网站")
print("2. 按 F12 打开开发者工具")
print("3. 点击 Console（控制台）标签")
print("4. 复制 console-code.txt 里的全部内容")
print("5. 粘贴进去，按回车")
print("6. 右上角就出现搜题悬浮窗了！")
