# 企业通信统一MCP服务

🤖 统一管理企业微信、飞书、钉钉三大平台的机器人配置和消息处理

## ✨ 特性

- ✅ **三大平台支持**: 企业微信、飞书、钉钉
- ✅ **双模式支持**: Webhook群机器人 + 企业应用
- ✅ **可视化配置**: Web界面配置，无需手动编辑文件
- ✅ **API配置**: 支持通过API后端配置
- ✅ **自动回复**: 基于规则引擎的智能自动回复
- ✅ **统一接口**: 统一的消息发送和接收接口

## 📦 目录结构

```
enterprise_comm_mcp/
├── mcp_server.py          # MCP服务器主程序
├── feishu_bot.py          # 飞书机器人实现
├── dingtalk_bot.py        # 钉钉机器人实现
├── config.yaml            # 配置文件
├── config.yaml.example    # 配置文件模板
└── static/
    └── config.html        # Web配置界面
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install flask pyyaml requests WechatPyCrypto
```

### 2. 创建配置文件

```bash
cd enterprise_comm_mcp
cp config.yaml.example config.yaml
```

### 3. 编辑配置

**方式A: 使用Web界面（推荐）**

```bash
# 启动服务器
python mcp_server.py

# 浏览器打开
http://localhost:8000/static/config.html
```

**方式B: 手动编辑配置文件**

编辑 `config.yaml`，填入相应平台的配置信息。

### 4. 启动服务

```bash
python mcp_server.py
```

## 📚 配置说明

### 企业微信配置

#### 方式1: 群机器人（Webhook）

1. 企业微信群 → 群设置 → 群机器人 → 添加
2. 复制 Webhook URL
3. 在配置中填入:

```yaml
wework:
  enabled: true
  type: webhook
  webhook_url: "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

#### 方式2: 企业应用

1. 登录企业微信管理后台
2. 应用管理 → 创建应用
3. 记录 CorpId、Secret、AgentId
4. 配置回调URL: `http://your-domain.com/callback/wework`
5. 在配置中填入:

```yaml
wework:
  enabled: true
  type: app
  corp_id: "ww1234567890abcdef"
  corp_secret: "YOUR_SECRET"
  agent_id: "1000001"
  token: "YOUR_TOKEN"
  encoding_aes_key: "YOUR_AES_KEY"
```

### 飞书配置

#### 方式1: 群机器人（Webhook）

1. 飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
2. 复制 Webhook 地址
3. 启用签名校验（可选），记录密钥

```yaml
feishu:
  enabled: true
  type: webhook
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
  secret: "YOUR_SECRET"  # 可选
```

#### 方式2: 自建应用

1. 开发者后台 → 创建自建应用
2. 记录 App ID 和 App Secret
3. 配置事件订阅 URL: `http://your-domain.com/callback/feishu`

```yaml
feishu:
  enabled: true
  type: app
  app_id: "cli_xxx"
  app_secret: "YOUR_SECRET"
```

### 钉钉配置

#### 方式1: 群机器人（Webhook）

1. 钉钉群 → 智能群助手 → 添加机器人 → 自定义
2. 复制 Webhook URL
3. 启用加签（可选），记录密钥

```yaml
dingtalk:
  enabled: true
  type: webhook
  webhook_url: "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
  secret: "YOUR_SECRET"  # 可选
```

#### 方式2: 企业内部应用

1. 开发者后台 → 创建应用
2. 记录 AppKey 和 AppSecret
3. 配置消息接收地址: `http://your-domain.com/callback/dingtalk`

```yaml
dingtalk:
  enabled: true
  type: app
  app_key: "dingxxx"
  app_secret: "YOUR_SECRET"
```

## 🌐 API文档

### 配置管理

#### 获取所有配置
```http
GET /api/config
```

#### 更新所有配置
```http
POST /api/config
Content-Type: application/json

{
  "wework": {...},
  "feishu": {...},
  "dingtalk": {...}
}
```

#### 获取指定平台配置
```http
GET /api/config/{platform}
```
platform: wework | feishu | dingtalk

#### 更新指定平台配置
```http
POST /api/config/{platform}
Content-Type: application/json

{
  "enabled": true,
  "type": "webhook",
  "webhook_url": "..."
}
```

### 消息发送

#### 发送消息到指定平台
```http
POST /api/send/{platform}
Content-Type: application/json

{
  "content": "消息内容"
}
```

### 系统状态

#### 健康检查
```http
GET /health
```

#### 获取系统状态
```http
GET /api/status
```

### 消息回调

- 企业微信: `POST /callback/wework`
- 飞书: `POST /callback/feishu`
- 钉钉: `POST /callback/dingtalk`

## 🔧 使用示例

### Python调用API

```python
import requests

# 发送消息到企业微信
response = requests.post(
    'http://localhost:8000/api/send/wework',
    json={'content': '测试消息'}
)
print(response.json())

# 更新飞书配置
response = requests.post(
    'http://localhost:8000/api/config/feishu',
    json={
        'enabled': True,
        'type': 'webhook',
        'webhook_url': 'https://...'
    }
)
print(response.json())
```

### curl调用API

```bash
# 发送消息
curl -X POST http://localhost:8000/api/send/dingtalk \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'

# 获取配置
curl http://localhost:8000/api/config

# 更新配置
curl -X POST http://localhost:8000/api/config/wework \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true, "type": "webhook", "webhook_url": "..."}'
```

## 📋 自动回复规则

修改 `config/reply_rules.yaml` 文件配置自动回复规则：

```yaml
rules:
  - name: "关键词回复"
    condition:
      type: keyword
      keywords: ["帮助", "help"]
    reply: "您好，我是自动回复机器人。需要什么帮助吗？"
  
  - name: "正则匹配"
    condition:
      type: regex
      pattern: "订单.*查询"
    reply: "请提供您的订单号，我来帮您查询。"
```

## 🔒 安全建议

1. **使用HTTPS**: 生产环境必须使用HTTPS
2. **配置签名/加签**: 启用各平台的签名验证
3. **API密钥**: 在配置中设置 `global.security.api_key`
4. **IP白名单**: 限制允许访问的IP地址
5. **回调验证**: 验证回调请求来源

## 🚀 部署建议

### 使用Gunicorn（生产环境）

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:8000 mcp_server:app
```

### 使用Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "mcp_server:app"]
```

### 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📖 相关文档

- [企业微信API文档](https://developer.work.weixin.qq.com/document/)
- [飞书开放平台](https://open.feishu.cn/document/)
- [钉钉开放平台](https://open.dingtalk.com/document/)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
