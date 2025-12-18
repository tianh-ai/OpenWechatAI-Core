# 快速开始指南

本指南帮助您快速搭建和运行 OpenWechatAI-Core 项目。

## 📋 前置要求

- Python 3.11+ （建议使用 3.12）
- Docker 和 Docker Compose
- Git
- macOS / Linux （Windows 用户建议使用 WSL2）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd OpenWechatAI-Core
```

### 2. 运行环境检查

项目提供了自动化环境检查脚本：

```bash
chmod +x scripts/check-env.sh
./scripts/check-env.sh
```

脚本会自动检查：
- ✅ Python 版本和环境
- ✅ Docker 服务状态
- ✅ 端口占用情况
- ✅ Python 依赖包
- ✅ 配置文件
- ✅ 目录结构

### 3. 配置环境变量

如果环境检查脚本已自动创建 `.env` 文件，请编辑配置：

```bash
vim .env
```

**重要配置项：**

```bash
# 端口配置（如有冲突请修改）
POSTGRES_PORT=5433  # 默认 5432 可能被占用
REDIS_PORT=6380     # 默认 6379 可能被占用
API_PORT=8000       # API 服务端口
MCP_PORT=3000       # MCP 服务端口

# MCP 数据库配置
MCP_DATABASE_ENDPOINT=http://localhost:3000/mcp
MCP_DATABASE_API_KEY=your_mcp_api_key_here

# AI 模型配置（至少配置一个）
OPENAI_API_KEY=sk-your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key

# 其他配置
DEBUG=true
LOG_LEVEL=INFO
```

### 4. 激活虚拟环境

```bash
source venv/bin/activate
```

### 5. 验证安装

运行测试确保一切正常：

```bash
pytest tests/unit -v
```

### 6. 启动服务

使用 Docker Compose 启动所有服务：

```bash
docker-compose up -d
```

查看服务状态：

```bash
docker-compose ps
```

查看日志：

```bash
docker-compose logs -f
```

### 7. 验证服务

检查 API 服务：

```bash
curl http://localhost:8000/health
```

预期响应：

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## 📁 项目结构

```
OpenWechatAI-Core/
├── api/                    # FastAPI 应用
│   ├── main.py            # API 主入口
│   └── routes/            # API 路由
├── core/                   # 核心业务逻辑
│   ├── config.py          # 配置管理
│   ├── main.py            # 应用主入口
│   └── tasks.py           # Celery 任务
├── models/                 # 数据模型
│   ├── database.py        # MCP 数据库接口
│   └── repositories.py    # 数据仓库层
├── rules/                  # 规则引擎
│   ├── engine.py          # 规则引擎核心
│   └── actions.py         # 规则动作
├── ai/                     # AI 集成
│   ├── chat.py            # AI 对话管理
│   └── providers/         # AI 提供商
├── wechat/                 # 微信自动化
│   ├── automation.py      # UI 自动化
│   └── message_handler.py # 消息处理
├── tests/                  # 测试
│   ├── unit/              # 单元测试
│   └── integration/       # 集成测试
├── docs/                   # 文档
│   ├── QUICKSTART.md      # 本文档
│   ├── PORT_CONFIG.md     # 端口配置指南
│   ├── MCP_INTEGRATION_RULES.md  # MCP 集成规范
│   └── MCP_DATABASE_REQUIREMENTS.md  # MCP 数据库需求
├── scripts/                # 工具脚本
│   └── check-env.sh       # 环境检查脚本
├── .env.example            # 环境变量模板
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile              # Docker 镜像定义
└── requirements.txt        # Python 依赖
```

## 🔧 常见问题

### Q1: 端口被占用怎么办？

修改 `.env` 文件中的端口配置：

```bash
# 查看被占用的端口
lsof -i :5432
lsof -i :6379

# 修改为备用端口
POSTGRES_PORT=5433
REDIS_PORT=6380
```

详细说明请参考：[docs/PORT_CONFIG.md](PORT_CONFIG.md)

### Q2: Python 版本不兼容？

项目需要 Python 3.11+。如果使用 pyenv：

```bash
# 安装 Python 3.12
pyenv install 3.12.3

# 切换到项目目录并设置本地版本
cd OpenWechatAI-Core
pyenv local 3.12.3

# 重新创建虚拟环境
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Q3: Docker 服务未运行？

确保 Docker Desktop 正在运行：

```bash
# 检查 Docker 状态
docker info

# macOS: 启动 Docker Desktop
open -a Docker
```

### Q4: 依赖包安装失败？

常见原因和解决方案：

```bash
# 1. 升级 pip
pip install --upgrade pip

# 2. 清理缓存
pip cache purge

# 3. 重新安装
pip install -r requirements.txt --no-cache-dir

# 4. 如果是编译错误，安装系统依赖（macOS）
brew install postgresql openssl
```

### Q5: MCP 数据库服务未启动？

MCP 数据库是外部服务，需要单独部署：

```bash
# 检查 MCP 服务状态
curl http://localhost:3000/health

# 如果未部署，请参考 MCP 服务文档
# docs/MCP_DATABASE_REQUIREMENTS.md
```

## 🧪 开发模式

### 启动开发服务器

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动 FastAPI 开发服务器（热重载）
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 启动 Celery Worker
celery -A core.tasks worker --loglevel=info

# 启动 WeChat 自动化（需要连接 Android 设备）
python core/main.py --platform wechat
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit -v

# 运行集成测试
pytest tests/integration -v

# 生成覆盖率报告
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### 代码格式化

```bash
# 安装开发工具
pip install black flake8 isort mypy

# 格式化代码
black .

# 检查代码风格
flake8 .

# 排序导入
isort .

# 类型检查
mypy .
```

## 📊 监控和日志

### 查看日志

```bash
# 应用日志
tail -f logs/app.log

# Docker 容器日志
docker-compose logs -f app
docker-compose logs -f celery-worker
docker-compose logs -f api

# Celery 任务日志
tail -f logs/celery.log
```

### 监控指标

访问 Prometheus 指标端点（如已启用）：

```bash
curl http://localhost:9090/metrics
```

## 🔐 安全建议

1. **不要提交 `.env` 文件到 Git**
   - `.env` 文件已在 `.gitignore` 中
   - 使用 `.env.example` 作为模板

2. **定期更新密钥**
   ```bash
   # 生成新的 SECRET_KEY
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **生产环境配置**
   ```bash
   ENVIRONMENT=production
   DEBUG=false
   LOG_LEVEL=WARNING
   ```

## 📚 更多文档

- [端口配置指南](PORT_CONFIG.md)
- [MCP 集成规范](MCP_INTEGRATION_RULES.md)
- [MCP 数据库需求](MCP_DATABASE_REQUIREMENTS.md)
- [MCP 数据库使用指南](MCP_DATABASE_USAGE.md)
- [架构迁移文档](MCP_DATABASE_MIGRATION.md)

## 🤝 获取帮助

如果遇到问题：

1. 查看 [常见问题](#常见问题) 部分
2. 查看相关文档
3. 检查 GitHub Issues
4. 联系开发团队

## 🎉 下一步

项目启动后，您可以：

- 配置 AI 对话规则（`rules/` 目录）
- 部署 MCP 数据库服务
- 连接 Android 设备测试微信自动化
- 查看 API 文档：http://localhost:8000/docs
- 开始开发自定义功能

祝您使用愉快！ 🚀
