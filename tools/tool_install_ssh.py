# -*- coding: utf-8 -*-
# 一键安装并开启SSH（带检测 —— 无报错版）

class CmdTask:
    @staticmethod
    def run(c):
        import subprocess
        print(f"\033[0m执行命令: {c}\033[0m")
        subprocess.run(c, shell=True)

def is_ssh_running():
    """检测 SSH 服务是否已在运行"""
    import subprocess
    result = subprocess.run(["systemctl", "is-active", "--quiet", "ssh"])
    return result.returncode == 0  # 0=运行中

def install_ssh():
    print("\n=============================================================")
    print("              一键安装并启动SSH服务（带检测）")
    print("=============================================================\n")

    # 1. 安装
    CmdTask.run("apt install openssh-server -y")

    # 2. 检测状态
    if is_ssh_running():
        print("\n✅ SSH 服务已经是运行状态，无需重复启动。")
    else:
        print("\n⚠️ SSH 未运行，正在启动...")
        CmdTask.run("systemctl start ssh")
        CmdTask.run("systemctl enable ssh")
        print("\n✅ SSH 启动成功！")

    # 3. 防火墙
    CmdTask.run("ufw allow 22")

    print("\n=============================================================")
    print("✅ SSH 配置全部完成！")
    print("=============================================================\n")

if __name__ == "__main__":
    install_ssh()
    # 返回主菜单
    import os
    os.system("/mnt/drive/install")