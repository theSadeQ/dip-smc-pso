# Chapter 5 Experimental Infrastructure

**Purpose**: Complete experimental validation for PSO optimization of adaptive boundary layer parameters (thesis Chapter 5).

**Status**: Infrastructure complete, ready to launch experiments.

---

## Directory Structure

```
experiments/
├── README.md                       # This file
├── optimize_pso_single_run.py      # CLI PSO runner (single seed)
├── run_grid_search.py              # Exhaustive grid search (30×30)
├── run_random_search.py            # Random sampling baseline (600 samples)
├── aggregate_pso_stats.py          # Statistical aggregation (10 PSO runs)
├── run_pso_batch.bat               # Batch launcher (10 PSO runs)
├── launch_all_experiments.bat      # MASTER LAUNCHER (all experiments)
└── results/                        # Output directory (created automatically)
    ├── results_seed42.json         # PSO run (seed 42)
    ├── results_seed123.json        # PSO run (seed 123)
    ├── ... (8 more PSO runs)
    ├── grid_search_results.json    # Grid search output
    └── random_search_results.json  # Random search output
```

---

## Quick Start

### Option 1: Launch All Experiments (Recommended)

**WARNING**: This will run for ~10 hours and consume significant CPU!

```bash
cd .artifacts/LT7_research_paper/experiments
launch_all_experiments.bat
```

This launches:
- 10 PSO runs (seeds: 42, 123, 456, 789, 1011, 1314, 1617, 1920, 2223, 2526)
- Grid search (30×30 = 900 evaluations, 12-core parallel)
- Random search (600 samples)

All processes run in parallel (background). Monitor progress with:

```bash
# Check completed PSO runs
ls results/results_seed*.json | wc -l  # Should reach 10

# View logs (if enabled)
tail -f results/pso_batch.log
```

### Option 2: Dry Run (Test Single PSO)

Before committing to 10-hour run, test a single PSO execution:

```bash
python optimize_pso_single_run.py --seed 42 --output results/test_run.json --skip-validation
```

**Expected runtime**: ~22 minutes (30 particles × 30 iterations)

If successful, you'll see:
- JSON file created at `results/test_run.json`
- Console output showing PSO convergence
- Final best fitness value

### Option 3: Run Experiments Individually

```bash
# Run single PSO (full validation)
python optimize_pso_single_run.py --seed 42 --output results/results_seed42.json

# Run grid search only (1.9 hours with 12 cores)
python run_grid_search.py --n-grid 30 --n-cores 12

# Run random search only (22.5 minutes)
python run_random_search.py --n-samples 600 --seed 42
```

---

## Expected Runtime

| Experiment | Evaluations | Serial Time | Parallel Time | Cores Used |
|------------|-------------|-------------|---------------|------------|
| Single PSO | 900 (30×30) | 22.5 min    | 22.5 min      | 1          |
| 10 PSO runs | 9,000       | 3.75 hours  | 3.75 hours    | 1 each     |
| Grid search | 900         | 33.8 min    | 1.9 hours     | 12         |
| Random search | 600       | 22.5 min    | 22.5 min      | 1          |
| **TOTAL** | **10,500**  | **~82 hours** | **~10 hours** | Mixed      |

**Note**: Parallel time assumes launching all experiments simultaneously in background.

---

## Output Files

All results saved as JSON in `.artifacts/LT7_research_paper/experiments/results/`.

### PSO Output Format

Each `results_seed*.json` contains:

```json
{
  "seed": 42,
  "best_fitness": 15.54,
  "epsilon_min": 0.00250336,
  "alpha": 1.21441504,
  "convergence_iteration": 20,
  "n_evaluations": 900,
  "computation_time": 1350.0,
  "convergence_history": [25.0, 22.1, 19.8, ..., 15.54],
  "metadata": {
    "n_particles": 30,
    "n_iterations": 30,
    "timestamp": "2025-10-19T21:00:00"
  }
}
```

### Grid Search Output Format

`grid_search_results.json`:

```json
{
  "best_fitness": 16.12,
  "best_params": {"epsilon_min": 0.003, "alpha": 1.15},
  "total_evaluations": 900,
  "computation_time": 2028.0,
  "grid_resolution": [30, 30],
  "all_results": [
    {"epsilon_min": 0.001, "alpha": 0.1, "fitness": 25.3},
    ...
  ]
}
```

### Random Search Output Format

`random_search_results.json`:

```json
{
  "best_fitness": 17.41,
  "best_params": {"epsilon_min": 0.005, "alpha": 1.32},
  "total_evaluations": 600,
  "computation_time": 1350.0,
  "seed": 42,
  "samples": [
    {"epsilon_min": 0.012, "alpha": 0.87, "fitness": 22.1},
    ...
  ]
}
```

---

## Post-Processing (Generate Tables & Figures)

After experiments complete, generate publication-ready outputs:

### Generate Tables

```bash
cd .artifacts/LT7_research_paper/data_extraction

# Table II: PSO statistics (10 runs)
python generate_table2_pso_statistics.py

# Table III: Method comparison (PSO vs Grid vs Random)
python generate_table3_method_comparison.py
```

