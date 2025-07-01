@echo off
echo ===== LangManus Main Launcher =====
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 20.10.0 or higher from https://nodejs.org/
    echo Then run this script again.
    pause
    exit /b 1
)

REM Display Node.js version
echo Node.js detected:
node -v
echo.

REM Create frontend environment file if it doesn't exist
if not exist "langmanus-web-main\.env" (
    echo Creating frontend environment file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > langmanus-web-main\.env
    echo Done.
    echo.
)

REM Check if frontend dependencies are installed
if not exist "langmanus-web-main\node_modules" (
    echo Frontend dependencies not found. Installing...
    cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"
    call npm config set registry https://registry.npmmirror.com
    call npm install
    cd /d "D:\eqrthquake\agent\langmaus"
    
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install frontend dependencies.
        echo Please try running the install_frontend_deps.bat script manually.
        pause
        exit /b 1
    )
    echo Frontend dependencies installed successfully.
    echo.
)

REM Start backend service
echo Starting LangManus backend service...
cd /d "D:\eqrthquake\agent\langmaus\langmanus-main\langmanus-main"
start cmd /k python server.py
cd /d "D:\eqrthquake\agent\langmaus"

REM Wait for backend to initialize
echo Waiting for backend service to initialize...
timeout /t 5 /nobreak > nul

REM Start frontend service
echo Starting LangManus frontend service...
cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"
start cmd /k npm run dev
cd /d "D:\eqrthquake\agent\langmaus"

echo.
echo ===== LangManus successfully started =====
echo.
echo Backend API is running at: http://localhost:8000
echo Frontend web interface is at: http://localhost:3000
echo.
echo [IMPORTANT] Please keep both command windows open
echo When you want to stop LangManus, close both command windows.
echo.
echo Opening web interface in your default browser in 5 seconds...
timeout /t 5 /nobreak > nul
start http://localhost:3000

pause
