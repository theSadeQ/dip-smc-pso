# E015: Architectural Standards and Patterns

**Hosts**: Dr. Sarah Chen (Control Systems) & Alex Rivera (Software Engineering)

---

## Opening Hook

**Alex**: You're browsing a codebase and see a file called `simulation_context.py` in THREE different locations. Bug? Duplication? Tech debt?

**Sarah**: Nope! **Intentional architectural pattern** for import path flexibility!

**Alex**: Or you notice 8 different dynamics files (`simplified_dynamics.py`, `full_nonlinear_dynamics.py`, `lowrank_dynamics.py`...). Redundant?

**Sarah**: Nope! **Deliberate model variants** offering accuracy/speed tradeoffs!

**Alex**: This is why architectural standards matter. Without documentation, these patterns look like MISTAKES. With standards, they're FEATURES.

**Sarah**: This episode covers:
- **Architectural invariants**: Patterns you must NEVER "fix"
- **Design patterns**: Factory, strategy, dependency injection
- **Code conventions**: File naming, directory structure, style guides
- **Quality gates**: What gets enforced, what gets flagged

**Alex**: Let's explore the architecture that makes 100,000+ lines of code maintainable!

---

## Introduction: Why Architectural Standards?

**Sarah**: A codebase without standards is like a city without zoning laws:

**No standards**:
```
src/
├── controller.py (which controller?)
├── Controller_v2.py (why v2?)
├── CONTROLLER_NEW.py (uppercase?)
├── my_controller_final_FINAL.py (sigh...)
└── temp_controller_backup_old_2.py (delete this?)
```

**With standards**:
```
src/controllers/
├── classical_smc.py
├── sta_smc.py
├── adaptive_smc.py
└── hybrid_adaptive_sta_smc.py
```

**Alex**: Standards answer:
- **WHERE** to put code (directory structure)
- **HOW** to name things (files, classes, functions)
- **WHAT** patterns to use (factories, not if-else chains)
- **WHEN** to deviate (documented exceptions)

## Documentation Scale \& Organization

**Documentation Statistics:**

        `docs/NAVIGATION.md` connects all 11 navigation systems \\
        Persona-based entry points, "I Want To..." quick navigation

---

## Documentation Categories

**Organized by Purpose \& Audience:**

    \begin{tabular}{lll}
        \toprule
        **Category** & **Files** & **Audience** \\
        \midrule
        Getting Started & 12 & Beginners \\
        Tutorials & 18 & All levels \\
        Theory \& Algorithms & 45 & Advanced \\
        API Reference & 120 & Developers \\
        Research Workflows & 28 & Researchers \\
        Development Guides & 32 & Contributors \\
        System Architecture & 15 & Advanced developers \\
        AI Workspace & 171 & Claude Code \\
        \bottomrule
    \end{tabular}

        API reference auto-generated from docstrings using Sphinx autodoc \\
        Ensures documentation stays synchronized with code

---

## Navigation Philosophy

**Three Entry Points for Different User Needs:**

        - **Persona-Based Navigation**

            - \textit{"I'm a student learning control theory"}
            - \textit{"I'm a researcher validating algorithms"}
            - \textit{"I'm a developer contributing code"}
            - \textit{"I'm an instructor teaching SMC"}

        - **Intent-Based Navigation ("I Want To...")**

            - \textit{"I want to run my first simulation"}
            - \textit{"I want to tune controller gains"}
            - \textit{"I want to understand the theory"}
            - \textit{"I want to add a new controller"}

        - **Category-Based Navigation**

            - Browse by topic (Theory, Tutorials, API)
            - 43 category index files
            - Visual sitemaps for overview

---

## Design Patterns: Factory Pattern

**Sarah**: Let's start with the Factory pattern - the backbone of our controller creation system.

**Alex**: **Why Factory?** Because we have 7 controller types and this pattern eliminates massive if-else chains:

