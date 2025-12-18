# skills/echo_skill.py
from typing import Dict, Any
from skills.base_skill import BaseSkill
from interfaces.message_platform import IMessagePlatform

class EchoSkill(BaseSkill):
    """
    一个简单的回显技能，用于演示。
    如果消息包含 "echo"，机器人会回复同样的内容。
    """
    @property
    def name(self) -> str:
        return "Echo Skill"

    def can_handle(self, message: Dict[str, Any]) -> bool:
        """如果消息内容包含 'echo'，则此技能可以处理。"""
        return 'echo' in message.get('content', '').lower()

    def execute(self, message: Dict[str, Any], platform: IMessagePlatform) -> None:
        """执行回显操作。"""
        sender = message.get('sender')
        content = message.get('content')
        reply_message = f"收到 '{content}'，正在回显: {content}"
        print(f"执行 EchoSkill: 回复给 {sender}")
        platform.send_message(sender, reply_message)
