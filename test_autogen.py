#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试autogen是否能正常工作
"""

try:
    import autogen
    print("autogen successfully imported")
    print(f"autogen version: {autogen.__version__}")
except ImportError as e:
    print(f"Failed to import autogen: {e}")

try:
    from autogen import UserProxyAgent, AssistantAgent
    print("UserProxyAgent and AssistantAgent successfully imported")
except ImportError as e:
    print(f"Failed to import UserProxyAgent or AssistantAgent: {e}")

try:
    from autogen.agentchat.groupchat import GroupChat, GroupChatManager
    print("GroupChat and GroupChatManager successfully imported")
except ImportError as e:
    print(f"Failed to import GroupChat or GroupChatManager: {e}")

print("Test completed")