#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析输入区域，找到语音/文字切换按钮
"""

import uiautomator2 as u2
import time

d = u2.connect()
print(f"📱 设备: {d.window_size()}")
width, height = d.window_size()

# 截图输入区域
print("\n正在截图...")
d.screenshot("screenshots/input_area_analysis.jpg")
print("✓ 已保存到 screenshots/input_area_analysis.jpg")

# 分析输入区域的关键位置
print("\n" + "="*60)
print("微信输入区域分析")
print("="*60)

# 输入框区域通常在底部 88-95% 的高度
input_area_top = int(height * 0.88)
input_area_bottom = int(height * 0.96)

print(f"\n输入区域高度: {input_area_top} - {input_area_bottom} px")
print(f"总高度: {height} px")

# 常见的按钮位置（基于1080x2400分辨率）
print("\n可能的按钮位置:")
print("-" * 60)

# 语音/键盘切换按钮通常在最左侧
keyboard_switch_x = int(width * 0.05)  # 5% 宽度 - 最左侧
keyboard_switch_y = int(height * 0.92)  # 92% 高度

print(f"1. 语音/键盘切换按钮 (最左侧):")
print(f"   位置: ({keyboard_switch_x}, {keyboard_switch_y})")
print(f"   说明: 通常是一个键盘图标或语音图标")

# 表情按钮
emoji_x = int(width * 0.15)  # 15% 宽度
emoji_y = int(height * 0.92)

print(f"\n2. 表情按钮:")
print(f"   位置: ({emoji_x}, {emoji_y})")

# 文字输入框中心
text_input_x = int(width * 0.45)  # 45% 宽度 - 输入框中心
text_input_y = int(height * 0.92)

print(f"\n3. 文字输入框 (中心):")
print(f"   位置: ({text_input_x}, {text_input_y})")

# 更多功能按钮 (+)
more_x = int(width * 0.85)  # 85% 宽度
more_y = int(height * 0.92)

print(f"\n4. 更多功能按钮 (+):")
print(f"   位置: ({more_x}, {more_y})")

# 发送按钮
send_x = int(width * 0.95)  # 95% 宽度
send_y = int(height * 0.92)

print(f"\n5. 发送按钮:")
print(f"   位置: ({send_x}, {send_y})")

print("\n" + "="*60)
print("建议操作流程:")
print("="*60)
print("\n1. 点击 ({}, {}) - 切换到键盘模式".format(keyboard_switch_x, keyboard_switch_y))
print("2. 点击 ({}, {}) - 激活输入框".format(text_input_x, text_input_y))
print("3. 输入文字")
print("4. 点击 ({}, {}) - 发送".format(send_x, send_y))

print("\n打开截图查看:")
print("  open screenshots/input_area_analysis.jpg")
