#!/usr/bin/env python3
"""
给文件传输助手发送消息
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os


def send_to_file_helper(message="你好"):
    """给文件传输助手发送消息
    
    Args:
        message: 要发送的消息内容
    """
    print("=" * 60)
    print("给文件传输助手发送消息")
    print("=" * 60)
    
    # 连接设备
    print("\n连接设备...")
    d = u2.connect()
    width, height = d.window_size()
    print(f"✓ 设备已连接: {d.device_info['model']}")
    print(f"✓ 分辨率: {width}x{height}")
    
    os.makedirs("screenshots/file_helper", exist_ok=True)
    
    # 1. 启动微信
    print("\n1. 启动微信...")
    d.app_start("com.tencent.mm")
    time.sleep(3)
    
    # 点击微信tab
    tab_x = int(width * 0.125)
    tab_y = int(height * 0.95)
    d.click(tab_x, tab_y)
    time.sleep(1)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/01_wechat_list.jpg")
    print("✓ 微信已启动")
    
    # 2. 点击搜索
    print("\n2. 打开搜索...")
    search_x = int(width * 0.5)
    search_y = int(height * 0.08)
    d.click(search_x, search_y)
    time.sleep(2)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/02_search_opened.jpg")
    print("✓ 搜索已打开")
    
    # 3. 输入"文件传输助手"
    print("\n3. 搜索文件传输助手...")
    d.send_keys("文件传输助手")
    time.sleep(2)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/03_search_result.jpg")
    print("✓ 已输入搜索关键词")
    
    # 4. 点击搜索结果（第一个结果）
    print("\n4. 点击搜索结果...")
    result_x = int(width * 0.5)
    result_y = int(height * 0.25)
    d.click(result_x, result_y)
    time.sleep(2)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/04_file_helper_opened.jpg")
    print("✓ 文件传输助手已打开")
    
    # 5. 点击输入框
    print("\n5. 准备输入消息...")
    input_x = int(width * 0.5)
    input_y = int(height * 0.92)
    d.click(input_x, input_y)
    time.sleep(1)
    
    # 6. 输入消息
    print(f"\n6. 输入消息: '{message}'")
    d.send_keys(message)
    time.sleep(1)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/05_message_typed.jpg")
    print("✓ 消息已输入")
    
    # 7. 点击发送
    print("\n7. 发送消息...")
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    d.click(send_x, send_y)
    time.sleep(1.5)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/06_message_sent.jpg")
    print("✓ 消息已发送！")
    
    # 8. 返回
    print("\n8. 返回微信列表...")
    d.press("back")
    time.sleep(1)
    d.press("back")  # 退出搜索
    time.sleep(1)
    
    img = d.screenshot()
    img.save("screenshots/file_helper/07_back_to_list.jpg")
    print("✓ 已返回列表")
    
    print("\n" + "=" * 60)
    print("✅ 消息发送完成！")
    print("=" * 60)
    print(f"\n发送的消息: {message}")
    print(f"截图目录: screenshots/file_helper/")
    print("\n查看截图:")
    print("  ls -lh screenshots/file_helper/*.jpg")


if __name__ == "__main__":
    import sys
    
    # 从命令行参数获取消息，默认为"你好"
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "你好"
    
    send_to_file_helper(message)
