#!/bin/bash
set -e

# ========================
# 统一颜色（和你所有脚本一致）
# ========================
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

# ========================
# 路径自动获取当前目录（可移植！）
# ========================
BASE_DIR=$(cd "$(dirname "$0")" && pwd)
DRIVER_FILE="${BASE_DIR}/NVIDIA-Linux-x86_64-590.44.01.run"
KERNEL_MODULES_DIR="${BASE_DIR}/open-gpu-kernel-modules"

# ========================
# 统一界面标题
# ========================
clear
echo "============================================================="
echo "              一键安装 NVIDIA-P2P 驱动（内核模块）"
echo "============================================================="

# ========================
# 1. 安装驱动
# ========================
echo -e "\n🔧 安装 NVIDIA 驱动（无内核模块）"
if [ -f "$DRIVER_FILE" ]; then
    chmod +x "$DRIVER_FILE"
    bash "$DRIVER_FILE" --no-kernel-modules -s
    echo -e "${GREEN}✅ 驱动安装完成${RESET}"
else
    echo -e "${RED}❌ 驱动文件不存在：$DRIVER_FILE${RESET}"
    exit 1
fi

# ========================
# 2. 编译安装内核模块
# ========================
echo -e "\n🔧 编译安装 open-gpu-kernel-modules"
if [ -d "$KERNEL_MODULES_DIR" ]; then
    cd "$KERNEL_MODULES_DIR" || exit 1
    chmod +x install.sh
    ./install.sh
    echo -e "${GREEN}✅ 内核模块安装完成${RESET}"
else
    echo -e "${RED}❌ 内核模块目录不存在：$KERNEL_MODULES_DIR${RESET}"
    exit 1
fi

# ========================
# 最终成功提示（统一风格）
# ========================
echo -e "\n============================================================="
echo -e "${GREEN}✅ NVIDIA-P2P 驱动全部安装完成！${RESET}"
echo "============================================================="