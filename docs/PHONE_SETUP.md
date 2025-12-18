# Android 手机配置指南

本指南帮助您配置 Android 手机以支持微信自动化。

## 📱 硬件要求

### 支持的设备
- **Android 版本**: 7.0 (API 24) 及以上
- **推荐版本**: Android 9.0+ 
- **内存**: 至少 2GB RAM
- **存储**: 至少 8GB 可用空间

### 推荐设备
- 小米系列（MIUI 开发版支持较好）
- 华为/荣耀系列
- OPPO/vivo 系列
- 三星系列
- Google Pixel 系列

## 🔧 准备工作

### 1. 启用开发者选项

#### 方法一：通过设置启用
1. 打开 **设置**
2. 进入 **关于手机**
3. 连续点击 **版本号** 7次
4. 输入锁屏密码（如有）
5. 看到提示"您已处于开发者模式"

#### 方法二：不同品牌的位置
- **小米**: 设置 → 我的设备 → 全部参数 → MIUI 版本（点击7次）
- **华为**: 设置 → 关于手机 → 版本号（点击7次）
- **OPPO**: 设置 → 关于手机 → 版本号（点击7次）
- **vivo**: 设置 → 更多设置 → 关于手机 → 软件版本号（点击7次）
- **三星**: 设置 → 关于手机 → 软件信息 → 版本号（点击7次）

### 2. 启用 USB 调试

1. 返回 **设置** 主页
2. 进入 **开发者选项**（通常在"系统"或"更多设置"中）
3. 打开 **开发者选项** 总开关
4. 启用以下选项：
   - ✅ **USB 调试**
   - ✅ **USB 安装**（部分手机有此选项）
   - ✅ **USB 调试（安全设置）**（小米等）
   - ✅ **仅充电模式下允许 ADB 调试**（部分手机）

### 3. 禁用 USB 验证（推荐）

部分手机需要额外设置：
- ✅ **禁用权限监控**
- ✅ **不监控 ADB 安装的应用**
- ✅ **允许通过 USB 验证应用**

### 4. 保持屏幕常亮（开发期间）

在开发者选项中：
- ✅ **不锁定屏幕**
- ✅ **充电时保持屏幕唤醒**

## 🔌 连接手机到 Mac

### 方法一：USB 数据线连接（推荐）

#### 1. 连接设备

```bash
# 使用原装或质量好的数据线连接手机到 Mac
# 确保数据线支持数据传输（不是仅充电线）
```

#### 2. 手机授权

连接后手机会弹出授权提示：
```
允许 USB 调试吗？
计算机的 RSA 密钥指纹为：
xx:xx:xx:xx:xx...

[取消] [始终允许此计算机] [确定]
```

**重要**: 勾选 **"始终允许此计算机"**，然后点击 **"确定"**

#### 3. 验证连接

```bash
# 检查设备是否连接
adb devices

# 正常输出：
List of devices attached
XXXXXXXXXX      device

# 如果显示 unauthorized，需要重新授权
# 如果显示 offline，尝试重新插拔数据线
```

### 方法二：无线 ADB 连接

#### 前提条件
- 手机和 Mac 在同一 WiFi 网络
- 已通过 USB 连接过一次

#### 1. 通过 USB 启动无线调试

```bash
# 连接 USB 数据线
adb devices

# 启用 TCP/IP 模式（端口 5555）
adb tcpip 5555

# 断开 USB 数据线
```

#### 2. 获取手机 IP 地址

在手机上：
- **设置** → **WLAN** → 点击已连接的网络
- 查看 **IP 地址**（例如：192.168.1.100）

#### 3. 无线连接

```bash
# 连接到手机（替换为实际 IP）
adb connect 192.168.1.100:5555

# 验证连接
adb devices

# 输出：
192.168.1.100:5555      device
```

#### 4. 断开无线连接

```bash
# 断开指定设备
adb disconnect 192.168.1.100:5555

# 或断开所有设备
adb disconnect
```

## 📦 安装必要的应用

### 1. 安装 ATX Agent

ATX Agent 是 uiautomator2 的核心服务。

#### 自动安装（推荐）

```bash
# 运行手机配置脚本
./scripts/setup-phone.sh
```

脚本会自动：
- 检测手机连接
- 安装 ATX Agent
- 安装 uiautomator2 APK
- 启动服务
- 验证安装

#### 手动安装

```python
# 激活虚拟环境
source venv/bin/activate

# 运行 Python 脚本
python3 << 'EOF'
import uiautomator2 as u2

# 连接设备（自动检测第一个设备）
d = u2.connect()

# 或指定设备序列号
# d = u2.connect("XXXXXXXXXX")

print(f"设备信息: {d.info}")
print("ATX Agent 安装成功！")
EOF
```

### 2. 安装微信

如果手机未安装微信：

#### 方法一：应用商店安装
1. 打开手机应用商店
2. 搜索"微信"
3. 下载安装官方版本

#### 方法二：通过 ADB 安装

```bash
# 下载微信 APK（从官网或其他可信来源）
# 例如：weixin_xxx.apk

# 安装到手机
adb install weixin_xxx.apk

# 或覆盖安装（保留数据）
adb install -r weixin_xxx.apk
```

### 3. 获取微信包名

```bash
# 查看已安装应用
adb shell pm list packages | grep tencent

# 输出（微信包名）：
package:com.tencent.mm
```

微信包名：`com.tencent.mm`

## ⚙️ 配置项目

### 1. 更新 .env 配置

```bash
vim .env
```

添加或修改以下配置：

