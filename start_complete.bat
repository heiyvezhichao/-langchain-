@echo off
echo ===== LangManus 一键启动脚本 =====
echo.

REM 创建前端环境文件（如果不存在）
if not exist "langmanus-web-main\.env" (
    echo 创建前端环境配置文件...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > langmanus-web-main\.env
    echo 完成
    echo.
)

REM 启动后端服务
echo 启动后端服务...
start cmd /k "cd langmanus-main\langmanus-main && python server.py"
echo 等待后端服务启动...
timeout /t 5 /nobreak > nul

REM 启动前端应用
echo 启动前端应用...
start cmd /k "cd langmanus-web-main && npm run dev"

echo.
echo ===== LangManus 已成功启动 =====
echo 后端API运行在: http://localhost:8000
echo 前端页面访问: http://localhost:3000
echo.
echo 您可以关闭这个窗口，但请保留前端和后端的命令行窗口运行
pause
