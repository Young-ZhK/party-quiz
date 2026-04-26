
import json

# 1. 读取题目数据
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 2. 把题目数据转为 JS 字符串
questions_js = json.dumps(questions, ensure_ascii=False)

# 3. 读取原始的 index-original.html
with open('index-original.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 4. 找到需要替换的部分：
# 替换 1: 开头的 allQuestionsData 部分（如果有）
# 替换 2: startQuiz 函数里的随机题数量（从 10 改到 20）
# 替换 3: startQuiz 函数不使用 API，直接从 allQuestionsData 读取
# 替换 4: submitQuiz 函数不使用 API，直接在客户端计算
# 替换 5: startBrowse 函数不使用 API，直接从 allQuestionsData 读取
# 替换 6: startReciteMode 函数不使用 API，直接从 allQuestionsData 读取
# 替换 7: showWrongQuestions 和 showStarredQuestions 函数不使用 API
# 替换 8: startImmersive 函数不使用 API

# 首先，移除 API_BASE 和 fetch 相关的，改成纯客户端版本

# 5. 完整的静态 JS 代码
static_js = f'''
    // ========== 嵌入式题目数据（共{len(questions)}道题）==========
    const allQuestionsData = {questions_js};
    
    // ========== 页面初始化 ==========
    window.onload = function() {{
        // 确保只显示菜单，隐藏所有其他容器
        document.getElementById('menu').style.display = 'block';
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        document.getElementById('immersive').style.display = 'none';
        document.getElementById('im-results').style.display = 'none';
        document.getElementById('recite').style.display = 'none';
        document.getElementById('special-list').style.display = 'none';
    }};
    
    let questions = [];
    let currentIndex = 0;
    let userAnswers = {{}};
    let currentQuizType = 'all';
    let currentSet = 'all';
    let answerShown = false;
    
    // ========== 错题本和重点题 ==========
    let wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    let starredQuestions = JSON.parse(localStorage.getItem('starredQuestions') || '[]');
    let reciteQuestions = [];
    let reciteIndex = 0;
    let reciteAnswerShown = false;
    let specialListType = '';
    
    function saveWrongQuestions() {{
        localStorage.setItem('wrongQuestions', JSON.stringify(wrongQuestions));
    }}
    
    function saveStarredQuestions() {{
        localStorage.setItem('starredQuestions', JSON.stringify(starredQuestions));
    }}
    
    function addToWrongQuestions(qId) {{
        if (!wrongQuestions.includes(qId)) {{
            wrongQuestions.push(qId);
            saveWrongQuestions();
        }}
    }}
    
    function removeFromWrongQuestions(qId) {{
        const idx = wrongQuestions.indexOf(qId);
        if (idx !== -1) {{
            wrongQuestions.splice(idx, 1);
            saveWrongQuestions();
        }}
    }}
    
    function isQuestionStarred(qId) {{
        return starredQuestions.includes(qId);
    }}
    
    function toggleReciteStar() {{
        const q = reciteQuestions[reciteIndex];
        if (!q) return;
        const wasStarred = toggleStar(q.uid);
        document.getElementById('recite-star-btn').textContent = wasStarred ? '⭐' : '☆';
    }}
    
    function toggleStar(qId) {{
        const idx = starredQuestions.indexOf(qId);
        if (idx === -1) {{
            starredQuestions.push(qId);
        }} else {{
            starredQuestions.splice(idx, 1);
        }}
        saveStarredQuestions();
        return idx === -1;
    }}
    
    // ========== 搜索功能 ==========
    function handleSearchKey(event) {{
        if (event.key === 'Enter') {{
            searchQuestions();
        }}
    }}
    
    function searchQuestions() {{
        const keyword = document.getElementById('search-input').value.trim().toLowerCase();
        const resultsContainer = document.getElementById('search-results');
        
        if (!keyword) {{
            resultsContainer.style.display = 'none';
            return;
        }}
        
        let results = [];
        for (const q of allQuestionsData) {{
            const questionText = q.question.toLowerCase();
            const answerText = String(q.answer).toLowerCase();
            if (questionText.includes(keyword) || answerText.includes(keyword)) {{
                results.push(q);
            }}
        }}
        
        if (results.length === 0) {{
            resultsContainer.innerHTML = '<p style="text-align: center; color: #666; font-size: 1.1em;">没有找到相关题目 😔</p>';
        }} else {{
            let html = '';
            for (const q of results) {{
                let setName = '';
                if (q.set === 1) setName = '第一套';
                else if (q.set === 2) setName = '第二套';
                else if (q.set === 3) setName = '第三套';
                else if (q.set === 4) setName = '第四套';
                else if (q.set === 5) setName = '第五套';
                else if (q.set === 6) setName = '第六套';
                else if (q.set === 7) setName = '第七套';
                else if (q.set === 8) setName = '第八套';
                
                let typeName = '';
                if (q.type === 'single_choice') typeName = '单选题';
                else if (q.type === 'multiple_choice') typeName = '多选题';
                else if (q.type === 'true_false') typeName = '判断题';
                else if (q.type === 'fill_blank') typeName = '填空题';
                
                let answerDisplay = '';
                if (q.type === 'true_false') {{
                    answerDisplay = q.answer ? '正确' : '错误';
                }} else {{
                    answerDisplay = q.answer;
                }}
                
                html += '<div class="search-item">';
                html += '<div style="margin-bottom: 8px;"><span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em; margin-right: 8px;">' + setName + '</span><span style="background: #f5576c; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em;">' + typeName + '</span></div>';
                html += '<div class="search-item-question">' + q.question + '</div>';
                if (q.options && q.options.length > 0) {{
                    html += '<div style="margin: 10px 0;">';
                    const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                    for (let i = 0; i < q.options.length; i++) {{
                        html += '<div style="margin: 5px 0; color: #555;">' + labels[i] + '. ' + q.options[i] + '</div>';
                    }}
                    html += '</div>';
                }}
                html += '<div class="search-item-answer">✅ 正确答案：' + answerDisplay + '</div>';
                html += '</div>';
            }}
            
            resultsContainer.innerHTML = html;
        }}
        
        resultsContainer.style.display = 'block';
    }}

    // 沉浸式做题的变量
    let imQuestions = [];
    let imCurrentIndex = 0;
    let imUserAnswers = {{}};
    let imCurrentSet = '1';

    function selectSet(set) {{
        currentSet = set;
        document.querySelectorAll('.set-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById('set-' + set).classList.add('active');
    }}

    function toggleAnswer() {{
        const q = questions[currentIndex];
        const answerSection = document.getElementById('answer-section');
        const showAnswerBtn = document.getElementById('show-answer-btn');
        
        if (answerShown) {{
            answerSection.classList.remove('show');
            showAnswerBtn.textContent = '显示答案';
            answerShown = false;
        }} else {{
            let answerText = '';
            
            if (q.type === 'true_false') {{
                answerText = q.answer ? '正确' : '错误';
            }} else {{
                answerText = q.answer;
            }}
            
            document.getElementById('answer-content').textContent = answerText;
            answerSection.classList.add('show');
            showAnswerBtn.textContent = '隐藏答案';
            answerShown = true;
        }}
    }}

    function startQuiz(type) {{
        currentQuizType = type;
        currentIndex = 0;
        userAnswers = {{}};
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        
        // 从 allQuestionsData 中筛选题目
        let filtered = [...allQuestionsData];
        if (currentSet !== 'all') {{
            filtered = filtered.filter(q => q.set === parseInt(currentSet));
        }}
        if (type !== 'all' && type !== 'random') {{
            filtered = filtered.filter(q => q.type === type);
        }}
        if (type === 'random') {{
            // 随机打乱，然后取前 20 题
            for (let i = filtered.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
            }}
            filtered = filtered.slice(0, 20);
        }}
        
        questions = filtered;
        displayQuestion();
    }}

    function displayQuestion() {{
        const q = questions[currentIndex];
        
        answerShown = false;
        document.getElementById('answer-section').classList.remove('show');
        document.getElementById('show-answer-btn').textContent = '显示答案';
        
        document.getElementById('q-number').textContent = '第 ' + (currentIndex + 1) + ' 题 / 共 ' + questions.length + ' 题';
        
        const typeNames = {{
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        }};
        
        const typeClass = {{
            'single_choice': 'type-single',
            'multiple_choice': 'type-multiple',
            'true_false': 'type-tf',
            'fill_blank': 'type-fill'
        }};
        
        const typeEl = document.getElementById('q-type');
        typeEl.textContent = typeNames[q.type];
        typeEl.className = 'question-type ' + typeClass[q.type];
        
        const setEl = document.getElementById('q-set');
        setEl.textContent = q.set ? '第' + q.set + '套' : '题目';
        
        document.getElementById('q-text').textContent = q.question;
        
        const optionsEl = document.getElementById('options');
        optionsEl.innerHTML = '';
        
        const qId = q.uid || q.id;
        
        if (q.type === 'fill_blank') {{
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'fill-input';
            input.placeholder = '请输入答案...';
            input.value = userAnswers[qId] || '';
            input.oninput = function(e) {{ userAnswers[qId] = e.target.value; }};
            optionsEl.appendChild(input);
            
            const checkBtn = document.createElement('button');
            checkBtn.className = 'show-answer-btn';
            checkBtn.textContent = '检查答案';
            checkBtn.style.marginTop = '10px';
            checkBtn.onclick = function() {{
                checkFillAnswer(qId, input, q, optionsEl);
            }};
            optionsEl.appendChild(checkBtn);
            
            const feedback = document.createElement('div');
            feedback.id = 'fill-feedback-' + qId;
            feedback.style.marginTop = '10px';
            feedback.style.padding = '10px';
            feedback.style.borderRadius = '8px';
            feedback.style.display = 'none';
            optionsEl.appendChild(feedback);
        }} else if (q.type === 'true_false') {{
            ['正确', '错误'].forEach((opt, i) => {{
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = opt;
                const val = i === 0;
                if (userAnswers[qId] === val) {{
                    div.classList.add('selected');
                    let isCorrect = (val === q.answer);
                    if (isCorrect) {{
                        div.classList.remove('selected');
                        div.classList.add('correct');
                        removeFromWrongQuestions(qId);
                    }} else {{
                        div.classList.remove('selected');
                        div.classList.add('wrong');
                        addToWrongQuestions(qId);
                    }}
                }}
                div.onclick = function() {{ selectOption(qId, val, div); }};
                optionsEl.appendChild(div);
            }});
        }} else {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {{
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = labels[i] + '. ' + opt;
                
                if (q.type === 'multiple_choice') {{
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {{
                        div.classList.add('selected');
                    }}
                }} else {{
                    if (userAnswers[qId] === labels[i]) {{
                        div.classList.add('selected');
                        let isCorrect = (labels[i] === String(q.answer).toUpperCase());
                        if (isCorrect) {{
                            div.classList.remove('selected');
                            div.classList.add('correct');
                            removeFromWrongQuestions(qId);
                        }} else {{
                            div.classList.remove('selected');
                            div.classList.add('wrong');
                            showCorrectAnswer(q, optionsEl);
                        }}
                    }}
                }}
                
                div.onclick = function() {{ selectOption(qId, labels[i], div, q.type); }};
                optionsEl.appendChild(div);
            }});
        }}
        
        document.getElementById('btn-prev').style.display = currentIndex > 0 ? 'block' : 'none';
        
        if (currentIndex === questions.length - 1) {{
            document.getElementById('btn-next').style.display = 'none';
            document.getElementById('btn-submit').style.display = 'block';
        }} else {{
            document.getElementById('btn-next').style.display = 'block';
            document.getElementById('btn-submit').style.display = 'none';
        }}
    }}

    function selectOption(qId, value, el, qType) {{
        const q = questions.find(x => (x.uid || x.id) === qId) || questions[currentIndex];
        
        if (qType === 'multiple_choice' || q.type === 'multiple_choice') {{
            if (!Array.isArray(userAnswers[qId])) {{
                userAnswers[qId] = [];
            }}
            const idx = userAnswers[qId].indexOf(value);
            if (idx === -1) {{
                userAnswers[qId].push(value);
            }} else {{
                userAnswers[qId].splice(idx, 1);
            }}
            
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            const siblings = el.parentElement.children;
            for (let i = 0; i < siblings.length; i++) {{
                const sibling = siblings[i];
                sibling.classList.remove('selected', 'correct', 'wrong');
                if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {{
                    sibling.classList.add('selected');
                }}
            }}
            
            const userAnswer = Array.isArray(userAnswers[qId]) ? userAnswers[qId].sort().join('') : '';
            const correctAnswer = String(q.answer).toUpperCase().split('').sort().join('');
            const isCorrect = userAnswer === correctAnswer;
            
            if (isCorrect) {{
                for (let i = 0; i < siblings.length; i++) {{
                    const sibling = siblings[i];
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {{
                        sibling.classList.remove('selected');
                        sibling.classList.add('correct');
                    }}
                }}
                removeFromWrongQuestions(qId);
            }} else {{
                showCorrectAnswer(q, el.parentElement);
                for (let i = 0; i < siblings.length; i++) {{
                    const sibling = siblings[i];
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {{
                        sibling.classList.remove('selected');
                        if (String(q.answer).toUpperCase().includes(labels[i])) {{
                            sibling.classList.add('correct');
                        }} else {{
                            sibling.classList.add('wrong');
                        }}
                    }}
                }}
                addToWrongQuestions(qId);
            }}
        }} else {{
            userAnswers[qId] = value;
            
            const siblings = el.parentElement.children;
            for (let sibling of siblings) {{
                sibling.classList.remove('selected', 'correct', 'wrong');
            }}
            el.classList.add('selected');
            
            let isCorrect = false;
            if (q.type === 'true_false') {{
                isCorrect = (value === true && q.answer === true) || (value === false && q.answer === false);
            }} else {{
                isCorrect = value.toUpperCase() === String(q.answer).toUpperCase();
            }}
            
            if (isCorrect) {{
                el.classList.remove('selected');
                el.classList.add('correct');
                removeFromWrongQuestions(qId);
            }} else {{
                el.classList.remove('selected');
                el.classList.add('wrong');
                showCorrectAnswer(q, el.parentElement);
                addToWrongQuestions(qId);
            }}
        }}
    }}
    
    function showCorrectAnswer(q, optionsContainer) {{
        if (q.type === 'true_false') {{
            const options = optionsContainer.children;
            const correctIndex = q.answer ? 0 : 1;
            if (options[correctIndex]) {{
                options[correctIndex].classList.add('correct');
            }}
        }} else {{
            const labels = ['A', 'B', 'C', 'D'];
            const answerStr = String(q.answer).toUpperCase();
            const options = optionsContainer.children;
            for (let i = 0; i < options.length; i++) {{
                if (answerStr.includes(labels[i])) {{
                    options[i].classList.add('correct');
                }}
            }}
        }}
    }}
    
    function checkFillAnswer(qId, input, q, container) {{
        const feedback = document.getElementById('fill-feedback-' + qId);
        const userAnswer = input.value.trim();
        const correctAnswer = String(q.answer || '').trim();
        
        const isCorrect = userAnswer === correctAnswer;
        
        feedback.style.display = 'block';
        if (isCorrect) {{
            feedback.style.background = '#d4edda';
            feedback.style.color = '#155724';
            feedback.innerHTML = '✅ 回答正确！';
            input.style.borderColor = '#38ef7d';
            removeFromWrongQuestions(qId);
        }} else {{
            feedback.style.background = '#f8d7da';
            feedback.style.color = '#721c24';
            feedback.innerHTML = '❌ 回答错误！正确答案是：<strong>' + correctAnswer + '</strong>';
            input.style.borderColor = '#f45c43';
            addToWrongQuestions(qId);
        }}
    }}

    function prevQuestion() {{
        if (currentIndex > 0) {{
            currentIndex--;
            displayQuestion();
        }}
    }}

    function nextQuestion() {{
        if (currentIndex < questions.length - 1) {{
            currentIndex++;
            displayQuestion();
        }}
    }}

    function submitQuiz() {{
        let correct = 0;
        const results = [];
        questions.forEach((q, index) => {{
            const qId = q.uid || q.id;
            let userAnswer = userAnswers[qId];
            let isCorrect = false;
            
            if (q.type === 'true_false') {{
                isCorrect = (userAnswer === q.answer);
            }} else if (q.type === 'multiple_choice') {{
                const userAnswerStr = Array.isArray(userAnswer) ? userAnswer.sort().join('') : '';
                const correctAnswerStr = String(q.answer).toUpperCase().split('').sort().join('');
                isCorrect = (userAnswerStr === correctAnswerStr);
                userAnswer = Array.isArray(userAnswer) ? userAnswer.join('') : '未作答';
            }} else if (q.type === 'fill_blank') {{
                isCorrect = String(userAnswer || '').trim() === String(q.answer || '').trim();
            }} else {{
                isCorrect = String(userAnswer || '').toUpperCase() === String(q.answer || '').toUpperCase();
            }}
            
            if (isCorrect) {{
                correct++;
            }} else {{
                addToWrongQuestions(qId);
            }}
            
            results.push({{
                id: qId,
                correct: isCorrect,
                user_answer: userAnswer || '未作答',
                correct_answer: q.type === 'true_false' ? (q.answer ? '正确' : '错误') : q.answer,
                question: q.question,
                set: q.set
            }});
        }});
        
        showResults({{
            score: correct,
            total: questions.length,
            results: results
        }});
    }}

    function showResults(result) {{
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'block';
        
        document.getElementById('score-display').textContent = result.score + '/' + result.total;
        
        const percentage = Math.round((result.score / result.total) * 100);
        let text = '';
        if (percentage >= 90) text = '🎉 太棒了！成绩优秀！';
        else if (percentage >= 70) text = '👍 不错！继续努力！';
        else if (percentage >= 60) text = '💪 及格了，但还需要加强！';
        else text = '📚 需要多练习哦！';
        document.getElementById('score-text').textContent = text;
        
        const detailsEl = document.getElementById('result-details');
        detailsEl.innerHTML = '';
        
        result.results.forEach((res, index) => {{
            const q = questions[index];
            let optionsHtml = '';
            let userAnswerWithOption = res.user_answer;
            let correctAnswerWithOption = res.correct_answer;
            
            if (q.type !== 'fill_blank' && q.type !== 'true_false' && q.options && q.options.length > 0) {{
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                optionsHtml = '<div style="font-size: 0.9em; margin-top: 8px; color: #666;">';
                
                q.options.forEach((opt, i) => {{
                    const label = labels[i] || String.fromCharCode(65 + i);
                    optionsHtml += '<div style="margin: 4px 0;">' + label + '. ' + opt + '</div>';
                }});
                optionsHtml += '</div>';
            }}
            
            detailsEl.innerHTML += '<div class="result-item ' + (res.correct ? 'result-correct' : 'result-wrong') + '">' +
                '<strong>第 ' + (index + 1) + ' 题（第' + res.set + '套）</strong>' + res.question +
                optionsHtml +
                '<br><em>你的答案：' + userAnswerWithOption + ' | 正确答案：' + correctAnswerWithOption + '</em>' +
                '</div>';
        }});
    }}

    function backToMenu() {{
        document.getElementById('menu').style.display = 'block';
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        document.getElementById('immersive').style.display = 'none';
        document.getElementById('im-results').style.display = 'none';
        document.getElementById('recite').style.display = 'none';
        document.getElementById('special-list').style.display = 'none';
    }}

    // ========== 沉浸式做题函数 ==========
    function startImmersive(set) {{
        imCurrentSet = set;
        imCurrentIndex = 0;
        imUserAnswers = {{}};

        document.getElementById('menu').style.display = 'none';
        document.getElementById('immersive').style.display = 'block';
        document.getElementById('im-results').style.display = 'none';

        // 获取指定套的100题
        imQuestions = allQuestionsData.filter(q => q.set === parseInt(set));

        // 渲染题目列表
        renderImQuestionGrid();

        imDisplayQuestion();
    }}

    function renderImQuestionGrid() {{
        const grid = document.getElementById('im-question-grid');
        grid.innerHTML = '';
        
        imQuestions.forEach((q, index) => {{
            const dot = document.createElement('div');
            dot.className = 'question-dot';
            dot.textContent = index + 1;
            dot.onclick = () => imGoToQuestion(index);
            grid.appendChild(dot);
        }});
        
        updateImQuestionGrid();
    }}

    function updateImQuestionGrid() {{
        const dots = document.querySelectorAll('#im-question-grid .question-dot');
        
        dots.forEach((dot, index) => {{
            dot.classList.remove('answered', 'current');
            
            const q = imQuestions[index];
            const qId = q.uid || q.id;
            const isAnswered = imUserAnswers[qId] !== undefined && 
                (Array.isArray(imUserAnswers[qId]) ? imUserAnswers[qId].length > 0 : imUserAnswers[qId] !== '');
            
            if (isAnswered) {{
                dot.classList.add('answered');
            }}
            
            if (index === imCurrentIndex) {{
                dot.classList.add('current');
            }}
        }});
    }}

    function imGoToQuestion(index) {{
        imCurrentIndex = index;
        imDisplayQuestion();
    }}

    function imDisplayQuestion() {{
        const q = imQuestions[imCurrentIndex];
        
        document.getElementById('im-q-number').textContent = '第 ' + (imCurrentIndex + 1) + ' 题 / 共 ' + imQuestions.length + ' 题';

        const typeNames = {{
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        }};

        const typeClass = {{
            'single_choice': 'type-single',
            'multiple_choice': 'type-multiple',
            'true_false': 'type-tf',
            'fill_blank': 'type-fill'
        }};

        const typeEl = document.getElementById('im-q-type');
        typeEl.textContent = typeNames[q.type];
        typeEl.className = 'question-type ' + typeClass[q.type];

        const setEl = document.getElementById('im-q-set');
        setEl.textContent = '第' + q.set + '套';

        document.getElementById('im-q-text').textContent = q.question;

        const optionsEl = document.getElementById('im-options');
        optionsEl.innerHTML = '';

        const qId = q.uid || q.id;

        if (q.type === 'fill_blank') {{
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'fill-input';
            input.placeholder = '请输入答案...';
            input.value = imUserAnswers[qId] || '';
            input.oninput = function(e) {{ 
                imUserAnswers[qId] = e.target.value; 
                updateImQuestionGrid();
            }};
            optionsEl.appendChild(input);
        }} else if (q.type === 'true_false') {{
            ['正确', '错误'].forEach((opt, i) => {{
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = opt;
                const val = i === 0;
                if (imUserAnswers[qId] === val) {{
                    div.classList.add('selected');
                }}
                div.onclick = function() {{ imSelectOption(qId, val, div); }};
                optionsEl.appendChild(div);
            }});
        }} else {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {{
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = labels[i] + '. ' + opt;
                
                if (q.type === 'multiple_choice') {{
                    if (Array.isArray(imUserAnswers[qId]) && imUserAnswers[qId].includes(labels[i])) {{
                        div.classList.add('selected');
                    }}
                }} else {{
                    if (imUserAnswers[qId] === labels[i]) {{
                        div.classList.add('selected');
                    }}
                }}
                
                div.onclick = function() {{ imSelectOption(qId, labels[i], div, q.type); }};
                optionsEl.appendChild(div);
            }});
        }}

        document.getElementById('im-btn-prev').style.display = imCurrentIndex > 0 ? 'block' : 'none';
        document.getElementById('im-btn-next').style.display = imCurrentIndex < imQuestions.length - 1 ? 'block' : 'none';
        
        updateImQuestionGrid();
    }}

    function imSelectOption(qId, value, el, qType) {{
        const q = imQuestions[imCurrentIndex];
        
        if (qType === 'multiple_choice' || q.type === 'multiple_choice') {{
            if (!Array.isArray(imUserAnswers[qId])) {{
                imUserAnswers[qId] = [];
            }}
            const idx = imUserAnswers[qId].indexOf(value);
            if (idx === -1) {{
                imUserAnswers[qId].push(value);
            }} else {{
                imUserAnswers[qId].splice(idx, 1);
            }}
            
            const labels = ['A', 'B', 'C', 'D'];
            const siblings = el.parentElement.children;
            for (let i = 0; i < siblings.length; i++) {{
                const sibling = siblings[i];
                sibling.classList.remove('selected');
                if (Array.isArray(imUserAnswers[qId]) && imUserAnswers[qId].includes(labels[i])) {{
                    sibling.classList.add('selected');
                }}
            }}
        }} else {{
            imUserAnswers[qId] = value;
            
            const siblings = el.parentElement.children;
            for (let sibling of siblings) {{
                sibling.classList.remove('selected');
            }}
            el.classList.add('selected');
        }}
        
        updateImQuestionGrid();
    }}

    function imPrevQuestion() {{
        if (imCurrentIndex > 0) {{
            imCurrentIndex--;
            imDisplayQuestion();
        }}
    }}

    function imNextQuestion() {{
        if (imCurrentIndex < imQuestions.length - 1) {{
            imCurrentIndex++;
            imDisplayQuestion();
        }}
    }}

    function imSubmitQuiz() {{
        let correct = 0;
        const results = [];

        imQuestions.forEach((q, index) => {{
            const qId = q.uid || q.id;
            let userAnswer = imUserAnswers[qId];
            let isCorrect = false;

            if (q.type === 'true_false') {{
                isCorrect = (userAnswer === q.answer);
            }} else if (q.type === 'multiple_choice') {{
                const userAnswerStr = Array.isArray(userAnswer) ? userAnswer.sort().join('') : String(userAnswer || '').toUpperCase();
                const correctAnswerStr = String(q.answer).toUpperCase().split('').sort().join('');
                isCorrect = userAnswerStr === correctAnswerStr;
                userAnswer = Array.isArray(userAnswer) ? userAnswer.join('') : userAnswer;
            }} else {{
                isCorrect = String(userAnswer || '').toUpperCase() === String(q.answer).toUpperCase();
            }}

            if (isCorrect) {{
                correct++;
            }} else {{
                addToWrongQuestions(qId);
            }}

            results.push({{
                id: qId,
                correct: isCorrect,
                user_answer: userAnswer || '未作答',
                correct_answer: q.type === 'true_false' ? (q.answer ? '正确' : '错误') : q.answer,
                question: q.question,
                set: q.set
            }});
        }});

        imShowResults({{
            score: correct,
            total: imQuestions.length,
            results: results
        }});
    }}

    function imShowResults(result) {{
        document.getElementById('immersive').style.display = 'none';
        document.getElementById('im-results').style.display = 'block';

        document.getElementById('im-score-display').textContent = result.score + '/' + result.total;

        const percentage = Math.round((result.score / result.total) * 100);
        let text = '';
        if (percentage >= 90) text = '🎉 太棒了！成绩优秀！';
        else if (percentage >= 70) text = '👍 不错！继续努力！';
        else if (percentage >= 60) text = '💪 及格了，但还需要加强！';
        else text = '📚 需要多练习哦！';
        document.getElementById('im-score-text').textContent = text;

        const detailsEl = document.getElementById('im-result-details');
        detailsEl.innerHTML = '';

        result.results.forEach((res, index) => {{
            const q = imQuestions[index];
            let optionsHtml = '';
            let userAnswerWithOption = res.user_answer;
            let correctAnswerWithOption = res.correct_answer;

            if (q.type !== 'fill_blank' && q.type !== 'true_false' && q.options && q.options.length > 0) {{
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                optionsHtml = '<div style="font-size: 0.9em; margin-top: 8px; color: #666;">';
                
                q.options.forEach((opt, i) => {{
                    const label = labels[i] || String.fromCharCode(65 + i);
                    optionsHtml += '<div style="margin: 4px 0;">' + label + '. ' + opt + '</div>';
                }});
                optionsHtml += '</div>';
            }}
            
            detailsEl.innerHTML += '<div class="result-item ' + (res.correct ? 'result-correct' : 'result-wrong') + '">' +
                '<strong>第 ' + (index + 1) + ' 题（第' + res.set + '套）</strong>' + res.question +
                optionsHtml +
                '<br><em>你的答案：' + userAnswerWithOption + ' | 正确答案：' + correctAnswerWithOption + '</em>' +
                '</div>';
        }});
    }}

    function imRestartQuiz() {{
        startImmersive(imCurrentSet);
    }}

    function restartQuiz() {{
        startQuiz(currentQuizType);
    }}

    function startBrowse() {{
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'block';
        
        filterBrowseQuestions();
    }}

    function filterBrowseQuestions() {{
        const setFilter = document.getElementById('browse-set-filter').value;
        const typeFilter = document.getElementById('browse-type-filter').value;
        
        let filtered = allQuestionsData;
        
        if (setFilter !== 'all') {{
            filtered = filtered.filter(q => q.set == setFilter);
        }}
        
        if (typeFilter !== 'all') {{
            filtered = filtered.filter(q => q.type === typeFilter);
        }}
        
        renderBrowseQuestions(filtered);
    }}

    function renderBrowseQuestions(questionsToRender) {{
        const listEl = document.getElementById('questions-list');
        listEl.innerHTML = '';
        
        if (questionsToRender.length === 0) {{
            listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">没有找到符合条件的题目</div>';
            return;
        }}
        
        const typeNames = {{
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        }};
        
        const typeColors = {{
            'single_choice': '#667eea',
            'multiple_choice': '#f093fb',
            'true_false': '#f5576c',
            'fill_blank': '#43e97b'
        }};
        
        const setNames = {{
            1: '第一套', 2: '第二套', 3: '第三套', 4: '第四套',
            5: '第五套', 6: '第六套', 7: '第七套', 8: '第八套'
        }};
        
        questionsToRender.forEach((q, index) => {{
            const card = document.createElement('div');
            card.className = 'browse-question-card';
            
            let optionsHtml = '';
            if (q.options && q.options.length > 0) {{
                optionsHtml = '<div class="browse-options">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {{
                    const isCorrect = (q.type === 'true_false') ? 
                        (i === 0 && q.answer) : 
                        (String(q.answer).toUpperCase().includes(labels[i]));
                    optionsHtml += '<div class="browse-option ' + (isCorrect ? 'correct' : '') + '">' + labels[i] + '. ' + opt + '</div>';
                }});
                optionsHtml += '</div>';
            }} else if (q.type === 'true_false') {{
                optionsHtml = '<div class="browse-options">';
                optionsHtml += '<div class="browse-option ' + (q.answer ? 'correct' : '') + '">正确</div>';
                optionsHtml += '<div class="browse-option ' + (!q.answer ? 'correct' : '') + '">错误</div>';
                optionsHtml += '</div>';
            }}
            
            let answerText = '';
            if (q.type === 'true_false') {{
                answerText = q.answer ? '正确' : '错误';
            }} else {{
                answerText = q.answer;
            }}
            
            card.innerHTML = '<div class="browse-header">' +
                '<div class="browse-question-number">第 ' + (index + 1) + ' 题（第' + q.set + '套 原编号' + q.id + '）</div>' +
                '<div class="browse-question-badges">' +
                '<span class="browse-badge" style="background: ' + typeColors[q.type] + ';">' + typeNames[q.type] + '</span>' +
                '</div>' +
                '</div>' +
                '<div class="browse-question-text">' + q.question + '</div>' +
                optionsHtml +
                '<div class="browse-answer-box">' +
                '<div class="browse-answer-label">正确答案</div>' +
                '<div class="browse-answer-text">' + answerText + '</div>' +
                '</div>';
            
            listEl.appendChild(card);
        }});
    }}

    // ========== 背诵模式函数 ==========
    function startReciteMode() {{
        const setFilter = document.getElementById('recite-set-filter').value;
        
        reciteQuestions = [];
        for (const q of allQuestionsData) {{
            if (setFilter === 'all' || String(q.set) === setFilter) {{
                reciteQuestions.push(q);
            }}
        }}
        
        reciteIndex = 0;
        reciteAnswerShown = false;
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('recite').style.display = 'block';
        
        renderReciteQuestionGrid();
        renderReciteQuestion();
    }}
    
    function renderReciteQuestionGrid() {{
        const grid = document.getElementById('recite-question-grid');
        grid.innerHTML = '';
        
        reciteQuestions.forEach((q, index) => {{
            const dot = document.createElement('div');
            dot.className = 'question-dot';
            dot.textContent = index + 1;
            dot.onclick = () => reciteGoToQuestion(index);
            grid.appendChild(dot);
        }});
        
        updateReciteQuestionGrid();
    }}
    
    function updateReciteQuestionGrid() {{
        const dots = document.querySelectorAll('#recite-question-grid .question-dot');
        
        dots.forEach((dot, index) => {{
            dot.classList.remove('current');
            if (index === reciteIndex) {{
                dot.classList.add('current');
            }}
        }});
    }}
    
    function reciteGoToQuestion(index) {{
        reciteIndex = index;
        renderReciteQuestion();
    }}
    
    function renderReciteQuestion() {{
        const q = reciteQuestions[reciteIndex];
        if (!q) return;
        
        document.getElementById('recite-number').textContent = '第 ' + (reciteIndex + 1) + ' 题（第' + q.set + '套）';
        document.getElementById('recite-question').textContent = q.question;
        document.getElementById('recite-star-btn').textContent = isQuestionStarred(q.uid) ? '⭐' : '☆';
        document.getElementById('recite-progress').textContent = (reciteIndex + 1) + '/' + reciteQuestions.length;
        
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            for (let i = 0; i < q.options.length; i++) {{
                optionsHtml += '<div style="margin: 8px 0; padding: 12px; background: #f5f5f5; border-radius: 8px;">' + labels[i] + '. ' + q.options[i] + '</div>';
            }}
        }} else if (q.type === 'true_false') {{
            optionsHtml += '<div style="margin: 8px 0; padding: 12px; background: #f5f5f5; border-radius: 8px;">正确</div>';
            optionsHtml += '<div style="margin: 8px 0; padding: 12px; background: #f5f5f5; border-radius: 8px;">错误</div>';
        }}
        document.getElementById('recite-options').innerHTML = optionsHtml;
        
        if (reciteAnswerShown) {{
            document.getElementById('recite-answer').style.display = 'block';
            document.getElementById('recite-toggle-btn').textContent = '隐藏答案';
            document.getElementById('recite-toggle-btn').style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
        }} else {{
            document.getElementById('recite-answer').style.display = 'none';
            document.getElementById('recite-toggle-btn').textContent = '显示答案';
            document.getElementById('recite-toggle-btn').style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }}
        
        let answerText = '';
        if (q.type === 'true_false') {{
            answerText = q.answer ? '正确' : '错误';
        }} else {{
            answerText = q.answer;
        }}
        document.getElementById('recite-answer-content').textContent = answerText;
        
        updateReciteQuestionGrid();
    }}
    
    function toggleReciteAnswer() {{
        reciteAnswerShown = !reciteAnswerShown;
        if (reciteAnswerShown) {{
            document.getElementById('recite-answer').style.display = 'block';
            document.getElementById('recite-toggle-btn').textContent = '隐藏答案';
            document.getElementById('recite-toggle-btn').style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
        }} else {{
            document.getElementById('recite-answer').style.display = 'none';
            document.getElementById('recite-toggle-btn').textContent = '显示答案';
            document.getElementById('recite-toggle-btn').style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }}
    }}
    
    function prevRecite() {{
        if (reciteIndex > 0) {{
            reciteIndex--;
            renderReciteQuestion();
        }}
    }}
    
    function nextRecite() {{
        if (reciteIndex < reciteQuestions.length - 1) {{
            reciteIndex++;
            renderReciteQuestion();
        }}
    }}

    // ========== 错题本和重点题函数 ==========
    function showWrongQuestions() {{
        specialListType = 'wrong';
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
        renderSpecialList();
    }}
    
    function showStarredQuestions() {{
        specialListType = 'starred';
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
        renderSpecialList();
    }}
    
    function renderSpecialList() {{
        const listEl = document.getElementById('special-list-content');
        listEl.innerHTML = '';
        
        let targetIds = specialListType === 'wrong' ? wrongQuestions : starredQuestions;
        let questionsToRender = allQuestionsData.filter(q => targetIds.includes(q.uid));
        
        if (questionsToRender.length === 0) {{
            listEl.innerHTML = '<div style="text-align: center; padding: 60px; color: #999; font-size: 1.2em;">' +
                (specialListType === 'wrong' ? '还没有错题哦，继续加油！' : '还没有重点题哦！') +
                '</div>';
            return;
        }}
        
        const typeNames = {{
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        }};
        
        const typeColors = {{
            'single_choice': '#667eea',
            'multiple_choice': '#f093fb',
            'true_false': '#f5576c',
            'fill_blank': '#43e97b'
        }};
        
        const setNames = {{
            1: '第一套', 2: '第二套', 3: '第三套', 4: '第四套',
            5: '第五套', 6: '第六套', 7: '第七套', 8: '第八套'
        }};
        
        questionsToRender.forEach((q, index) => {{
            const card = document.createElement('div');
            card.className = 'browse-question-card';
            
            let optionsHtml = '';
            if (q.options && q.options.length > 0) {{
                optionsHtml = '<div class="browse-options">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {{
                    const isCorrect = String(q.answer).toUpperCase().includes(labels[i]);
                    optionsHtml += '<div class="browse-option ' + (isCorrect ? 'correct' : '') + '">' + labels[i] + '. ' + opt + '</div>';
                }});
                optionsHtml += '</div>';
            }} else if (q.type === 'true_false') {{
                optionsHtml = '<div class="browse-options">';
                optionsHtml += '<div class="browse-option ' + (q.answer ? 'correct' : '') + '">正确</div>';
                optionsHtml += '<div class="browse-option ' + (!q.answer ? 'correct' : '') + '">错误</div>';
                optionsHtml += '</div>';
            }}
            
            let answerText = '';
            if (q.type === 'true_false') {{
                answerText = q.answer ? '正确' : '错误';
            }} else {{
                answerText = q.answer;
            }}
            
            const qId = q.uid || q.id;
            const extraButtons = (specialListType === 'wrong') ? 
                '<button onclick="removeFromWrongQuestions(' + qId + '); renderSpecialList();" style="padding: 8px 20px; background: #ff6b6b; color: white; border: none; border-radius: 8px; cursor: pointer;">从错题本移除</button>' :
                '<button onclick="toggleStar(' + qId + '); renderSpecialList();" style="padding: 8px 20px; background: #f9ca24; color: white; border: none; border-radius: 8px; cursor: pointer;">取消重点</button>';
            
            card.innerHTML = '<div class="browse-header">' +
                '<div class="browse-question-number">第 ' + (index + 1) + ' 题（第' + q.set + '套 原编号' + q.id + '）</div>' +
                '<div class="browse-question-badges">' +
                '<span class="browse-badge" style="background: ' + typeColors[q.type] + ';">' + typeNames[q.type] + '</span>' +
                '</div>' +
                '</div>' +
                '<div class="browse-question-text">' + q.question + '</div>' +
                optionsHtml +
                '<div class="browse-answer-box">' +
                '<div class="browse-answer-label">正确答案</div>' +
                '<div class="browse-answer-text">' + answerText + '</div>' +
                '</div>' +
                '<div style="margin-top: 15px;">' + extraButtons + '</div>';
            
            listEl.appendChild(card);
        }});
    }}
'''

# 6. 找到原始 HTML 中 script 标签的位置，替换它
script_start = html.find('<script>')
script_end = html.find('</script>', script_start)
new_html = html[:script_start + 8] + static_js + html[script_end:]

# 7. 保存到 index-github.html
with open('index-github.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('成功生成 index-github.html！共', len(questions), '道题！')

# 也同步更新到 index.html
import shutil
shutil.copy('index-github.html', 'index.html')
print('成功更新 index.html！')
