# -*- coding: utf-8 -*-
# 一键安装 CUDA 13.1（自动检测keyring + 自动下载 + 自动加源）
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYRING_FILE = "cuda-keyring_1.1-1_all.deb"
KEYRING_URL = "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb"

# 颜色输出（统一改成32m绿色，所有终端支持）
os.system('')
GREEN = "\033[32m"
RESET = "\033[0m"

class CmdTask:
    @staticmethod
    def run(c):
        print(f"执行命令: {c}")
        subprocess.run(c, shell=True)

def check_cuda_installed():
    try:
        res = subprocess.run("nvcc --version", shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.split("release ")[1].split(",")[0]
    except:
        return None

def get_cuda_run_files():
    return [f for f in os.listdir(BASE_DIR) if f.endswith(".run") and "cuda" in f.lower()]

def set_cuda_env():
    env = """
# CUDA ENV
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
"""
    with open("/etc/profile.d/cuda.sh", "w") as f:
        f.write(env)
    CmdTask.run("chmod +x /etc/profile.d/cuda.sh")

def install_cuda():
    print("\n=============================================================")
    print("              一键安装 CUDA（静默安装 + 自动配环境变量）")
    print("=============================================================\n")

    cuda_ver = check_cuda_installed()
    if cuda_ver:
        print(f"{GREEN}✅ CUDA 已安装！当前版本: {cuda_ver}{RESET}")
        return

    cuda_files = get_cuda_run_files()

    print("\n请选择安装方式：")
    print("  [1] 安装官方 CUDA Toolkit 13.1（推荐）")
    if cuda_files:
        print(f"  [2] {cuda_files[0]}")
    print("  [0] 返回主菜单")

    while True:
        choice = input("\n请输入序号: ").strip()
        if choice == "0":
            return

        elif choice == "1":
            print("\n🔍 检测 keyring 文件...")

            # ======================
            # 你的核心要求：检测文件
            # ======================
            keyring_path = os.path.join(BASE_DIR, KEYRING_FILE)
            if not os.path.exists(keyring_path):
                print("📥 未找到文件，自动下载 keyring...")
                CmdTask.run(f"wget -q {KEYRING_URL} -O {keyring_path}")
            else:
                print("✅ 已存在 keyring 文件，跳过下载")

            # 安装 keyring
            print("🔧 安装 keyring 以配置 NVIDIA 源...")
            CmdTask.run(f"dpkg -i {keyring_path}")

            # 更新并安装
            CmdTask.run("apt-get update")
            CmdTask.run("apt-get -y install cuda-toolkit-13-1")

            set_cuda_env()
            print(f"{GREEN}✅ CUDA 13.1 安装完成！{RESET}")
            return

        elif choice == "2" and cuda_files:
            path = os.path.join(BASE_DIR, cuda_files[0])
            print(f"\n📦 安装本地文件：{cuda_files[0]}")
            CmdTask.run("chmod +x " + path)
            CmdTask.run(path + " --silent --toolkit --override")
            set_cuda_env()
            print(f"{GREEN}✅ CUDA 安装完成！{RESET}")
            return

        else:
            print("❌ 输入无效")

if __name__ == "__main__":
    install_cuda()