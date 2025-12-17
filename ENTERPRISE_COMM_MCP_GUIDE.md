# 企业通信MCP - 完整解决方案

## 🎯 项目概述

本项目提供了一个**统一的企业通信MCP服务**，可以同时管理和集成：
- 企业微信
- 飞书  
- 钉钉

支持通过**Web界面配置**或**API后端配置**，实现消息的接收和自动回复。

---

## 📁 项目结构

```
OpenWechatAI-Core/
├── enterprise_comm_mcp/          # 企业通信MCP模块
│   ├── mcp_server.py            # MCP服务器（Flask）
│   ├── feishu_bot.py            # 飞书机器人实现
│   ├── dingtalk_bot.py          # 钉钉机器人实现
│   ├── config.yaml              # 配置文件
│   ├── config.yaml.example      # 配置文件模板
│   ├── start.sh                 # 快速启动脚本
│   ├── README.md                # 详细文档
│   └── static/
│       └── config.html          # Web配置界面
│
├── wework_bot.py                # 企业微信机器人（根目录）
├── wework_server.py             # 企业微信服务器（根目录）
│
├── wechat_auto_reply.py         # 个人微信自动回复（手机方案）
├── wechat_sender.py             # 微信发送模块
├── wechat_receiver.py           # 微信接收模块
├── message_ocr.py               # OCR识别模块
├── docker_ocr_adapter.py        # Docker OCR适配器
├── reply_rule_engine.py         # 回复规则引擎
│
├── config/
│   ├── reply_rules.yaml         # 自动回复规则配置
│   └── app_config.yaml          # 应用配置
│
└── docs/
    └── WEWORK_BOT_GUIDE.md      # 企业微信机器人指南
```

---

## 🚀 快速开始

### 方式1: 使用启动脚本（推荐）

```bash
# 给脚本添加执行权限（首次）
chmod +x enterprise_comm_mcp/start.sh

# 运行启动脚本
./enterprise_comm_mcp/start.sh
```

然后选择：
1. 启动MCP服务器（后台运行）
2. 启动MCP服务器（前台运行）
3. 打开Web配置界面
4. 测试配置
5. 查看服务状态
6. 停止服务

### 方式2: 手动启动

```bash
# 1. 安装依赖
pip install flask pyyaml requests WechatPyCrypto

# 2. 复制配置文件
cd enterprise_comm_mcp
cp config.yaml.example config.yaml

# 3. 编辑配置（或使用Web界面）
vim config.yaml

# 4. 启动服务
python mcp_server.py
```

### 方式3: Web配置（最简单）

```bash
# 1. 启动服务器
cd enterprise_comm_mcp
python mcp_server.py

# 2. 浏览器打开
http://localhost:8000/static/config.html

# 3. 在Web界面中配置各平台参数
# 4. 点击"保存配置"
# 5. 点击"测试发送"验证
```

---

## 📋 两种方案对比

### 方案A: 个人微信（手机方案）

**特点：**
- ✅ 支持个人微信
- ❌ **需要手机**
- ❌ 使用截屏+OCR识别
- ❌ 准确率70-90%
- ❌ 需要手机一直运行

**适用场景：**
- 个人微信自动回复
- 没有企业微信/飞书/钉钉账号

**使用方法：**
```bash
python wechat_auto_reply.py --interval 3 --ocr --ocr-engine docker
```

### 方案B: 企业通信MCP（API方案）⭐推荐

**特点：**
- ✅ 支持企业微信、飞书、钉钉
- ✅ **完全不需要手机**
- ✅ 使用官方HTTP API
- ✅ 准确率100%
- ✅ 稳定可靠
- ✅ 官方支持
- ✅ Web界面配置

**适用场景：**
- 企业微信/飞书/钉钉自动回复
- 企业客服机器人
- 工单处理系统
- 通知推送系统

**使用方法：**
```bash
cd enterprise_comm_mcp
python mcp_server.py
```

---

