#!/bin/bash
# Check status of nohup experiments

# Determine script location and set paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/results/experiment_pids.txt"
RESULTS_DIR="$SCRIPT_DIR/results"

if [ ! -f "$PID_FILE" ]; then
    echo "No experiments running (PID file not found)"
    exit 1
fi

echo "================================================================================"
echo "EXPERIMENT STATUS CHECK"
echo "================================================================================"
echo ""

# Count running processes
total_pids=$(wc -l < "$PID_FILE")
running_pids=$(cat "$PID_FILE" | xargs ps -p 2>/dev/null | grep -v PID | wc -l)

echo "Processes: $running_pids / $total_pids running"
echo ""

# Check each category
pso_running=$(ps -ef | grep "optimize_pso_single_run" | grep -v grep | wc -l)
grid_running=$(ps -ef | grep "run_grid_search" | grep -v grep | wc -l)
random_running=$(ps -ef | grep "run_random_search" | grep -v grep | wc -l)

echo "  - PSO runs: $pso_running / 10"
echo "  - Grid search: $grid_running / 1"
echo "  - Random search: $random_running / 1"
echo ""

# Check completion
completed_pso=$(ls "$RESULTS_DIR"/results_seed*.json 2>/dev/null | wc -l)
echo "Completed PSO runs: $completed_pso / 10"

if [ -f "$RESULTS_DIR/grid_search_results.json" ]; then
    echo "Grid search: COMPLETE ✓"
fi

if [ -f "$RESULTS_DIR/random_search_results.json" ]; then
    echo "Random search: COMPLETE ✓"
fi

echo ""
echo "================================================================================"

# If all done
if [ $completed_pso -eq 10 ] && [ -f "$RESULTS_DIR/grid_search_results.json" ] && [ -f "$RESULTS_DIR/random_search_results.json" ]; then
    echo "ALL EXPERIMENTS COMPLETE! Proceed to Phase 4 (generate tables/figures)"
fi
