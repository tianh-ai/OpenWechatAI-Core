#!/bin/bash
# 捕获触摸事件 - 请在运行此脚本后立即点击发送按钮

echo "======================================"
echo "准备捕获触摸坐标"
echo "======================================"
echo ""
echo "请在 3 秒后点击发送按钮..."
echo ""

sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
echo ""
echo "现在请点击发送按钮！"
echo ""

# 捕获5秒的触摸事件
timeout 5 adb shell getevent | grep -E "ABS_MT_POSITION|BTN_TOUCH" | while read line; do
    echo "$line"
done

echo ""
echo "======================================"
echo "捕获完成！"
echo "======================================"
