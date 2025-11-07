# GEMINI.md — Team Memory & Project Conventions

> This file contains project-specific instructions for Gemini Code operations and automatic repository management.

**Note:** This file uses ASCII text markers (e.g., [AI], [OK], [BLUE]) instead of Unicode emojis for Windows terminal compatibility. All documentation and scripts should follow this pattern to ensure proper display on Windows systems with cp1252 encoding.

------

## 1) Repository Information

**Primary Repository**: https://github.com/theSadeQ/dip-smc-pso.git
**Branch Strategy**: Main branch deployment
**Working Directory**: D:\Projects\main

------

## 2) Automatic Repository Management

**See:** `.gemini/repository_management.md` for complete details.

**Quick Reference:**
- MANDATORY: Auto-commit and push after ANY repository changes
- Commit message format: `<Action>: <Brief description>` with [AI] footer
- Always verify remote URL: `https://github.com/theSadeQ/dip-smc-pso.git`

------

## 3) Session Continuity System

**See:** `.gemini/session_continuity.md` for complete details.

**Quick Reference:**
- Zero-effort account switching via `.project/dev_tools/session_state.json`
- Auto-detect and resume from previous session if <24h old
- Maintain session state throughout every session
- Update todos, decisions, and next actions continuously

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

## 6) Key Technologies

- Python 3.9+
- NumPy, SciPy, Matplotlib
- Numba for vectorized/batch simulation
- PySwarms / Optuna for optimization (PSO primary)
- Pydantic‑validated YAML configs
- pytest + pytest‑benchmark; Hypothesis where useful
- Streamlit for UI

------

## 7) Usage & Essential Commands

### 7.1 Simulations

```bash
python simulate.py --ctrl classical_smc --plot
python simulate.py --ctrl sta_smc --plot
python simulate.py --load tuned_gains.json --plot
python simulate.py --print-config
```

### 7.2 PSO Optimization

```bash
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json
python simulate.py --ctrl adaptive_smc --run-pso --seed 42 --save gains_adaptive.json
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --save gains_hybrid.json
```

### 7.3 HIL

```bash
python simulate.py --run-hil --plot
python simulate.py --config custom_config.yaml --run-hil
```

### 7.4 Testing

```bash
python run_tests.py
python -m pytest tests/test_controllers/test_classical_smc.py -v
python -m pytest tests/test_benchmarks/ --benchmark-only
python -m pytest tests/ --cov=src --cov-report=html
```

### 7.5 Web Interface

```bash
streamlit run streamlit_app.py
```

------

## 8) Configuration System

- Central `config.yaml` with strict validation.
- Domains: physics params, controller settings, PSO parameters, simulation settings, HIL config.
- Prefer "configuration first": define parameters before implementation changes.

------

## 9) Development Guidelines

### 9.1 Code Style

- Type hints everywhere; clear, example‑rich docstrings.
- ASCII header format for Python files (≈90 chars width).
- Explicit error types; avoid broad excepts.
- Use informal, conversational comments that explain the "why" behind the code, similar to the style in `requirements.txt`.

### 9.2 Adding New Controllers

1. Implement in `src/controllers/`.
2. Add to `src/controllers/factory.py`.
3. Extend `config.yaml`.
4. Add tests under `tests/test_controllers/`.

### 9.3 Batch Simulation

```python
from src.core.vector_sim import run_batch_simulation
results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)
```

### 9.4 Configuration Loading

```python
from src.config import load_config
config = load_config("config.yaml", allow_unknown=False)
```

------

## 10) Testing & Coverage Standards

**See:** `.gemini/testing_standards.md` for complete details.

**Quick Reference:**
- Overall: ≥85% | Critical components: ≥95% | Safety‑critical: 100%
- Every `.py` file has a `test_*.py` peer
- Validate theoretical properties for critical algorithms

------

## 11) Visualization & Analysis Toolkit

- Real‑time animations (DIPAnimator), static performance plots, project movie generator.
- Statistical analysis: confidence intervals, bootstrap, Welch's t‑test, ANOVA, Monte Carlo.
- Real‑time monitoring (latency, deadline misses, weakly‑hard constraints) for control loops.

