// 背诵模式模块
import { allQuestionsData } from '../data/questions.js';
import { QUESTION_TYPE_NAMES, QUESTION_TYPE_CLASSES } from './constants.js';

// 全局变量
let reciteQuestions = [];
let reciteIndex = 0;
let reciteAnswerShown = false;
let autoShowAnswers = false; // 自动显示答案的标志

// 开始背诵模式
export function startReciteMode() {
    const setFilter = document.getElementById('recite-set-filter').value;
    
    reciteQuestions = [];
    for (const q of allQuestionsData) {
        if (setFilter === 'all' || String(q.set) === setFilter) {
            reciteQuestions.push(q);
        }
    }
    
    // 保持题目顺序不变
    
    reciteIndex = 0;
    reciteAnswerShown = false;
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('recite').style.display = 'block';
    
    renderReciteQuestionGrid();
    renderReciteQuestion();
}

// 渲染背诵题目网格
function renderReciteQuestionGrid() {
    const grid = document.getElementById('recite-question-grid');
    grid.innerHTML = '';
    
    reciteQuestions.forEach((q, index) => {
        const dot = document.createElement('div');
        dot.className = 'question-dot';
        dot.textContent = index + 1;
        dot.onclick = () => reciteGoToQuestion(index);
        grid.appendChild(dot);
    });
    
    updateReciteQuestionGrid();
}

// 更新背诵题目网格
function updateReciteQuestionGrid() {
    const dots = document.querySelectorAll('#recite-question-grid .question-dot');
    
    dots.forEach((dot, index) => {
        dot.classList.remove('current', 'mastered');
        
        if (index === reciteIndex) {
            dot.classList.add('current');
        }
    });
}

// 跳转到指定题目
export function reciteGoToQuestion(index) {
    reciteIndex = index;
    reciteAnswerShown = false;
    renderReciteQuestion();
}

// 渲染背诵题目
function renderReciteQuestion() {
    const q = reciteQuestions[reciteIndex];
    
    // 更新题目编号和进度
    document.getElementById('recite-number').textContent = `第 ${reciteIndex + 1} 题`;
    document.getElementById('recite-progress').textContent = `${reciteIndex + 1}/${reciteQuestions.length}`;
    
    // 更新题目内容
    document.getElementById('recite-question').textContent = q.question;
    
    const optionsEl = document.getElementById('recite-options');
    optionsEl.innerHTML = '';
    
    if (q.type === 'fill_blank') {
        // 填空题显示输入框
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'fill-input';
        input.placeholder = '请输入答案...';
        optionsEl.appendChild(input);
    } else if (q.type === 'true_false') {
        // 判断题显示正确/错误选项
        ['正确', '错误'].forEach(opt => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = opt;
            optionsEl.appendChild(div);
        });
    } else {
        // 选择题显示选项
        const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
        q.options.forEach((opt, i) => {
            const div = document.createElement('div');
            div.className = 'option';
            div.textContent = `${labels[i]}. ${opt}`;
            optionsEl.appendChild(div);
        });
    }
    
    const answerEl = document.getElementById('recite-answer');
    answerEl.style.display = 'none';
    
    document.getElementById('recite-toggle-btn').textContent = '显示答案';
    reciteAnswerShown = false;
    
    // 如果autoShowAnswers为true，自动显示答案
    if (autoShowAnswers) {
        let answerText = '';
        if (q.type === 'true_false') {
            // 处理A/B形式的答案
            if (q.answer === 'A') {
                answerText = '正确';
            } else if (q.answer === 'B') {
                answerText = '错误';
            } else {
                // 处理布尔值形式的答案
                answerText = q.answer ? '正确' : '错误';
            }
        } else {
            answerText = q.answer;
        }
        
        document.getElementById('recite-answer-content').textContent = answerText;
        answerEl.style.display = 'block';
        document.getElementById('recite-toggle-btn').textContent = '答案已显示';
        reciteAnswerShown = true;
    }
    
    updateReciteQuestionGrid();
}

// 显示答案（只显示，不隐藏）
export function reciteToggleAnswer() {
    const q = reciteQuestions[reciteIndex];
    const answerEl = document.getElementById('recite-answer');
    const showAnswerBtn = document.getElementById('recite-toggle-btn');
    
    // 只显示答案，不提供隐藏功能
    let answerText = '';
    if (q.type === 'true_false') {
        // 处理A/B形式的答案
        if (q.answer === 'A') {
            answerText = '正确';
        } else if (q.answer === 'B') {
            answerText = '错误';
        } else {
            // 处理布尔值形式的答案
            answerText = q.answer ? '正确' : '错误';
        }
    } else {
        answerText = q.answer;
    }
    
    document.getElementById('recite-answer-content').textContent = answerText;
    answerEl.style.display = 'block';
    showAnswerBtn.textContent = '答案已显示';
    showAnswerBtn.disabled = true;
    reciteAnswerShown = true;
    autoShowAnswers = true; // 设置自动显示答案标志
}

// 切换收藏状态
export function toggleReciteStar() {
    const q = reciteQuestions[reciteIndex];
    const qId = q.uid || q.id;
    const starBtn = document.getElementById('recite-star-btn');
    
    // 这里可以添加收藏功能的逻辑
    starBtn.textContent = starBtn.textContent === '⭐' ? '☆' : '⭐';
}

// 上一题
export function recitePrevQuestion() {
    if (reciteIndex > 0) {
        reciteIndex--;
        reciteAnswerShown = false;
        renderReciteQuestion();
    }
}

// 下一题
export function reciteNextQuestion() {
    if (reciteIndex < reciteQuestions.length - 1) {
        reciteIndex++;
        reciteAnswerShown = false;
        renderReciteQuestion();
    }
}

// 上一题（HTML中调用的函数名）
export function prevRecite() {
    recitePrevQuestion();
}

// 下一题（HTML中调用的函数名）
export function nextRecite() {
    reciteNextQuestion();
}

// 切换答案显示（HTML中调用的函数名）
export function toggleReciteAnswer() {
    reciteToggleAnswer();
}
