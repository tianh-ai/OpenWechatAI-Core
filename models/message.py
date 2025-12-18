"""
消息模型
存储接收和发送的消息
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models.database import Base

class MessageStatus(enum.Enum):
    """消息处理状态"""
    PENDING = "pending"       # 待处理
    PROCESSING = "processing" # 处理中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败

class MessageType(enum.Enum):
    """消息类型"""
    TEXT = "text"       # 文本
    IMAGE = "image"     # 图片
    VOICE = "voice"     # 语音
    VIDEO = "video"     # 视频
    FILE = "file"       # 文件
    LINK = "link"       # 链接
    LOCATION = "location" # 位置

class Message(Base):
    """消息表"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, comment="消息ID")
    
    # 消息基本信息
    platform = Column(String(50), nullable=False, index=True, comment="平台名称")
    sender = Column(String(255), nullable=False, index=True, comment="发送者")
    receiver = Column(String(255), comment="接收者")
    content = Column(Text, nullable=False, comment="消息内容")
    
    # 消息元数据
    message_type = Column(
        Enum(MessageType), 
        default=MessageType.TEXT, 
        nullable=False,
        comment="消息类型"
    )
    status = Column(
        Enum(MessageStatus), 
        default=MessageStatus.PENDING, 
        nullable=False,
        index=True,
        comment="处理状态"
    )
    
    # 时间戳
    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False,
        index=True,
        comment="创建时间"
    )
    processed_at = Column(DateTime, comment="处理时间")
    
    # 附加信息
    raw_data = Column(Text, comment="原始数据JSON")
    error_message = Column(Text, comment="错误信息")
    
    # 关联
    responses = relationship("MessageResponse", back_populates="message", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Message(id={self.id}, platform={self.platform}, sender={self.sender}, status={self.status.value})>"

class MessageResponse(Base):
    """消息响应表"""
    __tablename__ = "message_responses"
    
    id = Column(Integer, primary_key=True, index=True, comment="响应ID")
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False, index=True, comment="关联消息ID")
    
    # 响应信息
    skill_name = Column(String(100), comment="使用的技能名称")
    response_content = Column(Text, comment="响应内容")
    
    # 执行信息
    execution_time_ms = Column(Integer, comment="执行时间(毫秒)")
    success = Column(Boolean, default=True, comment="是否成功")
    error_message = Column(Text, comment="错误信息")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    
    # 关联
    message = relationship("Message", back_populates="responses")
    
    def __repr__(self):
        return f"<MessageResponse(id={self.id}, message_id={self.message_id}, skill={self.skill_name})>"
