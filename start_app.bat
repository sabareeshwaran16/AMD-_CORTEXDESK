@echo off
echo ========================================
echo CortexDesk - Complete Startup
echo ========================================
echo.

echo [Step 1] Stopping old processes...
call KILL_OLD_BACKEND.bat

echo [Step 2] Starting Backend...
start "CortexDesk Backend" cmd /k "cd /d %~dp0 && python -m uvicorn src.api:app --host 127.0.0.1 --port 8001"

echo [Step 3] Waiting for backend...
timeout /t 8 /nobreak >nul

echo [Step 4] Starting Desktop App...
cd desktop
start "" npm run dev

echo.
echo ========================================
echo App is starting!
echo ========================================
echo.
echo Backend: http://localhost:8001
echo Frontend: http://localhost:5173
echo.
echo Close this window when done.
pause
