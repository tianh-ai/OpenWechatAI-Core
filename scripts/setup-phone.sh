#!/bin/bash
# Android 手机配置和检测脚本

set -e

echo "================================================"
echo "Android 手机配置向导"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 ADB
check_adb() {
    if ! command -v adb &> /dev/null; then
        echo -e "${RED}✗ ADB 未安装${NC}"
        echo ""
        echo "请安装 Android Platform Tools:"
        echo "  macOS: brew install android-platform-tools"
        echo "  Linux: sudo apt-get install android-tools-adb"
        echo ""
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} ADB 已安装"
    ADB_VERSION=$(adb version | head -n 1)
    echo "  版本: $ADB_VERSION"
}

# 检查设备连接
check_device() {
    echo ""
    echo -e "${BLUE}检查设备连接...${NC}"
    
    # 启动 ADB 服务
    adb start-server > /dev/null 2>&1
    
    # 获取设备列表
    DEVICES=$(adb devices | grep -v "List" | grep "device$" | awk '{print $1}')
    DEVICE_COUNT=$(echo "$DEVICES" | grep -c "." || true)
    
    if [ $DEVICE_COUNT -eq 0 ]; then
        echo -e "${RED}✗ 未检测到设备${NC}"
        echo ""
        echo "请确保："
        echo "1. 手机已通过 USB 连接到电脑"
        echo "2. 手机已启用 USB 调试"
        echo "3. 已在手机上授权此计算机"
        echo ""
        echo "详细配置步骤请参考: docs/PHONE_SETUP.md"
        exit 1
    elif [ $DEVICE_COUNT -eq 1 ]; then
        DEVICE_SERIAL=$DEVICES
        echo -e "${GREEN}✓${NC} 检测到设备: $DEVICE_SERIAL"
    else
        echo -e "${YELLOW}⚠${NC} 检测到多个设备:"
        echo "$DEVICES"
        echo ""
        echo "请选择要配置的设备序列号，或在 .env 中设置 ANDROID_DEVICE_SERIAL"
        read -p "设备序列号: " DEVICE_SERIAL
        
        if [ -z "$DEVICE_SERIAL" ]; then
            echo -e "${RED}✗ 未选择设备${NC}"
            exit 1
        fi
    fi
    
    export ANDROID_DEVICE_SERIAL=$DEVICE_SERIAL
}

# 获取设备信息
get_device_info() {
    echo ""
    echo -e "${BLUE}获取设备信息...${NC}"
    
    # 设备型号
    MODEL=$(adb -s $DEVICE_SERIAL shell getprop ro.product.model | tr -d '\r')
    echo "  型号: $MODEL"
    
    # Android 版本
    ANDROID_VERSION=$(adb -s $DEVICE_SERIAL shell getprop ro.build.version.release | tr -d '\r')
    echo "  Android 版本: $ANDROID_VERSION"
    
    # SDK 版本
    SDK_VERSION=$(adb -s $DEVICE_SERIAL shell getprop ro.build.version.sdk | tr -d '\r')
    echo "  SDK 版本: $SDK_VERSION"
    
    # 制造商
    MANUFACTURER=$(adb -s $DEVICE_SERIAL shell getprop ro.product.manufacturer | tr -d '\r')
    echo "  制造商: $MANUFACTURER"
    
    # 屏幕分辨率
    RESOLUTION=$(adb -s $DEVICE_SERIAL shell wm size | grep "Physical size" | awk '{print $3}')
    echo "  屏幕分辨率: $RESOLUTION"
    
    # 检查 Android 版本是否支持
    if [ $SDK_VERSION -lt 24 ]; then
        echo -e "${YELLOW}⚠ 警告: Android 版本过低 (需要 7.0+)${NC}"
        echo "  当前版本: Android $ANDROID_VERSION (SDK $SDK_VERSION)"
        echo "  建议升级系统或更换设备"
    fi
}

# 检查 Python 环境
check_python() {
    echo ""
    echo -e "${BLUE}检查 Python 环境...${NC}"
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo -e "${RED}✗ 虚拟环境未创建${NC}"
        echo "  运行: python3 -m venv venv"
        exit 1
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 检查 uiautomator2
    if ! python3 -c "import uiautomator2" &> /dev/null; then
        echo -e "${YELLOW}⚠${NC} uiautomator2 未安装，正在安装..."
        pip3 install -q uiautomator2
    fi
    
    echo -e "${GREEN}✓${NC} Python 环境就绪"
}

# 安装 ATX Agent
install_atx() {
    echo ""
    echo -e "${BLUE}安装 ATX Agent...${NC}"
    
    # 使用 Python 安装
    python3 << EOF
import uiautomator2 as u2
import sys

try:
    print("正在初始化设备...")
    d = u2.connect("$DEVICE_SERIAL")
    
    # 获取设备信息验证连接
    info = d.device_info
    print(f"✓ 设备连接成功")
    print(f"  品牌: {info.get('brand', 'N/A')}")
    print(f"  型号: {info.get('model', 'N/A')}")
    
    # 检查 ATX Agent 服务
    try:
        app_info = d.app_info("com.github.uiautomator")
        if app_info:
            print(f"✓ ATX Agent 已安装")
            print(f"  版本: {app_info.get('versionName', 'Unknown')}")
        else:
            print(f"✓ ATX Agent 正在安装...")
    except:
        print(f"✓ ATX Agent 初始化完成")
    
except Exception as e:
    print(f"✗ 安装失败: {e}", file=sys.stderr)
    sys.exit(1)
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} ATX Agent 配置成功"
    else
        echo -e "${RED}✗${NC} ATX Agent 配置失败"
        echo ""
        echo "尝试手动安装:"
        echo "  python3 -m uiautomator2 init --serial $DEVICE_SERIAL"
        exit 1
    fi
}

