# CLAUDE.md — Team Memory & Project Conventions

> This file contains project-specific instructions for Claude Code operations and automatic repository management.

**Note:** This file uses ASCII text markers (e.g., [AI], [OK], [BLUE]) instead of Unicode emojis for Windows terminal compatibility. All documentation and scripts should follow this pattern to ensure proper display on Windows systems with cp1252 encoding.

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

## 3) Session Continuity System

**See:** `.ai/config/session_continuity.md` for complete details.

**Quick Reference:**
- Zero-effort account switching via `.dev_tools/session_state.json`
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

**See:** `.ai/config/testing_standards.md` for complete details.

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
- NEVER create files in root except: simulate.py, streamlit_app.py, config.yaml, requirements.txt, README.md, CHANGELOG.md, CLAUDE.md

**Full Details:**
- Comprehensive guide: `.ai/config/workspace_organization.md`
- Oct 2025 cleanup lessons (370MB recovered): `.ai/config/WORKSPACE_CLEANUP_2025-10-09.md`

------

## 14) Controller Memory Management

**See:** `.ai/config/controller_memory.md` for complete details.

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

**See:** `.ai/config/agent_orchestration.md` for complete details.

**Quick Reference:**
- 6-agent parallel orchestration workflow (Ultimate Orchestrator pattern)
- Automatic coordination for complex multi-domain tasks
- Subordinate agents: Integration, Control Systems, PSO, Documentation, Code Beautification
- Quality gates: ≥95% coverage critical, ≥85% overall, ≥7/8 system health

------

## 17) Documentation Quality Standards

**See:** `.ai/config/documentation_quality.md` for complete details.

**Quick Reference:**
- Direct, not conversational (avoid "Let's explore...")
- Specific, not generic (no "comprehensive" without metrics)
- Technical, not marketing (facts over enthusiasm)
- Run: `python scripts/docs/detect_ai_patterns.py --file <file.md>`
- Target: <5 AI-ish patterns per file

------

## 18) Documentation Build System

**MANDATORY FOR CLAUDE**: After ANY changes to documentation source files or static assets, you MUST rebuild the HTML documentation and verify changes are live.

### 18.1 Auto-Rebuild Triggers

**Rebuild Required When Modifying:**
- Sphinx source files: `docs/*.md`, `docs/**/*.rst`
- Static assets: `docs/_static/*.css`, `docs/_static/*.js`, `docs/_static/*.png`
- Configuration: `docs/conf.py`, `docs/_templates/*`
- Navigation: `docs/index.rst`, any `toctree` directives

### 18.2 Mandatory Rebuild Workflow

```bash
# 1. Make changes to docs
# 2. ALWAYS rebuild:
sphinx-build -M html docs docs/_build -W --keep-going

# 3. Verify changes copied (timestamps):
stat docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 4. Verify content matches (MD5):
md5sum docs/_static/your-file.css docs/_build/html/_static/your-file.css

# 5. Verify localhost serves new version:
curl -s "http://localhost:9000/_static/your-file.css" | grep "YOUR_CHANGE"
```

### 18.3 Browser Cache Handling

**CRITICAL**: Browsers cache static assets. After rebuild:

```bash
# Verify localhost serves your changes:
curl -s "http://localhost:9000/_static/code-collapse.css" | grep "YOUR_UNIQUE_COMMENT"
```

**Always tell user to hard refresh:**
- Chrome/Edge: Ctrl+Shift+R (Win) / Cmd+Shift+R (Mac)
- Firefox: Ctrl+F5 (Win) / Cmd+Shift+R (Mac)

### 18.4 Common Pitfalls

❌ **Don't assume changes are live** - always verify with `curl` or `stat`
❌ **Don't skip rebuild** - Sphinx doesn't auto-rebuild static files
❌ **Don't forget browser cache** - tell user to hard refresh

✅ **Do verify timestamps** - `stat` both source and build files
✅ **Do check MD5 sums** - ensure files actually copied
✅ **Do test with curl** - verify localhost serves new content

### 18.5 Example: CSS/JS Changes

```bash
# After editing docs/_static/code-collapse.css:
sphinx-build -M html docs docs/_build -W --keep-going

# Verify copy succeeded:
stat docs/_static/code-collapse.css docs/_build/html/_static/code-collapse.css
md5sum docs/_static/code-collapse.css docs/_build/html/_static/code-collapse.css

# Verify localhost serves new version:
curl -s "http://localhost:9000/_static/code-collapse.css" | grep "CRITICAL FIX"

# Tell user: "Hard refresh browser (Ctrl+Shift+R) to clear cache"
```

