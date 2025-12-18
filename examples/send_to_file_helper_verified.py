#!/usr/bin/env python3
"""
给文件传输助手发送消息（带人工验证版本）
每一步都会暂停让你确认
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os


def wait_for_confirm(step_name):
    """等待用户确认"""
    input(f"\n👀 请检查手机屏幕，确认 [{step_name}] 是否正确，然后按回车继续...")


def send_to_file_helper_verified(message="你好"):
    """给文件传输助手发送消息（带验证）"""
    print("=" * 60)
    print("给文件传输助手发送消息（验证版）")
    print("=" * 60)
    
    # 连接设备
    print("\n连接设备...")
    d = u2.connect()
    width, height = d.window_size()
    print(f"✓ 设备: {d.device_info['model']}")
    print(f"✓ 分辨率: {width}x{height}")
    
    os.makedirs("screenshots/file_helper_verified", exist_ok=True)
    
    # 步骤1: 启动微信
    print("\n" + "=" * 60)
    print("步骤1: 启动微信")
    print("=" * 60)
    d.app_start("com.tencent.mm")
    time.sleep(3)
    
    # 点击微信tab确保在聊天列表
    d.click(int(width * 0.125), int(height * 0.95))
    time.sleep(1)
    
    d.screenshot().save("screenshots/file_helper_verified/01_start.jpg")
    wait_for_confirm("微信是否在聊天列表页面")
    
    # 步骤2: 尝试点击顶部搜索
    print("\n" + "=" * 60)
    print("步骤2: 点击顶部搜索图标")
    print("=" * 60)
    print(f"点击位置: 右上角搜索图标")
    
    # 微信搜索图标通常在右上角
    search_x = int(width * 0.9)  # 右上角
    search_y = int(height * 0.06)  # 顶部
    
    print(f"坐标: ({search_x}, {search_y})")
    d.click(search_x, search_y)
    time.sleep(2)
    
    d.screenshot().save("screenshots/file_helper_verified/02_search_clicked.jpg")
    wait_for_confirm("是否打开了搜索页面")
    
    # 步骤3: 输入搜索关键词
    print("\n" + "=" * 60)
    print("步骤3: 输入'文件传输助手'")
    print("=" * 60)
    
    # 点击搜索输入框
    input_x = int(width * 0.5)
    input_y = int(height * 0.15)
    d.click(input_x, input_y)
    time.sleep(1)
    
    d.send_keys("文件传输助手")
    time.sleep(2)
    
    d.screenshot().save("screenshots/file_helper_verified/03_search_input.jpg")
    wait_for_confirm("是否显示了搜索结果")
    
    # 步骤4: 点击搜索结果
    print("\n" + "=" * 60)
    print("步骤4: 点击文件传输助手")
    print("=" * 60)
    
    # 第一个搜索结果
    result_x = int(width * 0.5)
    result_y = int(height * 0.3)
    
    print(f"点击第一个搜索结果: ({result_x}, {result_y})")
    d.click(result_x, result_y)
    time.sleep(2)
    
    d.screenshot().save("screenshots/file_helper_verified/04_helper_opened.jpg")
    wait_for_confirm("是否打开了文件传输助手聊天窗口")
    
    # 步骤5: 点击输入框
    print("\n" + "=" * 60)
    print("步骤5: 点击输入框")
    print("=" * 60)
    
    input_x = int(width * 0.5)
    input_y = int(height * 0.92)
    
    print(f"点击输入框: ({input_x}, {input_y})")
    d.click(input_x, input_y)
    time.sleep(1)
    
    d.screenshot().save("screenshots/file_helper_verified/05_input_focused.jpg")
    wait_for_confirm("输入框是否已激活（键盘弹出）")
    
    # 步骤6: 输入消息
    print("\n" + "=" * 60)
    print(f"步骤6: 输入消息 '{message}'")
    print("=" * 60)
    
    d.send_keys(message)
    time.sleep(1)
    
    d.screenshot().save("screenshots/file_helper_verified/06_message_typed.jpg")
    wait_for_confirm("消息是否已输入到输入框")
    
    # 步骤7: 点击发送按钮
    print("\n" + "=" * 60)
    print("步骤7: 点击发送按钮")
    print("=" * 60)
    
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    
    print(f"点击发送: ({send_x}, {send_y})")
    d.click(send_x, send_y)
    time.sleep(2)
    
    d.screenshot().save("screenshots/file_helper_verified/07_after_send.jpg")
    
    print("\n👀 请在手机上确认:")
    print("  1. 消息是否出现在聊天窗口中")
    print("  2. 消息是否在右侧（已发送状态）")
    print("  3. 输入框是否已清空")
    
    success = input("\n消息是否成功发送? (y/n): ").strip().lower()
    
    if success == 'y':
        print("\n✅ 消息发送成功！")
        return True
    else:
        print("\n❌ 消息未成功发送")
        print("请查看截图:")
        print("  screenshots/file_helper_verified/")
        return False


if __name__ == "__main__":
    import sys
    
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "你好"
    
    print(f"\n准备发送消息: {message}")
    print("每一步都会暂停等待你确认\n")
    
    result = send_to_file_helper_verified(message)
    
    if result:
        print("\n🎉 测试完成，消息已成功发送！")
    else:
        print("\n⚠️  测试未通过，需要调整")
