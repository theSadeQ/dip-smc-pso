@echo off
REM Master launcher for all Chapter 5 experiments
REM Launches all experiments in parallel (background processes)
REM Estimated total time: ~10 hours parallelized

echo ================================================================================
echo CHAPTER 5 EXPERIMENTS - MASTER LAUNCHER
echo ================================================================================
echo.
echo This script will launch ALL experiments in parallel:
echo   1. PSO (10 runs, seeds 42-2526)
echo   2. Grid Search (30x30 = 900 evaluations)
echo   3. Random Search (600 samples)
echo.
echo Estimated time: 10 hours (parallelized) or 82 hours (serial)
echo.
echo WARNING: This will consume significant CPU resources!
echo Press Ctrl+C to cancel, or
pause

set OUTPUT_DIR=.artifacts\LT7_research_paper\experiments\results
mkdir %OUTPUT_DIR% 2>nul

echo.
echo ================================================================================
echo EXPERIMENT 1: PSO Optimization (10 runs)
echo ================================================================================
echo.

REM Launch 10 PSO runs in sequence (can't easily parallelize in batch on Windows)
for %%s in (42 123 456 789 1011 1314 1617 1920 2223 2526) do (
    echo [SEED %%s] Starting PSO optimization...
    start /B python .artifacts\LT7_research_paper\experiments\optimize_pso_single_run.py --seed %%s --output "%OUTPUT_DIR%\results_seed%%s.json" --skip-validation
)

echo [INFO] Launched 10 PSO runs in background
echo.

echo ================================================================================
echo EXPERIMENT 2: Grid Search (30x30 = 900 evaluations)
echo ================================================================================
echo.

start /B python .artifacts\LT7_research_paper\experiments\run_grid_search.py --n-grid 30 --n-processes 12 --output "%OUTPUT_DIR%\grid_search.json"
echo [INFO] Launched grid search in background
echo.

echo ================================================================================
echo EXPERIMENT 3: Random Search (600 samples)
echo ================================================================================
echo.

start /B python .artifacts\LT7_research_paper\experiments\run_random_search.py --n-samples 600 --output "%OUTPUT_DIR%\random_search.json"
echo [INFO] Launched random search in background
echo.

echo ================================================================================
echo ALL EXPERIMENTS LAUNCHED
echo ================================================================================
echo.
echo All experiments are now running in the background.
echo.
echo Monitor progress by checking:
echo   - %OUTPUT_DIR%\results_seed*.json (PSO runs)
echo   - %OUTPUT_DIR%\grid_search.json (Grid search)
echo   - %OUTPUT_DIR%\random_search.json (Random search)
echo.
echo Expected completion: Check back in ~10 hours
echo.
echo To monitor CPU usage: Open Task Manager (Ctrl+Shift+Esc)
echo.
echo ================================================================================
pause
