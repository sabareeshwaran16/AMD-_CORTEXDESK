@echo off
echo Starting Backend...
echo.
cd /d %~dp0
python -m uvicorn src.api:app --host 127.0.0.1 --port 8001
echo.
echo Backend stopped!
pause
