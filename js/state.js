// 状态管理模块

// 答题状态
export let questions = [];
export let currentIndex = 0;
export let userAnswers = {};
export let currentQuizType = 'all';
export let currentSet = 'all';
export let answerShown = false;

// 沉浸式模式状态
export let imCurrentSet = null;
export let imCurrentIndex = 0;
export let imUserAnswers = {};
export let imQuestions = [];

// 背诵模式状态
export let reciteQuestions = [];
export let reciteIndex = 0;
export let reciteAnswerShown = false;

// 特殊列表类型
export let specialListType = 'wrong';

// 重置答题状态
export function resetQuizState() {
    questions = [];
    currentIndex = 0;
    userAnswers = {};
    currentQuizType = 'all';
    currentSet = 'all';
    answerShown = false;
}

// 重置背诵状态
export function resetReciteState() {
    reciteQuestions = [];
    reciteIndex = 0;
    reciteAnswerShown = false;
}

// 重置沉浸式模式状态
export function resetImmersiveState() {
    imCurrentSet = null;
    imCurrentIndex = 0;
    imUserAnswers = {};
    imQuestions = [];
}
