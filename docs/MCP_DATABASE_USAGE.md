# MCP数据库服务配置说明

## 配置项

在 `.env` 文件中添加以下配置：

```bash
# MCP数据库服务端点
MCP_DATABASE_ENDPOINT=http://localhost:3000/mcp

# MCP数据库API密钥
MCP_DATABASE_API_KEY=your_api_key_here

# MCP数据库请求超时（秒）
MCP_DATABASE_TIMEOUT=30
```

## 使用方法

### 1. 初始化MCP数据库

```python
from models import init_mcp_database

# 在应用启动时初始化
await init_mcp_database()
```

### 2. 使用仓库层访问数据

```python
from models import message_repo, rule_repo, user_repo

# 创建消息
message = await message_repo.create(
    platform="wechat",
    sender="user123",
    receiver="bot",
    content="你好",
    message_type="TEXT",
    status="PENDING"
)

# 查询待处理消息
pending = await message_repo.get_pending_messages(limit=10)

# 更新消息状态
await message_repo.update_status(message["id"], "COMPLETED")

# 获取或创建用户
user = await user_repo.get_or_create(
    platform="wechat",
    platform_user_id="wx_123",
    nickname="张三"
)

# 创建规则
rule = await rule_repo.create(
    name="智能问候",
    description="检测问候语自动回复",
    priority=10,
    conditions={"content_regex": "^(你好|hi)"},
    actions={"action": "auto_reply", "message": "您好！"}
)
```

### 3. 直接使用MCP客户端

```python
from models import get_mcp_db

db = get_mcp_db()

# 创建记录
result = await db.create("messages", {
    "platform": "wechat",
    "sender": "user123",
    "content": "测试消息"
})

# 查询记录
messages = await db.query(
    "messages",
    filters={"status": "PENDING"},
    order_by="-created_at",
    limit=10
)

# 更新记录
await db.update("messages", message_id, {
    "status": "COMPLETED"
})

# 删除记录
await db.delete("messages", message_id)
```

## 注意事项

1. **异步操作**: 所有数据库操作都是异步的，需要使用 `await`
2. **错误处理**: MCP服务可能不可用，需要妥善处理异常
3. **数据验证**: 发送到MCP的数据应该经过验证
4. **性能优化**: 考虑添加本地缓存层

## 迁移指南

从SQLAlchemy迁移到MCP数据库：

### 之前（SQLAlchemy）
```python
from models import Message, get_db_context

with get_db_context() as db:
    message = Message(
        platform="wechat",
        sender="user123",
        content="你好"
    )
    db.add(message)
    db.commit()
    
    messages = db.query(Message).filter_by(status="PENDING").all()
```

### 之后（MCP）
```python
from models import message_repo

# 创建
message = await message_repo.create(
    platform="wechat",
    sender="user123",
    content="你好"
)

# 查询
messages = await message_repo.get_pending_messages()
```
