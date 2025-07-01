#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangManus一键启动脚本
用于在PyCharm中一键启动LangManus前后端服务
"""

import os
import sys
import subprocess
import time
import platform
import shutil

# 设置默认编码为UTF-8
if sys.platform.startswith('win'):
    # Windows环境下设置控制台编码
    os.system('chcp 65001 >nul 2>&1')

# 项目路径定义
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'langmanus-main', 'langmanus-main')
FRONTEND_DIR = os.path.join(BASE_DIR, 'langmanus-web-main')

def check_dependencies():
    """检查必要的依赖是否已安装"""
    print("===== 检查依赖 =====")
    
    # 检查Python
    print("检查Python...", end="")
    if sys.version_info < (3, 8):
        print("\n[错误] Python版本需要3.8或更高")
        return False
    print("通过")
    
    # 检查Node.js - 尝试常见的安装位置
    print("检查Node.js...", end="")
    node_path = shutil.which("node")
    
    # 如果在PATH中找不到，尝试常见的安装位置
    if not node_path:
        common_node_paths = [
            r"C:\Program Files\nodejs\node.exe",
            r"C:\Program Files (x86)\nodejs\node.exe",
            os.path.expanduser("~\\AppData\\Roaming\\nvm\\current\\node.exe")
        ]
        
        for path in common_node_paths:
            if os.path.exists(path):
                node_path = path
                # 将Node.js添加到环境变量中
                os.environ["PATH"] = os.path.dirname(path) + os.pathsep + os.environ["PATH"]
                print(f"找到Node.js: {path}")
                break
                
    if not node_path:
        print("\n[错误] 未找到Node.js，请先安装Node.js")
        print("您可以从 https://nodejs.org/ 下载安装最新的LTS版本")
        print("如果您已经安装了Node.js，请确认它已添加到系统PATH环境变量中，或者重启计算机")
        return False
    print("通过" if "找到" not in str(node_path) else "")
    
    # 检查npm - 使用与node相同的目录
    print("检查npm...", end="")
    if node_path:
        node_dir = os.path.dirname(node_path)
        npm_path = os.path.join(node_dir, "npm.cmd" if platform.system() == "Windows" else "npm")
        if os.path.exists(npm_path):
            # 将npm添加到环境变量中
            os.environ["PATH"] = node_dir + os.pathsep + os.environ["PATH"]
            print("通过")
        else:
            print("\n[错误] 未找到npm，请确保Node.js安装正确")
            return False
    else:
        print("\n[错误] 未找到npm，请确保Node.js安装正确")
        return False
    
    return True

def setup_frontend_env():
    """设置前端环境变量"""
    print("\n===== 设置前端环境 =====")
    env_file = os.path.join(FRONTEND_DIR, '.env')
    
    if not os.path.exists(env_file):
        print("创建前端环境配置文件...")
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write("NEXT_PUBLIC_API_URL=http://localhost:8000/api\n")
        print("前端环境配置完成")
    else:
        print("前端环境配置已存在")

def install_dependencies():
    """安装项目依赖"""
    print("\n===== 安装项目依赖 =====")
    
    # 安装后端依赖
    print("正在安装后端Python依赖...")
    os.chdir(BACKEND_DIR)
    subprocess.run([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple", "-e", "."], check=True)
    print("后端依赖安装完成")
    
    # 安装前端依赖
    print("\n正在安装前端Node.js依赖...")
    os.chdir(FRONTEND_DIR)
    
    # 设置npm使用国内镜像
    subprocess.run(["npm", "config", "set", "registry", "https://registry.npmmirror.com"], check=True)
    
    # 安装pnpm
    subprocess.run(["npm", "install", "-g", "pnpm"], check=True)
    
    # 设置pnpm使用国内镜像
    subprocess.run(["pnpm", "config", "set", "registry", "https://registry.npmmirror.com"], check=True)
    
    # 使用pnpm安装依赖
    subprocess.run(["pnpm", "install"], check=True)
    print("前端依赖安装完成")
    
    # 回到项目根目录
    os.chdir(BASE_DIR)

def start_services():
    """启动前后端服务"""
    print("\n===== 启动服务 =====")
    
    # 构建启动命令
    backend_cmd = [sys.executable, "server.py"]
    frontend_cmd = ["pnpm", "dev"]
    
    # 根据操作系统选择不同的启动方式
    system = platform.system()
    
    # 启动后端
    print("启动后端服务...")
    os.chdir(BACKEND_DIR)
    if system == "Windows":
        backend_process = subprocess.Popen(backend_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        backend_process = subprocess.Popen(backend_cmd, start_new_session=True)
    
    # 等待几秒让后端启动
    print("等待后端服务启动...")
    time.sleep(5)
    
    # 启动前端
    print("启动前端应用...")
    os.chdir(FRONTEND_DIR)
    if system == "Windows":
        frontend_process = subprocess.Popen(frontend_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        frontend_process = subprocess.Popen(frontend_cmd, start_new_session=True)
    
    print("\n===== LangManus 启动成功 =====")
    print("后端API运行在: http://localhost:8000")
    print("前端页面访问: http://localhost:3000")
    print("\n您可以关闭这个窗口，但请保留前端和后端的命令行窗口运行")
    
    # 将进程ID保存，以便后续关闭
    with open(os.path.join(BASE_DIR, ".pid_file"), "w") as f:
        f.write(f"backend={backend_process.pid}\n")
        f.write(f"frontend={frontend_process.pid}\n")
    
    # 防止脚本立即退出
    try:
        print("\n按Ctrl+C可以退出此脚本（不会停止服务）")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n脚本已退出，服务仍在后台运行")

def main():
    """主函数"""
    print("\n===== LangManus 一键启动脚本 =====")
    
    # 检查依赖
    if not check_dependencies():
        input("按回车键退出...")
        return
    
    # 设置前端环境变量
    setup_frontend_env()
    
    # 询问是否需要安装依赖
    install_deps = input("\n是否需要安装项目依赖？首次运行需要安装 (y/n): ").lower()
    if install_deps == 'y':
        install_dependencies()
    
    # 启动服务
    start_services()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[错误] 启动过程中出现错误: {e}")
        input("按回车键退出...")
