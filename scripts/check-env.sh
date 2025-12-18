#!/bin/bash
# 环境检查和安装脚本

set -e

echo "================================================"
echo "OpenWechatAI-Core 环境检查"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 已安装"
        return 0
    else
        echo -e "${RED}✗${NC} $1 未安装"
        return 1
    fi
}

check_port() {
    port=$1
    service=$2
    if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠${NC} 端口 $port ($service) 被占用"
        return 1
    else
        echo -e "${GREEN}✓${NC} 端口 $port ($service) 可用"
        return 0
    fi
}

# 1. 检查Python
echo "1. 检查Python环境..."
if check_command python3; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "   版本: $PYTHON_VERSION"
    
    # 检查Python版本是否>=3.11
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ $MAJOR -ge 3 ] && [ $MINOR -ge 11 ]; then
        echo -e "   ${GREEN}版本符合要求${NC} (需要 Python 3.11+)"
    else
        echo -e "   ${RED}版本过低${NC} (当前: $PYTHON_VERSION, 需要: 3.11+)"
        echo "   请升级Python版本"
        exit 1
    fi
else
    echo -e "${RED}请安装Python 3.11或更高版本${NC}"
    echo "macOS: brew install python@3.11"
    exit 1
fi

# 2. 检查pip
echo ""
echo "2. 检查pip..."
if check_command pip3; then
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    echo "   版本: $PIP_VERSION"
else
    echo "   正在安装pip..."
    python3 -m ensurepip --upgrade
fi

# 3. 检查Docker
echo ""
echo "3. 检查Docker..."
if check_command docker; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo "   版本: $DOCKER_VERSION"
    
    # 检查Docker是否运行
    if docker info >/dev/null 2>&1; then
        echo -e "   ${GREEN}Docker服务正在运行${NC}"
    else
        echo -e "   ${RED}Docker服务未运行${NC}"
        echo "   请启动Docker Desktop"
        exit 1
    fi
else
    echo -e "${RED}Docker未安装${NC}"
    echo "请从 https://www.docker.com/products/docker-desktop 下载安装"
    exit 1
fi

# 4. 检查Docker Compose
echo ""
echo "4. 检查Docker Compose..."
if check_command docker-compose; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $NF}')
    echo "   版本: $COMPOSE_VERSION"
else
    echo -e "${RED}Docker Compose未安装${NC}"
    echo "请安装Docker Compose"
    exit 1
fi

# 5. 检查端口占用
echo ""
echo "5. 检查端口占用..."
PORT_CONFLICT=0

check_port 8000 "API服务" || PORT_CONFLICT=1
check_port 5432 "PostgreSQL" || PORT_CONFLICT=1
check_port 6379 "Redis" || PORT_CONFLICT=1
check_port 3000 "MCP服务" || PORT_CONFLICT=1

if [ $PORT_CONFLICT -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}检测到端口冲突${NC}"
    echo "建议修改 .env 文件使用备用端口："
    echo "  POSTGRES_PORT=5433"
    echo "  REDIS_PORT=6380"
    echo "  API_PORT=8001"
    echo ""
fi

# 6. 检查虚拟环境
echo ""
echo "6. 检查Python虚拟环境..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} 虚拟环境已存在"
else
    echo -e "${YELLOW}⚠${NC} 虚拟环境不存在，正在创建..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 虚拟环境创建完成"
fi

# 7. 检查依赖包
echo ""
echo "7. 检查Python依赖..."
if [ -f "requirements.txt" ]; then
    echo "   正在检查依赖包..."
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 检查是否需要安装
    MISSING_DEPS=0
    while IFS= read -r package; do
        # 跳过空行和注释
        [[ -z "$package" || "$package" =~ ^#.*$ ]] && continue
        
        pkg_name=$(echo $package | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1)
        
        if ! pip3 show "$pkg_name" >/dev/null 2>&1; then
            MISSING_DEPS=1
            break
        fi
    done < requirements.txt
    
    if [ $MISSING_DEPS -eq 1 ]; then
        echo -e "   ${YELLOW}⚠${NC} 检测到缺失的依赖包"
        echo "   正在安装依赖..."
        pip3 install -r requirements.txt
        echo -e "   ${GREEN}✓${NC} 依赖包安装完成"
    else
        echo -e "   ${GREEN}✓${NC} 所有依赖包已安装"
    fi
    
    deactivate
else
    echo -e "   ${RED}✗${NC} requirements.txt 不存在"
    exit 1
fi

# 8. 检查环境配置文件
echo ""
echo "8. 检查配置文件..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env 文件已存在"
else
    echo -e "${YELLOW}⚠${NC} .env 文件不存在"
    if [ -f ".env.example" ]; then
        echo "   正在从 .env.example 创建 .env..."
        cp .env.example .env
        echo -e "   ${GREEN}✓${NC} .env 文件已创建"
        echo -e "   ${YELLOW}请编辑 .env 文件填入实际配置${NC}"
    else
        echo -e "   ${RED}✗${NC} .env.example 不存在"
        exit 1
    fi
fi

# 9. 创建必要的目录
echo ""
echo "9. 创建必要的目录..."
mkdir -p logs screenshots rules tests/unit tests/integration docs

echo -e "${GREEN}✓${NC} 目录结构已创建"

# 10. 检查Git
echo ""
echo "10. 检查Git..."
if check_command git; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo "    版本: $GIT_VERSION"
    
    if [ -d ".git" ]; then
        echo -e "    ${GREEN}✓${NC} Git仓库已初始化"
    else
        echo -e "    ${YELLOW}⚠${NC} 不是Git仓库"
    fi
else
    echo -e "    ${YELLOW}⚠${NC} Git未安装（可选）"
fi

# 总结
echo ""
echo "================================================"
echo "环境检查完成"
echo "================================================"
echo ""

if [ $PORT_CONFLICT -eq 1 ]; then
    echo -e "${YELLOW}⚠ 注意：检测到端口冲突，请修改 .env 文件${NC}"
    echo ""
fi

echo "下一步："
echo "1. 编辑 .env 文件配置必要的环境变量"
echo "2. 激活虚拟环境: source venv/bin/activate"
echo "3. 运行测试: pytest"
echo "4. 启动服务: docker-compose up -d"
echo ""
echo "详细文档请查看:"
echo "- docs/QUICKSTART.md"
echo "- docs/PORT_CONFIG.md"
echo "- docs/MCP_DATABASE_REQUIREMENTS.md"
echo ""
