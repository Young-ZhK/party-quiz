// 智能复习模块
import { allQuestionsData } from '../data/questions.js';
import { getItem, setItem, STORAGE_KEYS } from './storage.js';
import { displayQuestion } from './quiz.js';
import { shuffleArray } from './utils.js';
import { PRIORITY_WEIGHTS, MASTERY_LEVELS } from './constants.js';

// 生成智能复习题目
export function generateSmartReviewQuestions() {
    // 计算需要复习的题目
    const needReviewQuestions = allQuestionsData.filter(q => {
        const qId = q.uid || q.id;
        const mastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {})[qId];
        if (!mastery) return true; // 未作答的题目
        return mastery.masteryLevel !== MASTERY_LEVELS.MASTERED; // 未掌握的题目
    });
    
    // 按复习优先级排序
    const prioritizedQuestions = needReviewQuestions.map(q => {
        const qId = q.uid || q.id;
        return {
            question: q,
            priority: calculateReviewPriority(qId)
        };
    }).sort((a, b) => b.priority - a.priority);
    
    // 为了增加随机性，对优先级相近的题目进行随机排序
    // 按优先级分组
    const priorityGroups = {};
    prioritizedQuestions.forEach(item => {
        const priority = Math.floor(item.priority);
        if (!priorityGroups[priority]) {
            priorityGroups[priority] = [];
        }
        priorityGroups[priority].push(item);
    });
    
    // 对每个优先级组内的题目进行随机排序
    const randomizedQuestions = [];
    Object.keys(priorityGroups).sort((a, b) => b - a).forEach(priority => {
        const group = priorityGroups[priority];
        // 随机打乱组内题目
        for (let i = group.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [group[i], group[j]] = [group[j], group[i]];
        }
        randomizedQuestions.push(...group);
    });
    
    // 去重并取前30题进行复习
    const uniqueQuestions = [];
    const seenIds = new Set();
    
    for (const item of randomizedQuestions) {
        const qId = item.question.uid || item.question.id;
        if (!seenIds.has(qId)) {
            seenIds.add(qId);
            uniqueQuestions.push(item.question);
            if (uniqueQuestions.length >= 30) break;
        }
    }
    
    return uniqueQuestions;
}

// 计算复习优先级
function calculateReviewPriority(qId) {
    const mastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {})[qId];
    if (!mastery) return 10; // 未作答的题目优先级最高
    
    let priority = 0;
    
    // 基于掌握程度
    if (mastery.masteryLevel === MASTERY_LEVELS.UNFAMILIAR) priority += PRIORITY_WEIGHTS.UNFAMILIAR;
    else if (mastery.masteryLevel === MASTERY_LEVELS.FAMILIAR) priority += PRIORITY_WEIGHTS.FAMILIAR;
    
    // 基于错误次数
    const wrongCount = mastery.totalAttempts - mastery.correctAttempts;
    priority += wrongCount * PRIORITY_WEIGHTS.WRONG_COUNT;
    
    // 基于时间间隔
    if (mastery.lastAttempt) {
        const daysSinceLast = (Date.now() - new Date(mastery.lastAttempt).getTime()) / (1000 * 60 * 60 * 24);
        priority += Math.min(daysSinceLast, PRIORITY_WEIGHTS.MAX_DAYS);
    }
    
    return priority;
}

// 开始智能复习
export function startSmartReview() {
    // 基于掌握程度生成智能复习题目
    const reviewQuestions = generateSmartReviewQuestions();
    
    if (reviewQuestions.length === 0) {
        alert('🎉 恭喜！所有题目都已掌握，无需复习！');
        return;
    }
    
    // 开始复习
    window.questions = reviewQuestions;
    window.currentIndex = 0;
    window.userAnswers = {};
    window.currentQuizType = 'smart';
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    
    displayQuestion();
}

// 仅复习错题
export function startSmartReviewWrongOnly() {
    // 仅复习错题
    const wrongQuestionIds = getItem(STORAGE_KEYS.WRONG_QUESTIONS, []);
    const wrongQuestions = allQuestionsData.filter(q => wrongQuestionIds.includes(q.uid || q.id));
    
    if (wrongQuestions.length === 0) {
        alert('🎉 恭喜！没有错题需要复习！');
        return;
    }
    
    // 开始复习
    window.questions = wrongQuestions;
    window.currentIndex = 0;
    window.userAnswers = {};
    window.currentQuizType = 'smart';
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('quiz').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    document.getElementById('browse').style.display = 'none';
    
    displayQuestion();
}

// 生成复习计划
export function generateStudyPlan() {
    // 计算需要复习的题目
    const needReviewQuestions = allQuestionsData.filter(q => {
        const qId = q.uid || q.id;
        const mastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {})[qId];
        if (!mastery) return true; // 未作答的题目
        return mastery.masteryLevel !== MASTERY_LEVELS.MASTERED; // 未掌握的题目
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
    
    const studyPlan = {
        generatedAt: new Date().toISOString(),
        totalDays: days,
        totalQuestions: prioritizedQuestions.length,
        plan: plan
    };
    
    setItem(STORAGE_KEYS.STUDY_PLAN, studyPlan);
    return studyPlan;
}

// 标记计划完成
export function markPlanDayComplete(dayIndex) {
    const studyPlan = getItem(STORAGE_KEYS.STUDY_PLAN, {});
    if (studyPlan.plan && studyPlan.plan[dayIndex]) {
        studyPlan.plan[dayIndex].completed = true;
        setItem(STORAGE_KEYS.STUDY_PLAN, studyPlan);
    }
}

// 获取今日学习计划
export function getTodayStudyPlan() {
    const studyPlan = getItem(STORAGE_KEYS.STUDY_PLAN, {});
    if (!studyPlan.plan || studyPlan.plan.length === 0) {
        return null;
    }
    
    const today = new Date().toISOString().split('T')[0];
    return studyPlan.plan.find(day => day.date === today) || 
           studyPlan.plan.find(day => !day.completed);
}

// 更新题目掌握程度
export function updateQuestionMastery(qId, isCorrect, timeSpent = 0) {
    const questionMastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {});
    
    if (!questionMastery[qId]) {
        questionMastery[qId] = {
            totalAttempts: 0,
            correctAttempts: 0,
            consecutiveCorrect: 0,
            lastAttempt: null,
            lastResult: null,
            averageTime: 0,
            masteryLevel: MASTERY_LEVELS.UNKNOWN,
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
        mastery.masteryLevel = MASTERY_LEVELS.MASTERED;
    } else if (mastery.correctAttempts >= mastery.totalAttempts / 2) {
        mastery.masteryLevel = MASTERY_LEVELS.FAMILIAR;
    } else {
        mastery.masteryLevel = MASTERY_LEVELS.UNFAMILIAR;
    }
    
    setItem(STORAGE_KEYS.QUESTION_MASTERY, questionMastery);
}
