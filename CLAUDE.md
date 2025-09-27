# CLAUDE.md — Team Memory & Project Conventions

> This file contains project-specific instructions for Claude Code operations and automatic repository management.

------

## 1) Repository Information

**Primary Repository**: https://github.com/theSadeQ/dip-smc-pso.git
**Branch Strategy**: Main branch deployment
**Working Directory**: D:\Projects\main

------

## 2) Automatic Repository Management

### 2.1 Auto-Update Policy

**MANDATORY**: After ANY changes to the repository content, Claude MUST automatically:

1. **Stage all changes**: `git add .`
2. **Commit with descriptive message**: Following the established pattern
3. **Push to main branch**: `git push origin main`

### 2.2 Commit Message Format

```
<Action>: <Brief description>

- <Detailed change 1>
- <Detailed change 2>
- <Additional context if needed>

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 2.3 Repository Address Verification

Before any git operations, verify the remote repository:
```bash
git remote -v
# Expected output:
# origin	https://github.com/theSadeQ/dip-smc-pso.git (fetch)
# origin	https://github.com/theSadeQ/dip-smc-pso.git (push)
```

If the remote is incorrect, update it:
```bash
git remote set-url origin https://github.com/theSadeQ/dip-smc-pso.git
```

### 2.4 Trigger Conditions

Claude MUST automatically update the repository when:
- Any source code files are modified
- Configuration files are changed
- Documentation is updated
- New files are added
- Test files are modified
- Any project structure changes occur

### 2.5 Update Sequence

```bash
# 1. Verify repository state
git status
git remote -v

# 2. Stage all changes
git add .

# 3. Commit with descriptive message
git commit -m "$(cat <<'EOF'
<Descriptive title>

- <Change 1>
- <Change 2>
- <Additional context>

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# 4. Push to main branch
git push origin main
```

### 2.6 Error Handling

If git operations fail:
1. Report the error to the user
2. Provide suggested resolution steps
3. Do not proceed with further operations until resolved

------

## 3) Project Overview

**Double‑Inverted Pendulum Sliding Mode Control with PSO Optimization**

A comprehensive Python framework for simulating, controlling, and analyzing a double‑inverted pendulum (DIP) system. It provides multiple SMC variants, optimization (PSO), a CLI and a Streamlit UI, plus rigorous testing and documentation.

------

## 2) Architecture

### 2.1 High‑Level Modules

- **Controllers**: classical SMC, super‑twisting, adaptive, hybrid adaptive STA‑SMC, swing‑up; experimental MPC.
- **Dynamics/Plant**: simplified and full nonlinear dynamics (plus low‑rank); shared base interfaces.
- **Core Engine**: simulation runner, unified simulation context, batch/Numba vectorized simulators.
- **Optimization**: PSO tuner (operational); additional algorithms staged via an optimization core.
- **Utils**: validation, control primitives (e.g., saturation), monitoring, visualization, analysis, types, reproducibility, dev tools.
- **HIL**: plant server + controller client for hardware‑in‑the‑loop experiments.

### 2.2 Representative Layout (merged)

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

## 3) Key Technologies

- Python 3.9+
- NumPy, SciPy, Matplotlib
- Numba for vectorized/batch simulation
- PySwarms / Optuna for optimization (PSO primary)
- Pydantic‑validated YAML configs
- pytest + pytest‑benchmark; Hypothesis where useful
- Streamlit for UI

------

## 4) Usage & Essential Commands

### 4.1 Simulations

```bash
python simulate.py --ctrl classical_smc --plot
python simulate.py --ctrl sta_smc --plot
python simulate.py --load tuned_gains.json --plot
python simulate.py --print-config
```

### 4.2 PSO Optimization

```bash
python simulate.py --ctrl classical_smc --run-pso --save gains_classical.json
python simulate.py --ctrl adaptive_smc --run-pso --seed 42 --save gains_adaptive.json
python simulate.py --ctrl hybrid_adaptive_sta_smc --run-pso --save gains_hybrid.json
```

### 4.3 HIL

```bash
python simulate.py --run-hil --plot
python simulate.py --config custom_config.yaml --run-hil
```

### 4.4 Testing

```bash
python run_tests.py
python -m pytest tests/test_controllers/test_classical_smc.py -v
python -m pytest tests/test_benchmarks/ --benchmark-only
python -m pytest tests/ --cov=src --cov-report=html
```

### 4.5 Web Interface

```bash
streamlit run streamlit_app.py
```

------

## 5) Configuration System

- Central `config.yaml` with strict validation.
- Domains: physics params, controller settings, PSO parameters, simulation settings, HIL config.
- Prefer “configuration first”: define parameters before implementation changes.

------

## 6) Development Guidelines

### 6.1 Code Style

- Type hints everywhere; clear, example‑rich docstrings.
- ASCII header format for Python files (≈90 chars width).
- Explicit error types; avoid broad excepts.

### 6.2 Adding New Controllers

1. Implement in `src/controllers/`.
2. Add to `src/controllers/factory.py`.
3. Extend `config.yaml`.
4. Add tests under `tests/test_controllers/`.

### 6.3 Batch Simulation

```python
from src.core.vector_sim import run_batch_simulation
results = run_batch_simulation(controller, dynamics, initial_conditions, sim_params)
```

### 6.4 Configuration Loading

```python
from src.config import load_config
config = load_config("config.yaml", allow_unknown=False)
```

------

## 7) Testing & Coverage Standards

### 7.1 Architecture of Tests

- Unit, integration, property‑based, benchmarks, and scientific validation.
- Example patterns:

```bash
pytest tests/test_controllers/ -k "not integration"
pytest tests/ -k "full_dynamics"
pytest --benchmark-only --benchmark-compare --benchmark-compare-fail=mean:5%
```

### 7.2 Coverage Targets

- **Overall** ≥ 85%
- **Critical components** (controllers, plant models, simulation engines) ≥ 95%
- **Safety‑critical** mechanisms: **100%**

### 7.3 Quality Gates (MANDATORY)

- Every new `.py` file has a `test_*.py` peer.
- Every public function/method has dedicated tests.
- Validate theoretical properties for critical algorithms.
- Include performance benchmarks for perf‑critical code.

------

## 8) Visualization & Analysis Toolkit

- Real‑time animations (DIPAnimator), static performance plots, project movie generator.
- Statistical analysis: confidence intervals, bootstrap, Welch’s t‑test, ANOVA, Monte Carlo.
- Real‑time monitoring (latency, deadline misses, weakly‑hard constraints) for control loops.

------

## 9) Production Safety & Readiness (Snapshot)

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

## 10) Workspace Organization & Hygiene

### 10.1 Clean Root

Keep visible items ≤ 12 (core files/dirs only). Hide dev/build clutter behind dot‑prefixed folders.

**Visible files**: `simulate.py`, `streamlit_app.py`, `config.yaml`, `requirements.txt`, `README.md`, `CHANGELOG.md`

**Visible dirs**: `src/`, `tests/`, `docs/`, `notebooks/`, `benchmarks/`, `config/`

**Hidden dev dirs (examples)**: `.archive/`, `.build/`, `.dev_tools/`, `.scripts/`, `.tools/`
 Move **CLAUDE.md → .CLAUDE.md** if you prefer a clean root.

### 10.2 Universal Cache Cleanup

```bash
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
rm -rf .pytest_cache .ruff_cache .numba_cache .benchmarks .hypothesis
```

### 10.3 Backup & Docs Artifacts

```bash
find . -name "*.bak" -o -name "*.backup" -o -name "*~" | xargs -I{} mv {} .archive/ 2>/dev/null
# Docs build artifacts → archive
mv docs/_build docs/_static docs/.github docs/.gitignore docs/.lycheeignore .archive/
```

### 10.4 Enhanced .gitignore

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

### 10.5 Automation & Verification

```bash
# Helper for a clean view
echo "(create) .dev_tools/clean_view.sh to list essentials, key dirs, hidden tools"

