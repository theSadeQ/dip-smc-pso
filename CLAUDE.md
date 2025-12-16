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

**See:** `.ai/config/repository_management.md` for complete details.

**Quick Reference:**
- MANDATORY: Auto-commit and push after ANY repository changes
- Commit message format: `<Action>: <Brief description>` with [AI] footer
- Always verify remote URL: `https://github.com/theSadeQ/dip-smc-pso.git`

------

## 3) Session Continuity & Project-wide Recovery System

**See:** `.project/ai/config/session_continuity.md` for complete details.

**Purpose:** 30-second recovery from token limits or multi-month gaps

**Status:** [OK] Operational (Oct 2025)

### Quick Recovery
```bash
# One-command Recovery After Token Limit
/recover

# Or Manually
bash .project/dev_tools/recover_project.sh

# Check Roadmap Progress
python .project/dev_tools/roadmap_tracker.py
```

### Multi-Account Recovery (NEW - Nov 2025)

**Quick Start**: Windows: `.project\dev_tools\quick_recovery.bat` | Linux/Mac: `bash .project/dev_tools/recover_project.sh && python .project/dev_tools/analyze_checkpoints.py`

**See**: `.project/dev_tools/MULTI_ACCOUNT_RECOVERY_GUIDE.md` for complete workflow

### Key Tools
1. **Project State Manager** (`.project/dev_tools/project_state_manager.py`) - Tracks phase, roadmap progress, completed tasks
2. **Git Recovery Script** (`.project/dev_tools/recover_project.sh`) - 30-second recovery workflow
3. **Roadmap Tracker** (`.project/dev_tools/roadmap_tracker.py`) - Parses 72-hour research roadmap (50 tasks)
4. **Agent Checkpoint System** (`.project/dev_tools/agent_checkpoint.py`) - Recovers interrupted multi-agent work
5. **Multi-Account Recovery** (`.project/dev_tools/MULTI_ACCOUNT_RECOVERY_GUIDE.md`) - Resume work across accounts/sessions

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

A Python framework for simulating, controlling, and analyzing a double‑inverted pendulum (DIP) system. It provides multiple SMC variants, optimization (PSO), a CLI and a Streamlit UI, plus 85%+ test coverage and 12,500+ lines of documentation.

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

**Directory**: `.ai/edu/` (Educational content, managed by Claude Code)

### 6.1 Available Resources

**Beginner Roadmap** (`.ai/edu/beginner-roadmap.md`):
- **Target**: Complete beginners with ZERO coding/control theory background
- **Duration**: 125-150 hours over 4-6 months
- **Coverage**: Phase 1 (Computing, Python, Physics, Math) -> Phase 2 (Control theory, SMC) -> Phases 3-5 (Hands-on to mastery)
- **Status**: Phases 1-2 complete (~2,000 lines), Phases 3-5 planned (~1,500-2,000 more lines)

### 6.2 Integration with Main Documentation

**Learning Path Progression**:
```bash
Path 0: Complete Beginner (NEW)
  .ai/edu/beginner-roadmap.md (125-150 hours) ->

Path 1: Quick Start (EXISTING)
  docs/guides/getting-started.md -> Tutorial 01 (1-2 hours) ->

Paths 2-4: Advanced (EXISTING)
  Tutorials 02-05, Theory, Research workflows
```

**Audience Segmentation**:
- `.ai/edu/` -> Prerequisites for absolute beginners (Path 0)
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

**See**: `.ai/edu/README.md` for complete details

### 6.4 NotebookLM Podcast Generation (NEW - Nov 2025)

**Purpose**: Convert educational content into podcast-style audio for commute/exercise learning

**Available Series**: 44 episodes (Phases 1-4), ~40 hours audio, 125 hours learning content

**Status**: [OK] Series complete at Phase 4 (November 2025)

**See**: `.project/ai/config/notebooklm_guide.md` for complete TTS optimization requirements, episode templates, validation checklists, phase examples, and usage workflows

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

**See:** `.ai/config/testing_standards.md` for complete details.

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

**See:** `.project/ai/config/phase4_status.md` for complete status.

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
- Weeks 2-4 (18h): multi-controller benchmark, boundary layer optimization - COMPLETE
- Months 2-3 (46h): Lyapunov proofs, model uncertainty, research paper - COMPLETE

