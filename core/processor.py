# 核心逻辑层 - 消息处理器
from typing import Dict, Any, List, Optional
from loguru import logger
from interfaces.message_platform import IMessagePlatform
from skills.base_skill import BaseSkill


class MessageProcessor:
    """
    消息处理器 - 核心逻辑层的主要组件
    负责接收消息、匹配技能、执行处理
    """
    
    def __init__(self):
        self.skills: List[BaseSkill] = []
        logger.info("消息处理器初始化")
    
    def register_skill(self, skill: BaseSkill):
        """注册技能"""
        self.skills.append(skill)
        logger.info(f"已注册技能: {skill.name}")
    
    def register_skills(self, skills: List[BaseSkill]):
        """批量注册技能"""
        for skill in skills:
            self.register_skill(skill)
    
    def find_handler(self, message: Dict[str, Any]) -> Optional[BaseSkill]:
        """
        查找能处理该消息的技能
        
        Args:
            message: 消息字典
            
        Returns:
            匹配的技能，如果没有则返回None
        """
        for skill in self.skills:
            try:
                if skill.can_handle(message):
                    logger.debug(f"消息匹配到技能: {skill.name}")
                    return skill
            except Exception as e:
                logger.error(f"技能 {skill.name} 匹配检查失败: {e}")
                continue
        
        logger.warning(f"没有找到能处理消息的技能: {message.get('content', '')[:50]}")
        return None
    
    def process(
        self, 
        message: Dict[str, Any], 
        platform: IMessagePlatform
    ) -> Dict[str, Any]:
        """
        处理单条消息
        
        Args:
            message: 消息字典
            platform: 消息平台实例
            
        Returns:
            处理结果
        """
        logger.info(f"开始处理消息: sender={message.get('sender')}, content={message.get('content', '')[:50]}")
        
        try:
            # 查找匹配的技能
            skill = self.find_handler(message)
            
            if not skill:
                return {
                    "status": "no_handler",
                    "message": "No skill found to handle this message"
                }
            
            # 执行技能
            logger.info(f"执行技能: {skill.name}")
            skill.execute(message, platform)
            
            logger.success(f"消息处理成功: skill={skill.name}")
            return {
                "status": "success",
                "skill": skill.name,
                "message_id": message.get("sender", "unknown")
            }
            
        except Exception as e:
            logger.error(f"消息处理失败: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }


# 全局消息处理器实例
message_processor = MessageProcessor()


def get_message_processor() -> MessageProcessor:
    """获取全局消息处理器实例"""
    return message_processor
