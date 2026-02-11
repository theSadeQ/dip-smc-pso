# Quick Reference Command Sheet - DIP-SMC-PSO Project

Print this single-page reference and keep it near your keyboard during the 14-day immersion.

---

## CRITICAL: Platform-Specific Commands

**Windows (Your Platform):**
- Use `python` NOT `python3` (python3 causes exit code 49 on Windows)
- Example: `python simulate.py` [OK] | `python3 simulate.py` [ERROR]

---

## Essential Simulation Commands

### Basic Simulations
```bash
# Run Classical SMC with plot
python simulate.py --ctrl classical_smc --plot

# Run Super-Twisting SMC
python simulate.py --ctrl sta_smc --plot

# Run Adaptive SMC
python simulate.py --ctrl adaptive_smc --plot

# Run Hybrid Adaptive STA-SMC
python simulate.py --ctrl hybrid_adaptive_sta_smc --plot

# Run Swing-Up Controller
python simulate.py --ctrl swing_up_smc --plot

# Run MPC (experimental)
python simulate.py --ctrl mpc --plot
```

### Load Optimized Gains
```bash
# Load pre-tuned gains from JSON
python simulate.py --load tuned_gains.json --plot

# Load your Day 3 optimized gains
python simulate.py --load day3_gains.json --plot
```

### Configuration Management
```bash
# Print current configuration
python simulate.py --print-config

# Use custom config file
python simulate.py --config custom_config.yaml --plot

# Use your Day 12 capstone config
python simulate.py --config capstone_config.yaml --plot
```

---

## PSO Optimization Commands

### Tune Controller Gains
```bash
# Optimize Classical SMC gains
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json

# Optimize with seed for reproducibility
python simulate.py --ctrl adaptive_smc --run-pso --seed 42 --save gains_adaptive.json

# Optimize Hybrid controller (Day 6 exercise)
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --save gains_hybrid.json

# Quick test run (fewer iterations)
python simulate.py --ctrl sta_smc --run-pso --pso-iters 10 --save quick_test.json
```

### PSO Result Analysis
```bash
# View saved gains
cat gains_classical.json

# Compare multiple gain sets
python -c "import json; print(json.load(open('gains_classical.json')))"
```

---

## Testing Commands

### Run Tests
```bash
# Run ALL tests
python -m pytest tests/ -v

# Run controller tests only
python -m pytest tests/test_controllers/ -v

# Run specific controller test
python -m pytest tests/test_controllers/test_classical_smc.py -v

# Run integration tests
python -m pytest tests/test_integration/ -v

# Run benchmarks
python -m pytest tests/test_benchmarks/ --benchmark-only
```

### Coverage Reports
```bash
# Generate HTML coverage report (Day 8)
python -m pytest tests/ --cov=src --cov-report=html

# View coverage in browser
start htmlcov/index.html  # Windows

# Generate terminal coverage summary
python -m pytest tests/ --cov=src --cov-report=term
```

### Quick Test During Development
```bash
# Run tests for file you're working on
python -m pytest tests/test_controllers/test_adaptive_smc.py -v

# Run with verbose output for debugging
python -m pytest tests/test_controllers/ -vv
```

---

## Hardware-in-the-Loop (HIL) Commands

### Run HIL Simulations (Day 10)
```bash
# Basic HIL run with plot
python simulate.py --run-hil --plot

# HIL with custom config
python simulate.py --config custom_config.yaml --run-hil

# HIL with specific controller
python simulate.py --ctrl classical_smc --run-hil --plot
```

---

## Web Interface

### Launch Streamlit App
```bash
# Start web interface (Day 1)
streamlit run streamlit_app.py

# Access at: http://localhost:8501
```

---

## Documentation Commands

### Build Sphinx Documentation (Day 13)
```bash
# Build HTML documentation
sphinx-build -M html docs docs/_build

# Build with warnings as errors (strict mode)
sphinx-build -M html docs docs/_build -W --keep-going

# View built docs
start docs/_build/html/index.html  # Windows
```

### Verify Documentation Changes
```bash
# Check if file was copied to build
python -c "import os; print(os.path.getmtime('docs/_static/style.css'))"
python -c "import os; print(os.path.getmtime('docs/_build/html/_static/style.css'))"

# Verify localhost serves new content
curl -s "http://localhost:9000/_static/style.css" | head -n 20
```

---

## Git Commands for Learning

