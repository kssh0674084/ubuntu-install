# -*- coding: utf-8 -*-
# 一键安装 Conda（终极修复版 · 路径正确 + 安装失败不会误报）
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_HOME = os.path.expanduser("~")

# 固定下载地址
ANACONDA_URL = "https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Linux-x86_64.sh"
ANACONDA_FILE = "Anaconda3-2025.12-2-Linux-x86_64.sh"

MINICONDA_URL = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
MINICONDA_FILE = "Miniconda3-latest-Linux-x86_64.sh"

# 颜色 【只改这里！92m → 32m】
os.system('')
GREEN = "\033[32m"    # 标准绿色，所有终端都支持
RED = "\033[31m"
RESET = "\033[0m"

class CmdTask:
    @staticmethod
    def run(c):
        print(f"执行命令: {c}")
        return subprocess.run(c, shell=True, cwd=BASE_DIR).returncode

def check_conda_installed():
    try:
        result = subprocess.run("conda --version 2>/dev/null", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_local_conda_files():
    files = []
    for f in os.listdir(BASE_DIR):
        low = f.lower()
        if f.endswith(".sh") and ("anaconda" in low or "miniconda" in low):
            files.append(f)
    return files

def choose_conda_type():
    print("\n请选择要安装的版本：")
    print("  [1] Anaconda3（2025.12-2 完整版，推荐）")
    print("  [2] Miniconda3（最新轻量版）")
    print("  [0] 返回主菜单")
    while True:
        choice = input("\n请输入序号: ").strip()
        if choice in ["0", "1", "2"]:
            return choice
        print("❌ 输入无效，请重新输入！")

def install_conda():
    print("\n=============================================================")
    print("              一键安装 Conda（Anaconda/Miniconda）")
    print("=============================================================\n")

    if check_conda_installed():
        print(f"{GREEN}✅ Conda 已安装！{RESET}")
        return

    # 选择安装类型
    conda_type = choose_conda_type()
    if conda_type == "0":
        return

    local_files = get_local_conda_files()
    print("\n请选择安装方式：")
    print("  [1] 在线安装（推荐）")
    if local_files:
        print(f"  [2] {local_files[0]}（本地安装）")
    print("  [0] 返回主菜单")

    while True:
        method = input("\n请输入序号: ").strip()
        if method == "0":
            return
        if method not in ["1", "2"]:
            print("❌ 输入无效")
            continue

        install_path = ""
        success = False

        # ========== 在线安装 ==========
        if method == "1":
            if conda_type == "1":
                install_path = os.path.join(USER_HOME, "anaconda3")
                print(f"\n📦 安装：Anaconda3 2025.12-2")
                print(f"📂 路径：{install_path}")
                
                if CmdTask.run(f"wget -q {ANACONDA_URL}") != 0:
                    print(f"{RED}❌ 下载失败！{RESET}")
                    continue
                if CmdTask.run(f"bash {ANACONDA_FILE} -b -p {install_path}") == 0:
                    success = True
                if os.path.exists(ANACONDA_FILE):
                    os.remove(ANACONDA_FILE)

            else:
                install_path = os.path.join(USER_HOME, "miniconda3")
                print(f"\n📦 安装：Miniconda3 最新版")
                print(f"📂 路径：{install_path}")
                
                if CmdTask.run(f"wget -q {MINICONDA_URL} -O {MINICONDA_FILE}") != 0:
                    print(f"{RED}❌ 下载失败！{RESET}")
                    continue
                if CmdTask.run(f"bash {MINICONDA_FILE} -b -p {install_path}") == 0:
                    success = True
                if os.path.exists(MINICONDA_FILE):
                    os.remove(MINICONDA_FILE)

        # ========== 本地安装 ==========
        elif method == "2" and local_files:
            local_file = local_files[0]
            local_file_path = os.path.join(BASE_DIR, local_file)

            if conda_type == "1":
                install_path = os.path.join(USER_HOME, "anaconda3")
                print(f"\n📦 本地安装 Anaconda3：{local_file}")
            else:
                install_path = os.path.join(USER_HOME, "miniconda3")
                print(f"\n📦 本地安装 Miniconda3：{local_file}")
            
            print(f"📂 路径：{install_path}")
            
            # 核心修复：确保进入安装包所在目录执行
            if CmdTask.run(f"bash {local_file} -b -p {install_path}") == 0:
                success = True

        # ========== 安装失败直接结束 ==========
        if not success or not os.path.exists(install_path):
            print(f"\n{RED}❌ 安装失败！文件不存在或安装出错！{RESET}")
            return

        # ========== 初始化 + 生效 ==========
        conda_bin = os.path.join(install_path, "bin/conda")
        CmdTask.run(f"{conda_bin} init bash")
        print(f"\n✅ 环境变量已配置，正在生效...")
        os.system("bash -c 'source ~/.bashrc'")

        # ========== 成功 ==========
        print("\n" + "="*60)
        print(f"{GREEN}✅ Conda 安装完成！{RESET}")
        print(f"{GREEN}📂 安装路径：{install_path}{RESET}")
        print(f"{GREEN}✅ 已自动配置环境变量并生效！{RESET}")
        print("="*60)
        return

if __name__ == "__main__":
    install_conda()
    sys.exit(0)