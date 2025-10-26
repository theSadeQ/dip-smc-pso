@echo off
REM Batch PSO runner for 10 seeds
REM Outputs: results_seed{42,123,...}.json

setlocal enabledelayedexpansion

set SEEDS=42 123 456 789 1011 1314 1617 1920 2223 2526
set OUTPUT_DIR=.artifacts\LT7_research_paper\experiments\results

echo [INFO] Starting batch PSO optimization with 10 seeds...
echo [INFO] Output directory: %OUTPUT_DIR%

for %%s in (%SEEDS%) do (
    echo.
    echo [SEED %%s] Running PSO optimization...
    python optimize_adaptive_boundary.py --seed %%s --output "%OUTPUT_DIR%\results_seed%%s.json"

    if errorlevel 1 (
        echo [ERROR] PSO run failed for seed %%s
    ) else (
        echo [SUCCESS] Completed seed %%s
    )
)

echo.
echo [INFO] All PSO runs completed. Results saved to %OUTPUT_DIR%
echo [INFO] Next step: Run aggregate_pso_stats.py to generate Table II

pause
