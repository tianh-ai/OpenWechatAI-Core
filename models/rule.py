"""
规则模型
存储自动化规则配置
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from datetime import datetime
from models.database import Base

class Rule(Base):
    """规则表"""
    __tablename__ = "rules"
    
    id = Column(Integer, primary_key=True, index=True, comment="规则ID")
    
    # 规则基本信息
    name = Column(String(255), nullable=False, unique=True, comment="规则名称")
    description = Column(Text, comment="规则描述")
    priority = Column(Integer, default=0, index=True, comment="优先级，数字越大优先级越高")
    enabled = Column(Boolean, default=True, index=True, comment="是否启用")
    
    # 规则条件和动作（JSON格式）
    conditions = Column(JSON, nullable=False, comment="触发条件")
    actions = Column(JSON, nullable=False, comment="执行动作")
    
    # 统计信息
    trigger_count = Column(Integer, default=0, comment="触发次数")
    success_count = Column(Integer, default=0, comment="成功次数")
    failure_count = Column(Integer, default=0, comment="失败次数")
    last_triggered_at = Column(DateTime, comment="最后触发时间")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    def __repr__(self):
        return f"<Rule(id={self.id}, name={self.name}, priority={self.priority}, enabled={self.enabled})>"

class RuleLog(Base):
    """规则执行日志表"""
    __tablename__ = "rule_logs"
    
    id = Column(Integer, primary_key=True, index=True, comment="日志ID")
    rule_id = Column(Integer, nullable=False, index=True, comment="规则ID")
    
    # 执行信息
    message_content = Column(Text, comment="触发消息内容")
    matched = Column(Boolean, default=False, comment="是否匹配")
    executed = Column(Boolean, default=False, comment="是否执行")
    success = Column(Boolean, comment="是否成功")
    
    # 详细信息
    execution_result = Column(JSON, comment="执行结果")
    error_message = Column(Text, comment="错误信息")
    execution_time_ms = Column(Integer, comment="执行时间(毫秒)")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True, comment="创建时间")
    
    def __repr__(self):
        return f"<RuleLog(id={self.id}, rule_id={self.rule_id}, success={self.success})>"
