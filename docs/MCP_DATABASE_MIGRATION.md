# MCP数据库架构变更总结

## 变更说明

已将项目从直接使用PostgreSQL/SQLAlchemy改为通过外部MCP数据库服务调用。

## 修改的文件

### 1. `models/database.py`
- ✅ 移除SQLAlchemy引擎和会话配置
- ✅ 新增 `MCPDatabaseInterface` 抽象接口
- ✅ 新增 `MCPDatabaseClient` 模拟实现
- ✅ 新增 `get_mcp_db()` 全局客户端获取函数
- ✅ 新增 `init_mcp_database()` 异步初始化函数

### 2. `models/__init__.py`
- ✅ 更新导出项，移除SQLAlchemy相关
- ✅ 导出MCP数据库接口和仓库

### 3. `models/repositories.py` (新增)
- ✅ `MessageRepository` - 消息数据仓库
- ✅ `RuleRepository` - 规则数据仓库
- ✅ `UserRepository` - 用户数据仓库
- ✅ 全局仓库实例: `message_repo`, `rule_repo`, `user_repo`

### 4. `core/config.py`
- ✅ 移除 `database_url` 配置
- ✅ 新增 `mcp_database_endpoint` 配置
- ✅ 新增 `mcp_database_api_key` 配置
- ✅ 新增 `mcp_database_timeout` 配置

### 5. `.env.example`
- ✅ 更新配置示例，使用MCP配置替代数据库URL

### 6. 文档
- ✅ `docs/MCP_DATABASE_REQUIREMENTS.md` - 完整需求文档
- ✅ `docs/MCP_DATABASE_USAGE.md` - 使用说明
- ✅ `docs/MCP_DATABASE_MIGRATION.md` - 本文档

## 数据模型保留

以下文件保留作为数据结构定义和类型提示：
- `models/message.py` - MessageStatus, MessageType 枚举
- `models/rule.py` - 规则条件和动作类
- `models/user.py` - 用户数据结构

这些文件不再使用SQLAlchemy ORM，但保留了数据结构定义供参考。

## MCP接口定义

### 基础操作
```python
class MCPDatabaseInterface(ABC):
    async def create(table: str, data: dict) -> dict
    async def read(table: str, id: int) -> dict | None
    async def update(table: str, id: int, data: dict) -> bool
    async def delete(table: str, id: int) -> bool
    async def query(table, filters, order_by, limit, offset) -> list[dict]
```

### 支持的表
- `messages` - 消息记录
- `message_responses` - 消息响应
- `rules` - 自动化规则
- `rule_logs` - 规则执行日志
- `users` - 用户信息
- `conversations` - 对话上下文

## 使用方式变更

### 旧方式（SQLAlchemy）
```python
from models import Message, get_db_context

with get_db_context() as db:
    message = Message(platform="wechat", sender="user", content="hi")
    db.add(message)
    db.commit()
```

### 新方式（MCP仓库）
```python
from models import message_repo

message = await message_repo.create(
    platform="wechat",
    sender="user",
    content="hi"
)
```

### 直接使用MCP客户端
```python
from models import get_mcp_db

db = get_mcp_db()
message = await db.create("messages", {
    "platform": "wechat",
    "sender": "user",
    "content": "hi"
})
```

## 待实现功能

### 当前状态
- ✅ 接口定义完成
- ✅ 仓库层实现
- ✅ 配置项更新
- ✅ 文档完善

### 待完成
- ⏳ MCP客户端实际连接逻辑
- ⏳ HTTP/WebSocket通信
- ⏳ 认证和授权
- ⏳ 错误重试机制
- ⏳ 本地缓存层
- ⏳ 批量操作
- ⏳ 事务支持

## 部署步骤

1. **配置MCP服务端点**
   ```bash
   export MCP_DATABASE_ENDPOINT=http://your-mcp-service:3000/mcp
   export MCP_DATABASE_API_KEY=your_api_key
   ```

2. **初始化MCP连接**
   ```python
   from models import init_mcp_database
   await init_mcp_database()
   ```

3. **使用仓库访问数据**
   ```python
   from models import message_repo
   messages = await message_repo.get_pending_messages()
   ```

## 回滚计划

如需回滚到SQLAlchemy模式：

1. 恢复 `models/database.py` 中的SQLAlchemy配置
2. 恢复 `models/__init__.py` 导出项
3. 恢复 `core/config.py` 中的 `database_url` 配置
4. 使用 `git revert` 回退变更

## 兼容性注意

- 所有数据库操作现在都是异步的（`async/await`）
- 需要确保调用代码在异步上下文中
- 返回值从ORM对象变为字典
- 需要手动管理数据验证

## 测试建议

1. 单元测试需要mock MCP客户端
2. 集成测试需要部署MCP测试服务
3. 性能测试比较MCP vs 直连数据库

## 参考文档

- [MCP数据库需求](./MCP_DATABASE_REQUIREMENTS.md)
- [MCP数据库使用指南](./MCP_DATABASE_USAGE.md)
- [Model Context Protocol规范](https://modelcontextprotocol.io/)
