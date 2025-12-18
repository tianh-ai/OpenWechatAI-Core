# OpenWechatAI Core

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Android](https://img.shields.io/badge/android-15%20ready-brightgreen)
![Enterprise](https://img.shields.io/badge/enterprise-WeWork%20%7C%20Feishu%20%7C%20DingTalk-orange)

**🤖 智能通信自动化平台 - 支持个人微信 + 企业通信（企业微信/飞书/钉钉）的AI驱动消息处理系统**

[快速开始](#-快速开始) · [企业通信MCP](#-企业通信mcp) · [手机配置](docs/PHONE_SETUP.md) · [微信自动化](docs/WECHAT_AUTOMATION.md)

</div>

---

## 📖 项目简介
OpenWechatAI-Core 是一个功能强大的智能通信自动化平台，提供**两种解决方案**：

1. **个人微信自动化** - 通过Android手机实现微信消息的自动检测、OCR识别和智能回复
2. **企业通信MCP** ⭐ **NEW** - 基于官方API的企业微信、飞书、钉钉统一管理平台

### ✨ 核心特性

#### 📱 个人微信自动化（手机方案）
- 🎯 **混合自动化**: 坐标点击 + OCR识别 + 图像对比
- 📱 **Android 15兼容**: 完美支持最新系统
- 🔍 **OCR识别**: Docker容器化PaddleOCR，高准确率
- 📊 **消息监控**: 实时检测新消息并自动进入聊天
- 🤖 **规则引擎**: 基于YAML的灵活回复规则
- 📸 **完整日志**: 截图存档和操作记录

#### 🏢 企业通信MCP（API方案）⭐ **推荐**
- ✅ **完全不需要手机** - 纯API方式，稳定可靠
- 🎯 **三大平台支持** - 企业微信、飞书、钉钉统一管理
- 🌐 **Web配置界面** - 可视化配置，简单易用
- 📡 **统一消息接口** - 一套API管理所有平台
- 🤖 **自动回复** - 基于规则引擎的智能回复
- 🔌 **双模式支持** - Webhook群机器人 + 企业应用
- 📊 **100%准确率** - 官方API，消息识别准确
- 🚀 **快速部署** - 5分钟完成配置和测试I和管理后台
- 🐳 **容器化部署**: 完整的Docker和Kubernetes支持

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      规则层 (Rules)                          │
│          YAML配置 + 规则引擎 + 动态热加载                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     逻辑层 (Logic)                           │
│    事件调度 + AI决策 + 插件管理 + 上下文管理                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    技能层 (Skills)                           │
│      插件化技能 + 技能注册 + 技能优先级 + 技能链             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   接口层 (Interfaces)                        │
│   IMessagePlatform + IControlBridge + IAIModel + IDatabase   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  实现层 (Implementations)                    │
│     微信 + 飞书 + 钉钉 + OpenAI + PostgreSQL + Redis         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 💡 选择您的方案

| 方案 | 适用场景 | 优势 | 限制 |
|------|----------|------|------|
| **企业通信MCP** ⭐ | 企业微信/飞书/钉钉 | ✅ 不需要手机<br>✅ 100%准确率<br>✅ Web界面配置<br>✅ 官方API支持 | ⚠️ 仅支持企业通信平台 |
| **个人微信自动化** | 个人微信 | ✅ 支持个人微信<br>✅ OCR识别消息 | ⚠️ 需要Android手机<br>⚠️ 70-90%准确率 |

---

## 🏢 企业通信MCP

### ⚡ 5分钟快速开始

```bash
# 1. 进入MCP目录
cd enterprise_comm_mcp

# 2. 复制配置文件
cp config.yaml.example config.yaml

# 3. 启动服务
python mcp_server.py

# 4. 打开Web配置界面
浏览器访问: http://localhost:8000/static/config.html

# 5. 在Web界面配置平台参数并测试
```

### 📋 支持的平台

#### 企业微信
- ✅ 群机器人（Webhook）
- ✅ 企业应用（完整功能）
- 📚 [配置指南](docs/WEWORK_BOT_GUIDE.md)

#### 飞书
- ✅ 群机器人（Webhook）
- ✅ 自建应用（完整功能）
- 📚 [官方文档](https://open.feishu.cn/document/)

#### 钉钉
- ✅ 群机器人（Webhook）
- ✅ 企业内部应用（完整功能）
- 📚 [官方文档](https://open.dingtalk.com/document/)

### 🎯 核心功能

**配置管理**
```bash
# API配置
curl -X POST http://localhost:8000/api/config/wework \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true, "type": "webhook", "webhook_url": "..."}'

# 获取配置
curl http://localhost:8000/api/config
```

**消息发送**
```bash
# 发送到企业微信
curl -X POST http://localhost:8000/api/send/wework \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'

# 发送到飞书
curl -X POST http://localhost:8000/api/send/feishu \
  -H 'Content-Type: application/json' \
  -d '{"content": "测试消息"}'
```

**Python调用**
```python
import requests

# 发送消息
response = requests.post(
    'http://localhost:8000/api/send/wework',
    json={'content': '自动回复消息'}
)

# 更新配置
response = requests.post(
    'http://localhost:8000/api/config/feishu',
    json={
        'enabled': True,
        'type': 'webhook',
        'webhook_url': 'https://...'
    }
)
```

### 📊 使用示例

查看完整示例：[企业通信MCP指南](ENTERPRISE_COMM_MCP_GUIDE.md)

---

## 📱 个人微信自动化

### 前置要求

- **Mac电脑**: macOS 10.15+
- **安卓手机**: Android 7.0+ (推荐Android 15)
- **Python**: 3.12+
- **Docker**: 用于运行PaddleOCR容器

### 快速安装

```bash
# 1. 克隆项目
git clone https://github.com/tianh-ai/OpenWechatAI-Core.git
cd OpenWechatAI-Core

# 2. 安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 启动Docker OCR服务
docker-compose up -d bidding_backend

# 4. 连接手机并启动
adb devices
python wechat_auto_reply.py --interval 3 --ocr --ocr-engine docker
```

详细步骤: [手机配置指南](docs/PHONE_SETUP.md)

---

## 📚 文档目录

### 企业通信MCP
| 文档 | 描述 |
|------|------|
| [企业通信MCP指南](ENTERPRISE_COMM_MCP_GUIDE.md) | 完整的使用指南和对比说明 |
| [企业微信机器人](docs/WEWORK_BOT_GUIDE.md) | 企业微信配置详解 |
| [MCP服务器文档](enterprise_comm_mcp/README.md) | API文档和部署说明 |
| [快速测试脚本](test_enterprise_mcp.py) | 自动化测试工具 |

### 个人微信自动化

| 文档 | 描述 |
|------|------|
| [快速开始](QUICKSTART.md) | 30分钟快速上手指南 |
| [实施规划](IMPLEMENTATION_PLAN.md) | 详细的开发实施路线图 |
| [优化指南](OPTIMIZATION_GUIDE.md) | 架构优化和性能提升方案 |
| [开发路线图](ROADMAP.md) | 版本规划和功能演进 |
| [项目规划](PROJECT_PLAN.md) | 原始项目设计文档 |

---

## 💡 使用示例

### 创建自动回复规则

编辑 `rules/auto_reply.yaml`:

```yaml
- name: "智能客服"
| 文档 | 描述 |
|------|------|
| [快速开始](QUICKSTART.md) | 30分钟上手指南 |
| [手机配置](docs/PHONE_SETUP.md) | Android手机配置详解 |
| [微信自动化](docs/WECHAT_AUTOMATION.md) | 微信控制说明 |
| [实施规划](IMPLEMENTATION_PLAN.md) | 开发路线图 |
| [优化指南](OPTIMIZATION_GUIDE.md) | 性能优化方案 |

---

## 💡 使用示例

### 企业通信MCP示例

#### 1. Web界面配置（最简单）

1. 访问配置页面: `http://localhost:8000/static/config.html`
2. 选择平台（企业微信/飞书/钉钉）
3. 填入Webhook URL或应用凭证
4. 点击"保存配置"
5. 点击"测试发送"验证

#### 2. API调用示例

```python
import requests

# 企业微信群机器人推送
bot_config = {
    'enabled': True,
    'type': 'webhook',
    'webhook_url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx'
}
requests.post('http://localhost:8000/api/config/wework', json=bot_config)

# 发送消息
requests.post(
    'http://localhost:8000/api/send/wework',
    json={'content': '📊 日报：今日订单量100单'}
)

# 飞书应用机器人
feishu_config = {
    'enabled': True,
    'type': 'app',
    'app_id': 'cli_xxx',
    'app_secret': 'your_secret'
}
requests.post('http://localhost:8000/api/config/feishu', json=feishu_config)

# 发送富文本消息
requests.post(
    'http://localhost:8000/api/send/feishu',
    json={'content': '**重要通知**\n请及时处理'}
)
```

#### 3. 自动回复配置

编辑 `config/reply_rules.yaml`:

```yaml
rules:
  - name: "工作时间自动回复"
    condition:
      type: time_range
      start_time: "09:00"
      end_time: "18:00"
    reply: "收到您的消息，我会尽快回复"
  
  - name: "关键词回复"
    condition:
      type: keyword
      keywords: ["价格", "报价", "优惠"]
    reply: "感谢咨询！请查看我们的最新价格表: https://..."
  
  - name: "休息时间回复"
    condition:
      type: time_range
      start_time: "22:00"
      end_time: "08:00"
    reply: "现在是休息时间，明天会回复您~"
```

### 个人微信自动化示例

#### 创建自动回复规则50
  enabled: true
  if:
    platform: "WeChat"
    sender: "老板"
    content_contains: "紧急"
  then:
    action: "forward"
    target: "DingTalk"
    notify_channels: ["email", "sms"]
```

### 创建自定义技能

```python
# skills/weather_skill.py
from skills.base_skill import BaseSkill
from interfaces.message_platform import IMessagePlatform
import httpx

class WeatherSkill(BaseSkill):
    """天气查询技能"""
    
    @property
    def name(self) -> str:
        return "Weather Skill"
    
    def can_handle(self, message: dict) -> bool:
        content = message.get("content", "")
        return "天气" in content or "weather" in content.lower()
    
    async def execute(self, message: dict, platform: IMessagePlatform):
        sender = message.get("sender")
        # 调用天气API获取数据
        weather_data = await self._get_weather()
        reply = f"今天天气: {weather_data}"
        platform.send_message(sender, reply)
```

---

## 🛠️ 技术栈

### 核心框架
- **Python 3.11+**: 主开发语言
- **uiautomator2**: 安卓UI自动化
- **FastAPI**: 高性能Web框架
- **Celery**: 分布式任务队列
- **SQLAlchemy**: ORM框架

### 数据存储
- **PostgreSQL**: 主数据库
- **Redis**: 缓存和消息队列

### AI集成
- **OpenAI GPT**: 智能对话
- **Google Gemini**: 多模态AI
- **Anthropic Claude**: 高级推理

### 监控运维
- **Loguru**: 日志管理
- **Prometheus**: 指标收集
- **Grafana**: 可视化监控
- **Sentry**: 错误追踪

- **Python 3.12+**: 主开发语言
- **Docker**: 容器化部署
- **ADB**: Android调试桥

---

## 📊 项目状态

### 当前版本: v1.0.0

| 模块 | 状态 | 完成度 |
|------|------|--------|
| 企业通信MCP | ✅ 稳定版 | 100% |
| - 企业微信支持 | ✅ 完成 | 100% |
| - 飞书支持 | ✅ 完成 | 100% |
| - 钉钉支持 | ✅ 完成 | 100% |
| - Web配置界面 | ✅ 完成 | 100% |
| - API接口 | ✅ 完成 | 100% |
| 个人微信自动化 | ✅ 稳定版 | 90% |
| - 消息检测 | ✅ 完成 | 100% |
| - OCR识别 | ✅ 完成 | 95% |
| - 自动回复 | ✅ 完成 | 90% |
| - 规则引擎 | ✅ 完成 | 100% |
| AI集成 | 📋 计划中 | 30% |

### 版本历史

- **v1.0.0** (2025-12-17) - 企业通信MCP正式版发布
  - ✅ 企业微信、飞书、钉钉三大平台完整支持
  - ✅ Web可视化配置界面
  - ✅ 统一REST API接口
  - ✅ 自动回复规则引擎
  - ✅ 完整文档和示例

- **v0.9.0** (2025-12-16) - 个人微信自动化稳定版
  - ✅ Android 15完全兼容
  - ✅ Docker OCR集成
  - ✅ 自动进入聊天功能
  - ✅ 多级输入备用方案
  - ✅ 屏幕管理优化

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！无论是报告Bug、提出新功能建议，还是提交代码，都非常感谢！

### 📋 贡献方式

- 🐛 **报告Bug**: [提交Bug报告](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=bug_report.md)
- 💡 **功能建议**: [提交功能请求](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=feature_request.md)
- ❓ **使用咨询**: [提问题](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=question.md)
- 💻 **代码贡献**: [创建Pull Request](https://github.com/tianh-ai/OpenWechatAI-Core/pulls)
- 📚 **文档改进**: 帮助完善文档和示例

### 🚀 快速开始贡献

1. **Fork 本项目**
2. **创建特性分支**
   ```bash
   git checkout -b feature/AmazingFeature
   # 或
   git checkout -b fix/BugFix
   ```
3. **提交更改**
   ```bash
   git commit -m "feat: 添加XXX功能"
   # 或
   git commit -m "fix: 修复XXX问题"
   ```
4. **推送到分支**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **开启 Pull Request**

### 📝 开发规范

- 遵循 [PEP 8](https://pep8.org/) 代码风格
- 使用 [Black](https://github.com/psf/black) 格式化代码
- 编写单元测试（目标覆盖率 > 80%）
- 添加必要的注释和文档字符串
- 更新相关文档和示例

### 🧪 测试要求

```bash
# 运行测试
pytest tests/

# 查看覆盖率
pytest --cov=. tests/

# 格式化代码
black .

# 检查代码风格
flake8 .
```

### 📚 更多信息

详细的贡献指南请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

您可以自由地：
- ✅ 使用本项目用于商业或非商业用途
- ✅ 修改和分发本项目
- ✅ 在您的项目中集成本项目

条件：
- 📋 保留版权声明和许可证声明
- 🚫 不提供任何担保

---

## 🙏 致谢

### 核心技术

感谢以下优秀的开源项目和技术：

#### 企业通信MCP
- [Flask](https://flask.palletsprojects.com/) - 强大的Python Web框架
- [企业微信API](https://developer.work.weixin.qq.com/) - 企业微信官方API
- [飞书开放平台](https://open.feishu.cn/) - 飞书官方开放平台
- [钉钉开放平台](https://open.dingtalk.com/) - 钉钉官方开放平台

#### 个人微信自动化
- [uiautomator2](https://github.com/openatx/uiautomator2) - Android UI自动化框架
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 百度开源OCR引擎
- [imagehash](https://github.com/JohannesBuchner/imagehash) - 图像哈希库

#### 开发工具
- [pytest](https://pytest.org/) - Python测试框架
- [black](https://github.com/psf/black) - Python代码格式化工具
- [flake8](https://flake8.pycqa.org/) - Python代码检查工具

### 贡献者

感谢所有为这个项目做出贡献的人！

<a href="https://github.com/tianh-ai/OpenWechatAI-Core/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tianh-ai/OpenWechatAI-Core" />
</a>

### 特别感谢

- 🎯 所有提出宝贵建议和反馈的用户
- 🐛 所有提交Bug报告的用户
- 💻 所有贡献代码的开发者
- 📚 所有完善文档的贡献者
- ⭐ 所有给予Star支持的朋友

你们的支持是这个项目持续发展的动力！❤️

---

## 📞 联系我们

### 社区支持

- 💬 **问题反馈**: [GitHub Issues](https://github.com/tianh-ai/OpenWechatAI-Core/issues)
- 💡 **功能建议**: [Feature Requests](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=feature_request.md)
- 🐛 **Bug报告**: [Bug Reports](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=bug_report.md)
- 💭 **讨论区**: [GitHub Discussions](https://github.com/tianh-ai/OpenWechatAI-Core/discussions)

### 项目资源

- 🏠 **项目主页**: https://github.com/tianh-ai/OpenWechatAI-Core
- 📖 **文档中心**: [完整文档](https://github.com/tianh-ai/OpenWechatAI-Core#-文档)
- 🚀 **快速开始**: [5分钟上手指南](https://github.com/tianh-ai/OpenWechatAI-Core#-快速开始)
- 📦 **Release**: [版本发布](https://github.com/tianh-ai/OpenWechatAI-Core/releases)

### 获取帮助

遇到问题？可以通过以下方式获取帮助：

1. 📚 查阅[文档](https://github.com/tianh-ai/OpenWechatAI-Core#-文档)和[示例代码](examples/)
2. 🔍 搜索[已有Issues](https://github.com/tianh-ai/OpenWechatAI-Core/issues)
3. 💬 在[Discussions](https://github.com/tianh-ai/OpenWechatAI-Core/discussions)提问
4. 🐛 如果是Bug，请[创建Issue](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=bug_report.md)

---

## 📊 项目统计

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/tianh-ai/OpenWechatAI-Core?style=social)
![GitHub forks](https://img.shields.io/github/forks/tianh-ai/OpenWechatAI-Core?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/tianh-ai/OpenWechatAI-Core?style=social)

![GitHub issues](https://img.shields.io/github/issues/tianh-ai/OpenWechatAI-Core)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tianh-ai/OpenWechatAI-Core)
![GitHub last commit](https://img.shields.io/github/last-commit/tianh-ai/OpenWechatAI-Core)
![GitHub contributors](https://img.shields.io/github/contributors/tianh-ai/OpenWechatAI-Core)

</div>

---

<div align="center">

### ⭐ 如果这个项目对您有帮助，请给我们一个Star！⭐

**让企业通信自动化变得简单而强大**

Made with ❤️ by [OpenWechatAI Team](https://github.com/tianh-ai)

[⬆ 回到顶部](#openwechatai-core)

</div>
