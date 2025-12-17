"""
企业通信统一MCP模块
集成企业微信、飞书、钉钉
"""

__version__ = "1.0.0"
__author__ = "OpenWechatAI"

from .feishu_bot import FeishuWebhookBot, FeishuAppBot
from .dingtalk_bot import DingTalkWebhookBot, DingTalkAppBot

__all__ = [
    'FeishuWebhookBot',
    'FeishuAppBot',
    'DingTalkWebhookBot',
    'DingTalkAppBot',
]
