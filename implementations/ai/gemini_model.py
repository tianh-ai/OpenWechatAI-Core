"""
Google Gemini模型实现
"""
import google.generativeai as genai
from typing import List
from loguru import logger
from interfaces.ai_model import IAIModel, Message, AIResponse
from core.config import settings


class GeminiModel(IAIModel):
    """Google Gemini模型"""
    
    # 模型价格（USD per 1K tokens）
    PRICING = {
        "gemini-pro": {"input": 0.00025, "output": 0.0005},
        "gemini-pro-vision": {"input": 0.00025, "output": 0.0005},
    }
    
    def __init__(self, model: str = "gemini-pro", api_key: str = None):
        """
        初始化Gemini模型
        
        Args:
            model: 模型名称
            api_key: API密钥（默认从配置读取）
        """
        self.model_name = model
        self.api_key = api_key or settings.gemini_api_key
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f"初始化Gemini模型: {model}")
    
    async def chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """聊天接口"""
        try:
            # 构建对话历史
            chat = self.model.start_chat(history=[])
            
            # 添加历史消息（除了最后一条）
            for msg in messages[:-1]:
                if msg.role == "user":
                    chat.history.append({
                        "role": "user",
                        "parts": [msg.content]
                    })
                elif msg.role == "assistant":
                    chat.history.append({
                        "role": "model",
                        "parts": [msg.content]
                    })
            
            # 发送最后一条消息
            last_message = messages[-1].content
            
            # 配置生成参数
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            # 发送请求
            response = await chat.send_message_async(
                last_message,
                generation_config=generation_config
            )
            
            # 估算token使用（Gemini API暂不直接提供）
            estimated_tokens = len(last_message.split()) * 2  # 粗略估算
            
            # 估算成本
            cost = self._calculate_cost(estimated_tokens, estimated_tokens)
            
            logger.info(f"Gemini响应: ~{estimated_tokens*2} tokens, ${cost:.4f}")
            
            return AIResponse(
                content=response.text,
                model=self.model_name,
                tokens_used=estimated_tokens * 2,
                finish_reason="stop",
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"Gemini调用失败: {e}", exc_info=True)
            raise
    
    async def complete(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """文本补全接口"""
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )
            
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            
            estimated_tokens = len(prompt.split()) * 2
            cost = self._calculate_cost(estimated_tokens, estimated_tokens)
            
            return AIResponse(
                content=response.text,
                model=self.model_name,
                tokens_used=estimated_tokens * 2,
                finish_reason="stop",
                cost=cost
            )
            
        except Exception as e:
            logger.error(f"Gemini补全失败: {e}", exc_info=True)
            raise
    
    def get_model_name(self) -> str:
        """获取模型名称"""
        return self.model_name
    
    def get_max_context_length(self) -> int:
        """获取最大上下文长度"""
        # Gemini Pro支持32K tokens
        return 32768
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """计算调用成本"""
        if self.model_name not in self.PRICING:
            return 0.0
        
        pricing = self.PRICING[self.model_name]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
