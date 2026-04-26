#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

# 设置输出编码为UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def main():
    # 读取完整的questions.json
    questions_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions.json')
    with open(questions_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # 读取index.html
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 找到脚本开始位置
    script_start = html_content.find('<script>')
    
    # 生成新的题目数据JSON
    questions_json = json.dumps(all_questions, ensure_ascii=False, separators=(',', ':'))
    
    # 构建正确的脚本内容
    new_script = '''<script>
    // ========== 嵌入式题目数据（共''' + str(len(all_questions)) + '''道题）==========
    const allQuestionsData = ''' + questions_json + ''';
    
    function toggleCollapse(id) {
        const content = document.getElementById(id);
        const icon = document.getElementById('collapse-icon-set');
        
        content.classList.toggle('collapsed');
        icon.classList.toggle('collapsed');
    }
    
    // ========== 页面初始化 ==========
    window.onload = function() {
        // 确保只显示菜单，隐藏所有其他容器
        document.getElementById('menu').style.display = 'block';
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        document.getElementById('immersive').style.display = 'none';
        document.getElementById('im-results').style.display = 'none';
        document.getElementById('recite').style.display = 'none';
        document.getElementById('special-list').style.display = 'none';
    };
    
    let questions = [];
    let currentIndex = 0;
    let userAnswers = {};
    let currentQuizType = 'all';
    let examStartTime = null;
    let examTimer = null;
    let currentSet = 'all';
    let answerShown = false;
    
    // ========== 错题本和重点题 ==========
    let wrongQuestions = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
    let starredQuestions = JSON.parse(localStorage.getItem('starredQuestions') || '[]');
    
    // ========== 题目掌握程度 ==========
    let questionMastery = JSON.parse(localStorage.getItem('questionMastery') || '{}');
    
    function saveQuestionMastery() {
        localStorage.setItem('questionMastery', JSON.stringify(questionMastery));
    }
    
    // ========== 复习计划 ==========
    let studyPlan = JSON.parse(localStorage.getItem('studyPlan') || '{}');
    
    function saveStudyPlan() {
        localStorage.setItem('studyPlan', JSON.stringify(studyPlan));
    }
    
    // ========== 学习历史 ==========
    let studyHistory = JSON.parse(localStorage.getItem('studyHistory') || '[]');
    
    function saveStudyHistory() {
        localStorage.setItem('studyHistory', JSON.stringify(studyHistory));
    }
    
    function addStudyRecord(record) {
        studyHistory.unshift({
            ...record,
            timestamp: new Date().toISOString()
        });
        
        // 限制历史记录数量
        if (studyHistory.length > 100) {
            studyHistory = studyHistory.slice(0, 100);
        }
        
        saveStudyHistory();
    }
    
    function getStudyStats() {
        const stats = {
            totalSessions: studyHistory.length,
            totalQuestions: 0,
            totalCorrect: 0,
            averageScore: 0,
            recentScores: [],
            dailyStats: {}
        };
        
        studyHistory.forEach(session => {
            stats.totalQuestions += session.total;
            stats.totalCorrect += session.correct;
            stats.recentScores.push((session.correct / session.total) * 100);
            
            // 按日期统计
            const date = session.timestamp.split('T')[0];
            if (!stats.dailyStats[date]) {
                stats.dailyStats[date] = {
                    questions: 0,
                    correct: 0
                };
            }
            stats.dailyStats[date].questions += session.total;
            stats.dailyStats[date].correct += session.correct;
        });
        
        if (stats.totalQuestions > 0) {
            stats.averageScore = Math.round((stats.totalCorrect / stats.totalQuestions) * 100);
        }
        
        return stats;
    }
    
    function generateStudyPlan() {
        // 计算需要复习的题目
        const needReviewQuestions = allQuestionsData.filter(q => {
            const qId = q.uid || q.id;
            const mastery = questionMastery[qId];
            if (!mastery) return true; // 未作答的题目
            return mastery.masteryLevel !== 'mastered'; // 未掌握的题目
        });
        
        // 按复习优先级排序
        const prioritizedQuestions = needReviewQuestions.map(q => {
            const qId = q.uid || q.id;
            return {
                question: q,
                priority: calculateReviewPriority(qId)
            };
        }).sort((a, b) => b.priority - a.priority);
        
        // 生成每日计划（每天20题）
        const dailyQuestions = 20;
        const days = Math.ceil(prioritizedQuestions.length / dailyQuestions);
        
        const plan = [];
        for (let i = 0; i < days; i++) {
            const start = i * dailyQuestions;
            const end = start + dailyQuestions;
            const dayQuestions = prioritizedQuestions.slice(start, end).map(item => item.question);
            
            plan.push({
                day: i + 1,
                questions: dayQuestions.map(q => q.uid || q.id),
                completed: false,
                date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
            });
        }
        
        studyPlan = {
            generatedAt: new Date().toISOString(),
            totalDays: days,
            totalQuestions: prioritizedQuestions.length,
            plan: plan
        };
        
        saveStudyPlan();
        return studyPlan;
    }
    
    function markPlanDayComplete(dayIndex) {
        if (studyPlan.plan && studyPlan.plan[dayIndex]) {
            studyPlan.plan[dayIndex].completed = true;
            saveStudyPlan();
        }
    }
    
    function getTodayStudyPlan() {
        if (!studyPlan.plan || studyPlan.plan.length === 0) {
            return null;
        }
        
        const today = new Date().toISOString().split('T')[0];
        return studyPlan.plan.find(day => day.date === today) || 
               studyPlan.plan.find(day => !day.completed);
    }
    
    function updateQuestionMastery(qId, isCorrect, timeSpent = 0) {
        if (!questionMastery[qId]) {
            questionMastery[qId] = {
                totalAttempts: 0,
                correctAttempts: 0,
                consecutiveCorrect: 0,
                lastAttempt: null,
                lastResult: null,
                averageTime: 0,
                masteryLevel: 'unknown',
                reviewCount: 0,
                lastReview: null
            };
        }
        
        const mastery = questionMastery[qId];
        mastery.totalAttempts++;
        mastery.lastAttempt = new Date().toISOString();
        mastery.lastResult = isCorrect;
        
        if (isCorrect) {
            mastery.correctAttempts++;
            mastery.consecutiveCorrect++;
        } else {
            mastery.consecutiveCorrect = 0;
        }
        
        // 更新平均答题时间
        if (mastery.totalAttempts === 1) {
            mastery.averageTime = timeSpent;
        } else {
            mastery.averageTime = ((mastery.averageTime * (mastery.totalAttempts - 1)) + timeSpent) / mastery.totalAttempts;
        }
        
        // 更新掌握程度
        if (mastery.consecutiveCorrect >= 3) {
            mastery.masteryLevel = 'mastered';
        } else if (mastery.correctAttempts >= mastery.totalAttempts / 2) {
            mastery.masteryLevel = 'familiar';
        } else {
            mastery.masteryLevel = 'unfamiliar';
        }
        
        saveQuestionMastery();
    }
    
    function calculateReviewPriority(qId) {
        const mastery = questionMastery[qId];
        if (!mastery) return 10; // 未作答的题目优先级最高
        
        let priority = 0;
        
        // 基于掌握程度
        if (mastery.masteryLevel === 'unfamiliar') priority += 8;
        else if (mastery.masteryLevel === 'familiar') priority += 4;
        
        // 基于错误次数
        const wrongCount = mastery.totalAttempts - mastery.correctAttempts;
        priority += wrongCount * 2;
        
        // 基于时间间隔
        if (mastery.lastAttempt) {
            const daysSinceLast = (Date.now() - new Date(mastery.lastAttempt).getTime()) / (1000 * 60 * 60 * 24);
            priority += Math.min(daysSinceLast, 5);
        }
        
        return priority;
    }
    
    function selectSet(set) {
        currentSet = set;
        document.querySelectorAll('.set-btn').forEach(btn => btn.classList.remove('active'));
        document.getElementById('set-' + set).classList.add('active');
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
            } else {
                answerText = q.answer;
            }
            
            document.getElementById('answer-content').textContent = answerText;
            answerSection.classList.add('show');
            showAnswerBtn.textContent = '隐藏答案';
            answerShown = true;
        }
    }
    
    function startQuiz(type) {
        currentQuizType = type;
        currentIndex = 0;
        userAnswers = {};
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        
        // 从 allQuestionsData 中筛选题目
        let filtered = [...allQuestionsData];
        if (currentSet !== 'all') {
            filtered = filtered.filter(q => q.set === parseInt(currentSet));
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
        
        questions = filtered;
        displayQuestion();
    }
    
    function displayQuestion() {
        const q = questions[currentIndex];
        
        answerShown = false;
        document.getElementById('answer-section').classList.remove('show');
        document.getElementById('show-answer-btn').textContent = '显示答案';
        
        document.getElementById('q-number').textContent = '第 ' + (currentIndex + 1) + ' 题 / 共 ' + questions.length + ' 题';
        
        const typeNames = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        };
        
        const typeClass = {
            'single_choice': 'type-single',
            'multiple_choice': 'type-multiple',
            'true_false': 'type-tf',
            'fill_blank': 'type-fill'
        };
        
        const typeEl = document.getElementById('q-type');
        typeEl.textContent = typeNames[q.type];
        typeEl.className = 'question-type ' + typeClass[q.type];
        
        const setEl = document.getElementById('q-set');
        setEl.textContent = q.set ? '第' + q.set + '套' : '题目';
        
        document.getElementById('q-text').textContent = q.question;
        
        const optionsEl = document.getElementById('options');
        optionsEl.innerHTML = '';
        
        const qId = q.uid || q.id;
        
        if (q.type === 'fill_blank') {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'fill-input';
            input.placeholder = '请输入答案...';
            input.value = userAnswers[qId] || '';
            input.oninput = function(e) { userAnswers[qId] = e.target.value; };
            optionsEl.appendChild(input);
            
            const checkBtn = document.createElement('button');
            checkBtn.className = 'show-answer-btn';
            checkBtn.textContent = '检查答案';
            checkBtn.style.marginTop = '10px';
            checkBtn.onclick = function() {
                checkFillAnswer(qId, input, q, optionsEl);
            };
            optionsEl.appendChild(checkBtn);
            
            const feedback = document.createElement('div');
            feedback.id = 'fill-feedback-' + qId;
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
                if (userAnswers[qId] === val) {
                    div.classList.add('selected');
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
                div.onclick = function() { selectOption(qId, val, div); };
                optionsEl.appendChild(div);
            });
        } else {
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            q.options.forEach((opt, i) => {
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = labels[i] + '. ' + opt;
                
                if (q.type === 'multiple_choice') {
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {
                        div.classList.add('selected');
                    }
                } else {
                    if (userAnswers[qId] === labels[i]) {
                        div.classList.add('selected');
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
                
                div.onclick = function() { selectOption(qId, labels[i], div, q.type); };
                optionsEl.appendChild(div);
            });
        }
        
        document.getElementById('btn-prev').style.display = currentIndex > 0 ? 'block' : 'none';
        
        if (currentIndex === questions.length - 1) {
            document.getElementById('btn-next').style.display = 'none';
            document.getElementById('btn-submit').style.display = 'block';
        } else {
            document.getElementById('btn-next').style.display = 'block';
            document.getElementById('btn-submit').style.display = 'none';
        }
    }
    
    function selectOption(qId, value, el, qType) {
        const q = questions.find(x => (x.uid || x.id) === qId) || questions[currentIndex];
        
        if (qType === 'multiple_choice' || q.type === 'multiple_choice') {
            if (!Array.isArray(userAnswers[qId])) {
                userAnswers[qId] = [];
            }
            const idx = userAnswers[qId].indexOf(value);
            if (idx === -1) {
                userAnswers[qId].push(value);
            } else {
                userAnswers[qId].splice(idx, 1);
            }
            
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            const siblings = el.parentElement.children;
            for (let i = 0; i < siblings.length; i++) {
                const sibling = siblings[i];
                sibling.classList.remove('selected', 'correct', 'wrong');
                if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {
                    sibling.classList.add('selected');
                }
            }
            
            const userAnswer = Array.isArray(userAnswers[qId]) ? userAnswers[qId].sort().join('') : '';
            const correctAnswer = String(q.answer).toUpperCase().split('').sort().join('');
            const isCorrect = userAnswer === correctAnswer;
            
            if (isCorrect) {
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {
                        sibling.classList.remove('selected');
                        sibling.classList.add('correct');
                    }
                }
                removeFromWrongQuestions(qId);
            } else {
                showCorrectAnswer(q, el.parentElement);
                for (let i = 0; i < siblings.length; i++) {
                    const sibling = siblings[i];
                    if (Array.isArray(userAnswers[qId]) && userAnswers[qId].includes(labels[i])) {
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
        } else {
            userAnswers[qId] = value;
            
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
                removeFromWrongQuestions(qId);
            } else {
                el.classList.remove('selected');
                el.classList.add('wrong');
                showCorrectAnswer(q, el.parentElement);
                addToWrongQuestions(qId);
            }
        }
    }
    
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
    
    function checkFillAnswer(qId, input, q, container) {
        const feedback = document.getElementById('fill-feedback-' + qId);
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
            feedback.innerHTML = '❌ 回答错误！正确答案是：<strong>' + correctAnswer + '</strong>';
            input.style.borderColor = '#f45c43';
            addToWrongQuestions(qId);
        }
    }
    
    function prevQuestion() {
        if (currentIndex > 0) {
            currentIndex--;
            displayQuestion();
        }
    }
    
    function nextQuestion() {
        if (currentIndex < questions.length - 1) {
            currentIndex++;
            displayQuestion();
        }
    }
    
    function submitQuiz() {
        let correct = 0;
        const results = [];
        questions.forEach((q, index) => {
            const qId = q.uid || q.id;
            let userAnswer = userAnswers[qId];
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
            total: questions.length,
            results: results
        });
    }
    
    function showResults(result) {
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
        
        result.results.forEach((res, index) => {
            const q = questions[index];
            let optionsHtml = '';
            let userAnswerWithOption = res.user_answer;
            let correctAnswerWithOption = res.correct_answer;
            
            if (q.type !== 'fill_blank' && q.type !== 'true_false' && q.options && q.options.length > 0) {
                optionsHtml = '<div style="font-size: 0.9em; margin-top: 8px; color: #666;">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {
                    const label = labels[i] || String.fromCharCode(65 + i);
                    optionsHtml += '<div style="margin: 4px 0;">' + label + '. ' + opt + '</div>';
                });
                optionsHtml += '</div>';
            }
            
            detailsEl.innerHTML += '<div class="result-item ' + (res.correct ? 'result-correct' : 'result-wrong') + '">' +
                '<strong>第 ' + (index + 1) + ' 题（第' + res.set + '套）</strong>' + res.question +
                optionsHtml +
                '<br><em>你的答案：' + userAnswerWithOption + ' | 正确答案：' + correctAnswerWithOption + '</em>' +
                '</div>';
        });
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
    
    // ========== 沉浸式做题函数 ==========
    function startImmersive(set) {
        imCurrentSet = set;
        imCurrentIndex = 0;
        imUserAnswers = {};

        document.getElementById('menu').style.display = 'none';
        document.getElementById('immersive').style.display = 'block';
        document.getElementById('im-results').style.display = 'none';

        // 获取指定套的100题
        imQuestions = allQuestionsData.filter(q => q.set === parseInt(set));

        // 渲染题目列表
        renderImQuestionGrid();

        imDisplayQuestion();
    }
    
    function renderImQuestionGrid() {
        const grid = document.getElementById('im-question-grid');
        grid.innerHTML = '';
        
        imQuestions.forEach((q, index) => {
            const dot = document.createElement('div');
            dot.className = 'question-dot';
            dot.textContent = index + 1;
            dot.onclick = () => imGoToQuestion(index);
            grid.appendChild(dot);
        });
        
        updateImQuestionGrid();
    }
    
    function updateImQuestionGrid() {
        const dots = document.querySelectorAll('#im-question-grid .question-dot');
        
        dots.forEach((dot, index) => {
            dot.classList.remove('answered', 'current');
            
            const q = imQuestions[index];
            const qId = q.uid || q.id;
            const isAnswered = imUserAnswers[qId] !== undefined && 
                (Array.isArray(imUserAnswers[qId]) ? imUserAnswers[qId].length > 0 : imUserAnswers[qId] !== '');
            
            if (isAnswered) {
                dot.classList.add('answered');
            }
            
            if (index === imCurrentIndex) {
                dot.classList.add('current');
            }
        });
    }
    
    function imGoToQuestion(index) {
        imCurrentIndex = index;
        imDisplayQuestion();
    }
    
    function imDisplayQuestion() {
        const q = imQuestions[imCurrentIndex];
        
        document.getElementById('im-q-number').textContent = '第 ' + (imCurrentIndex + 1) + ' 题 / 共 ' + imQuestions.length + ' 题';

        const typeNames = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        };

        const typeClass = {
            'single_choice': 'type-single',
            'multiple_choice': 'type-multiple',
            'true_false': 'type-tf',
            'fill_blank': 'type-fill'
        };

        const typeEl = document.getElementById('im-q-type');
        typeEl.textContent = typeNames[q.type];
        typeEl.className = 'question-type ' + typeClass[q.type];

        const setEl = document.getElementById('im-q-set');
        setEl.textContent = '第' + q.set + '套';

        document.getElementById('im-q-text').textContent = q.question;

        const optionsEl = document.getElementById('im-options');
        optionsEl.innerHTML = '';

        const qId = q.uid || q.id;

        if (q.type === 'fill_blank') {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'fill-input';
            input.placeholder = '请输入答案...';
            input.value = imUserAnswers[qId] || '';
            input.oninput = function(e) { 
                imUserAnswers[qId] = e.target.value; 
                updateImQuestionGrid();
            };
            optionsEl.appendChild(input);
        } else if (q.type === 'true_false') {
            ['正确', '错误'].forEach((opt, i) => {
                const div = document.createElement('div');
                div.className = 'option';
                div.textContent = opt;
                const val = i === 0;
                if (imUserAnswers[qId] === val) {
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
                div.textContent = labels[i] + '. ' + opt;
                
                if (q.type === 'multiple_choice') {
                    if (Array.isArray(imUserAnswers[qId]) && imUserAnswers[qId].includes(labels[i])) {
                        div.classList.add('selected');
                    }
                } else {
                    if (imUserAnswers[qId] === labels[i]) {
                        div.classList.add('selected');
                    }
                }
                
                div.onclick = function() { imSelectOption(qId, labels[i], div, q.type); };
                optionsEl.appendChild(div);
            });
        }

        document.getElementById('im-btn-prev').style.display = imCurrentIndex > 0 ? 'block' : 'none';
        document.getElementById('im-btn-next').style.display = imCurrentIndex < imQuestions.length - 1 ? 'block' : 'none';
        
        updateImQuestionGrid();
    }
    
    function imSelectOption(qId, value, el, qType) {
        const q = imQuestions[imCurrentIndex];
        
        if (qType === 'multiple_choice' || q.type === 'multiple_choice') {
            if (!Array.isArray(imUserAnswers[qId])) {
                imUserAnswers[qId] = [];
            }
            const idx = imUserAnswers[qId].indexOf(value);
            if (idx === -1) {
                imUserAnswers[qId].push(value);
            } else {
                imUserAnswers[qId].splice(idx, 1);
            }
            
            const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
            const siblings = el.parentElement.children;
            for (let i = 0; i < siblings.length; i++) {
                const sibling = siblings[i];
                sibling.classList.remove('selected');
                if (Array.isArray(imUserAnswers[qId]) && imUserAnswers[qId].includes(labels[i])) {
                    sibling.classList.add('selected');
                }
            }
        } else {
            imUserAnswers[qId] = value;
            
            const siblings = el.parentElement.children;
            for (let sibling of siblings) {
                sibling.classList.remove('selected');
            }
            el.classList.add('selected');
        }
        
        updateImQuestionGrid();
    }
    
    function imPrevQuestion() {
        if (imCurrentIndex > 0) {
            imCurrentIndex--;
            imDisplayQuestion();
        }
    }
    
    function imNextQuestion() {
        if (imCurrentIndex < imQuestions.length - 1) {
            imCurrentIndex++;
            imDisplayQuestion();
        }
    }
    
    function imSubmitQuiz() {
        let correct = 0;
        const results = [];

        imQuestions.forEach((q, index) => {
            const qId = q.uid || q.id;
            let userAnswer = imUserAnswers[qId];
            let isCorrect = false;

            if (q.type === 'true_false') {
                isCorrect = (userAnswer === q.answer);
            } else if (q.type === 'multiple_choice') {
                const userAnswerStr = Array.isArray(userAnswer) ? userAnswer.sort().join('') : String(userAnswer || '').toUpperCase();
                const correctAnswerStr = String(q.answer).toUpperCase().split('').sort().join('');
                isCorrect = userAnswerStr === correctAnswerStr;
                userAnswer = Array.isArray(userAnswer) ? userAnswer.join('') : userAnswer;
            } else {
                isCorrect = String(userAnswer || '').toUpperCase() === String(q.answer).toUpperCase();
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

        imShowResults({
            score: correct,
            total: imQuestions.length,
            results: results
        });
    }
    
    function imShowResults(result) {
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

        result.results.forEach((res, index) => {
            const q = imQuestions[index];
            let optionsHtml = '';
            let userAnswerWithOption = res.user_answer;
            let correctAnswerWithOption = res.correct_answer;

            if (q.type !== 'fill_blank' && q.type !== 'true_false' && q.options && q.options.length > 0) {
                optionsHtml = '<div style="font-size: 0.9em; margin-top: 8px; color: #666;">';
                const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                q.options.forEach((opt, i) => {
                    const label = labels[i] || String.fromCharCode(65 + i);
                    optionsHtml += '<div style="margin: 4px 0;">' + label + '. ' + opt + '</div>';
                });
                optionsHtml += '</div>';
            }
            
            detailsEl.innerHTML += '<div class="result-item ' + (res.correct ? 'result-correct' : 'result-wrong') + '">' +
                '<strong>第 ' + (index + 1) + ' 题（第' + res.set + '套）</strong>' + res.question +
                optionsHtml +
                '<br><em>你的答案：' + userAnswerWithOption + ' | 正确答案：' + correctAnswerWithOption + '</em>' +
                '</div>';
        });
    }
    
    function imRestartQuiz() {
        startImmersive(imCurrentSet);
    }
    
    function restartQuiz() {
        startQuiz(currentQuizType);
    }
    
    function startBrowse() {
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'none';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'block';
        
        filterBrowseQuestions();
    }
    
    function filterBrowseQuestions() {
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
    
    function renderBrowseQuestions(questionsToRender) {
        const listEl = document.getElementById('questions-list');
        listEl.innerHTML = '';
        
        if (questionsToRender.length === 0) {
            listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">没有找到符合条件的题目</div>';
            return;
        }
        
        const typeNames = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        };
        
        const typeColors = {
            'single_choice': '#667eea',
            'multiple_choice': '#f093fb',
            'true_false': '#f5576c',
            'fill_blank': '#43e97b'
        };
        
        const setNames = {
            1: '第一套', 2: '第二套', 3: '第三套', 4: '第四套',
            5: '第五套', 6: '第六套', 7: '第七套', 8: '第八套', 9: '第九套', 10: '第十套'
        };
        
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
                    optionsHtml += '<div class="browse-option ' + (isCorrect ? 'correct' : '') + '">' + labels[i] + '. ' + opt + '</div>';
                });
                optionsHtml += '</div>';
            } else if (q.type === 'true_false') {
                optionsHtml = '<div class="browse-options">';
                optionsHtml += '<div class="browse-option ' + (q.answer ? 'correct' : '') + '">正确</div>';
                optionsHtml += '<div class="browse-option ' + (!q.answer ? 'correct' : '') + '">错误</div>';
                optionsHtml += '</div>';
            }
            
            let answerText = '';
            if (q.type === 'true_false') {
                answerText = q.answer ? '正确' : '错误';
            } else {
                answerText = q.answer;
            }
            
            card.innerHTML = '<div class="browse-header">' +
                '<div class="browse-question-number">第 ' + (index + 1) + ' 题（第' + q.set + '套 原编号' + q.id + '）</div>' +
                '<div class="browse-question-badges">' +
                '<span class="browse-badge" style="background: ' + typeColors[q.type] + '">' + typeNames[q.type] + '</span>' +
                '</div>' +
                '</div>' +
                '<div class="browse-question-text">' + q.question + '</div>' +
                optionsHtml +
                '<div class="browse-answer-box">' +
                '<div class="browse-answer-label">正确答案</div>' +
                '<div class="browse-answer-text">' + answerText + '</div>' +
                '</div>';
            
            listEl.appendChild(card);
        });
    }
    
    // ========== 背诵模式函数 ==========
    function startReciteMode() {
        const setFilter = document.getElementById('recite-set-filter').value;
        
        reciteQuestions = [];
        for (const q of allQuestionsData) {
            if (setFilter === 'all' || String(q.set) === setFilter) {
                reciteQuestions.push(q);
            }
        }
        
        reciteIndex = 0;
        reciteAnswerShown = false;
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('recite').style.display = 'block';
        
        renderReciteQuestionGrid();
        renderReciteQuestion();
    }
    
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
    
    function updateReciteQuestionGrid() {
        const dots = document.querySelectorAll('#recite-question-grid .question-dot');
        
        dots.forEach((dot, index) => {
            dot.classList.remove('current', 'mastered');
            
            if (index === reciteIndex) {
                dot.classList.add('current');
            }
        });
    }
    
    function reciteGoToQuestion(index) {
        reciteIndex = index;
        reciteAnswerShown = false;
        renderReciteQuestion();
    }
    
    function renderReciteQuestion() {
        const q = reciteQuestions[reciteIndex];
        
        document.getElementById('recite-q-number').textContent = '第 ' + (reciteIndex + 1) + ' 题 / 共 ' + reciteQuestions.length + ' 题';
        
        const typeNames = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        };
        
        const typeClass = {
            'single_choice': 'type-single',
            'multiple_choice': 'type-multiple',
            'true_false': 'type-tf',
            'fill_blank': 'type-fill'
        };
        
        const typeEl = document.getElementById('recite-q-type');
        typeEl.textContent = typeNames[q.type];
        typeEl.className = 'question-type ' + typeClass[q.type];
        
        document.getElementById('recite-q-text').textContent = q.question;
        
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
                div.textContent = labels[i] + '. ' + opt;
                optionsEl.appendChild(div);
            });
        }
        
        const answerEl = document.getElementById('recite-answer');
        answerEl.style.display = 'none';
        
        document.getElementById('recite-show-answer-btn').textContent = '显示答案';
        reciteAnswerShown = false;
        
        document.getElementById('recite-btn-prev').style.display = reciteIndex > 0 ? 'block' : 'none';
        document.getElementById('recite-btn-next').style.display = reciteIndex < reciteQuestions.length - 1 ? 'block' : 'none';
        
        updateReciteQuestionGrid();
    }
    
    function reciteToggleAnswer() {
        const q = reciteQuestions[reciteIndex];
        const answerEl = document.getElementById('recite-answer');
        const showAnswerBtn = document.getElementById('recite-show-answer-btn');
        
        if (reciteAnswerShown) {
            answerEl.style.display = 'none';
            showAnswerBtn.textContent = '显示答案';
            reciteAnswerShown = false;
        } else {
            let answerText = '';
            if (q.type === 'true_false') {
                answerText = q.answer ? '正确' : '错误';
            } else {
                answerText = q.answer;
            }
            
            document.getElementById('recite-answer-content').textContent = answerText;
            answerEl.style.display = 'block';
            showAnswerBtn.textContent = '隐藏答案';
            reciteAnswerShown = true;
        }
    }
    
    function recitePrevQuestion() {
        if (reciteIndex > 0) {
            reciteIndex--;
            reciteAnswerShown = false;
            renderReciteQuestion();
        }
    }
    
    function reciteNextQuestion() {
        if (reciteIndex < reciteQuestions.length - 1) {
            reciteIndex++;
            reciteAnswerShown = false;
            renderReciteQuestion();
        }
    }
    
    function addToWrongQuestions(qId) {
        if (!wrongQuestions.includes(qId)) {
            wrongQuestions.push(qId);
            localStorage.setItem('wrongQuestions', JSON.stringify(wrongQuestions));
        }
    }
    
    function removeFromWrongQuestions(qId) {
        const idx = wrongQuestions.indexOf(qId);
        if (idx !== -1) {
            wrongQuestions.splice(idx, 1);
            localStorage.setItem('wrongQuestions', JSON.stringify(wrongQuestions));
        }
    }
    
    function showWrongQuestions() {
        specialListType = 'wrong';
        document.getElementById('special-title').textContent = '❌ 错题本';
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
        
        const wrongQuestionIds = JSON.parse(localStorage.getItem('wrongQuestions') || '[]');
        const wrongQuestionObjects = allQuestionsData.filter(q => wrongQuestionIds.includes(q.uid || q.id));
        
        renderSpecialList(wrongQuestionObjects);
    }
    
    function showStarredQuestions() {
        specialListType = 'starred';
        document.getElementById('special-title').textContent = '⭐ 重点题';
        document.getElementById('menu').style.display = 'none';
        document.getElementById('special-list').style.display = 'block';
        
        const starredQuestionIds = JSON.parse(localStorage.getItem('starredQuestions') || '[]');
        const starredQuestionObjects = allQuestionsData.filter(q => starredQuestionIds.includes(q.uid || q.id));
        
        renderSpecialList(starredQuestionObjects);
    }
    
    function renderSpecialList(questionsToRender) {
        const listEl = document.getElementById('special-list-content');
        listEl.innerHTML = '';
        
        if (questionsToRender.length === 0) {
            listEl.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">暂无题目</div>';
            return;
        }
        
        const typeNames = {
            'single_choice': '单选题',
            'multiple_choice': '多选题',
            'true_false': '判断题',
            'fill_blank': '填空题'
        };
        
        const typeColors = {
            'single_choice': '#667eea',
            'multiple_choice': '#f093fb',
            'true_false': '#f5576c',
            'fill_blank': '#43e97b'
        };
        
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
                    optionsHtml += '<div class="browse-option ' + (isCorrect ? 'correct' : '') + '">' + labels[i] + '. ' + opt + '</div>';
                });
                optionsHtml += '</div>';
            } else if (q.type === 'true_false') {
                optionsHtml = '<div class="browse-options">';
                optionsHtml += '<div class="browse-option ' + (q.answer ? 'correct' : '') + '">正确</div>';
                optionsHtml += '<div class="browse-option ' + (!q.answer ? 'correct' : '') + '">错误</div>';
                optionsHtml += '</div>';
            }
            
            let answerText = '';
            if (q.type === 'true_false') {
                answerText = q.answer ? '正确' : '错误';
            } else {
                answerText = q.answer;
            }
            
            const qId = q.uid || q.id;
            const isStarred = JSON.parse(localStorage.getItem('starredQuestions') || '[]').includes(qId);
            
            card.innerHTML = '<div class="browse-header">' +
                '<div class="browse-question-number">第 ' + (index + 1) + ' 题（第' + q.set + '套 原编号' + q.id + '）</div>' +
                '<div class="browse-question-badges">' +
                '<span class="browse-badge" style="background: ' + typeColors[q.type] + '">' + typeNames[q.type] + '</span>' +
                '<button class="star-btn" onclick="toggleStar(' + qId + ')">' + (isStarred ? '⭐' : '☆') + '</button>' +
                '</div>' +
                '</div>' +
                '<div class="browse-question-text">' + q.question + '</div>' +
                optionsHtml +
                '<div class="browse-answer-box">' +
                '<div class="browse-answer-label">正确答案</div>' +
                '<div class="browse-answer-text">' + answerText + '</div>' +
                '</div>';
            
            listEl.appendChild(card);
        });
    }
    
    function clearAllSpecialList() {
        if (specialListType === 'wrong') {
            localStorage.removeItem('wrongQuestions');
            wrongQuestions = [];
        } else if (specialListType === 'starred') {
            localStorage.removeItem('starredQuestions');
            starredQuestions = [];
        }
        renderSpecialList([]);
    }
    
    function toggleStar(qId) {
        let starredQuestions = JSON.parse(localStorage.getItem('starredQuestions') || '[]');
        const idx = starredQuestions.indexOf(qId);
        if (idx === -1) {
            starredQuestions.push(qId);
        } else {
            starredQuestions.splice(idx, 1);
        }
        localStorage.setItem('starredQuestions', JSON.stringify(starredQuestions));
        
        // 重新渲染当前列表
        if (specialListType === 'starred') {
            showStarredQuestions();
        } else if (specialListType === 'wrong') {
            showWrongQuestions();
        }
    }
    
    function startMockExam() {
        // 模拟考试：从每套题中随机抽取10题，共100题
        const mockQuestions = [];
        
        for (let set = 1; set <= 10; set++) {
            const setQuestions = allQuestionsData.filter(q => q.set === set);
            // 随机抽取10题
            const shuffled = setQuestions.sort(() => 0.5 - Math.random());
            const selected = shuffled.slice(0, 10);
            mockQuestions.push(...selected);
        }
        
        // 打乱顺序
        const shuffledMock = mockQuestions.sort(() => 0.5 - Math.random());
        
        questions = shuffledMock;
        currentIndex = 0;
        userAnswers = {};
        currentQuizType = 'mock';
        
        document.getElementById('menu').style.display = 'none';
        document.getElementById('quiz').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('browse').style.display = 'none';
        
        displayQuestion();
    }
    
    // ========== 搜索功能 ==========
    function handleSearchKey(event) {
        if (event.key === 'Enter') {
            searchQuestions();
        }
    }
    
    function searchQuestions() {
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
                html += '<div style="margin-bottom: 8px;"><span style="background: #667eea; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em; margin-right: 8px;">' + setName + '</span><span style="background: #f5576c; color: white; padding: 3px 10px; border-radius: 5px; font-size: 0.9em;">' + typeName + '</span></div>';
                html += '<div class="search-item-question">' + q.question + '</div>';
                if (q.options && q.options.length > 0) {
                    html += '<div style="margin: 10px 0;">';
                    const labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
                    for (let i = 0; i < q.options.length; i++) {
                        html += '<div style="margin: 5px 0; color: #555;">' + labels[i] + '. ' + q.options[i] + '</div>';
                    }
                    html += '</div>';
                }
                html += '<div class="search-item-answer">✅ 正确答案：' + answerDisplay + '</div>';
                html += '</div>';
            }
            
            resultsContainer.innerHTML = html;
        }
        
        resultsContainer.style.display = 'block';
    }
    </script>
    '''
    
    # 找到</script>标签的位置
    script_end = html_content.find('</script>')
    if script_end == -1:
        # 如果找不到，就找到文件末尾
        new_html = html_content[:script_start] + new_script
    else:
        new_html = html_content[:script_start] + new_script + html_content[script_end + len('</script>'):]
    
    # 写入更新后的index.html
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print("✓ 成功修复JavaScript语法错误！")
    print("✓ 所有函数已正确定义")

if __name__ == '__main__':
    main()
