@echo off
echo Stopping old backend processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do (
    if not "%%a"=="0" (
        taskkill /F /PID %%a 2>nul
    )
)
echo Done!
timeout /t 2 /nobreak >nul
