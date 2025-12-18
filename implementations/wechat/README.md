# 微信UI自动化配置指南

## 获取UI元素定位信息

### 1. 安装weditor
```bash
pip install weditor
```

### 2. 启动weditor
```bash
python -m weditor
```

### 3. 获取元素信息步骤

1. **连接设备**
   - 打开weditor界面（http://localhost:17310）
   - 输入设备序列号或留空使用默认设备
   - 点击Connect

2. **获取微信UI元素**
   - 在手机上打开微信
   - 在weditor中点击"Dump Hierarchy"刷新页面
   - 点击想要定位的元素（如输入框、发送按钮）
   - 记录resourceId、text、className等属性

3. **常用元素定位**

   需要获取的关键元素：
   
   - **聊天列表**: 主页面的聊天列表容器
   - **搜索按钮**: 顶部搜索图标
   - **搜索输入框**: 搜索页面的输入框
   - **消息输入框**: 聊天窗口的输入框
   - **发送按钮**: 消息发送按钮
   - **联系人名称**: 聊天列表中的联系人名称
   - **最新消息**: 聊天列表中的消息预览
   - **未读红点**: 未读消息标记

### 4. 更新配置

将获取的resourceId更新到 `wechat_platform.py` 的 `SELECTORS` 字典中：

```python
SELECTORS = {
    "chat_list": {"resourceId": "com.tencent.mm:id/xxx"},  # 替换为实际值
    "search_btn": {"resourceId": "com.tencent.mm:id/xxx"},
    # ... 其他元素
}
```

## 注意事项

1. **微信版本**
   - UI元素ID可能因微信版本不同而变化
   - 建议固定使用同一版本微信
   - 当前配置基于微信 8.0.x

2. **设备兼容性**
   - 不同Android版本可能有差异
   - 建议在实际设备上测试

3. **稳定性优化**
   - 增加适当的等待时间（time.sleep）
   - 使用重试机制（tenacity）
   - 添加异常处理

4. **权限要求**
   - USB调试已启用
   - 允许模拟点击权限
   - 微信已登录

## 测试脚本

```python
import uiautomator2 as u2

# 连接设备
d = u2.connect()

# 启动微信
d.app_start("com.tencent.mm")

# 等待并截图
import time
time.sleep(3)
d.screenshot("wechat_screenshot.png")

# 打印当前页面所有元素
print(d.dump_hierarchy())
```

## 常见问题

### Q: 找不到元素
A: 使用weditor实时查看UI树，确认元素是否存在，resourceId是否正确

### Q: 点击无效
A: 检查元素是否可点击（clickable=true），尝试使用坐标点击

### Q: 微信闪退
A: 检查自动化权限，某些操作可能触发安全检测

### Q: 消息发送失败
A: 确认已在聊天窗口，输入框已正确定位，网络连接正常
