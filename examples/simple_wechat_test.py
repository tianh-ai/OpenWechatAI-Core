#!/usr/bin/env python3
"""简化的微信测试 - 假设屏幕已手动解锁"""

import uiautomator2 as u2
import time
import os

print("连接设备...")
d = u2.connect()
print(f"✓ 已连接: {d.device_info['model']}")

# 创建截图目录
os.makedirs("screenshots", exist_ok=True)

print("\n启动微信...")
d.app_start("com.tencent.mm")
time.sleep(3)

# 检查当前应用
current = d.app_current()
print(f"当前应用: {current['package']}")

# 截图
print("\n截图...")
img = d.screenshot()
img.save("screenshots/wechat_unlocked.jpg")
print("✓ 保存: screenshots/wechat_unlocked.jpg")

# 获取界面元素
print("\n获取界面元素...")
xml = d.dump_hierarchy()
with open("screenshots/wechat_unlocked.xml", "w", encoding="utf-8") as f:
    f.write(xml)
print("✓ 保存: screenshots/wechat_unlocked.xml")

# 分析元素
import xml.etree.ElementTree as ET
root = ET.fromstring(xml)

clickable = []
texts = []
resource_ids = []

for elem in root.iter():
    if elem.get('clickable') == 'true':
        clickable.append({
            'class': elem.get('class'),
            'text': elem.get('text'),
            'resource-id': elem.get('resource-id'),
            'bounds': elem.get('bounds')
        })
    
    if elem.get('text'):
        texts.append(elem.get('text'))
    
    if elem.get('resource-id'):
        resource_ids.append(elem.get('resource-id'))

print(f"\n可点击元素: {len(clickable)}")
print(f"文本元素: {len(texts)}")
print(f"资源ID: {len(set(resource_ids))}")

# 打印前10个可点击元素
print("\n前10个可点击元素:")
for i, elem in enumerate(clickable[:10], 1):
    print(f"{i}. {elem['class']}")
    if elem['text']:
        print(f"   文本: {elem['text']}")
    if elem['resource-id']:
        print(f"   ID: {elem['resource-id']}")

# 打印所有文本
print("\n所有文本元素:")
for text in list(set(texts))[:20]:
    print(f"  - {text}")

print("\n完成！")
