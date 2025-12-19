# Workspace Organization & Hygiene

## Clean Root

Keep visible items ≤ 15 (core files/dirs only). Hide dev/build clutter behind dot‑prefixed folders.

**Visible files**: `simulate.py`, `streamlit_app.py`, `config.yaml`, `requirements.txt`, `README.md`, `CHANGELOG.md`

**Visible dirs**: `src/`, `tests/`, `docs/`, `benchmarks/`, `scripts/`, `envs/`, `optimization_results/`

**Hidden dev dirs (examples)**: `.archive/`, `.build/`, `.dev_tools/`, `.scripts/`, `.tools/`
 Move **CLAUDE.md → .CLAUDE.md** if you prefer a clean root.

## Universal Cache Cleanup

```bash
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache .ruff_cache .numba_cache .benchmarks .hypothesis
```

## Backup & Docs Artifacts

```bash
find . -name "*.bak" -o -name "*.backup" -o -name "*~" | xargs -I{} mv {} .archive/ 2>/dev/null
# Docs build artifacts → archive
mv docs/_build docs/_static docs/.github docs/.gitignore docs/.lycheeignore .archive/
```

## Enhanced .gitignore

```gitignore
**/__pycache__/
**/*.py[cod]
**/*$py.class
.benchmarks/
.numba_cache/
.pytest_cache/
.ruff_cache/
.hypothesis/
docs/_build/
docs/_static/
*.bak
*.backup
*~
```

## Automation & Verification

```bash
# Helper for a clean view
echo "(create) .dev_tools/clean_view.sh to list essentials, key dirs, hidden tools"

# Health checks
ls | wc -l                                    # target ≤ 15
find . -name "__pycache__" | wc -l            # target = 0
find . -name "*.bak" -o -name "*.backup" -o -name "*~" | wc -l  # target = 0
```

## Session Artifact Management (MANDATORY)

**Rules for EVERY session to maintain clean root directory:**

### File Placement Rules

1. **Logs** → `.logs/` directory (hidden, centralized)
   - **Centralized paths:** Use `src/utils/logging/paths.py` (MANDATORY)
   - **Structure:** `.logs/{pso,test,monitoring,archive}/`
   - **Format:** `{script}_{timestamp}.log`
   - **Examples:** `.logs/pso/pso_classical_20250930.log`, `.logs/test/pytest_run_20250930.log`
   - **Migration:** See `docs/guides/logs_migration_guide.md`
   - NEVER hardcode "logs/" paths in code

2. **Test Artifacts** → `.test_artifacts/` (auto-cleanup)
   - Use for temporary test runs
   - Examples: `.test_artifacts/pso_test_run/`, `.test_artifacts/validation_debug/`
   - Clean up before session ends

3. **Optimization Results** → Structured directories with timestamps
   - Use: `optimization_results/{controller}_{date}/`
   - Examples: `optimization_results/classical_smc_20250930/`
   - Include metadata JSON files

4. **Documentation** → `docs/` or `.archive/`
   - NEVER create `.md` files in root except README.md, CHANGELOG.md, CLAUDE.md
   - Analysis reports → `docs/analysis/`
   - Historical docs → `.archive/docs_{date}/`

5. **Scripts** → `scripts/` with subdirectories
   - Optimization scripts → `scripts/optimization/`
   - Analysis scripts → `scripts/analysis/`
   - Utility scripts → `scripts/utils/`

### Before Session Ends Checklist

- [x] Move all logs to `.logs/` directory (completed Dec 17, 2025)
- [x] Centralize log paths via `src/utils/logging/paths.py` (completed Dec 17, 2025)
- [x] Archive old logs to `.logs/archive/YYYY-MM-DD/` (completed Dec 17, 2025)
- [ ] Delete or archive test artifacts
- [ ] Organize optimization results into timestamped directories
- [ ] Move any root-level scripts to appropriate `scripts/` subdirectory
- [ ] Archive temporary documentation files
- [ ] Verify root item count: `ls | wc -l` (target: ≤19 visible, current: 20, pending 3 locked files)
- [ ] Verify `.logs/` size: `du -sh .logs/` (target: ≤100MB, current: 56MB [OK])
- [ ] Clean caches: `find . -name "__pycache__" -type d -exec rm -rf {} +`

### File Naming Conventions