**Without Factory (Bad)**:
```python
def create_controller(ctrl_type, config):
    if ctrl_type == "classical_smc":
        return ClassicalSMC(gains=config.gains, ...)
    elif ctrl_type == "sta_smc":
        return STASMC(gains=config.gains, ...)
    elif ctrl_type == "adaptive_smc":
        return AdaptiveSMC(gains=config.gains, ...)
    # ... 4 more elif blocks
    else:
        raise ValueError(f"Unknown controller: {ctrl_type}")
```

**With Factory (Good)**:
```python
# src/controllers/factory.py
CONTROLLER_REGISTRY = {
    "classical_smc": ClassicalSMC,
    "sta_smc": STASMC,
    "adaptive_smc": AdaptiveSMC,
    "hybrid_adaptive_sta_smc": HybridAdaptiveSTASMC,
    "integral_smc": IntegralSMC,
    "terminal_smc": TerminalSMC,
    "swing_up_smc": SwingUpSMC,
}

def create_controller(ctrl_type: str, config: ControllerConfig):
    """Factory method for controller instantiation."""
    controller_class = CONTROLLER_REGISTRY.get(ctrl_type)
    if controller_class is None:
        available = ", ".join(CONTROLLER_REGISTRY.keys())
        raise ValueError(f"Unknown controller '{ctrl_type}'. Available: {available}")
    return controller_class(gains=config.gains, physics=config.physics)
```

**Sarah**: **Benefits**:
- **Extensibility**: Add new controller → register in dict → done
- **Discoverability**: `CONTROLLER_REGISTRY.keys()` lists all options
- **Type safety**: Single creation point enforces consistent interfaces

**Alex**: Real-world impact: Adding MPC controller took **5 minutes** (not 30 minutes of chasing if-else blocks).

---

## Design Patterns: Strategy Pattern

**Alex**: Strategy pattern lets us swap algorithms at runtime without changing client code.

**Sarah**: **Use case**: Dynamics models with different accuracy/performance tradeoffs.

**Strategy Interface**:
```python
# src/plant/core/dynamics_interface.py
class DynamicsInterface(ABC):
    @abstractmethod
    def compute_derivatives(self, state: np.ndarray, u: float) -> np.ndarray:
        """Compute state derivatives: dx/dt = f(x, u)"""
        pass

    @abstractmethod
    def get_state_dimension(self) -> int:
        """Return state dimension (4 for simplified, 6 for full)"""
        pass
```

**Concrete Strategies**:
```python
# src/plant/models/simplified_dynamics.py
class SimplifiedDynamics(DynamicsInterface):
    """Fast dynamics (no friction, small-angle approximation)"""
    def compute_derivatives(self, state, u):
        # Simplified equations, 2× faster
        return derivatives

# src/plant/models/full_nonlinear_dynamics.py
class FullNonlinearDynamics(DynamicsInterface):
    """Accurate dynamics (friction, exact trig, Coriolis terms)"""
    def compute_derivatives(self, state, u):
        # Full nonlinear equations, more accurate
        return derivatives

# src/plant/models/lowrank_dynamics.py
class LowRankDynamics(DynamicsInterface):
    """Reduced-order dynamics for fast batch optimization"""
    def compute_derivatives(self, state, u):
        # Dimensionality reduction for PSO
        return derivatives
```

**Client Code (Strategy-Agnostic)**:
```python
# src/core/simulation_runner.py
def run_simulation(controller, dynamics: DynamicsInterface, t_span, x0):
    """Works with ANY dynamics strategy"""
    def state_derivative(t, x):
        u = controller.compute_control(x, ...)
        return dynamics.compute_derivatives(x, u)

    solution = solve_ivp(state_derivative, t_span, x0, method='RK45')
    return solution
```

**Alex**: **Why this matters**: Switching from `SimplifiedDynamics` to `FullNonlinearDynamics` requires **zero changes** to simulation code.

**Sarah**: PSO uses `LowRankDynamics` for 50 generations × 30 particles = 1500 simulations. **3× speedup** vs full dynamics!

