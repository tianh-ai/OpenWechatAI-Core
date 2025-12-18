#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息发送模块 - 最终可用版本
前提：微信设置中开启"回车键发送消息"
"""

import uiautomator2 as u2
import time
import os

class WeChatSender:
    def __init__(self):
        self.d = u2.connect()
        # 禁用自动切换输入法
        self.d.settings['operation_delay'] = (0, 0)
        self.d.settings['operation_delay_methods'] = []
        self.width, self.height = self.d.window_size()
        
        # 确保使用正确的输入法
        self._ensure_correct_ime()
    
    def _ensure_correct_ime(self):
        """确保使用正确的输入法（百度输入法）"""
        current_ime = os.popen('adb shell settings get secure default_input_method').read().strip()
        if 'AdbKeyboard' in current_ime:
            print("⚠️  检测到 AdbKeyboard，正在恢复...")
            os.system('adb shell ime set com.baidu.input_mi/.ImeService')
            print("✓ 已恢复百度输入法")
    
    def send_message(self, message, screenshot_dir=None):
        """
        发送消息到当前打开的聊天窗口
        
        Args:
            message: 要发送的消息内容
            screenshot_dir: 截图保存目录（可选）
        
        Returns:
            bool: 是否发送成功
        """
        if screenshot_dir:
            os.makedirs(screenshot_dir, exist_ok=True)
        
        text_input_x = int(self.width * 0.45)
        y = int(self.height * 0.92)
        
        try:
            # 1. 点击输入框
            self.d.click(text_input_x, y)
            time.sleep(0.5)
            
            # 2. 清空输入框
            for _ in range(25):
                self.d.press("del")
            time.sleep(0.3)
            
            if screenshot_dir:
                self.d.screenshot(f"{screenshot_dir}/01_cleared.jpg")
            
            # 3. 输入消息 - 使用更可靠的方法
            try:
                # 方法1: 尝试使用 send_keys
                self.d.send_keys(message)
            except Exception as e:
                # 方法2: 如果失败，使用 set_text (需要先找到输入框)
                print(f"  ⚠️  send_keys失败，使用备用方法: {e}")
                try:
                    # 使用坐标点击后再用 shell input
                    self.d.shell(f"input text '{message}'")
                except:
                    # 方法3: 最后的备用方案
                    print(f"  ⚠️  尝试使用ADB输入")
                    import subprocess
                    escaped_msg = message.replace("'", "\\'")
                    subprocess.run(['adb', 'shell', 'input', 'text', escaped_msg], check=False)
            
            time.sleep(0.8)
            
            if screenshot_dir:
                self.d.screenshot(f"{screenshot_dir}/02_typed.jpg")
            
            # 4. 按回车发送
            self.d.press("enter")
            time.sleep(1.0)
            
            if screenshot_dir:
                self.d.screenshot(f"{screenshot_dir}/03_sent.jpg")
            
            return True
            
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def send_to_contact(self, contact_name, message):
        """
        发送消息到指定联系人（需要先打开聊天列表）
        
        Args:
            contact_name: 联系人名称
            message: 消息内容
        
        Returns:
            bool: 是否发送成功
        """
        # TODO: 实现搜索联系人并打开聊天窗口
        pass

if __name__ == "__main__":
    import sys
    
    sender = WeChatSender()
    
    if len(sys.argv) > 1:
        msg = sys.argv[1]
    else:
        msg = "测试消息"
    
    print(f"📱 设备: {sender.width}x{sender.height}")
    print(f"📝 发送消息: {msg}")
    print()
    
    success = sender.send_message(msg, screenshot_dir="screenshots/send_message")
    
    if success:
        print()
        print("="*60)
        print("✅ 发送成功！")
        print("="*60)
        print("\n查看截图:")
        print("  open screenshots/send_message/02_typed.jpg")
        print("  open screenshots/send_message/03_sent.jpg")
    else:
        print("❌ 发送失败")