### 18.6 Example: Markdown/RST Changes

```bash
# After editing docs/guides/getting-started.md:
sphinx-build -M html docs docs/_build -W --keep-going

# Verify HTML updated:
stat docs/guides/getting-started.md docs/_build/html/guides/getting-started.html
```

------

## 19) Model Context Protocol (MCP) Auto-Triggers

**See:** `docs/mcp-debugging/README.md` for complete workflows | `.mcp.json` for server configuration

### 19.1 Automatic MCP Usage Rules

**FOR CLAUDE**: These rules are instructions for AI behavior, NOT requirements for user prompts.

**USER NOTE**: You DON'T need to use exact keywords or craft special prompts. Just ask naturally!
- "Where's the adaptive SMC?" → Claude uses context7 + filesystem automatically
- "Is this data good?" → Claude uses pandas-mcp + numpy-mcp automatically
- "Test the dashboard" → Claude uses puppeteer automatically

**MANDATORY FOR CLAUDE**: Claude MUST automatically use MCP servers when these conditions are detected:

#### Pandas MCP - Auto-trigger when:
- Analyzing CSV/JSON data files (PSO results, simulation logs)
- Computing statistics (mean, std, confidence intervals)
- Plotting convergence curves or performance metrics
- Keywords: "analyze data", "plot results", "statistical analysis", "convergence"

#### Context7 MCP - Auto-trigger when:
- Searching documentation for specific topics
- Finding related code/docs across the project
- Validating cross-references between files
- Keywords: "find", "search docs", "where is", "related to", "references"

#### Puppeteer MCP - Auto-trigger when:
- Testing Streamlit dashboard functionality
- Validating UI elements or layouts
- Taking screenshots of dashboard views
- Keywords: "test dashboard", "streamlit UI", "screenshot", "validate interface"

#### NumPy MCP - Auto-trigger when:
- Matrix operations (inversion, decomposition, eigenvalues)
- Numerical computations for control theory
- Linear algebra validations
- Keywords: "matrix", "eigenvalue", "numerical", "compute"

#### Git MCP - Auto-trigger when:
- Analyzing commit history beyond basic `git log`
- Complex branch operations
- Commit statistics or contributor analysis
- Keywords: "commit history", "branch analysis", "git stats"

#### SQLite MCP - Auto-trigger when:
- Querying PSO optimization results database
- Analyzing historical optimization runs
- Generating reports from stored results
- Keywords: "query results", "optimization history", "database"

#### Pytest MCP - Auto-trigger when:
- Debugging test failures with detailed traces
- Analyzing test patterns or flaky tests
- Keywords: "test failure", "pytest debug", "why test failed"

### 19.2 Configuration

**All servers enabled:** `.ai/config/settings.local.json` sets `"enableAllProjectMcpServers": true`

**Server definitions:** `.mcp.json` (11 configured servers)

### 19.3 Multi-MCP Collaboration Examples

**Single-MCP Tasks:**
```bash
# Context7 only
"Find documentation about sliding mode control"

# Pandas only
"Load and describe optimization_results/latest.csv"
```

**Multi-MCP Workflows (ENCOURAGED):**
```bash
# 3-MCP Pipeline: Research → Analysis → Computation
"Search documentation for PSO theory, then analyze convergence data from
optimization_results/pso_run_20250113.csv and compute statistical significance"
→ Triggers: context7 → pandas-mcp → numpy-mcp

# 4-MCP Pipeline: Search → Read → Test → Analyze
"Find the adaptive SMC controller code, inspect its implementation,
test it on the dashboard, and analyze its performance metrics"
→ Triggers: context7 → filesystem → puppeteer → pandas-mcp

# 5-MCP Pipeline: Quality → Lint → History → Fix → Test
"Analyze code quality issues in controllers, trace when they were introduced,
suggest fixes, and validate with pytest"
→ Triggers: mcp-analyzer → git-mcp → filesystem → pytest-mcp → sequential-thinking

# Database + Analysis Pipeline
"Query all PSO runs from the database where convergence < 0.01,
load the corresponding CSV files, and compute confidence intervals"
→ Triggers: sqlite-mcp → filesystem → pandas-mcp → numpy-mcp

# Complete Documentation Pipeline
"Search for all references to chattering mitigation, read the related files,
analyze git blame for authorship, and generate a cross-reference report"
→ Triggers: context7 → filesystem → git-mcp → pandas-mcp
```

### 19.4 Custom Slash Commands with MCP

