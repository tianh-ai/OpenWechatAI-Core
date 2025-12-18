#!/bin/bash
# 项目完成度验证脚本

set -e

echo "================================================"
echo "OpenWechatAI-Core 项目完成度验证"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

TOTAL_CHECKS=0
PASSED_CHECKS=0

check_item() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ $2 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

echo -e "${BLUE}1. 核心代码文件检查${NC}"
echo "-------------------------------------------"

# 核心配置
[ -f "core/config.py" ] && check_item "配置管理 (core/config.py)" 0 || check_item "配置管理 (core/config.py)" 1
[ -f "core/main.py" ] && check_item "主程序入口 (core/main.py)" 0 || check_item "主程序入口 (core/main.py)" 1
[ -f "core/tasks.py" ] && check_item "Celery 任务 (core/tasks.py)" 0 || check_item "Celery 任务 (core/tasks.py)" 1

# 数据模型
[ -f "models/database.py" ] && check_item "MCP 数据库接口 (models/database.py)" 0 || check_item "MCP 数据库接口 (models/database.py)" 1
[ -f "models/repositories.py" ] && check_item "Repository 层 (models/repositories.py)" 0 || check_item "Repository 层 (models/repositories.py)" 1

# 规则引擎
[ -f "rules/engine.py" ] && check_item "规则引擎 (rules/engine.py)" 0 || check_item "规则引擎 (rules/engine.py)" 1
[ -f "rules/actions.py" ] && check_item "规则动作 (rules/actions.py)" 0 || check_item "规则动作 (rules/actions.py)" 1

# AI 集成
[ -f "ai/chat.py" ] && check_item "AI 对话管理 (ai/chat.py)" 0 || check_item "AI 对话管理 (ai/chat.py)" 1
[ -f "ai/providers/openai_provider.py" ] && check_item "OpenAI 提供商 (ai/providers/openai_provider.py)" 0 || check_item "OpenAI 提供商 (ai/providers/openai_provider.py)" 1

# WeChat 自动化
[ -f "wechat/automation.py" ] && check_item "UI 自动化 (wechat/automation.py)" 0 || check_item "UI 自动化 (wechat/automation.py)" 1
[ -f "wechat/message_handler.py" ] && check_item "消息处理 (wechat/message_handler.py)" 0 || check_item "消息处理 (wechat/message_handler.py)" 1

# API 服务
[ -f "api/main.py" ] && check_item "FastAPI 应用 (api/main.py)" 0 || check_item "FastAPI 应用 (api/main.py)" 1

echo ""
echo -e "${BLUE}2. 配置文件检查${NC}"
echo "-------------------------------------------"

[ -f "docker-compose.yml" ] && check_item "Docker Compose 配置" 0 || check_item "Docker Compose 配置" 1
[ -f "Dockerfile" ] && check_item "Dockerfile" 0 || check_item "Dockerfile" 1
[ -f "requirements.txt" ] && check_item "Python 依赖" 0 || check_item "Python 依赖" 1
[ -f ".env.example" ] && check_item "环境变量模板" 0 || check_item "环境变量模板" 1
[ -f ".env" ] && check_item ".env 配置文件" 0 || check_item ".env 配置文件" 1

echo ""
echo -e "${BLUE}3. 测试文件检查${NC}"
echo "-------------------------------------------"

[ -f "tests/unit/test_config.py" ] && check_item "配置测试" 0 || check_item "配置测试" 1
[ -f "tests/unit/test_database.py" ] && check_item "数据库测试" 0 || check_item "数据库测试" 1
[ -f "tests/unit/test_rules_engine.py" ] && check_item "规则引擎测试" 0 || check_item "规则引擎测试" 1
[ -f "tests/integration/test_api_integration.py" ] && check_item "API 集成测试" 0 || check_item "API 集成测试" 1

echo ""
echo -e "${BLUE}4. 文档检查${NC}"
echo "-------------------------------------------"

