# CLAUDE.md — Team Memory & Project Conventions

> This file contains project-specific instructions for Claude Code operations and automatic repository management.

**CRITICAL RULE - NO EMOJIS:**
- **NEVER use Unicode emojis** (🚀, ✅, ❌, etc.) in any code, scripts, output, or documentation
- **ALWAYS use ASCII text markers** instead: [AI], [OK], [ERROR], [WARNING], [INFO], [BLUE], etc.
- **Reason:** Windows terminal (cp1252 encoding) cannot display Unicode properly, causing crashes
- **Applies to:** Python scripts, shell output, markdown docs, commit messages, all user-facing text
- **Example:** Use "[OK]" not "✅", "[ERROR]" not "❌", "[INFO]" not "ℹ️"

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

## 3) Session Continuity & Project-Wide Recovery System

**See:** `.project/ai/config/session_continuity.md` for complete details.

**Purpose:** 30-second recovery from token limits or multi-month gaps

**Status:** ✅ Operational (Oct 2025)

### Quick Recovery:
```bash
# ONE-COMMAND recovery after token limit
/recover

# Or manually:
bash .dev_tools/recover_project.sh

# Check roadmap progress
python .dev_tools/roadmap_tracker.py
```

### Key Tools:
1. **Project State Manager** (`.dev_tools/project_state_manager.py`) - Tracks phase, roadmap progress, completed tasks
2. **Git Recovery Script** (`.dev_tools/recover_project.sh`) - 30-second recovery workflow
3. **Roadmap Tracker** (`.dev_tools/roadmap_tracker.py`) - Parses 72-hour research roadmap (50 tasks)
4. **Agent Checkpoint System** (`.dev_tools/agent_checkpoint.py`) - Recovers interrupted multi-agent work

### What Survives Token Limits:
- ✅ Git commits (10/10), project state (9/10), agent checkpoints (9/10), data files (8/10)
- ❌ Background bash processes, in-memory agent state (BUT checkpoints preserve progress)

### Automated Tracking (Zero Manual Updates):
```bash
# Just commit with task ID - state auto-updates via Git hooks!
git commit -m "feat(MT-6): Complete boundary layer optimization"
# Pre-commit hook auto-detects MT-6 + updates project state
```

**Recovery Reliability:** Git commits (10/10) | Automated tracking (10/10) | Test coverage (11/11 tests, 100%)

**Current Phase:** Research (ROADMAP_EXISTING_PROJECT.md) | **Completed:** Phase 3 (UI 34/34), Phase 4 (Production 4.1+4.2)

------

## 4) Project Overview

**Double‑Inverted Pendulum Sliding Mode Control with PSO Optimization**

A Python framework for simulating, controlling, and analyzing a double‑inverted pendulum (DIP) system. It provides multiple SMC variants, optimization (PSO), a CLI and a Streamlit UI, plus rigorous testing and documentation.

------

## 5) Architecture

### 5.1 High‑Level Modules

- **Controllers**: classical SMC, super‑twisting, adaptive, hybrid adaptive STA‑SMC, swing‑up; experimental MPC.
- **Dynamics/Plant**: simplified and full nonlinear dynamics (plus low‑rank); shared base interfaces.
- **Core Engine**: simulation runner, unified simulation context, batch/Numba vectorized simulators.
- **Optimization**: PSO tuner (operational); additional algorithms staged via an optimization core.
- **Utils**: validation, control primitives (e.g., saturation), monitoring, visualization, analysis, types, reproducibility, dev tools.
- **HIL**: plant server + controller client for hardware‑in‑the‑loop experiments.

### 5.2 Representative Layout (merged)

```
src/
├─ controllers/
│  ├─ classic_smc.py
│  ├─ sta_smc.py
│  ├─ adaptive_smc.py
│  ├─ hybrid_adaptive_sta_smc.py
│  ├─ swing_up_smc.py
│  ├─ mpc_controller.py
│  └─ factory.py
├─ core/
│  ├─ dynamics.py
│  ├─ dynamics_full.py
│  ├─ simulation_runner.py
│  ├─ simulation_context.py
│  └─ vector_sim.py
├─ plant/
│  ├─ models/
│  │  ├─ simplified/
│  │  ├─ full/
│  │  └─ lowrank/
│  ├─ configurations/
│  └─ core/
├─ optimizer/
│  └─ pso_optimizer.py
├─ utils/
│  ├─ validation/
│  ├─ control/
│  ├─ monitoring/
│  ├─ visualization/
│  ├─ analysis/
│  ├─ types/
│  ├─ reproducibility/
│  └─ development/
└─ hil/
   ├─ plant_server.py
   └─ controller_client.py
```

