#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangManus启动脚本 - 增强版错误处理
"""

import os
import sys
import subprocess
import time
import platform
import traceback

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'langmanus-main', 'langmanus-main')
FRONTEND_DIR = os.path.join(BASE_DIR, 'langmanus-web-main')

def check_paths():
    """检查必要的路径是否存在"""
    print("检查项目路径...")
    
    paths_to_check = [
        (BASE_DIR, "项目根目录"),
        (BACKEND_DIR, "后端目录"),
        (FRONTEND_DIR, "前端目录"),
        (os.path.join(BACKEND_DIR, "server.py"), "后端服务器文件")
    ]
    
    all_exist = True
    for path, desc in paths_to_check:
        exists = os.path.exists(path)
        print(f"  {desc}: {'[OK]' if exists else '[缺失]'} ({path})")
        if not exists:
            all_exist = False
    
    return all_exist

def setup_frontend_env():
    """设置前端环境变量"""
    print("\n设置前端环境...")
    env_file = os.path.join(FRONTEND_DIR, '.env')
    
    if not os.path.exists(env_file):
        print("创建前端环境配置文件...")
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write("NEXT_PUBLIC_API_URL=http://localhost:8000/api\n")
            print("前端环境配置完成")
        except Exception as e:
            print(f"创建环境文件失败: {e}")
            return False
    else:
        print("前端环境配置已存在")
    
    return True

def start_backend():
    """启动后端服务"""
    print("\n启动后端服务...")
    os.chdir(BACKEND_DIR)
    backend_cmd = [sys.executable, "server.py"]
    
    try:
        if platform.system() == "Windows":
            backend_process = subprocess.Popen(backend_cmd, 
                                              creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            backend_process = subprocess.Popen(backend_cmd, 
                                              start_new_session=True)
        
        print(f"后端服务已启动 (PID: {backend_process.pid})")
        return backend_process
    except Exception as e:
        print(f"启动后端服务失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("\n启动前端服务...")
    os.chdir(FRONTEND_DIR)
    
    # 尝试用不同的命令启动前端
    commands = [
        ["npm", "run", "dev"],  # 常规npm
        ["pnpm", "dev"],        # 如果使用pnpm
        ["yarn", "dev"]         # 如果使用yarn
    ]
    
    frontend_process = None
    for cmd in commands:
        try:
            print(f"尝试使用命令: {' '.join(cmd)}")
            if platform.system() == "Windows":
                frontend_process = subprocess.Popen(cmd, 
                                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                frontend_process = subprocess.Popen(cmd, 
                                                   start_new_session=True)
            
            print(f"前端服务已启动 (PID: {frontend_process.pid})")
            break
        except FileNotFoundError:
            print(f"命令 {cmd[0]} 不可用，尝试下一个选项...")
        except Exception as e:
            print(f"启动失败: {e}")
    
    if not frontend_process:
        print("所有前端启动命令都失败了")
        print("请确认Node.js已正确安装，并安装了必要的依赖")
    
    return frontend_process

def main():
    print("\n===== LangManus 启动脚本 =====")
    
    # 检查路径
    if not check_paths():
        print("\n[错误] 一些必要的文件或目录不存在")
        print("请确认您已经正确克隆了LangManus项目")
        return False
    
    # 设置前端环境
    if not setup_frontend_env():
        return False
    
    # 询问是否先安装依赖
    choice = input("\n在启动之前是否需要安装依赖？(y/n): ").lower()
    if choice == 'y':
        print("\n请打开两个单独的命令提示符，分别执行以下命令：")
        print("\n后端依赖安装:")
        print(f"cd {BACKEND_DIR}")
        print("python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .")
        
        print("\n前端依赖安装:")
        print(f"cd {FRONTEND_DIR}")
        print("npm config set registry https://registry.npmmirror.com")
        print("npm install")
        
        input("\n安装完成后按回车继续...")
    
    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        return False
    
    # 等待后端启动
    print("等待5秒让后端服务启动...")
    time.sleep(5)
    
    # 启动前端
    frontend_process = start_frontend()
    
    if frontend_process:
        print("\n===== LangManus启动成功 =====")
        print("后端API: http://localhost:8000")
        print("前端页面: http://localhost:3000")
        print("\n您可以关闭此窗口，服务将在后台继续运行")
        
        # 保存进程ID
        try:
            with open(os.path.join(BASE_DIR, ".pid_file"), "w") as f:
                f.write(f"backend={backend_process.pid}\n")
                if frontend_process:
                    f.write(f"frontend={frontend_process.pid}\n")
        except Exception as e:
            print(f"保存进程ID失败: {e}")
    else:
        print("\n前端启动失败，但后端已启动")
        print("您可以手动进入前端目录运行: npm run dev")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            # 保持脚本运行
            input("\n按回车键退出此脚本（不会停止服务）...")
        else:
            input("\n启动失败，按回车键退出...")
    except Exception as e:
        print(f"\n[错误] 启动过程中出现错误: {e}")
        print("\n详细错误信息:")
        traceback.print_exc()
        input("\n按回车键退出...")
