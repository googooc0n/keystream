@echo off
REM =============================================
REM Auto-commit & push all changes batch script
REM Repository: https://github.com/googooc0n/keystream
REM Usage: Double-click or run from command line
REM =============================================

:: Change to script directory (project root)
cd /d "%~dp0"

:: Add current directory to git safe list (handle dubious ownership)
git config --global --add safe.directory "%~dp0"

:: Ensure remote origin is set correctly
echo Setting remote origin to googooc0n/keystream...
git remote remove origin 2>nul
git remote add origin https://github.com/googooc0n/keystream.git

:: Stage all changes
echo Staging all changes...
git add .

:: Commit with timestamp message
echo Committing changes...
git commit -m "Auto commit %DATE% %TIME%" || echo "No changes to commit."

:: Push to main branch
echo Pushing to origin main...
git push -u origin main

echo.
echo Done. Press any key to exit.
pause
