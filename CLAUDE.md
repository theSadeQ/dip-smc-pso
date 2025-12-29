# Claude.md — Team Memory & Project Conventions

> This file contains project-specific instructions for Claude Code operations and automatic repository management.

**CRITICAL RULE - NO EMOJIS:**
- **NEVER use Unicode emojis** ([LAUNCH], [OK], [ERROR], etc.) in any code, scripts, output, or documentation
- **ALWAYS use ASCII text markers** instead: [AI], [OK], [ERROR], [WARNING], [INFO], [BLUE], etc.
- **Reason:** Windows terminal (cp1252 encoding) cannot display Unicode properly, causing crashes
- **Applies to:** Python scripts, shell output, markdown docs, commit messages, all user-facing text
- **Example:** Use "[OK]" not "[OK]", "[ERROR]" not "[ERROR]", "[INFO]" not "[INFO]"

**CRITICAL RULE - AUTONOMOUS OPERATION:**
- **ALWAYS continue** with tasks automatically without asking for permission
- **NEVER ask** "Would you like to proceed?" or "Ready to continue?" or "Should I move to the next task?"
- **ALWAYS commit and push** changes automatically after completing work
- **NEVER ask** for commit/push confirmation - do it automatically per repository management rules
- **Action:** Complete task -> Update tracking docs -> Commit -> Push -> Start next task
- **Exception:** Only ask questions when user input is REQUIRED for implementation decisions

