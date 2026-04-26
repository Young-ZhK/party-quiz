const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 搜索第二套的题目
let count = 0;
let inSecondSet = false;
let currentQuestion = '';

const lines = content.split('\n');
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  
  if (line.includes('"set":2')) {
    inSecondSet = true;
    count++;
    currentQuestion = line;
    
    // 收集题目信息
    for (let j = i + 1; j < lines.length; j++) {
      const nextLine = lines[j];
      currentQuestion += nextLine;
      if (nextLine.includes('"uid":')) {
        break;
      }
    }
    
    // 检查是否是第55题
    if (count === 55) {
      console.log('第二套第55题:');
      console.log(currentQuestion);
      break;
    }
  } else if (inSecondSet && line.includes('"set":') && !line.includes('"set":2')) {
    inSecondSet = false;
  }
}

if (count < 55) {
  console.log('第二套没有55题，只有', count, '题');
}
