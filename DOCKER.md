# Docker部署指南

## 快速启动

### 1. 环境配置

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置必要的配置：

```bash
# 数据库密码
POSTGRES_PASSWORD=your_secure_password

# AI API密钥
OPENAI_API_KEY=sk-xxxxx
GEMINI_API_KEY=xxxxx

# 日志级别
LOG_LEVEL=INFO
DEBUG=false
```

### 2. 构建并启动

```bash
# 构建镜像
docker-compose build

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f app
```

### 3. 初始化数据库

```bash
# 进入应用容器
docker-compose exec app bash

# 运行数据库迁移
python -c "from models import init_db; init_db()"
```

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| postgres | 5432 | PostgreSQL数据库 |
| redis | 6379 | Redis缓存和消息队列 |
| app | - | 微信监听主程序 |
| celery-worker | - | 异步任务处理 |
| api | 8000 | FastAPI REST接口 |

## 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 删除服务（保留数据）
docker-compose down

# 删除服务和数据卷
docker-compose down -v
```

### 查看状态

```bash
# 查看运行状态
docker-compose ps

# 查看资源使用
docker stats

# 查看日志
docker-compose logs -f --tail=100
```

### 进入容器

```bash
# 进入应用容器
docker-compose exec app bash

# 进入数据库
docker-compose exec postgres psql -U openwechat

# 进入Redis
docker-compose exec redis redis-cli
```

### 扩容

```bash
# 增加Celery worker数量
docker-compose up -d --scale celery-worker=3
```

## 健康检查

### 检查服务健康状态

```bash
# 所有服务
docker-compose ps

# API健康检查
curl http://localhost:8000/health

# 数据库连接
docker-compose exec postgres pg_isready

# Redis连接
docker-compose exec redis redis-cli ping
```

## 数据备份

### 备份数据库

```bash
# 导出数据库
docker-compose exec postgres pg_dump -U openwechat openwechat > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker-compose exec -T postgres psql -U openwechat openwechat < backup_20231201.sql
```

### 备份Redis

```bash
# 触发保存
docker-compose exec redis redis-cli SAVE

# 复制RDB文件
docker cp openwechat-redis:/data/dump.rdb ./redis_backup.rdb
```

## 监控

### 查看日志

```bash
# 实时日志
docker-compose logs -f

# 应用日志文件
tail -f logs/app.log

# 错误日志
tail -f logs/error.log
```

### 性能监控

```bash
# 容器资源使用
docker stats openwechat-app openwechat-celery

# Celery监控
docker-compose exec celery-worker celery -A core.tasks inspect active
```

## 故障排查

### 容器无法启动

```bash
# 查看详细日志
docker-compose logs app

# 检查配置
docker-compose config

# 重新构建
docker-compose build --no-cache
```

### 数据库连接失败

```bash
# 检查数据库状态
docker-compose exec postgres pg_isready

# 查看连接数
docker-compose exec postgres psql -U openwechat -c "SELECT count(*) FROM pg_stat_activity;"
```

### Redis连接问题

```bash
# 测试连接
docker-compose exec redis redis-cli ping

# 查看连接客户端
docker-compose exec redis redis-cli CLIENT LIST
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建
docker-compose build

# 重启服务（滚动更新）
docker-compose up -d --no-deps --build app
```

## 生产环境建议

1. **安全性**
   - 修改默认密码
   - 使用secrets管理敏感信息
   - 启用SSL/TLS

2. **性能**
   - 增加worker数量
   - 调整数据库连接池
   - 配置Redis持久化

3. **监控**
   - 集成Prometheus
   - 使用Grafana可视化
   - 配置告警

4. **备份**
   - 定时备份数据库
   - 备份配置文件
   - 备份规则文件
