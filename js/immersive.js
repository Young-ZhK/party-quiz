// 沉浸式做题模块
import { allQuestionsData } from '../data/questions.js';
import { getItem, setItem, STORAGE_KEYS } from './storage.js';
import { QUESTION_TYPE_NAMES, QUESTION_TYPE_CLASSES } from './constants.js';

// 全局变量
window.imCurrentSet = null;
window.imCurrentIndex = 0;
window.imUserAnswers = {};
window.imQuestions = [];

// 开始沉浸式做题
export function startImmersive(set) {
    window.imCurrentSet = set;
    window.imCurrentIndex = 0;
    window.imUserAnswers = {};
    
    // 筛选题目
    window.imQuestions = allQuestionsData.filter(q => q.set === parseInt(set));
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('immersive').style.display = 'block';
    
    renderImmersiveQuestion();
    renderImmersiveQuestionGrid();
}

// 渲染沉浸式题目
function renderImmersiveQuestion() {
    const q = window.imQuestions[window.imCurrentIndex];
    
    document.getElementById('im-q-number').textContent = `第 ${window.imCurrentIndex + 1} 题 / 共 ${window.imQuestions.length} 题`;
    
    const typeEl = document.getElementById('im-q-type');
    typeEl.textContent = QUESTION_TYPE_NAMES[q.type];
    typeEl.className = `question-type ${QUESTION_TYPE_CLASSES[q.type]}`;
    
    document.getElementById('im-q-set').textContent = `第${window.imCurrentSet}套`;
    document.getElementById('im-q-text').textContent = q.question;
    
    const optionsEl = document.getElementById('im-options');
    optionsEl.innerHTML = '';
    
    const qId = q.uid || q.id;
    
    if (q.type === 'fill_blank') {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'fill-input';
        input.placeholder = '请输入答案...';
        input.value = window.imUserAnswers[qId] || '';
        input.oninput = function(e) { window.imUserAnswers[qId] = e.target.value; };
        optionsEl.appendChild(input);
    } else if (q.type === 'true_false') {
        ['正确', '错误'].forEach((opt, i) => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = opt;
            const val = i === 0;
            if (window.imUserAnswers[qId] === val) {
                div.classList.add('selected');
            }
            div.onclick = function() { imSelectOption(qId, val, div); };
            optionsEl.appendChild(div);
        });
    } else {
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        q.options.forEach((opt, i) => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = `${labels[i]}. ${opt}`;
            
            if (q.type === 'multiple_choice') {
                if (Array.isArray(window.imUserAnswers[qId]) && window.imUserAnswers[qId].includes(labels[i])) {
                    div.classList.add('selected');
                }
            } else {
                if (window.imUserAnswers[qId] === labels[i]) {
                    div.classList.add('selected');
                }
            }
            
            div.onclick = function() { imSelectOption(qId, labels[i], div, q.type); };
            optionsEl.appendChild(div);
        });
    }
    
    document.getElementById('im-btn-prev').style.display = window.imCurrentIndex > 0 ? 'block' : 'none';
    document.getElementById('im-btn-next').style.display = window.imCurrentIndex < window.imQuestions.length - 1 ? 'block' : 'none';
}

// 选择选项
function imSelectOption(qId, value, el, qType) {
    const q = window.imQuestions.find(x => (x.uid || x.id) === qId) || window.imQuestions[window.imCurrentIndex];
    
    if (qType === 'multiple_choice' || q.type === 'multiple_choice') {
        if (!Array.isArray(window.imUserAnswers[qId])) {
            window.imUserAnswers[qId] = [];
        }
        const idx = window.imUserAnswers[qId].indexOf(value);
        if (idx === -1) {
            window.imUserAnswers[qId].push(value);
        } else {
            window.imUserAnswers[qId].splice(idx, 1);
        }
        
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        const siblings = el.parentElement.children;
        for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            sibling.classList.remove('selected');
            if (Array.isArray(window.imUserAnswers[qId]) && window.imUserAnswers[qId].includes(labels[i])) {
                sibling.classList.add('selected');
            }
        }
    } else {
        window.imUserAnswers[qId] = value;
        
        const siblings = el.parentElement.children;
        for (let sibling of siblings) {
            sibling.classList.remove('selected');
        }
        el.classList.add('selected');
    }
    
    // 更新题目网格
    renderImmersiveQuestionGrid();
}

// 渲染题目网格
function renderImmersiveQuestionGrid() {
    const grid = document.getElementById('im-question-grid');
    grid.innerHTML = '';
    
    window.imQuestions.forEach((q, index) => {
        const qId = q.uid || q.id;
        const dot = document.createElement('div');
        dot.className = 'question-dot';
        if (window.imUserAnswers[qId]) {
            dot.classList.add('answered');
        }
        if (index === window.imCurrentIndex) {
            dot.classList.add('current');
        }
        dot.textContent = index + 1;
        dot.onclick = () => imGoToQuestion(index);
        grid.appendChild(dot);
    });
}

// 跳转到指定题目
export function imGoToQuestion(index) {
    window.imCurrentIndex = index;
    renderImmersiveQuestion();
    renderImmersiveQuestionGrid();
}

// 上一题
export function imPrevQuestion() {
    if (window.imCurrentIndex > 0) {
        window.imCurrentIndex--;
        renderImmersiveQuestion();
        renderImmersiveQuestionGrid();
    }
}

// 下一题
export function imNextQuestion() {
    if (window.imCurrentIndex < window.imQuestions.length - 1) {
        window.imCurrentIndex++;
        renderImmersiveQuestion();
        renderImmersiveQuestionGrid();
    }
}

// 提交答案
export function imSubmitQuiz() {
    let correct = 0;
    const results = [];
    window.imQuestions.forEach((q, index) => {
        const qId = q.uid || q.id;
        let userAnswer = window.imUserAnswers[qId];
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
    
    imShowResults({
        score: correct,
        total: window.imQuestions.length,
        results: results
    });
}

// 显示结果
function imShowResults(result) {
    document.getElementById('immersive').style.display = 'none';
    document.getElementById('im-results').style.display = 'block';
    
    document.getElementById('im-score-display').textContent = `${result.score}/${result.total}`;
    
    const percentage = Math.round((result.score / result.total) * 100);
    let text = '';
    if (percentage >= 90) text = '🎉 太棒了！成绩优秀！';
    else if (percentage >= 70) text = '👍 不错！继续努力！';
    else if (percentage >= 60) text = '💪 及格了，但还需要加强！';
    else text = '📚 需要多练习哦！';
    document.getElementById('im-score-text').textContent = text;
    
    const detailsEl = document.getElementById('im-result-details');
    detailsEl.innerHTML = '';
    
    result.results.forEach((res, index) => {
        const q = window.imQuestions[index];
        let optionsHtml = '';
        
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
            `<strong>第 ${index + 1} 题</strong>${res.question}` +
            optionsHtml +
            `<br><em>你的答案：${res.user_answer} | 正确答案：${res.correct_answer}</em>` +
            '</div>';
    });
}

// 重新开始
export function imRestartQuiz() {
    startImmersive(window.imCurrentSet);
}
