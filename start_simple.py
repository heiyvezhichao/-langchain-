"""
LangManus简易启动脚本 - 适用于PyCharm
"""

import os
import sys
import subprocess
import time

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'langmanus-main', 'langmanus-main')
FRONTEND_DIR = os.path.join(BASE_DIR, 'langmanus-web-main')

# Node.js路径 - 根据需要修改
# 如果Node.js已添加到PATH中，请保持为None
# 否则，请设置为Node.js安装目录，例如：r"C:\Program Files\nodejs"
NODE_PATH = None

def setup_env():
    # 设置环境变量
    if NODE_PATH and os.path.exists(NODE_PATH):
        os.environ["PATH"] = NODE_PATH + os.pathsep + os.environ["PATH"]
        print(f"已将Node.js路径添加到环境变量: {NODE_PATH}")

def create_env_file():
    # 创建前端环境文件
    env_file = os.path.join(FRONTEND_DIR, '.env')
    if not os.path.exists(env_file):
        print("创建前端环境配置文件...")
        with open(env_file, 'w') as f:
            f.write("NEXT_PUBLIC_API_URL=http://localhost:8000/api\n")
        print("完成")

def start_backend():
    # 启动后端服务
    print("\n启动后端服务...")
    os.chdir(BACKEND_DIR)
    backend_cmd = [sys.executable, "server.py"]
    backend_process = subprocess.Popen(backend_cmd, 
                                      creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(f"后端服务已启动 (PID: {backend_process.pid})")
    return backend_process

def start_frontend():
    # 启动前端服务
    print("\n启动前端服务...")
    os.chdir(FRONTEND_DIR)
    frontend_cmd = ["npm", "run", "dev"]
    
    try:
        frontend_process = subprocess.Popen(frontend_cmd, 
                                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(f"前端服务已启动 (PID: {frontend_process.pid})")
        return frontend_process
    except FileNotFoundError:
        print("启动前端失败：找不到npm命令")
        print("请确认Node.js已正确安装，或在脚本中设置正确的NODE_PATH")
        return None

def main():
    print("\n===== LangManus简易启动脚本 =====")
    
    # 设置环境变量
    setup_env()
    
    # 创建环境文件
    create_env_file()
    
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
        with open(os.path.join(BASE_DIR, ".pid_file"), "w") as f:
            f.write(f"backend={backend_process.pid}\n")
            if frontend_process:
                f.write(f"frontend={frontend_process.pid}\n")
    else:
        print("\n前端启动失败，但后端已启动")
        print("您可以手动进入前端目录运行: npm run dev")

if __name__ == "__main__":
    try:
        main()
        # 保持脚本运行
        input("\n按回车键退出此脚本（不会停止服务）...")
    except Exception as e:
        print(f"\n错误: {e}")
        input("\n按回车键退出...")
