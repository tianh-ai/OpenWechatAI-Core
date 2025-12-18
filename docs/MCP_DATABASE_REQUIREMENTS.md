# MCP数据库服务需求文档

## 概述

本项目使用外部MCP (Model Context Protocol) 数据库服务，而非直接配置本地数据库连接。通过MCP协议与数据库服务通信，实现数据的增删改查。

## 服务端点

- **MCP数据库服务地址**: 待配置
- **协议**: HTTP/HTTPS 或 WebSocket
- **认证方式**: API Key / OAuth 2.0

## 数据模型需求

### 1. Messages (消息表)

**用途**: 存储微信消息记录

```json
{
  "id": "integer (自增主键)",
  "platform": "string (平台: wechat)",
  "sender": "string (发送者ID)",
  "receiver": "string (接收者ID)",
  "content": "text (消息内容)",
  "message_type": "enum (TEXT, IMAGE, VOICE, VIDEO, FILE, LINK, LOCATION)",
  "status": "enum (PENDING, PROCESSING, COMPLETED, FAILED)",
  "raw_data": "json (原始消息数据)",
  "error_message": "text (错误信息)",
  "created_at": "timestamp (创建时间)",
  "updated_at": "timestamp (更新时间)"
}
```

**索引**:
- `platform, sender, created_at`
- `status, created_at`

---

### 2. MessageResponses (消息响应表)

**用途**: 存储AI处理消息的响应结果

```json
{
  "id": "integer (自增主键)",
  "message_id": "integer (外键 -> messages.id)",
  "skill_name": "string (技能名称)",
  "response_content": "text (响应内容)",
  "execution_time_ms": "integer (执行时间毫秒)",
  "success": "boolean (是否成功)",
  "error_message": "text (错误信息)",
  "created_at": "timestamp (创建时间)"
}
```

**关系**:
- `message_id` → `messages.id` (一对多)

---

### 3. Rules (规则表)

**用途**: 存储自动化规则配置

```json
{
  "id": "integer (自增主键)",
  "name": "string unique (规则名称)",
  "description": "text (规则描述)",
  "priority": "integer (优先级, 数字越大越优先)",
  "enabled": "boolean (是否启用)",
  "conditions": "json (匹配条件)",
  "actions": "json (执行动作)",
  "trigger_count": "integer (触发次数)",
  "success_count": "integer (成功次数)",
  "failure_count": "integer (失败次数)",
  "last_triggered_at": "timestamp (最后触发时间)",
  "created_at": "timestamp (创建时间)",
  "updated_at": "timestamp (更新时间)"
}
```

**条件示例** (conditions):
```json
{
  "platform": "wechat",
  "sender": "user_pattern",
  "content_contains": "紧急",
  "content_regex": "^(你好|hi).*",
  "time_range": "09:00-18:00"
}
```

**动作示例** (actions):
```json
{
  "action": "auto_reply",
  "message": "收到您的消息",
  "use_ai": true,
  "ai_model": "gpt-4"
}
```

---

### 4. RuleLogs (规则日志表)

**用途**: 记录规则执行历史

```json
{
  "id": "integer (自增主键)",
  "rule_id": "integer (外键 -> rules.id)",
  "message_content": "text (触发消息内容)",
  "matched": "boolean (是否匹配)",
  "executed": "boolean (是否执行)",
  "success": "boolean (是否成功)",
  "execution_result": "json (执行结果)",
  "error_message": "text (错误信息)",
  "created_at": "timestamp (创建时间)"
}
```

---

### 5. Users (用户表)

**用途**: 存储微信用户信息

```json
{
  "id": "integer (自增主键)",
  "platform": "string (平台)",
  "platform_user_id": "string (平台用户ID)",
  "username": "string (用户名)",
  "nickname": "string (昵称)",
  "is_blocked": "boolean (是否拉黑)",
  "is_vip": "boolean (是否VIP)",
  "tags": "json (用户标签)",
  "message_count": "integer (消息数)",
  "last_message_at": "timestamp (最后消息时间)",
  "created_at": "timestamp (创建时间)",
  "updated_at": "timestamp (更新时间)"
}
```

**唯一索引**:
- `platform, platform_user_id`

---

### 6. Conversations (对话上下文表)

**用途**: 存储AI对话上下文

```json
{
  "id": "integer (自增主键)",
  "platform": "string (平台)",
  "user_id": "integer (外键 -> users.id)",
  "context": "json (对话上下文)",
  "message_count": "integer (消息数)",
  "created_at": "timestamp (创建时间)",
  "updated_at": "timestamp (更新时间)"
}
```

**索引**:
- `platform, user_id`

---

## MCP接口定义

### 基础操作

#### 1. Create (创建记录)

```python
async def create(table: str, data: dict) -> dict
```