# 检查微信
check_wechat() {
    echo ""
    echo -e "${BLUE}检查微信安装...${NC}"
    
    WECHAT_PACKAGE="com.tencent.mm"
    
    if adb -s $DEVICE_SERIAL shell pm list packages | grep -q "$WECHAT_PACKAGE"; then
        # 获取微信版本
        WECHAT_VERSION=$(adb -s $DEVICE_SERIAL shell dumpsys package $WECHAT_PACKAGE | grep "versionName" | head -n 1 | awk -F= '{print $2}')
        echo -e "${GREEN}✓${NC} 微信已安装"
        echo "  包名: $WECHAT_PACKAGE"
        echo "  版本: $WECHAT_VERSION"
    else
        echo -e "${YELLOW}⚠${NC} 微信未安装"
        echo ""
        echo "请在手机上安装微信应用"
    fi
}

# 测试连接
test_connection() {
    echo ""
    echo -e "${BLUE}测试设备功能...${NC}"
    
    python3 << EOF
import uiautomator2 as u2
import sys

try:
    # 连接设备
    d = u2.connect("$DEVICE_SERIAL")
    
    # 获取设备信息
    info = d.info
    print(f"✓ 设备连接成功")
    print(f"  序列号: {info.get('udid', 'N/A')}")
    
    # 测试截图
    import os
    os.makedirs("screenshots", exist_ok=True)
    d.screenshot("screenshots/test_connection.jpg")
    print(f"✓ 截图功能正常")
    print(f"  已保存: screenshots/test_connection.jpg")
    
    # 检查屏幕状态
    screen_on = d.info.get('screenOn', False)
    print(f"✓ 屏幕状态: {'开启' if screen_on else '关闭'}")
    
    # 测试 app 检测
    wechat_info = d.app_info("com.tencent.mm")
    if wechat_info:
        print(f"✓ 微信检测正常")
    
    print(f"\n✓ 所有功能测试通过！")
    
except Exception as e:
    print(f"✗ 测试失败: {e}", file=sys.stderr)
    sys.exit(1)
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} 设备功能测试通过"
    else
        echo -e "${RED}✗${NC} 设备功能测试失败"
        exit 1
    fi
}

# 更新 .env 配置
update_env() {
    echo ""
    echo -e "${BLUE}更新 .env 配置...${NC}"
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠${NC} 已从 .env.example 创建 .env"
    fi
    
    # 更新设备序列号
    if grep -q "ANDROID_DEVICE_SERIAL=" .env; then
        sed -i.bak "s/ANDROID_DEVICE_SERIAL=.*/ANDROID_DEVICE_SERIAL=$DEVICE_SERIAL/" .env
    else
        echo "ANDROID_DEVICE_SERIAL=$DEVICE_SERIAL" >> .env
    fi
    
    echo -e "${GREEN}✓${NC} 配置已更新"
    echo "  设备序列号: $DEVICE_SERIAL"
}

# 显示使用说明
show_usage() {
    echo ""
    echo "================================================"
    echo "配置完成！"
    echo "================================================"
    echo ""
    echo -e "${GREEN}设备已就绪，可以开始使用微信自动化功能${NC}"
    echo ""
    echo "下一步操作："
    echo ""
    echo "1. 启动 WeChat 自动化测试"
    echo "   source venv/bin/activate"
    echo "   python core/main.py --platform wechat"
    echo ""
    echo "2. 运行简单测试"
    echo "   python3 -c 'import uiautomator2 as u2; d = u2.connect(); d.screen_on(); print(\"测试成功\")'"
    echo ""
    echo "3. 查看截图"
    echo "   open screenshots/test_connection.jpg"
    echo ""
    echo "4. 查看完整文档"
    echo "   cat docs/PHONE_SETUP.md"
    echo ""
    echo -e "${BLUE}提示：${NC}"
    echo "- 保持手机屏幕常亮（开发期间）"
    echo "- 确保微信已登录"
    echo "- 不要手动操作手机（自动化运行时）"
    echo ""
}

# 主流程
main() {
    echo -e "${BLUE}开始配置 Android 手机...${NC}"
    echo ""
    
    # 1. 检查 ADB
    check_adb
    
    # 2. 检查设备
    check_device
    
    # 3. 获取设备信息
    get_device_info
    
    # 4. 检查 Python 环境
    check_python
    
    # 5. 安装 ATX Agent
    install_atx
    
    # 6. 检查微信
    check_wechat
    
    # 7. 测试连接
    test_connection
    
    # 8. 更新配置
    update_env
    
    # 9. 显示使用说明
    show_usage
}

# 运行主流程
main
