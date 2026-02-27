@echo off
echo ========================================
echo CortexDesk - Complete Startup Guide
echo ========================================
echo.
echo You need to start TWO servers:
echo.
echo 1. Backend Server (Port 8000)
echo 2. Frontend App (Port 5173)
echo.
echo ========================================
echo STEP 1: Start Backend
echo ========================================
echo.
echo Open a NEW terminal and run:
echo    start_backend_server.bat
echo.
echo Or manually:
echo    cd backend
echo    python -m app.main
echo.
pause
echo.
echo ========================================
echo STEP 2: Start Frontend
echo ========================================
echo.
echo Open ANOTHER terminal and run:
echo    start_frontend.bat
echo.
echo Or manually:
echo    cd desktop
echo    npm run dev
echo.
pause
echo.
echo ========================================
echo Access the App
echo ========================================
echo.
echo Once both are running, open your browser:
echo    http://localhost:5173
echo.
echo Backend API will be at:
echo    http://localhost:8000
echo.
pause