**请求**:
```json
{
  "operation": "create",
  "table": "messages",
  "data": {
    "platform": "wechat",
    "sender": "user123",
    "content": "你好",
    "message_type": "TEXT",
    "status": "PENDING"
  }
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "platform": "wechat",
    "sender": "user123",
    "content": "你好",
    "created_at": "2025-01-16T10:00:00Z"
  }
}
```

---

#### 2. Read (读取记录)

```python
async def read(table: str, id: int) -> dict | None
```

**请求**:
```json
{
  "operation": "read",
  "table": "messages",
  "id": 1
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "platform": "wechat",
    "sender": "user123",
    "content": "你好",
    "status": "COMPLETED"
  }
}
```

---

#### 3. Update (更新记录)

```python
async def update(table: str, id: int, data: dict) -> bool
```

**请求**:
```json
{
  "operation": "update",
  "table": "messages",
  "id": 1,
  "data": {
    "status": "COMPLETED"
  }
}
```

**响应**:
```json
{
  "success": true,
  "updated": true
}
```

---

#### 4. Delete (删除记录)

```python
async def delete(table: str, id: int) -> bool
```

**请求**:
```json
{
  "operation": "delete",
  "table": "messages",
  "id": 1
}
```

**响应**:
```json
{
  "success": true,
  "deleted": true
}
```

---

#### 5. Query (查询记录)

```python
async def query(
    table: str,
    filters: dict = None,
    order_by: str = None,
    limit: int = None,
    offset: int = None
) -> list[dict]
```

**请求**:
```json
{
  "operation": "query",
  "table": "messages",
  "filters": {
    "status": "PENDING",
    "platform": "wechat"
  },
  "order_by": "-created_at",
  "limit": 10,
  "offset": 0
}
```

**响应**:
```json
{
  "success": true,
  "data": [
    {
      "id": 5,
      "platform": "wechat",
      "sender": "user456",
      "content": "测试消息",
      "status": "PENDING",
      "created_at": "2025-01-16T10:05:00Z"
    }
  ],
  "total": 1
}
```

---

## 过滤器语法

支持以下过滤操作符:

- **等于**: `{"status": "PENDING"}`
- **不等于**: `{"status__ne": "COMPLETED"}`
- **大于**: `{"id__gt": 100}`
- **大于等于**: `{"id__gte": 100}`
- **小于**: `{"id__lt": 200}`
- **小于等于**: `{"id__lte": 200}`
- **包含**: `{"content__contains": "紧急"}`
- **正则**: `{"sender__regex": "^user.*"}`
- **在列表中**: `{"status__in": ["PENDING", "PROCESSING"]}`
- **时间范围**: `{"created_at__range": ["2025-01-01", "2025-01-31"]}`

---

## 排序语法

- **升序**: `"created_at"` 或 `"+created_at"`
- **降序**: `"-created_at"`
- **多字段**: `"-priority,created_at"`

---

## 错误处理

**错误响应格式**:
```json
{
  "success": false,
  "error": {
    "code": "RECORD_NOT_FOUND",
    "message": "Record with id=123 not found in table 'messages'",
    "details": {}
  }
}
```

**错误代码**:
- `INVALID_TABLE` - 表名无效
- `RECORD_NOT_FOUND` - 记录不存在
- `VALIDATION_ERROR` - 数据验证失败
- `PERMISSION_DENIED` - 权限不足
- `INTERNAL_ERROR` - 服务器内部错误

---

## 使用示例

```python
from models.database import get_mcp_db

# 获取MCP数据库客户端
db = get_mcp_db()

# 创建消息
message = await db.create("messages", {
    "platform": "wechat",
    "sender": "user123",
    "content": "你好",
    "message_type": "TEXT",
    "status": "PENDING"
})

# 查询未读消息
pending_messages = await db.query(
    "messages",
    filters={"status": "PENDING"},
    order_by="-created_at",
    limit=10
)

# 更新消息状态
await db.update("messages", message["id"], {
    "status": "COMPLETED"
})

# 创建响应记录
await db.create("message_responses", {
    "message_id": message["id"],
    "skill_name": "echo",
    "response_content": "你好",
    "execution_time_ms": 50,
    "success": True
})
```

---

## 配置要求

在 `.env` 文件中添加:

```bash
# MCP数据库服务配置
MCP_DATABASE_ENDPOINT=http://localhost:3000/mcp
MCP_DATABASE_API_KEY=your_api_key_here
MCP_DATABASE_TIMEOUT=30
```

---

## 待实现功能

1. ✅ 接口定义完成
2. ⏳ MCP客户端连接实现
3. ⏳ 认证和授权
4. ⏳ 错误重试机制
5. ⏳ 数据缓存层
6. ⏳ 批量操作支持
7. ⏳ 事务支持
8. ⏳ 连接池管理

---

## 下一步

1. 部署MCP数据库服务
2. 配置服务端点和API Key
3. 实现 `MCPDatabaseClient` 的实际连接逻辑
4. 编写集成测试
5. 性能优化和监控
