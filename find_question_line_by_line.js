const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 逐行搜索第二套第55题
const lines = content.split('\n');
let setCount = 0;
let questionCount = 0;
let found = false;

for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 检查是否是第二套的题目
    if (line.includes('"set":2')) {
        questionCount++;
        
        // 检查是否是第55题
        if (questionCount === 55) {
            console.log('第二套第55题在第', i + 1, '行:');
            // 打印周围的行
            for (let j = Math.max(0, i - 2); j <= Math.min(lines.length - 1, i + 10); j++) {
                console.log(j + 1, ':', lines[j]);
            }
            found = true;
            break;
        }
    }
}

if (!found) {
    console.log('未找到第二套第55题');
}
