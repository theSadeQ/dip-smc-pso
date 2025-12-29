@echo off
REM Quick Template for Checkpoint Task Launcher
REM
REM INSTRUCTIONS:
REM 1. Edit this file in Notepad
REM 2. Fill in the YOUR_* sections below with your task details
REM 3. Save the file
REM 4. Double-click to launch your task with checkpointing!
REM
REM Variables to change:
REM   YOUR_TASK_ID       - e.g., LT-4, MT-6, QW-1
REM   YOUR_AGENT_ID      - e.g., agent1_theory, agent1_pso
REM   YOUR_ROLE          - e.g., Theory Specialist, PSO Engineer
REM   YOUR_DESCRIPTION   - e.g., Derive Lyapunov proofs, Optimize PSO
REM   YOUR_PROMPT        - Your full prompt for the agent
REM

setlocal enabledelayedexpansion

REM EDIT THESE VALUES
set TASK_ID=YOUR_TASK_ID
set AGENT_ID=YOUR_AGENT_ID
set ROLE=YOUR_ROLE
set DESCRIPTION=YOUR_DESCRIPTION
set PROMPT_TEXT=YOUR_PROMPT

REM Validate
if "!TASK_ID!"=="YOUR_TASK_ID" (
    echo [ERROR] Please edit this file and fill in the task details
    echo.
    echo Open this file in Notepad and change:
    echo   YOUR_TASK_ID - Task identifier
    echo   YOUR_AGENT_ID - Agent identifier
    echo   YOUR_ROLE - Agent role
    echo   YOUR_DESCRIPTION - Task description
    echo   YOUR_PROMPT - Full prompt for agent
    echo.
    pause
    exit /b 1
)

REM Launch
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task !TASK_ID! ^
    --agent !AGENT_ID! ^
    --role "!ROLE!" ^
    --description "!DESCRIPTION!" ^
    --prompt "!PROMPT_TEXT!"

echo.
echo Task completed. Press any key to close...
pause
