@echo off
REM ========================================
REM CortexDesk - Start Backend Server
REM ========================================
REM 
REM This script starts the backend API server
REM 
REM To run: Double-click this file or run "start_backend.bat" in terminal
REM Server will run on: http://127.0.0.1:8001
REM Open cortexdesk.html in your browser after server starts
REM Press Ctrl+C to stop the server
REM ========================================

echo Starting CortexDesk Backend...
echo Server: http://127.0.0.1:8001
echo.
python src\api.py
