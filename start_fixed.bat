@echo off
echo ========================================
echo CortexDesk - Document Upload Fix
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.

echo [2/4] Checking required directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\keys" mkdir data\keys
echo   - data\uploads: OK
echo   - data\keys: OK
echo.

echo [3/4] Checking dependencies...
python -c "import pdfplumber, docx, openpyxl, pptx, fastapi; print('  - All document parsers: OK')" 2>nul
if errorlevel 1 (
    echo   - Missing dependencies! Installing...
    pip install -r requirements.txt
)
echo.

echo [4/4] Starting API server...
echo   - Server will start on http://127.0.0.1:8001
echo   - Open cortexdesk.html in your browser
echo   - Press Ctrl+C to stop
echo.
python src\api.py
