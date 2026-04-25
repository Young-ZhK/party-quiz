
import json

# 1. 读取题目数据
with open('data/questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 2. 把题目数据转为 JS 字符串
questions_js = json.dumps(questions, ensure_ascii=False)

# 3. 完整的静态 JS 代码
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
        console.log('✅ 页面加载完成！共 ' + allQuestionsData.length + ' 道题');
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
        const qid = q.uid || q.id;
        const wasStarred = toggleStar(qid);
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
    
    // ========== 沉浸式做题 ==========
    let imQuestions = [];
    let imCurrentIndex = 0;
    let imUserAnswers = {{}};
    let imCurrentSet = '1';
    
    function startImmersive(setNum) {{
        imCurrentSet = setNum;
        imQuestions = allQuestionsData.filter(q => q.set === parseInt(setNum));
        imCurrentIndex = 0;
        imUserAnswers = {{}};
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('immersive').style.display = 'block';
        
        imShowQuestion();
        imRenderGrid();
    }}
    
    function imShowQuestion() {{
        const q = imQuestions[imCurrentIndex];
        
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
        
        document.getElementById('im-q-number').textContent = '第 ' + (imCurrentIndex + 1) + ' 题 / 共 ' + imQuestions.length + ' 题';
        document.getElementById('im-q-set').textContent = setName;
        document.getElementById('im-q-type').textContent = typeName;
        document.getElementById('im-q-text').textContent = q.question;
        
        const optionsEl = document.getElementById('im-options');
        optionsEl.innerHTML = '';
        
        if (q.type === 'single_choice' || q.type === 'multiple_choice') {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {{
                const div = document.createElement('div');
                div.className = 'option' + (imUserAnswers[q.id] === labels[i] ? ' selected' : '');
                div.textContent = labels[i] + '. ' + opt;
                div.onclick = function() {{ imSelectOption(q.id, labels[i], this); }};
                optionsEl.appendChild(div);
            }});
        }} else if (q.type === 'true_false') {{
            const divA = document.createElement('div');
            divA.className = 'option' + (imUserAnswers[q.id] === true ? ' selected' : '');
            divA.textContent = 'A. 正确';
            divA.onclick = function() {{ imSelectOption(q.id, true, this); }};
            optionsEl.appendChild(divA);
            
            const divB = document.createElement('div');
            divB.className = 'option' + (imUserAnswers[q.id] === false ? ' selected' : '');
            divB.textContent = 'B. 错误';
            divB.onclick = function() {{ imSelectOption(q.id, false, this); }};
            optionsEl.appendChild(divB);
        }} else {{
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'fill-input';
            input.placeholder = '请输入答案...';
            input.value = imUserAnswers[q.id] || '';
            input.oninput = function(e) {{ imUserAnswers[q.id] = e.target.value; }};
            optionsEl.appendChild(input);
        }}
    }}
    
    function imSelectOption(qId, value, el) {{
        imUserAnswers[qId] = value;
        const siblings = el.parentElement.children;
        for (let sib of siblings) {{
            sib.classList.remove('selected');
        }}
        el.classList.add('selected');
        imRenderGrid();
    }}
    
    function imRenderGrid() {{
        const grid = document.getElementById('im-question-grid');
        let html = '';
        imQuestions.forEach((q, i) => {{
            const answered = imUserAnswers[q.id] !== undefined;
            const current = i === imCurrentIndex;
            html += '<div class="question-dot' + (answered ? ' answered' : '') + (current ? ' current' : '') + '" onclick="imGoToQuestion(' + i + ')">' + (i + 1) + '</div>';
        }});
        grid.innerHTML = html;
    }}
    
    function imGoToQuestion(idx) {{
        imCurrentIndex = idx;
        imShowQuestion();
        imRenderGrid();
    }}
    
    function imPrevQuestion() {{
        if (imCurrentIndex > 0) {{
            imCurrentIndex--;
            imShowQuestion();
            imRenderGrid();
        }}
    }}
    
    function imNextQuestion() {{
        if (imCurrentIndex < imQuestions.length - 1) {{
            imCurrentIndex++;
            imShowQuestion();
            imRenderGrid();
        }}
    }}
    
    function imSubmitQuiz() {{
        let correct = 0;
        imQuestions.forEach(q => {{
            const userAns = imUserAnswers[q.id];
            let isCorrect = false;
            if (q.type === 'true_false') {{
                isCorrect = (userAns === q.answer);
            }} else if (q.type === 'fill_blank') {{
                isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
            }} else {{
                isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
            }}
            if (isCorrect) correct++;
        }});
        
        document.getElementById('im-score-display').textContent = correct + '/' + imQuestions.length;
        const percent = Math.round((correct / imQuestions.length) * 100);
        let text = '';
        if (percent >= 90) text = '🎉 太棒了！';
        else if (percent >= 70) text = '👍 不错！继续加油！';
        else if (percent >= 60) text = '💪 及格了，继续努力！';
        else text = '📚 还需要多练习哦！';
        document.getElementById('im-score-text').textContent = text;
        
        let detailsHtml = '';
        imQuestions.forEach(q => {{
            const userAns = imUserAnswers[q.id];
            let isCorrect = false;
            let answerDisplay = '';
            let userAnswerDisplay = '';
            
            if (q.type === 'true_false') {{
                isCorrect = (userAns === q.answer);
                answerDisplay = q.answer ? '正确' : '错误';
                userAnswerDisplay = userAns ? '正确' : '错误';
            }} else if (q.type === 'fill_blank') {{
                isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                answerDisplay = q.answer;
                userAnswerDisplay = userAns || '未作答';
            }} else {{
                isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                answerDisplay = q.answer;
                userAnswerDisplay = userAns || '未作答';
            }}
            
            detailsHtml += '<div class="result-item ' + (isCorrect ? 'result-correct' : 'result-wrong') + '">';
            detailsHtml += '<div style="font-weight: bold; margin-bottom: 8px;">第 ' + q.id + ' 题：' + q.question + '</div>';
            detailsHtml += '<div>你的答案：' + userAnswerDisplay + '</div>';
            detailsHtml += '<div>正确答案：' + answerDisplay + '</div>';
            detailsHtml += '</div>';
        }});
        document.getElementById('im-result-details').innerHTML = detailsHtml;
        
        document.getElementById('immersive').style.display = 'none';
        document.getElementById('im-results').style.display = 'block';
    }}
    
    function imRestartQuiz() {{
        startImmersive(imCurrentSet);
    }}
    
    // ========== 普通答题模式 ==========
    function selectSet(set) {{
        currentSet = set;
        document.querySelectorAll('.set-btn').forEach(btn => btn.classList.remove('active'));
        const btnId = 'set-' + set;
        if (document.getElementById(btnId)) {{
            document.getElementById(btnId).classList.add('active');
        }}
    }}
    
    function startQuiz(type) {{
        currentQuizType = type;
        
        let filtered = allQuestionsData;
        if (currentSet !== 'all') {{
            filtered = filtered.filter(q => q.set === parseInt(currentSet));
        }}
        if (type !== 'all' && type !== 'random') {{
            filtered = filtered.filter(q => q.type === type);
        }}
        if (type === 'random') {{
            filtered = [...filtered];
            for (let i = filtered.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
            }}
            filtered = filtered.slice(0, 10);
        }}
        
        questions = filtered;
        currentIndex = 0;
        userAnswers = {{}};
        answerShown = false;
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'block';
        
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
        let setName = '';
        if (q.set === 1) setName = '第一套';
        else if (q.set === 2) setName = '第二套';
        else if (q.set === 3) setName = '第三套';
        else if (q.set === 4) setName = '第四套';
        else if (q.set === 5) setName = '第五套';
        else if (q.set === 6) setName = '第六套';
        else if (q.set === 7) setName = '第七套';
        else if (q.set === 8) setName = '第八套';
        setEl.textContent = setName;
        
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
            feedback.className = 'fill-feedback';
            feedback.style.display = 'none';
            optionsEl.appendChild(feedback);
        }} else if (q.type === 'true_false') {{
            ['正确', '错误'].forEach((text, idx) => {{
                const div = document.createElement('div');
                const val = idx === 0;
                let cls = 'option';
                if (userAnswers[qId] === val) {{
                    cls += ' selected';
                    let isCorrect = (val === q.answer);
                    if (isCorrect) cls += ' correct';
                    else cls += ' wrong';
                }}
                div.className = cls;
                div.textContent = (idx === 0 ? 'A. ' : 'B. ') + text;
                div.onclick = function() {{ selectOption(qId, val, this); }};
                optionsEl.appendChild(div);
            }});
        }} else {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, idx) => {{
                const div = document.createElement('div');
                let cls = 'option';
                if (userAnswers[qId] === labels[idx]) {{
                    cls += ' selected';
                    let isCorrect = labels[idx] === String(q.answer).toUpperCase();
                    if (isCorrect) cls += ' correct';
                    else cls += ' wrong';
                }}
                div.className = cls;
                div.textContent = labels[idx] + '. ' + opt;
                div.onclick = function() {{ selectOption(qId, labels[idx], this); }};
                optionsEl.appendChild(div);
            }});
        }}
        
        const prevBtn = document.getElementById('btn-prev');
        const nextBtn = document.getElementById('btn-next');
        const submitBtn = document.getElementById('btn-submit');
        
        prevBtn.style.display = currentIndex > 0 ? 'block' : 'none';
        
        if (currentIndex < questions.length - 1) {{
            nextBtn.style.display = 'block';
            submitBtn.classList.add('hidden');
        }} else {{
            nextBtn.style.display = 'none';
            submitBtn.classList.remove('hidden');
        }}
    }}
    
    function checkFillAnswer(qId, input, q, container) {{
        const userAns = input.value.trim();
        const correctAns = String(q.answer).trim();
        const feedback = document.getElementById('fill-feedback-' + qId);
        
        const isCorrect = userAns === correctAns;
        
        feedback.style.display = 'block';
        feedback.style.marginTop = '10px';
        feedback.style.padding = '15px';
        feedback.style.borderRadius = '10px';
        if (isCorrect) {{
            feedback.style.background = '#d4edda';
            feedback.style.color = '#155724';
            feedback.innerHTML = '✅ 回答正确！';
            input.style.borderColor = '#38ef7d';
            removeFromWrongQuestions(qId);
        }} else {{
            feedback.style.background = '#f8d7da';
            feedback.style.color = '#721c24';
            feedback.innerHTML = '❌ 回答错误！正确答案是：<strong>' + correctAns + '</strong>';
            input.style.borderColor = '#f45c43';
            addToWrongQuestions(qId);
        }}
    }}
    
    function selectOption(qId, value, el) {{
        userAnswers[qId] = value;
        const q = questions.find(x => (x.uid || x.id) === qId) || questions[currentIndex];
        
        const siblings = el.parentElement.children;
        for (let sib of siblings) {{
            sib.classList.remove('selected', 'correct', 'wrong');
        }}
        el.classList.add('selected');
        
        let isCorrect = false;
        if (q.type === 'true_false') {{
            isCorrect = (value === q.answer);
        }} else {{
            isCorrect = String(value).toUpperCase() === String(q.answer).toUpperCase();
        }}
        
        if (isCorrect) {{
            el.classList.remove('selected');
            el.classList.add('correct');
            removeFromWrongQuestions(qId);
        }} else {{
            el.classList.remove('selected');
            el.classList.add('wrong');
            addToWrongQuestions(qId);
        }}
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
        questions.forEach(q => {{
            const qid = q.uid || q.id;
            const userAns = userAnswers[qid];
            let isCorrect = false;
            if (q.type === 'true_false') {{
                isCorrect = (userAns === q.answer);
            }} else if (q.type === 'fill_blank') {{
                isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
            }} else {{
                isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
            }}
            if (isCorrect) correct++;
        }});
        
        document.getElementById('score-display').textContent = correct + '/' + questions.length;
        const percent = Math.round((correct / questions.length) * 100);
        let text = '';
        if (percent >= 90) text = '🎉 太棒了！';
        else if (percent >= 70) text = '👍 不错！继续加油！';
        else if (percent >= 60) text = '💪 及格了，继续努力！';
        else text = '📚 还需要多练习哦！';
        document.getElementById('score-text').textContent = text;
        
        let detailsHtml = '';
        questions.forEach(q => {{
            const qid = q.uid || q.id;
            const userAns = userAnswers[qid];
            let isCorrect = false;
            let answerDisplay = '';
            let userAnswerDisplay = '';
            
            if (q.type === 'true_false') {{
                isCorrect = (userAns === q.answer);
                answerDisplay = q.answer ? '正确' : '错误';
                userAnswerDisplay = userAns ? '正确' : '错误';
            }} else if (q.type === 'fill_blank') {{
                isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                answerDisplay = q.answer;
                userAnswerDisplay = userAns || '未作答';
            }} else {{
                isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                answerDisplay = q.answer;
                userAnswerDisplay = userAns || '未作答';
            }}
            
            detailsHtml += '<div class="result-item ' + (isCorrect ? 'result-correct' : 'result-wrong') + '">';
            detailsHtml += '<div style="font-weight: bold; margin-bottom: 8px;">第 ' + q.id + ' 题：' + q.question + '</div>';
            detailsHtml += '<div>你的答案：' + userAnswerDisplay + '</div>';
            detailsHtml += '<div>正确答案：' + answerDisplay + '</div>';
            detailsHtml += '</div>';
        }});
        document.getElementById('result-details').innerHTML = detailsHtml;
        
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'block';
    }}
    
    function restartQuiz() {{
        startQuiz(currentQuizType);
    }}
    
    // ========== 浏览题目 ==========
    function startBrowse() {{
        document.getElementById('menu').style.display = 'none';
        document.getElementById('browse').style.display = 'block';
        filterBrowseQuestions();
    }}
    
    function filterBrowseQuestions() {{
        const setVal = document.getElementById('browse-set-filter').value;
        const typeVal = document.getElementById('browse-type-filter').value;
        
        let filtered = allQuestionsData;
        if (setVal !== 'all') {{
            filtered = filtered.filter(q => q.set === parseInt(setVal));
        }}
        if (typeVal !== 'all') {{
            filtered = filtered.filter(q => q.type === typeVal);
        }}
        
        const listEl = document.getElementById('questions-list');
        let html = '';
        
        filtered.forEach(q => {{
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
            
            html += '<div class="browse-question-card">';
            html += '<div class="browse-header">';
            html += '<div class="browse-question-number">第 ' + q.id + ' 题</div>';
            html += '<div class="browse-question-badges">';
            html += '<span class="browse-badge" style="background: #667eea;">' + setName + '</span>';
            html += '<span class="browse-badge" style="background: #f5576c;">' + typeName + '</span>';
            html += '</div>';
            html += '</div>';
            html += '<div class="browse-question-text">' + q.question + '</div>';
            
            if (q.options && q.options.length > 0) {{
                html += '<div class="browse-options">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {{
                    const isCorrect = (q.type === 'single_choice' || q.type === 'multiple_choice') && labels[i] === q.answer;
                    html += '<div class="browse-option' + (isCorrect ? ' correct' : '') + '">' + labels[i] + '. ' + opt + '</div>';
                }});
                html += '</div>';
            }}
            
            let answerDisplay = '';
            if (q.type === 'true_false') {{
                answerDisplay = q.answer ? '正确' : '错误';
            }} else {{
                answerDisplay = q.answer;
            }}
            
            html += '<div class="browse-answer-box">';
            html += '<div class="browse-answer-label">正确答案</div>';
            html += '<div class="browse-answer-text">' + answerDisplay + '</div>';
            html += '</div>';
            html += '</div>';
        }});
        
        listEl.innerHTML = html;
    }}
    
    // ========== 背诵模式 ==========
    function startReciteMode() {{
        const setVal = document.getElementById('recite-set-filter').value;
        
        if (setVal === 'all') {{
            reciteQuestions = [...allQuestionsData];
        }} else {{
            reciteQuestions = allQuestionsData.filter(q => q.set === parseInt(setVal));
        }}
        
        for (let i = reciteQuestions.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [reciteQuestions[i], reciteQuestions[j]] = [reciteQuestions[j], reciteQuestions[i]];
        }}
        
        reciteIndex = 0;
        reciteAnswerShown = false;
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('recite').style.display = 'block';
        
        showReciteQuestion();
    }}
    
    function showReciteQuestion() {{
        const q = reciteQuestions[reciteIndex];
        document.getElementById('recite-number').textContent = '第 ' + (reciteIndex + 1) + ' 题';
        document.getElementById('recite-progress').textContent = (reciteIndex + 1) + '/' + reciteQuestions.length;
        
        const qid = q.uid || q.id;
        if (isQuestionStarred(qid)) {{
            document.getElementById('recite-star-btn').textContent = '⭐';
        }} else {{
            document.getElementById('recite-star-btn').textContent = '☆';
        }}
        
        document.getElementById('recite-question').textContent = q.question;
        
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {{
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {{
                optionsHtml += '<div style="padding: 10px; margin: 5px 0; background: #f8f9ff; border-radius: 8px;">' + labels[i] + '. ' + opt + '</div>';
            }});
        }}
        document.getElementById('recite-options').innerHTML = optionsHtml;
        
        let answerDisplay = '';
        if (q.type === 'true_false') {{
            answerDisplay = q.answer ? '正确' : '错误';
        }} else {{
            answerDisplay = q.answer;
        }}
        document.getElementById('recite-answer-content').textContent = answerDisplay;
        
        document.getElementById('recite-answer').style.display = 'none';
        document.getElementById('recite-toggle-btn').textContent = '显示答案';
        reciteAnswerShown = false;
    }}
    
    function toggleReciteAnswer() {{
        const answerDiv = document.getElementById('recite-answer');
        const toggleBtn = document.getElementById('recite-toggle-btn');
        if (reciteAnswerShown) {{
            answerDiv.style.display = 'none';
            toggleBtn.textContent = '显示答案';
            reciteAnswerShown = false;
        }} else {{
            answerDiv.style.display = 'block';
            toggleBtn.textContent = '隐藏答案';
            reciteAnswerShown = true;
        }}
    }}
    
    function prevRecite() {{
        if (reciteIndex > 0) {{
            reciteIndex--;
            showReciteQuestion();
        }}
    }}
    
    function nextRecite() {{
        if (reciteIndex < reciteQuestions.length - 1) {{
            reciteIndex++;
            showReciteQuestion();
        }}
    }}
    
    // ========== 错题本和重点题 ==========
    function showWrongQuestions() {{
        specialListType = 'wrong';
        document.getElementById('special-title').textContent = '❌ 错题本';
        
        const list = allQuestionsData.filter(q => wrongQuestions.includes(q.uid || q.id));
        renderSpecialList(list);
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
    }}
    
    function showStarredQuestions() {{
        specialListType = 'starred';
        document.getElementById('special-title').textContent = '⭐ 重点题';
        
        const list = allQuestionsData.filter(q => starredQuestions.includes(q.uid || q.id));
        renderSpecialList(list);
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
    }}
    
    function renderSpecialList(list) {{
        const container = document.getElementById('special-list-content');
        
        if (list.length === 0) {{
            container.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">暂无题目</p>';
            return;
        }}
        
        let html = '';
        list.forEach(q => {{
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
            
            html += '<div class="browse-question-card">';
            html += '<div class="browse-header">';
            html += '<div class="browse-question-number">第 ' + q.id + ' 题</div>';
            html += '<div class="browse-question-badges">';
            html += '<span class="browse-badge" style="background: #667eea;">' + setName + '</span>';
            html += '<span class="browse-badge" style="background: #f5576c;">' + typeName + '</span>';
            html += '</div>';
            html += '</div>';
            html += '<div class="browse-question-text">' + q.question + '</div>';
            
            if (q.options && q.options.length > 0) {{
                html += '<div class="browse-options">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {{
                    html += '<div class="browse-option">' + labels[i] + '. ' + opt + '</div>';
                }});
                html += '</div>';
            }}
            
            html += '<div class="browse-answer-box">';
            html += '<div class="browse-answer-label">正确答案</div>';
            html += '<div class="browse-answer-text">' + answerDisplay + '</div>';
            html += '</div>';
            
            const qid = q.uid || q.id;
            html += '<div style="margin-top: 15px;">';
            if (specialListType === 'wrong') {{
                html += '<button onclick="removeFromWrongQuestions(' + qid + '); renderSpecialList(allQuestionsData.filter(x => wrongQuestions.includes(x.uid || x.id)));" style="padding: 8px 20px; background: #ff6b6b; color: white; border: none; border-radius: 8px; cursor: pointer;">从错题本移除</button>';
            }} else {{
                html += '<button onclick="toggleStar(' + qid + '); renderSpecialList(allQuestionsData.filter(x => starredQuestions.includes(x.uid || x.id)));" style="padding: 8px 20px; background: #f9ca24; color: white; border: none; border-radius: 8px; cursor: pointer;">取消重点</button>';
            }}
            html += '</div>';
            html += '</div>';
        }});
        
        container.innerHTML = html;
    }}
    
    // ========== 返回菜单 ==========
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
'''

# 4. 读取原始 HTML，找到 script 标签位置
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找到 <script> 开始和结束位置
script_start = html.find('<script>')
script_end = html.find('</script>', script_start)

# 替换整个 script 部分
new_html = html[:script_start + 8] + static_js + html[script_end:]

# 5. 保存新文件
with open('index-github.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print('✅ 生成完成！文件：index-github.html，共', len(questions), '道题')