## 🔧 配置示例

### 企业微信配置

```yaml
wework:
  enabled: true
  type: webhook  # 或 app
  webhook_url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

### 飞书配置

```yaml
feishu:
  enabled: true
  type: webhook  # 或 app
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
  secret: "your_secret"
```

### 钉钉配置

```yaml
dingtalk:
  enabled: true
  type: webhook  # 或 app
  webhook_url: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  secret: "your_secret"
```

---

## 🌐 API使用

### 发送消息

```bash
# 发送到企业微信
curl -X POST http://localhost:8000/api/send/wework \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'

# 发送到飞书
curl -X POST http://localhost:8000/api/send/feishu \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'

# 发送到钉钉
curl -X POST http://localhost:8000/api/send/dingtalk \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'
```

### 配置管理

```bash
# 获取所有配置
curl http://localhost:8000/api/config

# 更新企业微信配置
curl -X POST http://localhost:8000/api/config/wework \
  -H 'Content-Type: application/json' \
  -d '{
    "enabled": true,
    "type": "webhook",
    "webhook_url": "https://..."
  }'

# 获取系统状态
curl http://localhost:8000/api/status
```

### Python调用

```python
import requests

# 发送消息
response = requests.post(
    'http://localhost:8000/api/send/wework',
    json={'content': '测试消息'}
)
print(response.json())

# 更新配置
response = requests.post(
    'http://localhost:8000/api/config/feishu',
    json={
        'enabled': True,
        'type': 'webhook',
        'webhook_url': 'https://...',
        'secret': 'xxx'
    }
)
print(response.json())
```

---

## 📚 相关文档

- [企业通信MCP详细文档](enterprise_comm_mcp/README.md)
- [企业微信机器人指南](docs/WEWORK_BOT_GUIDE.md)
- [飞书开放平台文档](https://open.feishu.cn/document/)
- [钉钉开放平台文档](https://open.dingtalk.com/document/)
- [企业微信API文档](https://developer.work.weixin.qq.com/document/)

---

## 🎁 核心功能

### 1. 统一配置管理
- Web界面可视化配置
- API后端配置
- YAML文件配置
- 热重载（无需重启）

### 2. 多平台支持
- 企业微信（Webhook + 企业应用）
- 飞书（Webhook + 自建应用）
- 钉钉（Webhook + 企业应用）

### 3. 自动回复
- 基于规则引擎
- 支持关键词匹配
- 支持正则表达式
- 支持时间段规则
- 可配置回复延迟

### 4. 消息推送
- 统一API接口
- 支持文本消息
- 支持富文本消息
- 支持卡片消息
- 支持@功能

### 5. 系统监控
- 健康检查接口
- 状态监控
- 日志记录
- 错误追踪

---

## 🔒 安全建议

1. **生产环境使用HTTPS**
2. **启用各平台的签名验证**
3. **配置API密钥验证**
4. **设置IP白名单**
5. **定期更新密钥**

---

## 🚀 部署建议

### 开发环境
```bash
python mcp_server.py
```

### 生产环境
```bash
# 使用Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 mcp_server:app

# 或使用Docker
docker build -t enterprise-comm-mcp .
docker run -p 8000:8000 enterprise-comm-mcp
```

---

## 💡 使用建议

| 场景 | 推荐方案 |
|-----|---------|
| 个人微信自动回复 | 手机方案 |
| 企业微信自动回复 | MCP API方案 |
| 飞书自动回复 | MCP API方案 |
| 钉钉自动回复 | MCP API方案 |
| 多平台统一管理 | MCP API方案 |
| 通知推送 | MCP Webhook方案 |
| 智能客服 | MCP 应用方案 |

---

## 📞 支持

如有问题，请查看：
1. [详细文档](enterprise_comm_mcp/README.md)
2. [企业微信指南](docs/WEWORK_BOT_GUIDE.md)
3. 官方API文档
4. 提交Issue

---

## 📄 许可证

MIT License
