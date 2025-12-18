# MCP调用规则和集成规范

## MCP服务调用架构

```
┌─────────────────────────────────────────────────────────┐
│                     应用层                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ 消息处理 │  │ 规则引擎 │  │ AI技能   │              │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘              │
│        │             │              │                    │
│        └─────────────┼──────────────┘                    │
│                      │                                   │
│  ┌───────────────────▼────────────────────┐             │
│  │       仓库层 (repositories.py)         │             │
│  │  ┌─────────┐ ┌──────────┐ ┌────────┐  │             │
│  │  │Message  │ │Rule      │ │User    │  │             │
│  │  │Repo     │ │Repo      │ │Repo    │  │             │
│  │  └─────────┘ └──────────┘ └────────┘  │             │
│  └────────────────┬────────────────────────┘            │
│                   │                                      │
└───────────────────┼──────────────────────────────────────┘
                    │
                    │ MCP Protocol
                    │
┌───────────────────▼──────────────────────────────────────┐
│              MCP数据库客户端                             │
│  ┌──────────────────────────────────────────────┐       │
│  │   MCPDatabaseClient                          │       │
│  │   - create()   - read()   - update()         │       │
│  │   - delete()   - query()                     │       │
│  └──────────────────┬───────────────────────────┘       │
└─────────────────────┼───────────────────────────────────┘
                      │
                      │ HTTP/WebSocket
                      │
┌─────────────────────▼───────────────────────────────────┐
│            外部MCP数据库服务                             │
│  Endpoint: http://localhost:3000/mcp                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                 │
│  │Messages │  │Rules    │  │Users    │                 │
│  │Table    │  │Table    │  │Table    │                 │
│  └─────────┘  └─────────┘  └─────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## MCP调用规则

### 1. 调用原则

1. **单一入口**：所有数据库操作必须通过MCP客户端
2. **异步优先**：所有MCP调用使用async/await
3. **错误处理**：所有调用必须包含try-except
4. **超时控制**：设置合理的超时时间（默认30秒）
5. **重试机制**：网络错误自动重试（最多3次）
6. **日志记录**：记录所有MCP调用和响应

### 2. 调用流程

```python
# 标准调用流程
async def process_message(message_data):
    try:
        # 1. 通过仓库层调用
        message = await message_repo.create(
            platform=message_data["platform"],
            sender=message_data["sender"],
            content=message_data["content"]
        )
        
        # 2. 处理逻辑
        result = await process_logic(message)
        
        # 3. 更新状态
        await message_repo.update_status(
            message["id"],
            "COMPLETED"
        )
        
        return result
        
    except MCPConnectionError as e:
        logger.error(f"MCP连接失败: {e}")
        # 降级处理
        return fallback_processing(message_data)
    
    except MCPTimeoutError as e:
        logger.error(f"MCP超时: {e}")
        # 重试或降级
        return retry_or_fallback()
```

### 3. 仓库层使用规范

#### 消息操作

```python
from models import message_repo

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
pending = await message_repo.get_pending_messages(
    platform="wechat",
    limit=10
)

# 更新状态
await message_repo.update_status(
    message_id=message["id"],
    status="COMPLETED"
)

# 查询用户消息
user_messages = await message_repo.get_by_sender(
    sender="user123",
    limit=20
)
```

#### 规则操作

```python
from models import rule_repo

# 获取启用的规则
enabled_rules = await rule_repo.get_all_enabled()

# 更新规则统计
await rule_repo.update_statistics(
    rule_id=rule["id"],
    success=True
)

# 记录执行日志
await rule_repo.log_execution(
    rule_id=rule["id"],
    message_content="触发消息",
    matched=True,
    executed=True,
    success=True,
    execution_result={"action": "replied"}
)
```

#### 用户操作

```python
from models import user_repo

# 获取或创建用户
user = await user_repo.get_or_create(
    platform="wechat",
    platform_user_id="wx_123",
    username="user123",
    nickname="张三"
)

# 增加消息计数
await user_repo.update_message_count(user["id"])

# 获取对话上下文
context = await user_repo.get_conversation_context(
    platform="wechat",
    user_id=user["id"]
)

# 更新对话上下文
await user_repo.update_conversation_context(
    platform="wechat",
    user_id=user["id"],
    context={"messages": [...]}
)
```

### 4. 直接MCP客户端调用（高级用法）

```python
from models import get_mcp_db

db = get_mcp_db()

# 自定义查询
results = await db.query(
    "messages",
    filters={
        "status": "PENDING",
        "created_at__gte": "2025-12-16T00:00:00Z"
    },
    order_by="-priority,created_at",
    limit=100,
    offset=0
)

# 批量操作（如果MCP支持）
for item in batch_data:
    await db.create("messages", item)
```

### 5. 错误处理规范

```python
from models.database import (
    MCPConnectionError,
    MCPTimeoutError,
    MCPAuthenticationError,
    MCPValidationError
)

