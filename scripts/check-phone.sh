#!/bin/bash
# 快速手机连接检查

echo "================================================"
echo "Android 手机连接检查"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}1. 检查 ADB 状态...${NC}"
ADB_VERSION=$(adb version | head -n 1)
echo "  $ADB_VERSION"
echo ""

echo -e "${BLUE}2. 启动 ADB 服务...${NC}"
adb start-server
echo ""

echo -e "${BLUE}3. 扫描设备...${NC}"
echo ""
adb devices -l
echo ""

DEVICES=$(adb devices | grep -v "List" | grep "device$" | wc -l | xargs)

if [ "$DEVICES" = "0" ]; then
    echo -e "${YELLOW}⚠ 未检测到设备${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}请按照以下步骤连接手机：${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📱 第一步：启用开发者选项"
    echo "  1. 打开手机【设置】"
    echo "  2. 进入【关于手机】"
    echo "  3. 连续点击【版本号】7次"
    echo "  4. 看到提示"您已处于开发者模式""
    echo ""
    echo "🔧 第二步：启用 USB 调试"
    echo "  1. 返回【设置】主页"
    echo "  2. 进入【开发者选项】（在"系统"或"更多设置"中）"
    echo "  3. 打开【开发者选项】总开关"
    echo "  4. 启用【USB 调试】"
    echo ""
    echo "🔌 第三步：连接手机"
    echo "  1. 使用 USB 数据线连接手机到 Mac"
    echo "  2. 确保使用原装或质量好的数据线（支持数据传输）"
    echo "  3. 手机会弹出授权提示"
    echo "  4. 勾选【始终允许此计算机】"
    echo "  5. 点击【确定】"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "完成后重新运行此脚本："
    echo "  ./scripts/check-phone.sh"
    echo ""
    echo "或查看完整配置文档："
    echo "  cat docs/PHONE_SETUP.md"
    echo ""
else
    echo -e "${GREEN}✓ 检测到 $DEVICES 个设备${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "下一步：运行完整配置"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "运行手机配置向导："
    echo "  ./scripts/setup-phone.sh"
    echo ""
fi
