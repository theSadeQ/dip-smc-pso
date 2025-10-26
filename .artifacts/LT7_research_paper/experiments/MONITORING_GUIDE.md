# Experiment Monitoring Guide

## Current Status (as of 08:25 AM)

**PSO Optimization (10 runs):**
- Seed 456: **Iteration 24/30 (80% complete!)** - Will finish first (~30 min)
- Seed 42: Iteration 9/30 (30% complete) - Typical progress
- Other 8 seeds: Various iterations (1-10/30)

**Random Search:**
- Progress: 300/600 samples (50% complete)
- Estimated completion: ~30-40 minutes

**Grid Search:**
- Status: FAILED (pickle error)
- Not critical for thesis (PSO is the main focus)

---

## Monitoring Methods

### Method 1: Quick Status Check (Recommended)

**Best for:** Quick overview of all experiments

```bash
# Run from anywhere in the project:
bash .artifacts/LT7_research_paper/experiments/check_experiment_status.sh
```

**What you'll see:**
```
================================================================================
EXPERIMENT STATUS CHECK
================================================================================

Processes: 11 / 12 running

  - PSO runs: 10 / 10
  - Grid search: 0 / 1
  - Random search: 1 / 1

Completed PSO runs: 0 / 10

================================================================================
```

**How often to run:** Every 30-60 minutes

---

### Method 2: Live Log Viewing (Detailed Progress)

**Best for:** Watching real-time PSO iterations

```bash
# Watch PSO seed 42 live (press Ctrl+C to exit):
tail -f .artifacts/LT7_research_paper/experiments/results/pso_seed42.log

# Watch random search live:
tail -f .artifacts/LT7_research_paper/experiments/results/random_search.log
```

**What you'll see:**
```
2025-10-20 08:23:15,389 - optimize_adaptive_boundary - INFO - Iteration 9/30: best_fitness=15.5520, best_params=[0.0015, 1.22]
2025-10-20 08:23:20,549 - optimize_adaptive_boundary - INFO - Particle 0: epsilon=0.0195, alpha=0.49 -> chattering=2.1324, ...
```

**How to exit:** Press `Ctrl+C` to stop viewing (experiments keep running)

---

### Method 3: Check Specific Run Progress

**Best for:** Checking which run is furthest along

```bash
# Check all PSO runs for latest iteration:
for seed in 42 123 456 789 1011 1314 1617 1920 2223 2526; do
    latest=$(grep -a "Iteration" .artifacts/LT7_research_paper/experiments/results/pso_seed${seed}.log 2>/dev/null | tail -1)
    echo "Seed $seed: $latest"
done
```

**What you'll see:**
```
Seed 42: Iteration 9/30: best_fitness=15.5520
Seed 123: Iteration 7/30: best_fitness=15.6012
Seed 456: Iteration 24/30: best_fitness=15.4216
...
```

---

### Method 4: Check Running Processes

**Best for:** Verifying experiments are still running

```bash
# Count running experiment processes:
ps -ef | grep -E "optimize_pso_single_run|run_random_search" | grep -v grep | wc -l
# Should output: 11 (10 PSO + 1 Random)

# See detailed process list:
ps -ef | grep -E "optimize_pso_single_run|run_random_search" | grep -v grep
```

---

### Method 5: Check Completion

**Best for:** Knowing when experiments are done

```bash
# Count completed PSO runs:
ls .artifacts/LT7_research_paper/experiments/results/results_seed*.json 2>/dev/null | wc -l
# Should be 0 while running, 10 when all PSO complete

# Check if random search finished:
ls .artifacts/LT7_research_paper/experiments/results/random_search_results.json 2>/dev/null
# File exists = complete
```

---

## Monitoring Schedule (Recommended)

**During work hours:**
1. **Every 30 minutes:** Run `check_experiment_status.sh`
2. **Every 2 hours:** Check detailed progress (Method 3)
3. **Before bed:** Run status check, note ETA

**Next morning:**
1. Run `check_experiment_status.sh`
2. If "ALL EXPERIMENTS COMPLETE" → proceed to data extraction
3. If still running → check ETA, come back later

---

## What to Look For

### Good Signs ✅
- `Processes: 11 / 12 running` (PSO + Random running)
- Log files growing (timestamps increasing)
- Iteration numbers incrementing
- Best fitness values decreasing (optimization working)

