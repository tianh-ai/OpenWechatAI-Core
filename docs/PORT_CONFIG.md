# 端口配置规范

## 项目端口分配

本项目使用以下端口，如与现有程序冲突，优先修改本项目端口。

### 核心服务端口

| 服务 | 默认端口 | 备用端口 | 环境变量 | 说明 |
|------|---------|---------|----------|------|
| FastAPI | 8000 | 8001-8010 | API_PORT | REST API服务 |
| PostgreSQL | 5432 | 5433-5439 | POSTGRES_PORT | 数据库（Docker） |
| Redis | 6379 | 6380-6389 | REDIS_PORT | 缓存和消息队列 |
| MCP数据库服务 | 3000 | 3001-3010 | MCP_DATABASE_PORT | MCP数据库服务端点 |

### 端口冲突检测

使用以下命令检测端口占用：

```bash
# macOS/Linux
lsof -i :8000 -i :5432 -i :6379 -i :3000 | grep LISTEN

# 或使用netstat
netstat -an | grep LISTEN | grep -E ':(8000|5432|6379|3000)'
```

### 端口冲突解决方案

#### 1. FastAPI端口冲突（8000）

如果8000端口被占用，修改为8001：

```bash
# .env文件
API_PORT=8001
```

```yaml
# docker-compose.yml
api:
  ports:
    - "${API_PORT:-8001}:8000"
```

#### 2. PostgreSQL端口冲突（5432）

**当前检测到：5432端口被Docker占用**

修改为5433：

```bash
# .env文件
POSTGRES_PORT=5433
```

```yaml
# docker-compose.yml
postgres:
  ports:
    - "${POSTGRES_PORT:-5433}:5432"
```

#### 3. Redis端口冲突（6379）

**当前检测到：6379端口被Docker占用**

修改为6380：

```bash
# .env文件
REDIS_PORT=6380
```

```yaml
# docker-compose.yml
redis:
  ports:
    - "${REDIS_PORT:-6380}:6379"
```

#### 4. MCP数据库服务端口（3000）

如果3000端口被占用，修改为3001：

```bash
# .env文件
MCP_DATABASE_PORT=3001
MCP_DATABASE_ENDPOINT=http://localhost:3001/mcp
```

### 内部容器端口（不对外暴露）

以下端口仅在Docker网络内部使用，不需要映射到主机：

| 服务 | 内部端口 | 说明 |
|------|---------|------|
| Celery Worker | N/A | 无HTTP端口 |
| App Listener | N/A | 无HTTP端口 |

### 环境变量配置

在 `.env` 文件中配置：

```bash
# 端口配置（如有冲突则修改）
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
MCP_DATABASE_PORT=3000

# 完整端点URL
API_URL=http://localhost:${API_PORT}
REDIS_URL=redis://localhost:${REDIS_PORT}/0
MCP_DATABASE_ENDPOINT=http://localhost:${MCP_DATABASE_PORT}/mcp
```

### 端口使用建议

1. **开发环境**：使用默认端口（8000, 5432, 6379, 3000）
2. **测试环境**：使用备用端口（8001, 5433, 6380, 3001）
3. **生产环境**：根据实际部署情况配置，建议不暴露数据库端口

### 自动端口检测脚本

```bash
#!/bin/bash
# scripts/check-ports.sh

echo "检查端口占用情况..."

check_port() {
    port=$1
    service=$2
    if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
        echo "❌ 端口 $port ($service) 被占用"
        return 1
    else
        echo "✅ 端口 $port ($service) 可用"
        return 0
    fi
}

check_port 8000 "API"
check_port 5432 "PostgreSQL"
check_port 6379 "Redis"
check_port 3000 "MCP"
```

### Docker Compose端口配置

当前配置会自动使用环境变量中的端口：

```yaml
services:
  postgres:
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
  
  redis:
    ports:
      - "${REDIS_PORT:-6379}:6379"
  
  api:
    ports:
      - "${API_PORT:-8000}:8000"
```

### 当前端口状态（2025-12-16）

根据检测结果：
- ✅ 8000 (API) - 可用
- ❌ 5432 (PostgreSQL) - **被Docker占用，建议改为5433**
- ❌ 6379 (Redis) - **被Docker占用，建议改为6380**
- ✅ 3000 (MCP) - 可用

### 推荐配置

基于当前环境，建议使用以下端口配置：

```bash
# .env
API_PORT=8000
POSTGRES_PORT=5433  # 避免冲突
REDIS_PORT=6380     # 避免冲突
MCP_DATABASE_PORT=3000
```