------

## 12) Production Safety & Readiness (Snapshot)

**Production Readiness Score: 6.1/10** (recently improved)

### Verified Improvements

- **Dependency safety**: numpy 2.0 issues resolved; version bounds added; verification tests green.
- **Memory safety**: bounded metric collections; cleanup mechanisms; memory monitoring.
- **SPOF removal**: DI/factory registry; multi‑source resilient config; graceful degradation.

### Outstanding Risks — DO NOT DEPLOY MULTI‑THREADED

- **Thread safety**: suspected deadlocks; concurrent ops unsafe; validation currently failing.
- Safe for **single‑threaded** operation with monitoring.

### Validation Commands

```bash
python scripts/verify_dependencies.py
python scripts/test_memory_leak_fixes.py
python scripts/test_spof_fixes.py
python scripts/test_thread_safety_fixes.py  # currently failing
```

------

## 13) Workspace Organization & Hygiene

**Target:** ≤15 visible root items (currently: 15) ✓

**Weekly Health Check:**
```bash
ls | wc -l                          # ≤15
du -sh .test_artifacts/             # <10MB
du -sh .dev_validation/             # <5MB
du -sh logs/                        # <20MB
find . -name "*.log.*" | wc -l      # 0
```

**Before Every Commit:**
```bash
python scripts/cleanup/workspace_cleanup.py --verbose
```

**Directory Rules (Single Source of Truth):**
- Use `.artifacts/` NOT `artifacts/`
- Use `notebooks/` NOT `.notebooks/`
- Use `optimization_results/` NOT `.optimization_results/`
- NEVER create files in root except: simulate.py, streamlit_app.py, config.yaml, requirements.txt, README.md, CHANGELOG.md, GEMINI.md

**Full Details:**
- Comprehensive guide: `.gemini/workspace_organization.md`
- Oct 2025 cleanup lessons (370MB recovered): `.gemini/WORKSPACE_CLEANUP_2025-10-09.md`

------

## 14) Controller Memory Management

**See:** `.gemini/controller_memory.md` for complete details.

**Quick Reference:**
- All controllers use weakref patterns to prevent circular references
- Explicit `cleanup()` methods available for all controller types
- Memory leak prevention: periodic reset + monitoring in production
- Validation: `pytest tests/test_integration/test_memory_management/ -v`

------

## 15) Controller Factory & Example Snippets

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

## 16) Multi-Agent Orchestration System

**See:** `.gemini/agent_orchestration.md` for complete details.

**Quick Reference:**
- 6-agent parallel orchestration workflow (Ultimate Orchestrator pattern)
- Automatic coordination for complex multi-domain tasks
- Subordinate agents: Integration, Control Systems, PSO, Documentation, Code Beautification
- Quality gates: ≥95% coverage critical, ≥85% overall, ≥7/8 system health

------

## 17) Documentation Quality Standards

**See:** `.gemini/documentation_quality.md` for complete details.

**Quick Reference:**
- Direct, not conversational (avoid "Let's explore...")
- Specific, not generic (no "comprehensive" without metrics)
- Technical, not marketing (facts over enthusiasm)
- Run: `python scripts/docs/detect_ai_patterns.py --file <file.md>`
- Target: <5 AI-ish patterns per file

------

## 18) Success Criteria

- Clean root (≤ 12 visible entries), caches removed, backups archived.
- Test coverage gates met (85% overall / 95% critical / 100% safety‑critical).
- Single‑threaded operation stable; no dependency conflicts; memory bounded.
- Clear, validated configuration; reproducible experiments.

------

### Appendix: Notes

- Keep this file authoritative for style, testing, and operational posture.
- Treat it as versioned team memory; update via PRs with a short change log.
- **CRITICAL**: All git operations must target: https://github.com/theSadeQ/dip-smc-pso.git
- **MANDATORY**: Automatic updates are REQUIRED for all repository changes
- Maintain clean, professional commit messages following the established pattern
