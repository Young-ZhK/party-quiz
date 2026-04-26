// 题目数据模块

// 导出题目数据
export const allQuestionsData = [];

// 加载题目数据
async function loadQuestions() {
    try {
        const response = await fetch('./data/questions.json');
        const data = await response.json();
        allQuestionsData.splice(0, allQuestionsData.length, ...data);
        console.log('Loaded', allQuestionsData.length, 'questions');
    } catch (error) {
        console.error('Failed to load questions:', error);
    }
}

// 自动加载题目数据
loadQuestions();

// 获取指定套的题目
export function getQuestionsBySet(set) {
    return allQuestionsData.filter(q => q.set === parseInt(set));
}

// 获取指定类型的题目
export function getQuestionsByType(type) {
    return allQuestionsData.filter(q => q.type === type);
}

// 根据ID获取题目
export function getQuestionById(id) {
    return allQuestionsData.find(q => q.id === parseInt(id) || q.uid === parseInt(id));
}

// 获取题目总数
export function getTotalQuestions() {
    return allQuestionsData.length;
}

// 获取每套题的数量
export function getQuestionsCountBySet() {
    const counts = {};
    allQuestionsData.forEach(q => {
        counts[q.set] = (counts[q.set] || 0) + 1;
    });
    return counts;
}
