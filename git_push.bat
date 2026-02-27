@echo off
echo ========================================
echo Pushing CortexDesk to GitHub
echo ========================================
echo.

echo Adding remote (if not exists)...
git remote add origin https://github.com/Arunkumar-1129/amd--cortexdesk.git 2>nul
echo.

echo Staging all files...
git add .
echo.

echo Committing...
git commit -m "CortexDesk: AI-powered workspace assistant with Ollama integration - Full system with document processing, task extraction, and confirmation workflow"
echo.

echo Pushing to main branch...
git push -u origin main
echo.

echo ========================================
echo Done! View at: https://github.com/Arunkumar-1129/amd--cortexdesk
echo ========================================
pause
