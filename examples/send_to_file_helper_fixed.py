#!/usr/bin/env python3
"""
给文件传输助手发送消息 - 修复版（使用剪贴板输入）
"""

import uiautomator2 as u2
import time
import os


def send_to_file_helper_fixed(message="你好"):
    """使用剪贴板方式发送消息"""
    print("=" * 60)
    print("给文件传输助手发送消息（修复版）")
    print("=" * 60)
    
    d = u2.connect()
    width, height = d.window_size()
    print(f"\n设备: {d.device_info['model']} ({width}x{height})")
    
    os.makedirs("screenshots/fixed_send", exist_ok=True)
    
    # 步骤1: 启动微信
    print("\n[1/8] 启动微信...")
    d.app_start("com.tencent.mm")
    time.sleep(3)
    d.click(int(width * 0.125), int(height * 0.95))
    time.sleep(1)
    d.screenshot().save("screenshots/fixed_send/01_wechat_list.jpg")
    print("✓ 微信已启动")
    
    # 步骤2: 点击右上角搜索
    print("[2/8] 点击搜索...")
    search_x = int(width * 0.9)
    search_y = int(height * 0.06)
    d.click(search_x, search_y)
    time.sleep(2)
    d.screenshot().save("screenshots/fixed_send/02_search.jpg")
    print("✓ 搜索已打开")
    
    # 步骤3: 输入搜索词（使用剪贴板）
    print("[3/8] 输入'文件传输助手'...")
    d.set_clipboard("文件传输助手")
    time.sleep(0.5)
    # 长按输入框粘贴
    d.long_click(int(width * 0.5), int(height * 0.15), 1.5)
    time.sleep(1)
    # 点击粘贴按钮（通常在中间偏上）
    d.click(int(width * 0.5), int(height * 0.12))
    time.sleep(2)
    d.screenshot().save("screenshots/fixed_send/03_search_result.jpg")
    print("✓ 搜索词已输入")
    
    # 步骤4: 点击第一个结果
    print("[4/8] 点击搜索结果...")
    d.click(int(width * 0.5), int(height * 0.3))
    time.sleep(2)
    d.screenshot().save("screenshots/fixed_send/04_chat_opened.jpg")
    print("✓ 聊天窗口已打开")
    
    # 步骤5: 点击输入框
    print("[5/8] 点击输入框...")
    input_x = int(width * 0.4)  # 左侧一点，避开语音按钮
    input_y = int(height * 0.92)
    d.click(input_x, input_y)
    time.sleep(1)
    d.screenshot().save("screenshots/fixed_send/05_input_focused.jpg")
    print("✓ 输入框已激活")
    
    # 步骤6: 使用剪贴板输入消息
    print(f"[6/8] 使用剪贴板输入: '{message}'")
    d.set_clipboard(message)
    time.sleep(0.5)
    d.screenshot().save("screenshots/fixed_send/06_clipboard_set.jpg")
    print("✓ 剪贴板已设置")
    
    # 步骤7: 长按输入框并粘贴
    print("[7/8] 粘贴消息...")
    d.long_click(input_x, input_y, 1.5)
    time.sleep(1)
    # 点击粘贴选项（通常在输入框上方）
    paste_y = int(height * 0.85)
    d.click(int(width * 0.5), paste_y)
    time.sleep(1)
    d.screenshot().save("screenshots/fixed_send/07_message_pasted.jpg")
    print("✓ 消息已粘贴")
    
    # 步骤8: 点击发送
    print("[8/8] 点击发送按钮...")
    send_x = int(width * 0.95)
    send_y = int(height * 0.92)
    d.click(send_x, send_y)
    time.sleep(2)
    d.screenshot().save("screenshots/fixed_send/08_sent.jpg")
    print("✓ 已点击发送")
    
    print("\n" + "=" * 60)
    print("✅ 执行完成！")
    print("=" * 60)
    print(f"\n截图保存: screenshots/fixed_send/")
    print("\n⚠️  请检查手机:")
    print(f"  1. 文件传输助手中是否收到'{message}'?")
    print("  2. 是文字消息还是语音消息？")
    print("  3. 查看 screenshots/fixed_send/08_sent.jpg")


if __name__ == "__main__":
    import sys
    
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "你好"
    
    print(f"准备发送消息: {message}")
    print("使用剪贴板方式，避免触发语音输入\n")
    
    send_to_file_helper_fixed(message)
