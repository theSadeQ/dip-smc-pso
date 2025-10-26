#!/bin/bash
# Master launcher for all Chapter 5 experiments (BASH version)
# Launches all experiments in parallel (background processes)
# Estimated total time: ~10 hours parallelized

echo "================================================================================"
echo "CHAPTER 5 EXPERIMENTS - MASTER LAUNCHER"
echo "================================================================================"
echo ""
echo "This script will launch ALL experiments in parallel:"
echo "  1. PSO (10 runs, seeds 42-2526)"
echo "  2. Grid Search (30x30 = 900 evaluations)"
echo "  3. Random Search (600 samples)"
echo ""
echo "Estimated time: 10 hours (parallelized) or 82 hours (serial)"
echo ""
echo "WARNING: This will consume significant CPU resources!"
echo ""
echo "Press Ctrl+C within 5 seconds to cancel..."
sleep 5

# Create results directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
mkdir -p "$RESULTS_DIR"

echo ""
echo "================================================================================"
echo "LAUNCHING EXPERIMENTS"
echo "================================================================================"

# Launch 10 PSO runs in background
echo ""
echo "[1/3] Launching PSO optimization (10 runs)..."
for seed in 42 123 456 789 1011 1314 1617 1920 2223 2526; do
    echo "  - Launching PSO with seed $seed (background process)"
    python "$SCRIPT_DIR/optimize_pso_single_run.py" \
        --seed $seed \
        --output "$RESULTS_DIR/results_seed${seed}.json" \
        --skip-validation \
        > "$RESULTS_DIR/pso_seed${seed}.log" 2>&1 &
done

echo "  [OK] 10 PSO processes launched"

# Launch grid search in background
echo ""
echo "[2/3] Launching grid search (30x30 = 900 evaluations)..."
python "$SCRIPT_DIR/run_grid_search.py" \
    --n-grid 30 \
    --n-processes 12 \
    > "$RESULTS_DIR/grid_search.log" 2>&1 &

echo "  [OK] Grid search launched"

# Launch random search in background
echo ""
echo "[3/3] Launching random search (600 samples)..."
python "$SCRIPT_DIR/run_random_search.py" \
    --n-samples 600 \
    --seed 42 \
    > "$RESULTS_DIR/random_search.log" 2>&1 &

echo "  [OK] Random search launched"

echo ""
echo "================================================================================"
echo "ALL EXPERIMENTS LAUNCHED SUCCESSFULLY"
echo "================================================================================"
echo ""
echo "Background processes: $(jobs -p | wc -l)"
echo "Results directory: $RESULTS_DIR"
echo ""
echo "MONITORING COMMANDS:"
echo "  - Check completed PSO runs: ls -1 $RESULTS_DIR/results_seed*.json | wc -l"
echo "  - View PSO log (seed 42): tail -f $RESULTS_DIR/pso_seed42.log"
echo "  - View grid search log: tail -f $RESULTS_DIR/grid_search.log"
echo "  - View random search log: tail -f $RESULTS_DIR/random_search.log"
echo "  - Check all background jobs: jobs"
echo ""
echo "Expected completion: ~10 hours from now"
echo "You can safely close this terminal - processes will continue running."
echo ""
echo "================================================================================"
