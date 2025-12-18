#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用回车键发送消息（需要微信设置：回车键发送消息）
"""

import uiautomator2 as u2
import time
import os
import sys

def send_with_enter(message="你好"):
    """使用回车键发送（需要微信设置为回车发送）"""
    # 禁用 uiautomator2 的输入法切换
    d = u2.connect()
    d.settings['operation_delay'] = (0, 0)
    d.settings['operation_delay_methods'] = []
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/send_with_enter", exist_ok=True)
    
    text_input_x = int(width * 0.45)
    y = int(height * 0.92)
    
    print("\n" + "="*60)
    print("使用回车键发送消息")
    print("="*60)
    print("\n⚠️  前提：微信设置中已将\"回车键\"设为\"发送消息\"")
    
    # 截图初始
    d.screenshot("screenshots/send_with_enter/01_start.jpg")
    
    # 点击输入框
    print(f"\n[1/4] 点击输入框...")
    d.click(text_input_x, y)
    time.sleep(0.5)
    
    # 清空
    print("[2/4] 清空输入框...")
    for _ in range(20):
        d.press("del")
    time.sleep(0.3)
    
    # 输入
    print(f"[3/4] 输入: '{message}'")
    d.send_keys(message)
    time.sleep(0.8)
    d.screenshot("screenshots/send_with_enter/02_typed.jpg")
    
    # 按回车发送
    print("[4/4] 按回车键发送...")
    d.press("enter")
    time.sleep(1.0)
    d.screenshot("screenshots/send_with_enter/03_sent.jpg")
    
    print("\n" + "="*60)
    print("✅ 完成！")
    print("="*60)
    
    print("\n查看结果:")
    print("  open screenshots/send_with_enter/02_typed.jpg  # 输入后")
    print("  open screenshots/send_with_enter/03_sent.jpg   # 发送后")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "你好"
    send_with_enter(msg)
