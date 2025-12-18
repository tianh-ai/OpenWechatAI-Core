#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动测试不同位置的点击，找到正确的键盘切换按钮
"""

import uiautomator2 as u2
import time
import os

def test_click_positions():
    """测试多个可能的切换按钮位置"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/test_positions", exist_ok=True)
    
    # 测试多个X坐标位置（都在底部的Y坐标）
    y = int(height * 0.92)  # 92% 高度
    
    test_positions = [
        (int(width * 0.03), "3% - 极左"),   # 54px 左右
        (int(width * 0.05), "5% - 左"),     # 54px
        (int(width * 0.08), "8% - 偏左"),   # 86px
        (int(width * 0.10), "10% - 左侧"),  # 108px
        (int(width * 0.12), "12% - 中左"),  # 130px
    ]
    
    print("\n" + "="*60)
    print("测试不同位置的点击")
    print("="*60)
    
    for i, (x, desc) in enumerate(test_positions, 1):
        print(f"\n[测试 {i}/{len(test_positions)}] {desc}")
        print(f"  坐标: ({x}, {y})")
        
        # 截图前状态
        d.screenshot(f"screenshots/test_positions/before_{i}.jpg")
        
        # 点击
        d.click(x, y)
        time.sleep(1.5)  # 等待反应
        
        # 截图后状态
        d.screenshot(f"screenshots/test_positions/after_{i}.jpg")
        print(f"  ✓ 已点击并截图")
        
        # 等待用户观察
        print(f"  → 请查看手机，是否切换到了键盘模式？")
        print(f"    查看截图: open screenshots/test_positions/after_{i}.jpg")
        
        if i < len(test_positions):
            input("\n  按 Enter 继续测试下一个位置...")
    
    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)
    print("\n请告诉我哪个位置成功切换到了键盘模式")

if __name__ == "__main__":
    test_click_positions()
