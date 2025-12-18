#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动回复 - 简化版
"""

from wechat_sender import WeChatSender
from wechat_receiver import WeChatReceiver
from message_ocr import MessageOCR
from reply_rule_engine import ReplyRuleEngine
import time
import sys

def test_auto_reply():
    print("初始化...")
    sender = WeChatSender()
    receiver = WeChatReceiver()
    
    try:
        ocr = MessageOCR(ocr_engine='docker')
        print("✓ OCR已启用")
    except Exception as e:
        print(f"⚠️  OCR初始化失败: {e}")
        return False
    
    try:
        rule_engine = ReplyRuleEngine()
        print(f"✓ 已加载 {len(rule_engine.rules)} 条规则")
    except Exception as e:
        print(f"⚠️  规则引擎失败: {e}")
        return False
    
    print("\n开始监控...")
    print("按 Ctrl+C 停止\n")
    
    # 初始化基准
    receiver._has_new_message()
    message_count = 0
    max_messages = 3  # 只处理3条消息就停止，用于测试
    
    try:
        while message_count < max_messages:
            time.sleep(3)
            
            if receiver._has_new_message():
                message_count += 1
                print(f"\n[消息 #{message_count}] 检测到新消息")
                
                # 截图
                msg_path = f"screenshots/test_auto_reply/msg_{message_count}.jpg"
                receiver.get_latest_message_screenshot(msg_path)
                print(f"  截图: {msg_path}")
                
                # OCR识别
                try:
                    print("  OCR识别中...")
                    message_info = ocr.extract_latest_message(msg_path)
                    print(f"  内容: {message_info.get('content', 'N/A')}")
                    
                    # 生成回复
                    reply = rule_engine.match_rule(message_info)
                    if reply:
                        print(f"  回复: {reply}")
                        
                        # 发送
                        success = sender.send_message(reply)
                        if success:
                            print("  ✅ 已发送")
                            time.sleep(0.5)
                            receiver._has_new_message()  # 更新基准
                        else:
                            print("  ❌ 发送失败")
                    else:
                        print("  ⏭️  跳过")
                        
                except Exception as e:
                    print(f"  ❌ 处理失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 每次循环都打印一个点表示活着
            print(".", end="", flush=True)
    
    except KeyboardInterrupt:
        print("\n\n停止")
        print(f"共处理 {message_count} 条消息")
        return True
    
    print(f"\n测试完成，共处理 {message_count} 条消息")
    return True

if __name__ == "__main__":
    success = test_auto_reply()
    sys.exit(0 if success else 1)
