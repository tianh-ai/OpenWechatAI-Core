#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 ADB IME 方式发送消息到文件传输助手
需要先安装 ADBKeyBoard.apk
"""

import uiautomator2 as u2
import time
import os

def send_message_via_adb_ime(message="你好"):
    """使用 ADB IME 输入中文"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    # 创建截图目录
    os.makedirs("screenshots/adb_ime_send", exist_ok=True)
    
    # 步骤1: 确认界面
    print("\n[1/5] 确认当前界面...")
    d.screenshot("screenshots/adb_ime_send/01_current.jpg")
    print("  ✓ 已截图")
    
    # 步骤2: 点击输入框（左侧，避免语音）
    input_x = int(width * 0.4)  # 40% 宽度
    input_y = int(height * 0.92)  # 92% 高度
    
    print(f"\n[2/5] 点击输入框... 点击: ({input_x}, {input_y})")
    d.click(input_x, input_y)
    time.sleep(0.5)
    d.screenshot("screenshots/adb_ime_send/02_clicked.jpg")
    print("  ✓ 已点击")
    
    # 步骤3: 切换到 ADB Keyboard
    print("\n[3/5] 切换输入法...")
    os.system('adb shell ime set com.android.adbkeyboard/.AdbIME')
    time.sleep(0.5)
    print("  ✓ 已切换到 ADB Keyboard")
    
    # 步骤4: 通过 ADB 发送文本
    print(f"\n[4/5] 通过 ADB 输入消息...")
    # 使用 broadcast 方式发送文本
    cmd = f'adb shell am broadcast -a ADB_INPUT_TEXT --es msg "{message}"'
    os.system(cmd)
    time.sleep(0.8)
    d.screenshot("screenshots/adb_ime_send/03_typed.jpg")
    print(f"  ✓ 已输入'{message}'")
    
    # 步骤5: 点击发送按钮
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    
    print(f"\n[5/5] 点击发送... 点击: ({send_x}, {send_y})")
    d.click(send_x, send_y)
    time.sleep(0.5)
    d.screenshot("screenshots/adb_ime_send/04_sent.jpg")
    print("  ✓ 已点击发送")
    
    # 切回默认输入法
    print("\n[完成] 恢复默认输入法...")
    os.system('adb shell ime reset')
    d.screenshot("screenshots/adb_ime_send/05_final.jpg")
    
    print("\n" + "="*50)
    print("✅ 执行完成！")
    print("="*50)
    print("\n📸 生成了5张截图:")
    for i, name in enumerate(['01_current', '02_clicked', '03_typed', '04_sent', '05_final'], 1):
        print(f"  {name}.jpg")
    
    print("\n查看最后截图:")
    print("  open screenshots/adb_ime_send/05_final.jpg")

if __name__ == "__main__":
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else "你好"
    send_message_via_adb_ime(msg)
