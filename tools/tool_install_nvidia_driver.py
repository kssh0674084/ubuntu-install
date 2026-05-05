# -*- coding: utf-8 -*-
# 最终版：安装完 → 自动输出 nvidia-smi 信息
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 颜色
os.system('')
GREEN = "\033[32m"
RESET = "\033[0m"

class CmdTask:
    @staticmethod
    def run(c):
        print(f"执行命令: {c}")
        subprocess.run(c, shell=True)

def check_nvidia_installed():
    try:
        return subprocess.run("nvidia-smi", shell=True, capture_output=True).returncode == 0
    except:
        return False

def get_drivers():
    drivers = []
    for f in os.listdir(BASE_DIR):
        if f.endswith(".run") and "NVIDIA" in f:
            drivers.append(f)
    return drivers

def install():
    print("\n=============================================================")
    print("              一键安装 NVIDIA 显卡驱动（静默安装）")
    print("=============================================================\n")

    if check_nvidia_installed():
        print(f"{GREEN}✅ NVIDIA 驱动已安装！{RESET}")
        print("\n========== 当前显卡信息 ==========")
        subprocess.run("nvidia-smi", shell=True)
        return

    drivers = get_drivers()

    print("\n请选择安装方式：")
    print("  [1] 安装系统推荐驱动")
    if drivers:
        print(f"  [2] {drivers[0]}")
    print("  [0] 返回主菜单")

    while True:
        i = input("\n请输入序号: ").strip()
        if i == "0":
            return
        if i == "1":
            print("\n🔧 安装系统推荐驱动")
            CmdTask.run("ubuntu-drivers autoinstall")
            print(f"\n{GREEN}✅ 安装完成！请重启！{RESET}")
            return
        if i == "2" and drivers:
            path = os.path.join(BASE_DIR, drivers[0])
            
            print("\n🧹 清理 NVIDIA 环境...")
            CmdTask.run("systemctl stop gdm3 2>/dev/null")
            CmdTask.run("systemctl stop gdm 2>/dev/null")
            CmdTask.run("rmmod nvidia_drm 2>/dev/null")
            CmdTask.run("rmmod nvidia_modeset 2>/dev/null")
            CmdTask.run("rmmod nvidia 2>/dev/null")
            
            print(f"\n📦 静默安装：{drivers[0]}")
            CmdTask.run(f"chmod +x {path}")
            CmdTask.run(f"{path} --silent --accept-license --no-cc-version-check")
            
            print(f"\n{GREEN}✅ 驱动安装完成！请重启服务器！{RESET}")
            return
        print("❌ 输入无效")

if __name__ == "__main__":
    install()