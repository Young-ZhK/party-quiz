// 特殊列表模块（错题本、重点题）
import { allQuestionsData } from '../data/questions.js';
import { getItem, setItem, STORAGE_KEYS } from './storage.js';
import { QUESTION_TYPE_NAMES, QUESTION_TYPE_COLORS } from './constants.js';

// 显示错题本
export function showWrongQuestions() {
    window.specialListType = 'wrong';
    const wrongQuestionIds = getItem(STORAGE_KEYS.WRONG_QUESTIONS, []);
    const wrongQuestions = allQuestionsData.filter(q => wrongQuestionIds.includes(q.uid || q.id));
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('special-list').style.display = 'block';
    document.getElementById('special-title').textContent = '❌ 错题本';
    
    const contentEl = document.getElementById('special-list-content');
    
    if (wrongQuestions.length === 0) {
        contentEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">🎉 恭喜！没有错题需要复习</div>';
        document.getElementById('special-buttons').style.display = 'none';
        return;
    }
    
    document.getElementById('special-buttons').style.display = 'block';
    document.getElementById('clear-all-btn').onclick = clearAllWrongQuestions;
    
    let html = '<div style="padding: 20px;">';
    html += `<h3 style="text-align: center; margin-bottom: 20px;">错题本（共 ${wrongQuestions.length} 题）</h3>`;
    
    wrongQuestions.forEach((q, index) => {
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {
            optionsHtml = '<div class="browse-options">';
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {
                optionsHtml += `<div class="browse-option">${labels[i]}. ${opt}</div>`;
            });
            optionsHtml += '</div>';
        } else if (q.type === 'true_false') {
            optionsHtml = '<div class="browse-options">';
            optionsHtml += '<div class="browse-option">正确</div>';
            optionsHtml += '<div class="browse-option">错误</div>';
            optionsHtml += '</div>';
        }
        
        let answerText = '';
        if (q.type === 'true_false') {
            answerText = q.answer ? '正确' : '错误';
        } else {
            answerText = q.answer;
        }
        
        html += `<div class="browse-question-card">` +
            `<div class="browse-header">` +
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
            `</div>` +
            `</div>`;
    });
    
    html += '</div>';
    contentEl.innerHTML = html;
}

// 显示重点题
export function showStarredQuestions() {
    window.specialListType = 'starred';
    const starredQuestionIds = getItem(STORAGE_KEYS.STARRED_QUESTIONS, []);
    const starredQuestions = allQuestionsData.filter(q => starredQuestionIds.includes(q.uid || q.id));
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('special-list').style.display = 'block';
    document.getElementById('special-title').textContent = '⭐ 重点题';
    
    const contentEl = document.getElementById('special-list-content');
    
    if (starredQuestions.length === 0) {
        contentEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">还没有添加重点题</div>';
        document.getElementById('special-buttons').style.display = 'none';
        return;
    }
    
    document.getElementById('special-buttons').style.display = 'block';
    document.getElementById('clear-all-btn').onclick = clearAllStarredQuestions;
    
    let html = '<div style="padding: 20px;">';
    html += `<h3 style="text-align: center; margin-bottom: 20px;">重点题（共 ${starredQuestions.length} 题）</h3>`;
    
    starredQuestions.forEach((q, index) => {
        let optionsHtml = '';
        if (q.options && q.options.length > 0) {
            optionsHtml = '<div class="browse-options">';
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {
                optionsHtml += `<div class="browse-option">${labels[i]}. ${opt}</div>`;
            });
            optionsHtml += '</div>';
        } else if (q.type === 'true_false') {
            optionsHtml = '<div class="browse-options">';
            optionsHtml += '<div class="browse-option">正确</div>';
            optionsHtml += '<div class="browse-option">错误</div>';
            optionsHtml += '</div>';
        }
        
        let answerText = '';
        if (q.type === 'true_false') {
            answerText = q.answer ? '正确' : '错误';
        } else {
            answerText = q.answer;
        }
        
        html += `<div class="browse-question-card">` +
            `<div class="browse-header">` +
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
            `</div>` +
            `</div>`;
    });
    
    html += '</div>';
    contentEl.innerHTML = html;
}

// 清空所有错题
function clearAllWrongQuestions() {
    if (confirm('确定要清空所有错题吗？')) {
        setItem(STORAGE_KEYS.WRONG_QUESTIONS, []);
        showWrongQuestions();
    }
}

// 清空所有重点题
function clearAllStarredQuestions() {
    if (confirm('确定要清空所有重点题吗？')) {
        setItem(STORAGE_KEYS.STARRED_QUESTIONS, []);
        showStarredQuestions();
    }
}

// 清空特殊列表
export function clearAllSpecialList() {
    if (window.specialListType === 'wrong') {
        clearAllWrongQuestions();
    } else if (window.specialListType === 'starred') {
        clearAllStarredQuestions();
    }
}
