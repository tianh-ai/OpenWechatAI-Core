#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试获取输入区域的UI信息和使用长按来切换输入模式
"""

import uiautomator2 as u2
import time
import os

def try_different_methods():
    """尝试不同的方法切换输入模式"""
    d = u2.connect()
    
    print(f"📱 设备: {d.window_size()}")
    width, height = d.window_size()
    
    os.makedirs("screenshots/switch_methods", exist_ok=True)
    
    y = int(height * 0.92)
    
    print("\n" + "="*60)
    print("方法1: 尝试长按输入框区域（可能会弹出输入法选择）")
    print("="*60)
    
    # 截图初始状态
    d.screenshot("screenshots/switch_methods/01_initial.jpg")
    print("✓ 初始截图")
    
    # 长按输入框区域
    input_x = int(width * 0.4)
    print(f"\n长按位置: ({input_x}, {y})")
    d.long_click(input_x, y, duration=1.5)
    time.sleep(1)
    d.screenshot("screenshots/switch_methods/02_after_longclick.jpg")
    print("✓ 长按后截图")
    
    print("\n" + "="*60)
    print("方法2: 双击输入框左侧区域")
    print("="*60)
    
    time.sleep(1)
    left_x = int(width * 0.08)
    print(f"\n双击位置: ({left_x}, {y})")
    d.double_click(left_x, y)
    time.sleep(1)
    d.screenshot("screenshots/switch_methods/03_after_doubleclick.jpg")
    print("✓ 双击后截图")
    
    print("\n" + "="*60)
    print("方法3: 滑动操作（从左向右滑动输入框）")
    print("="*60)
    
    time.sleep(1)
    start_x = int(width * 0.05)
    end_x = int(width * 0.30)
    print(f"\n滑动: ({start_x}, {y}) → ({end_x}, {y})")
    d.swipe(start_x, y, end_x, y, duration=0.3)
    time.sleep(1)
    d.screenshot("screenshots/switch_methods/04_after_swipe.jpg")
    print("✓ 滑动后截图")
    
    print("\n" + "="*60)
    print("方法4: 尝试使用uiautomator2的文本选择器")
    print("="*60)
    
    # 尝试找到"按住说话"或类似的元素
    time.sleep(1)
    try:
        # 查找可能的元素
        print("\n尝试查找UI元素...")
        
        # 方法A: 通过文本查找
        if d(textContains="说话").exists:
            print("  找到包含'说话'的元素")
            d(textContains="说话").click()
            time.sleep(1)
            d.screenshot("screenshots/switch_methods/05_clicked_text.jpg")
        
        # 方法B: 通过描述查找
        elif d(descriptionContains="键盘").exists:
            print("  找到包含'键盘'描述的元素")
            d(descriptionContains="键盘").click()
            time.sleep(1)
            d.screenshot("screenshots/switch_methods/05_clicked_desc.jpg")
        
        # 方法C: 输出所有可点击的元素
        else:
            print("  未找到明确的元素")
            print("  尝试输出UI层级...")
            xml = d.dump_hierarchy()
            with open("screenshots/switch_methods/ui_hierarchy.xml", "w", encoding="utf-8") as f:
                f.write(xml)
            print("  ✓ UI层级已保存到 ui_hierarchy.xml")
    
    except Exception as e:
        print(f"  错误: {e}")
    
    print("\n" + "="*60)
    print("✅ 所有方法测试完成！")
    print("="*60)
    
    print("\n查看截图:")
    for i in range(1, 6):
        if os.path.exists(f"screenshots/switch_methods/0{i}_*.jpg"):
            print(f"  open screenshots/switch_methods/0{i}_*.jpg")
    
    print("\n请查看手机，哪个方法成功切换到了键盘模式？")

if __name__ == "__main__":
    try_different_methods()
