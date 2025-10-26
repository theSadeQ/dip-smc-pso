@echo off
REM Recreate Task Scheduler without password issues

echo ========================================
echo Recreating Task Scheduler Job
echo ========================================
echo.

REM Delete existing task
echo [1/2] Deleting existing task...
schtasks /Delete /TN "ClaudeCode-AutoBackup" /F 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   Task deleted successfully
) else (
    echo   No existing task found (OK)
)
echo.

REM Create new task using debug wrapper
echo [2/2] Creating new task with debug wrapper...
schtasks /Create ^
 /TN "ClaudeCode-AutoBackup" ^
 /TR "cmd.exe /c D:\Projects\main\.dev_tools\claude-backup-debug.bat" ^
 /SC MINUTE ^
 /MO 1 ^
 /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Task created successfully!
    echo.
    echo The task will now run every 1 minute.
    echo Debug logs will be written to:
    echo   D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
    echo.
    echo Testing task now...
    schtasks /Run /TN "ClaudeCode-AutoBackup"
    echo.
    echo Waiting 10 seconds...
    timeout /t 10 /nobreak >nul
    echo.
    echo Checking debug log...
    echo ========================================
    type D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
    echo ========================================
) else (
    echo.
    echo [ERROR] Failed to create task
    echo Error code: %ERRORLEVEL%
)

echo.
pause
