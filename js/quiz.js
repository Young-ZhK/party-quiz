// 答题功能模块
import { allQuestionsData } from '../data/questions.js';
import { getItem, setItem, STORAGE_KEYS } from './storage.js';
import { QUESTION_TYPE_NAMES, QUESTION_TYPE_CLASSES } from './constants.js';

// 全局变量
window.questions = [];
window.currentIndex = 0;
window.userAnswers = {};
window.currentQuizType = 'all';
window.currentSet = 'all';
window.answerShown = false;

// 初始化数据
let wrongQuestions = getItem(STORAGE_KEYS.WRONG_QUESTIONS, []);
let starredQuestions = getItem(STORAGE_KEYS.STARRED_QUESTIONS, []);
let questionMastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {});
let studyPlan = getItem(STORAGE_KEYS.STUDY_PLAN, {});
let studyHistory = getItem(STORAGE_KEYS.STUDY_HISTORY, []);

// 保存数据
function saveData() {
    setItem(STORAGE_KEYS.WRONG_QUESTIONS, wrongQuestions);
    setItem(STORAGE_KEYS.STARRED_QUESTIONS, starredQuestions);
    setItem(STORAGE_KEYS.QUESTION_MASTERY, questionMastery);
    setItem(STORAGE_KEYS.STUDY_PLAN, studyPlan);
    setItem(STORAGE_KEYS.STUDY_HISTORY, studyHistory);
}

// 显示题目
export function displayQuestion() {
    const q = window.questions[window.currentIndex];
    
    window.answerShown = false;
    document.getElementById('answer-section').classList.remove('show');
    document.getElementById('show-answer-btn').textContent = '显示答案';
    
    // 智能复习模式下隐藏显示答案按钮
    if (window.currentQuizType === 'smart') {
        document.getElementById('show-answer-btn').style.display = 'none';
    } else {
        document.getElementById('show-answer-btn').style.display = 'block';
    }
    
    document.getElementById('q-number').textContent = `第 ${window.currentIndex + 1} 题 / 共 ${window.questions.length} 题`;
    
    const typeEl = document.getElementById('q-type');
    typeEl.textContent = QUESTION_TYPE_NAMES[q.type];
    typeEl.className = `question-type ${QUESTION_TYPE_CLASSES[q.type]}`;
    
    const setEl = document.getElementById('q-set');
    setEl.textContent = q.set ? `第${q.set}套` : '题目';
    
    document.getElementById('q-text').textContent = q.question;
    
    const optionsEl = document.getElementById('options');
    optionsEl.innerHTML = '';
    
    const qId = q.uid || q.id;
    
    if (q.type === 'fill_blank') {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'fill-input';
        input.placeholder = '请输入答案...';
        input.value = window.userAnswers[qId] || '';
        input.oninput = function(e) { window.userAnswers[qId] = e.target.value; };
        optionsEl.appendChild(input);
        
        // 智能复习模式下隐藏检查答案按钮
        if (window.currentQuizType !== 'smart') {
            const checkBtn = document.createElement('button');
            checkBtn.className = 'show-answer-btn';
            checkBtn.textContent = '检查答案';
            checkBtn.style.marginTop = '10px';
            checkBtn.onclick = function() {
                checkFillAnswer(qId, input, q, optionsEl);
            };
            optionsEl.appendChild(checkBtn);
        }
        
        const feedback = document.createElement('div');
        feedback.id = `fill-feedback-${qId}`;
        feedback.style.marginTop = '10px';
        feedback.style.padding = '10px';
        feedback.style.borderRadius = '8px';
        feedback.style.display = 'none';
        optionsEl.appendChild(feedback);
    } else if (q.type === 'true_false') {
        ['正确', '错误'].forEach((opt, i) => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = opt;
            const val = i === 0;
            if (window.userAnswers[qId] === val) {
                div.classList.add('selected');
                // 智能复习模式下不显示正确/错误反馈
                if (window.currentQuizType !== 'smart') {
                    let isCorrect = (val === q.answer);
                    if (isCorrect) {
                        div.classList.remove('selected');
                        div.classList.add('correct');
                        removeFromWrongQuestions(qId);
                    } else {
                        div.classList.remove('selected');
                        div.classList.add('wrong');
                        addToWrongQuestions(qId);
                    }
                }
            }
            div.onclick = function() { selectOption(qId, val, div); };
            optionsEl.appendChild(div);
        });
    } else {
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        q.options.forEach((opt, i) => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = `${labels[i]}. ${opt}`;
            
            if (q.type === 'multiple_choice') {
                if (Array.isArray(window.userAnswers[qId]) && window.userAnswers[qId].includes(labels[i])) {
                    div.classList.add('selected');
                }
            } else {
                if (window.userAnswers[qId] === labels[i]) {
                    div.classList.add('selected');
                    // 智能复习模式下不显示正确/错误反馈
                    if (window.currentQuizType !== 'smart') {
                        let isCorrect = (labels[i] === String(q.answer).toUpperCase());
                        if (isCorrect) {
                            div.classList.remove('selected');
                            div.classList.add('correct');
                            removeFromWrongQuestions(qId);
                        } else {
                            div.classList.remove('selected');
                            div.classList.add('wrong');
                            showCorrectAnswer(q, optionsEl);
                        }
                    }
                }
            }
            
            div.onclick = function() { selectOption(qId, labels[i], div, q.type); };
            optionsEl.appendChild(div);
        });
    }
    
    document.getElementById('btn-prev').style.display = window.currentIndex > 0 ? 'block' : 'none';
    
    if (window.currentIndex === window.questions.length - 1) {
        document.getElementById('btn-next').style.display = 'none';
        document.getElementById('btn-submit').style.display = 'block';
    } else {
        document.getElementById('btn-next').style.display = 'block';
        document.getElementById('btn-submit').style.display = 'none';
    }
}