- Logs: `{purpose}_{YYYYMMDD}_HHMMSS.log`
- Optimization dirs: `optimization_results/{controller}_{YYYYMMDD}/`
- Test artifacts: `.test_artifacts/{purpose}_{iteration}/`
- Archived docs: `.archive/{category}_{YYYYMMDD}/`

### Acceptable Root Items (≤19 visible)

**Core Files (9):**
- `simulate.py`, `streamlit_app.py`, `config.yaml`
- `requirements.txt`, `README.md`, `CHANGELOG.md`, `CLAUDE.md`
- `package.json`, `package-lock.json` (MCP config)

**Core Dirs (8):**
- `src/`, `tests/`, `docs/`, `benchmarks/`, `scripts/`, `envs/`
- `optimization_results/`, `data/`

**Current:** 18 items (Dec 17, 2025 - meets target ≤19)

**Hidden Dirs (acceptable):**
- `.archive/`, `.test_artifacts/`, `.project/`, `.build/`, `.cache/`, `.coverage/`, `.artifacts/`
- `.logs/` (centralized logging), `.git/`, `.github/`

### File Organization Enforcement (MANDATORY)

**CRITICAL RULE**: NEVER create files in root directory except approved core files.

**Before Creating ANY File - Ask:**
1. Does this belong in root? (Answer: 99% NO)
2. What is the proper directory for this file type?
3. Does the target directory exist? If not, create it FIRST.
4. Is this temporary? If yes → use hidden directory (`.test_artifacts/`, `.archive/`)

**File Type Directory Map:**

| File Pattern | Destination | Example |
|-------------|-------------|---------|
| `test_*.py` | `tests/debug/` | `test_my_feature.py` → `tests/debug/test_my_feature.py` |
| `*.log`, `report.*` | `.logs/` | `output.log` → `.logs/script_20251009.log` |
| `*_gains*.json`, `optimized_*.json` | `optimization_results/{controller}_{date}/` | `optimized_gains_smc.json` → `optimization_results/classical_smc_20251009/gains.json` |
| `*_AUDIT.md`, `*_REPORT.md`, `INVESTIGATION_*.md` | `.archive/analysis_reports/` | `EXCEPTION_HANDLER_AUDIT.md` → `.archive/analysis_reports/EXCEPTION_HANDLER_AUDIT.md` |
| `*.txt` (analysis results) | `.archive/analysis_reports/` or `logs/` | `phase5_stats.txt` → `.archive/analysis_reports/phase5_stats.txt` |
| Coverage data | `.coverage/` or delete | `coverage.json` → `.coverage/coverage.json` or `rm coverage.json` |
| Build artifacts | Delete immediately | `__pycache__/`, `out/` → `rm -rf __pycache__ out` |

**Examples - WRONG vs. CORRECT:**

```bash
# WRONG: Creating test file in root
touch test_my_feature.py
python test_my_feature.py

# CORRECT: Test files in tests/debug/
mkdir -p tests/debug
touch tests/debug/test_my_feature.py
python tests/debug/test_my_feature.py
```

```bash
# WRONG: Dumping logs in root
python optimize.py > output.log

# CORRECT: Logs in .logs/ with timestamps
python optimize.py > .logs/optimize_$(date +%Y%m%d_%H%M%S).log
```

```bash
# WRONG: Saving optimization results in root
python scripts/optimization/tune_controller.py --save optimized_gains.json

# CORRECT: Results in organized timestamped directories
python scripts/optimization/tune_controller.py --save optimization_results/classical_smc_$(date +%Y%m%d)/gains.json
```

**Session End Enforcement (Run Before EVERY Commit):**

```bash
# Check root item count (must be ≤15)
ls -1 | wc -l

# Find any test files in root (should be empty)
find . -maxdepth 1 -name "test_*.py"

# Find any logs in root (should be empty)
find . -maxdepth 1 -name "*.log"

# Find any JSON results in root (should be empty except config.yaml)
find . -maxdepth 1 -name "*.json"

# Clean all caches
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
```

**Auto-cleanup Command (run at session end):**

```bash
# Move misplaced files to proper locations
mv test_*.py tests/debug/ 2>/dev/null || true
mv *.log .logs/ 2>/dev/null || true
mv *_gains*.json *optimized*.json optimization_results/ 2>/dev/null || true
mv *_AUDIT.md *_REPORT.md INVESTIGATION_*.md .archive/analysis_reports/ 2>/dev/null || true
rm -rf __pycache__ out
```

