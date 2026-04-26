// 数据分析模块
import { allQuestionsData } from '../data/questions.js';
import { getItem, STORAGE_KEYS } from './storage.js';
import { formatDate } from './utils.js';
import { generateStudyPlan, markPlanDayComplete } from './smart.js';

// 计算掌握程度统计
export function calculateMasteryStats() {
    const total = allQuestionsData.length;
    let mastered = 0;
    let familiar = 0;
    let unfamiliar = 0;
    
    const questionMastery = getItem(STORAGE_KEYS.QUESTION_MASTERY, {});
    
    allQuestionsData.forEach(q => {
        const qId = q.uid || q.id;
        const mastery = questionMastery[qId];
        if (!mastery) {
            unfamiliar++;
        } else {
            switch (mastery.masteryLevel) {
                case 'mastered':
                    mastered++;
                    break;
                case 'familiar':
                    familiar++;
                    break;
                case 'unfamiliar':
                    unfamiliar++;
                    break;
                default:
                    unfamiliar++;
            }
        }
    });
    
    return {
        total,
        mastered,
        familiar,
        unfamiliar,
        masteredPercentage: Math.round((mastered / total) * 100),
        familiarPercentage: Math.round((familiar / total) * 100),
        unfamiliarPercentage: Math.round((unfamiliar / total) * 100)
    };
}

// 显示掌握程度分析
export function showMasteryAnalysis() {
    // 显示掌握程度分析
    const stats = calculateMasteryStats();
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('special-list').style.display = 'block';
    document.getElementById('special-title').textContent = '📊 掌握程度分析';
    
    const contentEl = document.getElementById('special-list-content');
    
    contentEl.innerHTML = `
        <div style="padding: 20px;">
            <h3 style="text-align: center; margin-bottom: 30px;">题目掌握情况</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">${stats.total}</div>
                    <div style="color: #666;">总题目数</div>
                </div>
                <div style="background: #d4edda; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #28a745;">${stats.mastered}</div>
                    <div style="color: #666;">已掌握</div>
                </div>
                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #ffc107;">${stats.familiar}</div>
                    <div style="color: #666;">熟悉</div>
                </div>
                <div style="background: #f8d7da; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #dc3545;">${stats.unfamiliar}</div>
                    <div style="color: #666;">不熟悉</div>
                </div>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h4>掌握程度分布</h4>
                <div style="height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden;">
                    <div style="height: 100%; width: ${stats.masteredPercentage}%; background: #28a745; border-radius: 10px 0 0 10px;"></div>
                    <div style="height: 100%; width: ${stats.familiarPercentage}%; background: #ffc107;"></div>
                    <div style="height: 100%; width: ${stats.unfamiliarPercentage}%; background: #dc3545; border-radius: 0 10px 10px 0;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.9em; color: #666;">
                    <span>已掌握 ${stats.masteredPercentage}%</span>
                    <span>熟悉 ${stats.familiarPercentage}%</span>
                    <span>不熟悉 ${stats.unfamiliarPercentage}%</span>
                </div>
            </div>
            
            <div style="margin-top: 30px; text-align: center;">
                <button class="menu-btn" onclick="startSmartReview()" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer;">
                    🤖 开始智能复习
                </button>
            </div>
        </div>
    `;
}

// 获取学习统计
export function getStudyStats() {
    const studyHistory = getItem(STORAGE_KEYS.STUDY_HISTORY, []);
    
    const stats = {
        totalSessions: studyHistory.length,
        totalQuestions: 0,
        totalCorrect: 0,
        averageScore: 0,
        recentScores: [],
        dailyStats: {}
    };
    
    studyHistory.forEach(session => {
        stats.totalQuestions += session.total;
        stats.totalCorrect += session.correct;
        stats.recentScores.push((session.correct / session.total) * 100);
        
        // 按日期统计
        const date = session.timestamp.split('T')[0];
        if (!stats.dailyStats[date]) {
            stats.dailyStats[date] = {
                questions: 0,
                correct: 0
            };
        }
        stats.dailyStats[date].questions += session.total;
        stats.dailyStats[date].correct += session.correct;
    });
    
    if (stats.totalQuestions > 0) {
        stats.averageScore = Math.round((stats.totalCorrect / stats.totalQuestions) * 100);
    }
    
    return stats;
}

// 显示学习分析
export function showStudyAnalysis() {
    // 显示学习分析
    const stats = getStudyStats();
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('special-list').style.display = 'block';
    document.getElementById('special-title').textContent = '📈 学习分析';
    
    const contentEl = document.getElementById('special-list-content');
    
    contentEl.innerHTML = `
        <div style="padding: 20px;">
            <h3 style="text-align: center; margin-bottom: 30px;">学习统计</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">${stats.totalSessions}</div>
                    <div style="color: #666;">学习次数</div>
                </div>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">${stats.totalQuestions}</div>
                    <div style="color: #666;">答题总数</div>
                </div>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #28a745;">${stats.totalCorrect}</div>
                    <div style="color: #666;">正确数</div>
                </div>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #ffc107;">${stats.averageScore}%</div>
                    <div style="color: #666;">平均正确率</div>
                </div>
            </div>
            
            ${stats.recentScores.length > 0 ? `
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <h4>最近成绩</h4>
                    <div style="display: flex; align-items: end; gap: 10px; height: 200px;">
                        ${stats.recentScores.slice(-7).map((score, index) => `
                            <div style="flex: 1; display: flex; flex-direction: column; align-items: center;">
                                <div style="width: 30px; background: #667eea; border-radius: 5px 5px 0 0; transition: height 0.3s;">
                                    <div style="height: ${score}%; background: #764ba2; border-radius: 5px 5px 0 0;"></div>
                                </div>
                                <div style="margin-top: 10px; font-size: 0.8em; color: #666;">${index + 1}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <div style="margin-top: 30px; text-align: center;">
                <button class="menu-btn" onclick="backToMenu()" style="background: #6c757d; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 1em; cursor: pointer;">
                    返回菜单
                </button>
            </div>
        </div>
    `;
}

// 显示复习计划
export function showStudyPlan() {
    // 生成并显示复习计划
    const plan = generateStudyPlan();
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('special-list').style.display = 'block';
    document.getElementById('special-title').textContent = '📅 复习计划';
    
    const contentEl = document.getElementById('special-list-content');
    
    if (plan.plan.length === 0) {
        contentEl.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #999;">
                <h3>🎉 恭喜！所有题目都已掌握</h3>
                <p>无需制定复习计划</p>
            </div>
        `;
        return;
    }
    
    let planHtml = `
        <div style="padding: 20px;">
            <h3 style="text-align: center; margin-bottom: 20px;">复习计划</h3>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">共 ${plan.totalDays} 天，每天 ${plan.totalQuestions} 题</p>
            
            <div style="max-height: 600px; overflow-y: auto;">
    `;
    
    plan.plan.forEach((day, index) => {
        planHtml += `
            <div style="background: ${day.completed ? '#d4edda' : '#f8f9fa'}; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>第 ${day.day} 天 (${day.date})</h4>
                    <button onclick="markPlanDayComplete(${index})" style="background: ${day.completed ? '#6c757d' : '#28a745'}; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer;">
                        ${day.completed ? '已完成' : '标记完成'}
                    </button>
                </div>
                <p style="color: #666; margin-top: 10px;">${day.questions.length} 道题目</p>
            </div>
        `;
    });
    
    planHtml += `
            </div>
        </div>
    `;
    
    contentEl.innerHTML = planHtml;
}
