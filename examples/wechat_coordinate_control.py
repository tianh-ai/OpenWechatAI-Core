#!/usr/bin/env python3
"""
基于坐标的微信自动化
适用于Android 15无法获取UI元素的情况
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os
from PIL import Image


class WeChatCoordinateController:
    """基于坐标的微信控制器"""
    
    def __init__(self):
        """初始化"""
        print("初始化微信控制器...")
        self.d = u2.connect()
        self.package = "com.tencent.mm"
        
        # 获取屏幕尺寸
        self.width, self.height = self.d.window_size()
        print(f"✓ 设备: {self.d.device_info['model']}")
        print(f"✓ 分辨率: {self.width}x{self.height}")
        
        # 确保截图目录存在
        os.makedirs("screenshots", exist_ok=True)
        
        # 定义底部导航栏位置（基于比例）
        # 假设底部导航栏在屏幕底部5%的位置
        self.tab_y = self.height * 0.95
        
        # 4个tab的X坐标（微信、通讯录、发现、我）
        # 平分屏幕宽度
        self.tabs = {
            'chat': self.width * 0.125,      # 微信
            'contacts': self.width * 0.375,   # 通讯录
            'discover': self.width * 0.625,   # 发现
            'me': self.width * 0.875,         # 我
        }
    
    def screenshot(self, name="screenshot"):
        """截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.jpg"
        
        img = self.d.screenshot()
        img.save(filename)
        print(f"✓ 截图: {filename}")
        return filename, img
    
    def start_wechat(self):
        """启动微信"""
        print("\n启动微信...")
        self.d.app_start(self.package)
        time.sleep(3)
        
        current = self.d.app_current()
        if current['package'] == self.package:
            print("✓ 微信已启动")
            return True
        return False
    
    def go_to_tab(self, tab_name):
        """切换到指定tab
        
        Args:
            tab_name: 'chat', 'contacts', 'discover', 'me'
        """
        if tab_name not in self.tabs:
            print(f"⚠ 未知tab: {tab_name}")
            return False
        
        x = int(self.tabs[tab_name])
        y = int(self.tab_y)
        
        print(f"点击 {tab_name} tab ({x}, {y})...")
        self.d.click(x, y)
        time.sleep(1)
        return True
    
    def click_search(self):
        """点击搜索（顶部区域）"""
        x = int(self.width * 0.5)
        y = int(self.height * 0.08)
        
        print(f"点击搜索 ({x}, {y})...")
        self.d.click(x, y)
        time.sleep(1)
    
    def click_first_chat(self):
        """点击第一个聊天"""
        x = int(self.width * 0.5)
        y = int(self.height * 0.2)  # 顶部20%位置
        
        print(f"点击第一个聊天 ({x}, {y})...")
        self.d.click(x, y)
        time.sleep(1)
    
    def send_message(self, text):
        """发送消息
        
        Args:
            text: 消息内容
        """
        # 点击输入框（底部30%位置）
        input_x = int(self.width * 0.5)
        input_y = int(self.height * 0.9)
        
        print(f"点击输入框 ({input_x}, {input_y})...")
        self.d.click(input_x, input_y)
        time.sleep(0.5)
        
        # 输入文本
        print(f"输入文本: {text}")
        self.d.send_keys(text)
        time.sleep(0.5)
        
        # 点击发送按钮（右下角）
        send_x = int(self.width * 0.95)
        send_y = int(self.height * 0.9)
        
        print(f"点击发送 ({send_x}, {send_y})...")
        self.d.click(send_x, send_y)
        time.sleep(1)
    
    def back(self):
        """返回"""
        print("返回...")
        self.d.press("back")
        time.sleep(1)
    
    def compare_screenshots(self, img1_path, img2_path):
        """比较两张截图是否相同
        
        Returns:
            float: 相似度 (0-1)
        """
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        
        # 简单的像素差异比较
        if img1.size != img2.size:
            return 0.0
        
        # 缩小图片加速比较
        img1_small = img1.resize((108, 240))
        img2_small = img2.resize((108, 240))
        
        # 计算差异
        diff = 0
        total = 108 * 240
        
        for x in range(108):
            for y in range(240):
                p1 = img1_small.getpixel((x, y))
                p2 = img2_small.getpixel((x, y))
                
                # RGB差异
                if isinstance(p1, tuple) and isinstance(p2, tuple):
                    diff += sum(abs(a - b) for a, b in zip(p1, p2))
                else:
                    diff += abs(p1 - p2)
        
        # 归一化 (RGB最大差异是255*3)
        max_diff = total * 255 * 3
        similarity = 1 - (diff / max_diff)
        
        return similarity
    
    def demo_navigation(self):
        """演示导航功能"""
        print("=" * 60)
        print("微信导航演示（基于坐标）")
        print("=" * 60)
        
        # 启动微信
        if not self.start_wechat():
            print("✗ 启动失败")
            return
        
        # 遍历所有tab
        tabs = ['chat', 'contacts', 'discover', 'me']
        for tab in tabs:
            print(f"\n切换到 {tab}...")
            self.go_to_tab(tab)
            self.screenshot(f"tab_{tab}")
        
        # 返回聊天tab
        print("\n返回聊天列表...")
        self.go_to_tab('chat')
        self.screenshot("final_chat")
        
        print("\n" + "=" * 60)
        print("✓ 演示完成！")
        print("=" * 60)
        print("\n截图保存在 screenshots/ 目录")
        print("可以查看不同tab的截图验证导航是否正确")


def main():
    """主函数"""
    controller = WeChatCoordinateController()
    controller.demo_navigation()


if __name__ == "__main__":
    main()
