// 浏览题目模块
import { allQuestionsData } from '../data/questions.js';
import { QUESTION_TYPE_NAMES, QUESTION_TYPE_COLORS, SET_NAMES } from './constants.js';

// 开始浏览
export function startBrowse() {
    document.getElementById('menu').style.display = 'none';
    document.getElementById('quiz').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'block';
    
    filterBrowseQuestions();
}

// 筛选题目
export function filterBrowseQuestions() {
    const setFilter = document.getElementById('browse-set-filter').value;
    const typeFilter = document.getElementById('browse-type-filter').value;
    
    let filtered = allQuestionsData;
    
    if (setFilter !== 'all') {
        filtered = filtered.filter(q => q.set == setFilter);
    }
    
    if (typeFilter !== 'all') {
        filtered = filtered.filter(q => q.type === typeFilter);
    }
    
    renderBrowseQuestions(filtered);
}

// 渲染题目
export function renderBrowseQuestions(questionsToRender) {
    const listEl = document.getElementById('questions-list');
    listEl.innerHTML = '';
    
    if (questionsToRender.length === 0) {
        listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">没有找到符合条件的题目</div>';
        return;
    }
    
    questionsToRender.forEach((q, index) => {
        const card = document.createElement('div');
        card.className = 'browse-question-card';
        
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {
            optionsHtml = '<div class="browse-options">';
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {
                const isCorrect = (q.type === 'true_false') ? 
                    (i === 0 && q.answer) : 
                    (String(q.answer).toUpperCase().includes(labels[i]));
                optionsHtml += `<div class="browse-option ${isCorrect ? 'correct' : ''}">${labels[i]}. ${opt}</div>`;
            });
            optionsHtml += '</div>';
        } else if (q.type === 'true_false') {
            optionsHtml = '<div class="browse-options">';
            optionsHtml += `<div class="browse-option ${q.answer ? 'correct' : ''}">正确</div>`;
            optionsHtml += `<div class="browse-option ${!q.answer ? 'correct' : ''}">错误</div>`;
            optionsHtml += '</div>';
        }
        
        let answerText = '';
        if (q.type === 'true_false') {
            answerText = q.answer ? '正确' : '错误';
        } else {
            answerText = q.answer;
        }
        
        card.innerHTML = `<div class="browse-header">` +
            `<div class="browse-question-number">第 ${index + 1} 题（第${q.set}套 原编号${q.id}）</div>` +
            `<div class="browse-question-badges">` +
            `<span class="browse-badge" style="background: ${QUESTION_TYPE_COLORS[q.type]}">${QUESTION_TYPE_NAMES[q.type]}</span>` +
            `</div>` +
            `</div>` +
            `<div class="browse-question-text">${q.question}</div>` +
            optionsHtml +
            `<div class="browse-answer-box">` +
            `<div class="browse-answer-label">正确答案</div>` +
            `<div class="browse-answer-text">${answerText}</div>` +
            `</div>`;
        
        listEl.appendChild(card);
    });
}
