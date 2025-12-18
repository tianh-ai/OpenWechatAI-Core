"""
AI聊天技能 - 使用AI模型进行智能对话
"""
from typing import Dict, Any
from loguru import logger
from skills.base_skill import BaseSkill
from implementations.ai.ai_router import get_ai_router
from interfaces.ai_model import Message


class AIChatSkill(BaseSkill):
    """AI聊天技能"""
    
    def __init__(self, model: str = None, system_prompt: str = None):
        """
        初始化AI聊天技能
        
        Args:
            model: AI模型名称（None则使用默认）
            system_prompt: 系统提示词
        """
        super().__init__()
        self.model = model
        self.system_prompt = system_prompt or "你是一个友好、专业的AI助手。请用简洁明了的方式回答用户的问题。"
        self.ai_router = get_ai_router()
        
        # 用户对话上下文（简单内存存储，实际应使用数据库）
        self.conversations: Dict[str, list] = {}
    
    def can_handle(self, message: Dict[str, Any]) -> bool:
        """
        判断是否可以处理该消息
        
        Args:
            message: 消息字典
            
        Returns:
            是否可以处理
        """
        # AI聊天技能可以处理所有文本消息（作为兜底）
        return message.get("type") == "text" and bool(message.get("content"))
    
    async def execute(self, message: Dict[str, Any]) -> str:
        """
        执行AI聊天
        
        Args:
            message: 消息字典
            
        Returns:
            AI回复内容
        """
        sender = message.get("sender", "unknown")
        content = message.get("content", "")
        
        try:
            # 获取或创建对话上下文
            if sender not in self.conversations:
                self.conversations[sender] = [
                    Message(role="system", content=self.system_prompt)
                ]
            
            # 添加用户消息
            self.conversations[sender].append(
                Message(role="user", content=content)
            )
            
            # 限制上下文长度（保留最近10轮对话）
            if len(self.conversations[sender]) > 21:  # 1 system + 10*2 messages
                self.conversations[sender] = [
                    self.conversations[sender][0]  # 保留system
                ] + self.conversations[sender][-20:]  # 最近10轮
            
            # 调用AI模型
            response = await self.ai_router.chat(
                messages=self.conversations[sender],
                model=self.model,
                temperature=0.7,
                max_tokens=500
            )
            
            # 添加AI回复到上下文
            self.conversations[sender].append(
                Message(role="assistant", content=response.content)
            )
            
            logger.info(
                f"AI聊天: {sender} | "
                f"模型: {response.model} | "
                f"Tokens: {response.tokens_used} | "
                f"成本: ${response.cost:.4f}"
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"AI聊天失败: {e}", exc_info=True)
            return "抱歉，我现在无法回答您的问题。请稍后再试。"
    
    def clear_context(self, sender: str):
        """清除用户的对话上下文"""
        if sender in self.conversations:
            del self.conversations[sender]
            logger.info(f"已清除 {sender} 的对话上下文")
