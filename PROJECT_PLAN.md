# 智能微信机器人项目规划 v2.0 (Project Plan: Intelligent WeChat Bot v2.0)

**文档说明**: 这是对项目初始规划的重大升级，旨在将项目从“原型”提升为“生产级”应用。本次更新采纳了关于架构、技术栈和部署的专业建议，构建一个更健壮、可扩展、可维护的系统。

## 1. 项目目标 (Project Goal)

(与v1.0保持一致)
构建一个高度模块化、可扩展的智能机器人平台。该平台通过Mac连接并自动化控制安卓手机上的微信，同时能集成飞书、钉钉、企业微信等办公软件和外部数据库，实现智能化的消息处理与任务执行。

## 2. 核心架构设计 (v2.0)

v2.0架构的核心思想是 **事件驱动**、**异步处理** 和 **插件化**。

```
+-------------------------------------------------------------------+
|                        插件层 (Plugin System)                     |
|           (动态加载的技能、规则、AI集成、数据库交互等)            |
+-------------------------------------------------------------------+
|                        核心逻辑层 (Core Logic)                    |
|      (Celery Workers: 消费事件、执行任务、处理错误、重试)       |
+-------------------------------------------------------------------+
|                        消息队列 (Message Queue)                   |
|                      (Redis/RabbitMQ as Broker)                   |
+-------------------------------------------------------------------+
|                        事件生产者 (Event Producers)                 |
| (微信监听器, 飞书Webhook接收器, 定时任务触发器, API Endpoint) |
+-------------------------------------------------------------------+
```

### 2.1. 事件驱动模型 (Event-Driven Model)
放弃v1.0的循环轮询方式。所有输入源（如微信新消息、API请求）都被视为“事件”。
- **事件生产者**: 负责监听外部世界，并将事件（例如：`{"type": "new_wechat_message", "payload": {...}}`）发布到消息队列。
- **消息队列**: 作为系统的中央动脉，负责缓冲和分发事件，实现生产者和消费者的解耦。
- **事件消费者 (核心逻辑)**: `Celery` 的 `Worker` 进程会订阅消息队列中的事件，并在后台进行处理。这使得系统响应更迅速，且不会阻塞事件的接收。

### 2.2. 异步任务处理 (Asynchronous Task Processing)
所有耗时的操作（例如：调用AI API、访问数据库、执行复杂的UI自动化）都必须作为异步任务来执行。
- **技术实现**: 使用 **Celery** 框架。
- **好处**:
    - **非阻塞**: 接收消息的进程可以瞬间完成任务分发，立即处理下一条。
    - **可扩展**: 可以通过增加 `Celery Worker` 数量来水平扩展任务处理能力。
    - **可靠性**: Celery提供任务重试、错误处理等机制。

### 2.3. 插件化技能系统 (Pluggable Skill System)
将“技能”升级为可动态加载的“插件”。
- **实现**: 在 `plugins/` 目录下，每个子目录代表一个插件。主程序在启动时会自动扫描这些目录，加载并注册其中定义的任务和处理器。
- **优点**: 新增功能只需按规范创建一个新的插件目录，无需修改任何核心代码，极大地提高了可扩展性和可维护性。

### 2.4. 错误处理与重试 (Error Handling & Retries)
- **任务重试**: 利用Celery的内置功能，为可能因网络波动等临时问题失败的任务（如调用外部API）配置自动重试策略。
- **死信队列 (Dead Letter Queue)**: 对于反复失败的任务，将其移入一个特殊的“死信队列”，以便人工介入分析，避免无限重试耗尽系统资源。
- **全局异常捕获**: 在Celery任务和API端点中设置全局异常处理器，用于记录未知错误并发送告警。

### 2.5. 安全与权限 (Security & Permissions)
- **密钥管理**: **严禁**将任何敏感信息（API密钥、密码）硬编码在代码中。所有密钥必须通过环境变量或专门的密钥管理服务（如HashiCorp Vault）注入。
- **权限控制**: 对于规则和插件，可以设计一套简单的权限体系。例如，在规则文件中定义 `required_permission: "admin"`，并在执行前进行校验。

## 3. 技术选型 (v2.0)

| 类别             | 技术/库                                   | 职责                                       |
| ---------------- | ----------------------------------------- | ------------------------------------------ |
| **核心框架**     | Python 3.8+                               | 主要编程语言                               |
| **手机自动化**   | `uiautomator2`                            | 安卓UI控制                                 |
| **消息队列**     | `Celery`                                  | 异步任务分发与执行                         |
| **消息代理**     | `Redis`                                   | Celery的Broker，用于存储任务队列           |
| **数据库**       | `PostgreSQL`                              | 结构化数据存储（用户信息、日志、状态等）   |
| **ORM**          | `SQLAlchemy`                              | 数据库交互                                 |
| **日志**         | `Loguru`                                  | 结构化、易于配置的日志记录                 |
| **配置管理**     | `Pydantic` (Settings Management)          | 类型安全的环境变量与配置文件管理           |
| **监控**         | `Prometheus` + `Grafana`                  | 系统指标收集与可视化                       |
| **告警**         | `Alertmanager`                            | 告警规则与通知                             |
| **API框架**      | `FastAPI`                                 | 提供外部调用的API端点及Webhook接收器       |
| **重试机制**     | `tenacity` (或Celery内置)                 | 为关键函数调用提供重试逻辑                 |

## 4. 部署与DevOps (v2.0)

### 4.1. 容器化 (Containerization)
使用Docker将应用及其依赖打包，确保环境一致性。`docker-compose.yml` 用于在开发和生产环境中编排多容器应用。

