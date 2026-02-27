@echo off
echo ========================================
echo Pushing CortexDesk to GitHub
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    echo.
)

REM Add remote if not exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding remote repository...
    git remote add origin https://github.com/Arunkumar-1129/amd--cortexdesk.git
    echo.
)

echo Staging files...
git add .
echo.

echo Committing changes...
git commit -m "CortexDesk: AI-powered workspace assistant with Ollama integration"
echo.

echo Pushing to GitHub...
git branch -M main
git push -u origin main
echo.

echo ========================================
echo Done! Check: https://github.com/Arunkumar-1129/amd--cortexdesk
echo ========================================
pause