### Basic Workflow (Day 11, Day 14)
```bash
# Check repository status
git status

# Create feature branch
git checkout -b feature/my-experiment

# Stage changes
git add .

# Commit with message
git commit -m "feat: Complete Day 14 capstone project"

# View recent commits
git log --oneline -10

# Compare with main branch
git diff main...HEAD
```

### Recovery (If You Make Mistakes)
```bash
# Undo uncommitted changes
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View what changed
git diff
```

---

## Project Recovery Commands

### Session Recovery (Day 1, After Token Limits)
```bash
# One-command recovery
bash .ai_workspace/tools/recovery/recover_project.sh

# Check roadmap progress
python .ai_workspace/tools/analysis/roadmap_tracker.py

# View project state
cat .ai_workspace/state/project_state.json
```

### Quick Status Check
```bash
# Verify environment
python --version  # Should show 3.9+
pip list | grep numpy

# Check git remote
git remote -v  # Should show https://github.com/theSadeQ/dip-smc-pso.git
```

---

## File Navigation Commands

### Find Files
```bash
# Locate controller implementations
find src/controllers -name "*.py" -type f

# Find all test files
find tests -name "test_*.py"

# Find config files
find . -name "*.yaml" -o -name "*.json"
```

### Quick File Viewing
```bash
# View controller source
cat src/controllers/smc/algorithms/classical_smc.py

# Count lines in file
python -c "print(len(open('src/optimizer/pso_optimizer.py').readlines()))"

# View first 50 lines
head -n 50 src/core/simulation_runner.py
```

---

## Data Analysis Commands (Day 9)

### View Benchmark Results
```bash
# Navigate to comparative experiments
cd academic/paper/experiments/comparative

# List available benchmarks
ls -lh

# View specific results
cat MT-5_comprehensive_benchmark_summary.txt
```

### Quick Data Inspection
```bash
# View PSO optimization logs
cat academic/logs/pso/optimization_*.log

# View benchmark logs
cat academic/logs/benchmarks/*.log
```

---

## Common Troubleshooting

### Dependency Issues
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify critical packages
python -c "import numpy; print(numpy.__version__)"
python -c "import scipy; print(scipy.__version__)"
```

### Configuration Validation
```bash
# Validate config file
python -c "from src.config import load_config; load_config('config.yaml')"
```

### Clear Caches
```bash
# Clear pytest cache
rm -rf .pytest_cache

# Clear Python bytecode
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## Keyboard Shortcuts (Windows)

- `Ctrl+C` - Stop running simulation or command
- `Ctrl+L` - Clear terminal screen
- `Ctrl+R` - Search command history
- `Tab` - Autocomplete file/directory names
- `Up Arrow` - Previous command
- `Ctrl+Shift+R` - Hard refresh browser (Day 13)

---

## Daily Workflow Template

**Morning:**
```bash
# 1. Check git status
git status

# 2. Review yesterday's outputs
ls academic/logs/

# 3. Start Streamlit (background)
start streamlit run streamlit_app.py
```

**Afternoon:**
```bash
# 4. Run experiments from checklist
python simulate.py --ctrl <CONTROLLER> --plot

# 5. Run tests if you modified code
python -m pytest tests/test_controllers/ -v
```

**Evening:**
```bash
# 6. Commit your work
git add .
git commit -m "docs: Complete Day X immersion tasks"

# 7. Review progress
cat .ai_workspace/edu/immersion_schedule/progress_tracker.md
```

---

## Emergency Commands

### Stuck in Infinite Loop
- Press `Ctrl+C` to interrupt

### Simulation Not Plotting
```bash
# Check matplotlib backend
python -c "import matplotlib; print(matplotlib.get_backend())"
```

### Out of Memory
```bash
# Check Python process memory
tasklist /fi "imagename eq python.exe" /fo table  # Windows
```

---

## Learning Tips

1. **Copy-paste these commands** - Don't type from scratch during immersion
2. **Keep terminal history** - Use Up Arrow to repeat commands
3. **Run commands in parallel** - Open multiple terminals (Day 10+)
4. **Document failures** - Note which commands error for troubleshooting
5. **Bookmark this file** - Refer to it 20+ times per day

---

## Next Steps After Day 14

```bash
# Begin Tutorial 01
cat docs/guides/getting-started.md

# View available research tasks
ls .ai_workspace/planning/research/

# Explore advanced examples
python simulate.py --help
```

---

**Print Date:** _______________
**Keep this reference visible during all 14 days of immersion!**
