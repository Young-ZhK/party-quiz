// 本地存储模块

// 存储数据
export function setItem(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('存储数据失败:', error);
        return false;
    }
}

// 获取数据
export function getItem(key, defaultValue = null) {
    try {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : defaultValue;
    } catch (error) {
        console.error('读取数据失败:', error);
        return defaultValue;
    }
}

// 删除数据
export function removeItem(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('删除数据失败:', error);
        return false;
    }
}

// 清除所有数据
export function clear() {
    try {
        localStorage.clear();
        return true;
    } catch (error) {
        console.error('清除数据失败:', error);
        return false;
    }
}

// 存储键名常量
export const STORAGE_KEYS = {
    WRONG_QUESTIONS: 'wrongQuestions',
    STARRED_QUESTIONS: 'starredQuestions',
    QUESTION_MASTERY: 'questionMastery',
    STUDY_PLAN: 'studyPlan',
    STUDY_HISTORY: 'studyHistory'
};
