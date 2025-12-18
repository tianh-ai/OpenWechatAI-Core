# 🚀 快速开始指南

欢迎使用 **OpenWechatAI-Core**！本指南将帮助您在30分钟内启动并运行您的第一个智能微信机器人。

## 📋 前置要求

### 硬件要求
- **Mac电脑**: macOS 10.15+
- **安卓手机**: Android 7.0+
- **USB数据线**: 连接手机和Mac

### 软件要求
- **Python**: 3.11+
- **PostgreSQL**: 15+
- **Redis**: 7+
- **ADB**: Android Debug Bridge

### 可选（生产环境）
- Docker Desktop 4.0+
- Git

---

## 🛠️ 安装步骤

### 第一步: 环境准备

#### 1.1 安装Python依赖
```bash
# 确认Python版本
python3 --version  # 应该 >= 3.11

# 克隆项目
git clone https://github.com/tianh-ai/OpenWechatAI-Core.git
cd OpenWechatAI-Core

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 1.2 安装数据库

**PostgreSQL**:
```bash
# 使用Homebrew安装
brew install postgresql@15

# 启动服务
brew services start postgresql@15

# 创建数据库
createdb openwechatai

# 创建用户
psql -d openwechatai -c "CREATE USER wechat WITH PASSWORD 'your_password';"
psql -d openwechatai -c "GRANT ALL PRIVILEGES ON DATABASE openwechatai TO wechat;"
```

**Redis**:
```bash
# 安装
brew install redis

# 启动
brew services start redis

# 验证
redis-cli ping  # 应该返回 PONG
```

#### 1.3 安装ADB工具
```bash
# 安装Android Platform Tools
brew install android-platform-tools

# 验证安装
adb version
```

---

### 第二步: 配置项目

#### 2.1 创建环境变量文件
```bash
# 复制模板
cp .env.example .env

# 编辑配置
nano .env
```

**最小配置** (`.env`):
```bash
# 环境
ENVIRONMENT=development
DEBUG=true

# 数据库
DATABASE_URL=postgresql://wechat:your_password@localhost:5432/openwechatai

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# AI (至少配置一个)
OPENAI_API_KEY=sk-your-openai-key

# 安全
SECRET_KEY=your-random-secret-key-at-least-32-characters

# 日志
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

#### 2.2 初始化数据库
```bash
# 运行迁移
alembic upgrade head

# 或者直接创建表
python -c "from models.database import Base, engine; Base.metadata.create_all(engine)"
```

---

### 第三步: 连接安卓手机

#### 3.1 开启USB调试
1. 进入手机 **设置** → **关于手机**
2. 连续点击 **版本号** 7次，开启开发者模式
3. 返回 **设置** → **开发者选项**
4. 开启 **USB调试** 和 **USB调试（安全设置）**

#### 3.2 连接并授权
```bash
# 用USB线连接手机和Mac
# 手机上会弹出授权提示，点击"确定"

# 验证连接
adb devices

# 应该看到类似输出:
# List of devices attached
# 1A2B3C4D5E	device
```

#### 3.3 初始化uiautomator2
```bash
# 在手机上安装ATX Agent
python -m uiautomator2 init

# 验证安装
python -c "import uiautomator2 as u2; d = u2.connect(); print(d.info)"
```

---

### 第四步: 运行项目

#### 4.1 启动Redis和Celery Worker（终端1）
```bash
# 确保Redis正在运行
redis-cli ping

# 启动Celery Worker
celery -A core.tasks worker --loglevel=info
```

#### 4.2 启动消息监听器（终端2）
```bash
# 确保虚拟环境已激活
source .venv/bin/activate

# 启动监听器
python -m core.main listener
```

#### 4.3 （可选）启动API服务（终端3）
```bash
# 启动FastAPI服务
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 访问API文档
# http://localhost:8000/docs
```

---

## ✅ 验证安装

### 测试1: 检查服务状态
```bash
# 检查PostgreSQL
psql -U wechat -d openwechatai -c "SELECT 1;"

# 检查Redis
redis-cli ping

# 检查手机连接
adb devices

# 检查Python环境
python -c "import uiautomator2, openai, celery; print('所有依赖正常')"
```

### 测试2: 发送测试消息
```python
# test_connection.py
import uiautomator2 as u2
from implementations.wechat.wechat_platform import WeChatPlatform

# 连接设备
platform = WeChatPlatform()

# 连接微信
if platform.connect():
    print("✅ 微信连接成功")
    
    # 发送测试消息（替换为真实联系人）
    result = platform.send_message("文件传输助手", "测试消息")
    
    if result:
        print("✅ 消息发送成功")
    else:
        print("❌ 消息发送失败")
    
    platform.disconnect()
else:
    print("❌ 微信连接失败")
```

