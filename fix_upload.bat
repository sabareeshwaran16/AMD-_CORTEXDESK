@echo off
echo ========================================
echo CortexDesk - File Upload Fix
echo ========================================
echo.
echo Installing missing dependency: python-pptx
echo.

cd backend
pip install python-pptx==0.6.21

echo.
echo ========================================
echo Fix applied successfully!
echo ========================================
echo.
echo You can now upload PPTX files without errors.
echo.
pause
