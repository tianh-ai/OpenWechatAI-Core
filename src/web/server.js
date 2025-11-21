import express from "express";
import cors from "cors";

export function startWebServer() {
  const app = express();
  app.use(cors());
  app.use(express.json());

  app.get("/", (req, res) => {
    res.send("OpenWechatAI-Core 管理后台（骨架版）运行正常。");
  });

  const port = 3000;
  app.listen(port, () => {
    console.log("Web 管理后台启动：http://localhost:" + port);
  });
}