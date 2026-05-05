# -*- coding: utf-8 -*-

# ==========================
# 内置基础库
# ==========================
class BaseTool:
    TYPE_CONFIG = "config"
    TYPE_INSTALL = "install"
    def __init__(self):
        self.name = ""
        self.type = ""
        self.author = ""

class PrintUtils:
    @staticmethod
    def print_info(t): print(f"\033[0m{t}\033[0m")
    @staticmethod
    def print_success(t): print(f"\033[32m{t}\033[0m")
    @staticmethod
    def print_warn(t): print(f"\033[0m{t}\033[0m")
    @staticmethod
    def print_error(t): print(f"\033[31m{t}\033[0m")

class CmdTask:
    @staticmethod
    def run(c, t=None):
        import subprocess
        subprocess.run(c, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class FileUtils:
    @staticmethod
    def delete(p):
        import os
        os.system(f"rm -rf {p}")
    @staticmethod
    def new(p, n, c):
        import os
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, n), 'w', encoding='utf-8') as f:
            f.write(c)

class AptUtils:
    @staticmethod
    def test_speed(url):
        import subprocess, time
        host = url.replace("https://","").replace("http://","").split("/")[0]
        try:
            start=time.time()
            subprocess.run(["ping","-c","2", host], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
            return round(time.time()-start, 2)
        except:
            return 99.99

    @staticmethod
    def test_all_and_show(urls):
        PrintUtils.print_success("==============================================")
        PrintUtils.print_info("开始测速所有镜像源...")
        speed_map = {}
        for url, name in urls:
            t=AptUtils.test_speed(url)
            speed_map[url] = t
            PrintUtils.print_info(f"延迟: {t:.2f}s | 【{name}】 {url}")
        PrintUtils.print_success("==============================================")
        return speed_map

class osversion:
    @staticmethod
    def get_codename():
        import os
        return os.popen("lsb_release -cs").read().strip()

class ChooseTask:
    def __init__(self, dic, title):
        self.dic=dic
        self.title=title

    def run(self):
        PrintUtils.print_success("==============================================")
        PrintUtils.print_success(f"{self.title}")
        PrintUtils.print_success("==============================================")
        for k, v in self.dic.items():
            print(f"\033[0m[{k}]:{v}\033[0m")
        print(f"\033[0m[0]:退出\033[0m")
        while True:
            ipt=input("\033[0m请输入[]内的数字选择功能:\033[0m").strip()
            if ipt == "0":
                import sys
                sys.exit(0)
            try:
                code=int(ipt)
                if code in self.dic:
                    return (code, self.dic[code])
            except:
                PrintUtils.print_error("输入无效，请重新输入！")

# ==========================
# 镜像源 + 中文名称
# ==========================
ubuntu_amd64_sources = [
    ("https://mirrors.tuna.tsinghua.edu.cn/ubuntu", "清华大学源"),
    ("https://mirrors.aliyun.com/ubuntu", "阿里云源"),
    ("https://mirrors.cloud.tencent.com/ubuntu", "腾讯云源"),
    ("https://developer.download.nvidia.com/compute/cuda/repos/ubuntu", "英伟达NVIDIA源"),
    ("https://mirror.sysu.edu.cn/ubuntu/", "中山大学源"),
    ("https://mirrors.ustc.edu.cn/ubuntu", "中国科技大学源"),
    ("https://archive.ubuntu.com/ubuntu", "Ubuntu官方源"),
    ("https://mirrors.kernel.org/ubuntu", "Kernel官方源"),
]

ubuntu_amd64_sources_template = """
deb <sources>/ <code-name> main restricted universe multiverse
deb <sources>/ <code-name>-updates main restricted universe multiverse
deb <sources>/ <code-name>-backports main restricted universe multiverse
deb <sources>/ <code-name>-security main restricted universe multiverse
"""

# ==========================
# 主逻辑
# ==========================
class Tool(BaseTool):
    def __init__(self):
        self.type=BaseTool.TYPE_CONFIG
        self.name="一键更换系统源"
        self.author='刘镇龙'

    def clean_old_source(self):
        dic={1:"仅更换系统源", 2:"清理第三方源并更换"}
        code, _=ChooseTask(dic, "请选择换源方式").run()
        FileUtils.delete('/etc/apt/sources.list')
        if code == 2:
            FileUtils.delete('/etc/apt/sources.list.d')
            CmdTask.run('sudo mkdir -p /etc/apt/sources.list.d')

        dic_source_method={1:"自动选择最快源", 2:"手动选择源"}
        self.source_method_code, _=ChooseTask(dic_source_method, "请选择选择方式").run()

    def get_source_by_system(self):
        urls=ubuntu_amd64_sources
        speed_map=AptUtils.test_all_and_show(urls)

        if self.source_method_code == 2:
            source_dic={i+1: f"【{name}】 {url}" for i, (url, name) in enumerate(urls)}
            _, selected_full=ChooseTask(source_dic, "请手动选择镜像源").run()
            for url, name in urls:
                if f"【{name}】 {url}" == selected_full:
                    return url
        else:
            fastest=min(speed_map, key=speed_map.get)
            for url, name in urls:
                if url == fastest:
                    PrintUtils.print_success(f"✅ 最快镜像: 【{name}】 {url}")
            return fastest

    def replace_source(self):
        source=self.get_source_by_system()
        codename=osversion.get_codename()
        FileUtils.new('/etc/apt/', 'sources.list',
                       ubuntu_amd64_sources_template.replace("<code-name>", codename).replace('<sources>', source))
        return source

    def change_sys_source(self):
        self.clean_old_source()
        self.replace_source()

        PrintUtils.print_success("=============================================================")
        PrintUtils.print_success("              系统源已成功更换完成！")
        PrintUtils.print_success("=============================================================")

        dic={1:"立即更新", 2:"稍后更新"}
        code, _=ChooseTask(dic, "是否立即更新软件源？").run()

        if code == 1:
            PrintUtils.print_info("\n正在更新...")
            CmdTask.run("sudo apt update")
            PrintUtils.print_success("\n🎉 更新完成！")

    def run(self):
        self.change_sys_source()

# ==========================
# 执行入口
# ==========================
if __name__ == "__main__":
    Tool().run()