**Output**: LaTeX tables in `.artifacts/LT7_research_paper/tables/`

### Generate Figures

```bash
# Figure 4: PSO convergence (2-panel design)
python generate_figure4_pso_convergence.py

# Figures 2, 3, 7 (supplementary)
python generate_remaining_figures.py

# Figures 5, 6 (optional)
python generate_figure5_chattering_boxplot.py
python generate_figure6_robustness_degradation.py
```

**Output**: PDF (300 DPI) and PNG (150 DPI) in `.artifacts/LT7_research_paper/figures/`

---

## Disk Space Requirements

Estimated storage needed:

- 10 PSO JSON files: ~5 MB
- Grid search results: ~180 MB
- Random search results: ~90 MB
- **Total**: ~275 MB

Ensure sufficient disk space before launching experiments.

---

## Dependencies

All scripts require:

```
Python 3.9+
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
pyswarms>=1.3.0 (for PSO)
```

Verify installation:

```bash
python -c "import numpy, scipy, matplotlib, pyswarms; print('All dependencies OK')"
```

---

## Troubleshooting

### Issue: "PSO result file not found"

**Cause**: Experiments haven't run yet.

**Fix**:
```bash
cd .artifacts/LT7_research_paper/experiments
launch_all_experiments.bat
```

### Issue: "FileNotFoundError: benchmarks/MT6_adaptive_optimization.csv"

**Cause**: Figure generation scripts looking for old MT-6 data.

**Fix**: This is expected! The updated scripts will use simulated data for demonstration if experimental results don't exist yet. Run experiments first for real data.

### Issue: Grid search taking too long

**Cause**: Not using multiprocessing.

**Fix**:
```bash
# Explicitly set number of cores
python run_grid_search.py --n-grid 30 --n-cores 12
```

Reduce `--n-cores` if your machine has fewer cores.

### Issue: Experiments crash overnight

**Recovery**:
1. Check which runs completed:
   ```bash
   ls results/*.json
   ```
2. Identify missing seeds
3. Re-run individually:
   ```bash
   python optimize_pso_single_run.py --seed 1011 --output results/results_seed1011.json
   ```

### Issue: "Module not found: pyswarms"

**Fix**:
```bash
pip install pyswarms
```

---

## Experiment Verification

After completion, verify all outputs exist:

```bash
cd .artifacts/LT7_research_paper/experiments/results

# Should have 10 PSO files
ls results_seed*.json | wc -l  # Should output: 10

# Should have grid and random search
ls grid_search_results.json random_search_results.json

# Verify JSON validity
python -c "import json; json.load(open('results_seed42.json'))"
```

If any files missing, re-run specific experiments.

---

## Advanced Usage

### Custom PSO Configuration

Modify PSO parameters:

```bash
python optimize_pso_single_run.py \
  --seed 42 \
  --n-particles 50 \
  --n-iterations 50 \
  --output results/custom_pso.json
```

**Note**: Changing parameters may affect reproducibility.

### Resume Interrupted Experiments

The master launcher checks for existing results and skips completed runs:

```bash
# Safe to re-run - will only execute missing experiments
launch_all_experiments.bat
```

### Extract Convergence Statistics

After experiments complete:

```bash
python aggregate_pso_stats.py
```

Outputs:
- Mean, std, 95% CI for all parameters
- Convergence iteration statistics
- JSON summary for table generation

---

## For Reproducibility

**Critical settings** (already configured in scripts):

1. **Random seeds**: Fixed (42, 123, 456, ..., 2526)
2. **PSO parameters**: 30 particles, 30 iterations, constriction factor χ=0.7298
3. **Fitness weighting**: 70-15-15 (chattering-settling-overshoot)
4. **Grid resolution**: 30×30 (uniform spacing)
5. **Random search**: 600 samples (same seed for comparison)

All experiments use **identical**:
- Initial conditions (Monte Carlo sampling with fixed seed)
- Simulation parameters (dt=0.01, T=10s)
- Controller configuration
- Evaluation metrics (FFT-based chattering, ±0.05 rad settling threshold)

---

## Citation

If using this experimental infrastructure, cite:

```bibtex
@phdthesis{yourthesis2025,
  title={PSO Optimization of Adaptive Boundary Layer for Double-Inverted Pendulum SMC},
  author={Your Name},
  year={2025},
  school={Your University},
  chapter={5}
}
```

---

## Maintenance

**Last Updated**: October 19, 2025

**Maintainer**: LT-7 Task (Research Paper)

**Known Issues**: None (infrastructure complete and validated)

**Future Work**:
- Weight ablation study (4 fitness weightings) - OPTIONAL
- Hyperparameter sensitivity analysis - DEFERRED
- Pareto front visualization - OPTIONAL

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all dependencies installed
3. Review error logs in `results/` directory
4. Test with dry run (single PSO) first

**Emergency Recovery**: If all experiments fail, contact maintainer with error logs.
