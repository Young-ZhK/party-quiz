import json

# 读取题目
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

questions_json = json.dumps(questions, ensure_ascii=False, separators=(',', ':'))

# 书签代码（压缩版）
bookmarklet_code = f"""javascript:(function(){{const css='#party-search-box{{position:fixed!important;top:20px;right:20px;width:400px;max-height:80vh;background:white!important;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,0.3)!important;z-index:2147483647!important;overflow:hidden;font-family:'Microsoft YaHei',Arial,sans-serif!important}}#party-search-header{{background:#4a90d9!important;color:white!important;padding:10px 15px;display:flex;justify-content:space-between;align-items:center;user-select:none;cursor:move}}#party-search-title{{font-weight:bold;font-size:14px}}#party-search-btns{{display:flex;gap:8px}}#party-search-min,#party-search-close{{background:rgba(255,255,255,0.25)!important;border:none!important;color:white!important;width:24px;height:24px;border-radius:4px;cursor:pointer;font-size:14px;line-height:1}}#party-search-input{{width:100%;padding:12px 15px;border:none!important;border-bottom:1px solid #ddd!important;font-size:14px;outline:none;box-sizing:border-box}}#party-search-btn{{width:100%;padding:12px;background:#4a90d9!important;color:white!important;border:none!important;font-size:14px;cursor:pointer;font-weight:bold}}#party-search-results{{max-height:55vh;overflow-y:auto;padding:10px 15px}}.party-result-item{{padding:12px;margin:8px 0;background:#f5f5f5!important;border-radius:4px;font-size:13px;line-height:1.6;border-left:3px solid #4a90d9!important}}.party-result-q{{color:#333!important;margin-bottom:8px}}.party-result-a{{color:#28a745!important;font-weight:bold;font-size:14px}}.party-badge{{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;margin-right:5px;font-weight:bold}}.party-badge-set{{background:#4a90d9!important;color:white!important}}.party-badge-type{{background:#e74c3c!important;color:white!important}}#party-search-min-btn{{position:fixed!important;top:20px;right:20px;width:50px;height:50px;background:#4a90d9!important;color:white!important;border:none!important;border-radius:50%;cursor:pointer;font-size:24px;box-shadow:0 4px 15px rgba(0,0,0,0.3)!important;z-index:2147483647!important;display:none}}';const e=document.getElementById('party-search-box'),t=document.getElementById('party-search-min-btn'),n=document.getElementById('party-search-style');e&&e.remove(),t&&t.remove(),n&&n.remove();const o=document.createElement('style');o.id='party-search-style',o.textContent=css,document.head.appendChild(o);const i=document.createElement('button');i.id='party-search-min-btn',i.textContent='📚',i.onclick=function(){{a.style.display='block',this.style.display='none'}},document.body.appendChild(i);const a=document.createElement('div');a.id='party-search-box',a.innerHTML='<div id=\\'party-search-header\\'><span id=\\'party-search-title\\'>快速搜题</span><div id=\\'party-search-btns\\'><button id=\\'party-search-min\\' title=\\'最小化\\'>−</button><button id=\\'party-search-close\\' title=\\'关闭\\'>×</button></div></div><input type=\\'text\\' id=\\'party-search-input\\' placeholder=\\'输入关键词搜索...\\'><button id=\\'party-search-btn\\'>搜索</button><div id=\\'party-search-results\\'></div>',document.body.appendChild(a);function s(){{a.style.zIndex='2147483647',i.style.zIndex='2147483647'}}setInterval(s,500),document.getElementById('party-search-close').onclick=function(){{a.remove(),i.remove(),o.remove()},document.getElementById('party-search-min').onclick=function(){{const e=a.getBoundingClientRect();i.style.top=e.top+'px',i.style.right=window.innerWidth-e.right+'px',a.style.display='none',i.style.display='block'}};const r=document.getElementById('party-search-header');let l=!1,d,c,u,p;r.addEventListener('mousedown',function(e){{l=!0,d=e.clientX,c=e.clientY;const t=a.getBoundingClientRect();u=t.left,p=t.top,a.style.right='auto',a.style.left=u+'px',a.style.top=p+'px'}}),document.addEventListener('mousemove',function(e){{if(!l)return;const t=e.clientX-d,n=e.clientY-c;a.style.left=u+t+'px',a.style.top=p+n+'px'}}),document.addEventListener('mouseup',function(){{l=!1}});const h={questions_json};function y(){{const e=document.getElementById('party-search-input').value.trim().toLowerCase(),t=document.getElementById('party-search-results');if(!e)return t.innerHTML='<p style=\\'text-align:center;color:#999;padding:25px;font-size:14px;\\'>输入关键词搜索</p>';let n=h.filter(function(t){{const n=t.question.toLowerCase(),o=String(t.answer).toLowerCase();return n.includes(e)||o.includes(e)}});if(0===n.length?t.innerHTML='<p style=\\'text-align:center;color:#999;padding:25px;font-size:14px;\\'>未找到相关题目</p>':(t.innerHTML='',n.slice(0,15).forEach(function(e){{let t=1===e.set?'第一套':2===e.set?'第二套':'第三套',n='';'single_choice'===e.type?n='单选':'multiple_choice'===e.type?n='多选':'true_false'===e.type?n='判断':'fill_blank'===e.type&&(n='填空');let o='true_false'===e.type?e.answer?'正确':'错误':e.answer;t.innerHTML+='<div class=\\'party-result-item\\'><div style=\\'margin-bottom:6px;\\'><span class=\\'party-badge party-badge-set\\'>'+t+'</span><span class=\\'party-badge party-badge-type\\'>'+n+'</span></div><div class=\\'party-result-q\\'>'+e.question+'</div><div class=\\'party-result-a\\'>答案：'+o+'</div></div>'}}))}}document.getElementById('party-search-btn').onclick=y,document.getElementById('party-search-input').addEventListener('keypress',function(e){{'Enter'===e.key&&y()}),document.getElementById('party-search-results').innerHTML='<p style=\\'text-align:center;color:#999;padding:25px;font-size:14px;\\'>输入关键词搜索</p>',document.getElementById('party-search-input').focus(),console.log('✅ 悬浮窗已打开！')}})();"""

