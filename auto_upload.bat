@echo off
color 0A
echo ========================================================
echo        EP CODE AUTOMATIC WEBSITE UPDATER
echo ========================================================
echo.

:: Configure Git silently
git config --global user.name "Kartik"
git config --global user.email "kartik@example.com"

:: Ensure git is initialized
if not exist .git (
    git init
    git branch -m main
)

:: Automatically set the correct GitHub URL so you never have to type it!
git remote remove origin 2>nul
git remote add origin https://github.com/kartikmpatel90-cyber/earn-telegram-site.git

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
