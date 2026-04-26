const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 搜索第二套的题目
const secondSetMatches = content.match(/\{"id":\d+,"set":2,"type":"[^"]+","question":"[^"]+","options":\[[^\]]+\],"answer":"[^"]+"/g);

if (secondSetMatches) {
  console.log('第二套题目数量:', secondSetMatches.length);
  
  // 查找第55题（索引为54）
  if (secondSetMatches[54]) {
    const questionStr = secondSetMatches[54];
    console.log('第二套第55题:');
    console.log(questionStr);
    
    // 提取题目、选项和答案
    const questionMatch = questionStr.match(/"question":"([^"]+)"/);
    const optionsMatch = questionStr.match(/"options":\[([^\]]+)\]/);
    const answerMatch = questionStr.match(/"answer":"([^"]+)"/);
    
    if (questionMatch) console.log('题目:', questionMatch[1]);
    if (optionsMatch) console.log('选项:', optionsMatch[1]);
    if (answerMatch) console.log('答案:', answerMatch[1]);
  } else {
    console.log('第二套没有55题');
    console.log('第二套实际有', secondSetMatches.length, '题');
  }
} else {
  console.error('没有找到第二套题目');
}
