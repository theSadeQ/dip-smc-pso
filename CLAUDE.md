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

**Purpose:** Resume work when switching Claude Code accounts or starting new sessions

**Quick Start:**
```bash
# Windows: Double-click this file
.project\dev_tools\quick_recovery.bat

# Linux/Mac: Run recovery + checkpoint analysis
bash .project/dev_tools/recover_project.sh && python .project/dev_tools/analyze_checkpoints.py
```

**What it does:**
1. Shows recent commits and project status
2. Detects incomplete multi-agent work
3. Categorizes real vs test checkpoints
4. Provides resumption recommendations

**Then ask Claude:**
> "What should I resume based on the recovery output?"

**Detailed Guide:** See `.project/dev_tools/MULTI_ACCOUNT_RECOVERY_GUIDE.md` for complete workflow

**Tools:**
- **quick_recovery.bat** - One-click recovery for Windows
- **analyze_checkpoints.py** - Categorize incomplete work (real vs test)
- **cleanup_test_checkpoints.py** - Clean up test checkpoint artifacts
- **MULTI_ACCOUNT_RECOVERY_GUIDE.md** - Complete recovery workflow documentation

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

```bash
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

**Purpose**: Convert written educational content into podcast-style audio for commute/exercise learning

**Available Series**:
- **Phase 2**: `.ai/edu/notebooklm/phase2/` (12 episodes, ~5 hours audio, 30 hours learning content)
- **Phase 3**: `.ai/edu/notebooklm/phase3/` (8 episodes, ~2.5 hours audio, 25 hours learning content)

**Status**: [OK] Phase 2 complete (November 2025) | Phase 3 complete (November 2025)

#### What Is NotebookLM?

Google's AI-powered tool that generates podcast-style audio discussions from documents:
- Upload markdown files to [notebooklm.google.com](https://notebooklm.google.com)
- Click "Generate Audio Overview" button
- AI creates 20-30 minute conversational podcast with two hosts
- Technical terms pronounced correctly via TTS optimization

#### Quick Start (for Claude)

When user requests podcast generation for educational content:

**1. Identify Source Content**: Which phase/topic needs podcast optimization?
**2. Create Episode Structure**: Break content into 2-2.5 hour chunks (20-30 min audio each)
**3. Apply TTS Optimization**: Use enhanced narrative style + verbalized equations
**4. Generate Episodes**: Create separate markdown files per episode
**5. Create README**: Usage instructions for NotebookLM upload

#### TTS Optimization Requirements (MANDATORY)

**Mathematical Expressions - Verbalized Format**:
```
NOT: u = -K·sign(s)
BUT: u equals negative K times sign of s

NOT: s = k₁·θ₁ + k₂·θ̇₁
BUT: s equals k-one times theta-one plus k-two times theta-one-dot
```

**Greek Letters - Spelled Out**:
```
θ -> "theta"
ε -> "epsilon"
λ -> "lambda"
Δ -> "delta"
ω -> "omega"
```

**Mathematical Notation - Verbal Equivalents**:
```
θ̇ -> "theta-dot" (time derivative)
θ̂ -> "theta-hat" (estimate)
∫ -> "integral of"
∂ -> "partial derivative of"
≈ -> "approximately equals"
≤ -> "less than or equal to"
```

**Code Examples - Narrated Format**:
```markdown
Let's see this concept in action with a Python simulation.
First, we import NumPy for numerical operations...

[CODE BLOCK]
import numpy as np
...
[/CODE BLOCK]

Walking through the main loop: For each time step,
we calculate the error as setpoint minus current position...
```

**Diagrams - Verbal Descriptions**:
```markdown
Picture a flowchart with four boxes connected by arrows.
Starting at the top, we have the setpoint. An arrow flows down...
```

#### Enhanced Narrative Style Guidelines

**Conversational Framing**:
- Start with relatable scenario or question
- Use "imagine", "picture this", "let's think about"
- Progressive revelation (build complexity gradually)

**Analogy-First Approach**:
- Begin major concepts with physical analogies
- Transition to technical explanation
- Connect back to analogy for reinforcement

**Retention Techniques**:
- Recap every 5-7 minutes of content
- Callbacks to previous episodes
- "Pause and reflect" sections
- Preview of next episode

**Question-Driven Narrative**:
- Pose questions learners would ask
- Answer with examples first, then formalism
- "Now you might be wondering..." transitions

#### Episode Structure Template

```markdown
# Episode N: [Catchy Title]

