@echo off
echo ============================================
echo Local AI Workspace Assistant - Setup
echo ============================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

echo [3/3] Running system test...
python test_system.py
if errorlevel 1 (
    echo WARNING: Some tests failed. Check output above.
) else (
    echo All tests passed!
)
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the system:
echo   Web Interface: python src\api.py
echo   CLI Interface: python src\cli.py
echo.
pause
