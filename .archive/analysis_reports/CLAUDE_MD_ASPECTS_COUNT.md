# CLAUDE.md Aspects Count

**Analysis Date:** 2025-10-09
**Source:** `CLAUDE.md` (D:\Projects\main\CLAUDE.md)

---

## Main Documentation Sections (17)

1. **Repository Information** - Remote URL, branch strategy
2. **Automatic Repository Management** - Auto-update policy, commit formats, error handling
3. **Session Continuity System** - Zero-effort account switching, session state management
4. **Project Overview** - Double-inverted pendulum SMC/PSO framework
5. **Architecture** - Module structure, directory layout
6. **Key Technologies** - Python stack, libraries, frameworks
7. **Usage & Essential Commands** - CLI workflows for simulation, PSO, HIL, testing
8. **Configuration System** - YAML validation, parameter domains
9. **Development Guidelines** - Code style, controller development, batch simulation
10. **Testing & Coverage Standards** - Test architecture, coverage targets, quality gates
11. **Visualization & Analysis Toolkit** - Animations, plots, statistical analysis
12. **Production Safety & Readiness** - Safety score, dependency/memory/SPOF fixes
13. **Workspace Organization & Hygiene** - Clean root rules, artifact management, file placement
14. **Controller Memory Management** - Weakref patterns, cleanup protocols (Issue #15)
15. **Controller Factory & Example Snippets** - Code examples for common workflows
16. **Multi-Agent Orchestration System** - 6-agent parallel workflow architecture
17. **Success Criteria** - Quality gates and operational standards

---

## Thematic Aspects (10 Categories)

Grouped by functional themes:

1. **Version Control & Automation** (Sections 1-2)
2. **Session Management** (Section 3)
3. **Technical Architecture** (Sections 4-6)
4. **Configuration & Usage** (Sections 7-8)
5. **Development Practices** (Sections 9-10)
6. **Analysis & Visualization** (Section 11)
7. **Production Engineering** (Sections 12, 14)
8. **Workspace Hygiene** (Section 13)
9. **AI Orchestration** (Section 16)
10. **Quality Standards** (Section 17)

---

## Detailed Aspect Counts

### Category 1: Version Control & Automation (9 aspects)

**Section 1: Repository Information (3 aspects)**
1. Primary Repository URL
2. Branch Strategy (main branch deployment)
3. Working Directory path

**Section 2: Automatic Repository Management (6 subsections)**

**2.1 Auto-Update Policy**
- Mandatory automatic git operations after ANY changes
- 3-step workflow: stage → commit → push

**2.2 Commit Message Format**
- Structured template with action/description/details
- ASCII markers ([AI]) instead of emojis
- Co-authorship attribution

**2.3 Repository Address Verification**
- Remote verification commands
- URL correction procedures

**2.4 Trigger Conditions**
- 6 trigger types: source code, config, docs, new files, tests, structure changes

**2.5 Update Sequence**
- 4-step bash workflow with verification
- HEREDOC commit message formatting

**2.6 Error Handling**
- Error reporting protocol
- Resolution steps
- Operation blocking on failures

**Total:** 9 aspects (3 from Section 1, 6 from Section 2)

#### Related Files
- `.git/` - Git repository directory
- `CLAUDE.md` - Main project documentation
- `.gitignore` - Git ignore patterns
- Git configuration and hooks

---

### Category 2: Session Management (45+ aspects)

**Section 3: Session Continuity System (9 subsections)**

**3.1 Overview**
- Zero-effort account switching concept
- 3-step user experience workflow
- No manual handoff requirement

**3.2 Auto-Detection Protocol (MANDATORY)**
- First message session state check
- Recency evaluation (<24 hours)
- Auto-load vs fresh session decision
- Detection code pattern with examples

**3.3 Session State Maintenance (MANDATORY)**
- 5 update trigger types:
  1. Completing todo items
  2. Making important decisions
  3. Starting new tasks/changing phases
  4. Modifying significant files
  5. Identifying next actions
- Code examples for each trigger

**3.4 Token Limit Protocol**
- 4-step handoff procedure:
  1. Mark token limit approaching
  2. Ensure comprehensive state
  3. Commit session state
  4. User account switch (automatic)

**3.5 Session State File Structure**
- File location specification
- Complete JSON schema with 10 fields:
  - session_id, last_updated, account, token_limit_approaching, status
  - context, todos, decisions, next_actions, files_modified, important_context

**3.6 Integration with Automated Backups**
- Automatic 1-minute commit cycle
- Session state inclusion in backups
- Git history audit trail

**3.7 Python Helper: session_manager.py**
- File location
- 8 key functions with signatures:
  - has_recent_session(), load_session(), get_session_summary()
  - update_session_context(), add_completed_todo(), add_decision()
  - add_next_action(), mark_token_limit_approaching(), finalize_session()

**3.8 Benefits**
- 6 benefits listed with [OK] markers:
  - Zero manual handoff
  - Automatic resume
  - Audit trail
  - Reliability (JSON schema validation)
  - Transparency
  - Efficiency

**3.9 Example Usage**
- 2 complete session examples:
  - Session 1 (Account A hitting limit)
  - Session 2 (Account B resuming)
- Includes code snippets and expected behavior

**Aspect Breakdown:**
- 3 overview concepts (3.1)
- 4 auto-detection components (3.2)
- 5 maintenance triggers + code examples (3.3)
- 4 token limit steps (3.4)
- 10 JSON schema fields (3.5)
- 3 backup integration features (3.6)
- 8 Python helper functions (3.7)
- 6 documented benefits (3.8)
- 2 usage examples (3.9)

**Total:** 45+ aspects

#### Related Files
- `.dev_tools/session_state.json` - Session state storage (JSON format)
- `.dev_tools/session_manager.py` - Python helper functions for session management
- `.dev_tools/claude-backup.ps1` - PowerShell backup script (1-minute automation)
- Task Scheduler configuration for automated backups

---

### Category 3: Technical Architecture (17 aspects)

**Section 4: Project Overview (2 aspects)**
1. System description (DIP SMC PSO)
2. Framework capabilities overview

**Section 5: Architecture (8 aspects)**

**5.1 High-Level Modules (6 aspects)**
1. Controllers (6 variants)
2. Dynamics/Plant models
3. Core Engine
4. Optimization
5. Utils
6. HIL

**5.2 Representative Layout (2 aspects)**
1. Directory tree structure
2. Top-level files list

**Section 6: Key Technologies (7 aspects)**
1. Python 3.9+
2. NumPy, SciPy, Matplotlib
3. Numba optimization
4. PySwarms/Optuna
5. Pydantic validation
6. pytest framework
7. Streamlit UI

**Total:** 17 aspects (2 + 8 + 7)

#### Related Files
- `src/controllers/` - Controller implementations
  - `classic_smc.py`, `sta_smc.py`, `adaptive_smc.py`
  - `hybrid_adaptive_sta_smc.py`, `swing_up_smc.py`, `mpc_controller.py`
  - `factory.py` - Controller factory
- `src/core/` - Core simulation engine
  - `dynamics.py`, `dynamics_full.py`
  - `simulation_runner.py`, `simulation_context.py`, `vector_sim.py`
- `src/plant/` - Plant models
  - `models/simplified/`, `models/full/`, `models/lowrank/`
  - `configurations/`, `core/`
- `src/optimizer/` - Optimization algorithms
  - `pso_optimizer.py`
- `src/utils/` - Utility modules
  - `validation/`, `control/`, `monitoring/`, `visualization/`, `analysis/`
  - `types/`, `reproducibility/`, `development/`
- `src/hil/` - Hardware-in-the-loop
  - `plant_server.py`, `controller_client.py`
- `simulate.py` - CLI entry point
- `streamlit_app.py` - Web UI
- `requirements.txt` - Dependencies

---

### Category 4: Configuration & Usage (17 aspects)

**Section 7: Usage & Essential Commands (14 aspects)**

**7.1 Simulations (4 command patterns)**
1. Basic simulation with plot
2. STA-SMC simulation
3. Load tuned gains and simulate
4. Print configuration

**7.2 PSO Optimization (3 command patterns)**
1. Optimize classical SMC gains
2. Optimize adaptive SMC with seed
3. Optimize hybrid STA-SMC

**7.3 HIL (2 command patterns)**
1. Run HIL with plot
2. Run HIL with custom config

**7.4 Testing (4 command patterns)**
1. Run all tests
2. Run specific controller tests
3. Run benchmarks only
4. Run with coverage report

**7.5 Web Interface (1 command pattern)**
1. Launch Streamlit app

**Section 8: Configuration System (3 aspects)**
1. Central config.yaml with strict validation
2. Configuration domains (physics, controller, PSO, simulation, HIL)
3. Configuration-first philosophy

**Total:** 17 aspects (14 + 3)

#### Related Files
- `config.yaml` - Main configuration file (Pydantic-validated)
- `simulate.py` - CLI entry point for all commands
- `streamlit_app.py` - Web interface
- `run_tests.py` - Test runner helper
- `requirements.txt` - Dependency specifications
- Custom configuration files (e.g., `custom_config.yaml`)
- Tuned gains JSON files (e.g., `tuned_gains.json`, `gains_classical.json`)

---

### Category 5: Development Practices (23 aspects)

**Section 9: Development Guidelines (10 aspects)**

**9.1 Code Style (4 aspects)**
1. Type hints everywhere
2. Clear, example-rich docstrings
3. ASCII header format for Python files
4. Error handling philosophy (explicit error types, conversational comments)

**9.2 Adding New Controllers (4 aspects)**
1. Implement in `src/controllers/`
2. Add to `src/controllers/factory.py`
3. Extend `config.yaml`
4. Add tests under `tests/test_controllers/`

**9.3 Batch Simulation (1 aspect)**
- Code example with run_batch_simulation

**9.4 Configuration Loading (1 aspect)**
- Code example with load_config

**Section 10: Testing & Coverage Standards (13 aspects)**

**10.1 Architecture of Tests (6 aspects)**
1. Unit tests
2. Integration tests
3. Property-based tests
4. Benchmarks
5. Scientific validation
6. Command examples (3 patterns)

**10.2 Coverage Targets (3 aspects)**
1. Overall ≥85%
2. Critical components ≥95%
3. Safety-critical 100%

**10.3 Quality Gates (MANDATORY) (4 aspects)**
1. Every new `.py` file has a `test_*.py` peer
2. Every public function/method has dedicated tests
3. Validate theoretical properties for critical algorithms
4. Include performance benchmarks for perf-critical code

**Total:** 23 aspects (10 + 13)

#### Related Files
- `src/controllers/` - Controller implementation directory
  - `factory.py` - Controller factory registry
- `src/core/vector_sim.py` - Batch simulation functions
- `src/config.py` - Configuration loading utilities
- `tests/` - All test directories
  - `test_controllers/` - Controller-specific tests
  - `test_benchmarks/` - Performance benchmarks
  - `test_integration/` - Integration tests
- `.gitignore` - Comprehensive ignore patterns
- `pytest.ini` - pytest configuration (if exists)
- `.hypothesis/` - Hypothesis framework data
- Coverage configuration files

---

### Category 6: Analysis & Visualization (9 aspects)

**Section 11: Visualization & Analysis Toolkit (9 aspects)**

**Real-time Visualization (3 aspects)**
1. DIPAnimator
2. Static performance plots
3. Project movie generator

**Statistical Analysis (6 aspects)**
4. Confidence intervals
5. Bootstrap methods
6. Welch's t-test
7. ANOVA
8. Monte Carlo analysis
9. Real-time control loop monitoring (latency, deadlines, weakly-hard constraints)

**Total:** 9 aspects

#### Related Files
- `src/utils/visualization/` - Visualization utilities
  - DIPAnimator class
  - Plot generation modules
  - Movie generator
- `src/utils/analysis/` - Statistical analysis tools
  - Bootstrap methods
  - Statistical tests (t-test, ANOVA)
  - Monte Carlo analysis
- `src/utils/monitoring/` - Real-time monitoring
  - `latency.py` - LatencyMonitor class
  - Deadline tracking
  - Weakly-hard constraint monitoring

---

### Category 7: Production Engineering (29 aspects)

**Section 12: Production Safety & Readiness (9 aspects)**

**Overall Status (1 aspect)**
1. Production Readiness Score: 6.1/10

**Verified Improvements (3 aspects)**
2. Dependency safety
3. Memory safety
4. SPOF removal

**Outstanding Risks (1 aspect)**
5. Thread safety (NOT production ready for multi-threading)

**Validation Commands (4 aspects)**
6. Dependency verification
7. Memory leak testing
8. SPOF validation
9. Thread safety testing (currently failing)

**Section 14: Controller Memory Management (20 aspects)**

**Overview (2 aspects)**
1. Explicit memory cleanup implementation
2. Issue #15 resolution date

**Key Patterns (4 aspects)**
1. Weakref for Model References
2. Explicit Cleanup
3. Automatic Cleanup (Destructor)
4. Production Memory Monitoring

**Memory Leak Prevention Checklist (5 aspects)**
1. Periodic controller recreation
2. Active memory monitoring
3. Periodic history buffer clearing
4. Garbage collection after batch operations
5. Memory leak test validation

**Usage Patterns (3 aspects)**
1. Short-lived (single simulation)
2. Long-running (server deployment)
3. Batch operations (PSO optimization)

**Validation Commands (2 aspects)**
1. Quick memory leak test (1000 instantiations)
2. 8-hour stress test

**Acceptance Criteria (4 aspects)**
1. No memory leaks in 8-hour continuous operation
2. Memory growth < 1MB per 1000 instantiations
3. Explicit cleanup methods for all 4 controller types
4. Automated production memory monitoring available

**Total:** 29 aspects (9 + 20)

#### Related Files
- `scripts/verify_dependencies.py` - Dependency verification script
- `scripts/test_memory_leak_fixes.py` - Memory leak validation
- `scripts/test_spof_fixes.py` - SPOF validation
- `scripts/test_thread_safety_fixes.py` - Thread safety testing (currently failing)
- `docs/memory_management_patterns.md` - Memory management comprehensive guide
- `docs/memory_management_quick_reference.md` - Quick lookup reference
- `tests/test_integration/test_memory_management/` - Memory leak tests
  - `test_memory_resource_deep.py` - Deep memory validation
- `src/controllers/` - All controllers with cleanup methods
  - `smc.py` (ClassicalSMC with weakref and cleanup)
  - `sta_smc.py`, `adaptive_smc.py`, `hybrid_adaptive_sta_smc.py`

---

### Category 8: Workspace Hygiene (70+ aspects)

**Section 13: Workspace Organization & Hygiene (8 subsections)**

**13.1 Clean Root (3 aspects)**
1. Visible files (≤6)
2. Visible directories (≤6)
3. Hidden development directories

**13.2 Universal Cache Cleanup (1 aspect)**
1. Cache cleanup command

**13.3 Backup & Docs Artifacts (2 aspects)**
1. Backup file cleanup
2. Documentation build artifacts

**13.4 Enhanced .gitignore (1 aspect)**
1. Comprehensive ignore patterns

**13.5 Automation & Verification (4 aspects)**
1. Clean view helper
2. Root item count health check
3. Cache detection
4. Backup file detection

**13.6 Session Artifact Management (MANDATORY) (~40 aspects)**

**File Placement Rules (5 aspects)**
1. Logs → `logs/`
2. Test artifacts → `.test_artifacts/`
3. Optimization results → `optimization_results/{controller}_{date}/`
4. Documentation → `docs/` or `.archive/`
5. Scripts → `scripts/` with subdirectories

**Before Session Ends Checklist (6 aspects)**
1. Move all logs to `logs/`
2. Delete or archive test artifacts
3. Organize optimization results
4. Move root-level scripts
5. Archive temporary documentation
6. Verify root item count and clean caches

**File Naming Conventions (4 aspects)**
1. Logs format
2. Optimization directories format
3. Test artifacts format
4. Archived docs format

**Acceptable Root Items (3 aspects)**
1. Core Files (6)
2. Core Directories (6)
3. Hidden Directories (acceptable, unlimited)

**File Organization Enforcement (~22 aspects)**
- 4 critical questions (decision tree)
- File Type Directory Map (8 entries)
- 3 wrong vs correct example scenarios
- 4 session end enforcement commands
- 1 auto-cleanup command
- 2 additional organizational guidelines

**13.7 Long-Running Optimization Processes (PSO) (16 aspects)**

**Before Starting PSO (3 aspects)**
1. Verify Configuration
2. Prepare Monitoring
3. Session Continuity

**During PSO Execution (9 aspects - 3 categories)**
- Monitoring Tools (3 aspects)
- Progress Tracking (3 aspects)
- Resource Management (3 aspects)

**After PSO Completion (3 aspects - 3 categories)**
- Immediate Actions
- Decision Point
- Cleanup

**Automation Templates (2 aspects)**
1. End-to-End PSO Workflow
2. Validation Pipeline

**Lessons Learned (5 aspects from Issue #12)**
1. Fitness Function Matters
2. Document Expected Outcomes
3. Prepare Alternative Paths
4. Full Automation
5. Comprehensive Handoff

**13.8 After Moving/Consolidation (4 aspects)**
1. Search & replace hardcoded paths
2. Update README and diagrams
3. Fix CI workflows
4. Re-run tests

**Total:** 70+ aspects

#### Related Files
**Core Directories (6 visible):**
- `src/` - Source code
- `tests/` - Test suites
- `docs/` - Documentation
- `notebooks/` - Jupyter notebooks
- `benchmarks/` - Performance tests
- `scripts/` - Utility scripts
  - `scripts/optimization/` - PSO and optimization scripts
  - `scripts/analysis/` - Analysis scripts
  - `scripts/utils/` - Utility scripts

**Core Files (6 visible):**
- `simulate.py` - CLI entry
- `streamlit_app.py` - Web UI
- `config.yaml` - Configuration
- `requirements.txt` - Dependencies
- `README.md` - Documentation
- `CHANGELOG.md` - Version history

**Hidden Development Directories:**
- `.archive/` - Historical files, backups
  - `.archive/analysis_reports/` - Analysis and audit reports
  - `.archive/docs_{date}/` - Archived documentation
- `.test_artifacts/` - Temporary test runs (auto-cleanup)
- `.dev_tools/` - Development utilities
  - `.dev_tools/session_state.json`
  - `.dev_tools/session_manager.py`
  - `.dev_tools/clean_view.sh`
- `.build/` - Build artifacts
- `.coverage/` - Coverage data
- `.artifacts/` - Temporary build outputs

**Artifact Directories:**
- `logs/` - All log files
  - `logs/pso_runs_archive/` - Archived PSO runs
- `optimization_results/` - Optimization artifacts
  - `optimization_results/{controller}_{date}/` - Timestamped results

**Cache Directories (to be cleaned):**
- `__pycache__/` - Python bytecode cache
- `.pytest_cache/` - pytest cache
- `.ruff_cache/` - Ruff linter cache
- `.numba_cache/` - Numba compilation cache
- `.benchmarks/` - Benchmark cache
- `.hypothesis/` - Hypothesis data

**Configuration Files:**
- `.gitignore` - Enhanced ignore patterns
- `CLAUDE.md` - Project instructions (or `.CLAUDE.md`)

---

### Category 9: AI Orchestration (38 aspects)

**Section 16: Multi-Agent Orchestration System (5 subsections)**

**16.1 Core Agent Architecture (24 aspects)**

**Ultimate Orchestrator (4 aspects)**
1. Strategic planning and dependency-free task decomposition
2. Parallel delegation to 5 subordinate specialist agents
3. Integration of artifacts and interface reconciliation
4. Final verification, validation, and production readiness assessment

**Subordinate Specialist Agents (5 agents - counted as 5 aspects)**
1. Integration Coordinator
2. Control Systems Specialist
3. PSO Optimization Engineer
4. Documentation Expert
5. Code Beautification Specialist

**Documentation Expert Capabilities (8 aspects)**
1. Mathematical Documentation
2. Controller Implementation Guides
3. Optimization Documentation
4. HIL Systems Documentation
5. Scientific Validation Documentation
6. Configuration Schema Documentation
7. Performance Engineering Documentation
8. Testing Documentation

**Code Beautification Specialist Capabilities (9 aspects)**
1. ASCII Header Management
2. Deep Internal Folder Organization
3. Advanced Static Analysis
4. Type System Enhancement
5. Import Organization & Dependency Management
6. Enterprise Directory Architecture
7. Performance & Memory Optimization
8. Architecture Pattern Enforcement
9. Version Control & CI Integration

**16.2 Orchestration Protocol (Automatic) (3 aspects)**
1. Planning Phase (4 steps)
2. Parallel Agent Execution
3. Integration & Verification (4 steps)

**16.3 Usage Examples (3 aspects)**
1. Integration Validation
2. Critical Fixes Orchestration
3. Code Beautification Workflow

**16.4 Expected Artifacts Pattern (4 aspects)**
1. `validation/` directory
2. `patches/` directory
3. `artifacts/` directory
4. JSON Reports

**16.5 Quality Assurance Integration (4 aspects)**
1. Coverage Thresholds
2. Validation Matrix
3. Production Gates
4. Regression Detection

**Total:** 38 aspects (24 + 3 + 3 + 4 + 4)

#### Related Files
- `prompt/` - Orchestration prompt specifications
  - `prompt/integration_recheck_validation_prompt.md`
  - `prompt/integration_critical_fixes_orchestration.md`
- `validation/` - Validation artifacts from orchestration
  - Test results
  - System health scores
  - Coverage reports
- `patches/` - Integration improvement patches
  - Controller fixes
  - Optimization enhancements
  - Configuration updates
- `artifacts/` - Orchestration artifacts
  - Configuration samples
  - Optimization results
  - Convergence plots
  - Performance benchmarks
- Orchestration JSON reports (structured data for CI/automation)

---

### Category 10: Quality Standards (9 aspects)

**Section 17: Success Criteria (9 aspects)**

1. Clean root (≤12 visible entries)
2. Caches removed
3. Backups archived
4. Test coverage gates met (85% overall, 95% critical, 100% safety-critical)
5. Single-threaded operation stable
6. No dependency conflicts
7. Memory bounded
8. Clear validated configuration
9. Reproducible experiments

**Total:** 9 aspects

#### Related Files
- `config.yaml` - Validated configuration
- `pytest.ini` - pytest configuration
- `.coverage/` - Coverage data directory
- `tests/` - Complete test suite
- Coverage report outputs (`htmlcov/`, coverage.xml)
- Benchmark results
- CI/CD configuration files (e.g., `.github/workflows/`)
- Quality gate scripts and validation tools

---

## Summary Table

| Category | Sections | Subsections | Aspects |
|----------|----------|-------------|---------|
| 1. Version Control & Automation | 2 | 6 | 9 |
| 2. Session Management | 1 | 9 | 45+ |
| 3. Technical Architecture | 3 | 2 | 17 |
| 4. Configuration & Usage | 2 | 5 | 17 |
| 5. Development Practices | 2 | 7 | 23 |
| 6. Analysis & Visualization | 1 | 0 | 9 |
| 7. Production Engineering | 2 | 6 | 29 |
| 8. Workspace Hygiene | 1 | 8 | 70+ |
| 9. AI Orchestration | 1 | 5 | 38 |
| 10. Quality Standards | 1 | 0 | 9 |
| **TOTAL** | **16** | **48** | **266+** |

---

## Complexity Distribution

| Category | Aspects | % of Total |
|----------|---------|------------|
| Workspace Hygiene | 70+ | 26.3% |
| Session Management | 45+ | 16.9% |
| AI Orchestration | 38 | 14.3% |
| Production Engineering | 29 | 10.9% |
| Development Practices | 23 | 8.6% |
| Technical Architecture | 17 | 6.4% |
| Configuration & Usage | 17 | 6.4% |
| Version Control & Automation | 9 | 3.4% |
| Quality Standards | 9 | 3.4% |
| Analysis & Visualization | 9 | 3.4% |

---

## Key Insights

**Most Comprehensive Sections:**
1. Section 13: Workspace Hygiene (70+ aspects)
2. Section 3: Session Management (45+ aspects)
3. Section 16: AI Orchestration (38 aspects)

**Documentation Coverage:**
Your CLAUDE.md documentation is comprehensive, covering:
- Operational workflows
- Technical architecture
- Development standards
- AI-assisted automation
- Production readiness
- Quality assurance

This represents a complete "team memory" system for the project.
