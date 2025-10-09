# Workspace Organization & Hygiene

## Clean Root

Keep visible items ≤ 15 (core files/dirs only). Hide dev/build clutter behind dot‑prefixed folders.

**Visible files**: `simulate.py`, `streamlit_app.py`, `config.yaml`, `requirements.txt`, `README.md`, `CHANGELOG.md`

**Visible dirs**: `src/`, `tests/`, `docs/`, `notebooks/`, `benchmarks/`, `scripts/`

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

1. **Logs** → `logs/` directory
   - Format: `{script}_{timestamp}.log`
   - Examples: `pso_classical_20250930.log`, `pytest_run_20250930.log`
   - NEVER leave `.log` files in root

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

- [ ] Move all logs to `logs/` directory
- [ ] Delete or archive test artifacts
- [ ] Organize optimization results into timestamped directories
- [ ] Move any root-level scripts to appropriate `scripts/` subdirectory
- [ ] Archive temporary documentation files
- [ ] Verify root item count: `ls | wc -l` (target: ≤12 visible)
- [ ] Clean caches: `find . -name "__pycache__" -type d -exec rm -rf {} +`

### File Naming Conventions

- Logs: `{purpose}_{YYYYMMDD}_HHMMSS.log`
- Optimization dirs: `optimization_results/{controller}_{YYYYMMDD}/`
- Test artifacts: `.test_artifacts/{purpose}_{iteration}/`
- Archived docs: `.archive/{category}_{YYYYMMDD}/`

### Acceptable Root Items (≤15 visible)

**Core Files (6):**
- `simulate.py`, `streamlit_app.py`, `config.yaml`
- `requirements.txt`, `README.md`, `CHANGELOG.md`

**Additional Accepted:**
- `CLAUDE.md`, `logs/`, `optimization_results/`

**Core Dirs (6):**
- `src/`, `tests/`, `docs/`, `notebooks/`, `benchmarks/`, `scripts/`

**Total:** ≤15 items (realistic target)

**Hidden Dirs (acceptable):**
- `.archive/`, `.test_artifacts/`, `.dev_tools/`, `.build/`, `.cache/`, `.coverage/`, `.artifacts/`

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
| `*.log`, `report.*` | `logs/` | `output.log` → `logs/script_20251009.log` |
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

# CORRECT: Logs in logs/ with timestamps
python optimize.py > logs/optimize_$(date +%Y%m%d_%H%M%S).log
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
mv *.log logs/ 2>/dev/null || true
mv *_gains*.json *optimized*.json optimization_results/ 2>/dev/null || true
mv *_AUDIT.md *_REPORT.md INVESTIGATION_*.md .archive/analysis_reports/ 2>/dev/null || true
rm -rf __pycache__ out
```

## Long-Running Optimization Processes (PSO)

**Best practices for managing multi-hour PSO optimization runs:**

### Before Starting PSO

1. **Verify Configuration**
   - Check fitness function aligns with optimization goal
   - Verify parameter bounds are reasonable
   - Set appropriate iteration count and swarm size

2. **Prepare Monitoring**
   - Set up log directory: `logs/`
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
   - Monitor log files: `tail -f logs/pso_*.log`
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
- [ ] `logs/` directory > 20MB
- [ ] More than 3 validation/phase report .md files in `docs/`

**Check command:**
```bash
# Quick health check
ls | wc -l                           # Target: ≤15
du -sh .test_artifacts/              # Target: <10MB
du -sh .dev_validation/              # Target: <5MB
du -sh logs/                         # Target: <20MB
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
| Active notebooks | `notebooks/` | `.notebooks/` | Visible = actively used |
| Optimization results | `optimization_results/` | `.optimization_results/` | Visible = current results |
| Test artifacts | `.test_artifacts/` | `test_artifacts/` | Hidden = temporary |
| Archives | `.archive/` | `archive/` | Hidden = historical |
| Development tools | `.dev_tools/` | `dev_tools/` | Hidden = internal tooling |

**Rule**: If you find both visible and hidden versions, merge to the preferred location and delete the other.

## After Moving/Consolidation — Update References

1. Search & replace hardcoded paths.
2. Update README and diagrams.
3. Fix CI workflows.
4. Re‑run tests.
