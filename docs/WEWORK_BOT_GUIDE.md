# 企业微信机器人使用指南

## 🎯 核心优势

✅ **完全不需要手机**  
✅ **不需要截屏OCR**  
✅ **直接HTTP API调用**  
✅ **官方支持，稳定可靠**  

---

## 📋 两种实现方式对比

### 方式1: 群机器人（Webhook）

**特点：**
- ✅ 配置极简单（5分钟搞定）
- ✅ 不需要服务器
- ❌ 只能发送，不能接收
- 📝 适合：通知、告警、单向推送

**使用场景：**
```python
# 系统告警通知
# 定时报表推送
# 任务完成提醒
```

**配置步骤：**
1. 企业微信群 → 群设置 → 群机器人 → 添加
2. 复制 Webhook URL
3. 使用代码发送消息

**代码示例：**
```python
from wework_bot import WeWorkWebhookBot

webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
bot = WeWorkWebhookBot(webhook_url)

# 发送文本
bot.send_text("测试消息")

# @指定成员
bot.send_text("重要通知", mentioned_list=["userid1", "@all"])

# 发送Markdown
bot.send_markdown("### 标题\n- 列表1\n- 列表2")
```

---

### 方式2: 应用机器人（推荐）

**特点：**
- ✅ 可以接收消息
- ✅ 可以自动回复
- ✅ 支持所有消息类型
- ✅ 可以获取通讯录
- 🔧 需要配置回调服务器

**使用场景：**
```python
# 智能客服机器人
# 自动问答系统
# 工单处理系统
# 智能助手
```

**配置步骤：**

#### 1. 创建企业微信应用
```
1. 登录企业微信管理后台
   https://work.weixin.qq.com/

2. 应用管理 → 应用 → 创建应用
   - 设置应用名称、Logo
   - 记录 AgentId

3. 应用详情页面
   - 记录 Secret（点击查看）
   - 配置可见范围（哪些成员可以使用）
```

#### 2. 获取企业ID
```
我的企业 → 企业信息 → 企业ID
复制 CorpId
```

#### 3. 配置接收消息
```
应用详情 → 接收消息 → 设置API接收

URL: https://your-domain.com/wework/callback
Token: 随机字符串（自己设置，如：abc123）
EncodingAESKey: 点击"随机生成"

点击"保存" → 企业微信会验证URL
```

#### 4. 配置环境变量
```bash
# 复制配置文件
cp .env.wework.example .env.wework

# 编辑配置
vim .env.wework
```

填入：
```env
WEWORK_CORP_ID=ww1234567890abcdef
WEWORK_CORP_SECRET=your_secret_here
WEWORK_AGENT_ID=1000001
WEWORK_TOKEN=abc123
WEWORK_ENCODING_AES_KEY=your_aes_key_here
```

#### 5. 安装依赖
```bash
pip install flask
pip install WechatPyCrypto  # 消息加解密库
```

#### 6. 启动服务器
```bash
# 加载环境变量并启动
source .env.wework
python wework_server.py
```

#### 7. 配置公网访问（重要！）

企业微信需要能访问你的回调URL，有几种方案：

**方案A: 使用云服务器**
```bash
# 购买阿里云/腾讯云服务器
# 部署服务，配置域名和HTTPS
# 推荐使用 gunicorn + nginx
```

**方案B: 内网穿透（测试用）**
```bash
# 使用 ngrok
ngrok http 5000

# 或使用 natapp
# https://natapp.cn/
```

**方案C: 使用Serverless**
```bash
# 部署到腾讯云函数/阿里云函数计算
# 自动获得公网访问能力
```

---

## 🚀 快速开始

### 测试群机器人
```bash
python -c "
from wework_bot import WeWorkWebhookBot
bot = WeWorkWebhookBot('YOUR_WEBHOOK_URL')
bot.send_text('Hello 企业微信！')
"
```

### 测试应用机器人（发送）
```bash
python -c "
from wework_bot import WeWorkBot
bot = WeWorkBot(
    corpid='YOUR_CORP_ID',
    corpsecret='YOUR_SECRET',
    agentid='YOUR_AGENT_ID'
)
bot.send_text_message('@all', '测试消息')
"
```

### 启动自动回复服务
```bash
# 1. 配置环境变量
export WEWORK_CORP_ID=xxx
export WEWORK_CORP_SECRET=xxx
export WEWORK_AGENT_ID=xxx
export WEWORK_TOKEN=xxx
export WEWORK_ENCODING_AES_KEY=xxx

# 2. 启动服务器
python wework_server.py

# 3. 在企业微信中给应用发送消息
# 系统会自动根据 config/reply_rules.yaml 回复
```

---

## 🔄 工作流程

```
用户发送消息
    ↓
企业微信服务器
    ↓
HTTP POST → 你的回调服务器 (wework_server.py)
    ↓
解密消息内容
    ↓
规则引擎匹配 (reply_rules.yaml)
    ↓
调用企业微信API发送回复
    ↓
用户收到自动回复
```

---

## 📚 官方文档

- 企业微信API文档: https://developer.work.weixin.qq.com/document/
- 群机器人配置: https://developer.work.weixin.qq.com/document/path/91770
- 应用消息推送: https://developer.work.weixin.qq.com/document/path/90664
- 接收消息: https://developer.work.weixin.qq.com/document/path/90239

---

## ⚖️ 对比总结

| 特性 | 手机方案 | 企业微信API |
|-----|---------|------------|
| 需要手机 | ✅ 是 | ❌ 否 |
| 技术方案 | 截屏+OCR | HTTP API |
| 稳定性 | 一般 | 优秀 |
| 识别准确率 | 70-90% | 100% |
| 支持类型 | 个人微信 | 企业微信 |
| 配置难度 | 中等 | 简单 |
| 运维成本 | 高（需要手机一直运行） | 低（服务器运行） |

**推荐：**
- 个人微信 → 使用手机方案（当前实现）
- 企业微信 → **使用官方API**（本文档方案）
