import time
from loguru import logger
from core.tasks import process_wechat_message
from implementations.wechat.wechat_platform import WeChatPlatform
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def initialize_platform():
    """初始化微信平台，带重试机制"""
    logger.info("正在初始化微信平台...")
    platform = WeChatPlatform()
    if not platform.connect():
        raise ConnectionError("无法连接到微信平台")
    return platform

def run_wechat_listener():
    """
    初始化微信平台并运行轮询循环，监听新消息
    将消息分发到Celery队列进行异步处理
    """
    logger.info("微信消息监听服务启动中...")
    
    try:
        platform = initialize_platform()
        logger.success("微信平台初始化成功")
    except Exception as e:
        logger.error(f"初始化微信平台失败: {e}", exc_info=True)
        logger.error("监听服务退出")
        return

    logger.info("开始轮询消息...")
    consecutive_errors = 0
    max_consecutive_errors = 5
    
    while True:
        try:
            # 获取未读消息（当前是模拟实现）
            unread_messages = platform.get_unread_messages()

            if unread_messages:
                logger.info(f"发现 {len(unread_messages)} 条新消息，分发到Celery队列...")
                for msg in unread_messages:
                    try:
                        # 分发消息到Celery worker异步处理
                        task = process_wechat_message.delay(msg)
                        logger.debug(f"消息已分发: task_id={task.id}, sender={msg.get('sender')}")
                    except Exception as dispatch_error:
                        logger.error(f"消息分发失败: {dispatch_error}", exc_info=True)
                
                # 重置错误计数
                consecutive_errors = 0
            
            # 等待一段时间再次轮询，避免高CPU占用
            time.sleep(10)

        except KeyboardInterrupt:
            logger.info("接收到键盘中断信号，正在关闭监听服务...")
            platform.disconnect()
            break
            
        except Exception as e:
            consecutive_errors += 1
            logger.error(
                f"轮询过程中发生错误 ({consecutive_errors}/{max_consecutive_errors}): {e}",
                exc_info=True
            )
            
            # 检查是否超过最大连续错误次数
            if consecutive_errors >= max_consecutive_errors:
                logger.critical("连续错误次数过多，监听服务退出")
                platform.disconnect()
                break
            
            # 错误后等待更长时间
            wait_time = min(30 * consecutive_errors, 300)  # 最多等待5分钟
            logger.info(f"等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            
            # 尝试重新连接
            try:
                logger.info("尝试重新连接微信平台...")
                platform = initialize_platform()
                logger.success("重新连接成功")
                consecutive_errors = 0
            except Exception as reconnect_error:
                logger.error(f"重新连接失败: {reconnect_error}")
    
    logger.info("微信消息监听服务已停止")
