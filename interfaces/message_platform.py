# interfaces/message_platform.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IMessagePlatform(ABC):
    """
    消息平台的抽象基类 (接口)。
    任何希望被核心逻辑层支持的平台（如微信、钉钉）都必须实现这些方法。
    """

    @abstractmethod
    def connect(self) -> bool:
        """连接到平台。"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """断开与平台的连接。"""
        pass

    @abstractmethod
    def send_message(self, contact_id: str, message: str) -> bool:
        """向指定联系人发送消息。"""
        pass

    @abstractmethod
    def get_unread_messages(self) -> List[Dict[str, Any]]:
        """获取所有未读消息。返回消息列表，每条消息是一个字典。"""
        pass

    @abstractmethod
    def get_contacts(self) -> List[Dict[str, Any]]:
        """获取联系人列表。"""
        pass

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """返回平台的名称，如 'WeChat', 'Feishu'。"""
        pass
