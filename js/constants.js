// 常量定义模块

// 题目类型
export const QUESTION_TYPES = {
    SINGLE_CHOICE: 'single_choice',
    MULTIPLE_CHOICE: 'multiple_choice',
    TRUE_FALSE: 'true_false',
    FILL_BLANK: 'fill_blank'
};

// 题目类型名称
export const QUESTION_TYPE_NAMES = {
    'single_choice': '单选题',
    'multiple_choice': '多选题',
    'true_false': '判断题',
    'fill_blank': '填空题'
};

// 题目类型样式类
export const QUESTION_TYPE_CLASSES = {
    'single_choice': 'type-single',
    'multiple_choice': 'type-multiple',
    'true_false': 'type-tf',
    'fill_blank': 'type-fill'
};

// 题目类型颜色
export const QUESTION_TYPE_COLORS = {
    'single_choice': '#667eea',
    'multiple_choice': '#f093fb',
    'true_false': '#f5576c',
    'fill_blank': '#43e97b'
};

// 套数名称
export const SET_NAMES = {
    1: '第一套', 2: '第二套', 3: '第三套', 4: '第四套',
    5: '第五套', 6: '第六套', 7: '第七套', 8: '第八套', 9: '第九套', 10: '第十套'
};

// 掌握程度
export const MASTERY_LEVELS = {
    MASTERED: 'mastered',
    FAMILIAR: 'familiar',
    UNFAMILIAR: 'unfamiliar',
    UNKNOWN: 'unknown'
};

// 复习优先级权重
export const PRIORITY_WEIGHTS = {
    UNFAMILIAR: 8,
    FAMILIAR: 4,
    WRONG_COUNT: 2,
    MAX_DAYS: 5
};
