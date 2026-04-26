const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 提取allQuestionsData数组
const dataMatch = content.match(/const allQuestionsData =\[([\s\S]*?)\];/);
if (dataMatch) {
  try {
    // 解析数据
    const data = JSON.parse('[' + dataMatch[1] + ']');
    
    // 筛选第二套的题目
    const secondSetQuestions = data.filter(q => q.set === 2);
    
    console.log('第二套题目数量:', secondSetQuestions.length);
    
    // 查找第55题（索引为54）
    if (secondSetQuestions[54]) {
      const question = secondSetQuestions[54];
      console.log('第二套第55题:');
      console.log('题目:', question.question);
      console.log('选项:', question.options);
      console.log('答案:', question.answer);
      console.log('类型:', question.type);
    } else {
      console.log('第二套没有55题');
      // 显示所有第二套题目
      console.log('第二套所有题目:');
      secondSetQuestions.forEach((q, index) => {
        console.log(`第${index + 1}题: ${q.question.substring(0, 50)}...`);
      });
    }
  } catch (error) {
    console.error('解析数据失败:', error);
  }
} else {
  console.error('没有找到题目数据');
}