**Completed Tasks**:
- QW-1 through QW-5 (quick wins: theory docs, benchmarks, PSO viz, chattering, status updates)
- MT-5, MT-6, MT-7, MT-8 (medium-term: multi-controller benchmarks, boundary layer, PSO with validation, disturbances)
- LT-4, LT-6, LT-7 (long-term: Lyapunov proofs, model uncertainty, research paper)

**Final Deliverable**: LT-7 research paper SUBMISSION-READY (v2.1) with 14 figures, automation scripts, bibliography (68 citations)

**See Also**: `.project/ai/planning/research/RESEARCH_COMPLETION_SUMMARY.md` | `.project/ai/planning/CURRENT_STATUS.md`

------

## 14) Workspace Organization & Hygiene

**See:** `.project/ai/config/workspace_organization.md` for complete details.

**Quick Reference:**
- Target: ≤19 visible root items, ≤3 hidden dirs
- Use `.project/` for ALL AI/dev configs (CANONICAL)
- Runtime artifacts ARCHIVED externally (no .artifacts/ in repo)
- Use `.cache/` for ephemeral data (regenerable only)

### Config Consolidation (Use `.project/` as CANONICAL)
```bash
.project/                          # CANONICAL CONFIG ROOT
├─ ai/config/                     # AI configurations
├─ claude/                        # Claude Code settings
├─ dev_tools/                     # Development scripts (CANONICAL)
└─ archive/                       # Archived artifacts
```

### DO NOT USE (deprecated Aliases)
- [ERROR] `.ai/` -> use `.project/ai/`
- [ERROR] `.dev_tools/` at root -> use `.project/dev_tools/`

### Directory Rules
- **Hidden directories** (3): `.git/` (essential), `.github/` (CI/CD workflows), `.project/` (canonical config root)
- **Runtime caches**: `.cache/` (pytest, hypothesis - regenerable only, NOT in git)
- **Visible directories** (9): `src/`, `tests/`, `docs/`, `scripts/`, `benchmarks/`, `optimization_results/`, `thesis/`, `research/`, `logs/`
  - `scripts/research/{mt6_boundary_layer,mt7_robustness,mt8_reproducibility,lt6_model_uncertainty,lt7_paper}/` - Research task scripts
  - `scripts/optimization/` - PSO tuning and monitoring
  - `scripts/testing/` - Test automation and validation
  - `scripts/debug/` - Debug and verification scripts
  - `scripts/monitoring/` - PSO and system monitoring scripts
  - `scripts/fixes/` - One-off fix scripts
  - `scripts/docs/` - Documentation build and maintenance
  - `scripts/benchmarks/` - Performance benchmarking
  - `scripts/coverage/` - Coverage analysis
- **Root files** (3 core + 5 config + 2 MCP):
  - Core: `README.md`, `CHANGELOG.md`, `CLAUDE.md`
  - Config: `config.yaml`, `requirements.txt`, `setup.py`, `simulate.py`, `streamlit_app.py`
  - MCP: `package.json`, `package-lock.json`

### Protected Files (never Delete)
- `.project/dev_tools/Switch-ClaudeAccount.ps1` - Multi-account switcher (CANONICAL)

### Weekly Health Check
```bash
ls | wc -l                                          # ≤19 visible items
find . -maxdepth 1 -type d -name ".*" | wc -l      # ≤3 hidden dirs (.git, .github, .project)
du -sh .cache/                                      # <10MB (regenerable only)
du -sh .project/                                    # <5MB (config + active dev tools only)
```

### Post-Audit Status (December 16, 2025)
- **Hidden directories**: 3 [OK] (.git/, .github/, .project/)
- **Visible directories**: 9 [OK] (removed monitoring_data/)
- **.project/ size**: ~1.5MB (reduced from 6.4MB, -77%)
- **External archive**: ~250MB (caches, old docs, historical artifacts)
- **Space savings**: ~410MB total (160MB deleted regenerable, 250MB archived)

**See Also**: `.project/dev_tools/RESTRUCTURING_PLAN_2025-10-26.md` | `.project/ai/config/WORKSPACE_CLEANUP_2025-10-26.md`

------

## 15) Controller Memory Management

