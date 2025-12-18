"""
集成测试 - 消息流程
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from core.processor import MessageProcessor
from skills.echo_skill import EchoSkill
from models import Message, MessageResponse
from models.message import MessageStatus, MessageType


@pytest.mark.integration
class TestMessageFlow:
    """消息流程集成测试"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_echo(self, db_session):
        """测试端到端Echo流程"""
        # 1. 创建消息
        message_data = {
            "platform": "wechat",
            "sender": "test_user",
            "receiver": "bot",
            "content": "echo hello",
            "type": "text"
        }
        
        # 2. 保存到数据库
        db_message = Message(
            platform=message_data["platform"],
            sender=message_data["sender"],
            receiver=message_data["receiver"],
            content=message_data["content"],
            message_type=MessageType.TEXT,
            status=MessageStatus.PENDING
        )
        db_session.add(db_message)
        db_session.commit()
        
        # 3. 处理消息
        processor = MessageProcessor()
        processor.register_skill(EchoSkill())
        
        result = await processor.process(message_data)
        
        # 4. 验证结果
        assert result == "hello"
        
        # 5. 保存响应
        response = MessageResponse(
            message_id=db_message.id,
            skill_name="EchoSkill",
            response_content=result,
            execution_time_ms=50,
            success=True
        )
        db_session.add(response)
        
        # 6. 更新消息状态
        db_message.status = MessageStatus.COMPLETED
        db_session.commit()
        
        # 7. 验证数据库
        assert db_message.status == MessageStatus.COMPLETED
        assert len(db_message.responses) == 1
        assert db_message.responses[0].response_content == "hello"
    
    @pytest.mark.asyncio
    async def test_message_flow_with_failure(self, db_session):
        """测试失败消息流程"""
        # 创建会失败的消息
        message_data = {
            "platform": "wechat",
            "sender": "test_user",
            "receiver": "bot",
            "content": "invalid command",
            "type": "text"
        }
        
        db_message = Message(
            platform=message_data["platform"],
            sender=message_data["sender"],
            receiver=message_data["receiver"],
            content=message_data["content"],
            message_type=MessageType.TEXT,
            status=MessageStatus.PROCESSING
        )
        db_session.add(db_message)
        db_session.commit()
        
        # 处理（没有匹配的技能）
        processor = MessageProcessor()
        processor.register_skill(EchoSkill())  # 只有echo技能
        
        result = await processor.process(message_data)
        
        # 验证返回错误消息
        assert "无法处理" in result
        
        # 更新为失败状态
        db_message.status = MessageStatus.FAILED
        db_message.error_message = "No matching skill"
        db_session.commit()
        
        assert db_message.status == MessageStatus.FAILED
        assert db_message.error_message is not None