# 保存书签代码
with open('bookmarklet-code.txt', 'w', encoding='utf-8') as f:
    f.write(bookmarklet_code)

# 做一个安装页面
install_page = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>党旗飘飘 - 搜题工具 - 一键安装</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 30px;
            margin: 0;
        }}
        .container {{
            max-width: 750px;
            margin: 0 auto;
        }}
        h1 {{
            color: white;
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .card {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 25px;
        }}
        .card h2 {{
            color: #333;
            margin-bottom: 25px;
            font-size: 1.6em;
        }}
        .step {{
            margin: 20px 0;
            padding-left: 28px;
            position: relative;
            line-height: 1.9;
            color: #444;
        }}
        .step::before {{
            content: '';
            width: 14px;
            height: 14px;
            background: #4a90d9;
            border-radius: 50%;
            position: absolute;
            left: 0;
            top: 7px;
        }}
        .bookmarklet-box {{
            background: #f8f9ff;
            border: 2px dashed #4a90d9;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            margin: 25px 0;
        }}
        .bookmarklet-btn {{
            display: inline-block;
            background: #4a90d9;
            color: white;
            padding: 18px 45px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 1.3em;
            font-weight: bold;
            cursor: grab;
        }}
        .bookmarklet-btn:hover {{
            background: #3a7bc8;
        }}
        .note {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }}
        .note strong {{ color: #856404; }}
        .success {{
            color: #28a745;
            font-weight: bold;
        }}
        .tip {{
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 党旗飘飘 - 搜题工具</h1>
        
        <div class="card">
            <h2>✨ 最方便的方法：添加到浏览器书签</h2>
            
            <div class="step">
                先按 <strong>Ctrl + Shift + B</strong>（Chrome/Edge），显示书签栏
            </div>
            
            <div class="step">
                用鼠标<strong>点住</strong>下面这个按钮
            </div>
            
            <div class="bookmarklet-box">
                <a href="{bookmarklet_code}" class="bookmarklet-btn" draggable="true">
                    📚 快速搜题
                </a>
            </div>
            
            <div class="step">
                <strong>拖到</strong>浏览器顶部的书签栏里，松开
            </div>
            
            <div class="step">
                完成！以后在任何网页，点一下书签，悬浮窗就出来了！
            </div>
            
            <div class="note">
                <strong>提示：</strong> 如果不能拖？看下面备用方法！
            </div>
        </div>
        
        <div class="card">
            <h2>📋 备用方法：手动添加书签</h2>
            
            <div class="step">
                在浏览器书签栏<strong>右键</strong> → 点击「添加书签」或「添加页」
            </div>
            <div class="step">
                名称填：<strong>快速搜题</strong>
            </div>
            <div class="step">
                网址（URL）：打开 <strong>bookmarklet-code.txt</strong>，复制全部内容，粘贴进去
            </div>
            <div class="step">
                保存！
            </div>
        </div>
        
        <div class="card">
            <h2>💡 功能说明</h2>
            <ul style="line-height: 2; color: #555;">
                <li>✅ 可拖动（按住标题栏）</li>
                <li>✅ 可最小化（点击「−」）</li>
                <li>✅ 永远在最上层</li>
                <li>✅ 包含完整300道题</li>
                <li>✅ 任何网页都能用</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

with open('bookmarklet-install.html', 'w', encoding='utf-8') as f:
    f.write(install_page)

print("OK 完成！")
print()
print("已生成文件：")
print("- bookmarklet-install.html  (推荐直接打开，拖按钮到书签栏")
print("- bookmarklet-code.txt (备用，手动添加用")
print()
print("用法：")
print("1. 双击打开 bookmarklet-install.html")
print("2. 按 Ctrl+Shift+B 显示书签栏")
print("3. 把蓝色按钮拖到书签栏")
print("4. 以后在任何网页点一下书签就出来了！")
