"""
OpenAI GPT模型实现
"""
import openai
from typing import List, Dict, Any
from loguru import logger
from interfaces.ai_model import IAIModel, Message, AIResponse
from core.config import settings


class OpenAIModel(IAIModel):
    """OpenAI GPT模型"""
    
    # 模型价格（USD per 1K tokens）
    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-32k": {"input": 0.06, "output": 0.12},
        "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
        "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004},
    }
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str = None):
        """
        初始化OpenAI模型
        
        Args:
            model: 模型名称
            api_key: API密钥（默认从配置读取）
        """
        self.model = model
        self.api_key = api_key or settings.openai_api_key
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        logger.info(f"初始化OpenAI模型: {model}")
    
    async def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """聊天接口"""
        try:
            # 转换消息格式
            openai_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            # 调用OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            # 解析响应
            choice = response.choices[0]
            usage = response.usage
            
            # 计算成本
            cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)
            
            logger.info(f"OpenAI响应: {usage.total_tokens} tokens, ${cost:.4f}")
            
            return AIResponse(
                content=choice.message.content,
                model=self.model,
                tokens_used=usage.total_tokens,
                finish_reason=choice.finish_reason,
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"OpenAI调用失败: {e}", exc_info=True)
            raise
    
    async def complete(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """文本补全接口"""
        # 对于聊天模型，使用chat接口
        messages = [Message(role="user", content=prompt)]
        return await self.chat(messages, temperature, max_tokens, **kwargs)
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.model
    
    def get_max_context_length(self) -> int:
        """获取最大上下文长度"""
        context_lengths = {
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384,
        }
        return context_lengths.get(self.model, 4096)
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """计算调用成本"""
        if self.model not in self.PRICING:
            return 0.0
        
        pricing = self.PRICING[self.model]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
