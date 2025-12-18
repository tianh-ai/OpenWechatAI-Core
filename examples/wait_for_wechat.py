#!/usr/bin/env python3
"""等待微信完全启动并获取界面元素"""

import uiautomator2 as u2
import time
import os
import xml.etree.ElementTree as ET

print("连接设备...")
d = u2.connect()
print(f"✓ 已连接: {d.device_info['model']}")

os.makedirs("screenshots", exist_ok=True)

print("\n启动微信...")
d.app_start("com.tencent.mm")

# 等待应用完全启动
print("等待微信加载...")
for i in range(10):
    time.sleep(1)
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    
    # 查找微信的可见节点
    wechat_nodes = []
    for node in root.iter():
        if node.get('package') == 'com.tencent.mm':
            visible = node.get('visible-to-user') == 'true'
            bounds = node.get('bounds', '[0,0][0,0]')
            wechat_nodes.append({
                'visible': visible,
                'bounds': bounds,
                'class': node.get('class'),
                'text': node.get('text')
            })
    
    visible_count = sum(1 for n in wechat_nodes if n['visible'])
    print(f"  {i+1}s: 找到 {len(wechat_nodes)} 个微信节点，其中 {visible_count} 个可见")
    
    if visible_count > 5:  # 至少有5个可见元素说明界面已加载
        print(f"✓ 微信界面已加载！")
        break
else:
    print("⚠ 微信可能没有完全加载")

# 最终截图和分析
print("\n截图...")
img = d.screenshot()
img.save("screenshots/wechat_ready.jpg")
print("✓ 保存: screenshots/wechat_ready.jpg")

print("\n获取界面元素...")
xml = d.dump_hierarchy()
with open("screenshots/wechat_ready.xml", "w", encoding="utf-8") as f:
    f.write(xml)

root = ET.fromstring(xml)

# 详细分析
clickable = []
texts = []
resource_ids = []
wechat_elements = []

for elem in root.iter():
    package = elem.get('package')
    
    # 只看微信的元素
    if package == 'com.tencent.mm' and elem.get('visible-to-user') == 'true':
        wechat_elements.append(elem)
        
        if elem.get('clickable') == 'true':
            clickable.append({
                'class': elem.get('class'),
                'text': elem.get('text'),
                'resource-id': elem.get('resource-id'),
                'content-desc': elem.get('content-desc'),
                'bounds': elem.get('bounds')
            })
        
        if elem.get('text'):
            texts.append(elem.get('text'))
        
        if elem.get('resource-id'):
            rid = elem.get('resource-id')
            if rid:
                resource_ids.append(rid)

print(f"\n微信可见元素: {len(wechat_elements)}")
print(f"可点击元素: {len(clickable)}")
print(f"文本元素: {len(texts)}")
print(f"资源ID: {len(set(resource_ids))}")

if clickable:
    print("\n可点击元素 (前20个):")
    for i, elem in enumerate(clickable[:20], 1):
        print(f"\n{i}. {elem['class']}")
        if elem['text']:
            print(f"   文本: {elem['text']}")
        if elem['content-desc']:
            print(f"   描述: {elem['content-desc']}")
        if elem['resource-id']:
            print(f"   ID: {elem['resource-id']}")
        print(f"   坐标: {elem['bounds']}")

if texts:
    print("\n文本元素 (前30个):")
    unique_texts = list(set(texts))[:30]
    for text in unique_texts:
        print(f"  - {text}")

if resource_ids:
    print("\n资源ID (前30个):")
    unique_ids = list(set(resource_ids))[:30]
    for rid in unique_ids:
        print(f"  - {rid}")

print("\n完成！")