---

## Design Patterns: Dependency Injection

**Sarah**: Dependency Injection (DI) makes code testable and flexible.

**Alex**: **Bad approach (hard-coded dependencies)**:
```python
class Controller:
    def __init__(self, gains):
        self.monitor = LatencyMonitor(dt=0.01)  # Hard-coded!
        self.dynamics = FullNonlinearDynamics()  # Hard-coded!
```

**Problems**:
- Can't test without real `LatencyMonitor` (slow, non-deterministic)
- Can't swap dynamics models
- Can't disable monitoring in production

**Good approach (DI)**:
```python
class Controller:
    def __init__(self, gains, monitor: Optional[LatencyMonitor] = None,
                 dynamics: Optional[DynamicsInterface] = None):
        self.gains = gains
        self.monitor = monitor  # Injected dependency
        self.dynamics = dynamics  # Injected dependency

    def compute_control(self, state, ...):
        if self.monitor:
            start = self.monitor.start()

        u = self._compute_control_law(state)

        if self.monitor:
            self.monitor.end(start)

        return u
```

**Sarah**: Now we can inject **mock objects** for testing:
```python
# tests/test_controllers/test_classical_smc.py
def test_controller_without_monitoring():
    controller = ClassicalSMC(gains=[...], monitor=None)  # No monitoring overhead
    u = controller.compute_control(state, ...)
    assert -100 <= u <= 100

def test_controller_with_mock_dynamics():
    mock_dynamics = MockDynamics(return_value=np.zeros(4))
    controller = ClassicalSMC(gains=[...], dynamics=mock_dynamics)
    # Test controller in isolation
```

**Alex**: Production uses real dependencies, tests use mocks. **Best of both worlds!**

---

## Critical Architectural Patterns

**Alex**: Now the patterns that look like **bugs** but are actually **features**.

**Sarah**: These are **architectural invariants** - NEVER "fix" them!

### Pattern 1: Compatibility Layers

**File duplication you'll see**:
```
src/optimizer/           # Legacy path (backward compatibility)
src/optimization/        # New canonical path
```

**Why both exist**:
- External tools use `from src.optimizer import PSOTuner`
- New code uses `from src.optimization import PSOTuner`
- Both work via re-export: `src/optimizer/__init__.py` imports from `src/optimization/`

**Alex**: **NEVER delete** `src/optimizer/` - it's a compatibility shim, not duplication!

### Pattern 2: Re-export Chains

**File appears in 3 locations**:
```
src/core/simulation_context.py               # Canonical implementation
src/simulation_context.py                     # Root-level re-export
tests/simulation_context.py                   # Test-level re-export
```

**Why 3 copies**:
```python
# Import flexibility for different contexts
from src.core.simulation_context import SimulationContext  # Explicit
from src.simulation_context import SimulationContext       # Convenient
from simulation_context import SimulationContext           # Test-local
```

**Sarah**: This is **intentional import path flexibility**, not tech debt!

### Pattern 3: Model Variants

**8 dynamics files you'll find**:
```
src/plant/models/
├── simplified_dynamics.py        # Fast, small-angle approximation
├── full_nonlinear_dynamics.py    # Accurate, exact trig
├── lowrank_dynamics.py           # Reduced-order for PSO
├── friction_dynamics.py          # Friction-only model
├── coriolis_dynamics.py          # Coriolis-only model
├── linearized_dynamics.py        # Linearized around equilibrium
├── stochastic_dynamics.py        # Noise injection for robustness
└── hybrid_dynamics.py            # Mode-switching model
```

**Alex**: Each file serves a **different purpose**:
- `simplified_dynamics.py`: Tutorial code (easy to understand)
- `full_nonlinear_dynamics.py`: Production validation
- `lowrank_dynamics.py`: PSO optimization (3× faster)
- Others: Research variants for specific experiments

**Sarah**: NEVER "consolidate" these into one file - they're deliberate accuracy/speed tradeoffs!