**`docker-compose.yml` 示例:**
```yaml
version: '3.8'

services:
  app:
    build: .
    command: python -m core.main  # 或者启动Celery Worker的命令
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydatabase
      - REDIS_URL=redis://redis:6379/0
      # - ... 其他API密钥

  celery_worker:
    build: .
    command: celery -A core.tasks worker --loglevel=info
    volumes:
      - .:/app
    depends_on:
      - redis
      - db
    environment:
      # ... 与 app 相同的环境变量

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"

  db:
    image: "postgres:13-alpine"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydatabase
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

**`Dockerfile` 示例:**
```dockerfile
# 使用官方Python镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码到工作目录
COPY . .

# (可选) 暴露API端口
# EXPOSE 8000

# 默认启动命令 (可以在docker-compose中覆盖)
CMD ["python", "-m", "core.main"]
```

### 4.2. CI/CD (持续集成/持续部署)
使用GitHub Actions自动化测试和部署流程。

**`.github/workflows/ci-cd.yml` 示例:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run tests (TODO: add tests)
      run: |
        # pytest .
        echo "Tests would run here"

  build-and-push-docker:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
      
    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
        
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: your-docker-repo/wechat-bot:latest
```

### 4.3. 监控与告警
- **监控**: 应用通过Prometheus客户端库暴露一个 `/metrics` 端点，报告关键指标（如：处理的消息数、任务延迟、错误率）。Prometheus服务器定期抓取这些数据。
- **告警**: 在Prometheus中定义告警规则（例如：`5分钟内错误率 > 5%`）。触发时，Prometheus将告警发送给Alertmanager，后者负责去重、分组，并发送通知到钉钉、Email等。

### 4.4. 备份与恢复
- **数据库**: 使用 `pg_dump` 对PostgreSQL数据库进行每日定时备份，并将备份文件存储在安全的位置（如对象存储S3）。
- **配置**: 关键的 `.env` 配置文件应被版本控制（如果无密钥）或安全存储。容器化部署使得恢复应用本身变得简单，只需重新拉取镜像并启动。

## 5. 进化版执行步骤 (Revised Execution Steps)

1.  **环境容器化**: 编写 `Dockerfile` 和 `docker-compose.yml`，确保一键 `docker-compose up` 可以启动所有基础服务（App骨架, Redis, Postgres）。
2.  **配置与日志**: 集成 `Pydantic` 管理配置，集成 `Loguru` 记录结构化日志。
3.  **重构核心为事件驱动**:
    - 创建 `core/tasks.py` 用于定义Celery任务。
    - 修改事件生产者（如 `wechat_platform.py`），使其不再直接处理逻辑，而是将事件发送到Celery任务队列。
    - `main.py` 的职责变为启动事件监听器。
4.  **数据库集成**: 使用SQLAlchemy定义数据模型（如 `MessageLog`），并让任务在处理时读写数据库。
5.  **开发第一个插件**: 将 `EchoSkill` 重构为一个独立的插件。
6.  **API与Webhook**: 使用FastAPI创建一个简单的API服务器，用于接收Webhook事件（如飞书）或提供控制端点。
7.  **CI/CD搭建**: 在代码仓库中配置GitHub Actions，实现自动化测试和镜像构建。
8.  **监控落地**: 在代码中加入Prometheus指标，并搭建Grafana仪表盘进行可视化。

---

## 功能完善计划 (Feature Improvement Plan)

为了将项目打造成一个健壮、可扩展、易于集成的智能微信助手平台，我们规划了以下几个核心开发方向。

### 1. 外部API接口 (High Priority)
- **目标**: 实现一个标准化的API接口（例如 RESTful API），允许第三方应用（如Web应用、移动App）与本系统进行交互。这是实现外部调用的关键。
- **功能**:
    - **发送消息**: 外部应用可以通过API向指定联系人或群组发送消息。
    - **接收消息**: 外部应用可以通过Webhook或其他机制，实时接收来自微信的消息。
    - **查询状态**: 提供查询机器人状态、好友列表等辅助接口。
- **技术选型**: 推荐使用 `FastAPI` 框架来快速构建此API服务。

### 2. 错误处理与重试策略
- **现状**: [尚未实现] Celery自带任务重试，但应用层缺少统一错误处理。
- **目标**: 建立全局的错误捕获机制，对可预见的失败（如网络中断、API调用失败）进行分类处理和优雅重试，确保任务的最终完成。

### 3. 安全认证与权限管理
- **现状**: [尚未实现]
- **目标**: 为外部API接口添加认证机制（如 API Key、OAuth2），确保只有授权应用可以访问。未来可扩展至更细粒度的权限管理。

### 4. 日志、监控与数据库支持
- **现状**: [尚未实现]
- **目标**:
    - **日志**: 引入结构化日志（如使用 `loguru`），记录关键操作和错误，便于调试和审计。
    - **监控**: 对接 `Prometheus` 或类似的监控系统，收集应用关键指标（如消息吞吐量、任务延迟、错误率）。
    - **数据库**: 集成数据库（如 `PostgreSQL` 或 `SQLite`），用于持久化存储用户信息、聊天记录、任务状态等关键数据。

### 5. 容器化与CI/CD
- **现状**: [部分实现] 已有 Dockerfile 和 docker-compose.yml。
- **目标**: 建立完整的CI/CD流水线（如使用 `GitHub Actions`），实现代码提交后自动测试、构建Docker镜像和部署。

### 6. 监控告警与备份恢复
- **现状**: [尚未实现]
- **目标**:
    - **告警**: 基于监控数据建立告警规则（例如，错误率激增时发送通知）。
    - **备份**: 制定数据库和重要配置的定期备份和恢复策略。