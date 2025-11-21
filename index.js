import { WechatyBuilder } from "wechaty";
import { startWebServer } from "./src/web/server.js";
import cron from "cron";
import fs from "fs";
import path from "path";
import axios from "axios";
import { SummaryManager } from "./src/modules/summaryManager.js";
import qrTerm from "qrcode-terminal";

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

  const options = {
    name: "OpenWechatAI-Core"
  };

  const bot = WechatyBuilder.build(options);

  bot.on("scan", (qrcode, status) => {
    console.log("请扫描二维码登录：");
    console.log("二维码状态:", status);
    // 使用简单的文本输出二维码URL
    const qrcodeUrl = "https://wechaty.js.org/qrcode/" + encodeURIComponent(qrcode);
    console.log("如果二维码显示不正常，请访问以下链接：");
    console.log(qrcodeUrl);
    // 同时显示二维码
    qrTerm.generate(qrcode, { small: true });
  });

  bot.on("login", (user) => {
    console.log("登录成功：", user.name());
    // 登录后显示群组信息
    setTimeout(async () => {
      const rooms = await bot.Room.findAll();
      console.log("\n=== 您加入的微信群组 ===");
      for (const room of rooms) {
        const topic = await room.topic();
        console.log(`群组名称: ${topic}`);
        console.log(`群组ID: ${room.id}`);
        console.log("---");
      }
      console.log("请将需要的群组ID添加到配置文件中\n");
    }, 3000);
  });

  bot.on("logout", (user) => {
    console.log("登出：", user.name());
  });

  bot.on("message", async (msg) => {
    const text = msg.text();
    const talker = msg.talker();
    const senderName = talker.name();
    const senderId = talker.id;
    const room = msg.room();
    const groupId = room ? room.id : null;
    const groupName = room ? await room.topic() : null;

    // 处理特殊命令
    if (text === "群组列表") {
      const rooms = await bot.Room.findAll();
      let reply = "=== 您加入的微信群组 ===\n";
      for (const room of rooms) {
        const topic = await room.topic();
        reply += `群组名称: ${topic}\n`;
        reply += `群组ID: ${room.id}\n---\n`;
      }
      await msg.say(reply);
      return;
    }

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

  // ===== 每日自动生成日报 =====
  const [hour, minute] = (config.dailySummaryTime || "18:00").split(":");

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