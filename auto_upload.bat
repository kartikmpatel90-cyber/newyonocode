@echo off
color 0A
echo ========================================================
echo        NEWYONO CODE AUTOMATIC WEBSITE UPDATER
echo ========================================================
echo.

:: Configure Git silently
"C:\Program Files\Git\bin\git.exe" config --global user.name "Kartik"
"C:\Program Files\Git\bin\git.exe" config --global user.email "kartik@example.com"

:: Ensure git is initialized
if not exist .git (
    "C:\Program Files\Git\bin\git.exe" init
    "C:\Program Files\Git\bin\git.exe" branch -m main
)

:: Automatically set the correct GitHub URL
"C:\Program Files\Git\bin\git.exe" remote remove origin 2>nul
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/kartikmpatel90-cyber/newyonocode.git

echo Scanning for new images and code updates...
"C:\Program Files\Git\bin\git.exe" add .

echo.
echo Saving updates...
"C:\Program Files\Git\bin\git.exe" commit -m "Auto-update website from computer"

echo.
echo Uploading directly to GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main --force



echo.
echo ========================================================
echo        UPDATE COMPLETE!
echo        Your live website will refresh in a few minutes!
echo ========================================================
pause
