@echo off
REM Quick Recovery Script for Multi-Account Sessions
REM ==================================================
REM
REM Usage: Double-click this file when starting a new session
REM        Or run from command line: quick_recovery.bat

echo.
echo ========================================
echo MULTI-ACCOUNT SESSION RECOVERY
echo ========================================
echo.

REM Check if we're in the project root
if not exist ".project\dev_tools" (
    echo [ERROR] Please run this script from the project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [STEP 1] Running project recovery script...
echo.
bash .project\dev_tools\recover_project.sh
echo.

echo [STEP 2] Analyzing checkpoint status...
echo.
python .project\dev_tools\analyze_checkpoints.py
echo.

echo ========================================
echo RECOVERY COMPLETE
echo ========================================
echo.
echo Next steps:
echo   1. Review the output above
echo   2. Check "REAL INCOMPLETE AGENTS" section
echo   3. If incomplete agents found, verify against git history
echo   4. Ask Claude: "What should I resume based on this output?"
echo.
echo For detailed recovery instructions, see:
echo   .project\dev_tools\MULTI_ACCOUNT_RECOVERY_GUIDE.md
echo.
pause
