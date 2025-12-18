@echo off
REM Example Checkpoint Task Launches
REM
REM Pick one of the examples below and modify it for your needs.
REM Then save it as a new .bat file and double-click to run!
REM

setlocal enabledelayedexpansion

cls
echo.
echo ================================================
echo   Checkpoint Task Launch Examples
echo ================================================
echo.
echo Choose an example to launch:
echo.
echo [1] Lyapunov Proof Theory Work (LT-4)
echo [2] PSO Optimization (MT-6)
echo [3] Research Paper Writing (LT-7)
echo [4] Data Analysis (MT-7)
echo [5] Custom Task (Interactive)
echo.

set /p CHOICE="Enter your choice (1-5): "

if "!CHOICE!"=="1" (
    call :launch_lt4
) else if "!CHOICE!"=="2" (
    call :launch_mt6
) else if "!CHOICE!"=="3" (
    call :launch_lt7
) else if "!CHOICE!"=="4" (
    call :launch_mt7
) else if "!CHOICE!"=="5" (
    call ".project\dev_tools\launch-checkpoint-task.bat"
) else (
    echo [ERROR] Invalid choice
    pause
    exit /b 1
)

goto end

REM ================================================
REM Example 1: Lyapunov Proof Theory Work (LT-4)
REM ================================================
:launch_lt4
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task LT-4 ^
    --agent agent1_theory ^
    --role "Lyapunov Proof Specialist" ^
    --description "Derive Lyapunov stability proofs for 5 controllers" ^
    --prompt "Analyze the 5 SMC controllers (Classical, STA, Adaptive, Hybrid Adaptive STA, Swing-Up) and derive complete, mathematically rigorous Lyapunov stability proofs for each. Output should be peer-review ready with all assumptions clearly stated."
goto show_recovery

REM ================================================
REM Example 2: PSO Optimization (MT-6)
REM ================================================
:launch_mt6
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task MT-6 ^
    --agent agent1_pso ^
    --role "PSO Optimization Engineer" ^
    --description "Optimize PSO parameters for Classical SMC controller" ^
    --prompt "Run comprehensive PSO optimization for the Classical SMC controller with objectives: 1. Minimize steady-state chattering 2. Maintain fast system response (< 2 seconds) 3. Keep control gains within reasonable bounds. Generate detailed benchmark results with 5+ performance metrics."
goto show_recovery

REM ================================================
REM Example 3: Research Paper Writing (LT-7)
REM ================================================
:launch_lt7
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task LT-7 ^
    --agent agent1_paper ^
    --role "Research Paper Specialist" ^
    --description "Write comprehensive research paper on SMC optimization" ^
    --prompt "Based on controller benchmarks, theoretical analysis, and PSO optimization results, write a publication-ready research paper including: title and abstract, introduction, methodology, comprehensive benchmark results with 14+ figures, statistical analysis, conclusions, and complete bibliography. Follow IEEE Transactions format."
goto show_recovery

REM ================================================
REM Example 4: Data Analysis (MT-7)
REM ================================================
:launch_mt7
python ".project\dev_tools\launch_checkpoint_task.py" ^
    --task MT-7 ^
    --agent agent1_analysis ^
    --role "Data Science Analyst" ^
    --description "Analyze benchmark results and create statistics" ^
    --prompt "Analyze the comprehensive benchmark results from all 5 SMC controllers. Create detailed statistical analysis including: performance metrics comparison, confidence intervals, ANOVA tests, correlation analysis, and visual representations. Generate executive summary with key findings and recommendations."
goto show_recovery

REM ================================================
REM Show Recovery Command
REM ================================================
:show_recovery
echo.
echo ================================================
echo   If interrupted, use:
echo ================================================
echo.
echo   /recover
echo.
echo   Then:
echo.
echo   /resume [TASK_ID] [AGENT_ID]
echo.
pause
goto end

REM ================================================
REM End
REM ================================================
:end
