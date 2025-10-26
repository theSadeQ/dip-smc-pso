#!/bin/bash
# Nohup-compatible launcher for Chapter 5 experiments
# Processes survive terminal/session termination

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
PID_FILE="$RESULTS_DIR/experiment_pids.txt"

mkdir -p "$RESULTS_DIR"
rm -f "$PID_FILE"  # Clear old PID file

echo "================================================================================"
echo "CHAPTER 5 EXPERIMENTS - NOHUP LAUNCHER (Session-Independent)"
echo "================================================================================"
echo ""
echo "Launching 10 PSO + Grid + Random (total: 12 processes)"
echo "Processes will continue running even if this terminal/session ends."
echo ""
echo "Press Ctrl+C within 5 seconds to cancel..."
sleep 5

# Launch 10 PSO runs with nohup
echo ""
echo "[1/3] Launching PSO optimization (10 runs with nohup)..."
for seed in 42 123 456 789 1011 1314 1617 1920 2223 2526; do
    nohup python "$SCRIPT_DIR/optimize_pso_single_run.py" \
        --seed $seed \
        --output "$RESULTS_DIR/results_seed${seed}.json" \
        --skip-validation \
        > "$RESULTS_DIR/pso_seed${seed}.log" 2>&1 &

    echo $! >> "$PID_FILE"  # Save PID
    echo "  - PSO seed $seed launched (PID: $!)"
done

# Launch grid search with nohup (FIXED PARAMETER)
echo ""
echo "[2/3] Launching grid search with nohup..."
nohup python "$SCRIPT_DIR/run_grid_search.py" \
    --n-grid 30 \
    --n-processes 12 \
    > "$RESULTS_DIR/grid_search.log" 2>&1 &

echo $! >> "$PID_FILE"
echo "  - Grid search launched (PID: $!)"

# Launch random search with nohup
echo ""
echo "[3/3] Launching random search with nohup..."
nohup python "$SCRIPT_DIR/run_random_search.py" \
    --n-samples 600 \
    --seed 42 \
    > "$RESULTS_DIR/random_search.log" 2>&1 &

echo $! >> "$PID_FILE"
echo "  - Random search launched (PID: $!)"

echo ""
echo "================================================================================"
echo "ALL EXPERIMENTS LAUNCHED WITH NOHUP"
echo "================================================================================"
echo ""
echo "PIDs saved to: $PID_FILE"
echo "Results directory: $RESULTS_DIR"
echo ""
echo "MONITORING COMMANDS:"
echo "  - Check running processes: cat $PID_FILE | xargs ps -p"
echo "  - View PSO log: tail -f $RESULTS_DIR/pso_seed42.log"
echo "  - View grid log: tail -f $RESULTS_DIR/grid_search.log"
echo "  - View random log: tail -f $RESULTS_DIR/random_search.log"
echo "  - Check progress: bash check_experiment_status.sh"
echo ""
echo "TO STOP ALL EXPERIMENTS:"
echo "  cat $PID_FILE | xargs kill -TERM"
echo ""
echo "You can now safely close this terminal. Experiments will continue."
echo "================================================================================"
