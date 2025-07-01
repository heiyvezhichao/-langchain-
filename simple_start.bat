@echo off
echo === LangManus Simple Starter ===
echo.

echo 1. Starting backend server...
start cmd /k "cd langmanus-main\langmanus-main && python server.py"

echo 2. Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak > nul

echo 3. Starting frontend server...
start cmd /k "cd langmanus-web-main && npm run dev"

echo.
echo === Startup complete ===
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo You can close this window, but keep the server windows open.
pause