- `/analyze-logs` → Pandas MCP + SQLite MCP for log analysis
- `/debug-with-mcp` → Multi-server integrated debugging
- `/inspect-server` → MCP Inspector for server testing
- `/analyze-dashboard` → Puppeteer MCP for UI validation
- `/test-browser` → Playwright/Puppeteer for dashboard testing

### 19.5 Development Guidelines

**Adding New MCP Servers:**
1. Add server config to `.mcp.json` with clear description
2. Add to `mcp_usage` section with specific use cases
3. Define auto-trigger keywords in this section
4. Document in `docs/mcp-debugging/`
5. Test with relevant workflows

**Auto-trigger Requirements:**
- Clear keyword matching (e.g., "analyze data" → pandas-mcp)
- **Multiple servers SHOULD activate simultaneously for complex tasks**
- No user confirmation needed (auto-approved)
- Fallback to manual tools if MCP unavailable

**MCP Collaboration Patterns (MANDATORY):**
- **Data Analysis Pipeline**: filesystem → pandas-mcp → numpy-mcp → sqlite-mcp
- **Documentation Workflow**: context7 → filesystem → git-mcp (find → read → trace history)
- **Testing Pipeline**: pytest-mcp → puppeteer → pandas-mcp (debug → UI test → analyze results)
- **Code Quality**: mcp-analyzer → filesystem → git-mcp (lint → inspect → commit analysis)
- **Research Workflow**: context7 → pandas-mcp → numpy-mcp (search theory → load data → compute)
- **Debugging Session**: sequential-thinking → pytest-mcp → filesystem (systematic → test trace → code inspection)

### 19.6 Available MCP Servers (11 Total)

| Server | Auto-Trigger Keywords | Primary Use Cases |
|--------|----------------------|-------------------|
| **pandas-mcp** | analyze, plot, statistics, convergence | Data analysis, PSO results |
| **context7** | find, search, where, related | Doc search, cross-refs |
| **puppeteer** | test, screenshot, UI, dashboard | Streamlit testing |
| **numpy-mcp** | matrix, eigenvalue, numerical | Linear algebra ops |
| **filesystem** | inspect, read, analyze files | Code/log analysis |
| **github** | issue, PR, commit | Issue tracking |
| **sequential-thinking** | debug, systematic, multi-step | Complex debugging |
| **git-mcp** | git history, branch, stats | Advanced Git ops |
| **sqlite-mcp** | query, database, results | PSO results DB |
| **pytest-mcp** | test failure, pytest, debug | Test debugging |
| **mcp-analyzer** | lint, ruff, vulture, quality | Code quality checks |

### 19.7 MCP Orchestration Philosophy

**Why Multi-MCP is Superior:**
- **Single-MCP**: Limited to one domain (e.g., pandas can only analyze data)
- **Multi-MCP**: Complete workflows across domains (search → read → analyze → test → validate)
- **Efficiency**: One complex request > multiple simple requests
- **Context preservation**: MCPs share results within the same Claude response

**How Claude Should Think:**
1. **Identify task domains**: "Search docs" = context7, "analyze data" = pandas, "test UI" = puppeteer
2. **Chain dependencies**: What output from MCP A feeds into MCP B?
3. **Parallel vs Sequential**: Independent tasks → parallel; dependent tasks → sequential
4. **Always prefer more MCPs**: If 3 MCPs can solve it better than 1, use all 3

**Examples of Orchestration Thinking:**

❌ **Bad (Single-MCP thinking):**
```
User: "Find the controller and analyze its test results"
Claude: Uses context7 to find controller → stops
         User asks again → uses pandas to analyze → stops
```

✅ **Good (Multi-MCP orchestration):**
```
User: "Find the controller and analyze its test results"
Claude: context7 (find file) → filesystem (read code) →
        pytest-mcp (get test results) → pandas-mcp (analyze metrics) →
        numpy-mcp (compute statistics) → Complete answer in one response
```

**Mandatory Orchestration Rules (FOR CLAUDE):**
1. If user mentions 2+ domains (docs + data + testing), use 2+ MCPs
2. For "complete analysis" tasks, use full pipeline (3-5 MCPs minimum)
3. For debugging tasks, always combine sequential-thinking + domain-specific MCPs
4. For research workflows, always: context7 → filesystem → relevant analysis MCPs
5. Never ask user "should I also analyze X?" - just do it with appropriate MCP
6. **Understand intent, not keywords**: "where is" = search, "check" = analyze, "test" = validate
7. **Be proactive**: If task implies data analysis, use pandas even if not explicitly requested
8. **Chain automatically**: Don't wait for user to ask for next step, complete the full workflow

### 19.8 Natural Language Flexibility (For Users)

