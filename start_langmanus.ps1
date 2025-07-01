# LangManus 一键启动脚本 (PowerShell版本)
Write-Host "===== LangManus 一键启动脚本 =====" -ForegroundColor Green
Write-Host ""

# 检查安装的Node.js版本
$nodeInstalled = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
if (-not $nodeInstalled) {
    Write-Host "[错误] 未检测到Node.js，请先安装Node.js" -ForegroundColor Red
    Write-Host "您可以从 https://nodejs.org/ 下载安装最新的LTS版本" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 检查Python安装
$pythonInstalled = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
if (-not $pythonInstalled) {
    Write-Host "[错误] 未检测到Python，请先安装Python" -ForegroundColor Red
    Write-Host "您可以从 https://www.python.org/downloads/ 下载安装Python 3.8+" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 创建前端环境文件（如果不存在）
$envFilePath = "langmanus-web-main\.env"
if (-not (Test-Path $envFilePath)) {
    Write-Host "创建前端环境配置文件..." -ForegroundColor Cyan
    "NEXT_PUBLIC_API_URL=http://localhost:8000/api" | Out-File -FilePath $envFilePath -Encoding utf8
    Write-Host "完成" -ForegroundColor Green
    Write-Host ""
}

# 安装Python依赖
Write-Host "开始安装后端Python依赖..." -ForegroundColor Cyan
Set-Location -Path "langmanus-main\langmanus-main"
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .
Write-Host "后端依赖安装完成" -ForegroundColor Green
Write-Host ""

# 安装Node.js依赖
Write-Host "开始安装前端Node.js依赖..." -ForegroundColor Cyan
Set-Location -Path "..\..\langmanus-web-main"
npm config set registry https://registry.npmmirror.com
npm install -g pnpm
pnpm config set registry https://registry.npmmirror.com
pnpm install
Write-Host "前端依赖安装完成" -ForegroundColor Green
Write-Host ""

# 返回项目根目录
Set-Location -Path ".."

# 启动后端服务
Write-Host "启动后端服务..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -Path 'langmanus-main\langmanus-main'; python server.py"
Write-Host "等待后端服务启动..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 启动前端应用
Write-Host "启动前端应用..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -Path 'langmanus-web-main'; pnpm dev"

Write-Host ""
Write-Host "===== LangManus 已成功启动 =====" -ForegroundColor Green
Write-Host "后端API运行在: http://localhost:8000" -ForegroundColor Yellow
Write-Host "前端页面访问: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "您可以关闭这个窗口，但请保留前端和后端的命令行窗口运行" -ForegroundColor Magenta
Read-Host "按回车键退出此窗口"
