#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信联系人管理模块
"""

import uiautomator2 as u2
import time
import os

class WeChatContactManager:
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
            os.system('adb shell ime set com.baidu.input_mi/.ImeService')
    
    def go_to_chat_list(self):
        """返回到聊天列表首页"""
        # 点击底部"微信"标签（通常在最左侧）
        chat_tab_x = int(self.width * 0.12)  # 12% 宽度
        chat_tab_y = int(self.height * 0.98)  # 98% 高度（底部导航栏）
        
        print("📱 返回聊天列表...")
        self.d.click(chat_tab_x, chat_tab_y)
        time.sleep(0.5)
        
        return True
    
    def open_search(self):
        """打开搜索功能"""
        # 搜索按钮通常在右上角
        search_x = int(self.width * 0.90)  # 90% 宽度
        search_y = int(self.height * 0.06)  # 6% 高度（顶部）
        
        print("🔍 打开搜索...")
        self.d.click(search_x, search_y)
        time.sleep(1.0)
        
        return True
    
    def search_contact(self, contact_name):
        """
        搜索联系人
        
        Args:
            contact_name: 联系人名称
        
        Returns:
            bool: 是否搜索成功
        """
        # 搜索框通常在顶部中间
        search_input_x = int(self.width * 0.50)
        search_input_y = int(self.height * 0.10)
        
        print(f"🔎 搜索: {contact_name}")
        
        # 点击搜索框
        self.d.click(search_input_x, search_input_y)
        time.sleep(0.5)
        
        # 清空
        for _ in range(20):
            self.d.press("del")
        time.sleep(0.3)
        
        # 输入联系人名称
        self.d.send_keys(contact_name)
        time.sleep(1.5)  # 等待搜索结果
        
        return True
    
    def select_first_result(self):
        """选择第一个搜索结果"""
        # 第一个结果通常在搜索框下方
        result_x = int(self.width * 0.50)
        result_y = int(self.height * 0.25)  # 25% 高度
        
        print("✅ 选择第一个结果...")
        self.d.click(result_x, result_y)
        time.sleep(1.0)
        
        return True
    
    def open_chat_window(self, contact_name):
        """
        打开指定联系人的聊天窗口
        
        Args:
            contact_name: 联系人名称
        
        Returns:
            bool: 是否成功打开
        """
        try:
            print(f"\n{'='*60}")
            print(f"打开联系人聊天窗口: {contact_name}")
            print('='*60)
            
            # 1. 返回聊天列表
            self.go_to_chat_list()
            time.sleep(0.5)
            
            # 2. 打开搜索
            self.open_search()
            time.sleep(0.5)
            
            # 3. 搜索联系人
            self.search_contact(contact_name)
            time.sleep(1.0)
            
            # 4. 选择第一个结果
            self.select_first_result()
            time.sleep(1.0)
            
            print("✅ 聊天窗口已打开")
            return True
            
        except Exception as e:
            print(f"❌ 打开聊天窗口失败: {e}")
            return False
    
    def screenshot_chat_window(self, save_path="screenshots/current_chat.jpg"):
        """截图当前聊天窗口"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.d.screenshot(save_path)
        print(f"📸 截图已保存: {save_path}")
        return save_path

if __name__ == "__main__":
    import sys
    
    contact_manager = WeChatContactManager()
    
    if len(sys.argv) > 1:
        contact_name = sys.argv[1]
    else:
        contact_name = "文件传输助手"
    
    # 打开聊天窗口
    success = contact_manager.open_chat_window(contact_name)
    
    if success:
        # 截图确认
        contact_manager.screenshot_chat_window(f"screenshots/contact_{contact_name}.jpg")
        print(f"\n✅ 已成功打开 '{contact_name}' 的聊天窗口")
    else:
        print(f"\n❌ 无法打开 '{contact_name}' 的聊天窗口")