// 选择选项
export function selectOption(qId, value, el, qType) {
    const q = window.questions.find(x => (x.uid || x.id) === qId) || window.questions[window.currentIndex];
    
    if (qType === 'multiple_choice' || q.type === 'multiple_choice') {
        if (!Array.isArray(window.userAnswers[qId])) {
            window.userAnswers[qId] = [];
        }
        const idx = window.userAnswers[qId].indexOf(value);
        if (idx === -1) {
            window.userAnswers[qId].push(value);
        } else {
            window.userAnswers[qId].splice(idx, 1);
        }
        
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        const siblings = el.parentElement.children;
        for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            sibling.classList.remove('selected', 'correct', 'wrong');
            if (Array.isArray(window.userAnswers[qId]) && window.userAnswers[qId].includes(labels[i])) {
                sibling.classList.add('selected');
            }
        }
        
        // 智能复习模式下不显示答案反馈
        if (window.currentQuizType !== 'smart') {
            const userAnswer = Array.isArray(window.userAnswers[qId]) ? window.userAnswers[qId].sort().join('') : '';
            const correctAnswer = String(q.answer).toUpperCase().split('').sort().join('');
            const isCorrect = userAnswer === correctAnswer;
            
            if (isCorrect) {
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (Array.isArray(window.userAnswers[qId]) && window.userAnswers[qId].includes(labels[i])) {
                        sibling.classList.remove('selected');
                        sibling.classList.add('correct');
                    }
                }
                removeFromWrongQuestions(qId);
            } else {
                showCorrectAnswer(q, el.parentElement);
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (Array.isArray(window.userAnswers[qId]) && window.userAnswers[qId].includes(labels[i])) {
                        sibling.classList.remove('selected');
                        if (String(q.answer).toUpperCase().includes(labels[i])) {
                            sibling.classList.add('correct');
                        } else {
                            sibling.classList.add('wrong');
                        }
                    }
                }
                addToWrongQuestions(qId);
            }
        }
    } else {
        window.userAnswers[qId] = value;
        
        const siblings = el.parentElement.children;
        for (let sibling of siblings) {
            sibling.classList.remove('selected', 'correct', 'wrong');
        }
        el.classList.add('selected');
        
        // 智能复习模式下不显示答案反馈
        if (window.currentQuizType !== 'smart') {
            let isCorrect = false;
            if (q.type === 'true_false') {
                isCorrect = (value === true && q.answer === true) || (value === false && q.answer === false);
            } else {
                isCorrect = value.toUpperCase() === String(q.answer).toUpperCase();
            }
            
            if (isCorrect) {
                el.classList.remove('selected');
                el.classList.add('correct');
                removeFromWrongQuestions(qId);
            } else {
                el.classList.remove('selected');
                el.classList.add('wrong');
                showCorrectAnswer(q, el.parentElement);
                addToWrongQuestions(qId);
            }
        }
    }
}

