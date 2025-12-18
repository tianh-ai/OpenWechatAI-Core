# core/main.py
import sys
import os
import argparse
from pathlib import Path

# Add the project root to the Python path for cross-module imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 初始化日志系统（必须在其他导入之前）
from core.logging_config import setup_logging
logger = setup_logging()

from core.listeners import run_wechat_listener
# from core.api import run_api_server # To be implemented

def main():
    """
    Main entry point for the application.
    Uses command-line arguments to start different services
    (e.g., the message listener, the API server, or a Celery worker).
    """
    logger.info("OpenWechatAI-Core 启动中...")
    
    parser = argparse.ArgumentParser(description="OpenWechatAI-Core Services")
    parser.add_argument(
        "service", 
        choices=["listener", "api", "worker"], 
        help="The service to start: listener (消息监听), api (API服务), worker (Celery工作进程)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    args = parser.parse_args()
    
    # 设置调试模式
    if args.debug:
        logger.info("调试模式已启用")
        os.environ["DEBUG"] = "true"

    try:
        if args.service == "listener":
            logger.info("启动微信消息监听服务...")
            run_wechat_listener()
            
        elif args.service == "api":
            logger.info("启动API服务...")
            # run_api_server() # To be implemented
            logger.warning("API服务尚未实现，请等待后续版本")
            
        elif args.service == "worker":
            logger.info("Celery Worker应通过命令行启动:")
            logger.info("  celery -A core.tasks worker --loglevel=info")
            logger.warning("请使用上述命令启动Celery Worker")
            
    except KeyboardInterrupt:
        logger.info("接收到中断信号，正在关闭...")
    except Exception as e:
        logger.error(f"服务启动失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("OpenWechatAI-Core 已停止")

if __name__ == "__main__":
    main()
