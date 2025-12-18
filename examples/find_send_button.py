#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
找到正确的发送按钮位置
"""

import uiautomator2 as u2
import time
import os

def find_send_button():
    """测试不同的发送按钮位置"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/find_send_button", exist_ok=True)
    
    y = int(height * 0.92)
    
    # 当前状态（应该已经输入了文字）
    d.screenshot("screenshots/find_send_button/00_current.jpg")
    print("✓ 当前状态已截图")
    
    # 测试不同的X坐标
    test_positions = [
        (int(width * 0.90), "90%"),
        (int(width * 0.92), "92%"),
        (int(width * 0.95), "95%"),
        (int(width * 0.97), "97%"),
        (int(width * 0.98), "98%"),
    ]
    
    print("\n测试发送按钮位置...")
    print("请确保输入框中已经有文字！\n")
    
    for i, (x, desc) in enumerate(test_positions, 1):
        print(f"[测试 {i}] 点击位置: ({x}, {y}) - 宽度{desc}")
        
        # 点击
        d.click(x, y)
        time.sleep(1.0)
        
        # 截图
        d.screenshot(f"screenshots/find_send_button/{i:02d}_clicked_{desc}.jpg")
        print(f"  ✓ 已点击并截图")
        
        # 检查是否发送成功（简单判断：如果输入框清空了，说明发送了）
        print(f"  → 查看截图看是否发送: open screenshots/find_send_button/{i:02d}_clicked_{desc}.jpg")
        
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)
    print("\n请查看手机，哪次点击成功发送了消息？")
    print("或者查看截图对比，哪张截图中输入框被清空了？")

if __name__ == "__main__":
    find_send_button()
