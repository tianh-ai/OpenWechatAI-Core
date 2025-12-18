# 微信自动化实现方案

## 问题分析

### Android 15 限制
- **SDK 35** (Android 15) 对第三方应用UI层级访问有严格限制
- 微信界面元素被标记为 `visible-to-user="false"`
- 无法通过传统的 `text`、`resource-id` 等属性定位元素

### 解决方案
采用**混合自动化策略**：
1. **坐标点击** - 用于导航和基本操作
2. **OCR识别** - 用于读取消息内容
3. **图像对比** - 用于状态检测

## 实现架构

### 1. 坐标映射系统
```python
# 基于屏幕比例的坐标定义
coordinates = {
    'tabs': {
        'chat': (0.125, 0.95),      # 微信tab
        'contacts': (0.375, 0.95),   # 通讯录tab
        'discover': (0.625, 0.95),   # 发现tab
        'me': (0.875, 0.95),         # 我tab
    },
    'search': (0.5, 0.08),           # 搜索框
    'first_chat': (0.5, 0.2),        # 第一个聊天
    'input': (0.5, 0.9),             # 输入框
    'send': (0.95, 0.9),             # 发送按钮
}
```

### 2. OCR文字识别
使用 PaddleOCR 或 Tesseract 识别屏幕文字：
- 消息内容
- 联系人姓名
- 时间戳

### 3. 图像对比检测
- 检测界面变化
- 判断消息是否发送成功
- 识别新消息到达

## 核心功能实现

### 已实现
✅ 坐标导航系统
✅ Tab切换（微信、通讯录、发现、我）
✅ 截图功能
✅ 基本点击操作

### 待实现
- [ ] OCR消息识别
- [ ] 新消息检测
- [ ] 自动回复
- [ ] 联系人管理
- [ ] 群聊管理

## 技术栈

### 核心依赖
- `uiautomator2==3.5.0` - Android自动化
- `Pillow` - 图像处理
- `paddleocr` 或 `pytesseract` - OCR识别
- `opencv-python` - 图像对比

### 可选优化
- `numpy` - 数值计算
- `scikit-image` - 高级图像处理
- `imagehash` - 图像哈希对比

## 使用示例

### 基本导航
```python
from wechat_coordinate_control import WeChatCoordinateController

controller = WeChatCoordinateController()
controller.start_wechat()
controller.go_to_tab('chat')
controller.screenshot('current_state')
```

### 发送消息（开发中）
```python
controller.click_first_chat()
controller.send_message("你好，这是自动消息")
controller.back()
```

## 已知限制

1. **坐标固定性**
   - 不同设备分辨率需要调整
   - 微信界面更新可能导致坐标失效
   - 解决：使用相对坐标和图像识别辅助

2. **无法读取文字**
   - UI层级不可访问
   - 解决：集成OCR识别

3. **新消息检测**
   - 无法通过属性监听
   - 解决：定时截图+图像对比

## 下一步计划

1. **集成OCR** - 实现消息内容读取
2. **消息监控** - 检测新消息到达
3. **智能回复** - 基于规则或AI的自动回复
4. **联系人管理** - 通讯录操作
5. **群聊支持** - 群消息处理

## 参考文档
- [uiautomator2官方文档](https://github.com/openatx/uiautomator2)
- [PaddleOCR文档](https://github.com/PaddlePaddle/PaddleOCR)
- [Android 15行为变更](https://developer.android.com/about/versions/15/behavior-changes-15)
