#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信消息接收模块 - 基于OCR识别
"""

import uiautomator2 as u2
import time
import os
from PIL import Image
import imagehash

class WeChatReceiver:
    def __init__(self):
        self.d = u2.connect()
        self.width, self.height = self.d.window_size()
        self.last_screenshot_hash = None
        self.current_chat_title = None  # 当前聊天窗口标题
        
    def _get_chat_area_screenshot(self):
        """截取聊天区域（排除底部输入框）"""
        # 聊天区域大约是顶部到88%高度
        self.d.screenshot("screenshots/temp_full.jpg")
        
        img = Image.open("screenshots/temp_full.jpg")
        # 裁剪聊天区域（顶部10% - 底部88%）
        chat_area = img.crop((0, int(self.height * 0.10), self.width, int(self.height * 0.88)))
        
        return chat_area
    
    def click_latest_chat_with_red_dot(self):
        """点击最新的有红点标记的聊天（新消息）"""
        try:
            # 方法1: 查找红点标记（未读消息数字）
            # 微信的未读消息通常显示为红色圆圈数字
            red_dots = self.d.xpath('//*[@resource-id="com.tencent.mm:id/h8h"]').all()
            
            if red_dots:
                # 找到最上面的红点（最新消息）
                first_dot = red_dots[0]
                # 点击红点所在的聊天项
                parent = first_dot.parent()
                if parent:
                    bounds = parent.info.get('bounds', {})
                    center_x = (bounds.get('left', 0) + bounds.get('right', self.width)) / 2
                    center_y = (bounds.get('top', 0) + bounds.get('bottom', self.height)) / 2
                    self.d.click(center_x, center_y)
                    print("  👆 点击进入聊天窗口（通过红点定位）")
                    time.sleep(1)  # 等待进入
                    return True
            
            # 方法2: 点击聊天列表第一项（最新对话）
            # 微信聊天列表通常在顶部显示最新消息
            # 点击屏幕上方中间位置（第一个聊天项）
            click_y = int(self.height * 0.20)  # 顶部20%位置
            click_x = int(self.width * 0.50)   # 中间
            self.d.click(click_x, click_y)
            print("  👆 点击进入聊天窗口（点击列表第一项）")
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"  ⚠️  进入聊天失败: {e}")
            # 降级方案：点击屏幕上方
            click_y = int(self.height * 0.20)
            click_x = int(self.width * 0.50)
            self.d.click(click_x, click_y)
            time.sleep(1)
            return True
    
    def _has_new_message(self):
        """检测是否有新消息（通过截图对比）"""
        current_img = self._get_chat_area_screenshot()
        current_hash = imagehash.average_hash(current_img)
        
        if self.last_screenshot_hash is None:
            self.last_screenshot_hash = current_hash
            return False
        
        # 计算差异
        diff = current_hash - self.last_screenshot_hash
        
        if diff > 5:  # 差异阈值
            self.last_screenshot_hash = current_hash
            return True
        
        return False
    
    def wait_for_new_message(self, timeout=60):
        """
        等待新消息到来
        
        Args:
            timeout: 超时时间（秒）
        
        Returns:
            bool: 是否收到新消息
        """
        print(f"⏳ 等待新消息（超时: {timeout}秒）...")
        
        start_time = time.time()
        check_interval = 2  # 每2秒检查一次
        
        # 初始化
        self._has_new_message()
        
        while time.time() - start_time < timeout:
            time.sleep(check_interval)
            
            if self._has_new_message():
                print("✓ 检测到新消息！")
                return True
            
            elapsed = int(time.time() - start_time)
            print(f"  已等待 {elapsed}秒...", end='\r')
        
        print(f"\n⏱️  超时，未收到新消息")
        return False
    
    def get_latest_message_screenshot(self, save_path="screenshots/latest_message.jpg"):
        """
        获取最新消息的截图
        
        Args:
            save_path: 保存路径
        
        Returns:
            str: 截图路径
        """
        # 截取聊天区域下半部分（最新消息通常在底部）
        self.d.screenshot("screenshots/temp_full.jpg")
        
        img = Image.open("screenshots/temp_full.jpg")
        # 裁剪最底部的一条消息区域（更精确，减少干扰）
        # 微信消息通常在底部，输入框上方
        latest_area = img.crop((
            0, 
            int(self.height * 0.75),  # 从75%高度开始（只截取最底部）
            self.width, 
            int(self.height * 0.88)   # 到88%高度（输入框上方）
        ))
        
        # 确保保存路径的目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        latest_area.save(save_path)
        return save_path

if __name__ == "__main__":
    receiver = WeChatReceiver()
    
    print("="*60)
    print("微信消息监控测试")
    print("="*60)
    print(f"\n📱 设备: {receiver.width}x{receiver.height}")
    print("\n请在手机上向当前聊天窗口发送一条消息...")
    
    # 等待新消息
    if receiver.wait_for_new_message(timeout=30):
        # 截图保存
        msg_path = receiver.get_latest_message_screenshot()
        print(f"\n📸 最新消息截图: {msg_path}")
        print(f"    查看: open {msg_path}")
    else:
        print("\n未检测到新消息")