## Benchmarks Directory Organization

**Status:** Reorganized December 18, 2025 for publication-ready structure

### Directory Structure

```
benchmarks/
├── raw/                    # Immutable original benchmark outputs (organized by research task)
│   ├── MT-5_comprehensive/ # MT-5: Comprehensive benchmark suite (Oct 25, 2025)
│   ├── baselines/          # Original baseline performance data
│   └── README.md           # Task provenance and metadata
├── processed/              # Derived/aggregated analysis datasets
├── figures/                # Publication-ready plots (PRESERVED PATH - DO NOT MOVE)
└── reports/                # Task completion summaries and research documentation

src/benchmarks/             # Analysis modules (moved from benchmarks/ root)
├── analysis/               # Accuracy metrics, statistical analysis
├── benchmark/              # Integration benchmark runner
├── comparison/             # Method comparison utilities
├── integration/            # Numerical integration methods
└── examples/               # Usage examples

.logs/benchmarks/           # Log files (9.7 MB, hidden directory)
```

### Key Principles

1. **Raw Data Immutability**: Original benchmark outputs never modified
2. **Task Traceability**: Clear provenance (which research task generated which data)
3. **Publication Ready**: Figures/ path preserved for existing references
4. **Proper Package Structure**: Analysis modules in src/, not data directory

### Import Path Changes

**Old (deprecated):**
```python
from benchmarks.analysis import accuracy_metrics
from benchmarks.benchmark import IntegrationBenchmark
```

**New:**
```python
from src.benchmarks.analysis import accuracy_metrics
from src.benchmarks.benchmark import IntegrationBenchmark
```

All imports automatically updated by `scripts/migration/update_benchmark_paths.py`.

### Research Task Provenance

- **MT-5** (Oct 25, 2025): Comprehensive benchmark suite (7 controllers)
- **MT-6** (Oct 26-27, 2025): Boundary layer optimization
- **MT-7** (Oct 28, 2025): Robust PSO tuning
- **MT-8** (Oct 29, 2025): Disturbance rejection testing
- **LT-4** (Oct 30, 2025): Lyapunov stability proofs
- **QW-2** (Nov 7, 2025): Quick win comprehensive benchmark

### Migration Artifacts

- **Backup:** `.artifacts/backups/benchmarks_pre_reorg_20251218.tar.gz`
- **Script:** `scripts/migration/update_benchmark_paths.py`
- **Validation:** 111 benchmark tests collected successfully

### DO NOT

- Move or rename `benchmarks/figures/` (breaks existing references)
- Create new files in `benchmarks/` root (use subdirectories)
- Import from `benchmarks.*` (use `src.benchmarks.*`)

### See Also

- Complete reorganization plan: `C:\Users\SadeQ\.claude42\plans\polished-inventing-spindle.md`
- Benchmark README files: `benchmarks/README.md`, `benchmarks/raw/*/README.md`

## Logs and Monitoring Consolidation

**Status:** Consolidated December 19, 2025

### Legacy Directories Removed

**Visible directories removed from root:**
- `logs/` (120 KB) → `.logs/` (centralized)
- `monitoring_data/` (56 MB) → `.logs/archive/` (compressed to 214 KB)

**Result:** Removed 1 visible root directory (monitoring_data/), improved workspace hygiene

**Note:** `logs/` directory still exists with 1 locked file (pso_results.db, 0 bytes) pending manual cleanup

### Centralized Logging Structure

All logs now in `.logs/` (hidden directory):

```
.logs/
├── README.md                       # Documentation and retention policies
├── combined_YYYYMMDD.log           # Active MCP server logs
├── archive/                        # Compressed historical logs
│   └── 2025-12-16/                 # Compressed monitoring logs
│       └── data_manager_20251216.log.gz (214 KB, was 56 MB)
├── benchmarks/                     # Research task logs (9.7 MB)
├── pso/                            # PSO optimization logs (978 KB)
│   ├── 2025-12-09_*.log            # Root PSO logs (from optimization_results/)
│   └── phase2/                     # Phase 2 PSO logs
├── monitoring/                     # Monitoring system logs (reserved)
└── test/                           # Test runner logs (reserved)
```

**Total Size:** 12 MB (well under 100 MB target)

### Optimization Results Restructuring

Organized PSO gains and analysis results for clarity:

