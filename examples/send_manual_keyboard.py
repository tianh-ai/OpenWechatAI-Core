#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送消息 - 需要手动先切换到键盘模式
使用前请手动在手机上点击切换到键盘输入模式
"""

import uiautomator2 as u2
import time
import os
import sys

def send_message_manual_keyboard(message="你好"):
    """发送消息（假设已经手动切换到键盘模式）"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/manual_keyboard_send", exist_ok=True)
    
    # 关键坐标
    text_input_x = int(width * 0.45)   # 输入框中心
    send_x = int(width * 0.95)         # 发送按钮
    y = int(height * 0.92)
    
    print("\n" + "="*60)
    print("⚠️  请先确认手机上已经是键盘输入模式！")
    print("="*60)
    print("\n如果还是语音模式，请手动点击左下角图标切换到键盘")
    
    input("\n准备好后按 Enter 继续...")
    
    print("\n" + "="*60)
    print("开始发送消息")
    print("="*60)
    
    # 步骤1: 确认当前界面
    print("\n[1/5] 确认当前界面（应该是键盘模式）...")
    d.screenshot("screenshots/manual_keyboard_send/01_keyboard_ready.jpg")
    print("  ✓ 已截图")
    
    # 步骤2: 点击输入框
    print(f"\n[2/5] 点击输入框... ({text_input_x}, {y})")
    d.click(text_input_x, y)
    time.sleep(0.5)
    d.screenshot("screenshots/manual_keyboard_send/02_clicked.jpg")
    print("  ✓ 已点击")
    
    # 步骤3: 清空
    print("\n[3/5] 清空输入框...")
    for _ in range(15):
        d.press("del")
    time.sleep(0.3)
    print("  ✓ 已清空")
    
    # 步骤4: 输入文字
    print(f"\n[4/5] 输入: '{message}'")
    d.send_keys(message)
    time.sleep(1.0)
    d.screenshot("screenshots/manual_keyboard_send/03_typed.jpg")
    print(f"  ✓ 已输入")
    
    # 步骤5: 发送
    print(f"\n[5/5] 点击发送... ({send_x}, {y})")
    d.click(send_x, y)
    time.sleep(0.8)
    d.screenshot("screenshots/manual_keyboard_send/04_sent.jpg")
    print("  ✓ 已发送")
    
    # 最终确认
    time.sleep(0.5)
    d.screenshot("screenshots/manual_keyboard_send/05_final.jpg")
    
    print("\n" + "="*60)
    print("✅ 执行完成！")
    print("="*60)
    
    print("\n📸 关键截图:")
    print("  open screenshots/manual_keyboard_send/03_typed.jpg  # 输入后")
    print("  open screenshots/manual_keyboard_send/05_final.jpg  # 发送后")
    
    print("\n" + "="*60)
    print("请检查:")
    print("="*60)
    print("1. 输入框中是否出现了文字？")
    print("2. 消息是否已发送到右侧（绿色气泡）？")
    print("3. 是文字消息还是语音消息？")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "你好"
    send_message_manual_keyboard(msg)
