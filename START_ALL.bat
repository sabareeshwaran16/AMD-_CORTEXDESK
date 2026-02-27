@echo off
echo ========================================
echo CortexDesk - Starting All Services
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start "CortexDesk Backend" cmd /k "cd /d %~dp0 && python run_backend.py"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend App...
start "CortexDesk Frontend" cmd /k "cd /d %~dp0desktop && npm run dev"

echo.
echo ========================================
echo Services Starting...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Wait 10-15 seconds, then open:
echo http://localhost:5173
echo.
echo Close this window when done.
pause
