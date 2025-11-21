import fs from "fs";
import path from "path";

const __dirname = path.resolve();

export const SummaryManager = {
  collect() {},
  generate() {},
  
  // 新增日报生成功能
  async generateDailyReport(ai, dailyLogs) {
    const report = {};
    
    for (const [uid, member] of Object.entries(dailyLogs.members)) {
      // 构造AI提示词
      let prompt = `请为以下员工生成今日工作日报总结，要求专业、简洁、突出重点：
员工姓名：${member.name}
今日聊天记录：
`;
      
      // 添加聊天记录
      for (const msg of member.messages) {
        prompt += `- ${msg.text}\n`;
      }
      
      // 调用AI生成总结
      const summary = await ai(prompt);
      
      report[uid] = {
        name: member.name,
        summary: summary
      };
    }
    
    return report;
  },
  
  // 保存日报到文件
  saveDailyReport(report) {
    const dateStr = new Date().toISOString().split('T')[0];
    const filename = `report-${dateStr}.json`;
    const filepath = path.join(__dirname, 'data', 'dailyReports', filename);
    
    // 确保目录存在
    const dir = path.dirname(filepath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(filepath, JSON.stringify(report, null, 2));
    return filepath;
  }
};