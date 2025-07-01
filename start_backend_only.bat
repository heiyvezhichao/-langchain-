@echo off
echo ===== 启动LangManus后端服务 =====
echo.

cd langmanus-main\langmanus-main
start cmd /k python server.py

echo 后端服务已启动在: http://localhost:8000
echo.
echo 请保持后端窗口打开
echo.
