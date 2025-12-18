#!/usr/bin/env python3
"""
微信自动化示例脚本
演示基本的微信控制功能
"""

import uiautomator2 as u2
import time
from datetime import datetime


class WeChatAutomation:
    """微信自动化控制类"""
    
    def __init__(self, device_serial=None):
        """初始化
        
        Args:
            device_serial: 设备序列号，None 则自动连接第一个设备
        """
        print("正在连接设备...")
        self.device = u2.connect(device_serial)
        self.package_name = "com.tencent.mm"
        print(f"✓ 已连接设备: {self.device.device_info['model']}")
    
    def start_wechat(self):
        """启动微信"""
        print("\n启动微信...")
        self.device.screen_on()
        self.device.app_start(self.package_name)
        time.sleep(3)  # 等待启动
        
        if self.is_wechat_running():
            print("✓ 微信已启动")
            return True
        else:
            print("✗ 微信启动失败")
            return False
    
    def is_wechat_running(self):
        """检查微信是否在前台运行"""
        current = self.device.app_current()
        return current['package'] == self.package_name
    
    def take_screenshot(self, filename=None):
        """截图
        
        Args:
            filename: 保存路径，None 则自动生成
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/wechat_{timestamp}.jpg"
        
        img = self.device.screenshot()
        img.save(filename)
        print(f"✓ 截图已保存: {filename}")
        return filename
    
    def go_to_chats(self):
        """切换到聊天列表"""
        print("\n切换到聊天列表...")
        # 点击底部导航栏的"微信"或"聊天"
        if self.device(text="微信").exists:
            self.device(text="微信").click()
            print("✓ 已切换到聊天")
        elif self.device(text="聊天").exists:
            self.device(text="聊天").click()
            print("✓ 已切换到聊天")
        else:
            print("⚠ 未找到聊天入口")
        time.sleep(1)
    
    def go_to_contacts(self):
        """切换到通讯录"""
        print("\n切换到通讯录...")
        if self.device(text="通讯录").exists:
            self.device(text="通讯录").click()
            print("✓ 已切换到通讯录")
            time.sleep(1)
        else:
            print("⚠ 未找到通讯录")
    
    def go_to_discover(self):
        """切换到发现"""
        print("\n切换到发现...")
        if self.device(text="发现").exists:
            self.device(text="发现").click()
            print("✓ 已切换到发现")
            time.sleep(1)
        else:
            print("⚠ 未找到发现")
    
    def go_to_me(self):
        """切换到我"""
        print("\n切换到我...")
        if self.device(text="我").exists:
            self.device(text="我").click()
            print("✓ 已切换到我")
            time.sleep(1)
        else:
            print("⚠ 未找到我")
    
    def search_contact(self, keyword):
        """搜索联系人
        
        Args:
            keyword: 搜索关键词
        """
        print(f"\n搜索联系人: {keyword}")
        
        # 先切到聊天页
        self.go_to_chats()
        
        # 点击搜索
        if self.device(description="搜索").exists:
            self.device(description="搜索").click()
            time.sleep(1)
            
            # 输入关键词
            if self.device(className="android.widget.EditText").exists:
                self.device(className="android.widget.EditText").set_text(keyword)
                print(f"✓ 已输入搜索词: {keyword}")
                time.sleep(2)
            else:
                print("⚠ 未找到搜索输入框")
        else:
            print("⚠ 未找到搜索按钮")
    
    def get_ui_hierarchy(self):
        """获取当前界面层级结构"""
        print("\n获取界面层级...")
        xml = self.device.dump_hierarchy()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/hierarchy_{timestamp}.xml"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml)
        
        print(f"✓ 界面层级已保存: {filename}")
        return filename
    
    def back(self):
        """返回上一页"""
        print("\n返回上一页...")
        self.device.press("back")
        time.sleep(1)
    
    def home(self):
        """返回主屏幕"""
        print("\n返回主屏幕...")
        self.device.press("home")
        time.sleep(1)
    
    def stop_wechat(self):
        """停止微信"""
        print("\n停止微信...")
        self.device.app_stop(self.package_name)
        print("✓ 微信已停止")


def demo_basic_operations():
    """演示基本操作"""
    print("=" * 60)
    print("微信自动化基本操作演示")
    print("=" * 60)
    
    # 初始化
    wechat = WeChatAutomation()
    
    try:
        # 启动微信
        if not wechat.start_wechat():
            return
        
        # 截图
        wechat.take_screenshot("screenshots/demo_1_start.jpg")
        
        # 导航测试
        wechat.go_to_chats()
        time.sleep(1)
        wechat.take_screenshot("screenshots/demo_2_chats.jpg")
        
        wechat.go_to_contacts()
        time.sleep(1)
        wechat.take_screenshot("screenshots/demo_3_contacts.jpg")
        
        wechat.go_to_discover()
        time.sleep(1)
        wechat.take_screenshot("screenshots/demo_4_discover.jpg")
        
        wechat.go_to_me()
        time.sleep(1)
        wechat.take_screenshot("screenshots/demo_5_me.jpg")
        
        # 回到聊天页
        wechat.go_to_chats()
        
        # 获取界面层级
        wechat.get_ui_hierarchy()
        
        print("\n" + "=" * 60)
        print("✓ 演示完成！")
        print("=" * 60)
        print("\n已生成截图:")
        print("  - screenshots/demo_1_start.jpg")
        print("  - screenshots/demo_2_chats.jpg")
        print("  - screenshots/demo_3_contacts.jpg")
        print("  - screenshots/demo_4_discover.jpg")
        print("  - screenshots/demo_5_me.jpg")
        print("\n界面层级文件:")
        print("  - screenshots/hierarchy_*.xml")
        
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
    finally:
        # 不关闭微信，保持运行状态
        print("\n提示: 微信保持运行状态")


if __name__ == "__main__":
    demo_basic_operations()