[ -f "README.md" ] && check_item "项目 README" 0 || check_item "项目 README" 1
[ -f "docs/QUICKSTART.md" ] && check_item "快速开始指南" 0 || check_item "快速开始指南" 1
[ -f "docs/PORT_CONFIG.md" ] && check_item "端口配置文档" 0 || check_item "端口配置文档" 1
[ -f "docs/MCP_INTEGRATION_RULES.md" ] && check_item "MCP 集成规范" 0 || check_item "MCP 集成规范" 1
[ -f "docs/MCP_DATABASE_REQUIREMENTS.md" ] && check_item "MCP 数据库需求" 0 || check_item "MCP 数据库需求" 1
[ -f "docs/PROJECT_SUMMARY.md" ] && check_item "项目实现总结" 0 || check_item "项目实现总结" 1

echo ""
echo -e "${BLUE}5. 工具脚本检查${NC}"
echo "-------------------------------------------"

[ -f "scripts/check-env.sh" ] && [ -x "scripts/check-env.sh" ] && check_item "环境检查脚本" 0 || check_item "环境检查脚本" 1

echo ""
echo -e "${BLUE}6. 环境验证${NC}"
echo "-------------------------------------------"

# Python 环境
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check_item "Python 环境 (${PYTHON_VERSION})" 0
else
    check_item "Python 环境" 1
fi

# 虚拟环境
[ -d "venv" ] && check_item "Python 虚拟环境" 0 || check_item "Python 虚拟环境" 1

# Docker
if command -v docker &> /dev/null; then
    check_item "Docker 已安装" 0
else
    check_item "Docker 已安装" 1
fi

# Docker Compose
if command -v docker-compose &> /dev/null; then
    check_item "Docker Compose 已安装" 0
else
    check_item "Docker Compose 已安装" 1
fi

echo ""
echo -e "${BLUE}7. 依赖包验证${NC}"
echo "-------------------------------------------"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    
    # 检查关键包
    pip show fastapi &>/dev/null && check_item "FastAPI 已安装" 0 || check_item "FastAPI 已安装" 1
    pip show pydantic &>/dev/null && check_item "Pydantic 已安装" 0 || check_item "Pydantic 已安装" 1
    pip show celery &>/dev/null && check_item "Celery 已安装" 0 || check_item "Celery 已安装" 1
    pip show redis &>/dev/null && check_item "Redis 已安装" 0 || check_item "Redis 已安装" 1
    pip show pytest &>/dev/null && check_item "Pytest 已安装" 0 || check_item "Pytest 已安装" 1
    
    deactivate
else
    check_item "无法验证依赖包（虚拟环境未激活）" 1
fi

echo ""
echo "================================================"
echo "验证完成"
echo "================================================"
echo ""

# 计算完成度
PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

echo -e "总检查项: ${BLUE}${TOTAL_CHECKS}${NC}"
echo -e "通过项目: ${GREEN}${PASSED_CHECKS}${NC}"
echo -e "失败项目: ${RED}$((TOTAL_CHECKS - PASSED_CHECKS))${NC}"
echo ""

if [ $PERCENTAGE -ge 90 ]; then
    echo -e "完成度: ${GREEN}${PERCENTAGE}%${NC} ✨ 优秀！"
elif [ $PERCENTAGE -ge 70 ]; then
    echo -e "完成度: ${YELLOW}${PERCENTAGE}%${NC} ⚠️  良好"
else
    echo -e "完成度: ${RED}${PERCENTAGE}%${NC} ❌ 需要改进"
fi

echo ""
echo "下一步操作建议："
echo "1. 查看快速开始文档: cat docs/QUICKSTART.md"
echo "2. 配置环境变量: vim .env"
echo "3. 启动服务: docker-compose up -d"
echo "4. 运行测试: source venv/bin/activate && pytest"
echo ""

exit 0
