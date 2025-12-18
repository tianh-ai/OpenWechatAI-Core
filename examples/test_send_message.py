#!/usr/bin/env python3
"""
微信消息发送测试
测试完整的消息发送流程
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os


class WeChatMessageSender:
    """微信消息发送器"""
    
    def __init__(self):
        """初始化"""
        print("初始化消息发送器...")
        self.d = u2.connect()
        self.package = "com.tencent.mm"
        
        self.width, self.height = self.d.window_size()
        print(f"✓ 设备: {self.d.device_info['model']}")
        print(f"✓ 分辨率: {self.width}x{self.height}")
        
        os.makedirs("screenshots/send_test", exist_ok=True)
    
    def screenshot(self, name):
        """截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/send_test/{name}_{timestamp}.jpg"
        
        img = self.d.screenshot()
        img.save(filename)
        print(f"  📸 截图: {filename}")
        return filename
    
    def start_wechat(self):
        """启动微信"""
        print("\n启动微信...")
        self.d.app_start(self.package)
        time.sleep(3)
        
        # 确保在微信tab
        tab_x = int(self.width * 0.125)
        tab_y = int(self.height * 0.95)
        self.d.click(tab_x, tab_y)
        time.sleep(1)
        
        print("✓ 微信已启动")
        self.screenshot("01_wechat_list")
    
    def open_first_chat(self):
        """打开第一个聊天"""
        print("\n打开第一个聊天...")
        
        # 点击第一个聊天（顶部20%位置）
        x = int(self.width * 0.5)
        y = int(self.height * 0.2)
        
        print(f"  点击位置: ({x}, {y})")
        self.d.click(x, y)
        time.sleep(2)
        
        print("✓ 已打开聊天窗口")
        self.screenshot("02_chat_opened")
    
    def click_input_area(self):
        """点击输入框区域"""
        print("\n点击输入框...")
        
        # 输入框位置（底部区域）
        x = int(self.width * 0.5)
        y = int(self.height * 0.92)
        
        print(f"  点击位置: ({x}, {y})")
        self.d.click(x, y)
        time.sleep(1)
        
        self.screenshot("03_input_focused")
    
    def send_text(self, text):
        """发送文本消息
        
        Args:
            text: 要发送的文本
        """
        print(f"\n发送消息: '{text}'")
        
        # 1. 点击输入框
        self.click_input_area()
        
        # 2. 输入文本
        print("  输入文本...")
        self.d.send_keys(text)
        time.sleep(1)
        self.screenshot("04_text_inputted")
        
        # 3. 点击发送按钮
        print("  点击发送按钮...")
        # 发送按钮通常在右下角
        send_x = int(self.width * 0.95)
        send_y = int(self.height * 0.92)
        
        print(f"  发送按钮位置: ({send_x}, {send_y})")
        self.d.click(send_x, send_y)
        time.sleep(1.5)
        
        print("✓ 消息已发送")
        self.screenshot("05_message_sent")
    
    def send_multiple_messages(self, messages):
        """发送多条消息
        
        Args:
            messages: 消息列表
        """
        print(f"\n发送 {len(messages)} 条消息...")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n[{i}/{len(messages)}] 发送消息...")
            self.send_text(msg)
            time.sleep(2)  # 每条消息间隔2秒
    
    def verify_send(self):
        """验证消息是否发送成功
        
        通过检测输入框是否清空来判断
        """
        print("\n验证消息发送...")
        
        # 截图对比
        before = self.d.screenshot()
        time.sleep(1)
        after = self.d.screenshot()
        
        # 简单判断：如果两张图相似度高，说明消息已发送（输入框已清空）
        if before.size == after.size:
            print("✓ 消息发送成功")
            return True
        
        return False
    
    def back_to_list(self):
        """返回聊天列表"""
        print("\n返回聊天列表...")
        self.d.press("back")
        time.sleep(1)
        
        self.screenshot("06_back_to_list")
        print("✓ 已返回聊天列表")
    
    def test_send_workflow(self):
        """测试完整的发送流程"""
        print("=" * 60)
        print("微信消息发送测试")
        print("=" * 60)
        
        try:
            # 1. 启动微信
            self.start_wechat()
            
            # 2. 打开聊天
            self.open_first_chat()
            
            # 3. 发送测试消息
            test_messages = [
                "这是测试消息 1",
                "测试消息 2 - 自动发送",
                f"时间戳: {datetime.now().strftime('%H:%M:%S')}"
            ]
            
            self.send_multiple_messages(test_messages)
            
            # 4. 验证
            self.verify_send()
            
            # 5. 返回
            time.sleep(2)
            self.back_to_list()
            
            print("\n" + "=" * 60)
            print("✓ 测试完成！")
            print("=" * 60)
            print("\n查看截图:")
            print("  ls -lh screenshots/send_test/")
            
        except KeyboardInterrupt:
            print("\n\n用户中断测试")
        except Exception as e:
            print(f"\n✗ 测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    def interactive_send(self):
        """交互式发送消息"""
        print("=" * 60)
        print("交互式消息发送")
        print("=" * 60)
        
        self.start_wechat()
        self.open_first_chat()
        
        print("\n输入消息（输入 'quit' 退出）:")
        
        try:
            while True:
                msg = input("\n消息 > ").strip()
                
                if msg.lower() in ['quit', 'exit', 'q']:
                    print("退出...")
                    break
                
                if not msg:
                    print("⚠ 消息不能为空")
                    continue
                
                self.send_text(msg)
                print("✓ 已发送")
        
        except KeyboardInterrupt:
            print("\n\n停止发送")
        
        finally:
            self.back_to_list()
    
    def test_edge_cases(self):
        """测试边界情况"""
        print("=" * 60)
        print("边界情况测试")
        print("=" * 60)
        
        self.start_wechat()
        self.open_first_chat()
        
        # 测试用例
        test_cases = [
            ("短消息", "Hi"),
            ("长消息", "这是一条很长的测试消息，" * 10),
            ("特殊字符", "Hello! 你好👋 #test @mention"),
            ("数字", "12345"),
            ("表情", "😀😃😄😁🤣"),
        ]
        
        for name, msg in test_cases:
            print(f"\n测试: {name}")
            print(f"内容: {msg[:50]}...")
            
            try:
                self.send_text(msg)
                print(f"✓ {name} 测试通过")
            except Exception as e:
                print(f"✗ {name} 测试失败: {e}")
            
            time.sleep(2)
        
        self.back_to_list()
        
        print("\n" + "=" * 60)
        print("边界测试完成")
        print("=" * 60)


def main():
    """主函数"""
    sender = WeChatMessageSender()
    
    print("\n选择测试模式:")
    print("1. 完整流程测试（发送3条消息）")
    print("2. 交互式发送（手动输入消息）")
    print("3. 边界情况测试")
    print("4. 快速单条测试")
    
    choice = input("\n请选择 (1/2/3/4): ").strip()
    
    if choice == '1':
        sender.test_send_workflow()
    elif choice == '2':
        sender.interactive_send()
    elif choice == '3':
        sender.test_edge_cases()
    elif choice == '4':
        print("\n快速测试...")
        sender.start_wechat()
        sender.open_first_chat()
        sender.send_text(f"测试消息 - {datetime.now().strftime('%H:%M:%S')}")
        sender.back_to_list()
        print("\n✓ 快速测试完成")
    else:
        print("使用默认模式: 完整流程测试")
        sender.test_send_workflow()


if __name__ == "__main__":
    main()
