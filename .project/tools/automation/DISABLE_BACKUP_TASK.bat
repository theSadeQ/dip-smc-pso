@echo off
echo Unregistering ClaudeCodeAutoBackup scheduled task...
schtasks /Delete /TN "ClaudeCodeAutoBackup" /F
if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: Scheduled task has been deleted.
    echo The CMD window will no longer appear every minute.
) else (
    echo.
    echo WARNING: Task may not exist or already deleted.
    echo Error code: %ERRORLEVEL%
)
echo.
pause
