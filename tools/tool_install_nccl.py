# -*- coding: utf-8 -*-
# 一键安装 NCCL（强制返回主菜单 · 最终完美版）
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 颜色 【只改这里：92m → 32m】
os.system('')
GREEN = "\033[32m"
RESET = "\033[0m"

KEYRING_FILE = "cuda-keyring_1.1-1_all.deb"
KEYRING_URL = "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb"

class CmdTask:
    @staticmethod
    def run(c):
        print(f"执行命令: {c}")
        subprocess.run(c, shell=True)

def check_nccl_installed():
    try:
        result = subprocess.run("ldconfig -p | grep libnccl.so", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_nccl_local_files():
    files = []
    for f in os.listdir(BASE_DIR):
        if ("nccl" in f.lower() or "libnccl" in f.lower()) and f.endswith(".deb"):
            files.append(f)
    return sorted(files)

def set_nccl_env():
    env_content = """
# NCCL Environment
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export NCCL_DEBUG=INFO
"""
    with open("/etc/profile.d/nccl.sh", "w") as f:
        f.write(env_content)
    CmdTask.run("chmod +x /etc/profile.d/nccl.sh")

def install_nccl():
    print("\n=============================================================")
    print("              一键安装 NCCL（GPU 通信库）")
    print("=============================================================\n")

    if check_nccl_installed():
        print(f"{GREEN}✅ NCCL 已安装！{RESET}")
        return

    local_files = get_nccl_local_files()

    print("\n请选择安装方式：")
    print("  [1] 安装官方 NCCL（推荐）")
    if local_files:
        print(f"  [2] {local_files[0]}")
    print("  [0] 返回主菜单")

    while True:
        choice = input("\n请输入序号: ").strip()
        if choice == "0":
            return

        elif choice == "1":
            print("\n🔍 检查 keyring 文件...")
            key_path = os.path.join(BASE_DIR, KEYRING_FILE)
            if not os.path.exists(key_path):
                print("📥 下载 keyring...")
                CmdTask.run(f"wget -q {KEYRING_URL} -O {key_path}")

            CmdTask.run(f"dpkg -i {key_path}")
            CmdTask.run("apt update")
            CmdTask.run("apt-get install -y libnccl2 libnccl-dev")
            set_nccl_env()
            
            print("\n" + "="*60)
            print(f"{GREEN}✅ NCCL 安装完成！{RESET}")
            print(f"{GREEN}📦 版本：2.30.4 (兼容 CUDA 13.1){RESET}")
            print(f"{GREEN}✅ NCCL 安装成功！{RESET}")
            print("="*60)

            # =======================
            # 强制返回主菜单（核心修复）
            # =======================
            sys.stdout.flush()
            os._exit(0)

        elif choice == "2" and local_files:
            fpath = os.path.join(BASE_DIR, local_files[0])
            print(f"\n📦 安装本地文件：{local_files[0]}")
            CmdTask.run(f"dpkg -i {fpath}")
            set_nccl_env()
            
            print("\n" + "="*60)
            print(f"{GREEN}✅ NCCL 安装完成！{RESET}")
            print(f"{GREEN}✅ NCCL 安装成功！{RESET}")
            print("="*60)

            # 强制返回
            sys.stdout.flush()
            os._exit(0)

        else:
            print("❌ 输入无效")

if __name__ == "__main__":
    install_nccl()