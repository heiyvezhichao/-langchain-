@echo off
echo ===== Creating LangManus Frontend .env file =====
echo.

cd /d "D:\eqrthquake\agent\langmaus\langmanus-web-main"

echo Creating frontend environment file...
echo # This file was created by the LangManus startup script > .env
echo NEXT_PUBLIC_API_URL=http://localhost:8000/api >> .env
echo Done.
echo.

echo Environment file content:
type .env
echo.

echo If the file looks correct, you can now run start_frontend_cmd.bat to start the frontend
pause