### Warning Signs ⚠️
- Process count drops (e.g., `Processes: 8 / 12 running`)
- Log files not updating (timestamps frozen)
- No new iterations after 10+ minutes

### What to Do if Process Dies
```bash
# 1. Check which seed failed
bash check_experiment_status.sh

# 2. Look for errors in log
tail -50 .artifacts/LT7_research_paper/experiments/results/pso_seed{FAILED_SEED}.log

# 3. Relaunch manually
cd .artifacts/LT7_research_paper/experiments
nohup python optimize_pso_single_run.py \
    --seed {FAILED_SEED} \
    --output results/results_seed{FAILED_SEED}.json \
    --skip-validation \
    > results/pso_seed{FAILED_SEED}.log 2>&1 &
```

---

## Stopping Experiments (if needed)

**Stop all experiments:**
```bash
cat .artifacts/LT7_research_paper/experiments/results/experiment_pids.txt | xargs kill -TERM
```

**Stop specific PSO run:**
```bash
# Find PID for specific seed
ps -ef | grep "optimize_pso.*seed 42" | grep -v grep | awk '{print $2}'

# Kill that PID
kill -TERM {PID}
```

---

## Expected Timeline

**Seed 456 (fastest):** ~30 min (started at iteration 21, now at 24/30)
**Most PSO runs:** ~4-5 hours (30 iterations, ~10 min/iteration)
**Random search:** ~1 hour (600 samples, ~0.1 sec/sample)

**Overall completion:** ~5-6 hours from launch (08:06 AM) = **~1:00-2:00 PM**

---

## What Happens When Complete

When all experiments finish, you'll see:

```bash
bash check_experiment_status.sh
```

Output:
```
================================================================================
ALL EXPERIMENTS COMPLETE! Proceed to Phase 4 (generate tables/figures)
================================================================================
```

**Next steps:**
1. Verify all result files exist (10 PSO JSON + 1 Random JSON)
2. Generate Table 2 (PSO statistics)
3. Generate Table 3 (Method comparison)
4. Generate Figure 4 (PSO convergence curves)

See: `.artifacts/LT7_research_paper/experiments/RECOVERY_GUIDE.md` for details

---

## Troubleshooting

### "No experiments running (PID file not found)"
**Cause:** Script can't find PID file
**Solution:** Run script from project root: `bash .artifacts/LT7_research_paper/experiments/check_experiment_status.sh`

### "Processes: 1 / 12 running" but you see 11 processes with `ps`
**Cause:** Script's PID check uses `ps -p` which may fail on Windows
**Solution:** Ignore the "1/12", check the category counts instead:
- `PSO runs: 10 / 10` ✅
- `Random search: 1 / 1` ✅

### Log file shows "Binary file matches"
**Cause:** Non-ASCII characters in log (Unicode warnings)
**Solution:** Use `grep -a` to force text mode:
```bash
grep -a "Iteration" .artifacts/LT7_research_paper/experiments/results/pso_seed456.log | tail -5
```

### Experiment seems stuck (no new iterations)
**Possible causes:**
1. Normal (some iterations take 15-20 min)
2. Numerical issue (solver struggling)
3. Process died silently

**Check:**
```bash
# Is process still running?
ps -p {PID}

# Check if log file still growing:
ls -lh .artifacts/LT7_research_paper/experiments/results/pso_seed42.log
# Wait 5 minutes, run again - size should increase
```

---

## Pro Tips

1. **Don't panic if one run dies** - You need 10/10, but if one fails you can relaunch it later
2. **Seed 456 will finish first** - Good test case to verify data extraction scripts work
3. **Grid search failure is OK** - PSO is the main focus for Chapter 5, grid is supplementary
4. **You can close all terminals** - Experiments run via nohup (session-independent)
5. **Check from phone/remote** - SSH in, run `check_experiment_status.sh`, disconnect

---

## Quick Commands Cheat Sheet

```bash
# Quick status
bash .artifacts/LT7_research_paper/experiments/check_experiment_status.sh

# Watch live (seed 42)
tail -f .artifacts/LT7_research_paper/experiments/results/pso_seed42.log

# Count running
ps -ef | grep optimize_pso | grep -v grep | wc -l

# Count complete
ls .artifacts/LT7_research_paper/experiments/results/results_seed*.json | wc -l

# Stop all
cat .artifacts/LT7_research_paper/experiments/results/experiment_pids.txt | xargs kill -TERM
```