**Duration**: 20-30 minutes | **Learning Time**: 2-2.5 hours | **Difficulty**: [Level]

## Opening Hook
[Relatable scenario that introduces the concept]

## What You'll Discover
[Bullet list of key takeaways]

## [Section 1]: [Main Content]
[Enhanced narrative with analogies, examples, TTS-optimized equations]

## [Section 2]: [Code/Visualization]
[Narrated walkthrough with verbal descriptions]

## Key Takeaways
[Numbered recap of essential insights]

## Pronunciation Guide
[Technical terms with phonetic spellings]

## What's Next
[Preview of next episode]

## Pause and Reflect
[Questions to consider before continuing]

---

**Episode N of M** | [Phase/Topic]

**Previous**: [Link] | **Next**: [Link]
```

#### Phase 2 Example (Reference Implementation)

**Location**: `.ai/edu/notebooklm/phase2/`

**Structure**:
- 12 episodes covering Control Theory, SMC, Optimization, DIP System
- Episodes 1-2: Control theory fundamentals
- Episodes 3-4: PID control and limitations
- Episodes 5-7: Sliding Mode Control trilogy
- Episodes 8-9: Optimization and PSO
- Episodes 10-12: DIP system understanding

**Key Files**:
- `phase2_episode01.md` through `phase2_episode12.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM

**Total Output**: ~150 KB markdown, generates ~5 hours podcast audio

#### Phase 3 Example (Reference Implementation)

**Location**: `.ai/edu/notebooklm/phase3/`

**Structure**:
- 8 episodes covering Hands-On Learning, Simulations, Controller Comparison
- Episodes 1-2: Environment setup, first simulation, plot interpretation
- Episodes 3-4: Controller comparison, performance metrics
- Episodes 5-6: Config modification, PSO optimization
- Episodes 7-8: Troubleshooting, phase wrap-up

**Key Features**:
- Rich verbal descriptions of 6 simulation plots (multi-pass: sketch → story → meaning)
- Commands spelled out phonetically ("dash dash ctrl classical underscore s-m-c")
- YAML hierarchy verbalized for configuration edits
- "Tour guide + sports commentary" style for live plot narration

**Key Files**:
- `phase3_episode01.md` through `phase3_episode08.md`: Individual episodes
- `README.md`: Complete usage guide for NotebookLM

**Total Output**: ~85 KB markdown, generates ~2.5 hours podcast audio

**Key Difference from Phase 2**: Focuses on hands-on workflows and plot interpretation rather than theory

#### Validation Checklist (Per Episode)

Before finalizing any NotebookLM episode:

- [ ] **Length**: 2,500-3,500 words (~130-150 lines)
- [ ] **TTS Optimization**: All equations verbalized phonetically
- [ ] **Greek Letters**: Spelled out on first use
- [ ] **Code Examples**: Narrated with context
- [ ] **Diagrams**: Verbally described in detail
- [ ] **Analogies**: At least 2 physical examples per episode
- [ ] **Retention**: Recap section every 700-1,000 words
- [ ] **Callbacks**: Reference to previous episodes (Episodes 2+)
- [ ] **Preview**: Teaser for next episode at end
- [ ] **Technical Accuracy**: All formulas verified
- [ ] **Pronunciation Guide**: Included for technical terms
- [ ] **Self-Contained**: Understandable independently

#### User Workflow

