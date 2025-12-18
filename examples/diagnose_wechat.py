#!/usr/bin/env python3
"""诊断微信界面访问问题"""

import uiautomator2 as u2
import time

d = u2.connect()

print("=" * 60)
print("微信界面诊断")
print("=" * 60)

# 1. 检查当前应用
current = d.app_current()
print(f"\n1. 当前应用:")
print(f"   包名: {current['package']}")
print(f"   Activity: {current['activity']}")
print(f"   PID: {current['pid']}")

# 2. 检查屏幕状态
info = d.info
print(f"\n2. 屏幕状态:")
print(f"   屏幕开启: {info['screenOn']}")
print(f"   分辨率: {info['displayWidth']}x{info['displayHeight']}")
print(f"   SDK版本: {info['sdkInt']}")

# 3. 检查窗口层级
print(f"\n3. 窗口层级分析:")
xml = d.dump_hierarchy()
with open("screenshots/diagnostic.xml", "w", encoding="utf-8") as f:
    f.write(xml)

import xml.etree.ElementTree as ET
root = ET.fromstring(xml)

packages = {}
for elem in root.iter():
    pkg = elem.get('package')
    if pkg:
        if pkg not in packages:
            packages[pkg] = {'total': 0, 'visible': 0}
        packages[pkg]['total'] += 1
        if elem.get('visible-to-user') == 'true':
            packages[pkg]['visible'] += 1

print("\n   所有应用的界面元素:")
for pkg, counts in sorted(packages.items(), key=lambda x: x[1]['visible'], reverse=True):
    print(f"   {pkg}:")
    print(f"     总节点: {counts['total']}, 可见: {counts['visible']}")

# 4. 检查微信的具体节点
print(f"\n4. 微信节点详情:")
wechat_nodes = [elem for elem in root.iter() if elem.get('package') == 'com.tencent.mm']
if wechat_nodes:
    for i, node in enumerate(wechat_nodes[:5], 1):
        print(f"\n   节点 {i}:")
        print(f"     class: {node.get('class')}")
        print(f"     visible: {node.get('visible-to-user')}")
        print(f"     enabled: {node.get('enabled')}")
        print(f"     bounds: {node.get('bounds')}")
        print(f"     text: {node.get('text')}")
        print(f"     resource-id: {node.get('resource-id')}")
else:
    print("   ⚠ 没有找到微信节点")

# 5. 检查是否有对话框或遮挡
print(f"\n5. 可能的遮挡层:")
dialog_keywords = ['dialog', 'popup', 'alert', 'permission', 'overlay']
for elem in root.iter():
    cls = (elem.get('class') or '').lower()
    rid = (elem.get('resource-id') or '').lower()
    if any(kw in cls or kw in rid for kw in dialog_keywords):
        if elem.get('visible-to-user') == 'true':
            print(f"   发现: {elem.get('class')} - {elem.get('resource-id')}")

# 6. 尝试点击屏幕唤醒界面
print(f"\n6. 尝试唤醒界面...")
d.click(540, 1200)  # 点击屏幕中央
time.sleep(2)

# 再次检查
xml2 = d.dump_hierarchy()
root2 = ET.fromstring(xml2)
visible_count = sum(1 for elem in root2.iter() 
                   if elem.get('package') == 'com.tencent.mm' 
                   and elem.get('visible-to-user') == 'true')
print(f"   点击后微信可见元素: {visible_count}")

print("\n" + "=" * 60)
print("诊断完成！请查看上述信息并告诉我屏幕上显示的内容")
print("=" * 60)
