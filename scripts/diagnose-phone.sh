#!/bin/bash
# 手机连接诊断工具

echo "================================================"
echo "Android 手机连接诊断工具"
echo "================================================"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}正在诊断连接问题...${NC}"
echo ""

# 1. 检查 USB 设备
echo -e "${BLUE}1. 检查 USB 设备列表${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
system_profiler SPUSBDataType | grep -A 10 "Android\|Phone\|Mobile"
echo ""

# 2. 重启 ADB
echo -e "${BLUE}2. 重启 ADB 服务${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
adb kill-server
sleep 1
adb start-server
echo ""

# 3. 检查 ADB 设备
echo -e "${BLUE}3. 扫描 ADB 设备${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
adb devices -l
echo ""

# 4. 检查未授权设备
UNAUTHORIZED=$(adb devices | grep "unauthorized" | wc -l | xargs)
OFFLINE=$(adb devices | grep "offline" | wc -l | xargs)
DEVICE=$(adb devices | grep -v "List" | grep "device$" | wc -l | xargs)

echo -e "${BLUE}4. 连接状态分析${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$DEVICE" != "0" ]; then
    echo -e "${GREEN}✓ 已连接设备: $DEVICE 个${NC}"
    echo ""
    echo "设备已就绪！运行配置脚本："
    echo "  ./scripts/setup-phone.sh"
    exit 0
fi

if [ "$UNAUTHORIZED" != "0" ]; then
    echo -e "${YELLOW}⚠ 检测到未授权设备: $UNAUTHORIZED 个${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}解决方案：授权设备${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📱 在手机上操作："
    echo "  1. 查看手机屏幕是否有弹窗"
    echo "     【允许 USB 调试吗？】"
    echo "  2. ✅ 勾选【始终允许此计算机】"
    echo "  3. 点击【确定】或【允许】"
    echo ""
    echo "如果没有弹窗："
    echo "  1. 断开 USB 连接"
    echo "  2. 设置 → 开发者选项 → 撤销 USB 调试授权"
    echo "  3. 重新连接 USB"
    echo "  4. 在弹窗上授权"
    echo ""
    exit 1
fi

if [ "$OFFLINE" != "0" ]; then
    echo -e "${YELLOW}⚠ 设备离线: $OFFLINE 个${NC}"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${YELLOW}解决方案：重新连接${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. 断开 USB 数据线"
    echo "2. 在手机上重启 USB 调试："
    echo "   设置 → 开发者选项 → USB 调试（关闭再开启）"
    echo "3. 重新插入 USB 数据线"
    echo "4. 运行诊断："
    echo "   ./scripts/diagnose-phone.sh"
    echo ""
    exit 1
fi

# 5. 未检测到任何设备
echo -e "${RED}✗ 未检测到任何设备${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${YELLOW}可能的原因及解决方案${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${CYAN}原因 1: USB 调试未启用${NC}"
echo "解决："
echo "  1. 手机设置 → 关于手机"
echo "  2. 连续点击【版本号】7次（启用开发者选项）"
echo "  3. 返回设置 → 开发者选项"
echo "  4. 开启【开发者选项】总开关"
echo "  5. 开启【USB 调试】"
echo ""

echo -e "${CYAN}原因 2: USB 数据线问题${NC}"
echo "解决："
echo "  • 使用手机原装数据线"
echo "  • 确保数据线支持数据传输（不是仅充电线）"
echo "  • 尝试更换 USB 接口"
echo "  • 尝试更换数据线"
echo ""

echo -e "${CYAN}原因 3: USB 连接模式错误${NC}"
echo "解决："
echo "  1. 连接 USB 后，手机会显示 USB 用途"
echo "  2. 选择【文件传输 (MTP)】或【传输文件】"
echo "  3. 不要选择【仅充电】"
echo ""

echo -e "${CYAN}原因 4: Mac 未识别设备${NC}"
echo "解决："
echo "  1. 打开【系统信息】(按住 Option 点击左上角 Apple 图标)"
echo "  2. 查看 USB 设备列表"
echo "  3. 确认是否有 Android 设备或手机品牌名称"
echo "  4. 如果没有，尝试更换 USB 接口或数据线"
echo ""

echo -e "${CYAN}原因 5: 特定品牌需要额外设置${NC}"
echo ""
echo "小米/Redmi:"
echo "  • 开发者选项 → 关闭【MIUI 优化】→ 重启手机"
echo "  • 开发者选项 → 开启【USB 调试（安全设置）】"
echo ""
echo "华为/荣耀:"
echo "  • 开发者选项 → 开启【仅充电模式下允许 ADB 调试】"
echo "  • 开发者选项 → 关闭【监控 ADB 安装应用】"
echo ""
echo "OPPO/Realme:"
echo "  • 开发者选项 → 开启【USB 调试】"
echo "  • 开发者选项 → 开启【禁止权限监控】"
echo ""
echo "vivo/iQOO:"
echo "  • 开发者选项 → 开启【USB 调试】"
echo "  • 可能需要插入 SIM 卡才能使用 USB 调试"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}快速检查清单${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "[ ] 1. 开发者选项已启用（点击版本号7次）"
echo "[ ] 2. USB 调试已开启（开发者选项中）"
echo "[ ] 3. 使用原装或质量好的数据线"
echo "[ ] 4. USB 连接模式选择【文件传输】"
echo "[ ] 5. Mac 能识别设备（系统信息 → USB）"
echo "[ ] 6. 手机屏幕已解锁"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "完成检查后，重新运行诊断："
echo "  ./scripts/diagnose-phone.sh"
echo ""
echo "或查看详细配置文档："
echo "  cat docs/PHONE_SETUP.md"
echo ""