**For Listeners**:
1. Visit [notebooklm.google.com](https://notebooklm.google.com), create notebook
2. Upload episode markdown files (one or multiple)
3. Click "Generate Audio Overview"
4. Listen during commute/exercise (20-30 min per episode)
5. Read detailed roadmap for exercises and deeper understanding

**For Content Creators (Claude)**:
1. Identify educational content needing audio format
2. Generate TTS-optimized episodes using guidelines above
3. Create README with NotebookLM usage instructions
4. Test by uploading to NotebookLM and verifying audio quality
5. Update CLAUDE.md section 6.4 with new content location

#### Success Metrics

Podcast content is successful when:
- Users can follow along by audio alone (no visual needed)
- Technical terms pronounced correctly by TTS
- Concepts build progressively without confusion
- Listeners can explain key ideas after one listen
- Retention matches or exceeds reading comprehension

**See Also**:
- Phase 2 usage guide: `.ai/edu/notebooklm/phase2/README.md`
- Phase 3 usage guide: `.ai/edu/notebooklm/phase3/README.md`

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

**Safe for Research/Academic Use:**
- [OK] Single-threaded & multi-threaded operation validated
- [OK] Controllers functional and tested
- [OK] Documentation complete and accurate

**NOT Ready for Production:**
- [ERROR] Quality gates: 1/8 passing
- [ERROR] Coverage measurement broken (pytest Unicode issue)
- [ERROR] Production score: 23.9/100 (BLOCKED)

### Validation Commands
```bash
# Thread Safety (works - 11/11 Passing)
python -m pytest tests/test_integration/test_thread_safety/test_production_thread_safety.py -v

# Production Readiness (works - Reports 23.9/100)
python -c "from src.integration.production_readiness import ProductionReadinessScorer; \
           scorer = ProductionReadinessScorer(); \
           result = scorer.assess_production_readiness(); \
           print(f'Score: {result.overall_score:.1f}/100')"
```

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

**See Also**: `.project/ai/planning/research/RESEARCH_COMPLETION_SUMMARY.md` | `.project/ai/planning/CURRENT_STATUS.md`

------

## 14) Workspace Organization & Hygiene

**See:** `.project/ai/config/workspace_organization.md` for complete details.

**Quick Reference:**
- Target: ≤19 visible root items, ≤7 hidden dirs
- Use `.project/` for ALL AI/dev configs (CANONICAL)
- Use `.artifacts/` NOT `artifacts/`
- Use `.cache/` for ephemeral data

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
- **Runtime artifacts**: `.artifacts/` (outputs, research papers, scripts)
- **Runtime caches**: `.cache/` (pytest, hypothesis, htmlcov, benchmarks)
- **Visible directories** (8): `src/`, `tests/`, `docs/`, `scripts/`, `notebooks/`, `data/`, `benchmarks/`, `optimization_results/`
- **Root files** (9 core + 2 MCP): `README.md`, `CHANGELOG.md`, `CLAUDE.md`, `config.yaml`, `requirements.txt`, `simulate.py`, `streamlit_app.py`, `package.json`, `package-lock.json`

### Protected Files (never Delete)
- `.project/dev_tools/Switch-ClaudeAccount.ps1` - Multi-account switcher (CANONICAL)

### Weekly Health Check
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

### Quick Reference: Available MCP Servers (12 Total - All Operational)

| Server | Auto-Trigger Keywords | Primary Use Cases |
|--------|----------------------|-------------------|
| **filesystem** | inspect, read, analyze files | Code/log analysis |
| **github** | issue, PR, commit | Issue tracking |
| **sequential-thinking** | **plan**, debug, investigate, verify, figure out | **Planning**, debugging, systematic analysis |
| **puppeteer** | test, screenshot, UI, dashboard | Streamlit testing |
| **mcp-debugger** | debug, postman, API | API endpoint testing |
| **pytest-mcp** | test failure, pytest, debug | Test debugging |
| **git-mcp** | git history, branch, stats | Advanced Git ops |
| **sqlite-mcp** | query, database, results | PSO results DB |
| **mcp-analyzer** | lint, ruff, vulture, quality | Code quality checks |
| **lighthouse-mcp** | audit, accessibility, performance | Lighthouse audits |
| **pandas-mcp** | data analysis, statistics, plotting | PSO data analysis |
| **numpy-mcp** | matrix ops, numerical compute | Control theory math |

**NOTES:**
- **pandas-mcp** and **numpy-mcp** are local custom servers (configured in `.project/mcp/servers/`)
- For semantic documentation search, use **filesystem** + **git-mcp** + **Grep** combination

### Multi-mcp Collaboration (mandatory)

**Chain 3-5 MCPs for complete workflows:**
- **Data Analysis**: filesystem -> sqlite-mcp -> pandas-mcp -> mcp-analyzer
- **Documentation**: filesystem -> git-mcp -> Grep (built-in search)
- **Testing**: pytest-mcp -> puppeteer -> mcp-analyzer
- **Research**: Grep -> filesystem -> git-mcp -> pandas-mcp
- **Debugging**: sequential-thinking -> pytest-mcp -> filesystem

**Example Multi-MCP Workflow:**
```bash
# User: "find the Adaptive SMC Controller and Analyze Its Test Results"
# Claude Triggers: Grep -> Filesystem -> Pytest-mcp -> Mcp-analyzer
```

## Overview

### Orchestration Rules (for Claude)

1. If user mentions 2+ domains (docs + data + testing), use 2+ MCPs
2. For "complete analysis" tasks, use full pipeline (3-5 MCPs minimum)
3. For debugging, combine sequential-thinking + domain-specific MCPs
4. **For PLANNING, ALWAYS use sequential-thinking first** (most commonly missed!)
5. For research workflows: Grep -> filesystem -> relevant analysis MCPs
6. **Understand intent, not keywords**: "where is" = search, "check" = analyze, "test" = validate, **"plan" = systematic thinking**
7. **Chain automatically**: Complete full workflow without asking user for next step

### Natural Language Examples

**Users can ask naturally (all work the same):**
- "Where's the adaptive SMC?" -> Grep + filesystem
- "Check code quality" -> mcp-analyzer + filesystem
- "Test the dashboard" -> puppeteer + lighthouse-mcp
- "What's wrong with this controller?" -> filesystem + pytest-mcp + sequential-thinking

**Configuration:** `.mcp.json` (12 servers) | `.project/ai/config/mcp_usage_guide.md` (auto-trigger guide)

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

**Navigation Systems:**
1. **NAVIGATION.md** - Master unified hub (NEW: Nov 2025)
2. **docs/index.md** - Sphinx homepage with 11 toctrees
3. **guides/INDEX.md** - User guides hub (43 files, 12,525 lines)
4. **README.md** - GitHub entry point with architecture diagrams
5. **CLAUDE.md** - Team memory & project conventions (this file)
6. **sitemap_cards.md** - Card-based tree view with icons
7. **sitemap_interactive.md** - D3.js force-directed graph (985 files)
8. **sitemap_visual.md** - Mermaid mindmap & flowcharts
9. **architecture_control_room.md** - 3D isometric system visualization
10. **3d-pendulum-demo** - Interactive WebGL pendulum simulation
11. **live-python-demo** - Browser-based Python code execution

**User Journeys:**
- **Complete Beginners**: NAVIGATION.md -> Path 0 (beginner-roadmap.md) -> Tutorial 01
- **Quick Start**: NAVIGATION.md -> Getting Started -> Tutorial 01 (1-2 hrs)
- **Researchers**: NAVIGATION.md -> Research Workflows -> Citations & Theory
- **Developers**: NAVIGATION.md -> API Reference -> Architecture -> Testing
- **Integrators**: NAVIGATION.md -> HIL Quickstart -> Docker Deployment

**Cross-References:**
- All 43 category indexes link to NAVIGATION.md (standardized footer)
- All 4 main entry points link bidirectionally to NAVIGATION.md
- All 4 visual navigation systems include NAVIGATION.md node/card

**Maintenance:**
- Update NAVIGATION.md when adding new category indexes
- Run validation script: `python .project/dev_tools/validate_navigation.py`
- Rebuild Sphinx after changes: `sphinx-build -M html docs docs/_build -W`

------

## 24) Task Wrapper & Checkpoint System for Multi-Agent Orchestration

**See:** `.project/dev_tools/TASK_WRAPPER_USAGE.md` for complete guide.

**Quick Reference:**
- Automatic checkpointing for Task tool invocations
- Survives token limits, crashes, session interruptions
- Hybrid auto-polling: tracks progress every 5 minutes
- Zero-friction recovery: `/recover` + `/resume` commands
- Output preservation: agent work saved to `.artifacts/`

### One-Line Integration Pattern

```python
from .project.dev_tools.task_wrapper import checkpoint_task_launch

# Automatic checkpointing - work survives token limits!
result = checkpoint_task_launch(
    task_id="LT-4",
    agent_id="agent1_theory",
    task_config={
        "subagent_type": "general-purpose",
        "description": "Derive Lyapunov proofs",
        "prompt": "Your detailed prompt..."
    },
    role="Theory Specialist - Derive Lyapunov proofs"
)

# Result includes:
# - result["task_result"] - Agent output
# - result["checkpoint_file"] - Location of complete checkpoint
# - result["hours_spent"] - Total time elapsed
# - result["output_artifact"] - Location of saved output JSON
```

### Recovery After Token Limit

```bash
# 1. Detect incomplete work
/recover

# 2. Auto-resume interrupted agents
/resume LT-4 agent1_theory

# 3. Verify completion
/recover
```

### Key Features

**Auto-Checkpointing:**
- Plan approval checkpoint (pre-launch)
- Agent launch checkpoint (at start)
- Progress checkpoints (every 5 min, hybrid auto-polling)
- Completion checkpoint (at finish)
- Output capture (auto-save to .artifacts/)

**Checkpoint Files Location:**
```
.artifacts/
├── lt4_plan_approved.json
├── lt4_agent1_theory_launched.json
├── lt4_agent1_theory_progress.json
├── lt4_agent1_theory_complete.json
└── lt4_agent1_theory_output.json
```

**Recovery Functions:**
- `resume_incomplete_agents(task_id)` - List incomplete agents for recovery
- `cleanup_task_checkpoints(task_id)` - Clean up after git commit
- `get_task_status(task_id)` - Check task progress
- `get_incomplete_agents()` - Find all interrupted work

### Multi-Agent Patterns

**Sequential (Agent 2 depends on Agent 1):**
```python
result1 = checkpoint_task_launch(task_id="LT-7", agent_id="agent1_research", ...)
result2 = checkpoint_task_launch(
    task_id="LT-7",
    agent_id="agent2_paper",
    dependencies=[result1["output_artifact"]]
)
```

**Parallel (Independent agents):**
```python
result1 = checkpoint_task_launch(task_id="MT-6", agent_id="agent1_sim", ...)
result2 = checkpoint_task_launch(task_id="MT-6", agent_id="agent2_analysis", ...)
```

### Configuration

**Custom polling interval:**
```python
checkpoint_task_launch(
    ...,
    poll_interval_seconds=600  # Every 10 min instead of 5
)
```

**Disable auto-polling (manual updates only):**
```python
checkpoint_task_launch(
    ...,
    auto_progress=False
)
```

### Implementation Details

**Location:** `.project/dev_tools/task_wrapper.py` (250+ lines)

**Files Modified:**
- `.project/dev_tools/agent_checkpoint.py` - Added `resume_incomplete_agents()`, `cleanup_task_checkpoints()`
- `.project/dev_tools/recover_project.sh` - Enhanced section [5] with recovery suggestions

**Test Suite:** `.project/dev_tools/test_task_wrapper.py`

**Documentation:** `.project/dev_tools/TASK_WRAPPER_USAGE.md` (complete usage guide with examples)

### Status

[OK] **Operational** (November 2025)
- Task wrapper implementation complete
- Checkpoint system integrated and tested
- Recovery system fully functional
- Documentation comprehensive with examples
- Ready for multi-agent orchestration workflows

### Usage Checklist

Before launching multi-agent tasks:
- [OK] Use `checkpoint_task_launch()` instead of bare Task tool calls
- [OK] Provide task_id and agent_id (consistent naming)
- [OK] Include descriptive role for recovery context
- [OK] Set dependencies if agents depend on each other
- [OK] After completion, run cleanup: `cleanup_task_checkpoints(task_id)`

### Success Criteria

✅ Multi-agent work survives token limits
✅ Recovery is automatic (one-command: `/resume`)
✅ Progress tracking shows where agents left off
✅ Output preserved in .artifacts/
✅ No manual recovery work needed

**See Also:** `.project/ai/config/agent_checkpoint_system.md` (original design), `.project/ai/config/agent_orchestration.md` (orchestration patterns)

------

### Appendix: Notes

- Keep this file authoritative for style, testing, and operational posture.
- Treat it as versioned team memory; update via PRs with a short change log.
- **CRITICAL**: All git operations must target: https://github.com/theSadeQ/dip-smc-pso.git
- **MANDATORY**: Automatic updates are REQUIRED for all repository changes
- Maintain clean, professional commit messages following the established pattern
