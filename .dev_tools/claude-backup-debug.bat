@echo off
REM Debug wrapper for Task Scheduler

echo ========================================  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo Task Scheduler Run: %DATE% %TIME%      >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo ========================================  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo.                                         >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo Current Directory: %CD%                  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo User: %USERNAME%                         >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo PATH: %PATH%                             >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo.                                         >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log

REM Change to repo directory
cd /d D:\Projects\main

REM Run PowerShell backup script (using full path)
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\Projects\main\.dev_tools\claude-backup.ps1  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log 2>&1

echo.                                         >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo Exit Code: %ERRORLEVEL%                  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
echo ========================================  >> D:\Projects\main\.dev_tools\backup\task_scheduler_debug.log
