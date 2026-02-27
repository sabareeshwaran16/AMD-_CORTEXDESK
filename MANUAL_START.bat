@echo off
echo ========================================
echo STEP 1: Start Backend
echo ========================================
echo.
echo Open a NEW terminal and run:
echo    python src\api.py
echo.
echo Wait until you see: "Uvicorn running on http://127.0.0.1:8001"
echo.
pause
echo.
echo ========================================
echo STEP 2: Start Desktop App
echo ========================================
echo.
echo Open ANOTHER terminal and run:
echo    cd desktop
echo    npm run dev
echo.
echo Wait until you see: "Local: http://localhost:5173"
echo.
pause
echo.
echo ========================================
echo STEP 3: Open App
echo ========================================
echo.
echo Desktop app should open automatically
echo If not, open: http://localhost:5173
echo.
pause
