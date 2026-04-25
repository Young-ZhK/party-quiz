import json

# 读取题目数据
with open('../data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把数据转成JS字符串
questions_js = json.dumps(questions, ensure_ascii=False)

# 读取旧的HTML模板
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>党旗飘飘 - 在线答题</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            -webkit-tap-highlight-color: transparent;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        /* 移动端优化 */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            .header p {
                font-size: 1em;
            }
            
            .menu {
                padding: 20px;
                border-radius: 12px;
            }
            
            .menu h2 {
                font-size: 1.3em;
            }
            
            .set-btn {
                padding: 10px 20px;
                font-size: 1em;
            }
            
            .menu-buttons {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
            
            .menu-btn {
                padding: 15px;
                font-size: 1em;
            }
            
            .quiz-container {
                padding: 20px;
            }
            
            .question {
                font-size: 1.1em;
                line-height: 1.8;
            }
            
            .option {
                padding: 15px;
                font-size: 1em;
            }
            
            .show-answer-btn {
                padding: 10px 20px;
                font-size: 0.95em;
            }
            
            .result-container {
                padding: 20px;
            }
            
            .score-display {
                font-size: 3em;
            }
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .menu {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .menu h2 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .set-selector {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .set-btn {
            padding: 12px 30px;
            border: 3px solid #667eea;
            border-radius: 10px;
            background: white;
            color: #667eea;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .set-btn.active {
            background: #667eea;
            color: white;
        }
        
        .set-btn:hover {
            transform: translateY(-2px);
        }
        
        .menu-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .menu-btn {
            padding: 20px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
            font-weight: bold;
        }
        
        .menu-btn:hover {
            transform: translateY(-2px);
        }
        
        .menu-btn.start {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .menu-btn.browse {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        
        /* 答题界面 */
        .quiz-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
        }
        
        .question-card {
            margin-bottom: 30px;
        }
        
        .question-number {
            color: #667eea;
            font-size: 1.2em;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .question {
            color: #333;
            font-size: 1.3em;
            line-height: 1.8;
            margin-bottom: 25px;
        }
        
        .options {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .option {
            padding: 18px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
        }
        
        .option:hover {
            border-color: #667eea;
        }
        
        .option.selected {
            border-color: #667eea;
            background: #f0f0ff;
        }
        
        .option.correct {
            border-color: #38ef7d;
            background: #d4edda;
            color: #155724;
        }
        
        .option.wrong {
            border-color: #f45c43;
            background: #f8d7da;
            color: #721c24;
        }
        
        .show-answer-btn {
            margin-top: 15px;
            padding: 12px 25px;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border: none;
            border-radius: 10px;
            color: white;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .show-answer-btn:hover {
            transform: translateY(-2px);
        }
        
        .answer-display {
            margin-top: 15px;
            padding: 15px;
            background: #e8f5e9;
            border: 1px solid #38ef7d;
            border-radius: 10px;
            color: #2e7d32;
            display: none;
        }
        
        .fill-input {
            width: 100%;
            padding: 15px;
            font-size: 1.1em;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            margin-top: 15px;
        }
        
        .fill-feedback {
            margin-top: 10px;
            padding: 10px;
            border-radius: 8px;
            display: none;
        }
        
        /* 按钮区域 */
        .buttons {
            display: flex;
            gap: 15px;
            margin-top: 30px;
            flex-wrap: wrap;
        }
        
        .btn {
            flex: 1;
            padding: 15px 25px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        /* 结果界面 */
        .result-container {
            background: white;
            border-radius: 15px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
            display: none;
        }
        
        .score-display {
            font-size: 4em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .result-text {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 30px;
        }
        
        /* 浏览题目 */
        .browse-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            display: none;
        }
        
        .browse-filters {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #667eea;
            border-radius: 8px;
            background: white;
            color: #667eea;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
        }
        
        .filter-btn:hover {
            transform: translateY(-2px);
        }
        
        .browse-list {
            max-height: 600px;
            overflow-y: auto;
        }
        
        .browse-item {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        .browse-question {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 15px;
            line-height: 1.8;
        }
        
        .browse-options {
            margin-bottom: 10px;
        }
        
        .browse-option {
            color: #666;
            margin: 5px 0;
        }
        
        .browse-answer {
            color: #2e7d32;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 党旗飘飘</h1>
            <p>在线答题系统</p>
        </div>

        <!-- 主菜单 -->
        <div class="menu" id="menu">
            <h2>选择题目集</h2>
            <div class="set-selector">
                <button class="set-btn active" onclick="selectSet(1)">第一套</button>
                <button class="set-btn" onclick="selectSet(2)">第二套</button>
                <button class="set-btn" onclick="selectSet(3)">第三套</button>
                <button class="set-btn" onclick="selectSet(0)">全部题目</button>
            </div>
            <div class="menu-buttons">
                <button class="menu-btn start" onclick="startQuiz()">开始答题</button>
                <button class="menu-btn browse" onclick="startBrowse()">浏览题目</button>
            </div>
        </div>

        <!-- 答题界面 -->
        <div class="quiz-container" id="quiz">
            <div class="question-card" id="questionCard"></div>
            <div class="buttons">
                <button class="btn btn-secondary" onclick="prevQuestion()">上一题</button>
                <button class="btn btn-primary" onclick="nextQuestion()">下一题</button>
            </div>
            <div class="buttons">
                <button class="btn btn-secondary" onclick="showResult()" style="flex: 1; margin-top: 15px;">查看答案</button>
                <button class="btn btn-secondary" onclick="backToMenu()">返回菜单</button>
            </div>
        </div>

        <!-- 结果界面 -->
        <div class="result-container" id="result">
            <div class="score-display" id="scoreDisplay">0</div>
            <div class="result-text" id="resultText"></div>
            <div class="buttons">
                <button class="btn btn-primary" onclick="startQuiz()">再来一次</button>
                <button class="btn btn-secondary" onclick="backToMenu()">返回菜单</button>
            </div>
        </div>

        <!-- 浏览题目 -->
        <div class="browse-container" id="browse">
            <div class="browse-filters">
                <button class="filter-btn active" onclick="filterBrowse(0)">全部</button>
                <button class="filter-btn" onclick="filterBrowse('single_choice')">单选题</button>
                <button class="filter-btn" onclick="filterBrowse('multiple_choice')">多选题</button>
                <button class="filter-btn" onclick="filterBrowse('true_false')">判断题</button>
                <button class="filter-btn" onclick="filterBrowse('fill_blank')">填空题</button>
            </div>
            <div class="browse-list" id="browseList"></div>
            <div class="buttons" style="margin-top: 25px;">
                <button class="btn btn-secondary" onclick="backToMenu()">返回菜单</button>
            </div>
        </div>
    </div>

    <script>
        // 题目数据
        const allQuestions = QUESTIONS_DATA;
        let currentSet = 1;
        let quizQuestions = [];
        let currentIndex = 0;
        let userAnswers = {};
        let browseFilter = 0;

        // 初始化
        function selectSet(set) {
            currentSet = set;
            document.querySelectorAll('.set-btn').forEach((btn, idx) => {
                btn.classList.toggle('active', (idx === 0 && set === 1) || (idx === 1 && set === 2) || (idx === 2 && set === 3) || (idx === 3 && set === 0));
            });
            // 修正按钮状态
            const buttons = document.querySelectorAll('.set-btn');
            buttons[0].classList.toggle('active', set === 1);
            buttons[1].classList.toggle('active', set === 2);
            buttons[2].classList.toggle('active', set === 3);
            buttons[3].classList.toggle('active', set === 0);
        }

        // 开始答题
        function startQuiz() {
            if (currentSet === 0) {
                quizQuestions = [...allQuestions];
            } else {
                quizQuestions = allQuestions.filter(q => q.set === currentSet);
            }
            // 打乱题目
            for (let i = quizQuestions.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [quizQuestions[i], quizQuestions[j]] = [quizQuestions[j], quizQuestions[i];
            }
            currentIndex = 0;
            userAnswers = {};
            showMenu(false);
            showQuiz(true);
            showQuestion();
        }

        // 显示题目
        function showQuestion() {
            const q = quizQuestions[currentIndex];
            const card = document.getElementById('questionCard');
            
            let html = `
                <div class="question-number">
                    第 ${currentIndex + 1} 题 / 共 ${quizQuestions.length} 题
                    <span style="float:right;">
                        ${q.set === 1 ? '第一套' : q.set === 2 ? '第二套' : '第三套'} · 
                        ${q.type === 'single_choice' ? '单选题' : q.type === 'multiple_choice' ? '多选题' : q.type === 'true_false' ? '判断题' : '填空题'}
                    </span>
                </div>
                <div class="question">${q.question}</div>
            `;

            if (q.type === 'single_choice' || q.type === 'multiple_choice') {
                html += '<div class="options">';
                q.options.forEach((opt, idx) => {
                    const letter = String.fromCharCode(65 + idx);
                    const selected = userAnswers[q.id] === letter;
                    html += `<div class="option ${selected ? 'selected' : ''}" onclick="selectOption(${q.id}, '${letter}', this)">${letter}. ${opt}</div>`;
                });
                html += '</div>';
            } else if (q.type === 'true_false') {
                html += '<div class="options">';
                html += `<div class="option ${userAnswers[q.id] === true ? 'selected' : ''}" onclick="selectOption(${q.id}, true, this)">A. 正确</div>';
                html += `<div class="option ${userAnswers[q.id] === false ? 'selected' : ''}" onclick="selectOption(${q.id}, false, this)">B. 错误</div>';
                html += '</div>';
            } else {
                html += `<input type="text" class="fill-input" id="fill-${q.id}" placeholder="请输入答案" value="${userAnswers[q.id] || ''}" oninput="userAnswers[${q.id}] = this.value">`;
                html += `<div class="buttons" style="margin-top: 15px;">
                    <button class="show-answer-btn" onclick="checkFillAnswer(${q.id}, this)">检查答案</button>
                </div>`;
                html += `<div class="fill-feedback" id="fill-feedback-${q.id}"></div>`;
            }

            // 显示答案按钮
            html += `<div class="answer-display" id="answer-${q.id}">正确答案：${q.answer}</div>`;

            card.innerHTML = html;
        }

        // 选择选项
        function selectOption(qid, value, el) {
            userAnswers[qid] = value;
            const q = quizQuestions.find(x => x.id === qid);
            
            const siblings = el.parentElement.children;
            for (let sibling of siblings) {
                sibling.classList.remove('selected', 'correct', 'wrong');
            }
            el.classList.add('selected');
            
            let isCorrect = false;
            if (q.type === 'true_false') {
                isCorrect = (value === true && q.answer === true) || (value === false && q.answer === false);
            } else {
                isCorrect = value.toUpperCase() === String(q.answer).toUpperCase();
            }
            
            if (isCorrect) {
                el.classList.remove('selected');
                el.classList.add('correct');
            } else {
                el.classList.remove('selected');
                el.classList.add('wrong');
                showCorrectAnswer(q, el.parentElement);
            }
        }

        // 显示正确答案
        function showCorrectAnswer(q, container) {
            const answerDiv = document.createElement('div');
            answerDiv.className = 'answer-display';
            answerDiv.style.display = 'block';
            answerDiv.textContent = '正确答案：' + q.answer;
            container.appendChild(answerDiv);
        }

        // 检查填空答案
        function checkFillAnswer(qid, btn) {
            const input = document.getElementById(`fill-${qid}');
            const feedback = document.getElementById(`fill-feedback-${qid}`);
            const q = quizQuestions.find(x => x.id === qid);
            const userAnswer = input.value.trim();
            const correctAnswer = String(q.answer || '').trim();
            
            const isCorrect = userAnswer === correctAnswer;
            
            feedback.style.display = 'block';
            if (isCorrect) {
                feedback.style.background = '#d4edda';
                feedback.style.color = '#155724';
                feedback.innerHTML = '✅ 回答正确！';
                input.style.borderColor = '#38ef7d';
            } else {
                feedback.style.background = '#f8d7da';
                feedback.style.color = '#721c24';
                feedback.innerHTML = '❌ 回答错误！正确答案是：<strong>' + correctAnswer + '</strong>';
                input.style.borderColor = '#f45c43';
            }
        }

        // 上一题
        function prevQuestion() {
            if (currentIndex > 0) {
                currentIndex--;
                showQuestion();
            }
        }

        // 下一题
        function nextQuestion() {
            if (currentIndex < quizQuestions.length - 1) {
                currentIndex++;
                showQuestion();
            } else {
                calculateResult();
            }
        }

        // 查看答案
        function showResult() {
            const q = quizQuestions[currentIndex];
            const answerDiv = document.getElementById(`answer-${q.id}`);
            if (answerDiv) {
                answerDiv.style.display = 'block';
            }
        }

        // 计算结果
        function calculateResult() {
            let correct = 0;
            quizQuestions.forEach(q => {
                const userAns = userAnswers[q.id];
                if (q.type === 'true_false') {
                    if ((userAns === true && q.answer === true) || (userAns === false && q.answer === false)) {
                        correct++;
                    }
                } else {
                    if (String(userAns || '').toUpperCase() === String(q.answer).toUpperCase()) {
                        correct++;
                    }
                }
            });
            document.getElementById('scoreDisplay').textContent = `${correct} / ${quizQuestions.length}`;
            const percent = Math.round((correct / quizQuestions.length) * 100);
            let text = '';
            if (percent >= 90) text = '🎉 太棒了！';
            else if (percent >= 70) text = '👍 不错！继续加油！';
            else if (percent >= 60) text = '💪 及格了，继续努力！';
            else text = '📚 还需要多练习哦！';
            document.getElementById('resultText').textContent = text;
            showQuiz(false);
            showResultDiv(true);
        }

        // 开始浏览
        function startBrowse() {
            showMenu(false);
            showBrowse(true);
            renderBrowseList();
        }

        // 渲染浏览列表
        function renderBrowseList() {
            let questionsToShow;
            if (currentSet === 0) {
                questionsToShow = [...allQuestions];
            } else {
                questionsToShow = allQuestions.filter(q => q.set === currentSet);
            }
            if (browseFilter !== 0) {
                questionsToShow = questionsToShow.filter(q => q.type === browseFilter);
            }
            const list = document.getElementById('browseList');
            let html = '';
            questionsToShow.forEach(q => {
                html += '<div class="browse-item">';
                html += `<div class="browse-question">【${q.set === 1 ? '第一套' : q.set === 2 ? '第二套' : '第三套'} · ${q.type === 'single_choice' ? '单选题' : q.type === 'multiple_choice' ? '多选题' : q.type === 'true_false' ? '判断题' : '填空题'}】${q.question}</div>`;
                if (q.type === 'single_choice' || q.type === 'multiple_choice') {
                    html += '<div class="browse-options">';
                    q.options.forEach((opt, idx) => {
                        const letter = String.fromCharCode(65 + idx);
                        html += `<div class="browse-option">${letter}. ${opt}</div>`;
                    });
                    html += '</div>';
                }
                html += `<div class="browse-answer">正确答案：${q.answer}</div>`;
                html += '</div>';
            });
            list.innerHTML = html;
        }

        // 过滤浏览
        function filterBrowse(type) {
            browseFilter = type;
            document.querySelectorAll('.filter-btn').forEach((btn, idx) => {
                btn.classList.toggle('active', (idx === 0 && type === 0) || (idx === 1 && type === 'single_choice') || (idx === 2 && type === 'multiple_choice') || (idx === 3 && type === 'true_false') || (idx === 4 && type === 'fill_blank'));
            });
            renderBrowseList();
        }

        // 显示/隐藏界面
        function showMenu(show) {
            document.getElementById('menu').classList.toggle('hidden', !show);
        }

        function showQuiz(show) {
            document.getElementById('quiz').classList.toggle('hidden', !show);
        }

        function showResultDiv(show) {
            document.getElementById('result').classList.toggle('hidden', !show);
        }

        function showBrowse(show) {
            document.getElementById('browse').classList.toggle('hidden', !show);
        }

        function backToMenu() {
            showQuiz(false);
            showResultDiv(false);
            showBrowse(false);
            showMenu(true);
        }
    </script>
</body>
</html>'''

# 替换数据
final_html = html_template.replace('QUESTIONS_DATA', questions_js)

# 保存
with open('../index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print('✅ 纯静态网页生成成功！')
