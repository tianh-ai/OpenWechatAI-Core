#!/usr/bin/env python3
"""
微信消息监控和自动回复
使用OCR识别消息内容
"""

import uiautomator2 as u2
import time
from datetime import datetime
from PIL import Image
import os


class WeChatMessageMonitor:
    """微信消息监控器"""
    
    def __init__(self):
        """初始化"""
        print("初始化消息监控器...")
        self.d = u2.connect()
        self.package = "com.tencent.mm"
        
        self.width, self.height = self.d.window_size()
        print(f"✓ 设备: {self.d.device_info['model']}")
        
        os.makedirs("screenshots/monitor", exist_ok=True)
        
        # 聊天区域（顶部20% - 底部20%）
        self.chat_area = {
            'x': 0,
            'y': int(self.height * 0.15),
            'width': self.width,
            'height': int(self.height * 0.7)
        }
        
        self.last_screenshot = None
        self.check_interval = 2  # 检查间隔（秒）
    
    def start_wechat(self):
        """启动微信并进入聊天列表"""
        print("\n启动微信...")
        self.d.app_start(self.package)
        time.sleep(3)
        
        # 点击微信tab
        tab_x = int(self.width * 0.125)
        tab_y = int(self.height * 0.95)
        self.d.click(tab_x, tab_y)
        time.sleep(1)
        
        print("✓ 进入聊天列表")
    
    def get_chat_area_screenshot(self):
        """获取聊天列表区域截图"""
        full_img = self.d.screenshot()
        
        # 裁剪聊天区域
        chat_img = full_img.crop((
            self.chat_area['x'],
            self.chat_area['y'],
            self.chat_area['x'] + self.chat_area['width'],
            self.chat_area['y'] + self.chat_area['height']
        ))
        
        return chat_img
    
    def detect_new_message(self):
        """检测是否有新消息
        
        Returns:
            bool: 是否检测到新消息
        """
        current = self.get_chat_area_screenshot()
        
        if self.last_screenshot is None:
            self.last_screenshot = current
            return False
        
        # 简单的像素差异检测
        # 缩小图片加速比较
        curr_small = current.resize((108, 168))
        last_small = self.last_screenshot.resize((108, 168))
        
        diff_count = 0
        threshold = 30  # 差异阈值
        
        for x in range(108):
            for y in range(168):
                p1 = curr_small.getpixel((x, y))
                p2 = last_small.getpixel((x, y))
                
                if isinstance(p1, tuple):
                    diff = sum(abs(a - b) for a, b in zip(p1, p2))
                    if diff > threshold:
                        diff_count += 1
                else:
                    if abs(p1 - p2) > threshold:
                        diff_count += 1
        
        # 如果超过5%的像素有变化，认为有新消息
        total_pixels = 108 * 168
        change_ratio = diff_count / total_pixels
        
        has_new = change_ratio > 0.05
        
        if has_new:
            print(f"✓ 检测到变化 ({change_ratio*100:.1f}%)")
            self.last_screenshot = current
        
        return has_new
    
    def click_first_chat(self):
        """点击第一个聊天"""
        x = int(self.width * 0.5)
        y = int(self.height * 0.2)
        
        print(f"打开第一个聊天...")
        self.d.click(x, y)
        time.sleep(2)
    
    def get_chat_screenshot(self):
        """获取聊天窗口截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/monitor/chat_{timestamp}.jpg"
        
        img = self.d.screenshot()
        img.save(filename)
        
        return filename, img
    
    def extract_messages_ocr(self, img):
        """使用OCR提取消息（需要安装paddleocr）
        
        Args:
            img: PIL Image对象
        
        Returns:
            list: 识别到的文字列表
        """
        try:
            from paddleocr import PaddleOCR
            
            # 初始化OCR（首次会下载模型）
            if not hasattr(self, 'ocr'):
                self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
            
            # 保存临时图片
            temp_path = "screenshots/monitor/temp_ocr.jpg"
            img.save(temp_path)
            
            # OCR识别
            result = self.ocr.ocr(temp_path, cls=True)
            
            # 提取文字
            messages = []
            if result and result[0]:
                for line in result[0]:
                    text = line[1][0]
                    confidence = line[1][1]
                    if confidence > 0.8:  # 置信度阈值
                        messages.append(text)
            
            return messages
            
        except ImportError:
            print("⚠ PaddleOCR未安装，无法识别消息")
            print("  安装命令: pip install paddleocr")
            return []
        except Exception as e:
            print(f"⚠ OCR识别失败: {e}")
            return []
    
    def send_reply(self, text):
        """发送回复"""
        # 点击输入框
        input_x = int(self.width * 0.5)
        input_y = int(self.height * 0.9)
        self.d.click(input_x, input_y)
        time.sleep(0.5)
        
        # 输入文本
        self.d.send_keys(text)
        time.sleep(0.5)
        
        # 点击发送
        send_x = int(self.width * 0.95)
        send_y = int(self.height * 0.9)
        self.d.click(send_x, send_y)
        time.sleep(1)
        
        print(f"✓ 已发送回复: {text}")
    
    def back_to_chat_list(self):
        """返回聊天列表"""
        self.d.press("back")
        time.sleep(1)
    
    def monitor_loop(self, duration=60):
        """监控循环
        
        Args:
            duration: 监控时长（秒），0表示持续监控
        """
        print("=" * 60)
        print("开始监控微信消息")
        print("=" * 60)
        print(f"检查间隔: {self.check_interval}秒")
        if duration > 0:
            print(f"监控时长: {duration}秒")
        else:
            print("持续监控（按Ctrl+C停止）")
        print()
        
        self.start_wechat()
        
        start_time = time.time()
        check_count = 0
        
        try:
            while True:
                check_count += 1
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 检查 #{check_count}...")
                
                # 检测新消息
                if self.detect_new_message():
                    print("→ 发现新消息！")
                    
                    # 打开聊天
                    self.click_first_chat()
                    
                    # 截图
                    filename, img = self.get_chat_screenshot()
                    print(f"→ 保存截图: {filename}")
                    
                    # OCR识别（可选）
                    messages = self.extract_messages_ocr(img)
                    if messages:
                        print(f"→ 识别到消息:")
                        for msg in messages[-3:]:  # 显示最后3条
                            print(f"   {msg}")
                    
                    # 返回列表
                    self.back_to_chat_list()
                
                # 检查是否超时
                if duration > 0 and time.time() - start_time > duration:
                    print("\n监控时间结束")
                    break
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n\n用户停止监控")
        
        print("\n" + "=" * 60)
        print(f"✓ 监控完成！共检查 {check_count} 次")
        print("=" * 60)
    
    def demo_with_reply(self):
        """演示监控和自动回复"""
        print("=" * 60)
        print("消息监控和自动回复演示")
        print("=" * 60)
        
        self.start_wechat()
        
        print("\n等待30秒，检测新消息...")
        print("（请在手机上给自己发送测试消息）\n")
        
        for i in range(15):  # 30秒，每2秒检查一次
            print(f"[{i+1}/15] 检查中...")
            
            if self.detect_new_message():
                print("\n✓ 检测到新消息！")
                
                # 打开聊天
                self.click_first_chat()
                
                # 截图
                filename, img = self.get_chat_screenshot()
                print(f"截图: {filename}")
                
                # 发送自动回复
                reply = "这是自动回复消息"
                self.send_reply(reply)
                
                # 再次截图
                filename2, _ = self.get_chat_screenshot()
                print(f"回复后截图: {filename2}")
                
                # 返回
                self.back_to_chat_list()
                
                print("\n✓ 自动回复完成！")
                break
            
            time.sleep(2)
        else:
            print("\n⚠ 未检测到新消息")
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)


def main():
    """主函数"""
    monitor = WeChatMessageMonitor()
    
    # 选择演示模式
    print("\n选择模式:")
    print("1. 消息监控演示（30秒）")
    print("2. 持续监控（60秒）")
    print("3. 自动回复演示")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == '1':
        monitor.monitor_loop(duration=30)
    elif choice == '2':
        monitor.monitor_loop(duration=60)
    elif choice == '3':
        monitor.demo_with_reply()
    else:
        print("使用默认模式: 监控30秒")
        monitor.monitor_loop(duration=30)


if __name__ == "__main__":
    main()
