
import json

# 读取题目数据
with open(r'c:\Users\86183\Desktop\111\111\data\questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 把数据转成 JS 字符串
questions_js = json.dumps(questions, ensure_ascii=False)

# 读取完整的 index.html
with open(r'c:\Users\86183\Desktop\111\111\index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. 将所有 API 调用部分替换为直接使用本地数据
# 查找并替换获取题目的逻辑
# 原始代码有 API 调用，我们需要用嵌入式数据替换

# 首先，在 script 开头添加嵌入式题目数据
# 找到 window.onload 后面的部分，在那里添加数据

# 替换的关键部分：
# - 将 const API_BASE = '/api'; 删除
# - 将所有 API 调用的函数替换为直接使用嵌入式数据
# - 添加 let allQuestionsData = QUESTIONS_DATA;

# 进行替换
# 首先，替换 API_BASE 定义
html_content = html_content.replace(
    '        const API_BASE = \'/api\';',
    '        // ========== 嵌入式题目数据 ==========\n        const allQuestionsData = QUESTIONS_DATA;'
)

# 替换 QUESTIONS_DATA 标记
html_content = html_content.replace('QUESTIONS_DATA', questions_js)

# 现在，需要替换所有从 API 获取数据的函数，改成直接使用 allQuestionsData
# 查找并修改 startQuiz, startBrowse, startImmersive 等函数

# 简单的方法：查找所有 fetch 调用并替换，不过我们需要重写关键函数

# 让我们手动修改关键的初始化代码
# 找到 window.onload，在那里直接加载数据
# 查找 window.onload 函数，修改它让它直接初始化数据

original_onload = '''        window.onload = function() {
            // 确保只显示菜单，隐藏所有其他容器
            document.getElementById('menu').style.display = 'block';
            document.getElementById('quiz').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('browse').style.display = 'none';
            document.getElementById('immersive').style.display = 'none';
            document.getElementById('im-results').style.display = 'none';
            document.getElementById('recite').style.display = 'none';
            document.getElementById('special-list').style.display = 'none';
        };'''

new_onload = '''        window.onload = function() {
            // 确保只显示菜单，隐藏所有其他容器
            document.getElementById('menu').style.display = 'block';
            document.getElementById('quiz').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('browse').style.display = 'none';
            document.getElementById('immersive').style.display = 'none';
            document.getElementById('im-results').style.display = 'none';
            document.getElementById('recite').style.display = 'none';
            document.getElementById('special-list').style.display = 'none';
            
            // 初始化题目数据
            console.log('已加载 ' + allQuestionsData.length + ' 道题目');
        };'''

html_content = html_content.replace(original_onload, new_onload)

# 现在，我们需要重写所有使用 API 的函数
# 比如 startQuiz, startBrowse 等，让它们直接使用 allQuestionsData

# 查找并替换 startQuiz 函数
# 查找原始的 startQuiz（带 API 调用的版本），替换为使用本地数据

# 查找原始的 startQuiz 函数（简化匹配）
# 让我们用一个更简单的方案：搜索所有 function startQuiz(...) 并替换

# 我们需要重写关键函数，让它们直接使用 allQuestionsData
# 最简单的方法是直接写完整的函数替换

# 关键：我们需要替换所有的 API 调用为直接使用本地数据
# 让我们创建一个完整的替换脚本

# 首先，找到原始的 startQuiz 函数（从 index.html 中）

# 让我们写一个完整的 JavaScript 部分替换方案
# 我们需要替换的核心函数：
# - startQuiz
# - startBrowse
# - startImmersive
# - showQuestion
# - filterBrowseQuestions
# 等等

# 这里我用一个简单的方案：在原代码基础上，直接将所有从 API 获取数据的部分
# 替换为直接使用 allQuestionsData

# 查找函数定义，逐个替换

# 原始代码中有类似这样的：
# fetch('/api/questions?set=' + currentSet + '&type=' + quizType)
# 我们需要替换为直接从 allQuestionsData 过滤

# 为了简化，我们直接替换关键的函数
# 让我们直接用一个完整的替换，把所有需要修改的函数都改成使用本地数据

# 让我们写一个完整的替换脚本，重写关键函数

# 这部分比较复杂，我们用一个更直接的方案：
# 直接在 HTML 中添加完整的静态版本函数

# 我先保存一份原始 HTML 备份，然后进行完整替换

# 我们的核心思路：
# 1. 保留所有 HTML 结构和样式
# 2. 在 script 开头添加嵌入式题目数据
# 3. 重写所有与 API 相关的函数，让它们直接使用本地数据

# 为了简化，让我们创建一个完整的替换

# 让我先读取一些关键的函数代码，然后进行替换

# 这里我直接写一个完整的方案

# 首先，找到 script 标签的开始位置
# 然后，在其中添加我们的函数替换

# 我们主要需要修改的函数：

# 1. startQuiz - 从 API 改为本地过滤
# 2. startBrowse - 从 API 改为本地过滤
# 3. startImmersive - 从 API 改为本地过滤
# 4. 确保所有函数都直接使用 allQuestionsData

# 让我们创建一个完整的静态版本函数代码

static_functions = '''
        // ========== 纯静态版本函数 ==========
        
        function startQuiz(quizType) {
            currentQuizType = quizType;
            
            // 根据当前选择的套题和类型过滤题目
            let filtered = allQuestionsData;
            
            if (currentSet !== 'all') {
                filtered = filtered.filter(q => q.set === parseInt(currentSet));
            }
            
            if (quizType !== 'all' && quizType !== 'random') {
                filtered = filtered.filter(q => q.type === quizType);
            }
            
            if (quizType === 'random') {
                // 随机取 10 题
                filtered = [...filtered];
                for (let i = filtered.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
                }
                filtered = filtered.slice(0, 10);
            }
            
            questions = filtered;
            currentIndex = 0;
            userAnswers = {};
            answerShown = false;
            
            // 显示答题界面
            document.getElementById('menu').style.display = 'none';
            document.getElementById('quiz').style.display = 'block';
            
            showQuestion();
        }
        
        function startBrowse() {
            document.getElementById('menu').style.display = 'none';
            document.getElementById('browse').style.display = 'block';
            filterBrowseQuestions();
        }
        
        function filterBrowseQuestions() {
            const setFilter = document.getElementById('browse-set-filter').value;
            const typeFilter = document.getElementById('browse-type-filter').value;
            
            let filtered = allQuestionsData;
            
            if (setFilter !== 'all') {
                filtered = filtered.filter(q => q.set === parseInt(setFilter));
            }
            
            if (typeFilter !== 'all') {
                filtered = filtered.filter(q => q.type === typeFilter);
            }
            
            const listContainer = document.getElementById('questions-list');
            let html = '';
            
            filtered.forEach((q, idx) => {
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
                html += '<div class="browse-question-header">';
                html += '<div class="browse-question-number">第 ' + q.id + ' 题</div>';
                html += '<div class="browse-question-badges">';
                html += '<span class="browse-badge" style="background: #667eea;">' + setName + '</span>';
                html += '<span class="browse-badge" style="background: #f5576c;">' + typeName + '</span>';
                html += '</div>';
                html += '</div>';
                html += '<div class="browse-question-text">' + q.question + '</div>';
                
                if (q.options && q.options.length > 0) {
                    html += '<div class="browse-options">';
                    const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                    q.options.forEach((opt, optIdx) => {
                        const isCorrect = (q.type === 'single_choice' || q.type === 'multiple_choice') 
                            && labels[optIdx] === q.answer;
                        html += '<div class="browse-option' + (isCorrect ? ' correct' : '') + '">' + labels[optIdx] + '. ' + opt + '</div>';
                    });
                    html += '</div>';
                }
                
                let answerDisplay = '';
                if (q.type === 'true_false') {
                    answerDisplay = q.answer ? '正确' : '错误';
                } else {
                    answerDisplay = q.answer;
                }
                
                html += '<div class="browse-answer-box">';
                html += '<div class="browse-answer-label">正确答案</div>';
                html += '<div class="browse-answer-text">' + answerDisplay + '</div>';
                html += '</div>';
                html += '</div>';
            });
            
            listContainer.innerHTML = html;
        }
        
        function startImmersive(setNum) {
            imCurrentSet = setNum;
            imQuestions = allQuestionsData.filter(q => q.set === parseInt(setNum));
            imCurrentIndex = 0;
            imUserAnswers = {};
            
            document.getElementById('menu').style.display = 'none';
            document.getElementById('immersive').style.display = 'block';
            
            imShowQuestion();
            imRenderGrid();
        }
        
        function imShowQuestion() {
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
            
            const optionsContainer = document.getElementById('im-options');
            let optionsHtml = '';
            
            if (q.type === 'single_choice' || q.type === 'multiple_choice') {
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, idx) => {
                    const isSelected = imUserAnswers[q.id] === labels[idx];
                    optionsHtml += '<div class="option' + (isSelected ? ' selected' : '') + '" onclick="imSelectOption(\'' + q.id + '\', \'' + labels[idx] + '\', this)">' + labels[idx] + '. ' + opt + '</div>';
                });
            } else if (q.type === 'true_false') {
                optionsHtml += '<div class="option' + (imUserAnswers[q.id] === true ? ' selected' : '') + '" onclick="imSelectOption(\'' + q.id + '\', true, this)">A. 正确</div>';
                optionsHtml += '<div class="option' + (imUserAnswers[q.id] === false ? ' selected' : '') + '" onclick="imSelectOption(\'' + q.id + '\', false, this)">B. 错误</div>';
            } else {
                const savedValue = imUserAnswers[q.id] || '';
                optionsHtml += '<input type="text" class="fill-input" id="im-fill-' + q.id + '" placeholder="请输入答案" value="' + savedValue + '" oninput="imUserAnswers[\'' + q.id + '\'] = this.value">';
            }
            
            optionsContainer.innerHTML = optionsHtml;
        }
        
        function imSelectOption(qId, value, element) {
            imUserAnswers[qId] = value;
            
            const siblings = element.parentElement.children;
            for (let sibling of siblings) {
                sibling.classList.remove('selected');
            }
            element.classList.add('selected');
            
            imRenderGrid();
        }
        
        function imRenderGrid() {
            const grid = document.getElementById('im-question-grid');
            let html = '';
            
            imQuestions.forEach((q, idx) => {
                const isAnswered = imUserAnswers[q.id] !== undefined;
                const isCurrent = idx === imCurrentIndex;
                html += '<div class="question-dot' + (isAnswered ? ' answered' : '') + (isCurrent ? ' current' : '') + '" onclick="imGoToQuestion(' + idx + ')">' + (idx + 1) + '</div>';
            });
            
            grid.innerHTML = html;
        }
        
        function imGoToQuestion(idx) {
            imCurrentIndex = idx;
            imShowQuestion();
            imRenderGrid();
        }
        
        function imPrevQuestion() {
            if (imCurrentIndex > 0) {
                imCurrentIndex--;
                imShowQuestion();
                imRenderGrid();
            }
        }
        
        function imNextQuestion() {
            if (imCurrentIndex < imQuestions.length - 1) {
                imCurrentIndex++;
                imShowQuestion();
                imRenderGrid();
            }
        }
        
        function imSubmitQuiz() {
            let correct = 0;
            
            imQuestions.forEach(q => {
                const userAns = imUserAnswers[q.id];
                let isCorrect = false;
                
                if (q.type === 'true_false') {
                    isCorrect = (userAns === q.answer);
                } else if (q.type === 'fill_blank') {
                    isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                } else {
                    isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                }
                
                if (isCorrect) correct++;
            });
            
            const total = imQuestions.length;
            document.getElementById('im-score-display').textContent = correct + '/' + total;
            const percentage = Math.round((correct / total) * 100);
            let text = '';
            if (percentage >= 90) text = '🎉 太棒了！';
            else if (percentage >= 70) text = '👍 不错！继续加油！';
            else if (percentage >= 60) text = '💪 及格了，继续努力！';
            else text = '📚 还需要多练习哦！';
            document.getElementById('im-score-text').textContent = text;
            
            let detailsHtml = '';
            imQuestions.forEach(q => {
                const userAns = imUserAnswers[q.id];
                let isCorrect = false;
                let answerDisplay = '';
                let userAnswerDisplay = '';
                
                if (q.type === 'true_false') {
                    isCorrect = (userAns === q.answer);
                    answerDisplay = q.answer ? '正确' : '错误';
                    userAnswerDisplay = userAns ? '正确' : '错误';
                } else if (q.type === 'fill_blank') {
                    isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                    answerDisplay = q.answer;
                    userAnswerDisplay = userAns || '未作答';
                } else {
                    isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                    answerDisplay = q.answer;
                    userAnswerDisplay = userAns || '未作答';
                }
                
                detailsHtml += '<div class="result-item ' + (isCorrect ? 'result-correct' : 'result-wrong') + '">';
                detailsHtml += '<div style="font-weight: bold; margin-bottom: 8px;">第 ' + q.id + ' 题：' + q.question + '</div>';
                detailsHtml += '<div>你的答案：' + userAnswerDisplay + '</div>';
                detailsHtml += '<div>正确答案：' + answerDisplay + '</div>';
                detailsHtml += '</div>';
            });
            document.getElementById('im-result-details').innerHTML = detailsHtml;
            
            document.getElementById('immersive').style.display = 'none';
            document.getElementById('im-results').style.display = 'block';
        }
        
        function imRestartQuiz() {
            startImmersive(imCurrentSet);
        }
        
        function showQuestion() {
            const q = questions[currentIndex];
            
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
            
            document.getElementById('q-number').textContent = '第 ' + (currentIndex + 1) + ' 题 / 共 ' + questions.length + ' 题';
            document.getElementById('q-set').textContent = setName;
            document.getElementById('q-type').textContent = typeName;
            document.getElementById('q-text').textContent = q.question;
            
            const optionsContainer = document.getElementById('options');
            let optionsHtml = '';
            
            if (q.type === 'single_choice' || q.type === 'multiple_choice') {
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, idx) => {
                    const isSelected = userAnswers[q.id] === labels[idx];
                    optionsHtml += '<div class="option' + (isSelected ? ' selected' : '') + '" onclick="selectOption(\'' + q.id + '\', \'' + labels[idx] + '\', this)">' + labels[idx] + '. ' + opt + '</div>';
                });
            } else if (q.type === 'true_false') {
                optionsHtml += '<div class="option' + (userAnswers[q.id] === true ? ' selected' : '') + '" onclick="selectOption(\'' + q.id + '\', true, this)">A. 正确</div>';
                optionsHtml += '<div class="option' + (userAnswers[q.id] === false ? ' selected' : '') + '" onclick="selectOption(\'' + q.id + '\', false, this)">B. 错误</div>';
            } else {
                const savedValue = userAnswers[q.id] || '';
                optionsHtml += '<input type="text" class="fill-input" id="fill-' + q.id + '" placeholder="请输入答案" value="' + savedValue + '" oninput="userAnswers[\'' + q.id + '\'] = this.value">';
            }
            
            optionsContainer.innerHTML = optionsHtml;
            
            // 重置答案显示
            answerShown = false;
            document.getElementById('answer-section').classList.remove('show');
            document.getElementById('show-answer-btn').textContent = '显示答案';
            
            // 更新导航按钮
            document.getElementById('btn-prev').style.display = currentIndex > 0 ? 'block' : 'none';
            if (currentIndex < questions.length - 1) {
                document.getElementById('btn-next').style.display = 'block';
                document.getElementById('btn-submit').classList.add('hidden');
            } else {
                document.getElementById('btn-next').style.display = 'none';
                document.getElementById('btn-submit').classList.remove('hidden');
            }
        }
        
        function selectOption(qId, value, element) {
            userAnswers[qId] = value;
            const q = questions.find(x => String(x.id) === String(qId));
            
            const siblings = element.parentElement.children;
            for (let sibling of siblings) {
                sibling.classList.remove('selected', 'correct', 'wrong');
            }
            element.classList.add('selected');
            
            let isCorrect = false;
            if (q.type === 'true_false') {
                isCorrect = (value === q.answer);
            } else {
                isCorrect = String(value).toUpperCase() === String(q.answer).toUpperCase();
            }
            
            if (isCorrect) {
                element.classList.remove('selected');
                element.classList.add('correct');
                removeFromWrongQuestions(q.uid || q.id);
            } else {
                element.classList.remove('selected');
                element.classList.add('wrong');
                addToWrongQuestions(q.uid || q.id);
                showCorrectAnswer(q, element.parentElement);
            }
        }
        
        function showCorrectAnswer(q, container) {
            let answerText = '';
            if (q.type === 'true_false') {
                answerText = q.answer ? '正确' : '错误';
            } else {
                answerText = q.answer;
            }
            
            const answerDiv = document.createElement('div');
            answerDiv.className = 'answer-section';
            answerDiv.style.display = 'block';
            answerDiv.style.marginTop = '15px';
            answerDiv.innerHTML = '<div class="answer-title">正确答案</div><div class="answer-content">' + answerText + '</div>';
            container.appendChild(answerDiv);
        }
        
        function toggleAnswer() {
            const q = questions[currentIndex];
            const answerSection = document.getElementById('answer-section');
            const showAnswerBtn = document.getElementById('show-answer-btn');
            
            if (answerShown) {
                answerSection.classList.remove('show');
                showAnswerBtn.textContent = '显示答案';
                answerShown = false;
            } else {
                let answerText = '';
                
                if (q.type === 'true_false') {
                    answerText = q.answer ? '正确' : '错误';
                } else if (q.type === 'fill_blank') {
                    answerText = q.answer;
                } else {
                    answerText = q.answer;
                }
                
                document.getElementById('answer-content').textContent = answerText;
                answerSection.classList.add('show');
                showAnswerBtn.textContent = '隐藏答案';
                answerShown = true;
            }
        }
        
        function prevQuestion() {
            if (currentIndex > 0) {
                currentIndex--;
                showQuestion();
            }
        }
        
        function nextQuestion() {
            if (currentIndex < questions.length - 1) {
                currentIndex++;
                showQuestion();
            }
        }
        
        function submitQuiz() {
            let correct = 0;
            
            questions.forEach(q => {
                const userAns = userAnswers[q.id];
                let isCorrect = false;
                
                if (q.type === 'true_false') {
                    isCorrect = (userAns === q.answer);
                } else if (q.type === 'fill_blank') {
                    isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                } else {
                    isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                }
                
                if (isCorrect) correct++;
            });
            
            const total = questions.length;
            document.getElementById('score-display').textContent = correct + '/' + total;
            const percentage = Math.round((correct / total) * 100);
            let text = '';
            if (percentage >= 90) text = '🎉 太棒了！';
            else if (percentage >= 70) text = '👍 不错！继续加油！';
            else if (percentage >= 60) text = '💪 及格了，继续努力！';
            else text = '📚 还需要多练习哦！';
            document.getElementById('score-text').textContent = text;
            
            let detailsHtml = '';
            questions.forEach(q => {
                const userAns = userAnswers[q.id];
                let isCorrect = false;
                let answerDisplay = '';
                let userAnswerDisplay = '';
                
                if (q.type === 'true_false') {
                    isCorrect = (userAns === q.answer);
                    answerDisplay = q.answer ? '正确' : '错误';
                    userAnswerDisplay = userAns ? '正确' : '错误';
                } else if (q.type === 'fill_blank') {
                    isCorrect = String(userAns || '').trim() === String(q.answer || '').trim();
                    answerDisplay = q.answer;
                    userAnswerDisplay = userAns || '未作答';
                } else {
                    isCorrect = String(userAns || '').toUpperCase() === String(q.answer || '').toUpperCase();
                    answerDisplay = q.answer;
                    userAnswerDisplay = userAns || '未作答';
                }
                
                detailsHtml += '<div class="result-item ' + (isCorrect ? 'result-correct' : 'result-wrong') + '">';
                detailsHtml += '<div style="font-weight: bold; margin-bottom: 8px;">第 ' + q.id + ' 题：' + q.question + '</div>';
                detailsHtml += '<div>你的答案：' + userAnswerDisplay + '</div>';
                detailsHtml += '<div>正确答案：' + answerDisplay + '</div>';
                detailsHtml += '</div>';
            });
            document.getElementById('result-details').innerHTML = detailsHtml;
            
            document.getElementById('quiz').style.display = 'none';
            document.getElementById('results').style.display = 'block';
        }
        
        function restartQuiz() {
            startQuiz(currentQuizType);
        }
        
        function startReciteMode() {
            const setFilter = document.getElementById('recite-set-filter').value;
            
            if (setFilter === 'all') {
                reciteQuestions = [...allQuestionsData];
            } else {
                reciteQuestions = allQuestionsData.filter(q => q.set === parseInt(setFilter));
            }
            
            // 打乱顺序
            for (let i = reciteQuestions.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [reciteQuestions[i], reciteQuestions[j]] = [reciteQuestions[j], reciteQuestions[i]];
            }
            
            reciteIndex = 0;
            reciteAnswerShown = false;
            
            document.getElementById('menu').style.display = 'none';
            document.getElementById('recite').style.display = 'block';
            
            showReciteQuestion();
        }
        
        function showReciteQuestion() {
            const q = reciteQuestions[reciteIndex];
            
            document.getElementById('recite-number').textContent = '第 ' + (reciteIndex + 1) + ' 题 / 共 ' + reciteQuestions.length + ' 题';
            document.getElementById('recite-progress').textContent = (reciteIndex + 1) + '/' + reciteQuestions.length;
            
            // 更新收藏按钮
            if (isQuestionStarred(q.uid || q.id)) {
                document.getElementById('recite-star-btn').textContent = '⭐';
            } else {
                document.getElementById('recite-star-btn').textContent = '☆';
            }
            
            document.getElementById('recite-question').textContent = q.question;
            
            let optionsHtml = '';
            if (q.options && q.options.length > 0) {
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, idx) => {
                    optionsHtml += '<div style="padding: 10px; margin: 5px 0; background: #f8f9ff; border-radius: 8px;">' + labels[idx] + '. ' + opt + '</div>';
                });
            }
            document.getElementById('recite-options').innerHTML = optionsHtml;
            
            // 显示答案
            let answerDisplay = '';
            if (q.type === 'true_false') {
                answerDisplay = q.answer ? '正确' : '错误';
            } else {
                answerDisplay = q.answer;
            }
            document.getElementById('recite-answer-content').textContent = answerDisplay;
            
            // 隐藏答案
            document.getElementById('recite-answer').style.display = 'none';
            document.getElementById('recite-toggle-btn').textContent = '显示答案';
            reciteAnswerShown = false;
        }
        
        function toggleReciteAnswer() {
            const answerDiv = document.getElementById('recite-answer');
            const toggleBtn = document.getElementById('recite-toggle-btn');
            
            if (reciteAnswerShown) {
                answerDiv.style.display = 'none';
                toggleBtn.textContent = '显示答案';
                reciteAnswerShown = false;
            } else {
                answerDiv.style.display = 'block';
                toggleBtn.textContent = '隐藏答案';
                reciteAnswerShown = true;
            }
        }
        
        function prevRecite() {
            if (reciteIndex > 0) {
                reciteIndex--;
                showReciteQuestion();
            }
        }
        
        function nextRecite() {
            if (reciteIndex < reciteQuestions.length - 1) {
                reciteIndex++;
                showReciteQuestion();
            }
        }
        
        function showWrongQuestions() {
            specialListType = 'wrong';
            document.getElementById('special-title').textContent = '❌ 错题本';
            
            const wrongList = allQuestionsData.filter(q => wrongQuestions.includes(q.uid || q.id));
            renderSpecialList(wrongList);
            
            document.getElementById('menu').style.display = 'none';
            document.getElementById('special-list').style.display = 'block';
        }
        
        function showStarredQuestions() {
            specialListType = 'starred';
            document.getElementById('special-title').textContent = '⭐ 重点题';
            
            const starredList = allQuestionsData.filter(q => starredQuestions.includes(q.uid || q.id));
            renderSpecialList(starredList);
            
            document.getElementById('menu').style.display = 'none';
            document.getElementById('special-list').style.display = 'block';
        }
        
        function renderSpecialList(questionsList) {
            const container = document.getElementById('special-list-content');
            
            if (questionsList.length === 0) {
                container.innerHTML = '<p style="text-align: center; color: #999; padding: 40px;">暂无题目</p>';
                return;
            }
            
            let html = '';
            questionsList.forEach(q => {
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
                if (q.type === 'true_false') {
                    answerDisplay = q.answer ? '正确' : '错误';
                } else {
                    answerDisplay = q.answer;
                }
                
                html += '<div class="browse-question-card">';
                html += '<div class="browse-question-header">';
                html += '<div class="browse-question-number">第 ' + q.id + ' 题</div>';
                html += '<div class="browse-question-badges">';
                html += '<span class="browse-badge" style="background: #667eea;">' + setName + '</span>';
                html += '<span class="browse-badge" style="background: #f5576c;">' + typeName + '</span>';
                html += '</div>';
                html += '</div>';
                html += '<div class="browse-question-text">' + q.question + '</div>';
                
                if (q.options && q.options.length > 0) {
                    html += '<div class="browse-options">';
                    const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                    q.options.forEach((opt, idx) => {
                        html += '<div class="browse-option">' + labels[idx] + '. ' + opt + '</div>';
                    });
                    html += '</div>';
                }
                
                html += '<div class="browse-answer-box">';
                html += '<div class="browse-answer-label">正确答案</div>';
                html += '<div class="browse-answer-text">' + answerDisplay + '</div>';
                html += '</div>';
                
                // 添加移除按钮
                html += '<div style="margin-top: 15px;">';
                if (specialListType === 'wrong') {
                    html += '<button onclick="removeFromWrongQuestions(' + (q.uid || q.id) + '); renderSpecialList(allQuestionsData.filter(x => wrongQuestions.includes(x.uid || x.id)));" style="padding: 8px 20px; background: #ff6b6b; color: white; border: none; border-radius: 8px; cursor: pointer;">从错题本移除</button>';
                } else {
                    html += '<button onclick="toggleStar(' + (q.uid || q.id) + '); renderSpecialList(allQuestionsData.filter(x => starredQuestions.includes(x.uid || x.id)));" style="padding: 8px 20px; background: #f9ca24; color: white; border: none; border-radius: 8px; cursor: pointer;">取消重点</button>';
                }
                html += '</div>';
                
                html += '</div>';
            });
            
            container.innerHTML = html;
        }
        
        function backToMenu() {
            document.getElementById('menu').style.display = 'block';
            document.getElementById('quiz').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('browse').style.display = 'none';
            document.getElementById('immersive').style.display = 'none';
            document.getElementById('im-results').style.display = 'none';
            document.getElementById('recite').style.display = 'none';
            document.getElementById('special-list').style.display = 'none';
        }
'''

# 现在，我们需要找到原始 HTML 中的 script 部分，替换所有这些函数
# 为了简单，我们在嵌入数据后，直接添加这些静态版本函数
# 同时保留原有的变量定义和辅助函数

# 我们用一个特殊的标记来插入这些函数
# 找到 script 标签，在变量定义之后，原函数之前插入

# 让我们直接在替换 API_BASE 的地方后面，添加我们的静态函数
# 同时，我们需要确保删除或替换原有的 API 相关函数

# 这里，我采取一个更简单的方案：
# 1. 先替换 API_BASE 为嵌入式数据
# 2. 然后找到原始的 script 结束位置，在之前添加完整的静态函数
# 3. 确保我们的静态函数会覆盖原有的同名函数

# 查找 script 标签结束位置 </script>
# 在那之前添加我们的静态函数

script_end = '</script>'

# 先把我们的静态函数插在 script 结束之前
html_content = html_content.replace(script_end, static_functions + '\n' + script_end)

# 现在，保存为 GitHub Pages 使用的 index.html
output_path = r'c:\Users\86183\Desktop\111\111\index-github.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'✅ GitHub Pages 静态版本已生成：{output_path}')
print(f'   包含 {len(questions)} 道题目')
