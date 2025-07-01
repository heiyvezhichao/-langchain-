@echo off
echo ===== LangManus 一键启动脚本 =====
echo.

:: 检查安装的Node.js版本
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Node.js，请先安装Node.js
    echo 您可以从 https://nodejs.org/ 下载安装最新的LTS版本
    pause
    exit /b 1
)

:: 检查Python安装
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未检测到Python，请先安装Python
    echo 您可以从 https://www.python.org/downloads/ 下载安装Python 3.8+
    pause
    exit /b 1
)

:: 创建前端环境文件（如果不存在）
if not exist "langmanus-web-main\.env" (
    echo 创建前端环境配置文件...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > langmanus-web-main\.env
    echo 完成
    echo.
)

:: 安装Python依赖
echo 开始安装后端Python依赖...
cd langmanus-main\langmanus-main
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .
echo 后端依赖安装完成
echo.

:: 安装Node.js依赖
echo 开始安装前端Node.js依赖...
cd ..\..\langmanus-web-main
call npm config set registry https://registry.npmmirror.com
call npm install -g pnpm
call pnpm config set registry https://registry.npmmirror.com
call pnpm install
echo 前端依赖安装完成
echo.

:: 启动后端服务
echo 启动后端服务...
start cmd /k "cd ..\\langmanus-main\\langmanus-main && python server.py"
echo 等待后端服务启动...
timeout /t 5 /nobreak > nul

:: 启动前端应用
echo 启动前端应用...
start cmd /k "cd ..\\langmanus-web-main && pnpm dev"

echo.
echo ===== LangManus 已成功启动 =====
echo 后端API运行在: http://localhost:8000
echo 前端页面访问: http://localhost:3000
echo.
echo 您可以关闭这个窗口，但请保留前端和后端的命令行窗口运行
pause
