# Experiment Recovery Guide

## If Claude Code Session Ends

**DON'T PANIC!** Experiments are running with nohup and will continue.

### Check Status

```bash
bash check_experiment_status.sh
```

### View Live Logs

```bash
# PSO logs
tail -f .artifacts/LT7_research_paper/experiments/results/pso_seed42.log

# Grid search
tail -f .artifacts/LT7_research_paper/experiments/results/grid_search.log

# Random search
tail -f .artifacts/LT7_research_paper/experiments/results/random_search.log
```

### Stop All Experiments

```bash
cat .artifacts/LT7_research_paper/experiments/results/experiment_pids.txt | xargs kill -TERM
```

### Restart Failed Experiments

```bash
# Check which PSO runs completed
ls .artifacts/LT7_research_paper/experiments/results/results_seed*.json

# Manually relaunch missing seeds (example for seed 789)
cd .artifacts/LT7_research_paper/experiments
nohup python optimize_pso_single_run.py \
    --seed 789 \
    --output results/results_seed789.json \
    --skip-validation \
    > results/pso_seed789.log 2>&1 &
```

### When All Complete

```bash
# Check completion
bash check_experiment_status.sh

# If all done, proceed to Phase 4 (data extraction)
cd .artifacts/LT7_research_paper/data_extraction
python generate_table2_pso_statistics.py
python generate_table3_method_comparison.py
python generate_figure4_pso_convergence.py
```

---

## Process Independence Verification

To verify experiments survive terminal closure:

```bash
# List all experiment processes
ps -ef | grep -E "optimize_pso|run_grid|run_random" | grep -v grep

# Close terminal, open new one, run same command
# Processes should still be listed
```

---

## Log File Locations

All logs are in: `.artifacts/LT7_research_paper/experiments/results/`

- `pso_seed42.log`, `pso_seed123.log`, ... (10 PSO logs)
- `grid_search.log`
- `random_search.log`

---

## Expected Timeline

- **PSO (10 runs)**: ~5-6 hours (30 iterations each)
- **Grid Search**: ~3-4 hours (30×30 = 900 evaluations)
- **Random Search**: ~1 hour (600 samples)

**Total**: ~10 hours (runs in parallel, so max of above)

---

## Completion Criteria

All experiments complete when:

1. **10 PSO result files exist**: `results_seed42.json`, `results_seed123.json`, etc.
2. **Grid search complete**: `grid_search_results.json` exists
3. **Random search complete**: `random_search_results.json` exists
4. **All processes terminated**: `check_experiment_status.sh` shows 0/12 running

---

## Next Steps After Completion

Once all experiments complete:

1. **Verify results**: `bash check_experiment_status.sh` (should show all complete)
2. **Generate Table 2**: PSO statistics across 10 runs
3. **Generate Table 3**: Method comparison (PSO vs Grid vs Random)
4. **Generate Figure 4**: PSO convergence curves
5. **Incorporate into Chapter 5**: Copy LaTeX tables/figures to thesis

**Estimated time for Phase 4**: 30-60 minutes (mostly automated)
