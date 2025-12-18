# 日志系统配置和初始化
from loguru import logger
import sys
from pathlib import Path
from core.config import settings

def setup_logging():
    """
    配置应用日志系统
    使用loguru进行统一的日志管理
    """
    # 创建日志目录
    log_file = Path(settings.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 移除默认的handler
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # 添加文件输出
    logger.add(
        settings.log_file,
        rotation="500 MB",  # 文件达到500MB时轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        enqueue=True,  # 异步写入
    )
    
    # 添加错误日志单独记录
    logger.add(
        "logs/errors.log",
        rotation="100 MB",
        retention="60 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        backtrace=True,
        diagnose=True,
    )
    
    logger.info("日志系统初始化完成")
    logger.debug(f"日志级别: {settings.log_level}")
    logger.debug(f"日志文件: {settings.log_file}")
    
    return logger

# 全局logger实例
app_logger = logger
