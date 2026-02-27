@echo off
echo Checking if backend is running...
curl -s http://127.0.0.1:8001/ >nul 2>&1
if %errorlevel% == 0 (
    echo Backend is already running on port 8001
    echo.
    echo Open cortexdesk.html in your browser
    pause
) else (
    echo Backend not running. Starting now...
    echo.
    echo Server will run on: http://127.0.0.1:8001
    echo Open cortexdesk.html in your browser
    echo Press Ctrl+C to stop
    echo.
    python src\api.py
)
