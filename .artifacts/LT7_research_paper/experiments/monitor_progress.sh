#!/bin/bash
# Monitor progress of Chapter 5 experiments
# Usage: bash monitor_progress.sh

RESULTS_DIR=".artifacts/LT7_research_paper/experiments/results"

echo "================================================================================"
echo "CHAPTER 5 EXPERIMENTS - PROGRESS MONITOR"
echo "================================================================================"
echo ""
echo "Timestamp: $(date)"
echo ""

# PSO Progress
echo "--- PSO OPTIMIZATION (10 runs) ---"
completed=$(ls -1 $RESULTS_DIR/results_seed*.json 2>/dev/null | wc -l)
echo "Completed runs: $completed / 10"

if [ $completed -gt 0 ]; then
    echo ""
    echo "Completed seeds:"
    for f in $RESULTS_DIR/results_seed*.json; do
        if [ -f "$f" ]; then
            seed=$(basename "$f" | sed 's/results_seed\([0-9]*\)\.json/\1/')
            size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null)
            echo "  - Seed $seed ($(echo "scale=1; $size/1024" | bc)KB)"
        fi
    done
fi

echo ""
echo "Active PSO runs (check log timestamps):"
for seed in 42 123 456 789 1011 1314 1617 1920 2223 2526; do
    logfile="$RESULTS_DIR/pso_seed${seed}.log"
    if [ -f "$logfile" ]; then
        lastline=$(tail -1 "$logfile" 2>/dev/null)
        if echo "$lastline" | grep -q "pyswarms"; then
            echo "  - Seed $seed: RUNNING ($(wc -l < "$logfile") log lines)"
        elif echo "$lastline" | grep -q "Saved results"; then
            echo "  - Seed $seed: COMPLETE ✓"
        else
            echo "  - Seed $seed: In progress... ($(wc -l < "$logfile") log lines)"
        fi
    else
        echo "  - Seed $seed: NOT STARTED"
    fi
done

echo ""
echo "--- GRID SEARCH (30x30 = 900 evaluations) ---"
if [ -f "$RESULTS_DIR/grid_search_results.json" ]; then
    size=$(stat -f%z "$RESULTS_DIR/grid_search_results.json" 2>/dev/null || stat -c%s "$RESULTS_DIR/grid_search_results.json" 2>/dev/null)
    echo "Status: COMPLETE ✓ ($(echo "scale=1; $size/1024" | bc)KB)"
elif [ -f "$RESULTS_DIR/grid_search.log" ]; then
    lines=$(wc -l < "$RESULTS_DIR/grid_search.log")
    echo "Status: Running ($lines log lines)"
    tail -3 "$RESULTS_DIR/grid_search.log" 2>/dev/null | head -1
else
    echo "Status: NOT STARTED"
fi

echo ""
echo "--- RANDOM SEARCH (600 samples) ---"
if [ -f "$RESULTS_DIR/random_search_results.json" ]; then
    size=$(stat -f%z "$RESULTS_DIR/random_search_results.json" 2>/dev/null || stat -c%s "$RESULTS_DIR/random_search_results.json" 2>/dev/null)
    echo "Status: COMPLETE ✓ ($(echo "scale=1; $size/1024" | bc)KB)"
elif [ -f "$RESULTS_DIR/random_search.log" ]; then
    lines=$(wc -l < "$RESULTS_DIR/random_search.log")
    echo "Status: Running ($lines log lines)"
    tail -3 "$RESULTS_DIR/random_search.log" 2>/dev/null | head -1
else
    echo "Status: NOT STARTED"
fi

echo ""
echo "--- DISK USAGE ---"
total_size=$(du -sh $RESULTS_DIR 2>/dev/null | cut -f1)
echo "Results directory: $total_size"

echo ""
echo "--- ESTIMATED COMPLETION ---"
if [ $completed -eq 10 ] && [ -f "$RESULTS_DIR/grid_search_results.json" ] && [ -f "$RESULTS_DIR/random_search_results.json" ]; then
    echo "ALL EXPERIMENTS COMPLETE! ✓✓✓"
    echo ""
    echo "Next steps:"
    echo "  1. Generate tables: cd .artifacts/LT7_research_paper/data_extraction"
    echo "  2. Run: python generate_table2_pso_statistics.py"
    echo "  3. Run: python generate_table3_method_comparison.py"
    echo "  4. Run: python generate_figure4_pso_convergence.py"
else
    # Estimate completion based on current progress
    elapsed_mins=$(($(date +%s) - $(stat -f%m "$RESULTS_DIR" 2>/dev/null || stat -c%Y "$RESULTS_DIR")))
    elapsed_mins=$((elapsed_mins / 60))

    if [ $completed -gt 0 ]; then
        avg_time_per_pso=$((elapsed_mins / completed))
        remaining_pso=$((10 - completed))
        est_remaining=$(($remaining_pso * $avg_time_per_pso))

        echo "Elapsed: ${elapsed_mins} minutes"
        echo "Estimated remaining: ~${est_remaining} minutes (~$((est_remaining / 60)) hours)"
    else
        echo "Estimated total: ~10 hours (600 minutes)"
    fi
fi

echo ""
echo "================================================================================"
echo "To view live logs:"
echo "  tail -f $RESULTS_DIR/pso_seed42.log"
echo "  tail -f $RESULTS_DIR/grid_search.log"
echo "  tail -f $RESULTS_DIR/random_search.log"
echo "================================================================================"
