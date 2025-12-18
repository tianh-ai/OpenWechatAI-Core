#!/usr/bin/env python3
"""
微信界面分析工具
分析微信界面元素，找到正确的定位方式
"""

import uiautomator2 as u2
import xml.etree.ElementTree as ET
from datetime import datetime


def analyze_wechat_ui():
    """分析微信界面"""
    print("=" * 60)
    print("微信界面分析工具")
    print("=" * 60)
    
    # 连接设备
    print("\n连接设备...")
    d = u2.connect()
    print(f"✓ 已连接: {d.device_info['model']}")
    
    # 启动微信
    print("\n启动微信...")
    d.screen_on()
    d.app_start("com.tencent.mm")
    import time
    time.sleep(3)
    
    # 获取界面层级
    print("\n分析界面元素...")
    xml_content = d.dump_hierarchy()
    
    # 保存 XML
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_file = f"screenshots/wechat_ui_{timestamp}.xml"
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    print(f"✓ XML 已保存: {xml_file}")
    
    # 解析 XML
    root = ET.fromstring(xml_content)
    
    # 查找可点击元素
    print("\n" + "=" * 60)
    print("可点击元素分析")
    print("=" * 60)
    
    clickable_elements = []
    for elem in root.iter():
        if elem.attrib.get('clickable') == 'true':
            info = {
                'class': elem.attrib.get('class', ''),
                'text': elem.attrib.get('text', ''),
                'content-desc': elem.attrib.get('content-desc', ''),
                'resource-id': elem.attrib.get('resource-id', ''),
                'bounds': elem.attrib.get('bounds', '')
            }
            clickable_elements.append(info)
    
    print(f"\n找到 {len(clickable_elements)} 个可点击元素")
    print("\n底部导航栏元素（根据位置判断）:")
    
    # 获取屏幕高度
    screen_height = d.window_size()[1]
    bottom_threshold = screen_height * 0.8  # 底部 20% 区域
    
    bottom_elements = []
    for elem in clickable_elements:
        bounds = elem['bounds']
        if bounds:
            # 解析 bounds: [x1,y1][x2,y2]
            import re
            match = re.findall(r'\[(\d+),(\d+)\]', bounds)
            if match and len(match) == 2:
                y1 = int(match[0][1])
                y2 = int(match[1][1])
                if y1 > bottom_threshold:
                    bottom_elements.append(elem)
    
    print(f"\n找到 {len(bottom_elements)} 个底部元素:")
    for i, elem in enumerate(bottom_elements, 1):
        print(f"\n元素 {i}:")
        if elem['text']:
            print(f"  文本: {elem['text']}")
        if elem['content-desc']:
            print(f"  描述: {elem['content-desc']}")
        if elem['resource-id']:
            print(f"  ID: {elem['resource-id']}")
        print(f"  位置: {elem['bounds']}")
    
    # 查找所有文本元素
    print("\n" + "=" * 60)
    print("所有文本元素")
    print("=" * 60)
    
    text_elements = set()
    for elem in root.iter():
        text = elem.attrib.get('text', '').strip()
        if text:
            text_elements.add(text)
    
    print(f"\n找到 {len(text_elements)} 个不同的文本:")
    for text in sorted(text_elements):
        print(f"  - {text}")
    
    # 查找所有描述元素
    print("\n" + "=" * 60)
    print("所有描述元素 (content-desc)")
    print("=" * 60)
    
    desc_elements = set()
    for elem in root.iter():
        desc = elem.attrib.get('content-desc', '').strip()
        if desc:
            desc_elements.add(desc)
    
    print(f"\n找到 {len(desc_elements)} 个不同的描述:")
    for desc in sorted(desc_elements):
        print(f"  - {desc}")
    
    # 查找所有资源ID
    print("\n" + "=" * 60)
    print("所有资源 ID")
    print("=" * 60)
    
    resource_ids = set()
    for elem in root.iter():
        rid = elem.attrib.get('resource-id', '').strip()
        if rid and 'com.tencent.mm' in rid:
            resource_ids.add(rid)
    
    print(f"\n找到 {len(resource_ids)} 个不同的资源 ID:")
    for rid in sorted(resource_ids):
        print(f"  - {rid}")
    
    # 截图当前状态
    print("\n截图当前界面...")
    screenshot_file = f"screenshots/wechat_analyzed_{timestamp}.jpg"
    d.screenshot().save(screenshot_file)
    print(f"✓ 截图已保存: {screenshot_file}")
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)
    print(f"\n文件:")
    print(f"  - {xml_file}")
    print(f"  - {screenshot_file}")
    print("\n提示: 使用找到的元素属性来定位界面元素")


if __name__ == "__main__":
    analyze_wechat_ui()