**You can ask in ANY of these ways - all work the same:**

| Your Natural Request | What Claude Understands | MCPs Used |
|---------------------|------------------------|-----------|
| "Where's the code for X?" | Search + Read | context7 → filesystem |
| "Show me X" | Search + Read | context7 → filesystem |
| "Find X implementation" | Search + Read | context7 → filesystem |
| "I need to see X" | Search + Read | context7 → filesystem |
| **All trigger same MCPs** | ↑ | ↑ |
|  |  |  |
| "Is this CSV any good?" | Load + Analyze | pandas-mcp → numpy-mcp |
| "Check this data file" | Load + Analyze | pandas-mcp → numpy-mcp |
| "What's in this optimization result?" | Load + Analyze | pandas-mcp → numpy-mcp |
| "Analyze these numbers" | Load + Analyze | pandas-mcp → numpy-mcp |
| **All trigger same MCPs** | ↑ | ↑ |
|  |  |  |
| "Does the UI work?" | Test Interface | puppeteer |
| "Test the dashboard" | Test Interface | puppeteer |
| "Check if page loads" | Test Interface | puppeteer |
| "Screenshot the app" | Test Interface | puppeteer |
| **All trigger same MCPs** | ↑ | ↑ |

**The Point**: Speak naturally! Claude figures out intent → picks right MCPs → chains them intelligently.

**DON'T STRESS ABOUT:**
- Exact keywords ("analyze" vs "check" vs "look at")
- MCP names (never say "use pandas-mcp")
- Prompt structure (questions, commands, descriptions all work)
- Triggering tools (Claude does this automatically)

**JUST ASK NATURALLY:**
- "What's wrong with this controller?" (triggers: filesystem → pytest-mcp → sequential-thinking)
- "Check that optimization run" (triggers: pandas-mcp → numpy-mcp)
- "Find docs about PSO and show me the code" (triggers: context7 → filesystem)

### 19.9 Troubleshooting

**Server won't start:**
```bash
# Verify configuration
cat .mcp.json | grep -A5 "server-name"

# Check if npx/node available
npx --version

# Check Python servers
python -m pip list | grep mcp
```

**See Also:**
- `docs/mcp-debugging/QUICK_REFERENCE.md` - Quick troubleshooting
- `docs/mcp-debugging/workflows/` - Complete workflows
- `.mcp.json` - Full server configuration

------

## 20) Phase 3 UI/UX Status & Maintenance Mode

**Phase 3 Completion**: ✅ **COMPLETE** (October 9-16, 2025)
**Status**: Merged to main | UI work in maintenance mode
**Handoff Document**: `.codex/phase3/HANDOFF.md`

### What Was Accomplished

**UI Issues Resolved**: 17/34 (50% | All Critical/High severity complete)
- WCAG 2.1 Level AA compliant (97.8/100 Lighthouse accessibility)
- Design tokens consolidated (18 core tokens, 94% stability)
- Responsive validated (4 breakpoints: 375px, 768px, 1024px, 1920px)
- Cross-platform parity (Sphinx + Streamlit, 100% token reuse)
- Performance optimized (<3KB gzipped CSS budget met)

**Browser Support**:
- ✅ Chromium (Chrome/Edge): Validated across all UI features
- ⏸️ Firefox/Safari: Deferred (research audience <5%, standard CSS)

### UI Maintenance Mode (Current Policy)

**DO**:
- Fix Critical/High severity bugs if users report issues
- Update docs when adding new controllers/features
- Maintain WCAG AA compliance for new UI elements

**DON'T**:
- Proactively work on 17 deferred Medium/Low issues
- Spend time on Firefox validation
- Implement "nice-to-have" UI polish

### 17 Deferred Issues

**Medium Severity (7)**: UI-006, UI-009, UI-010, UI-011, UI-015, UI-017, UI-018
**Low Severity (10)**: UI-012, UI-013, UI-014, UI-016, UI-019, UI-028, UI-030, UI-032, UI-034

**Rationale for Deferral**:
- All Critical/High resolved (no user blockers)
- Diminishing returns (2-3 weeks for <10% improvement)
- Research focus prioritized over UI perfectionism

### Phase 4 Decision

**Skip Phase 4 Production Hardening** if:
- Research-only use case (local/academic environment)
- Single-user operation
- No cloud deployment planned

**Execute Phase 4** only if:
- Planning production deployment (cloud, multi-user)
- Industrial applications requiring stability
- Multi-threaded operation needed

**Current Recommendation**: Skip Phase 4, focus on research (controllers, PSO, SMC theory)

------

## 21) Success Criteria

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
