@echo off
echo ============================================
echo Local AI Workspace Assistant
echo ============================================
echo.
echo Select interface:
echo   1. Web Interface (Recommended)
echo   2. Command Line Interface
echo   3. Run Tests
echo   4. Exit
echo.
set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Web Interface...
    echo Open src\ui\index.html in your browser
    echo API running at http://127.0.0.1:8000
    echo Press Ctrl+C to stop
    echo.
    python src\api.py
) else if "%choice%"=="2" (
    echo.
    echo Starting CLI...
    echo.
    python src\cli.py
) else if "%choice%"=="3" (
    echo.
    echo Running tests...
    echo.
    python test_system.py
    pause
) else if "%choice%"=="4" (
    exit /b 0
) else (
    echo Invalid choice
    pause
)
