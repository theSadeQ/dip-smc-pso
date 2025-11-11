@echo off
REM Checkpoint Task Launcher - Windows Batch File
REM
REM Usage:
REM   1. Double-click this file to launch with GUI prompts
REM   2. Or use command line:
REM      launch-checkpoint-task.bat LT-4 agent1 "Theory Specialist" "Your prompt"
REM

setlocal enabledelayedexpansion

REM Check if running from project root
if not exist ".project\dev_tools\launch_checkpoint_task.py" (
    echo [ERROR] Must run from project root directory
    echo [INFO] Current directory: %cd%
    echo.
    echo Please navigate to: D:\Projects\main
    echo Then try again.
    pause
    exit /b 1
)

REM If no arguments provided, show interactive mode
if "%1"=="" (
    cls
    echo.
    echo ===============================================
    echo   Checkpoint Task Launcher - Interactive Mode
    echo ===============================================
    echo.

    set /p TASK_ID="Enter Task ID (e.g., LT-4, MT-6): "
    if "!TASK_ID!"=="" (
        echo [ERROR] Task ID required
        pause
        exit /b 1
    )

    set /p AGENT_ID="Enter Agent ID (e.g., agent1_theory): "
    if "!AGENT_ID!"=="" (
        echo [ERROR] Agent ID required
        pause
        exit /b 1
    )

    set /p ROLE="Enter Agent Role (e.g., Theory Specialist): "
    if "!ROLE!"=="" (
        echo [ERROR] Agent Role required
        pause
        exit /b 1
    )

    set /p DESCRIPTION="Enter Task Description (e.g., Derive Lyapunov proofs): "
    if "!DESCRIPTION!"=="" (
        echo [ERROR] Task Description required
        pause
        exit /b 1
    )

    echo.
    echo Enter your full prompt (can be multiple lines).
    echo When done, type DONE on a new line:
    echo.
    set PROMPT_TEXT=
    :prompt_loop
    set /p PROMPT_LINE=">> "
    if /i "!PROMPT_LINE!"=="DONE" goto prompt_done
    if "!PROMPT_TEXT!"=="" (
        set PROMPT_TEXT=!PROMPT_LINE!
    ) else (
        set PROMPT_TEXT=!PROMPT_TEXT! !PROMPT_LINE!
    )
    goto prompt_loop

    :prompt_done
    if "!PROMPT_TEXT!"=="" (
        echo [ERROR] Prompt required
        pause
        exit /b 1
    )

) else (
    REM Command-line arguments provided
    set TASK_ID=%1
    set AGENT_ID=%2
    set ROLE=%3
    set DESCRIPTION=%3
    set PROMPT_TEXT=%4
)

REM Launch the task
cls
echo.
echo ===============================================
echo   Launching Checkpoint Task
echo ===============================================
echo.
echo Task ID:     !TASK_ID!
echo Agent ID:    !AGENT_ID!
echo Role:        !ROLE!
echo Description: !DESCRIPTION!
echo.
echo Launching in 2 seconds...
timeout /t 2 /nobreak

python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task !TASK_ID! ^
    --agent !AGENT_ID! ^
    --role "!ROLE!" ^
    --description "!DESCRIPTION!" ^
    --prompt "!PROMPT_TEXT!"

echo.
echo ===============================================
echo   Task Launch Complete
echo ===============================================
echo.
echo Recovery command (if needed):
echo   /resume !TASK_ID! !AGENT_ID!
echo.
pause
