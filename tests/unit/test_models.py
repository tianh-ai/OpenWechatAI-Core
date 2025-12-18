"""
数据库模型测试
"""
import pytest
from datetime import datetime
from models import Message, MessageResponse, Rule, RuleLog, User, Conversation
from models.message import MessageStatus, MessageType


class TestMessageModel:
    """消息模型测试"""
    
    def test_create_message(self, db_session):
        """测试创建消息"""
        message = Message(
            platform="wechat",
            sender="test_user",
            receiver="bot",
            content="测试消息",
            message_type=MessageType.TEXT,
            status=MessageStatus.PENDING
        )
        
        db_session.add(message)
        db_session.commit()
        
        assert message.id is not None
        assert message.created_at is not None
    
    def test_message_with_response(self, db_session):
        """测试消息和响应关联"""
        message = Message(
            platform="wechat",
            sender="test_user",
            receiver="bot",
            content="测试",
            message_type=MessageType.TEXT
        )
        db_session.add(message)
        db_session.flush()
        
        response = MessageResponse(
            message_id=message.id,
            skill_name="echo",
            response_content="回复内容",
            execution_time_ms=100,
            success=True
        )
        db_session.add(response)
        db_session.commit()
        
        assert len(message.responses) == 1
        assert message.responses[0].skill_name == "echo"


class TestRuleModel:
    """规则模型测试"""
    
    def test_create_rule(self, db_session):
        """测试创建规则"""
        rule = Rule(
            name="test_rule",
            description="测试规则",
            priority=10,
            enabled=True,
            conditions={"content_contains": "hello"},
            actions={"action": "reply", "message": "hi"}
        )
        
        db_session.add(rule)
        db_session.commit()
        
        assert rule.id is not None
        assert rule.trigger_count == 0
    
    def test_rule_with_log(self, db_session):
        """测试规则和日志关联"""
        rule = Rule(
            name="test_rule",
            description="测试",
            priority=1,
            conditions={},
            actions={}
        )
        db_session.add(rule)
        db_session.flush()
        
        log = RuleLog(
            rule_id=rule.id,
            message_content="测试消息",
            matched=True,
            executed=True,
            success=True,
            execution_result={"status": "ok"}
        )
        db_session.add(log)
        db_session.commit()
        
        assert len(rule.logs) == 1


class TestUserModel:
    """用户模型测试"""
    
    def test_create_user(self, db_session):
        """测试创建用户"""
        user = User(
            platform="wechat",
            platform_user_id="wx_123",
            username="testuser",
            nickname="测试用户"
        )
        
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.message_count == 0
        assert user.is_blocked is False
    
    def test_user_conversation(self, db_session):
        """测试用户对话上下文"""
        user = User(
            platform="wechat",
            platform_user_id="wx_123",
            username="testuser"
        )
        db_session.add(user)
        db_session.flush()
        
        conv = Conversation(
            platform="wechat",
            user_id=user.id,
            context={"messages": []},
            message_count=0
        )
        db_session.add(conv)
        db_session.commit()
        
        # 查询
        found_conv = db_session.query(Conversation).filter_by(user_id=user.id).first()
        assert found_conv is not None
        assert found_conv.user_id == user.id