# Health checks
ls | wc -l                                    # target ≤ 12
find . -name "__pycache__" | wc -l            # target = 0
find . -name "*.bak" -o -name "*.backup" -o -name "*~" | wc -l  # target = 0
```

### 10.6 After Moving/Consolidation — Update References

1. Search & replace hardcoded paths.
2. Update README and diagrams.
3. Fix CI workflows.
4. Re‑run tests.

------

## 11) Controller Factory & Example Snippets

```python
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

## 12) Multi-Agent Orchestration System

**6-Agent Parallel Orchestration Workflow**

This project employs an advanced **Ultimate Orchestrator** pattern for complex multi-domain tasks. The system automatically coordinates 6 specialized agents working in parallel to maximize efficiency and ensure comprehensive coverage.

### 12.1 Core Agent Architecture

**🔵 Ultimate Orchestrator (Blue)** - Master conductor and headless CI coordinator
- Strategic planning and dependency-free task decomposition
- Parallel delegation to 5 subordinate specialist agents
- Integration of artifacts and interface reconciliation
- Final verification, validation, and production readiness assessment

**Subordinate Specialist Agents (Parallel Execution):**
- 🌈 **Integration Coordinator** - Cross-domain orchestration, system health, configuration validation
- 🔴 **Control Systems Specialist** - Controller factory, SMC logic, dynamics models, stability analysis
- 🔵 **PSO Optimization Engineer** - Parameter tuning, optimization workflows, convergence validation
- 🟢 **Control Systems Documentation Expert** - Specialized technical writing for control theory and optimization systems
- 🟣 **Code Beautification & Directory Organization Specialist** - Advanced codebase aesthetic and structural optimization expert

