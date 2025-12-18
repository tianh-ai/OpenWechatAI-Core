#!/usr/bin/env python3
"""
微信手机通信完整测试
包含发送、接收、自动回复
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os
from PIL import Image


class WeChatCommunicationTest:
    """微信通信测试器"""
    
    def __init__(self):
        """初始化"""
        print("初始化通信测试器...")
        self.d = u2.connect()
        self.package = "com.tencent.mm"
        
        self.width, self.height = self.d.window_size()
        device_info = self.d.device_info
        
        print(f"✓ 设备: {device_info['model']}")
        print(f"✓ Android: {device_info.get('version', 'Unknown')}")
        print(f"✓ 分辨率: {self.width}x{self.height}")
        
        os.makedirs("screenshots/comm_test", exist_ok=True)
        
        # 消息计数
        self.sent_count = 0
        self.received_count = 0
    
    def screenshot(self, name):
        """截图并返回路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/comm_test/{name}_{timestamp}.jpg"
        
        img = self.d.screenshot()
        img.save(filename)
        return filename, img
    
    def log(self, message, level="INFO"):
        """日志输出"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✓",
            "ERROR": "✗",
            "SEND": "📤",
            "RECEIVE": "📥",
        }.get(level, "•")
        
        print(f"[{timestamp}] {prefix} {message}")
    
    def start_wechat(self):
        """启动微信"""
        self.log("启动微信...")
        
        # 停止微信（如果正在运行）
        self.d.app_stop(self.package)
        time.sleep(1)
        
        # 启动微信
        self.d.app_start(self.package)
        time.sleep(3)
        
        # 点击微信tab
        tab_x = int(self.width * 0.125)
        tab_y = int(self.height * 0.95)
        self.d.click(tab_x, tab_y)
        time.sleep(1)
        
        self.log("微信已启动", "SUCCESS")
        self.screenshot("startup")
    
    def open_chat(self, position=0.2):
        """打开聊天
        
        Args:
            position: 聊天位置比例 (0.15-0.8)
        """
        x = int(self.width * 0.5)
        y = int(self.height * position)
        
        self.log(f"打开聊天 (位置: {position*100:.0f}%)")
        self.d.click(x, y)
        time.sleep(2)
        
        filename, _ = self.screenshot("chat_opened")
        self.log(f"聊天已打开", "SUCCESS")
    
    def send_message(self, text):
        """发送消息
        
        Args:
            text: 消息内容
        """
        self.log(f"准备发送: '{text}'", "SEND")
        
        # 1. 点击输入框
        input_x = int(self.width * 0.5)
        input_y = int(self.height * 0.92)
        self.d.click(input_x, input_y)
        time.sleep(0.5)
        
        # 2. 输入文本
        self.d.send_keys(text)
        time.sleep(0.8)
        
        # 截图
        self.screenshot(f"msg_{self.sent_count}_typed")
        
        # 3. 点击发送
        send_x = int(self.width * 0.95)
        send_y = int(self.height * 0.92)
        self.d.click(send_x, send_y)
        time.sleep(1)
        
        self.sent_count += 1
        self.log(f"消息已发送 (#{self.sent_count})", "SUCCESS")
        
        # 发送后截图
        self.screenshot(f"msg_{self.sent_count}_sent")
    
    def wait_for_reply(self, timeout=30):
        """等待回复
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            bool: 是否收到回复
        """
        self.log(f"等待回复 (最多{timeout}秒)...", "RECEIVE")
        
        # 获取初始截图
        _, initial_img = self.screenshot("wait_initial")
        
        start_time = time.time()
        check_interval = 2
        
        while time.time() - start_time < timeout:
            time.sleep(check_interval)
            
            # 获取当前截图
            _, current_img = self.screenshot("wait_checking")
            
            # 简单对比（裁剪聊天区域）
            chat_area = (0, int(self.height * 0.15), 
                        self.width, int(self.height * 0.85))
            
            initial_crop = initial_img.crop(chat_area)
            current_crop = current_img.crop(chat_area)
            
            # 检测变化
            if self._images_different(initial_crop, current_crop):
                elapsed = time.time() - start_time
                self.log(f"检测到新消息！({elapsed:.1f}秒)", "RECEIVE")
                self.received_count += 1
                self.screenshot("reply_received")
                return True
            
            elapsed = time.time() - start_time
            remaining = timeout - elapsed
            self.log(f"继续等待... (剩余 {remaining:.0f}秒)")
        
        self.log("等待超时，未收到回复", "ERROR")
        return False
    
    def _images_different(self, img1, img2, threshold=0.05):
        """检测两张图片是否不同
        
        Args:
            img1, img2: PIL Image对象
            threshold: 差异阈值
        
        Returns:
            bool: 是否不同
        """
        # 缩小图片加速对比
        size = (108, 168)
        img1_small = img1.resize(size)
        img2_small = img2.resize(size)
        
        diff_count = 0
        total = size[0] * size[1]
        
        for x in range(size[0]):
            for y in range(size[1]):
                p1 = img1_small.getpixel((x, y))
                p2 = img2_small.getpixel((x, y))
                
                if isinstance(p1, tuple):
                    diff = sum(abs(a - b) for a, b in zip(p1, p2))
                    if diff > 30:
                        diff_count += 1
                else:
                    if abs(p1 - p2) > 30:
                        diff_count += 1
        
        change_ratio = diff_count / total
        return change_ratio > threshold
    
    def auto_reply(self, reply_text):
        """自动回复
        
        Args:
            reply_text: 回复内容
        """
        self.log(f"自动回复: '{reply_text}'")
        time.sleep(1)
        self.send_message(reply_text)
    
    def back_to_list(self):
        """返回聊天列表"""
        self.log("返回聊天列表...")
        self.d.press("back")
        time.sleep(1)
        self.screenshot("back_to_list")
    
    def test_basic_send(self):
        """测试基本发送"""
        print("\n" + "=" * 60)
        print("测试1: 基本消息发送")
        print("=" * 60)
        
        self.start_wechat()
        self.open_chat()
        
        messages = [
            "测试消息 1",
            "Hello, World!",
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ]
        
        for msg in messages:
            self.send_message(msg)
            time.sleep(2)
        
        self.back_to_list()
        
        print("\n" + "=" * 60)
        print(f"✓ 测试完成！已发送 {self.sent_count} 条消息")
        print("=" * 60)
    
    def test_send_and_receive(self):
        """测试发送并等待回复"""
        print("\n" + "=" * 60)
        print("测试2: 发送消息并等待回复")
        print("=" * 60)
        print("\n⚠️  请在手机上准备给测试聊天发送回复")
        print("提示: 等待10秒后，请手动发送一条消息\n")
        
        input("按回车开始测试...")
        
        self.start_wechat()
        self.open_chat()
        
        # 发送测试消息
        self.send_message("请回复这条消息进行测试")
        
        # 等待回复
        if self.wait_for_reply(timeout=30):
            print("\n✓ 成功接收到回复！")
        else:
            print("\n⚠ 未收到回复（可能是超时）")
        
        self.back_to_list()
        
        print("\n" + "=" * 60)
        print(f"测试完成！发送: {self.sent_count}, 接收: {self.received_count}")
        print("=" * 60)
    
    def test_auto_reply(self):
        """测试自动回复"""
        print("\n" + "=" * 60)
        print("测试3: 自动回复功能")
        print("=" * 60)
        print("\n📱 测试步骤:")
        print("1. 脚本会发送一条消息")
        print("2. 等待你手动回复")
        print("3. 检测到回复后自动发送回复\n")
        
        input("按回车开始测试...")
        
        self.start_wechat()
        self.open_chat()
        
        # 发送初始消息
        self.send_message("请回复任意消息，我会自动回复你")
        
        # 等待用户回复
        if self.wait_for_reply(timeout=60):
            # 自动回复
            self.auto_reply("收到！这是自动回复消息 🤖")
            time.sleep(2)
            
            print("\n✓ 自动回复成功！")
        else:
            print("\n⚠ 未检测到回复")
        
        self.back_to_list()
        
        print("\n" + "=" * 60)
        print("自动回复测试完成")
        print("=" * 60)
    
    def test_continuous_monitor(self):
        """测试持续监控"""
        print("\n" + "=" * 60)
        print("测试4: 持续监控和自动回复")
        print("=" * 60)
        print("\n🤖 监控模式:")
        print("- 持续监控新消息")
        print("- 每次收到消息自动回复")
        print("- 按 Ctrl+C 停止\n")
        
        input("按回车开始监控...")
        
        self.start_wechat()
        self.open_chat()
        
        self.send_message("监控已开启，请发送消息测试")
        
        reply_count = 0
        
        try:
            while True:
                self.log("等待新消息...")
                
                if self.wait_for_reply(timeout=60):
                    reply_count += 1
                    
                    # 自动回复
                    reply = f"自动回复 #{reply_count} - {datetime.now().strftime('%H:%M:%S')}"
                    self.auto_reply(reply)
                    
                    self.log(f"已回复 {reply_count} 次", "SUCCESS")
                else:
                    self.log("监控超时，继续等待...")
        
        except KeyboardInterrupt:
            print("\n\n停止监控")
        
        finally:
            self.back_to_list()
            
            print("\n" + "=" * 60)
            print(f"监控结束！共处理 {reply_count} 条消息")
            print("=" * 60)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "=" * 60)
        print("完整通信测试套件")
        print("=" * 60)
        
        tests = [
            ("基本发送", self.test_basic_send),
            ("发送接收", self.test_send_and_receive),
            ("自动回复", self.test_auto_reply),
        ]
        
        for name, test_func in tests:
            try:
                print(f"\n开始测试: {name}")
                test_func()
                print(f"✓ {name} 测试通过")
            except Exception as e:
                print(f"✗ {name} 测试失败: {e}")
            
            time.sleep(3)
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print(f"总发送: {self.sent_count}")
        print(f"总接收: {self.received_count}")
        print("=" * 60)


def main():
    """主函数"""
    tester = WeChatCommunicationTest()
    
    print("\n" + "=" * 60)
    print("微信手机通信测试")
    print("=" * 60)
    print("\n选择测试:")
    print("1. 基本发送测试（快速）")
    print("2. 发送并等待回复")
    print("3. 自动回复测试")
    print("4. 持续监控模式")
    print("5. 运行所有测试")
    
    choice = input("\n请选择 (1-5): ").strip()
    
    tests = {
        '1': tester.test_basic_send,
        '2': tester.test_send_and_receive,
        '3': tester.test_auto_reply,
        '4': tester.test_continuous_monitor,
        '5': tester.run_all_tests,
    }
    
    test_func = tests.get(choice, tester.test_basic_send)
    test_func()
    
    print("\n📊 测试统计:")
    print(f"  发送消息: {tester.sent_count}")
    print(f"  接收消息: {tester.received_count}")
    print(f"\n📁 截图目录: screenshots/comm_test/")


if __name__ == "__main__":
    main()