### Pattern 4: Framework Files in Unexpected Places

**Alex**: You'll see this file and think "Should this be in tests/?"
```
src/interfaces/hil/test_automation.py
```

**Sarah**: NOPE! This is a **testing framework** (production code), not a **test file** (pytest code).

**Distinction**:
- **Test files** (`tests/test_*.py`): Use pytest, imported by pytest runner
- **Testing frameworks** (`src/**/test_*.py`): Provide infrastructure, imported by production code

**Example**:
```python
# src/interfaces/hil/test_automation.py (Framework - belongs in src/)
class HILTestFramework:
    """Framework for automating HIL experiments"""
    def run_test_sequence(self, scenarios): ...
    def validate_results(self, results): ...

# tests/test_hil/test_plant_server.py (Test - belongs in tests/)
def test_plant_server_timeout():
    """Pytest test using the framework"""
    framework = HILTestFramework()
    result = framework.run_test_sequence([...])
    assert result.success
```

---

## Directory Structure Rules

**Sarah**: Where to put code? Follow these rules:

### Rule 1: src/ = Production Code

**Criteria** (any ONE triggers src/ placement):
- Exported in `__init__.py`
- Imported by production code
- Framework/infrastructure code
- Provides reusable functionality

**Examples**:
```python
# src/controllers/classical_smc.py - CORRECT
# Exported in src/controllers/__init__.py, imported by simulate.py

# src/utils/validation.py - CORRECT
# Provides validate_state() used by all controllers

# src/interfaces/hil/test_automation.py - CORRECT
# Framework code, imported by src/hil/controller_client.py
```

### Rule 2: scripts/ = Development Tools

**Criteria** (ALL must be true):
- Executed directly (not imported)
- Development/automation tool
- Not part of production runtime

**Examples**:
```bash
# scripts/benchmarks/run_mt5.py - CORRECT
# Automation tool, executed via: python scripts/benchmarks/run_mt5.py

# scripts/docs/detect_ai_patterns.py - CORRECT
# Doc quality tool, executed via: python scripts/docs/detect_ai_patterns.py

# scripts/testing/run_coverage.py - CORRECT
# CI tool, executed via: python scripts/testing/run_coverage.py
```

### Rule 3: tests/ = Pytest Tests

**Criteria** (ALL must be true):
- Filename matches `test_*.py` or `*_test.py`
- Uses pytest imports (`import pytest`, `from pytest import ...`)
- Contains test functions (`def test_*()`)

**Examples**:
```python
# tests/test_controllers/test_classical_smc.py - CORRECT
import pytest
def test_classical_smc_stability(): ...

# tests/test_integration/test_memory_management.py - CORRECT
from pytest import fixture
@fixture
def controller(): ...
```

---

## Code Style Conventions

**Alex**: Naming rules that prevent chaos:

### File Naming

**Python modules**:
```
✓ classical_smc.py         # snake_case, descriptive
✓ pso_optimizer.py
✓ latency_monitor.py

✗ ClassicalSMC.py          # No PascalCase for files
✗ classical-smc.py         # No hyphens (breaks imports)
✗ classical_smc_v2.py      # No version suffixes
✗ classical_smc_FINAL.py   # No "final" labels
```

**Configuration files**:
```
✓ config.yaml              # Canonical config
✓ .pre-commit-config.yaml  # Tool-specific (hyphens OK)
✓ pytest.ini

✗ Config.yaml              # No capital first letter
✗ config_backup.yaml       # No backup suffixes
```

### Class Naming

```python
✓ class ClassicalSMC:          # PascalCase, acronyms uppercase
✓ class LatencyMonitor:
✓ class PSOTuner:

✗ class classical_smc:         # No snake_case
✗ class ClassicalSmc:          # Acronyms should be uppercase
✗ class Classical_SMC:         # No underscores in PascalCase
```

### Function Naming