运行测试:
```bash
python test_connection.py
```

---

## 🎯 第一个机器人

### 创建简单的自动回复规则

编辑 `rules/default.yaml`:
```yaml
# 自动回复规则
- name: "关键词自动回复"
  priority: 50
  enabled: true
  if:
    platform: "WeChat"
    content_contains: "你好"
  then:
    action: "auto_reply"
    message: "你好！我是智能助手，有什么可以帮您？"

- name: "Echo测试"
  priority: 30
  enabled: true
  if:
    platform: "WeChat"
    content_regex: "^echo\\s+(.+)"
  then:
    action: "auto_reply"
    skill: "EchoSkill"
```

### 创建自定义技能

创建文件 `skills/hello_skill.py`:
```python
from typing import Dict, Any
from skills.base_skill import BaseSkill
from interfaces.message_platform import IMessagePlatform

class HelloSkill(BaseSkill):
    """问候技能"""
    
    @property
    def name(self) -> str:
        return "Hello Skill"
    
    def can_handle(self, message: Dict[str, Any]) -> bool:
        content = message.get("content", "").lower()
        return "你是谁" in content or "你叫什么" in content
    
    def execute(self, message: Dict[str, Any], platform: IMessagePlatform) -> None:
        sender = message.get("sender")
        reply = "我是OpenWechatAI智能助手，可以帮您自动处理微信消息。我支持:\n" \
                "1. 关键词自动回复\n" \
                "2. AI智能对话\n" \
                "3. 消息转发\n" \
                "4. 定时提醒\n\n" \
                "发送 @AI 开头的消息可以与我对话哦！"
        
        platform.send_message(sender, reply)
```

### 测试机器人

1. 在手机上打开微信
2. 给自己（文件传输助手）或测试联系人发送：
   - "你好" → 应该收到自动回复
   - "你是谁" → 应该收到详细介绍
   - "echo 测试" → 应该回显消息

---

## 🐳 Docker快速启动（推荐）

### 使用Docker Compose
```bash
# 创建 .env 文件（参考上面的配置）
cp .env.example .env

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

这将自动启动:
- PostgreSQL数据库
- Redis
- Celery Worker
- API服务
- 消息监听器

---

## 🔧 常见问题

### Q1: adb devices 显示 unauthorized
**解决**: 在手机上重新授权USB调试，勾选"总是允许这台电脑"

### Q2: uiautomator2 连接失败
**解决**: 
```bash
# 重新初始化
python -m uiautomator2 init

# 或手动安装
adb install -r -t app-uiautomator.apk
adb install -r -t app-uiautomator-test.apk
```

### Q3: 数据库连接失败
**解决**:
```bash
# 检查PostgreSQL是否运行
brew services list | grep postgresql

# 检查数据库是否存在
psql -l | grep openwechatai

# 检查连接字符串
echo $DATABASE_URL
```

### Q4: Celery worker无法启动
**解决**:
```bash
# 确认Redis正在运行
redis-cli ping

# 检查Celery配置
python -c "from core.tasks import celery_app; print(celery_app.conf)"
```

### Q5: 微信UI元素找不到
**解决**:
```bash
# 使用weditor工具查看UI结构
pip install weditor
weditor

# 然后在浏览器打开 http://localhost:17310
# 连接设备后可以查看所有UI元素
```

---

## 📚 下一步

恭喜！您已经成功运行了第一个智能微信机器人。接下来您可以:

1. **学习更多技能**: 查看 `skills/` 目录下的示例
2. **配置规则**: 编辑 `rules/*.yaml` 文件
3. **集成AI**: 配置OpenAI API实现智能对话
4. **Web管理**: 访问 http://localhost:8000 管理机器人
5. **阅读文档**: 
   - [实施规划](IMPLEMENTATION_PLAN.md)
   - [优化指南](OPTIMIZATION_GUIDE.md)
   - [开发路线图](ROADMAP.md)

---

## 🆘 获取帮助

- **文档**: 查看 `docs/` 目录
- **示例**: 查看 `examples/` 目录
- **问题**: 提交 GitHub Issue
- **讨论**: GitHub Discussions

---

## 📄 许可证

MIT License

---

**最后更新**: 2025-12-16  
**版本**: v0.5
