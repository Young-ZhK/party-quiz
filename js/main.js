// 主模块
import { initPage, backToMenu, toggleCollapse, searchQuestions, handleSearchKey } from './ui.js';
import { startQuiz, prevQuestion, nextQuestion, submitQuiz, restartQuiz, selectSet, toggleAnswer, reviewWrongQuestions, startMockExam } from './quiz.js';
import { startBrowse, filterBrowseQuestions } from './browse.js';
import { startReciteMode, reciteGoToQuestion, reciteToggleAnswer, recitePrevQuestion, reciteNextQuestion, toggleReciteStar, prevRecite, nextRecite, toggleReciteAnswer } from './recite.js';
import { startSmartReview, startSmartReviewWrongOnly, generateStudyPlan, markPlanDayComplete } from './smart.js';
import { showMasteryAnalysis, showStudyAnalysis, showStudyPlan } from './analysis.js';
import { startImmersive, imPrevQuestion, imNextQuestion, imSubmitQuiz, imRestartQuiz } from './immersive.js';
import { showWrongQuestions, showStarredQuestions, clearAllSpecialList } from './special.js';

// 全局变量 - 定义到window对象上
window.questions = [];
window.currentIndex = 0;
window.userAnswers = {};
window.currentQuizType = 'all';
window.currentSet = 'all';
window.answerShown = false;

// 沉浸式模式变量
window.imCurrentSet = null;
window.imCurrentIndex = 0;
window.imUserAnswers = {};
window.imQuestions = [];

// 背诵模式变量
window.reciteQuestions = [];
window.reciteIndex = 0;
window.reciteAnswerShown = false;

// 特殊列表类型
window.specialListType = 'wrong';

// 导出全局函数，供HTML调用
globalThis.backToMenu = backToMenu;
globalThis.toggleCollapse = toggleCollapse;
globalThis.searchQuestions = searchQuestions;
globalThis.handleSearchKey = handleSearchKey;
globalThis.startQuiz = startQuiz;
globalThis.startMockExam = startMockExam;
globalThis.prevQuestion = prevQuestion;
globalThis.nextQuestion = nextQuestion;
globalThis.submitQuiz = submitQuiz;
globalThis.restartQuiz = restartQuiz;
globalThis.selectSet = selectSet;
globalThis.toggleAnswer = toggleAnswer;
globalThis.startBrowse = startBrowse;
globalThis.filterBrowseQuestions = filterBrowseQuestions;
globalThis.startReciteMode = startReciteMode;
globalThis.reciteGoToQuestion = reciteGoToQuestion;
globalThis.reciteToggleAnswer = reciteToggleAnswer;
globalThis.recitePrevQuestion = recitePrevQuestion;
globalThis.reciteNextQuestion = reciteNextQuestion;
globalThis.toggleReciteStar = toggleReciteStar;
globalThis.toggleReciteAnswer = toggleReciteAnswer;
globalThis.prevRecite = prevRecite;
globalThis.nextRecite = nextRecite;
globalThis.startSmartReview = startSmartReview;
globalThis.startSmartReviewWrongOnly = startSmartReviewWrongOnly;
globalThis.showMasteryAnalysis = showMasteryAnalysis;
globalThis.showStudyAnalysis = showStudyAnalysis;
globalThis.showStudyPlan = showStudyPlan;
globalThis.markPlanDayComplete = markPlanDayComplete;
globalThis.generateStudyPlan = generateStudyPlan;
globalThis.reviewWrongQuestions = reviewWrongQuestions;
globalThis.startImmersive = startImmersive;
globalThis.imPrevQuestion = imPrevQuestion;
globalThis.imNextQuestion = imNextQuestion;
globalThis.imSubmitQuiz = imSubmitQuiz;
globalThis.imRestartQuiz = imRestartQuiz;
globalThis.showWrongQuestions = showWrongQuestions;
globalThis.showStarredQuestions = showStarredQuestions;
globalThis.clearAllSpecialList = clearAllSpecialList;

// 页面加载完成后初始化
window.onload = function() {
    initPage();
};