```python
✓ def compute_control(state):        # snake_case, verb-noun
✓ def validate_state_bounds(state):
✓ def run_pso_optimization(params):

✗ def ComputeControl(state):         # No PascalCase
✗ def compute_Control(state):        # No camelCase
✗ def control(state):                # Missing verb
```

### Variable Naming

```python
✓ state_dimension = 4               # snake_case, descriptive
✓ max_iterations = 100
✓ dt = 0.01                         # Short names OK for math

✗ StateDimension = 4                # No PascalCase
✗ state_dim = 4                     # Avoid abbreviations
✗ sd = 4                            # Too cryptic (not math)
```

---

## Quality Gates (Enforce Strictly)

**Sarah**: These are the HARD LIMITS enforced by CI:

### Gate 1: Test Pass Rate
```
MANDATORY: 100% tests passing
Current: 668/668 passing [OK]
Action if failing: ALL work stops until fixed
```

### Gate 2: Critical Issues
```
MANDATORY: 0 critical issues
Examples: Security vulnerabilities, data corruption, safety violations
Action if found: Immediate rollback + root cause analysis
```

### Gate 3: Coverage Thresholds
```
REQUIRED:
- Overall: ≥85%
- Critical components (controllers, dynamics): ≥95%
- Safety-critical (saturation, bounds checking): 100%

Current: 87% overall [OK]
Action if failing: No merge to main
```

### Gate 4: Root Directory Cleanliness
```
REQUIRED: ≤19 visible items in project root
Current: 14 items [OK]
Threshold: 19 items (red flag at 20+)
Action if exceeded: Cleanup sprint required
```

### Gate 5: Documentation Build
```
MANDATORY: Sphinx docs build without warnings
Command: sphinx-build -M html docs docs/_build -W --keep-going
Action if failing: Fix warnings before merge
```

### Gate 6: Code Style
```
REQUIRED: Black + isort + flake8 pass
Command: pre-commit run --all-files
Action if failing: Auto-fix or manual correction
```

### Gate 7: Type Checking
```
REQUIRED: mypy passes on critical modules
Threshold: 0 errors in src/controllers/, src/core/, src/plant/
Action if failing: Add type hints or use # type: ignore with justification
```

### Gate 8: Filename Validation
```
MANDATORY: No malformed filenames
Forbidden:
- Windows device names (nul, con, prn, aux, com1-9, lpt1-9)
- Braces/spaces ({dir}/, my folder/)
- Unicode on Windows (emoji in filenames)
Action if found: Rename via git mv immediately
```

**Alex**: **Why so strict?** Because catching issues at commit time is 100× cheaper than catching them in production!

---

## Quality Audit Results (CA-02)

**Sarah**: Here's proof the standards work - results from our comprehensive audit:

### Coverage Analysis
```
Component                    Coverage    Status
--------------------------------------------
Controllers (critical)       98.7%       [OK]
Dynamics models (critical)   96.2%       [OK]
Simulation core (critical)   95.8%       [OK]
Optimization (important)     91.4%       [OK]
Utils (important)            88.3%       [OK]
HIL (important)              87.9%       [OK]
--------------------------------------------
Overall                      87.1%       [OK] (≥85% required)
```

### Test Pyramid
```
Unit tests:        542 (81%)     [OK] (target: 70-80%)
Integration tests:  98 (15%)     [OK] (target: 15-20%)
System tests:       28 (4%)      [OK] (target: 5-10%)
--------------------------------------------
Total:             668 (100%)    [OK]
```

### Architectural Compliance
```
Gate                          Status
----------------------------------------
Dependency injection usage    100%  [OK]
Factory pattern compliance    100%  [OK]
Strategy pattern usage         95%  [OK]
Proper directory placement     98%  [OK]
Naming convention adherence    97%  [OK]
```

**Alex**: **5% strategy gap** comes from experimental MPC controller (still hardcodes some dynamics). Tracked in technical debt register.

---

## Architectural Decision Records (ADRs)

**Sarah**: Major design decisions are documented as ADRs:

