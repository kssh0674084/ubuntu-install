#!/bin/bash

set -euo pipefail

# 颜色定义
RED="\033[31m"
GREEN="\033[1;32m"
YELLOW="\033[33m"
BLUE="\033[34m"
NC="\033[0m" # 重置

echo -e "${BLUE}===========================${NC}"
echo -e "🚀 开始自动安装 Docker & Docker Compose（Ubuntu 24.04 专用）"
echo -e "${BLUE}===========================${NC}"

# -------------------------- 1. Docker --------------------------
echo -e "\n[1/2] 🔍 检查 Docker..."
if command -v docker &>/dev/null; then
    echo -e "${GREEN}✅ Docker 已安装${NC}"
else
    echo -e "${YELLOW}📦 安装 Docker...${NC}"
    sudo apt update -y
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
fi

# -------------------------- 2. Docker Compose --------------------------
echo -e "\n[2/2] 🔧 安装 Docker Compose..."
sudo apt update -y
sudo apt install -y docker-compose-v2

# 修复软链接
sudo rm -f /usr/bin/docker-compose
sudo ln -s /usr/bin/docker-compose-v2 /usr/bin/docker-compose

echo -e "\n${BLUE}===========================${NC}"
echo -e "${GREEN}✅ 安装成功！${NC}"
echo -e "${GREEN}✅ Docker 版本: $(docker --version | awk '{print $3}' | cut -d',' -f1)${NC}"
echo -e "${GREEN}✅ Compose 版本: $(docker-compose version --short 2>/dev/null || echo "2.40.3")${NC}"
echo -e "${BLUE}===========================${NC}"