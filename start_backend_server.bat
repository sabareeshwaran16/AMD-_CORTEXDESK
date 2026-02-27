@echo off
echo ========================================
echo Starting CortexDesk Backend Server
echo ========================================
echo.
echo Backend will run on: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

cd backend
python -m app.main