async def safe_mcp_call():
    try:
        result = await message_repo.create(...)
        return result
    
    except MCPConnectionError as e:
        logger.error(f"MCP连接失败: {e}")
        # 重试逻辑
        return await retry_with_backoff()
    
    except MCPTimeoutError as e:
        logger.error(f"MCP超时: {e}")
        # 降级处理
        return fallback_handler()
    
    except MCPAuthenticationError as e:
        logger.error(f"MCP认证失败: {e}")
        # 刷新token或报警
        raise
    
    except MCPValidationError as e:
        logger.error(f"数据验证失败: {e}")
        # 数据清洗或修正
        return sanitize_and_retry()
    
    except Exception as e:
        logger.error(f"未知错误: {e}", exc_info=True)
        raise
```

### 6. 性能优化规范

#### 批量操作

```python
# 不推荐：循环调用
for message in messages:
    await message_repo.create(**message)

# 推荐：批量创建（如果MCP支持）
await message_repo.batch_create(messages)
```

#### 缓存使用

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedRuleRepo:
    def __init__(self):
        self._cache = {}
        self._cache_time = None
    
    async def get_all_enabled(self):
        # 缓存5分钟
        if self._cache_time and \
           datetime.now() - self._cache_time < timedelta(minutes=5):
            return self._cache
        
        # 从MCP获取
        rules = await rule_repo.get_all_enabled()
        self._cache = rules
        self._cache_time = datetime.now()
        
        return rules
```

### 7. 监控和日志

```python
import time
from loguru import logger

async def monitored_mcp_call(operation, *args, **kwargs):
    """监控MCP调用性能"""
    start_time = time.time()
    
    try:
        result = await operation(*args, **kwargs)
        
        duration = (time.time() - start_time) * 1000
        logger.info(
            f"MCP调用成功: {operation.__name__} "
            f"耗时: {duration:.2f}ms"
        )
        
        return result
    
    except Exception as e:
        duration = (time.time() - start_time) * 1000
        logger.error(
            f"MCP调用失败: {operation.__name__} "
            f"耗时: {duration:.2f}ms "
            f"错误: {e}"
        )
        raise
```

### 8. 测试规范

```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_mcp_client():
    """模拟MCP客户端"""
    client = AsyncMock()
    client.create.return_value = {
        "id": 1,
        "created_at": "2025-12-16T10:00:00Z"
    }
    return client

@pytest.mark.asyncio
async def test_message_creation(mock_mcp_client):
    """测试消息创建"""
    # 注入mock客户端
    message_repo.db = mock_mcp_client
    
    result = await message_repo.create(
        platform="wechat",
        sender="test",
        content="test"
    )
    
    assert result["id"] == 1
    mock_mcp_client.create.assert_called_once()
```

### 9. 配置管理

```python
# core/config.py
class Settings(BaseSettings):
    # MCP配置
    mcp_database_endpoint: str = "http://localhost:3000/mcp"
    mcp_database_api_key: Optional[str] = None
    mcp_database_timeout: int = 30
    mcp_database_retry_times: int = 3
    mcp_database_retry_delay: float = 1.0
    
    # 缓存配置
    mcp_cache_enabled: bool = True
    mcp_cache_ttl: int = 300  # 5分钟
```

### 10. 集成示例

完整的消息处理流程：

```python
async def handle_message(raw_message: dict):
    """完整的消息处理流程"""
    try:
        # 1. 创建消息记录
        message = await message_repo.create(
            platform=raw_message["platform"],
            sender=raw_message["sender"],
            receiver="bot",
            content=raw_message["content"],
            message_type=raw_message.get("type", "TEXT"),
            status="PENDING",
            raw_data=raw_message
        )
        
        # 2. 获取或创建用户
        user = await user_repo.get_or_create(
            platform=raw_message["platform"],
            platform_user_id=raw_message["sender"]
        )
        
        # 3. 更新用户消息计数
        await user_repo.update_message_count(user["id"])
        
        # 4. 获取匹配的规则
        rules = await rule_repo.get_all_enabled()
        
        # 5. 执行规则匹配和处理
        for rule in rules:
            if rule_matches(rule, message):
                result = await execute_rule(rule, message)
                
                # 6. 记录规则执行
                await rule_repo.log_execution(
                    rule_id=rule["id"],
                    message_content=message["content"],
                    matched=True,
                    executed=True,
                    success=result["success"],
                    execution_result=result
                )
                
                # 7. 更新规则统计
                await rule_repo.update_statistics(
                    rule_id=rule["id"],
                    success=result["success"]
                )
        
        # 8. 更新消息状态
        await message_repo.update_status(
            message["id"],
            "COMPLETED"
        )
        
        return {"status": "success", "message_id": message["id"]}
    
    except Exception as e:
        logger.error(f"消息处理失败: {e}", exc_info=True)
        
        # 标记为失败
        if message:
            await message_repo.update_status(
                message["id"],
                "FAILED",
                error_message=str(e)
            )
        
        raise
```

## 注意事项

1. **始终使用仓库层**：不要直接使用MCP客户端，除非有特殊需求
2. **异步上下文**：确保在async函数中调用
3. **错误处理**：所有调用都要有完善的错误处理
4. **性能监控**：记录调用耗时，识别性能瓶颈
5. **数据验证**：发送到MCP前验证数据格式
6. **版本兼容**：MCP API可能升级，注意兼容性
7. **降级方案**：MCP不可用时的备用方案
8. **测试覆盖**：所有MCP调用都要有单元测试