**Top‑level**

```
simulate.py        # CLI entry
streamlit_app.py   # Web UI
config.yaml        # Main configuration
requirements.txt   # Pinned deps / ranges
run_tests.py       # Test runner helper
README.md, CHANGELOG.md
```

------

## 6) Educational Materials (.ai/edu)

**Purpose**: Learning roadmaps for users at all skill levels, separate from project-specific documentation.

**Directory**: `.ai/edu/` (Educational content, managed by Claude Code)

### 6.1 Available Resources

**Beginner Roadmap** (`.ai/edu/beginner-roadmap.md`):
- **Target**: Complete beginners with ZERO coding/control theory background
- **Duration**: 125-150 hours over 4-6 months
- **Coverage**: Phase 1 (Computing, Python, Physics, Math) → Phase 2 (Control theory, SMC) → Phases 3-5 (Hands-on to mastery)
- **Status**: Phases 1-2 complete (~2,000 lines), Phases 3-5 planned (~1,500-2,000 more lines)

### 6.2 Integration with Main Documentation

**Learning Path Progression**:
```
Path 0: Complete Beginner (NEW)
  .ai/edu/beginner-roadmap.md (125-150 hours) →

Path 1: Quick Start (EXISTING)
  docs/guides/getting-started.md → Tutorial 01 (1-2 hours) →

Paths 2-4: Advanced (EXISTING)
  Tutorials 02-05, Theory, Research workflows
```

**Audience Segmentation**:
- `.ai/edu/` → Prerequisites for absolute beginners (Path 0)
- `docs/guides/` → Project-specific documentation (Paths 1-4)

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

## 13) Production Safety & Readiness (Phase 4 Status)

**See:** `.project/ai/config/phase4_status.md` for complete status.

**Quick Reference:**
- Production Readiness: 23.9/100 (Phase 4.1+4.2 complete)
- Thread Safety: 100% (11/11 tests passing)
- Status: RESEARCH-READY ✅ | NOT production-ready ❌

### Current Status: RESEARCH-READY ✅

**Safe for Research/Academic Use:**
- ✅ Single-threaded & multi-threaded operation validated
- ✅ Controllers functional and tested
- ✅ Documentation complete and accurate

**NOT Ready for Production:**
- ❌ Quality gates: 1/8 passing
- ❌ Coverage measurement broken (pytest Unicode issue)
- ❌ Production score: 23.9/100 (BLOCKED)

### Validation Commands:
```bash
# Thread Safety (WORKS - 11/11 passing)
python -m pytest tests/test_integration/test_thread_safety/test_production_thread_safety.py -v

# Production Readiness (WORKS - reports 23.9/100)
python -c "from src.integration.production_readiness import ProductionReadinessScorer; \
           scorer = ProductionReadinessScorer(); \
           result = scorer.assess_production_readiness(); \
           print(f'Score: {result.overall_score:.1f}/100')"
```

### Phase 5: Research Phase (October 29, 2025)

**Status**: ✅ LAUNCHED (QW-5 complete)
**Focus**: Validate, document, and benchmark 7 controllers
**Roadmap**: 72 hours over 12-16 weeks
- Week 1 (8h): benchmarks, chattering metrics, visualization
- Weeks 2-4 (18h): comprehensive benchmark, boundary layer optimization
- Months 2-3 (46h): Lyapunov proofs, model uncertainty, research paper

**Key Tasks**: QW-2 (benchmarks), QW-4 (chattering), MT-5 (7-controller comparison), LT-4 (Lyapunov proofs), LT-7 (research paper)

**See Also**: `.artifacts/RESEARCH_STATUS_2025_10_29.md` | `.ai/planning/phase4/FINAL_ASSESSMENT.md`

