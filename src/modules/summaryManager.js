import fs from "fs";
import path from "path";

const __dirname = path.resolve();

export const SummaryManager = {

  collect(dailyLogs) {
    let result = {};
    for (const [uid, info] of Object.entries(dailyLogs.members || {})) {
      const text = (info.messages || [])
        .map(m => m.text)
        .join("\n");

      result[uid] = {
        name: info.name || uid,
        text
      };
    }
    return result;
  },

  async generateDailyReport(aiFunc, dailyLogs) {
    const collected = this.collect(dailyLogs);
    let final = {};

    for (const [uid, item] of Object.entries(collected)) {
      const prompt = `
你是一名工程项目AI助手，请根据以下聊天内容生成【工作日报】：

要求：
1. 今日完成内容（重点）
2. 遇到的问题/风险
3. 沟通情况
4. 明日计划（如可判断）

聊天内容：
${item.text}
`;

      const summary = await aiFunc(prompt, "summary");
      final[uid] = {
        name: item.name,
        summary
      };
    }
    return final;
  },

  saveDailyReport(report) {
    const day = new Date().toISOString().slice(0,10);
    const file = path.join(__dirname, "data/dailyReports", day + ".json");
    fs.writeFileSync(file, JSON.stringify(report, null, 2));
    return file;
  }
};