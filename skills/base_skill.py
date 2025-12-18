# skills/base_skill.py
from abc import ABC, abstractmethod
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from interfaces.message_platform import IMessagePlatform

class BaseSkill(ABC):
    """
    所有技能的抽象基类。
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """技能的名称。"""
        pass

    @abstractmethod
    def can_handle(self, message: Dict[str, Any]) -> bool:
        """
        判断此技能是否能处理给定的消息。
        :param message: 消息字典，包含 'content', 'sender' 等信息。
        :return: 如果能处理，返回 True，否则 False。
        """
        pass

    @abstractmethod
    def execute(self, message: Dict[str, Any], platform: 'IMessagePlatform') -> None:
        """
        执行技能。
        :param message: 触发此技能的消息。
        :param platform: 用于发送响应的平台实例。
        """
        pass