```bash
# ==================== 手机控制配置 ====================
# 设备序列号（留空则自动检测第一个设备）
ANDROID_DEVICE_SERIAL=

# 微信包名
WECHAT_PACKAGE_NAME=com.tencent.mm

# UI 自动化配置
UI_AUTOMATION_TIMEOUT=10  # 元素查找超时（秒）
UI_AUTOMATION_RETRY=3     # 失败重试次数
UI_WAIT_TIMEOUT=20        # 等待超时（秒）

# 无线 ADB 配置（可选）
ADB_WIFI_ENABLED=false
ADB_WIFI_IP=192.168.1.100
ADB_WIFI_PORT=5555
```

### 2. 测试连接

运行手机配置脚本：

```bash
./scripts/setup-phone.sh
```

或手动测试：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试脚本
python3 << 'EOF'
import uiautomator2 as u2

# 连接设备
d = u2.connect()

# 获取设备信息
info = d.info
print(f"设备型号: {info['productName']}")
print(f"Android 版本: {info['version']}")
print(f"屏幕分辨率: {info['displayWidth']}x{info['displayHeight']}")

# 截图测试
d.screenshot("test_screenshot.png")
print("截图已保存: test_screenshot.png")

# 检查微信是否安装
wechat_installed = d.app_info("com.tencent.mm")
if wechat_installed:
    print(f"微信已安装: {wechat_installed['versionName']}")
else:
    print("警告: 微信未安装")

print("\n✓ 设备配置成功！")
EOF
```

## 🔍 故障排查

### 问题 1: adb: command not found

**原因**: ADB 未安装或未添加到 PATH

**解决方案**:

```bash
# macOS: 安装 Android Platform Tools
brew install android-platform-tools

# 验证安装
adb version
```

### 问题 2: unauthorized 设备

**原因**: USB 调试未授权

**解决方案**:
1. 断开 USB 连接
2. 在手机上：设置 → 开发者选项 → 撤销 USB 调试授权
3. 重新连接 USB
4. 勾选"始终允许"并确认授权

### 问题 3: device offline

**原因**: ADB 守护进程异常

**解决方案**:

```bash
# 重启 ADB 服务
adb kill-server
adb start-server

# 重新连接
adb devices
```

### 问题 4: 找不到设备

**原因**: 驱动问题或连接问题

**解决方案**:
1. 更换 USB 数据线（使用原装线）
2. 更换 USB 接口
3. 重启手机和电脑
4. 检查 USB 调试是否开启

### 问题 5: ATX Agent 安装失败

**原因**: 网络问题或权限问题

**解决方案**:

```bash
# 手动初始化
python3 -m uiautomator2 init

# 指定设备
python3 -m uiautomator2 init --serial XXXXXXXXXX

# 清理并重新安装
adb uninstall com.github.uiautomator
adb uninstall com.github.uiautomator.test
python3 -m uiautomator2 init
```

### 问题 6: 无线连接失败

**原因**: 网络不通或端口被占用

**解决方案**:

```bash
# 检查网络连通性
ping 192.168.1.100

# 检查端口是否开放
nc -zv 192.168.1.100 5555

# 重新启动 TCP/IP 模式
adb usb
adb tcpip 5555
adb connect 192.168.1.100:5555
```

### 问题 7: 权限被拒绝

**原因**: 应用权限未授予

**解决方案**:

在手机上手动授予权限：
- 设置 → 应用管理 → ATXAgent
- 开启所有权限（存储、辅助功能等）

## 🔒 安全建议

### 开发期间

1. **仅在可信网络使用无线 ADB**
2. **开发完成后关闭 USB 调试**
3. **定期清理调试授权**
4. **不要在公共场所使用无线 ADB**

### 生产环境

```bash
# 开发完成后，恢复 USB 模式
adb usb

# 关闭开发者选项
在手机设置中关闭"开发者选项"
```

## 📱 不同品牌的特殊设置

### 小米 (MIUI)

1. **关闭 MIUI 优化**
   - 开发者选项 → 关闭"MIUI 优化"
   - 重启手机

2. **允许后台弹出界面**
   - 设置 → 应用设置 → 应用管理 → ATXAgent
   - 开启"后台弹出界面"权限

3. **允许自启动**
   - 设置 → 应用设置 → 应用管理 → ATXAgent
   - 开启"自启动"

### 华为 / 荣耀 (EMUI)

1. **允许通过 USB 安装应用**
   - 开发者选项 → 监控 ADB 安装应用 → 关闭

2. **电池优化**
   - 设置 → 电池 → 应用启动管理 → ATXAgent
   - 设置为"手动管理"，全部允许

### OPPO / vivo (ColorOS / FuntouchOS)

1. **允许后台运行**
   - 设置 → 电池 → 后台高耗电 → ATXAgent
   - 允许后台运行

2. **允许自启动**
   - 设置 → 应用管理 → 权限 → 自启动 → ATXAgent
   - 允许自启动

## 🎯 验证清单

配置完成后，确认以下项目：

- [ ] 开发者选项已启用
- [ ] USB 调试已启用
- [ ] 设备已通过 `adb devices` 检测到
- [ ] ATX Agent 已安装并运行
- [ ] 微信已安装
- [ ] 项目 `.env` 已配置
- [ ] 测试脚本运行成功
- [ ] 截图功能正常

## 📚 相关文档

- [快速开始指南](QUICKSTART.md)
- [项目总结](PROJECT_SUMMARY.md)
- [端口配置](PORT_CONFIG.md)
- [MCP 集成规范](MCP_INTEGRATION_RULES.md)

## 🤝 获取帮助

如果遇到问题：
1. 查看 [故障排查](#故障排查) 部分
2. 检查手机品牌特殊设置
3. 查阅 uiautomator2 官方文档
4. 提交 GitHub Issue

---

配置完成后，您可以开始使用微信自动化功能！🎉
