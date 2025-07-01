@echo off
echo ===== Starting LangManus Frontend Service =====
echo.

cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating frontend environment file...
    echo NEXT_PUBLIC_API_URL=http://localhost:8000/api > .env
    echo Done.
    echo.
)

start cmd /k npm run dev

echo Frontend service should start at: http://localhost:3000
echo.
echo Please keep the frontend window open
pause
