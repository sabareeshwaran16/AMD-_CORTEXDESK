@echo off
echo ========================================
echo CortexDesk Desktop Application
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "CortexDesk Backend" cmd /k "python start_backend.py"

echo Waiting for backend to start...
timeout /t 8 /nobreak >nul

echo [2/2] Starting Desktop App...
cd desktop
start "" npm run dev

echo.
echo Desktop app will open in a few seconds...
echo Backend running in separate window
echo.
pause