**See:** `.ai/config/controller_memory.md` for complete details.

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

**See:** `.ai/config/agent_orchestration.md` for complete details.

**Quick Reference:**
- 6-agent parallel orchestration workflow (Ultimate Orchestrator pattern)
- Automatic coordination for complex multi-domain tasks
- Subordinate agents: Integration, Control Systems, PSO, Documentation, Code Beautification
- Quality gates: ≥95% coverage critical, ≥85% overall, ≥7/8 system health

**Checkpoint System Integration (NEW - Oct 2025):**
- All multi-agent tasks MUST use checkpoint system
- Checkpoints prevent loss of work on token limits/crashes
- Recovery script automatically detects incomplete agent work
- See: `.ai/config/agent_checkpoint_system.md` for usage guide

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

**See:** `.ai/config/documentation_quality.md` for complete details.

**Quick Reference:**
- Direct, not conversational (avoid "Let's explore...")
- Specific, not generic (no "comprehensive" without metrics)
- Technical, not marketing (facts over enthusiasm)
- Run: `python scripts/docs/detect_ai_patterns.py --file <file.md>`
- Target: <5 AI-ish patterns per file

------

## 19) Documentation Build System

**See:** `.project/ai/config/documentation_build_system.md` for complete workflow.

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

**See:** `.project/ai/config/mcp_usage_guide.md` for complete guide | `docs/mcp-debugging/README.md` for workflows

**For Claude:** Auto-trigger MCPs based on task keywords (NO user confirmation needed).

**For Users:** Just ask naturally! No special keywords required.

### Quick Reference: Available MCP Servers (12 Total)

**Core Servers**: filesystem (file ops), github (issues/PRs), sequential-thinking (planning/debugging), puppeteer (UI testing), pytest-mcp (test debugging), git-mcp (advanced Git), sqlite-mcp (PSO DB), mcp-analyzer (code quality), lighthouse-mcp (audits), pandas-mcp (data analysis), numpy-mcp (numerical compute), mcp-debugger (API testing)

**Auto-Trigger Strategy**: Chain 3-5 MCPs for complete workflows. Use sequential-thinking for planning, filesystem+Grep for search, pytest-mcp for debugging.

**Common Workflows**:
- Data Analysis: filesystem -> sqlite-mcp -> pandas-mcp
- Testing: pytest-mcp -> puppeteer -> mcp-analyzer
- Research: Grep -> filesystem -> git-mcp -> pandas-mcp

**Configuration:** `.mcp.json` (12 servers) | **See**: `.project/ai/config/mcp_usage_guide.md` for complete auto-trigger keywords and orchestration patterns

------

## 21) Phase 3 Ui/ux Status & Maintenance Mode

**See:** `.project/ai/config/phase3_status.md` for complete status.

**Quick Reference:**
- Phase 3: [OK] COMPLETE (34/34 issues, October 9-17, 2025)
- Status: Merged to main | UI work in MAINTENANCE MODE
- Achievement: WCAG 2.1 Level AA, 18 design tokens, 4 breakpoints validated
- Browser: Chromium validated [OK] | Firefox/Safari deferred [PAUSE]

**UI Maintenance Mode Policy:**
- **DO**: Fix critical bugs, update docs for new features, maintain WCAG AA
- **DON'T**: Proactive enhancements, Firefox/Safari validation, "nice-to-have" polish
- **Focus**: 80-90% time on research (controllers, PSO, SMC theory)

**See Also**: `.ai/planning/phase3/HANDOFF.md` for handoff document

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
- Total Documentation: 985 files (814 in docs/, 171 in .project/)
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

**See**: `.project/dev_tools/TASK_WRAPPER_USAGE.md` for complete guide, code examples, multi-agent patterns, and configuration options

**See Also**: `.project/ai/config/agent_checkpoint_system.md` (design), `.project/ai/config/agent_orchestration.md` (patterns)

------

### Appendix: Notes

- Keep this file authoritative for style, testing, and operational posture.
- Treat it as versioned team memory; update via PRs with a short change log.
- **CRITICAL**: All git operations must target: https://github.com/theSadeQ/dip-smc-pso.git
- **MANDATORY**: Automatic updates are REQUIRED for all repository changes
- Maintain clean, professional commit messages following the established pattern
