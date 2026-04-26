const fs = require('fs');

// 读取index.html文件
const content = fs.readFileSync('index.html', 'utf8');

// 找到第二套第55题并修复选项
const fixedContent = content.replace(
  /\{"id":155,"set":2,"type":"multiple_choice","question":"鏂版椂浠ｅ崄骞寸殑浼熷ぇ 鍙橀潻锛屽湪锛堬級涓婂叿鏈夐噷绋嬬鎰忎箟銆?,","options":\["鍏氬彶","鏂颁腑鍥藉彶","鏀归潻寮€鏀惧彶","绀句細涓讳箟鍙戝睍鍙?E銆佷腑鍗庢皯鏃忓彂灞曞彶"\],"answer":"ABCDE"/,
  '{"id":155,"set":2,"type":"multiple_choice","question":"新时代十年的伟大变革，在（）上具有里程碑意义。","options":["党史","新中国史","改革开放史","社会主义发展史","中华民族发展史"],"answer":"ABCDE","explanation":"","uid":155}'
);

// 保存修复后的文件
fs.writeFileSync('index.html', fixedContent);

console.log('已修复第二套第55题的选项问题');