// 显示正确答案
function showCorrectAnswer(q, optionsContainer) {
    if (q.type === 'true_false') {
        const options = optionsContainer.children;
        const correctIndex = q.answer ? 0 : 1;
        if (options[correctIndex]) {
            options[correctIndex].classList.add('correct');
        }
    } else {
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        const answerStr = String(q.answer).toUpperCase();
        const options = optionsContainer.children;
        for (let i = 0; i < options.length; i++) {
            if (answerStr.includes(labels[i])) {
                options[i].classList.add('correct');
            }
        }
    }
}

// 检查填空题答案
function checkFillAnswer(qId, input, q, container) {
    const feedback = document.getElementById(`fill-feedback-${qId}`);
    const userAnswer = input.value.trim();
    const correctAnswer = String(q.answer || '').trim();
    
    const isCorrect = userAnswer === correctAnswer;
    
    feedback.style.display = 'block';
    if (isCorrect) {
        feedback.style.background = '#d4edda';
        feedback.style.color = '#155724';
        feedback.innerHTML = '✅ 回答正确！';
        input.style.borderColor = '#38ef7d';
        removeFromWrongQuestions(qId);
    } else {
        feedback.style.background = '#f8d7da';
        feedback.style.color = '#721c24';
        feedback.innerHTML = `❌ 回答错误！正确答案是：<strong>${correctAnswer}</strong>`;
        input.style.borderColor = '#f45c43';
        addToWrongQuestions(qId);
    }
}

// 上一题
export function prevQuestion() {
    if (window.currentIndex > 0) {
        window.currentIndex--;
        displayQuestion();
    }
}

// 下一题
export function nextQuestion() {
    if (window.currentIndex < window.questions.length - 1) {
        window.currentIndex++;
        displayQuestion();
    }
}

// 提交答案
export function submitQuiz() {
    let correct = 0;
    const results = [];
    window.questions.forEach((q, index) => {
        const qId = q.uid || q.id;
        let userAnswer = window.userAnswers[qId];
        let isCorrect = false;
        
        if (q.type === 'true_false') {
            isCorrect = (userAnswer === q.answer);
        } else if (q.type === 'multiple_choice') {
            const userAnswerStr = Array.isArray(userAnswer) ? userAnswer.sort().join('') : '';
            const correctAnswerStr = String(q.answer).toUpperCase().split('').sort().join('');
            isCorrect = (userAnswerStr === correctAnswerStr);
            userAnswer = Array.isArray(userAnswer) ? userAnswer.join('') : '未作答';
        } else if (q.type === 'fill_blank') {
            isCorrect = String(userAnswer || '').trim() === String(q.answer || '').trim();
        } else {
            isCorrect = String(userAnswer || '').toUpperCase() === String(q.answer || '').toUpperCase();
        }
        
        if (isCorrect) {
            correct++;
        } else {
            addToWrongQuestions(qId);
        }
        
        results.push({
            id: qId,
            correct: isCorrect,
            user_answer: userAnswer || '未作答',
            correct_answer: q.type === 'true_false' ? (q.answer ? '正确' : '错误') : q.answer,
            question: q.question,
            set: q.set
        });
    });
    
    showResults({
        score: correct,
        total: window.questions.length,
        results: results
    });
}

