const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 找到allQuestionsData的定义
const startIndex = content.indexOf('const allQuestionsData =');
const endIndex = content.indexOf(';', startIndex);

if (startIndex !== -1 && endIndex !== -1) {
    // 提取JSON字符串
    const jsonStr = content.substring(startIndex + 22, endIndex);
    
    try {
        // 解析JSON
        const questions = JSON.parse(jsonStr);
        
        // 找到第二套第55题
        const targetQuestion = questions.find(q => q.id === 155 && q.set === 2);
        
        if (targetQuestion) {
            console.log('找到题目:', targetQuestion);
            
            // 修复选项
            targetQuestion.question = '新时代十年的伟大变革，在（）上具有里程碑意义。';
            targetQuestion.options = ['党史', '新中国史', '改革开放史', '社会主义发展史', '中华民族发展史'];
            targetQuestion.answer = 'ABCDE';
            targetQuestion.explanation = '';
            targetQuestion.uid = 155;
            
            console.log('修复后的题目:', targetQuestion);
            
            // 将修复后的数据转换回字符串
            const updatedJsonStr = JSON.stringify(questions);
            
            // 替换原文件中的数据
            const updatedContent = content.replace(jsonStr, updatedJsonStr);
            
            // 保存修复后的文件
            fs.writeFileSync('index.html', updatedContent);
            console.log('已修复第二套第55题的选项问题');
        } else {
            console.log('未找到第二套第55题');
        }
    } catch (error) {
        console.error('解析JSON时出错:', error);
    }
} else {
    console.log('未找到allQuestionsData的定义');
}
