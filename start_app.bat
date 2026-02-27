@echo off
echo ========================================
echo CortexDesk - Local AI Workspace
echo ========================================
echo.
echo Starting backend server...
echo Server: http://127.0.0.1:8001
echo Interface: cortexdesk.html
echo.
echo Press Ctrl+C to stop
echo.

start "" "cortexdesk.html"
python src\api.py