// 显示结果
function showResults(result) {
    document.getElementById('quiz').style.display = 'none';
    document.getElementById('results').style.display = 'block';
    
    document.getElementById('score-display').textContent = `${result.score}/${result.total}`;
    
    const percentage = Math.round((result.score / result.total) * 100);
    let text = '';
    if (percentage >= 90) text = '🎉 太棒了！成绩优秀！';
    else if (percentage >= 70) text = '👍 不错！继续努力！';
    else if (percentage >= 60) text = '💪 及格了，但还需要加强！';
    else text = '📚 需要多练习哦！';
    document.getElementById('score-text').textContent = text;
    
    const detailsEl = document.getElementById('result-details');
    detailsEl.innerHTML = '';
    
    result.results.forEach((res, index) => {
        const q = window.questions[index];
        let optionsHtml = '';
        let userAnswerWithOption = res.user_answer;
        let correctAnswerWithOption = res.correct_answer;
        
        if (q.type !== 'fill_blank' && q.type !== 'true_false' && q.options && q.options.length > 0) {
            optionsHtml = '<div style="font-size: 0.9em; margin-top: 8px; color: #666;">';
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {
                const label = labels[i] || String.fromCharCode(65 + i);
                optionsHtml += `<div style="margin: 4px 0;">${label}. ${opt}</div>`;
            });
            optionsHtml += '</div>';
        }
        
        detailsEl.innerHTML += `<div class="result-item ${res.correct ? 'result-correct' : 'result-wrong'}">` +
            `<strong>第 ${index + 1} 题（第${res.set}套）</strong>${res.question}` +
            optionsHtml +
            `<br><em>你的答案：${userAnswerWithOption} | 正确答案：${correctAnswerWithOption}</em>` +
            '</div>';
    });
    
    // 添加智能复习后的功能按钮
    const resultActionsEl = document.getElementById('result-actions');
    if (window.currentQuizType === 'smart') {
        const wrongCount = result.total - result.score;
        if (wrongCount > 0) {
            resultActionsEl.innerHTML = `
                <button class="menu-btn" onclick="reviewWrongQuestions()" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; margin-right: 10px;">
                    ❌ 仅查看错题
                </button>
                <button class="menu-btn" onclick="backToMenu()" style="background: #6c757d; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer;">
                    返回菜单
                </button>
            `;
        } else {
            resultActionsEl.innerHTML = `
                <button class="menu-btn" onclick="backToMenu()" style="background: #6c757d; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer;">
                    返回菜单
                </button>
            `;
        }
    } else {
        resultActionsEl.innerHTML = `
            <button class="menu-btn" onclick="restartQuiz()" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer; margin-right: 10px;">
                重新开始
            </button>
            <button class="menu-btn" onclick="backToMenu()" style="background: #6c757d; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer;">
                返回菜单
            </button>
        `;
    }
    
    // 添加学习记录
    addStudyRecord({
        correct: result.score,
        total: result.total,
        type: window.currentQuizType,
        set: window.currentSet
    });
}

// 增加错题
function addToWrongQuestions(qId) {
    if (!wrongQuestions.includes(qId)) {
        wrongQuestions.push(qId);
        saveData();
    }
}

// 移除错题
function removeFromWrongQuestions(qId) {
    const idx = wrongQuestions.indexOf(qId);
    if (idx !== -1) {
        wrongQuestions.splice(idx, 1);
        saveData();
    }
}

// 添加学习记录
function addStudyRecord(record) {
    studyHistory.unshift({
        ...record,
        timestamp: new Date().toISOString()
    });
    
    // 限制历史记录数量
    if (studyHistory.length > 100) {
        studyHistory = studyHistory.slice(0, 100);
    }
    
    saveData();
}

