@echo off
REM Fix Task Scheduler working directory issue

echo Deleting existing task...
schtasks /Delete /TN "ClaudeCode-AutoBackup" /F 2>nul

echo.
echo Creating task with correct working directory...
schtasks /Create ^
 /TN "ClaudeCode-AutoBackup" ^
 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -Command \"Set-Location 'D:\Projects\main'; & '.\\.dev_tools\\claude-backup.ps1'\"" ^
 /SC MINUTE ^
 /MO 1 ^
 /RL LIMITED ^
 /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Task registered with working directory fix!
    echo.
    echo Testing task now...
    schtasks /Run /TN "ClaudeCode-AutoBackup"
    echo.
    echo Waiting 10 seconds for task to complete...
    timeout /t 10 /nobreak >nul
    echo.
    echo Checking result...
    schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST | findstr /C:"Last Result"
    echo.
) else (
    echo.
    echo [ERROR] Failed to create task
)

pause
