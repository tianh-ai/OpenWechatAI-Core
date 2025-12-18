#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接发送消息 - 无需交互确认
"""

import uiautomator2 as u2
import time
import os
import sys

def send_message_direct(message="你好"):
    """直接发送消息"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/direct_send_final", exist_ok=True)
    
    # 关键坐标
    text_input_x = int(width * 0.45)
    send_x = int(width * 0.95)
    y = int(height * 0.92)
    
    print("\n开始发送...")
    
    # 截图初始状态
    d.screenshot("screenshots/direct_send_final/01_start.jpg")
    
    # 点击输入框
    d.click(text_input_x, y)
    time.sleep(0.5)
    
    # 清空
    for _ in range(15):
        d.press("del")
    time.sleep(0.3)
    
    # 输入
    print(f"输入: {message}")
    d.send_keys(message)
    time.sleep(1.0)
    d.screenshot("screenshots/direct_send_final/02_typed.jpg")
    
    # 发送
    d.click(send_x, y)
    time.sleep(0.8)
    d.screenshot("screenshots/direct_send_final/03_sent.jpg")
    
    print("✅ 完成！")
    print("\n查看结果:")
    print("  open screenshots/direct_send_final/02_typed.jpg")
    print("  open screenshots/direct_send_final/03_sent.jpg")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "你好"
    send_message_direct(msg)