------

## 14) Workspace Organization & Hygiene

**See:** `.project/ai/config/workspace_organization.md` for complete details.

**Quick Reference:**
- Target: ≤19 visible root items, ≤7 hidden dirs
- Use `.project/` for ALL AI/dev configs (CANONICAL)
- Use `.artifacts/` NOT `artifacts/`
- Use `.cache/` for ephemeral data

### Config Consolidation (Use `.project/` as CANONICAL):
```
.project/                          # CANONICAL CONFIG ROOT
├─ ai/config/                     # AI configurations
├─ claude/                        # Claude Code settings
├─ dev_tools/                     # Development scripts (CANONICAL)
└─ archive/                       # Archived artifacts
```

### DO NOT USE (deprecated aliases):
- ❌ `.ai/` → use `.project/ai/`
- ❌ `.dev_tools/` at root → use `.project/dev_tools/`

### Directory Rules:
- **Runtime artifacts**: `.artifacts/` (outputs, research papers, scripts)
- **Runtime caches**: `.cache/` (pytest, hypothesis, htmlcov, benchmarks)
- **Visible directories** (8): `src/`, `tests/`, `docs/`, `scripts/`, `notebooks/`, `data/`, `benchmarks/`, `optimization_results/`
- **Root files** (9 core + 2 MCP): `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `config.yaml`, `requirements.txt`, `simulate.py`, `streamlit_app.py`, `package.json`, `package-lock.json`

### Protected Files (NEVER DELETE):
- `.project/dev_tools/Switch-ClaudeAccount.ps1` - Multi-account switcher (CANONICAL)

### Weekly Health Check:
```bash
ls | wc -l                                          # ≤19 visible items
find . -maxdepth 1 -type d -name ".*" | wc -l      # ≤7 hidden dirs
du -sh .cache/                                      # <50MB
du -sh .artifacts/                                  # <100MB
```

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
# example-metadata:
# runnable: false

from src.controllers.factory import create_controller
controller = create_controller(
  'classical_smc',
  config=controller_config,
  gains=[10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
)
control_output = controller.compute_control(state, last_control, history)
# Optimization (PSO)
from src.optimizer.pso_optimizer import PSOTuner
# ... initialize bounds, tuner, and run pso.optimize(...)
# Monitoring
from src.utils.monitoring.latency import LatencyMonitor
monitor = LatencyMonitor(dt=0.01)
start = monitor.start()
# ... loop ...
missed = monitor.end(start)
```

------

## 17) Multi-Agent Orchestration System

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
# When user approves plan
checkpoint_plan_approved(task_id, plan_summary, hours, agents, deliverables)

# When launching each agent
checkpoint_agent_launched(task_id, agent_id, role, hours)

# Every 5-10 minutes during agent execution
checkpoint_agent_progress(task_id, agent_id, hours_completed, deliverables, current_phase)

# When agent completes or fails
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

### Rebuild Workflow:
```bash
# 1. Make changes to docs
# 2. ALWAYS rebuild:
sphinx-build -M html docs docs/_build -W --keep-going

# 3. Verify changes copied:
stat docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 4. Verify localhost serves new version:
curl -s "http://localhost:9000/_static/your-file.css" | grep "YOUR_CHANGE"

# 5. Tell user to hard refresh browser (Ctrl+Shift+R)
```

### Auto-Rebuild Triggers:
- Sphinx source files: `docs/*.md`, `docs/**/*.rst`
- Static assets: `docs/_static/*.css`, `docs/_static/*.js`, `docs/_static/*.png`
- Configuration: `docs/conf.py`, `docs/_templates/*`
- Navigation: `docs/index.rst`, any `toctree` directives

### Common Pitfalls:
❌ Don't assume changes are live - verify with `curl` or `stat`
❌ Don't skip rebuild - Sphinx doesn't auto-rebuild static files
❌ Don't forget browser cache - tell user to hard refresh

✅ Do verify timestamps - `stat` both source and build files
✅ Do check MD5 sums - ensure files actually copied
✅ Do test with curl - verify localhost serves new content

------