**🟢 Documentation Expert Capabilities:**
  - **Mathematical Documentation**: Lyapunov stability proofs, sliding surface design theory, convergence analysis, PSO algorithmic foundations with LaTeX notation
  - **Controller Implementation Guides**: SMC variant documentation (classical, super-twisting, adaptive, hybrid STA-SMC), parameter tuning methodology, stability margin analysis
  - **Optimization Documentation**: PSO parameter bounds rationale, fitness function design, convergence criteria, multi-objective optimization strategies, benchmark interpretation
  - **HIL Systems Documentation**: Real-time communication protocols, safety constraint specifications, latency analysis, hardware interface contracts
  - **Scientific Validation Documentation**: Experimental design for control systems, statistical analysis of performance metrics, Monte Carlo validation, benchmark comparison methodology
  - **Configuration Schema Documentation**: YAML validation rules, parameter interdependencies, migration guides, configuration validation workflows
  - **Performance Engineering Documentation**: Numba optimization guides, vectorized simulation scaling analysis, memory usage profiling, real-time constraint validation
  - **Testing Documentation**: Property-based test design for control laws, coverage analysis for safety-critical components, scientific test validation, benchmark regression analysis

**🟣 Code Beautification & Directory Organization Specialist Capabilities:**
  - **ASCII Header Management**: Enforcement of 90-character wide ASCII banners with centered file paths, validation of `#===...===\\\` format compliance, automated header generation and correction across Python files
  - **Deep Internal Folder Organization**: Hierarchical restructuring of files within directories to match architectural patterns, test structure mirroring src/ layout, controller categorization by type (base/, factory/, mpc/, smc/, specialized/), utility organization into logical subdirectories (analysis/, control/, monitoring/, types/, validation/, visualization/), elimination of file dumping in favor of proper logical placement
  - **Advanced Static Analysis**: Cyclomatic complexity analysis, code duplication detection, dead code elimination, security vulnerability scanning, maintainability index calculation
  - **Type System Enhancement**: Comprehensive type hint coverage analysis (target: 95%), missing annotation detection, generic type optimization, return type inference
  - **Import Organization & Dependency Management**: Import sorting (standard → third-party → local), unused import detection and removal, circular dependency resolution, dependency version audit
  - **Enterprise Directory Architecture**: Module placement validation against architectural patterns, file naming convention enforcement, package initialization standardization, hidden directory management, proper hierarchical nesting to prevent flat file structures
  - **Performance & Memory Optimization**: Numba compilation target identification, vectorization opportunity detection, memory leak pattern recognition, generator vs list comprehension optimization
  - **Architecture Pattern Enforcement**: Factory pattern compliance validation, singleton pattern detection, observer pattern implementation verification, dependency injection container optimization
  - **Version Control & CI Integration**: Commit message formatting, branch naming convention enforcement, pre-commit hook optimization, CI/CD pipeline file organization

### 12.2 Orchestration Protocol (Automatic)

When Claude encounters complex multi-domain problems, it automatically:

1. **Ultimate Orchestrator Planning Phase:**
   - Reads problem specification (e.g., `prompt/integration_recheck_validation_prompt.md`)
   - Extracts objectives, constraints, acceptance criteria
   - Creates dependency-free execution plan with artifacts
   - Generates JSON delegation specification

2. **Parallel Agent Execution:**
   ```bash
   # Automatic parallel launch (single message, multiple Task calls):
   Task(ultimate-orchestrator) -> delegates to:
     ├─ Task(integration-coordinator)
     ├─ Task(control-systems-specialist)
     ├─ Task(pso-optimization-engineer)
     ├─ Task(documentation-expert)
     └─ Task(code-beautification-directory-specialist)
   ```

3. **Integration & Verification:**
   - Collects artifacts from all subordinate agents
   - Reconciles interfaces and data contracts
   - Prepares unified patches and validation reports
   - Executes verification commands and quality gates

### 12.3 Usage Examples

**Integration Validation:**
```bash
# Problem: D:\Projects\main\prompt\integration_recheck_validation_prompt.md
# Auto-deploys: Ultimate Orchestrator + 5 specialists in parallel
# Result: 90% system health, production deployment approved
```

**Critical Fixes Orchestration:**
```bash
# Problem: D:\Projects\main\prompt\integration_critical_fixes_orchestration.md
# Auto-deploys: All 6 agents with strategic coordination
# Result: 100% functional capability, all blocking issues resolved
```

**Code Beautification Workflow:**
```bash
# Problem: Code style and organization optimization
# Auto-deploys: Ultimate Orchestrator + Code Beautification Specialist
# Beautifies: ASCII headers, directory structure, import organization, type hints
# Result: 100% style compliance, optimized file organization
```

### 12.4 Expected Artifacts Pattern

Each orchestration produces standardized outputs:
- **`validation/`** - Comprehensive test results and health scores
- **`patches/`** - Minimal diffs for integration improvements
- **`artifacts/`** - Configuration samples and optimization results
- **JSON Reports** - Structured data for CI/automation consumption

### 12.5 Quality Assurance Integration

The orchestrator enforces quality gates:
- **Coverage Thresholds:** ≥95% critical components, ≥85% overall
- **Validation Matrix:** Must pass ≥7/8 system health components
- **Production Gates:** Automated go/no-go deployment decisions
- **Regression Detection:** Systematic comparison with baseline claims

This **headless CI coordinator** approach ensures consistent, high-quality results across complex multi-domain engineering tasks while maintaining full traceability and reproducibility.

------

## 13) Success Criteria

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