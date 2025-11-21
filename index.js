import { WechatBot } from "openwechat";
import { startWebServer } from "./src/web/server.js";

async function main() {
  console.log("启动 OpenWechatAI-Core（骨架版）...");

  startWebServer();

  const bot = new WechatBot({ debug: true });

  bot.on("scan", (qrcode) => {
    console.log("请扫描二维码登录：", qrcode);
  });

  bot.on("login", (user) => {
    console.log("登录成功：", user);
  });

  bot.on("message", (msg) => {
    console.log("收到消息（骨架版不处理）：", msg.content);
  });

  await bot.start();
}

main();