"""
AI模型路由器 - 管理和选择AI模型
"""
from typing import Dict, List, Optional
from loguru import logger
from interfaces.ai_model import IAIModel, Message, AIResponse
from implementations.ai.openai_model import OpenAIModel
from implementations.ai.gemini_model import GeminiModel


class AIRouter:
    """AI模型路由器"""
    
    def __init__(self):
        self.models: Dict[str, IAIModel] = {}
        self.default_model: Optional[str] = None
    
    def register_model(self, name: str, model: IAIModel, set_default: bool = False):
        """
        注册AI模型
        
        Args:
            name: 模型名称
            model: 模型实例
            set_default: 是否设为默认模型
        """
        self.models[name] = model
        logger.info(f"注册AI模型: {name}")
        
        if set_default or self.default_model is None:
            self.default_model = name
            logger.info(f"设置默认模型: {name}")
    
    def get_model(self, name: Optional[str] = None) -> IAIModel:
        """
        获取AI模型
        
        Args:
            name: 模型名称（None则使用默认）
            
        Returns:
            AI模型实例
        """
        model_name = name or self.default_model
        
        if not model_name:
            raise ValueError("No AI model specified and no default model set")
        
        if model_name not in self.models:
            raise ValueError(f"AI model not found: {model_name}")
        
        return self.models[model_name]
    
    async def chat(
        self,
        messages: List[Message],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """
        使用指定模型进行聊天
        
        Args:
            messages: 消息历史
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            AI响应
        """
        ai_model = self.get_model(model)
        return await ai_model.chat(messages, temperature, max_tokens, **kwargs)
    
    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> AIResponse:
        """
        使用指定模型进行补全
        
        Args:
            prompt: 提示词
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            AI响应
        """
        ai_model = self.get_model(model)
        return await ai_model.complete(prompt, temperature, max_tokens, **kwargs)
    
    def list_models(self) -> List[str]:
        """列出所有已注册的模型"""
        return list(self.models.keys())


# 全局AI路由器实例
ai_router = AIRouter()


def get_ai_router() -> AIRouter:
    """获取全局AI路由器"""
    return ai_router


def init_ai_models():
    """初始化AI模型"""
    try:
        # 尝试初始化OpenAI
        try:
            openai_model = OpenAIModel(model="gpt-3.5-turbo")
            ai_router.register_model("gpt-3.5-turbo", openai_model, set_default=True)
            
            openai_gpt4 = OpenAIModel(model="gpt-4")
            ai_router.register_model("gpt-4", openai_gpt4)
            
            logger.success("OpenAI模型初始化成功")
        except Exception as e:
            logger.warning(f"OpenAI模型初始化失败: {e}")
        
        # 尝试初始化Gemini
        try:
            gemini_model = GeminiModel(model="gemini-pro")
            ai_router.register_model("gemini-pro", gemini_model)
            logger.success("Gemini模型初始化成功")
        except Exception as e:
            logger.warning(f"Gemini模型初始化失败: {e}")
        
        if not ai_router.list_models():
            logger.error("未能初始化任何AI模型")
        else:
            logger.success(f"AI模型初始化完成: {ai_router.list_models()}")
            
    except Exception as e:
        logger.error(f"AI模型初始化失败: {e}", exc_info=True)
