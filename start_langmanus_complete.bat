@echo off
chcp 437 > nul
echo ===== LangManus Complete Launcher =====
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
cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"
if not exist ".env" (
    echo Creating frontend environment file...
    echo # This file was created by the LangManus startup script > .env
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api >> .env
    echo Done.
    echo.
)
cd /d "D:\eqrthquake\agent\langmaus"

REM Start backend service
echo Starting LangManus backend service...
cd /d "D:\eqrthquake\agent\langmaus\langmanus-main\langmanus-main"

REM Verify server.py exists
if not exist "server.py" (
    echo [ERROR] server.py not found in %CD%
    cd /d "D:\eqrthquake\agent\langmaus"
    pause
    exit /b 1
)

REM Start backend in new window
start "LangManus Backend" cmd /c python server.py
cd /d "D:\eqrthquake\agent\langmaus"

REM Wait for backend to initialize
echo Waiting for backend service to initialize (10 seconds)...
timeout /t 10 /nobreak > nul

REM Start frontend service
echo Starting LangManus frontend service...
cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"

REM Verify package.json exists
if not exist "package.json" (
    echo [ERROR] package.json not found in %CD%
    cd /d "D:\eqrthquake\agent\langmaus"
    pause
    exit /b 1
)

REM Start frontend in new window
start "LangManus Frontend" cmd /c npm run dev
cd /d "D:\eqrthquake\agent\langmaus"

echo.
echo ===== LangManus startup complete =====
echo.
echo Backend API is at: http://localhost:8000
echo Frontend is at: http://localhost:3000
echo.
echo [IMPORTANT] Please keep both command windows open
echo It may take up to 30 seconds for the servers to fully start
echo.
echo Waiting 20 seconds before opening browser...
timeout /t 20 /nobreak > nul

echo Opening frontend in browser...
start http://localhost:3000

pause
