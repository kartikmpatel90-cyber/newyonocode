@echo off
color 0A
echo ========================================================
echo        EP CODE AUTOMATIC WEBSITE UPDATER
echo ========================================================
echo.

:: Configure Git silently so it doesn't throw errors
git config --global user.name "Kartik"
git config --global user.email "kartik@example.com"

if not exist .git (
    echo Setting up auto-update for the first time...
    git init
    git branch -m main
    
    :ask_url
    echo.
    echo Please enter your GitHub Repository URL 
    echo Example: https://github.com/yourusername/yonosite.git
    set /p repo_url="Repository URL: "
    if "%repo_url%"=="" goto ask_url
    
    git remote add origin "%repo_url%"
    echo Successfully connected to your repository!
    echo.
)

echo Scanning for new images and code updates...
git add .

echo.
echo Saving updates...
git commit -m "Auto-update website from computer"

echo.
echo Uploading directly to GitHub...
git push -u origin main

echo.
echo ========================================================
echo        UPDATE COMPLETE!
echo        Your live website will refresh in a few minutes!
echo ========================================================
pause
