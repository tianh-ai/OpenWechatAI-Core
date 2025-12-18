#!/usr/bin/env python3
"""
给文件传输助手发送消息 - ADB输入版本
"""

import uiautomator2 as u2
import time
import os
import subprocess


def adb_input_text(text):
    """使用ADB输入文本"""
    # 转义特殊字符
    escaped = text.replace(' ', '%s')
    cmd = f'adb shell input text "{escaped}"'
    subprocess.run(cmd, shell=True)


def send_to_file_helper_adb(message="你好"):
    """使用ADB输入方式发送消息"""
    print("=" * 60)
    print("给文件传输助手发送消息（ADB输入版）")
    print("=" * 60)
    
    d = u2.connect()
    width, height = d.window_size()
    print(f"\n设备: {d.device_info['model']} ({width}x{height})")
    
    os.makedirs("screenshots/adb_send", exist_ok=True)
    
    # 步骤1: 启动微信
    print("\n[1/7] 启动微信...")
    d.app_start("com.tencent.mm")
    time.sleep(3)
    d.click(int(width * 0.125), int(height * 0.95))
    time.sleep(1)
    d.screenshot().save("screenshots/adb_send/01_wechat.jpg")
    print("✓ 微信已启动")
    
    # 步骤2: 点击搜索
    print("[2/7] 点击搜索...")
    d.click(int(width * 0.9), int(height * 0.06))
    time.sleep(2)
    d.screenshot().save("screenshots/adb_send/02_search.jpg")
    print("✓ 搜索已打开")
    
    # 步骤3: 使用ADB输入搜索词
    print("[3/7] 使用ADB输入搜索词...")
    print("      (中文需要等待输入法)...")
    time.sleep(1)
    # 直接点击搜索框
    d.click(int(width * 0.5), int(height * 0.15))
    time.sleep(1)
    # 使用ADB输入（只支持英文，中文会有问题）
    # 改用模拟键盘输入
    subprocess.run('adb shell input text "wenjian"', shell=True)
    time.sleep(2)
    d.screenshot().save("screenshots/adb_send/03_input.jpg")
    print("✓ 已输入'wenjian'（拼音）")
    
    print("\n⚠️  问题：ADB input 不支持中文")
    print("让我改用另一种方法...")
    
    return False


def send_direct_to_chat(message="你好"):
    """直接进入第一个聊天发送（不用搜索）"""
    print("=" * 60)
    print("直接发送到第一个聊天")
    print("=" * 60)
    print("⚠️  请先手动打开文件传输助手聊天窗口")
    
    d = u2.connect()
    width, height = d.window_size()
    print(f"\n设备: {width}x{height}")
    
    os.makedirs("screenshots/direct_send", exist_ok=True)
    
    input("\n按回车开始（确保文件传输助手聊天窗口已打开）...")
    
    # 1. 截图确认
    print("\n[1/4] 确认当前界面...")
    d.screenshot().save("screenshots/direct_send/01_current.jpg")
    print("✓ 已截图")
    
    # 2. 点击输入框（文字输入区域，避开语音）
    print("[2/4] 点击输入框...")
    input_x = int(width * 0.4)  # 偏左，避免点到语音
    input_y = int(height * 0.92)
    print(f"      点击: ({input_x}, {input_y})")
    d.click(input_x, input_y)
    time.sleep(1)
    d.screenshot().save("screenshots/direct_send/02_clicked.jpg")
    print("✓ 已点击")
    
    # 3. 使用键盘输入（英文测试）
    print(f"[3/4] 尝试输入消息...")
    print("      使用d.send_keys()方法")
    
    # 清空输入
    for _ in range(10):
        d.press("del")
    time.sleep(0.5)
    
    # 输入消息
    d.send_keys(message)
    time.sleep(1.5)
    d.screenshot().save("screenshots/direct_send/03_typed.jpg")
    print(f"✓ 已输入'{message}'")
    
    # 4. 点击发送
    print("[4/4] 点击发送...")
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    print(f"      点击: ({send_x}, {send_y})")
    d.click(send_x, send_y)
    time.sleep(2)
    d.screenshot().save("screenshots/direct_send/04_sent.jpg")
    print("✓ 已点击发送")
    
    print("\n" + "=" * 60)
    print("完成！请查看:")
    print("  1. 手机上是否收到消息")
    print("  2. screenshots/direct_send/04_sent.jpg")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    # 使用英文测试，避免中文输入问题
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "hello"
    
    print("由于Android 15限制，我们采用直接发送方式")
    print("请先手动在手机上打开文件传输助手聊天窗口\n")
    
    send_direct_to_chat(message)