**CRITICAL RULE - WINDOWS PLATFORM:**
- **Platform**: Windows (win32) - Working Directory: D:\Projects\main
- **ALWAYS use `python`** NOT `python3` (python3 doesn't exist on Windows, causes exit code 49)
- **ALWAYS use `python -m pytest`** NOT `python3 -m pytest`
- **ALWAYS use `python simulate.py`** NOT `python3 simulate.py`
- **Example:** `python --version` works [DONE] | `python3 --version` fails with exit code 49 [FAIL]

------

## 1) Repository Information

**Primary Repository**: https://github.com/theSadeQ/dip-smc-pso.git
**Branch Strategy**: Main branch deployment
**Working Directory**: D:\Projects\main

------

## 2) Automatic Repository Management

**See:** `.ai_workspace/config/repository_management.md` for complete details.

**Quick Reference:**
- MANDATORY: Auto-commit and push after ANY repository changes
- Commit message format: `<Action>: <Brief description>` with [AI] footer
- Always verify remote URL: `https://github.com/theSadeQ/dip-smc-pso.git`

------

## 3) Session Continuity & Project-wide Recovery System

**See:** `.ai_workspace/guides/session_continuity.md` for complete details.

**Purpose:** 30-second recovery from token limits or multi-month gaps

**Status:** [OK] Operational (Oct 2025)

### Quick Recovery
```bash
# One-command Recovery After Token Limit
/recover

# Or Manually
bash .ai_workspace/tools/recovery/recover_project.sh

# Check Roadmap Progress
python .ai_workspace/tools/analysis/roadmap_tracker.py
```

### Multi-Account Recovery (NEW - Nov 2025)

**Quick Start**: Windows: `.project\tools\recovery\quick_recovery.bat` | Linux/Mac: `bash .ai_workspace/tools/recovery/recover_project.sh && python .ai_workspace/tools/checkpoints/analyze_checkpoints.py`

**See**: `.ai_workspace/tools/multi_account/MULTI_ACCOUNT_RECOVERY_GUIDE.md` for complete workflow

### Key Tools
1. **Project State Manager** (`.ai_workspace/tools/recovery/project_state_manager.py`) - Tracks phase, roadmap progress, completed tasks
2. **Git Recovery Script** (`.ai_workspace/tools/recovery/recover_project.sh`) - 30-second recovery workflow
3. **Roadmap Tracker** (`.ai_workspace/tools/analysis/roadmap_tracker.py`) - Parses 72-hour research roadmap (50 tasks)
4. **Agent Checkpoint System** (`.ai_workspace/tools/checkpoints/agent_checkpoint.py`) - Recovers interrupted multi-agent work
5. **Multi-Account Recovery** (`.ai_workspace/tools/multi_account/MULTI_ACCOUNT_RECOVERY_GUIDE.md`) - Resume work across accounts/sessions

### What Survives Token Limits
- [OK] Git commits (10/10), project state (9/10), agent checkpoints (9/10), data files (8/10)
- [ERROR] Background bash processes, in-memory agent state (BUT checkpoints preserve progress)

### Automated Tracking (zero Manual Updates)
```bash
# Just Commit with Task ID - State Auto-updates via Git Hooks
git commit -m "feat(MT-6): Complete boundary layer optimization"
# Pre-commit Hook Auto-detects Mt-6 + Updates Project State
```

**Recovery Reliability:** Git commits (10/10) | Automated tracking (10/10) | Multi-account recovery (NEW) | Test coverage (11/11 tests, 100%)

**Current Phase:** Maintenance/Publication | **Completed:** Phase 3 (UI 34/34), Phase 4 (Production 4.1+4.2), Phase 5 (Research 11/11 tasks, LT-7 submission-ready)

------

## 4) Project Overview

**Double‑Inverted Pendulum Sliding Mode Control with PSO Optimization**

A Python framework for simulating, controlling, and analyzing a double‑inverted pendulum (DIP) system. It provides multiple SMC variants, optimization (PSO), a CLI and a Streamlit UI, plus rigorous testing and documentation.

------

## 5) Architecture

### 5.1 High‑level Modules

- **Controllers**: classical SMC, super‑twisting, adaptive, hybrid adaptive STA‑SMC, swing‑up; experimental MPC.
- **Dynamics/Plant**: simplified and full nonlinear dynamics (plus low‑rank); shared base interfaces.
- **Core Engine**: simulation runner, unified simulation context, batch/Numba vectorized simulators.
- **Optimization**: PSO tuner (operational); additional algorithms staged via an optimization core.
- **Utils**: validation, control primitives (e.g., saturation), monitoring, visualization, analysis, types, reproducibility, dev tools.
- **HIL**: plant server + controller client for hardware‑in‑the‑loop experiments.

### 5.2 Representative Layout (merged)

```bash
src/
├─ controllers/     # SMC variants (classical, STA, adaptive, hybrid, swing-up, MPC), factory
├─ core/           # Dynamics, simulation runner, context, vectorized simulators
├─ plant/          # Models (simplified/full/lowrank), configurations, core interfaces
├─ optimizer/      # PSO tuner
├─ utils/          # Validation, control primitives, monitoring, visualization, analysis
└─ hil/            # Plant server, controller client

Top-level: simulate.py, streamlit_app.py, config.yaml, requirements.txt
```

------

## 6) Educational Materials (.ai/edu)

**Purpose**: Learning roadmaps for users at all skill levels, separate from project-specific documentation.

**Directory**: `.ai_workspace/edu/` (Educational content, managed by Claude Code)

### 6.1 Available Resources

**Beginner Roadmap** (`.ai_workspace/edu/beginner-roadmap.md`):
- **Target**: Complete beginners with ZERO coding/control theory background
- **Duration**: 125-150 hours over 4-6 months
- **Coverage**: Phase 1 (Computing, Python, Physics, Math) -> Phase 2 (Control theory, SMC) -> Phases 3-5 (Hands-on to mastery)
- **Status**: Phases 1-2 complete (~2,000 lines), Phases 3-5 planned (~1,500-2,000 more lines)

### 6.2 Integration with Main Documentation

**Learning Path Progression**:
```bash
Path 0: Complete Beginner (NEW)
  .ai_workspace/education/beginner-roadmap.md (125-150 hours) ->

Path 1: Quick Start (EXISTING)
  docs/guides/getting-started.md -> Tutorial 01 (1-2 hours) ->

Paths 2-4: Advanced (EXISTING)
  Tutorials 02-05, Theory, Research workflows
```

**Audience Segmentation**:
- `.ai_workspace/edu/` -> Prerequisites for absolute beginners (Path 0)
- `docs/guides/` -> Project-specific documentation (Paths 1-4)

**Cross-References**:
- Phase 5 of beginner roadmap connects to Tutorial 01
- Getting started guide links to beginner roadmap for prerequisites
- INDEX.md includes Path 0 reference

### 6.3 Future Educational Content

**Planned**:
- Intermediate roadmap (advanced control theory, Python)
- Quick reference cheatsheets (Python, Git, CLI)
- Video curriculum (curated YouTube playlists)
- Exercise solutions (worked examples)
- FAQ for beginners

**See**: `.ai_workspace/edu/README.md` for complete details

### 6.4 NotebookLM Podcast Generation (NEW - Nov 2025)

**Purpose**: Convert educational content into podcast-style audio for commute/exercise learning

**Available Series**: 44 episodes (Phases 1-4), ~40 hours audio, 125 hours learning content

**Status**: [OK] Series complete at Phase 4 (November 2025)

**See**: `.ai_workspace/guides/notebooklm_guide.md` for complete TTS optimization requirements, episode templates, validation checklists, phase examples, and usage workflows

------

## 7) Key Technologies

- Python 3.9+
- NumPy, SciPy, Matplotlib
- Numba for vectorized/batch simulation
- PySwarms / Optuna for optimization (PSO primary)
- Pydantic‑validated YAML configs
- pytest + pytest‑benchmark; Hypothesis where useful
- Streamlit for UI

------

## 8) Usage & Essential Commands

### 8.1 Simulations

```bash
python simulate.py --ctrl classical_smc --plot
python simulate.py --ctrl sta_smc --plot
python simulate.py --load tuned_gains.json --plot
python simulate.py --print-config
```

### 8.2 PSO Optimization

```bash
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json
python simulate.py --ctrl adaptive_smc --run-pso --seed 42 --save gains_adaptive.json
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --save gains_hybrid.json
```

### 8.3 HIL

```bash
python simulate.py --run-hil --plot
python simulate.py --config custom_config.yaml --run-hil
```

### 8.4 Testing

```bash
python run_tests.py
python -m pytest tests/test_controllers/test_classical_smc.py -v
python -m pytest tests/test_benchmarks/ --benchmark-only
python -m pytest tests/ --cov=src --cov-report=html
```

### 8.5 Web Interface

```bash
streamlit run streamlit_app.py
```

------

## 9) Configuration System

- Central `config.yaml` with strict validation.
- Domains: physics params, controller settings, PSO parameters, simulation settings, HIL config.
- Prefer "configuration first": define parameters before implementation changes.

------

## 10) Development Guidelines

### 10.1 Code Style

- Type hints everywhere; clear, example‑rich docstrings.
- ASCII header format for Python files (≈90 chars width).
- Explicit error types; avoid broad excepts.
- Use informal, conversational comments that explain the "why" behind the code, similar to the style in `requirements.txt`.

### 10.2 Adding New Controllers

1. Implement in `src/controllers/`.
2. Add to `src/controllers/factory.py`.
3. Extend `config.yaml`.
4. Add tests under `tests/test_controllers/`.

### 10.3 Batch Simulation

```python
from src.core.vector_sim import run_batch_simulation
results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)
```

### 10.4 Configuration Loading

```python
from src.config import load_config
config = load_config("config.yaml", allow_unknown=False)
```

------

## 11) Testing & Coverage Standards

**See:** `.ai_workspace/config/testing_standards.md` for complete details.

**Quick Reference:**
- Overall: ≥85% | Critical components: ≥95% | Safety‑critical: 100%
- Every `.py` file has a `test_*.py` peer
- Validate theoretical properties for critical algorithms

------

## 12) Visualization & Analysis Toolkit

- Real‑time animations (DIPAnimator), static performance plots, project movie generator.
- Statistical analysis: confidence intervals, bootstrap, Welch's t‑test, ANOVA, Monte Carlo.
- Real‑time monitoring (latency, deadline misses, weakly‑hard constraints) for control loops.

------

## 13) Production Safety & Readiness (phase 4 Status)

**See:** `.ai_workspace/guides/phase4_status.md` for complete status.

**Quick Reference:**
- Production Readiness: 23.9/100 (Phase 4.1+4.2 complete)
- Thread Safety: 100% (11/11 tests passing)
- Status: RESEARCH-READY [OK] | NOT production-ready [ERROR]

### Current Status: Research-ready [ok]

**Safe for Research/Academic Use**: Single-threaded & multi-threaded operation validated, controllers functional and tested, documentation complete

**NOT Ready for Production**: Quality gates 1/8 passing, coverage measurement broken, production score 23.9/100

## Production Readiness Reports

### Phase 5: Research Phase (october 29 - November 7, 2025)

**Status**: [OK] COMPLETE (11/11 tasks, 100%)
**Focus**: Validate, document, and benchmark 7 controllers
**Roadmap**: 72 hours over 8 weeks - COMPLETED
- Week 1 (8h): benchmarks, chattering metrics, visualization - COMPLETE
- Weeks 2-4 (18h): comprehensive benchmark, boundary layer optimization - COMPLETE
- Months 2-3 (46h): Lyapunov proofs, model uncertainty, research paper - COMPLETE

**Completed Tasks**:
- QW-1 through QW-5 (quick wins: theory docs, benchmarks, PSO viz, chattering, status updates)
- MT-5, MT-6, MT-7, MT-8 (medium-term: comprehensive benchmarks, boundary layer, robust PSO, disturbances)
- LT-4, LT-6, LT-7 (long-term: Lyapunov proofs, model uncertainty, research paper)

**Final Deliverable**: LT-7 research paper SUBMISSION-READY (v2.1) with 14 figures, automation scripts, comprehensive bibliography

**See Also**: `.ai_workspace/planning/research/RESEARCH_COMPLETION_SUMMARY.md` | `.ai_workspace/planning/CURRENT_STATUS.md`

------

## 14) Workspace Organization & Hygiene

**See:** `.ai_workspace/guides/workspace_organization.md` for complete details.

**Quick Reference:**
- Target: ≤19 visible root items, ≤100MB academic/logs/
- Current: 22 visible items, academic/logs/ 13MB [OK] (Dec 29, 2025)
- Centralized log paths: `src/utils/logging/paths.py` (single source of truth)
- Use `.ai_workspace/` for ALL AI/dev configs (CANONICAL)
- Use `academic/` for THREE-CATEGORY STRUCTURE (paper/, logs/, dev/)
  - `academic/paper/` [202 MB] - Research papers, thesis, documentation
  - `academic/logs/` [13 MB] - Runtime and development logs
  - `academic/dev/` [46 MB] - QA audits, coverage reports, caches
- Use `.cache/` for project root ephemeral data
- Use `D:\Tools\Claude\` for system-level external tools (account switcher)
- Migration guide: `academic/paper/README.md`, `academic/logs/README.md`, `academic/dev/README.md`

### Config Consolidation (Use `.ai_workspace/` as CANONICAL)
```bash
.ai_workspace/                     # CANONICAL CONFIG ROOT
├─ config/                         # Configuration files
│  ├─ claude/                      # Claude Code settings
│  └─ mcp/                         # MCP server configs
├─ tools/                          # Development scripts (CANONICAL)
├─ guides/                         # AI operation guides
├─ planning/                       # Project planning docs
├─ education/                      # Educational materials
├─ state/                          # Project state tracking
└─ archive/                        # Archived artifacts
```

### DO NOT USE (deprecated Aliases)
- [ERROR] `.project/` -> migrated to `.ai_workspace/` (Dec 29, 2025)
- [ERROR] `.ai/` -> migrated to `.ai_workspace/` or `academic/archive/` (Dec 29, 2025)
- [ERROR] `.artifacts/` -> migrated to `academic/` (visible directory)
- [ERROR] `.logs/` -> migrated to `academic/logs/` (visible directory)

### Directory Rules
- **Academic outputs**: `academic/` (THREE-CATEGORY STRUCTURE - reorganized Dec 29, 2025)
  - **paper/** [~202 MB] - Research papers, thesis, documentation
    - `thesis/` [98 MB] - LaTeX thesis source and PDFs
    - `research/` [28 MB] - Research papers, experiments, phase data
    - `docs/` [64 MB] - Sphinx documentation build outputs
    - `archive/` [12 MB] - Archived research artifacts
    - `data/` [3 KB] - Simulation and research data
  - **logs/** [~13 MB] - Runtime and development logs
    - `benchmarks/` [~10 MB] - Research task execution logs
    - `pso/` [978 KB] - PSO optimization logs
    - `docs_build/` [352 KB] - Sphinx build logs
    - `monitoring/` - Runtime monitoring logs
    - `test/` - Test execution logs
    - `migration/` - Migration logs
    - `archive/` [214 KB] - Compressed historical logs
  - **dev/** [~46 MB] - Development artifacts
    - `quality/` [46 MB] - QA audits, coverage reports
    - `caches/` [133 KB] - Pytest, hypothesis, benchmark caches
- **AI workspace**: `.ai_workspace/` (AI operation configs, tools, guides - HIDDEN directory)
  - `tools/` - Development and recovery scripts
  - `guides/` - AI operation documentation
  - `planning/` - Project planning and roadmaps
  - `state/` - Project state tracking
  - `config/` - Claude and MCP configurations
- **Runtime caches**: `.cache/` (pytest, hypothesis, htmlcov, benchmarks - project root caches)
- **Visible directories** (core): `src/`, `tests/`, `academic/`, `scripts/`, `data/`, `benchmarks/`, `optimization_results/`
- **Root files** (9 core + 2 MCP): `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `config.yaml`, `requirements.txt`, `simulate.py`, `streamlit_app.py`, `package.json`, `package-lock.json`
- **Benchmarks organization** (reorganized Dec 18, 2025):
  - `benchmarks/raw/` - Immutable original outputs by research task (MT-5, baselines, etc.)
  - `benchmarks/processed/` - Derived/aggregated analysis datasets
  - `benchmarks/figures/` - Publication-ready plots (PRESERVED PATH)
  - `benchmarks/reports/` - Task completion summaries
  - `src/benchmarks/` - Analysis modules (moved from benchmarks/ root for proper package structure)
  - `.logs/benchmarks/` - Log files (9.7 MB, hidden directory)
  - Import changes: `from benchmarks.*` → `from src.benchmarks.*` (auto-updated)

### Recent Reorganization

**Dec 29, 2025 - Academic Folder Reorganization (THREE-CATEGORY STRUCTURE):**
- [OK] Created three top-level categories: paper/, logs/, dev/
- [OK] paper/ consolidation (202 MB total):
  - thesis/ [98 MB], research/ [28 MB], docs/ [64 MB], archive/ [12 MB], data/ [3 KB]
  - Flattened nested structures: docs/docs/ → docs/, research/papers/papers/ → research/papers/
- [OK] logs/ reorganization (13 MB total):
  - Flattened .logs/ → logs/ (merged nested structure)
  - Added migration/ subdirectory for migration logs
  - Moved archive/docs_build/logs/ → logs/docs_build/
- [OK] dev/ consolidation (46 MB total):
  - quality/ [46 MB] - QA audits, coverage reports
  - caches/ [133 KB] - Pytest, hypothesis, benchmark caches
- [OK] Cleanup: Deleted 294 MB backup file (52% size reduction)
- [OK] Cleanup: Removed redundant archive backups (4.6 MB saved)
- [OK] README files created for paper/, logs/, dev/
- [OK] Updated CLAUDE.md Section 14 with new structure
- [OK] Git history preserved: All moves use git mv

**Dec 29, 2025 - AI Workspace Migration:**
- [OK] .project/ → .ai_workspace/ (complete AI workspace consolidation)
- [OK] .project/ai/ subdirectories → .ai_workspace/ (planning, guides, education, issues, testing, quality, orchestration, collaboration, ultrathink_sessions)
- [OK] .project/tools/ → .ai_workspace/tools/ (recovery scripts, checkpoints, automation)
- [OK] .project/config/ → .ai_workspace/config/ (claude, mcp)
- [OK] .project/state/ → .ai_workspace/state/ (project state tracking)
- [OK] .ai/paper_enhancement_plans → academic/archive/ (historical research plans)
- [OK] Documentation updated: CLAUDE.md path references, .ai_workspace/ markdown files
- [OK] Cleanup: Removed .project/, .ai/, .benchmarks/, malformed files, Python cache
- [OK] Git history preserved: All migrations use git mv

**Dec 18, 2025 - Benchmarks:**
- [OK] benchmarks/ → Publication-ready structure (raw/, processed/, figures/, reports/)
- [OK] benchmarks/{analysis,benchmark,comparison} → src/benchmarks/ (proper package structure)
- [OK] benchmarks/*.log → .logs/benchmarks/ (9.7 MB logs centralized)
- [OK] 8 README files added with research task provenance
- [OK] 567 files scanned, 8 modified, imports auto-updated

**Dec 19, 2025 - docs/ Directory:**
- [OK] docs/ → Clean root structure (102 root files → 5 core files, 95% reduction)
- [OK] Moved 70 markdown files to 8 categorized subdirectories (theory/, optimization/, production/, testing/, architecture/, guides/, reference/, meta/)
- [OK] Moved 15 build artifacts to .artifacts/docs_build/logs/
- [OK] Moved 6 scripts to .ai_workspace/tools/validation/docs/ and .ai_workspace/tools/docs/
- [OK] Moved 8 data files to docs/_data/, docs/bib/, docs/_static/pwa/
- [OK] Deleted 1 obsolete backup file; 564 total markdown files now organized

**Dec 19, 2025 - Root Directory Cleanup:**
- [OK] Root cleanup → 22 visible items → 18 items (exceeds ≤19 target)
- [OK] Deleted build artifacts: __pycache__/, nul
- [OK] Moved test artifacts: coverage.xml → .cache/coverage/, report.log → .logs/
- [OK] Workspace health: 18 visible items (1 below target, 99% reorganization value achieved)
- [OK] Documented deferrals: tests/ (HIGH risk, deferred) + data/ (zero benefit, skipped)
- [OK] Backlog created: .ai_workspace/planning/BACKLOG.md

**Dec 19, 2025 - Scripts Directory:**
- [OK] scripts/ → Publication-ready structure (21 root files → 5 root files, 73% reduction)
- [OK] Consolidated duplicate directories: documentation/ + docs_organization/ → docs/
- [OK] Created categorized subdirectories: testing/, infrastructure/, utils/
- [OK] 18 files moved with git mv (history preserved), 4 files updated (path/import fixes)
- [OK] 195 Python scripts across 21 categorized subdirectories
- [OK] Migration docs: scripts/README.md, scripts/MIGRATION_HISTORY.md

**Dec 19, 2025 - Logs/Monitoring + Optimization Results:**
- [OK] monitoring_data/ (56MB) → .logs/archive/ (compressed to 214KB, 99.6% reduction)
- [OK] 13 PSO logs (978KB) → .logs/pso/ (from optimization_results/)
- [OK] optimization_results/ restructured: active/, phases/, analysis_results/, archive/
- [OK] Removed 1 visible directory (monitoring_data/), 22 visible items total
- [OK] .logs/ size: 12MB (under 100MB target)

**Dec 17, 2025 - Workspace:**
- [OK] thesis/ (98MB) → .artifacts/thesis/
- [OK] logs/ → .logs/ (hidden, centralized logging)
- [OK] notebooks/ → docs/tutorials/notebooks/
- [OK] Research outputs from benchmarks/ → .artifacts/research/
- [OK] Scripts organized: 55 → 15 at root, 40 in subdirectories (superseded by Dec 19 reorganization)

### Protected Files (never Delete)
- `D:\Tools\Claude\Switch-ClaudeAccount.ps1` - Multi-account switcher (EXTERNAL LOCATION)

### Weekly Health Check
```bash
ls | wc -l                                          # ≤19 visible items (current: 22)
find . -maxdepth 1 -type d -name ".*" | wc -l      # ≤9 hidden dirs (current: 9)
du -sh .cache/                                      # <50MB
du -sh .artifacts/                                  # <150MB (includes 98MB thesis)
du -sh .logs/                                       # <100MB (current: 12MB)
```

### Automatic Cleanup Policy (MANDATORY)

**CRITICAL RULE - PROFESSIONAL CLEANUP:**
- **ALWAYS cleanup** folder after creating/editing multiple files
- **NEVER leave** intermediate versions, test files, or build artifacts at root level
- **Action:** Create/Edit files -> Archive old versions -> Add README.md -> Commit
- **Target:** ≤5 active files at folder root (final deliverables only)

**Cleanup Principles:**

1. **Archive Structure** - Create subdirectories for organization:
   - `archive/old_versions/` - Previous iterations (PDFs, source files)
   - `archive/planning/` - Planning docs, progress reports, completion summaries
   - `archive/test_files/` - Test compilations and validation files
   - `archive/build_artifacts/` - Compiler outputs (.aux, .log, .toc, .out, etc.)

2. **Keep at Root** - Only essential deliverables:
   - Final output files (e.g., `PROJECT_FINAL.pdf`, `PROJECT_FINAL.tex`)
   - Active source files (e.g., `PROJECT.md`, `PROJECT.bib`)
   - Documentation (`README.md`, `CHECKLIST.md`, `MANUAL.md`)

3. **Archive Pattern** - Move intermediate files:
   ```bash
   # Old versions
   mv PROJECT_v1.pdf PROJECT_v2.pdf archive/old_versions/

   # Test files
   mv TEST_*.pdf TEST_*.tex archive/test_files/

   # Build artifacts
   mv *.aux *.log *.toc *.out archive/build_artifacts/

   # Planning docs
   mv *_PLAN.md *_REPORT.md *_SUMMARY.md archive/planning/
   ```

4. **README Creation** - Always create `README.md` with:
   - Section: Final Deliverables (list primary outputs with sizes)
   - Section: Source Files (working files, databases)
   - Section: Submission Materials (if applicable)
   - Section: Archive Structure (describe subdirectories)
   - Section: Status (completion date, version, quality metrics)
   - Section: Usage (how to compile/run/view outputs)

5. **Verification** - Before committing:
   ```bash
   ls -lah                    # Verify root has ≤5 core files
   ls archive/*/              # Verify archive structure
   cat README.md              # Verify documentation complete
   ```

**Example: Research Paper Cleanup**
```bash
# BEFORE: 95 files at root (messy)
# AFTER: 12 files at root + archive/ subdirectories (professional)
#
# Root structure:
# - PAPER_FINAL.pdf (final output)
# - PAPER_FINAL.tex (LaTeX source)
# - PAPER.md (markdown master)
# - PAPER.bib (bibliography)
# - README.md (documentation)
# - CHECKLIST.md (submission guide)
# - archive/ (old versions, planning, tests, build artifacts)
```

**When to Cleanup:**
- [MANDATORY] After completing any multi-file creation task
- [MANDATORY] After PDF/LaTeX compilation creates build artifacts
- [MANDATORY] After iterative development creates v1, v2, v3 versions
- [MANDATORY] Before committing changes to repository
- [RECOMMENDED] Weekly during active development

**See Also**: `.ai_workspace/archive/RESTRUCTURING_PLAN_2025-10-26.md` | `.ai_workspace/archive/WORKSPACE_CLEANUP_2025-10-26.md`

------

## 15) Controller Memory Management

**See:** `.ai_workspace/config/controller_memory.md` for complete details.

**Quick Reference:**
- All controllers use weakref patterns to prevent circular references
- Explicit `cleanup()` methods available for all controller types
- Memory leak prevention: periodic reset + monitoring in production
- Validation: `pytest tests/test_integration/test_memory_management/ -v`

------

## 16) Controller Factory & Example Snippets

```python
# Example-metadata
# Runnable: False

from src.controllers.factory import create_controller
controller = create_controller(
  'classical_smc',
  config=controller_config,
  gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
)
control_output = controller.compute_control(state, last_control, history)
# Optimization (pso)
from src.optimizer.pso_optimizer import PSOTuner
# ... Initialize Bounds, Tuner, and Run Pso.optimize(...)
# Monitoring
from src.utils.monitoring.latency import LatencyMonitor
monitor = LatencyMonitor(dt=0.01)
start = monitor.start()
# ... Loop
missed = monitor.end(start)
```

------

## 17) Multi-agent Orchestration System

**See:** `.ai_workspace/config/agent_orchestration.md` for complete details.

**Quick Reference:**
- 6-agent parallel orchestration workflow (Ultimate Orchestrator pattern)
- Automatic coordination for complex multi-domain tasks
- Subordinate agents: Integration, Control Systems, PSO, Documentation, Code Beautification
- Quality gates: ≥95% coverage critical, ≥85% overall, ≥7/8 system health

**Checkpoint System Integration (NEW - Oct 2025):**
- All multi-agent tasks MUST use checkpoint system
- Checkpoints prevent loss of work on token limits/crashes
- Recovery script automatically detects incomplete agent work
- See: `.ai_workspace/config/agent_checkpoint_system.md` for usage guide

**Mandatory Checkpoint Calls:**
```python
# When User Approves Plan
checkpoint_plan_approved(task_id, plan_summary, hours, agents, deliverables)

# When Launching Each Agent
checkpoint_agent_launched(task_id, agent_id, role, hours)

# Every 5-10 Minutes During Agent Execution
checkpoint_agent_progress(task_id, agent_id, hours_completed, deliverables, current_phase)

# When Agent Completes or Fails
checkpoint_agent_complete(task_id, agent_id, hours, deliverables, summary)
checkpoint_agent_failed(task_id, agent_id, hours, reason, recovery_recommendation)
```

------

## 18) Documentation Quality Standards

**See:** `.ai_workspace/config/documentation_quality.md` for complete details.

**Quick Reference:**
- Direct, not conversational (avoid "Let's explore...")
- Specific, not generic (no "comprehensive" without metrics)
- Technical, not marketing (facts over enthusiasm)
- Run: `python scripts/docs/detect_ai_patterns.py --file <file.md>`
- Target: <5 AI-ish patterns per file

------

## 19) Documentation Build System

**See:** `.ai_workspace/guides/documentation_build_system.md` for complete workflow.

**MANDATORY FOR CLAUDE**: After ANY documentation changes, rebuild and verify.

### Rebuild Workflow
```bash
# 1. Make Changes to Docs
# 2. ALWAYS Rebuild
sphinx-build -M html docs docs/_build -W --keep-going

# 3. Verify Changes Copied
stat docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 4. Verify Localhost Serves New Version
curl -s "http://localhost:9000/_static/your-file.css" | grep "YOUR_CHANGE"

# 5. Tell User to Hard Refresh Browser (ctrl+shift+r)
```

## Overview

### Auto-rebuild Triggers
- Sphinx source files: `docs/*.md`, `docs/**/*.rst`
- Static assets: `docs/_static/*.css`, `docs/_static/*.js`, `docs/_static/*.png`
- Configuration: `docs/conf.py`, `docs/_templates/*`
- Navigation: `docs/index.rst`, any `toctree` directives

### Common Pitfalls
[ERROR] Don't assume changes are live - verify with `curl` or `stat`
[ERROR] Don't skip rebuild - Sphinx doesn't auto-rebuild static files
[ERROR] Don't forget browser cache - tell user to hard refresh

[OK] Do verify timestamps - `stat` both source and build files
[OK] Do check MD5 sums - ensure files actually copied
[OK] Do test with curl - verify localhost serves new content

------

## 20) Model Context Protocol (mcp) Auto-triggers

**See:** `.ai_workspace/guides/mcp_usage_guide.md` for complete guide | `docs/mcp-debugging/README.md` for workflows

**For Claude:** Auto-trigger MCPs based on task keywords (NO user confirmation needed).

**For Users:** Just ask naturally! No special keywords required.

### Quick Reference: Available MCP Servers (12 Total)

**Core Servers**: filesystem (file ops), github (issues/PRs), sequential-thinking (planning/debugging), puppeteer (UI testing), pytest-mcp (test debugging), git-mcp (advanced Git), sqlite-mcp (PSO DB), mcp-analyzer (code quality), lighthouse-mcp (audits), pandas-mcp (data analysis), numpy-mcp (numerical compute), mcp-debugger (API testing)

**Auto-Trigger Strategy**: Chain 3-5 MCPs for complete workflows. Use sequential-thinking for planning, filesystem+Grep for search, pytest-mcp for debugging.

**Common Workflows**:
- Data Analysis: filesystem -> sqlite-mcp -> pandas-mcp
- Testing: pytest-mcp -> puppeteer -> mcp-analyzer
- Research: Grep -> filesystem -> git-mcp -> pandas-mcp

**Configuration:** `.mcp.json` (12 servers) | **See**: `.ai_workspace/guides/mcp_usage_guide.md` for complete auto-trigger keywords and orchestration patterns

------

## 21) Phase 3 Ui/ux Status & Maintenance Mode

**See:** `.ai_workspace/guides/phase3_status.md` for complete status.

**Quick Reference:**
- Phase 3: [OK] COMPLETE (34/34 issues, October 9-17, 2025)
- Status: Merged to main | UI work in MAINTENANCE MODE
- Achievement: WCAG 2.1 Level AA, 18 design tokens, 4 breakpoints validated
- Browser: Chromium validated [OK] | Firefox/Safari deferred [PAUSE]

**UI Maintenance Mode Policy:**
- **DO**: Fix critical bugs, update docs for new features, maintain WCAG AA
- **DON'T**: Proactive enhancements, Firefox/Safari validation, "nice-to-have" polish
- **Focus**: 80-90% time on research (controllers, PSO, SMC theory)

**See Also**: `.ai_workspace/planning/phase3/HANDOFF.md` for handoff document

------

## 22) Success Criteria

- Clean root (≤ 12 visible entries), caches removed, backups archived.
- Test coverage gates met (85% overall / 95% critical / 100% safety‑critical).
- Single‑threaded operation stable; no dependency conflicts; memory bounded.
- Clear, validated configuration; reproducible experiments.
- MCP servers auto-trigger for appropriate tasks; all 12 servers operational.

------

## 23) Documentation Navigation System

**See:** `docs/NAVIGATION.md` for master navigation hub.

**Quick Reference:**
- Total Documentation: 985 files (814 in docs/, 171 in .ai_workspace/)
- Navigation Systems: 11 total (NAVIGATION.md is the master hub)
- Category Indexes: 43 index.md files across all documentation domains
- Learning Paths: 5 paths (Path 0: 125-150 hrs -> Path 4: 12+ hrs)

**Primary Navigation Hub:**
- [NAVIGATION.md](docs/NAVIGATION.md) - Master hub connecting all 11 navigation systems
  - "I Want To..." quick navigation (6 intent categories)
  - Persona-based entry points (4 user types)
  - Complete category index directory (43 indexes)
  - Visual navigation tools (6 interactive systems)
  - Attribution & cross-references (citations, dependencies, patterns)

**Navigation Systems**: 11 total including NAVIGATION.md (master hub), docs/index.md (Sphinx), guides/INDEX.md, README.md, 3 visual sitemaps, 2 interactive demos

**User Journeys**: 5 learning paths from Complete Beginners (Path 0: 125-150 hrs) to Advanced (Path 4: 12+ hrs)

------

## 24) Task Wrapper & Checkpoint System for Multi-Agent Orchestration

**Quick Reference:**
- Automatic checkpointing for Task tool invocations
- Survives token limits, crashes, session interruptions
- Zero-friction recovery: `/recover` + `/resume` commands
- Output preservation: agent work saved to `.artifacts/`

**Usage**:
```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch
result = checkpoint_task_launch(task_id="LT-4", agent_id="agent1", task_config={...}, role="...")
```

**Recovery**: `/recover` -> `/resume LT-4 agent1` -> verify completion

**Status**: [OK] Operational (November 2025)

**See**: `.ai_workspace/tools/checkpoints/TASK_WRAPPER_USAGE.md` for complete guide, code examples, multi-agent patterns, and configuration options

**See Also**: `.ai_workspace/guides/agent_checkpoint_system.md` (design), `.ai_workspace/guides/agent_orchestration.md` (patterns)

------

### Appendix: Notes

- Keep this file authoritative for style, testing, and operational posture.
- Treat it as versioned team memory; update via PRs with a short change log.
- **CRITICAL**: All git operations must target: https://github.com/theSadeQ/dip-smc-pso.git
- **MANDATORY**: Automatic updates are REQUIRED for all repository changes
- Maintain clean, professional commit messages following the established pattern
