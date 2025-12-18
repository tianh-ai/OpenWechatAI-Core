"""
AI模型接口定义
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Message:
    """聊天消息"""
    role: str  # system, user, assistant
    content: str


@dataclass
class AIResponse:
    """AI响应"""
    content: str
    model: str
    tokens_used: int
    finish_reason: str
    cost: float = 0.0


class IAIModel(ABC):
    """AI模型接口"""
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """
        聊天接口
        
        Args:
            messages: 消息历史
            temperature: 温度参数（0-1）
            max_tokens: 最大生成token数
            **kwargs: 其他参数
            
        Returns:
            AI响应
        """
        pass
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """
        文本补全接口
        
        Args:
            prompt: 提示词
            temperature: 温度参数
            max_tokens: 最大生成token数
            **kwargs: 其他参数
            
        Returns:
            AI响应
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass
    
    @abstractmethod
    def get_max_context_length(self) -> int:
        """获取最大上下文长度"""
        pass
