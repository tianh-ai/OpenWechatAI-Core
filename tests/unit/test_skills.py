"""
技能测试
"""
import pytest
from skills.echo_skill import EchoSkill
from skills.ai_chat_skill import AIChatSkill


class TestEchoSkill:
    """Echo技能测试"""
    
    def setup_method(self):
        """初始化"""
        self.skill = EchoSkill()
    
    def test_can_handle_text_message(self):
        """测试处理文本消息"""
        message = {
            "type": "text",
            "content": "echo test"
        }
        
        assert self.skill.can_handle(message) is True
    
    def test_cannot_handle_non_text(self):
        """测试不处理非文本消息"""
        message = {
            "type": "image",
            "content": ""
        }
        
        assert self.skill.can_handle(message) is False
    
    def test_cannot_handle_without_echo_prefix(self):
        """测试不处理没有echo前缀的消息"""
        message = {
            "type": "text",
            "content": "hello world"
        }
        
        assert self.skill.can_handle(message) is False
    
    @pytest.mark.asyncio
    async def test_execute_returns_content(self):
        """测试执行返回内容"""
        message = {
            "type": "text",
            "content": "echo hello"
        }
        
        result = await self.skill.execute(message)
        
        assert result == "hello"
    
    @pytest.mark.asyncio
    async def test_execute_strips_whitespace(self):
        """测试执行去除空格"""
        message = {
            "type": "text",
            "content": "echo   hello world   "
        }
        
        result = await self.skill.execute(message)
        
        assert result == "hello world"


class TestAIChatSkill:
    """AI聊天技能测试"""
    
    def test_can_handle_text(self, mock_ai_router):
        """测试处理文本消息"""
        skill = AIChatSkill()
        skill.ai_router = mock_ai_router
        
        message = {
            "type": "text",
            "content": "你好"
        }
        
        assert skill.can_handle(message) is True
    
    def test_cannot_handle_empty(self, mock_ai_router):
        """测试不处理空消息"""
        skill = AIChatSkill()
        skill.ai_router = mock_ai_router
        
        message = {
            "type": "text",
            "content": ""
        }
        
        assert skill.can_handle(message) is False
    
    @pytest.mark.asyncio
    async def test_execute_calls_ai(self, mock_ai_router):
        """测试执行调用AI"""
        skill = AIChatSkill()
        skill.ai_router = mock_ai_router
        
        message = {
            "sender": "test_user",
            "type": "text",
            "content": "你好"
        }
        
        result = await skill.execute(message)
        
        assert mock_ai_router.chat.called
        assert result == "AI回复内容"
    
    def test_clear_context(self, mock_ai_router):
        """测试清除上下文"""
        skill = AIChatSkill()
        skill.ai_router = mock_ai_router
        
        # 添加对话
        sender = "test_user"
        skill.conversations[sender] = ["message1", "message2"]
        
        # 清除
        skill.clear_context(sender)
        
        assert sender not in skill.conversations
