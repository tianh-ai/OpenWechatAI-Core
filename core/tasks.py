from celery import Celery
from core.config import settings
from typing import Dict, Any
import logging

# 配置日志
logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "tasks",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_soft_time_limit=300,  # 5分钟软超时
    task_time_limit=600,  # 10分钟硬超时
)

# 简单的技能注册表（后续会改为动态加载）
_skills_registry = []

def register_skill(skill):
    """注册技能到注册表"""
    _skills_registry.append(skill)
    logger.info(f"已注册技能: {skill.name}")

def get_skills():
    """获取所有已注册的技能"""
    if not _skills_registry:
        # 延迟导入避免循环依赖
        from skills.echo_skill import EchoSkill
        register_skill(EchoSkill())
    return _skills_registry

@celery_app.task(name="tasks.process_wechat_message", bind=True, max_retries=3)
def process_wechat_message(self, message: Dict[str, Any]):
    """
    异步处理微信消息。
    
    Args:
        message: 消息字典，包含 sender, content, platform 等字段
        
    Returns:
        处理结果字典
    """
    logger.info(f"开始处理消息: {message}")
    
    try:
        # 1. 获取所有技能
        skills = get_skills()
        
        # 2. 查找能处理此消息的技能
        for skill in skills:
            try:
                if skill.can_handle(message):
                    logger.info(f"使用技能: {skill.name}")
                    
                    # 3. 获取平台实例（延迟导入）
                    from implementations.wechat.wechat_platform import WeChatPlatform
                    platform = WeChatPlatform()
                    
                    # 4. 执行技能
                    skill.execute(message, platform)
                    
                    logger.info(f"技能 {skill.name} 执行成功")
                    return {
                        "status": "success",
                        "skill": skill.name,
                        "message_id": message.get("sender", "unknown")
                    }
            except Exception as skill_error:
                logger.error(f"技能 {skill.name} 执行失败: {skill_error}", exc_info=True)
                # 继续尝试下一个技能
                continue
        
        # 5. 没有找到合适的技能
        logger.warning(f"没有找到处理消息的技能: {message}")
        return {
            "status": "no_handler",
            "message": "No skill could handle this message"
        }
        
    except Exception as e:
        logger.error(f"处理消息时发生错误: {e}", exc_info=True)
        
        # 重试机制
        try:
            raise self.retry(exc=e, countdown=60)  # 1分钟后重试
        except self.MaxRetriesExceededError:
            logger.error(f"消息处理失败，已达最大重试次数: {message}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Max retries exceeded"
            }

@celery_app.task(name="tasks.send_reply")
def send_reply(platform: str, contact_id: str, message: str):
    """
    Asynchronous task to send a reply back to a platform.
    """
    print(f"Sending reply via Celery to {platform}: {contact_id} -> {message}")
    # TODO:
    # 1. Get the platform implementation instance.
    # 2. Call the platform's send_message method.
    pass