## 20) Model Context Protocol (MCP) Auto-Triggers

**See:** `.project/ai/config/mcp_usage_guide.md` for complete guide | `docs/mcp-debugging/README.md` for workflows

**For Claude:** Auto-trigger MCPs based on task keywords (NO user confirmation needed).

**For Users:** Just ask naturally! No special keywords required.

### Quick Reference: Available MCP Servers (11 Total)

| Server | Auto-Trigger Keywords | Primary Use Cases |
|--------|----------------------|-------------------|
| **pandas-mcp** | analyze, plot, statistics, convergence | Data analysis, PSO results |
| **context7** | find, search, where, related | Doc search, cross-refs |
| **puppeteer** | test, screenshot, UI, dashboard | Streamlit testing |
| **numpy-mcp** | matrix, eigenvalue, numerical | Linear algebra ops |
| **filesystem** | inspect, read, analyze files | Code/log analysis |
| **github** | issue, PR, commit | Issue tracking |
| **sequential-thinking** | **plan**, debug, investigate, verify, figure out | **Planning**, debugging, systematic analysis |
| **git-mcp** | git history, branch, stats | Advanced Git ops |
| **sqlite-mcp** | query, database, results | PSO results DB |
| **pytest-mcp** | test failure, pytest, debug | Test debugging |
| **mcp-analyzer** | lint, ruff, vulture, quality | Code quality checks |

### Multi-MCP Collaboration (MANDATORY)

**Chain 3-5 MCPs for complete workflows:**
- **Data Analysis**: filesystem → pandas-mcp → numpy-mcp → sqlite-mcp
- **Documentation**: context7 → filesystem → git-mcp
- **Testing**: pytest-mcp → puppeteer → pandas-mcp
- **Research**: context7 → pandas-mcp → numpy-mcp
- **Debugging**: sequential-thinking → pytest-mcp → filesystem

**Example Multi-MCP Workflow:**
```bash
# User: "Find the adaptive SMC controller and analyze its test results"
# Claude triggers: context7 → filesystem → pytest-mcp → pandas-mcp → numpy-mcp
```

### Orchestration Rules (FOR CLAUDE)

1. If user mentions 2+ domains (docs + data + testing), use 2+ MCPs
2. For "complete analysis" tasks, use full pipeline (3-5 MCPs minimum)
3. For debugging, combine sequential-thinking + domain-specific MCPs
4. **For PLANNING, ALWAYS use sequential-thinking first** (most commonly missed!)
5. For research workflows: context7 → filesystem → relevant analysis MCPs
6. **Understand intent, not keywords**: "where is" = search, "check" = analyze, "test" = validate, **"plan" = systematic thinking**
7. **Chain automatically**: Complete full workflow without asking user for next step

### Natural Language Examples

**Users can ask naturally (all work the same):**
- "Where's the adaptive SMC?" → context7 + filesystem
- "Is this CSV good?" → pandas-mcp + numpy-mcp
- "Test the dashboard" → puppeteer
- "What's wrong with this controller?" → filesystem + pytest-mcp + sequential-thinking

**Configuration:** `.mcp.json` (11 servers) | `.ai/config/settings.local.json` (`enableAllProjectMcpServers: true`)

------

## 21) Phase 3 UI/UX Status & Maintenance Mode

**See:** `.project/ai/config/phase3_status.md` for complete status.

**Quick Reference:**
- Phase 3: ✅ COMPLETE (34/34 issues, October 9-17, 2025)
- Status: Merged to main | UI work in MAINTENANCE MODE
- Achievement: WCAG 2.1 Level AA, 18 design tokens, 4 breakpoints validated
- Browser: Chromium validated ✅ | Firefox/Safari deferred ⏸️

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
- MCP servers auto-trigger for appropriate tasks; all 11 servers operational.

------

### Appendix: Notes

- Keep this file authoritative for style, testing, and operational posture.
- Treat it as versioned team memory; update via PRs with a short change log.
- **CRITICAL**: All git operations must target: https://github.com/theSadeQ/dip-smc-pso.git
- **MANDATORY**: Automatic updates are REQUIRED for all repository changes
- Maintain clean, professional commit messages following the established pattern
