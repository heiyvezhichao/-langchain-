@echo off
echo ===== 安装LangManus前端依赖 =====
echo.

cd langmanus-web-main

REM 设置npm使用国内镜像
echo 设置npm使用国内镜像源...
call npm config set registry https://registry.npmmirror.com

REM 安装依赖
echo 正在安装前端依赖(可能需要几分钟)...
call npm install

echo.
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 安装前端依赖失败
    echo 请检查是否安装了Node.js (20.10.0或更高版本)
) else (
    echo 前端依赖安装成功！
    echo.
    echo 现在您可以使用以下命令启动前端：
    echo cd langmanus-web-main
    echo npm run dev
)

pause
