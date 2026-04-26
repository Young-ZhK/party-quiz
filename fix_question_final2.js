const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 查找第二套第55题的正则表达式
const regex = /\{"id":155,"set":2,"type":"multiple_choice","question":"[^"]*","options":\[[^\]]*\],"answer":"ABCDE"/;

// 检查是否找到匹配
const match = content.match(regex);
if (match) {
    console.log('找到题目:', match[0]);
    
    // 替换为修复后的题目，确保选项格式正确
    const fixedContent = content.replace(regex, '{"id":155,"set":2,"type":"multiple_choice","question":"新时代十年的伟大变革，在（）上具有里程碑意义。","options":["党史","新中国史","改革开放史","社会主义发展史","中华民族发展史"],"answer":"ABCDE","explanation":"","uid":155}');
    
    // 保存修复后的文件
    fs.writeFileSync('index.html', fixedContent);
    console.log('已修复第二套第55题的选项问题');
} else {
    console.log('未找到题目');
}