```
optimization_results/
├── README.md                       # Comprehensive documentation
├── active/                         # Current working results (MT-8, test panels)
├── phases/                         # Phase-organized gains
│   ├── phase2/gains/               # Comprehensive benchmark gains
│   └── phase53/                    # Lyapunov-optimized gains
├── analysis_results/               # Comparison JSONs, summary statistics
│   ├── phase2_summary.json
│   ├── phase2_vs_mt8_comparison.json
│   └── standard_vs_robust_comparison.json
└── archive/                        # Historical/deprecated gains
    ├── 2024_10/                    # October 2024 gains
    └── robust_2025_12/             # December 2025 robust variants
```

**Changes:**
- Moved 13 PSO logs (978 KB) → `.logs/pso/`
- Organized gains: active/, phases/, analysis_results/, archive/
- Removed empty directories: analysis/, comparisons/
- Created comprehensive README.md

### Centralized Path Configuration

**Single Source of Truth:** `src/utils/logging/paths.py`

All logging uses centralized configuration:
```python
from src.utils.logging.paths import LOG_DIR, PSO_LOG_DIR, MONITORING_LOG_DIR

# Automatically resolves to .logs/ subdirectories
pso_log = PSO_LOG_DIR / f"{datetime.now():%Y%m%d}_{controller}_pso.log"
```

**Environment Override:**
```bash
export LOG_DIR="/custom/log/path"  # Override default .logs/
```

### DO NOT

- Create logs in root directory (use `.logs/`)
- Hardcode "logs/" paths (use `src/utils/logging/paths.py`)
- Create visible log directories (always use hidden `.logs/`)
- Store PSO logs in `optimization_results/` (use `.logs/pso/`)

### See Also

- Log paths config: `src/utils/logging/paths.py`
- Logging handlers: `src/utils/logging/handlers.py`
- Logs README: `.logs/README.md`
- Optimization results README: `optimization_results/README.md`

## Long-Running Optimization Processes (PSO)

**Best practices for managing multi-hour PSO optimization runs:**

### Before Starting PSO

1. **Verify Configuration**
   - Check fitness function aligns with optimization goal
   - Verify parameter bounds are reasonable
   - Set appropriate iteration count and swarm size

2. **Prepare Monitoring**
   - Set up log directory: `.logs/`
   - Create monitoring scripts ready
   - Document expected completion time

3. **Session Continuity**
   - Create comprehensive handoff documentation
   - Document current state and next steps
   - Prepare automation for when PSO completes

### During PSO Execution

1. **Monitoring Tools**
   ```bash
   # Quick status check
   python scripts/optimization/check_pso_completion.py

   # Live dashboard
   python scripts/optimization/watch_pso.py

   # Automated monitoring
   python scripts/optimization/monitor_and_validate.py --auto-update-config
   ```

2. **Progress Tracking**
   - Monitor log files: `tail -f .logs/pso_*.log`
   - Check iteration progress and convergence
   - Verify no errors or instability

