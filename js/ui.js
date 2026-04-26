// UI操作模块
import { allQuestionsData } from '../data/questions.js';

// 页面初始化
export function initPage() {
    // 确保只显示菜单，隐藏所有其他容器
    document.getElementById('menu').style.display = 'block';
    document.getElementById('quiz').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    document.getElementById('immersive').style.display = 'none';
    document.getElementById('im-results').style.display = 'none';
    document.getElementById('recite').style.display = 'none';
    document.getElementById('special-list').style.display = 'none';
}

// 返回菜单
export function backToMenu() {
    document.getElementById('menu').style.display = 'block';
    document.getElementById('quiz').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    document.getElementById('immersive').style.display = 'none';
    document.getElementById('im-results').style.display = 'none';
    document.getElementById('recite').style.display = 'none';
    document.getElementById('special-list').style.display = 'none';
}

// 切换折叠
export function toggleCollapse(id) {
    const content = document.getElementById(id);
    const icon = document.getElementById('collapse-icon-set');
    
    content.classList.toggle('collapsed');
    icon.classList.toggle('collapsed');
}

// 搜索功能
export function searchQuestions() {
    const keyword = document.getElementById('search-input').value.trim().toLowerCase();
    const resultsContainer = document.getElementById('search-results');
    
    if (!keyword) {
        resultsContainer.style.display = 'none';
        return;
    }
    
    let results = [];
    for (const q of allQuestionsData) {
        const questionText = q.question.toLowerCase();
        const answerText = String(q.answer).toLowerCase();
        if (questionText.includes(keyword) || answerText.includes(keyword)) {
            results.push(q);
        }
    }
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p style="text-align: center; color: #666; font-size: 1.1em;">没有找到相关题目 😔</p>';
    } else {
        let html = '';
        for (const q of results) {
            let setName = '';
            if (q.set === 1) setName = '第一套';
            else if (q.set === 2) setName = '第二套';
            else if (q.set === 3) setName = '第三套';
            else if (q.set === 4) setName = '第四套';
            else if (q.set === 5) setName = '第五套';
            else if (q.set === 6) setName = '第六套';
            else if (q.set === 7) setName = '第七套';
            else if (q.set === 8) setName = '第八套';
            else if (q.set === 9) setName = '第九套';
            else if (q.set === 10) setName = '第十套';
            
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
            
            html += '<div class="search-item">';
            html += `<div style="margin-bottom: 8px;"><span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em; margin-right: 8px;">${setName}</span><span style="background: #f5576c; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em;">${typeName}</span></div>`;
            html += `<div class="search-item-question">${q.question}</div>`;
            if (q.options && q.options.length > 0) {
                html += '<div style="margin: 10px 0;">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                for (let i = 0; i < q.options.length; i++) {
                    html += `<div style="margin: 5px 0; color: #555;">${labels[i]}. ${q.options[i]}</div>`;
                }
                html += '</div>';
            }
            html += `<div class="search-item-answer">✅ 正确答案：${answerDisplay}</div>`;
            html += '</div>';
        }
        
        resultsContainer.innerHTML = html;
    }
    
    resultsContainer.style.display = 'block';
}

// 处理搜索键盘事件
export function handleSearchKey(event) {
    if (event.key === 'Enter') {
        searchQuestions();
    }
}
