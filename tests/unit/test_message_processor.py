"""
消息处理器测试
"""
import pytest
from unittest.mock import Mock, AsyncMock
from core.processor import MessageProcessor
from skills.base_skill import BaseSkill


class MockSkill(BaseSkill):
    """模拟技能"""
    
    def __init__(self, can_handle_result=True, execute_result="mock result"):
        super().__init__()
        self.can_handle_result = can_handle_result
        self.execute_result = execute_result
    
    def can_handle(self, message):
        return self.can_handle_result
    
    async def execute(self, message):
        return self.execute_result


class TestMessageProcessor:
    """消息处理器测试"""
    
    def setup_method(self):
        """初始化"""
        self.processor = MessageProcessor()
    
    def test_register_skill(self):
        """测试注册技能"""
        skill = MockSkill()
        
        self.processor.register_skill(skill)
        
        assert len(self.processor.skills) == 1
        assert self.processor.skills[0] == skill
    
    @pytest.mark.asyncio
    async def test_find_handler_returns_skill(self):
        """测试查找处理器返回技能"""
        skill = MockSkill(can_handle_result=True)
        self.processor.register_skill(skill)
        
        message = {"type": "text", "content": "test"}
        
        handler = self.processor.find_handler(message)
        
        assert handler == skill
    
    @pytest.mark.asyncio
    async def test_find_handler_returns_none(self):
        """测试查找处理器无匹配"""
        skill = MockSkill(can_handle_result=False)
        self.processor.register_skill(skill)
        
        message = {"type": "text", "content": "test"}
        
        handler = self.processor.find_handler(message)
        
        assert handler is None
    
    @pytest.mark.asyncio
    async def test_process_calls_skill(self):
        """测试处理调用技能"""
        skill = MockSkill(execute_result="success")
        self.processor.register_skill(skill)
        
        message = {"type": "text", "content": "test"}
        
        result = await self.processor.process(message)
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_process_no_handler(self):
        """测试无处理器"""
        skill = MockSkill(can_handle_result=False)
        self.processor.register_skill(skill)
        
        message = {"type": "text", "content": "test"}
        
        result = await self.processor.process(message)
        
        assert "无法处理" in result
    
    @pytest.mark.asyncio
    async def test_process_multiple_skills(self):
        """测试多个技能优先级"""
        skill1 = MockSkill(can_handle_result=False)
        skill2 = MockSkill(can_handle_result=True, execute_result="skill2")
        
        self.processor.register_skill(skill1)
        self.processor.register_skill(skill2)
        
        message = {"type": "text", "content": "test"}
        
        result = await self.processor.process(message)
        
        assert result == "skill2"