// 开始答题
export function startQuiz(type, set = 'all') {
    window.currentQuizType = type;
    window.currentSet = set;
    window.currentIndex = 0;
    window.userAnswers = {};
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    
    // 筛选题目
    let filtered = [...allQuestionsData];
    if (set !== 'all') {
        filtered = filtered.filter(q => q.set === parseInt(set));
    }
    if (type !== 'all' && type !== 'random') {
        filtered = filtered.filter(q => q.type === type);
    }
    if (type === 'random') {
        // 随机打乱，然后取前 20 题
        for (let i = filtered.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [filtered[i], filtered[j]] = [filtered[j], filtered[i]];
        }
        filtered = filtered.slice(0, 20);
    }
    
    window.questions = filtered;
    displayQuestion();
}

// 开始模拟考试
export function startMockExam() {
    window.currentQuizType = 'mock';
    window.currentSet = 'all';
    window.currentIndex = 0;
    window.userAnswers = {};
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    
    // 从每套题中随机抽取10题，共100题
    const mockQuestions = [];
    for (let set = 1; set <= 10; set++) {
        const setQuestions = allQuestionsData.filter(q => q.set === set);
        // 随机打乱
        for (let i = setQuestions.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [setQuestions[i], setQuestions[j]] = [setQuestions[j], setQuestions[i]];
        }
        // 取前10题
        mockQuestions.push(...setQuestions.slice(0, 10));
    }
    
    window.questions = mockQuestions;
    displayQuestion();
}

// 重新开始
export function restartQuiz() {
    startQuiz(window.currentQuizType, window.currentSet);
}

// 选择套数
export function selectSet(set) {
    window.currentSet = set;
    document.querySelectorAll('.set-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`set-${set}`).classList.add('active');
}

// 切换答案显示
export function toggleAnswer() {
    const q = window.questions[window.currentIndex];
    const answerSection = document.getElementById('answer-section');
    const showAnswerBtn = document.getElementById('show-answer-btn');
    
    if (window.answerShown) {
        answerSection.classList.remove('show');
        showAnswerBtn.textContent = '显示答案';
        window.answerShown = false;
    } else {
        let answerText = '';
        
        if (q.type === 'true_false') {
            answerText = q.answer ? '正确' : '错误';
        } else {
            answerText = q.answer;
        }
        
        document.getElementById('answer-content').textContent = answerText;
        answerSection.classList.add('show');
        showAnswerBtn.textContent = '隐藏答案';
        window.answerShown = true;
    }
}

// 仅查看错题
export function reviewWrongQuestions() {
    // 收集错题
    const wrongQuestions = [];
    window.questions.forEach((q, index) => {
        const qId = q.uid || q.id;
        const userAnswer = window.userAnswers[qId];
        let isCorrect = false;
        
        if (q.type === 'true_false') {
            isCorrect = (userAnswer === q.answer);
        } else if (q.type === 'multiple_choice') {
            const userAnswerStr = Array.isArray(userAnswer) ? userAnswer.sort().join('') : '';
            const correctAnswerStr = String(q.answer).toUpperCase().split('').sort().join('');
            isCorrect = (userAnswerStr === correctAnswerStr);
        } else if (q.type === 'fill_blank') {
            isCorrect = String(userAnswer || '').trim() === String(q.answer || '').trim();
        } else {
            isCorrect = String(userAnswer || '').toUpperCase() === String(q.answer || '').toUpperCase();
        }
        
        if (!isCorrect) {
            wrongQuestions.push(q);
        }
    });
    
    if (wrongQuestions.length === 0) {
        alert('🎉 恭喜！没有错题需要复习！');
        return;
    }
    
    // 开始复习错题
    window.questions = wrongQuestions;
    window.currentIndex = 0;
    window.userAnswers = {};
    window.currentQuizType = 'smart';
    
    document.getElementById('results').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    
    displayQuestion();
}
