#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整通信测试 - 发送、接收、自动回复
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from wechat_sender import WeChatSender
from wechat_receiver import WeChatReceiver
import time

def test_send():
    """测试发送功能"""
    print("\n" + "="*60)
    print("测试1: 发送消息")
    print("="*60)
    
    sender = WeChatSender()
    success = sender.send_message("自动发送测试", screenshot_dir="screenshots/test/send")
    
    if success:
        print("✅ 发送测试通过")
    else:
        print("❌ 发送测试失败")
    
    return success

def test_receive():
    """测试接收功能"""
    print("\n" + "="*60)
    print("测试2: 接收消息")
    print("="*60)
    print("\n请在10秒内向当前聊天窗口发送一条消息...")
    
    receiver = WeChatReceiver()
    has_message = receiver.wait_for_new_message(timeout=10)
    
    if has_message:
        msg_path = receiver.get_latest_message_screenshot("screenshots/test/received.jpg")
        print(f"✅ 接收测试通过")
        print(f"   截图: {msg_path}")
        return True
    else:
        print("❌ 接收测试失败（未检测到新消息）")
        return False

def test_auto_reply():
    """测试自动回复（运行30秒）"""
    print("\n" + "="*60)
    print("测试3: 自动回复（30秒）")
    print("="*60)
    print("\n请向当前聊天窗口发送消息，系统会自动回复...")
    print("按 Ctrl+C 可提前停止\n")
    
    from wechat_auto_reply import WeChatAutoReply
    
    auto_reply = WeChatAutoReply()
    
    try:
        # 修改监控逻辑，30秒后自动停止
        start_time = time.time()
        auto_reply.running = True
        auto_reply.receiver._has_new_message()  # 初始化
        
        message_count = 0
        
        while time.time() - start_time < 30:
            time.sleep(2)
            
            if auto_reply.receiver._has_new_message():
                message_count += 1
                print(f"[{message_count}] 收到消息并自动回复")
                
                msg_path = auto_reply.receiver.get_latest_message_screenshot(
                    f"screenshots/test/auto_{message_count}.jpg"
                )
                
                reply = "这是自动回复测试"
                auto_reply.sender.send_message(reply)
                time.sleep(1)
        
        print(f"\n✅ 自动回复测试完成（处理了 {message_count} 条消息）")
        return True
        
    except KeyboardInterrupt:
        print("\n⏹️  测试提前停止")
        return True

if __name__ == "__main__":
    print("="*60)
    print("🧪 微信通信功能完整测试")
    print("="*60)
    print("\n确保:")
    print("  1. 手机已连接")
    print("  2. 微信已打开文件传输助手聊天窗口")
    print("  3. 微信设置中已开启\"回车键发送消息\"")
    
    input("\n准备好后按 Enter 开始测试...")
    
    os.makedirs("screenshots/test", exist_ok=True)
    
    results = []
    
    # 测试1: 发送
    results.append(("发送", test_send()))
    time.sleep(2)
    
    # 测试2: 接收
    results.append(("接收", test_receive()))
    time.sleep(2)
    
    # 测试3: 自动回复
    results.append(("自动回复", test_auto_reply()))
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试结果")
    print("="*60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + "="*60)
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败")
    print("="*60)
