import { WechatBot } from "openwechat";
import { startWebServer } from "./src/web/server.js";
import cron from "cron";
import fs from "fs";
import path from "path";
import axios from "axios";
import { SummaryManager } from "./src/modules/summaryManager.js";

const __dirname = path.resolve();

function loadJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(path.join(__dirname, file))); }
  catch { return fallback; }
}
function saveJson(file, data) {
  fs.writeFileSync(path.join(__dirname, file), JSON.stringify(data, null, 2));
}

let config = loadJson("src/config/config.json", {});
let access = loadJson("src/core/access.json", {});
let dailyLogs = loadJson("data/dailyLogs.json", { members: {} });

// AI封装
async function ai(prompt, mode="summary") {
  if (!config.apiKey) return "(AI API Key 未配置)";
  const res = await axios.post(
    "https://api.deepseek.com/v1/chat/completions",
    {
      model: "deepseek-chat",
      messages: [{ role:"user", content: prompt }]
    },
    { headers: { Authorization: `Bearer ${config.apiKey}` } }
  );
  return res.data.choices[0].message.content;
}

async function main() {
  console.log("启动 OpenWechatAI-Core（含日报系统）...");

  startWebServer();

  const bot = new WechatBot({ debug: true });

  bot.on("scan", (qrcode) => {
    console.log("请扫描二维码登录：", qrcode);
  });

  bot.on("login", (user) => {
    console.log("登录成功：", user);
  });

  bot.on("message", async (msg) => {
    const text = msg.content || "";
    const talker = msg.talker();
    const senderName = talker ? talker.name() : "";
    const senderId = talker ? talker.id : "";
    const room = msg.room();
    const groupId = room ? room.id : null;
    const groupName = room ? await room.topic() : null;

    if (!senderId) return;

    // 群白名单校验
    if (groupId && !access.groupWhitelist.includes(groupId)) return;

    // 收集聊天日志
    if (!dailyLogs.members[senderId]) {
      dailyLogs.members[senderId] = { name: senderName, messages: [] };
    }
    dailyLogs.members[senderId].messages.push({
      text,
      groupId,
      groupName,
      time: new Date().toISOString()
    });
    saveJson("data/dailyLogs.json", dailyLogs);
  });

  // ===== 每日 18:00 自动生成日报 =====
  const [hour, minute] = "18:00".split(":");

  new cron.CronJob(`${minute} ${hour} * * *`, async () => {
    console.log("🟦 开始生成当日工作日报 ...");

    try {
      const report = await SummaryManager.generateDailyReport(ai, dailyLogs);

      const savedPath = SummaryManager.saveDailyReport(report);
      console.log("日报已保存到：", savedPath);

      // 推送内容
      let message = "【今日工作日报】\n";
      for (const [uid, item] of Object.entries(report)) {
        message += "\n-------------------------------------\n";
        message += `👤 ${item.name}\n`;
        message += item.summary + "\n";
      }

      // 推送到微信
      if (config.reportTargetType === "group" && config.reportTargetId) {
        const room = await bot.Room.find({ id: config.reportTargetId });
        if (room) {
          await room.say(message);
          console.log("📤 日报已推送到微信群：", config.reportTargetId);
        } else {
          console.log("❌ 找不到微信群，请检查 reportTargetId");
        }
      }

    } catch (e) {
      console.error("日报生成失败：", e);
    }

    dailyLogs = { members: {} };
    saveJson("data/dailyLogs.json", dailyLogs);

  }, null, true, "Asia/Shanghai");

  await bot.start();
}

main();