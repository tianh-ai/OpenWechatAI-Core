# OpenWechatAI-Core

这是一个基于 OpenWechat 的微信智能项目管理机器人内核，含：

- 日报系统（自动生成 + 自动微信推送）
- Web 管理后台
- 任务管理模块（骨架）
- 材料管理模块（骨架）
- 总结管理模块（含AI日报）
- 图片管理模块（骨架）
- JSON 数据库

运行方式：

```bash
npm install
npm start
```

后台访问：

http://localhost:3000

默认每日 18:00 自动生成日报并推送到配置的微信群。