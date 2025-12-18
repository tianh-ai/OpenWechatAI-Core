#!/usr/bin/env python3
"""
给文件传输助手发送消息 - 自动版本（保存每步截图）
"""

import uiautomator2 as u2
import time
import os


def send_to_file_helper_auto(message="你好"):
    """自动发送到文件传输助手"""
    print("=" * 60)
    print("给文件传输助手发送消息（自动版）")
    print("=" * 60)
    
    d = u2.connect()
    width, height = d.window_size()
    print(f"\n设备: {d.device_info['model']} ({width}x{height})")
    
    os.makedirs("screenshots/auto_send", exist_ok=True)
    
    steps = []
    
    # 步骤1: 启动微信
    print("\n[1/7] 启动微信...")
    d.app_start("com.tencent.mm")
    time.sleep(3)
    d.click(int(width * 0.125), int(height * 0.95))
    time.sleep(1)
    d.screenshot().save("screenshots/auto_send/01_wechat_list.jpg")
    steps.append("✓ 微信已启动")
    
    # 步骤2: 点击右上角搜索
    print("[2/7] 点击搜索...")
    search_x = int(width * 0.9)
    search_y = int(height * 0.06)
    print(f"      坐标: ({search_x}, {search_y})")
    d.click(search_x, search_y)
    time.sleep(2)
    d.screenshot().save("screenshots/auto_send/02_after_search.jpg")
    steps.append(f"✓ 点击搜索 ({search_x}, {search_y})")
    
    # 步骤3: 输入搜索词
    print("[3/7] 输入'文件传输助手'...")
    d.send_keys("文件传输助手")
    time.sleep(2)
    d.screenshot().save("screenshots/auto_send/03_search_result.jpg")
    steps.append("✓ 输入搜索词")
    
    # 步骤4: 点击第一个结果
    print("[4/7] 点击搜索结果...")
    result_x = int(width * 0.5)
    result_y = int(height * 0.3)
    print(f"      坐标: ({result_x}, {result_y})")
    d.click(result_x, result_y)
    time.sleep(2)
    d.screenshot().save("screenshots/auto_send/04_chat_opened.jpg")
    steps.append(f"✓ 点击结果 ({result_x}, {result_y})")
    
    # 步骤5: 点击输入框
    print("[5/7] 点击输入框...")
    input_x = int(width * 0.5)
    input_y = int(height * 0.92)
    print(f"      坐标: ({input_x}, {input_y})")
    d.click(input_x, input_y)
    time.sleep(1)
    d.screenshot().save("screenshots/auto_send/05_input_ready.jpg")
    steps.append(f"✓ 点击输入框 ({input_x}, {input_y})")
    
    # 步骤6: 输入消息
    print(f"[6/7] 输入消息: '{message}'")
    d.send_keys(message)
    time.sleep(1)
    d.screenshot().save("screenshots/auto_send/06_message_typed.jpg")
    steps.append(f"✓ 输入消息: {message}")
    
    # 步骤7: 点击发送
    print("[7/7] 点击发送按钮...")
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    print(f"      坐标: ({send_x}, {send_y})")
    d.click(send_x, send_y)
    time.sleep(2)
    d.screenshot().save("screenshots/auto_send/07_sent.jpg")
    steps.append(f"✓ 点击发送 ({send_x}, {send_y})")
    
    print("\n" + "=" * 60)
    print("执行完成！")
    print("=" * 60)
    
    print("\n执行的步骤:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    
    print(f"\n截图保存位置: screenshots/auto_send/")
    print(f"共 7 张截图")
    
    print("\n⚠️  请手动检查:")
    print("  1. 查看 screenshots/auto_send/07_sent.jpg")
    print("  2. 确认消息是否在聊天窗口右侧")
    print("  3. 确认输入框是否已清空")
    print("  4. 在手机上查看文件传输助手是否收到消息")
    
    return True


if __name__ == "__main__":
    import sys
    
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "你好"
    
    print(f"准备发送消息: {message}\n")
    send_to_file_helper_auto(message)
    
    print("\n" + "=" * 60)
    print("测试完成！请查看截图确认结果")
    print("=" * 60)
