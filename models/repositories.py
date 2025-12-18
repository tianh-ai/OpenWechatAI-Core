"""
数据仓库层 - 使用MCP数据库服务

提供高级数据访问接口，封装MCP数据库操作
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger
from models.database import get_mcp_db
from models.message import MessageStatus, MessageType


class MessageRepository:
    """消息仓库"""
    
    def __init__(self):
        self.db = get_mcp_db()
        self.table = "messages"
    
    async def create(
        self,
        platform: str,
        sender: str,
        receiver: str,
        content: str,
        message_type: str = "TEXT",
        status: str = "PENDING",
        raw_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """创建消息记录"""
        data = {
            "platform": platform,
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "message_type": message_type,
            "status": status,
            "raw_data": raw_data or {}
        }
        
        return await self.db.create(self.table, data)
    
    async def get_by_id(self, message_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取消息"""
        return await self.db.read(self.table, message_id)
    
    async def update_status(
        self,
        message_id: int,
        status: str,
        error_message: str = None
    ) -> bool:
        """更新消息状态"""
        data = {"status": status}
        if error_message:
            data["error_message"] = error_message
        
        return await self.db.update(self.table, message_id, data)
    
    async def get_pending_messages(
        self,
        platform: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """获取待处理消息"""
        filters = {"status": MessageStatus.PENDING.value}
        if platform:
            filters["platform"] = platform
        
        return await self.db.query(
            self.table,
            filters=filters,
            order_by="-created_at",
            limit=limit
        )
    
    async def get_by_sender(
        self,
        sender: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """获取某个发送者的消息"""
        return await self.db.query(
            self.table,
            filters={"sender": sender},
            order_by="-created_at",
            limit=limit
        )


class RuleRepository:
    """规则仓库"""
    
    def __init__(self):
        self.db = get_mcp_db()
        self.table = "rules"
        self.log_table = "rule_logs"
    
    async def create(
        self,
        name: str,
        description: str,
        priority: int,
        conditions: Dict[str, Any],
        actions: Dict[str, Any],
        enabled: bool = True
    ) -> Dict[str, Any]:
        """创建规则"""
        data = {
            "name": name,
            "description": description,
            "priority": priority,
            "enabled": enabled,
            "conditions": conditions,
            "actions": actions,
            "trigger_count": 0,
            "success_count": 0,
            "failure_count": 0
        }
        
        return await self.db.create(self.table, data)
    
    async def get_all_enabled(self) -> List[Dict[str, Any]]:
        """获取所有启用的规则"""
        return await self.db.query(
            self.table,
            filters={"enabled": True},
            order_by="-priority"
        )
    
    async def update_statistics(
        self,
        rule_id: int,
        success: bool
    ) -> bool:
        """更新规则统计"""
        # 先读取当前值
        rule = await self.db.read(self.table, rule_id)
        if not rule:
            return False
        
        # 更新计数
        data = {
            "trigger_count": rule.get("trigger_count", 0) + 1,
            "last_triggered_at": datetime.utcnow().isoformat()
        }
        
        if success:
            data["success_count"] = rule.get("success_count", 0) + 1
        else:
            data["failure_count"] = rule.get("failure_count", 0) + 1
        
        return await self.db.update(self.table, rule_id, data)
    
    async def log_execution(
        self,
        rule_id: int,
        message_content: str,
        matched: bool,
        executed: bool,
        success: bool,
        execution_result: Dict[str, Any] = None,
        error_message: str = None
    ) -> Dict[str, Any]:
        """记录规则执行日志"""
        data = {
            "rule_id": rule_id,
            "message_content": message_content[:500],
            "matched": matched,
            "executed": executed,
            "success": success,
            "execution_result": execution_result or {},
            "error_message": error_message
        }
        
        return await self.db.create(self.log_table, data)


class UserRepository:
    """用户仓库"""
    
    def __init__(self):
        self.db = get_mcp_db()
        self.table = "users"
        self.conversation_table = "conversations"
    
    async def get_or_create(
        self,
        platform: str,
        platform_user_id: str,
        username: str = None,
        nickname: str = None
    ) -> Dict[str, Any]:
        """获取或创建用户"""
        # 先尝试查询
        users = await self.db.query(
            self.table,
            filters={
                "platform": platform,
                "platform_user_id": platform_user_id
            },
            limit=1
        )
        
        if users:
            return users[0]
        
        # 不存在则创建
        data = {
            "platform": platform,
            "platform_user_id": platform_user_id,
            "username": username,
            "nickname": nickname,
            "is_blocked": False,
            "is_vip": False,
            "tags": [],
            "message_count": 0
        }
        
        return await self.db.create(self.table, data)
    
    async def update_message_count(self, user_id: int) -> bool:
        """增加用户消息计数"""
        user = await self.db.read(self.table, user_id)
        if not user:
            return False
        
        return await self.db.update(self.table, user_id, {
            "message_count": user.get("message_count", 0) + 1,
            "last_message_at": datetime.utcnow().isoformat()
        })
    
    async def get_conversation_context(
        self,
        platform: str,
        user_id: int
    ) -> Optional[Dict[str, Any]]:
        """获取对话上下文"""
        conversations = await self.db.query(
            self.conversation_table,
            filters={
                "platform": platform,
                "user_id": user_id
            },
            limit=1
        )
        
        return conversations[0] if conversations else None
    
    async def update_conversation_context(
        self,
        platform: str,
        user_id: int,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """更新对话上下文"""
        existing = await self.get_conversation_context(platform, user_id)
        
        if existing:
            await self.db.update(
                self.conversation_table,
                existing["id"],
                {"context": context}
            )
            return existing
        else:
            return await self.db.create(self.conversation_table, {
                "platform": platform,
                "user_id": user_id,
                "context": context,
                "message_count": 0
            })


# 全局仓库实例
message_repo = MessageRepository()
rule_repo = RuleRepository()
user_repo = UserRepository()