**Example: ADR-003 - Factory Pattern for Controllers**
```markdown
# ADR-003: Factory Pattern for Controller Instantiation

**Status**: Accepted (Oct 2025)

**Context**: Adding new controllers required modifying 5+ files (simulate.py,
streamlit_app.py, tests, benchmarks, docs). High coupling, error-prone.

**Decision**: Implement factory pattern with registry dictionary.

**Consequences**:
- Positive: Adding controller = single dict entry, extensible, testable
- Negative: Indirection (registry lookup), less obvious from IDE
- Mitigation: Registry is well-documented, IDE autocomplete works via type hints

**Alternatives Considered**:
- If-else chain: Rejected (not extensible)
- Plugin system: Rejected (too complex for 7 controllers)
- Abstract factory: Rejected (overkill, no controller families)
```

**Alex**: ADRs answer "Why did we do it this way?" when reviewing code 6 months later.

---

## Common Anti-Patterns (Avoid These)

**Alex**: Patterns that seem reasonable but violate our standards:

### Anti-Pattern 1: God Objects
```python
# BAD: One class doing everything
class Controller:
    def compute_control(self, state): ...
    def log_telemetry(self, state): ...
    def plot_results(self, results): ...
    def save_to_database(self, results): ...
    def send_email_report(self, results): ...
    # 500 lines later...
```

**Fix: Single Responsibility Principle**
```python
# GOOD: Separate concerns
class Controller:
    def compute_control(self, state): ...  # Only control logic

class TelemetryLogger:
    def log(self, state): ...  # Only logging

class ResultsVisualizer:
    def plot(self, results): ...  # Only plotting
```

### Anti-Pattern 2: Magic Numbers
```python
# BAD: Unexplained constants
def compute_control(error):
    return 10.5 * error + 3.2 * integral + 0.8 * derivative
```

**Fix: Named Constants**
```python
# GOOD: Self-documenting
KP = 10.5  # Proportional gain (tuned via PSO)
KI = 3.2   # Integral gain
KD = 0.8   # Derivative gain

def compute_control(error):
    return KP * error + KI * integral + KD * derivative
```

### Anti-Pattern 3: Mutable Default Arguments
```python
# BAD: Mutable default (shared across calls!)
def add_state(state, history=[]):
    history.append(state)
    return history
```

**Fix: None Default + Initialize Inside**
```python
# GOOD: Fresh list each call
def add_state(state, history=None):
    if history is None:
        history = []
    history.append(state)
    return history
```

---

## Summary: Architectural Lessons

**Sarah**: What makes this architecture successful?

**Alex**: **Three core principles**:

1. **Intentional Patterns Over Clever Code**
   - Factory pattern beats if-else cleverness
   - Strategy pattern beats inheritance hierarchies
   - DI beats hard-coded dependencies

2. **Standards Prevent Chaos**
   - 8 quality gates enforced at commit time
   - Directory rules (src/ vs scripts/ vs tests/)
   - Naming conventions (no "final_v2_REALLY_FINAL.py")

3. **Document the Why**
   - ADRs explain design decisions
   - CLAUDE.md captures architectural invariants
   - Comments explain non-obvious patterns

**Sarah**: **Key metrics**:
- 87.1% test coverage (≥85% required)
- 668 tests (100% passing)
- 14 visible root items (≤19 limit)
- 0 critical issues (100% quality gates)
- 50× productivity gain from good tooling (MT-5: 8 min vs 2 days)

**Alex**: The architecture isn't perfect, but it's **maintainable**, **extensible**, and **documented**.

**Sarah**: And that's what matters when you're managing 100,000+ lines of code!

**Alex**: Standards beat cleverness. Every. Single. Time.

---

## Resources

- **Repository:** https://github.com/theSadeQ/dip-smc-pso.git
- **Documentation:** `docs/` directory
- **Getting Started:** `docs/guides/getting-started.md`

---

*Educational podcast episode generated from comprehensive presentation materials*
