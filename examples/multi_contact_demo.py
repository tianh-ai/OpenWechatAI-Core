#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整示例：多联系人智能回复系统
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from wechat_contact_manager import WeChatContactManager
from wechat_sender import WeChatSender
from wechat_receiver import WeChatReceiver
from reply_rule_engine import ReplyRuleEngine
import time

def multi_contact_auto_reply():
    """多联系人自动回复示例"""
    
    # 配置要监控的联系人列表
    contacts = [
        "文件传输助手",
        # "张三",
        # "李四",
    ]
    
    print("="*60)
    print("🤖 多联系人智能回复系统")
    print("="*60)
    print(f"\n监控联系人: {', '.join(contacts)}")
    print("\n按 Ctrl+C 停止\n")
    
    # 初始化组件
    contact_manager = WeChatContactManager()
    sender = WeChatSender()
    receiver = WeChatReceiver()
    rule_engine = ReplyRuleEngine()
    
    # 当前正在监控的联系人
    current_contact = None
    contact_index = 0
    
    # 每个联系人的消息计数
    message_counts = {contact: 0 for contact in contacts}
    
    try:
        while True:
            # 轮询所有联系人
            for contact in contacts:
                print(f"\n[检查] {contact}")
                
                # 切换到该联系人的聊天窗口
                if current_contact != contact:
                    contact_manager.open_chat_window(contact)
                    current_contact = contact
                    time.sleep(1)
                    # 初始化该联系人的消息检测
                    receiver._has_new_message()
                
                # 检查新消息
                if receiver._has_new_message():
                    message_counts[contact] += 1
                    msg_count = message_counts[contact]
                    
                    print(f"  ✉️  收到新消息 (#{msg_count})")
                    
                    # 截图
                    msg_path = receiver.get_latest_message_screenshot(
                        f"screenshots/multi_contact/{contact}_{msg_count}.jpg"
                    )
                    
                    # 这里可以集成 OCR 识别消息内容
                    # 暂时使用模拟消息
                    message_info = {"type": "text", "content": "测试消息"}
                    
                    # 使用规则引擎生成回复
                    reply = rule_engine.match_rule(message_info, contact_name=contact)
                    
                    if reply:
                        print(f"  💬 回复: {reply}")
                        sender.send_message(reply)
                        time.sleep(1)
                    else:
                        print(f"  ⏭️  不回复")
                
                # 每个联系人检查间隔
                time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  已停止")
        total_messages = sum(message_counts.values())
        print(f"\n📊 统计:")
        for contact, count in message_counts.items():
            print(f"  {contact}: {count} 条消息")
        print(f"  总计: {total_messages} 条")

if __name__ == "__main__":
    multi_contact_auto_reply()
