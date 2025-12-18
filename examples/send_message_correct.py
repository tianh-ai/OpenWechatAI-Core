#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确的发送流程：先切换到键盘模式，再输入文字
"""

import uiautomator2 as u2
import time
import os
import sys

def send_message_correct(message="你好"):
    """正确的发送流程"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    # 创建截图目录
    os.makedirs("screenshots/correct_send", exist_ok=True)
    
    # 关键坐标
    keyboard_switch_x = int(width * 0.05)  # 最左侧 - 语音/键盘切换
    text_input_x = int(width * 0.45)        # 输入框中心
    send_x = int(width * 0.95)              # 发送按钮
    y = int(height * 0.92)                  # 统一的 Y 坐标
    
    print("\n" + "="*60)
    print("开始发送消息")
    print("="*60)
    
    # 步骤1: 确认初始界面
    print("\n[1/6] 确认当前界面...")
    d.screenshot("screenshots/correct_send/01_initial.jpg")
    print("  ✓ 已截图 (语音模式)")
    
    # 步骤2: 点击左侧按钮切换到键盘模式
    print(f"\n[2/6] 切换到键盘模式... 点击: ({keyboard_switch_x}, {y})")
    d.click(keyboard_switch_x, y)
    time.sleep(0.8)  # 等待键盘弹出
    d.screenshot("screenshots/correct_send/02_keyboard_mode.jpg")
    print("  ✓ 已切换到键盘模式")
    
    # 步骤3: 点击输入框激活
    print(f"\n[3/6] 激活输入框... 点击: ({text_input_x}, {y})")
    d.click(text_input_x, y)
    time.sleep(0.5)
    d.screenshot("screenshots/correct_send/03_input_activated.jpg")
    print("  ✓ 输入框已激活")
    
    # 步骤4: 清空输入框（以防有残留）
    print("\n[4/6] 清空输入框...")
    for _ in range(10):
        d.press("del")
    time.sleep(0.3)
    print("  ✓ 已清空")
    
    # 步骤5: 输入文字
    print(f"\n[5/6] 输入消息: '{message}'")
    d.send_keys(message)
    time.sleep(0.8)
    d.screenshot("screenshots/correct_send/04_text_entered.jpg")
    print(f"  ✓ 已输入 '{message}'")
    
    # 步骤6: 点击发送
    print(f"\n[6/6] 点击发送... 点击: ({send_x}, {y})")
    d.click(send_x, y)
    time.sleep(0.5)
    d.screenshot("screenshots/correct_send/05_sent.jpg")
    print("  ✓ 已发送")
    
    # 最终确认
    time.sleep(0.5)
    d.screenshot("screenshots/correct_send/06_final.jpg")
    
    print("\n" + "="*60)
    print("✅ 发送完成！")
    print("="*60)
    
    print("\n📸 生成了6张截图:")
    screenshots = [
        "01_initial.jpg      - 初始界面 (语音模式)",
        "02_keyboard_mode.jpg - 切换到键盘模式",
        "03_input_activated.jpg - 激活输入框",
        "04_text_entered.jpg  - 输入文字后",
        "05_sent.jpg          - 点击发送后",
        "06_final.jpg         - 最终状态"
    ]
    for s in screenshots:
        print(f"  {s}")
    
    print("\n查看关键截图:")
    print("  open screenshots/correct_send/04_text_entered.jpg  # 确认文字已输入")
    print("  open screenshots/correct_send/06_final.jpg         # 确认消息已发送")
    
    return True

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "你好"
    send_message_correct(msg)