3. **Resource Management**
   - PSO logs actively written (don't move/edit)
   - Leave processes undisturbed
   - Prepare validation scripts in parallel

### After PSO Completion

1. **Immediate Actions**
   - Run validation: `python scripts/optimization/validate_and_summarize.py`
   - Review results JSON files
   - Check acceptance criteria

2. **Decision Point**
   - **If PASS:** Update config, test, commit, close issue
   - **If FAIL:** Analyze failure, re-run with corrected parameters

3. **Cleanup**
   - Move logs to organized directories
   - Archive optimization artifacts
   - Update documentation with results

### Automation Templates

**Example: End-to-End PSO Workflow**
```python
# example-metadata:
# runnable: false

# scripts/optimization/monitor_and_validate.py pattern:
# 1. Monitor PSO logs for completion
# 2. Auto-trigger validation when done
# 3. Update config if validation passes
# 4. Provide clear next steps
```

**Example: Validation Pipeline**
```python
# example-metadata:
# runnable: false

# scripts/optimization/validate_and_summarize.py pattern:
# 1. Load optimized gains from JSON
# 2. Re-simulate with exact PSO metrics
# 3. Compare against acceptance criteria
# 4. Generate comprehensive summary JSON
```

### Lessons Learned (Issue #12)

1. **Fitness Function Matters:** Ensure fitness directly optimizes target metric
2. **Document Expected Outcomes:** Predict likely results based on fitness design
3. **Prepare Alternative Paths:** Have corrected scripts ready if validation fails
4. **Full Automation:** Create end-to-end workflows for reproducibility
5. **Comprehensive Handoff:** Document state for session continuity

## Cleanup History

### November 8, 2025 - Root Cleanup & Thesis Index
**Status:** COMPLETE

**Before**: 24 visible items
**After**: 17 visible items (29% reduction)

**Actions Taken:**
1. **Created** docs/thesis/index.md for organized subdirectory navigation
2. **Moved** coverage files:
   - `coverage.json` → `.cache/coverage/coverage.json`
   - `coverage_report.txt` → `.cache/coverage/coverage_report.txt`
3. **Moved** logs:
   - `report.log` → `.logs/report.log`
   - `logs/` → `.logs/` (made hidden)
4. **Moved** scripts:
   - `run_coverage.py` → `scripts/coverage/run_coverage.py`
5. **Deleted** ephemeral files:
   - `nul` (Windows null artifact)
   - `__pycache__/` (Python cache, regenerates as needed)

**Updates:**
- Updated `.gitignore` to include `.logs/`
- Fixed documentation references:
  - `docs/testing/coverage_baseline.md` - coverage.json path
  - `docs/presentation/results-discussion.md` - report.log path
  - `docs/presentation/THESIS_FINAL.md` - report.log path
  - `docs/testing/guides/control_systems_unit_testing.md` - report.log path

**Result:** ✅ Meets ≤17 target (15 with 2-item buffer)
**Verification:** All functionality tested (simulate.py, coverage script work)

## Lessons Learned from Major Cleanups

**Full cleanup analysis (370MB recovery):** `.claude/WORKSPACE_CLEANUP_2025-10-09.md`

### Red Flags (Check Weekly)

Early warning signs that cleanup is needed:

- [ ] `.test_artifacts/` size > 10MB
- [ ] `.dev_validation/` size > 5MB
- [ ] Root directory > 15 visible items
- [ ] Any `*.log.*` files anywhere in project
- [ ] Multiple backup files with incrementing numbers (file_v1, file_v2...)
- [ ] Duplicate directories (both visible and hidden versions exist)
- [ ] `.logs/` directory > 100MB
- [ ] More than 3 validation/phase report .md files in `docs/`

**Check command:**
```bash
# Quick health check
ls | wc -l                           # Target: ≤19 (current: 18)
du -sh .test_artifacts/              # Target: <10MB
du -sh .dev_validation/              # Target: <5MB
du -sh .logs/                        # Target: <100MB (current: ~8MB)
find . -name "*.log.*" | wc -l       # Target: 0
```

### Archive Immediately Patterns

Archive to `.archive/` when you see:
- `PHASE_*_COMPLETION_REPORT.md` → `docs_archive_YYYYMMDD/phase_reports/`
- `WEEK*_VALIDATION*.md` → `docs_archive_YYYYMMDD/validation_reports/`
- `issue_*.md`, `GitHub_Issue_*.md` → `docs_archive_YYYYMMDD/issue_reports/` (after closed)
- Backup CSVs, batch JSONs → `research_YYYYMMDD/`
- Experimental code → `experiments_YYYYMMDD/`
- Logs > 1MB → `pso_logs_YYYYMMDD/` or `test_logs_YYYYMMDD/`

### Duplicate Directory Prevention

**Single Source of Truth:**

| Purpose | Use This | NOT This | Reason |
|---------|----------|----------|--------|
| Research artifacts | `.artifacts/` | `artifacts/` | Hidden = not cluttering root |
| Active notebooks | `docs/tutorials/notebooks/` | `notebooks/` (moved Dec 17, 2025) | Integrated with documentation |
| Optimization results | `optimization_results/` | `.optimization_results/` | Visible = current results |
| Test artifacts | `.test_artifacts/` | `test_artifacts/` | Hidden = temporary |
| Archives | `.archive/` | `archive/` | Hidden = historical |
| Development tools | `.project/dev_tools/` | `.dev_tools/` (at root) | Centralized config location |

**Rule**: If you find both visible and hidden versions, merge to the preferred location and delete the other.

## After Moving/Consolidation — Update References

1. Search & replace hardcoded paths.
2. Update README and diagrams.
3. Fix CI workflows.
4. Re‑run tests.
