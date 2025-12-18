"""
数据模型包 - MCP数据库模式
"""
from models.database import (
    MCPDatabaseInterface,
    MCPDatabaseClient,
    DatabaseOperation,
    get_mcp_db,
    init_db,
    init_mcp_database
)

# 数据模型定义保留用于类型提示和文档
# 实际存储使用MCP服务，不使用SQLAlchemy
from models.message import MessageStatus, MessageType

# 仓库层
from models.repositories import message_repo, rule_repo, user_repo

__all__ = [
    # MCP数据库接口
    "MCPDatabaseInterface",
    "MCPDatabaseClient",
    "DatabaseOperation",
    "get_mcp_db",
    "init_db",
    "init_mcp_database",
    
    # 枚举类型
    "MessageStatus",
    "MessageType",
    
    # 仓库实例
    "message_repo",
    "rule_repo",
    "user_repo",
]
