@echo off
REM ==========================================================================================
REM Register Claude Code Auto-Backup Task Scheduler Job
REM ==========================================================================================
REM
REM This script registers a Windows Task Scheduler job that runs every 1 minute
REM to automatically backup your repository changes.
REM
REM Usage: Run this batch file as administrator (or as current user)
REM ==========================================================================================

echo.
echo ========================================
echo Claude Code Auto-Backup Registration
echo ========================================
echo.

REM Delete existing task if present
echo [1/3] Removing existing task (if any)...
schtasks /Delete /TN "ClaudeCode-AutoBackup" /F 2>nul
echo.

REM Create new scheduled task (every 1 minute)
echo [2/3] Creating new scheduled task...
schtasks /Create ^
 /TN "ClaudeCode-AutoBackup" ^
 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Projects\main\.dev_tools\claude-backup.ps1" ^
 /SC MINUTE ^
 /MO 1 ^
 /RL LIMITED ^
 /F ^
 /RU "%USERNAME%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [3/3] Task registered successfully!
    echo.
    echo ========================================
    echo Next Steps:
    echo ========================================
    echo 1. Task will run automatically every 1 minute
    echo 2. First backup will occur in ~1 minute
    echo 3. Monitor logs at: .dev_tools\backup\backup.log
    echo.
    echo To test immediately, run:
    echo   schtasks /Run /TN "ClaudeCode-AutoBackup"
    echo.
    echo To check status:
    echo   schtasks /Query /TN "ClaudeCode-AutoBackup" /V /FO LIST
    echo.
    echo To unregister:
    echo   schtasks /Delete /TN "ClaudeCode-AutoBackup" /F
    echo ========================================
) else (
    echo.
    echo [ERROR] Failed to register task!
    echo.
    echo Possible solutions:
    echo 1. Run this script with administrator privileges
    echo 2. Verify PowerShell execution policy allows scripts
    echo 3. Check that the backup script exists at:
    echo    D:\Projects\main\.dev_tools\claude-backup.ps1
    echo.
)

echo.
pause
