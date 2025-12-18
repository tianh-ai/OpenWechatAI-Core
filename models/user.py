"""
用户和会话模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from datetime import datetime
from models.database import Base

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    
    # 用户信息
    platform = Column(String(50), nullable=False, comment="所属平台")
    platform_user_id = Column(String(255), nullable=False, comment="平台用户ID")
    username = Column(String(255), comment="用户名")
    nickname = Column(String(255), comment="昵称")
    
    # 用户属性
    is_blocked = Column(Boolean, default=False, comment="是否屏蔽")
    is_vip = Column(Boolean, default=False, comment="是否VIP")
    tags = Column(JSON, comment="用户标签")
    
    # 统计信息
    message_count = Column(Integer, default=0, comment="消息数量")
    last_message_at = Column(DateTime, comment="最后消息时间")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def __repr__(self):
        return f"<User(id={self.id}, platform={self.platform}, username={self.username})>"

class Conversation(Base):
    """对话上下文表"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True, comment="对话ID")
    
    # 对话信息
    platform = Column(String(50), nullable=False, comment="平台")
    user_id = Column(String(255), nullable=False, index=True, comment="用户ID")
    
    # 上下文内容
    context = Column(JSON, nullable=False, comment="对话上下文")
    
    # 元数据
    message_count = Column(Integer, default=0, comment="消息数量")
    last_message_at = Column(DateTime, comment="最后消息时间")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, messages={self.message_count})>"
