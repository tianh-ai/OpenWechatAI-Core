#!/usr/bin/env python3
"""
完整的微信自动化测试
包含解锁、导航、消息读取等功能
"""

import uiautomator2 as u2
import time
from datetime import datetime
import os


class WeChatController:
    """微信控制器"""
    
    def __init__(self):
        """初始化"""
        print("初始化微信控制器...")
        self.d = u2.connect()
        self.package = "com.tencent.mm"
        print(f"✓ 已连接设备: {self.d.device_info['model']}")
        
        # 确保截图目录存在
        os.makedirs("screenshots", exist_ok=True)
    
    def unlock_screen(self):
        """解锁屏幕"""
        print("\n解锁屏幕...")
        
        # 唤醒屏幕
        self.d.screen_on()
        time.sleep(0.5)
        
        # 检查是否需要解锁
        if self.d.info.get('screenOn'):
            print("✓ 屏幕已唤醒")
            
            # 尝试上滑解锁
            width, height = self.d.window_size()
            self.d.swipe(width/2, height*0.8, width/2, height*0.2, duration=0.3)
            time.sleep(1)
        
        return True
    
    def start_wechat(self):
        """启动微信"""
        print("\n启动微信...")
        
        # 确保屏幕解锁
        self.unlock_screen()
        
        # 启动应用
        self.d.app_start(self.package)
        time.sleep(3)
        
        # 检查是否成功
        current = self.d.app_current()
        if current['package'] == self.package:
            print("✓ 微信已启动")
            return True
        else:
            print(f"⚠ 当前应用: {current['package']}")
            return False
    
    def take_screenshot(self, name="screenshot"):
        """截图"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.jpg"
        
        img = self.d.screenshot()
        img.save(filename)
        print(f"✓ 截图: {filename}")
        return filename
    
    def click_by_coordinate(self, x_ratio, y_ratio):
        """按坐标比例点击
        
        Args:
            x_ratio: X 坐标比例 (0-1)
            y_ratio: Y 坐标比例 (0-1)
        """
        width, height = self.d.window_size()
        x = int(width * x_ratio)
        y = int(height * y_ratio)
        
        print(f"点击坐标: ({x}, {y})")
        self.d.click(x, y)
        time.sleep(1)
    
    def navigate_tabs(self):
        """导航测试 - 点击底部标签栏的不同位置"""
        print("\n测试底部导航栏...")
        
        width, height = self.d.window_size()
        bottom_y = height * 0.95  # 底部 95% 位置
        
        # 微信底部通常有4个或5个tab
        # 从左到右依次点击
        positions = [
            (0.125, "标签1"),  # 最左
            (0.375, "标签2"),  # 中左
            (0.625, "标签3"),  # 中右
            (0.875, "标签4"),  # 最右
        ]
        
        for x_ratio, name in positions:
            print(f"\n点击 {name}...")
            x = int(width * x_ratio)
            self.d.click(x, int(bottom_y))
            time.sleep(2)
            self.take_screenshot(name)
    
    def test_search(self):
        """测试搜索功能"""
        print("\n测试搜索...")
        
        # 点击屏幕上方 (搜索区域)
        width, height = self.d.window_size()
        self.d.click(width/2, height*0.1)
        time.sleep(1)
        self.take_screenshot("search")
    
    def get_all_elements(self):
        """获取所有界面元素"""
        print("\n获取界面元素...")
        
        # 使用 xpath 获取所有元素
        try:
            # 获取所有可见元素
            elements = self.d.xpath('//*').all()
            print(f"找到 {len(elements)} 个元素")
            
            # 打印前10个元素信息
            print("\n前10个元素:")
            for i, elem in enumerate(elements[:10], 1):
                try:
                    info = elem.info
                    print(f"{i}. {info.get('className', 'Unknown')}")
                    if info.get('text'):
                        print(f"   文本: {info['text']}")
                    if info.get('contentDescription'):
                        print(f"   描述: {info['contentDescription']}")
                except:
                    pass
        except Exception as e:
            print(f"⚠ 获取元素失败: {e}")
    
    def comprehensive_test(self):
        """综合测试"""
        print("=" * 60)
        print("微信自动化综合测试")
        print("=" * 60)
        
        try:
            # 1. 启动微信
            if not self.start_wechat():
                print("✗ 微信启动失败")
                return
            
            # 2. 初始截图
            self.take_screenshot("01_initial")
            
            # 3. 导航测试
            self.navigate_tabs()
            
            # 4. 获取元素信息
            self.get_all_elements()
            
            # 5. 最终截图
            self.take_screenshot("99_final")
            
            print("\n" + "=" * 60)
            print("✓ 测试完成！")
            print("=" * 60)
            print("\n查看截图:")
            print("  ls -lh screenshots/")
            
        except KeyboardInterrupt:
            print("\n\n用户中断")
        except Exception as e:
            print(f"\n✗ 发生错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    controller = WeChatController()
    controller.comprehensive_test()


if __name__ == "__main__":
    main()
