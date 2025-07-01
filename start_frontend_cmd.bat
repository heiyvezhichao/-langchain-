@echo off
echo ===== Starting LangManus Frontend (CMD version) =====
echo.

cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating frontend environment file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env
    echo Done.
    echo.
)

echo Starting frontend using CMD (bypassing PowerShell restrictions)...
cmd.exe /c npm run dev

pause
