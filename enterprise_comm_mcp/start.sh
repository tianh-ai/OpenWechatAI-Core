#!/bin/bash
# 企业通信MCP快速启动脚本

set -e

echo "======================================"
echo "🤖 企业通信MCP服务 - 快速启动"
echo "======================================"
echo ""

# 检查Python版本
echo "📋 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python版本: $PYTHON_VERSION"

# 检查依赖
echo ""
echo "📦 检查依赖..."

check_package() {
    python3 -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✓ $1"
        return 0
    else
        echo "❌ $1 (未安装)"
        return 1
    fi
}

MISSING_PACKAGES=0

if ! check_package "flask"; then MISSING_PACKAGES=1; fi
if ! check_package "yaml"; then MISSING_PACKAGES=1; fi
if ! check_package "requests"; then MISSING_PACKAGES=1; fi

if [ $MISSING_PACKAGES -eq 1 ]; then
    echo ""
    echo "⚠️  发现缺失的依赖包"
    read -p "是否自动安装? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在安装依赖..."
        pip3 install flask pyyaml requests
    else
        echo "请手动安装: pip3 install flask pyyaml requests"
        exit 1
    fi
fi

# 检查配置文件
echo ""
echo "📝 检查配置文件..."

if [ ! -f "enterprise_comm_mcp/config.yaml" ]; then
    if [ -f "enterprise_comm_mcp/config.yaml.example" ]; then
        echo "⚠️  配置文件不存在，从模板创建..."
        cp enterprise_comm_mcp/config.yaml.example enterprise_comm_mcp/config.yaml
        echo "✓ 已创建配置文件: enterprise_comm_mcp/config.yaml"
        echo ""
        echo "💡 提示: 请编辑配置文件或使用Web界面配置"
    else
        echo "❌ 未找到配置文件模板"
        exit 1
    fi
else
    echo "✓ 配置文件存在"
fi

# 启动选项
echo ""
echo "======================================"
echo "请选择启动方式:"
echo "======================================"
echo "1) 启动MCP服务器 (后台运行)"
echo "2) 启动MCP服务器 (前台运行)"
echo "3) 打开Web配置界面"
echo "4) 测试配置"
echo "5) 查看服务状态"
echo "6) 停止服务"
echo "0) 退出"
echo ""
read -p "请输入选项 (0-6): " -n 1 -r
echo ""

case $REPLY in
    1)
        echo "🚀 启动MCP服务器（后台）..."
        cd enterprise_comm_mcp
        nohup python3 mcp_server.py > ../logs/mcp_server.log 2>&1 &
        echo $! > ../logs/mcp_server.pid
        echo "✓ 服务已启动"
        echo "  PID: $(cat ../logs/mcp_server.pid)"
        echo "  日志: logs/mcp_server.log"
        echo "  Web界面: http://localhost:8000/static/config.html"
        ;;
    
    2)
        echo "🚀 启动MCP服务器（前台）..."
        cd enterprise_comm_mcp
        python3 mcp_server.py
        ;;
    
    3)
        echo "🌐 打开Web配置界面..."
        if command -v open &> /dev/null; then
            open http://localhost:8000/static/config.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8000/static/config.html
        else
            echo "请在浏览器中打开: http://localhost:8000/static/config.html"
        fi
        ;;
    
    4)
        echo "🧪 测试配置..."
        cd enterprise_comm_mcp
        python3 -c "
import yaml
import sys

try:
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    print('✓ 配置文件格式正确')
    print('')
    print('平台状态:')
    print(f\"  企业微信: {'启用' if config.get('wework', {}).get('enabled') else '禁用'}\")
    print(f\"  飞书: {'启用' if config.get('feishu', {}).get('enabled') else '禁用'}\")
    print(f\"  钉钉: {'启用' if config.get('dingtalk', {}).get('enabled') else '禁用'}\")
except Exception as e:
    print(f'❌ 配置文件错误: {e}')
    sys.exit(1)
"
        ;;
    
    5)
        echo "📊 查看服务状态..."
        if [ -f "logs/mcp_server.pid" ]; then
            PID=$(cat logs/mcp_server.pid)
            if ps -p $PID > /dev/null; then
                echo "✓ 服务正在运行"
                echo "  PID: $PID"
                echo ""
                echo "最近日志:"
                tail -n 20 logs/mcp_server.log
            else
                echo "❌ 服务未运行（PID文件存在但进程不存在）"
            fi
        else
            echo "❌ 服务未运行"
        fi
        ;;
    
    6)
        echo "⏹️  停止服务..."
        if [ -f "logs/mcp_server.pid" ]; then
            PID=$(cat logs/mcp_server.pid)
            kill $PID 2>/dev/null && echo "✓ 服务已停止" || echo "❌ 停止失败"
            rm logs/mcp_server.pid
        else
            echo "⚠️  服务未运行"
        fi
        ;;
    
    0)
        echo "👋 退出"
        exit 0
        ;;
    
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "✓ 操作完成"
echo "======================================"
