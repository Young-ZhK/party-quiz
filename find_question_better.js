const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 使用正则表达式搜索第二套的题目
const secondSetRegex = /\{"id":\d+,"set":2,"type":"[^"]+","question":"[^"]+","options":\[[^\]]+\],"answer":"[^"]+"/g;
const matches = content.match(secondSetRegex);

if (matches) {
  console.log('第二套题目数量:', matches.length);
  
  // 查找第55题（索引为54）
  if (matches[54]) {
    console.log('第二套第55题:');
    console.log(matches[54]);
  } else {
    console.log('第二套没有55题');
  }
} else {
  console.log('没有找到第二套题目');
}
