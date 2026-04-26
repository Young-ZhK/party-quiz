# 题目掌握程度评估系统设计

## 1. 评估指标

### 1.1 核心指标
- **正确率**：题目回答正确的次数占总答题次数的比例
- **答题时间**：完成题目所需的平均时间
- **连续正确次数**：连续答对同一题目的次数
- **错误率**：题目回答错误的次数占总答题次数的比例
- **复习频率**：题目被复习的频率

### 1.2 掌握程度等级
- **掌握**（Mastered）：正确率 ≥ 80%，连续正确 ≥ 3次
- **熟悉**（Familiar）：正确率 60-79%，连续正确 1-2次
- **不熟悉**（Unfamiliar）：正确率 40-59%
- **陌生**（Unknown）：正确率 < 40%

## 2. 数据结构设计

### 2.1 题目掌握数据结构
```javascript
const questionMastery = {
  [questionId]: {
    totalAttempts: 0,      // 总答题次数
    correctAttempts: 0,    // 正确次数
    consecutiveCorrect: 0, // 连续正确次数
    lastAttempt: null,     // 最后答题时间
    lastResult: null,      // 最后答题结果 (true/false)
    averageTime: 0,        // 平均答题时间（秒）
    masteryLevel: 'unknown', // 掌握程度等级
    reviewCount: 0,        // 复习次数
    lastReview: null       // 最后复习时间
  }
};
```

### 2.2 存储方式
- 使用 LocalStorage 存储题目掌握数据
- 键名：`questionMastery`
- 数据格式：JSON

## 3. 评估算法

### 3.1 实时评估
每次答题后，系统会：
1. 更新题目掌握数据
2. 重新计算掌握程度等级
3. 根据新的掌握程度更新复习优先级

### 3.2 掌握程度计算
```javascript
function calculateMasteryLevel(questionData) {
  const { totalAttempts, correctAttempts, consecutiveCorrect } = questionData;
  
  if (totalAttempts === 0) return 'unknown';
  
  const accuracy = correctAttempts / totalAttempts;
  
  if (accuracy >= 0.8 && consecutiveCorrect >= 3) {
    return 'mastered';
  } else if (accuracy >= 0.6 && consecutiveCorrect >= 1) {
    return 'familiar';
  } else if (accuracy >= 0.4) {
    return 'unfamiliar';
  } else {
    return 'unknown';
  }
}
```

### 3.3 复习优先级计算
```javascript
function calculateReviewPriority(questionData) {
  const { masteryLevel, lastAttempt, reviewCount } = questionData;
  
  let basePriority = 0;
  
  switch (masteryLevel) {
    case 'unknown': basePriority = 100;
    case 'unfamiliar': basePriority = 80;
    case 'familiar': basePriority = 50;
    case 'mastered': basePriority = 20;
  }
  
  // 考虑时间因素：越久未复习，优先级越高
  if (lastAttempt) {
    const daysSinceLastAttempt = (Date.now() - new Date(lastAttempt).getTime()) / (1000 * 60 * 60 * 24);
    basePriority += daysSinceLastAttempt * 5;
  }
  
  // 考虑复习次数：复习次数越多，优先级越低
  basePriority -= reviewCount * 3;
  
  return Math.max(0, basePriority);
}
```

## 4. 功能集成

### 4.1 与现有功能的集成
- **答题功能**：每次答题后更新掌握数据
- **错题本**：自动记录错误题目，并提高其复习优先级
- **重点题**：标记为重点的题目，增加其复习频率
- **背诵模式**：根据掌握程度调整背诵顺序

### 4.2 新功能
- **智能复习推荐**：根据掌握程度和复习优先级推荐题目
- **个性化复习计划**：基于掌握情况生成复习计划
- **学习进度分析**：展示掌握程度分布和进步趋势

## 5. 界面设计

### 5.1 掌握程度可视化
- **进度条**：显示各掌握等级的题目数量
- **热力图**：展示题目掌握情况的分布
- **雷达图**：展示不同题型的掌握情况

### 5.2 复习推荐界面
- **推荐题目列表**：按复习优先级排序
- **掌握程度筛选**：可筛选特定掌握等级的题目
- **复习计划视图**：展示每日复习任务

## 6. 实现步骤

### 6.1 数据存储初始化
1. 检查 LocalStorage 中是否存在 `questionMastery` 数据
2. 如果不存在，初始化空对象
3. 确保与现有错题本和重点题数据的兼容性

### 6.2 数据更新机制
1. 答题完成后更新掌握数据
2. 复习完成后更新复习记录
3. 定期清理过期数据

### 6.3 推荐算法实现
1. 计算所有题目的复习优先级
2. 按优先级排序生成推荐列表
3. 考虑题目类型和难度的平衡

## 7. 预期效果

通过题目掌握程度评估系统，用户将能够：
- 清晰了解自己对各题目的掌握情况
- 获得个性化的复习推荐
- 有针对性地复习不熟悉的题目
- 跟踪学习进度和掌握程度的变化
- 提高学习效率和考试通过率