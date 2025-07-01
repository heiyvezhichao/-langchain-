@echo off
echo ===== Starting LangManus Backend Service =====
echo.

cd /d "D:\eqrthquake\agent\langmaus\langmanus-main\langmanus-main"
start cmd /k python server.py

echo Backend service started at: http://localhost:8000
echo.
echo Please keep the backend window open
pause
