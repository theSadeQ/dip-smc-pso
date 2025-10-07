# Week 3: Optimization & Simulation Modules - Complete Documentation Plan

**Project:** DIP_SMC_PSO Documentation Enhancement
**Phase:** Week 3 - Optimization & Simulation Modules
**Duration:** 10-14 days | **Effort:** 25-30 hours
**Target Files:** ~102 Python files (optimization + core/simulation)
**Status:** 📋 PLANNED

---

## Executive Summary

Week 3 builds on the successful Week 2 controllers documentation (7,450+ lines) to comprehensively document the **optimization and simulation infrastructure** that powers the DIP-SMC-PSO system. This week covers:

- **PSO Optimization Framework** (~60 files) - Particle swarm, evolutionary algorithms, Bayesian optimization
- **Core Simulation Engine** (~42 files) - Dynamics models, integration methods, batch simulation
- **Mathematical Foundations** - Convergence theory, Lagrangian mechanics, numerical analysis
- **Practical Workflows** - End-to-end optimization tutorials, performance benchmarking

**Expected Deliverables:**
- **~8,000 lines** of research-grade markdown documentation
- **10-12 major technical guides** with embedded source code
- **9+ tutorials** covering beginner to advanced optimization workflows
- **30+ code examples** demonstrating PSO integration and simulation patterns
- **Full Sphinx integration** with hierarchical navigation

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [Phase 1: Mathematical Foundations (Days 1-2)](#phase-1-mathematical-foundations-days-1-2)
3. [Phase 2: PSO Optimization Module (Days 3-5)](#phase-2-pso-optimization-module-days-3-5)
4. [Phase 3: Simulation & Dynamics (Days 6-8)](#phase-3-simulation--dynamics-days-6-8)
5. [Phase 4: Tutorials & Examples (Days 9-10)](#phase-4-tutorials--examples-days-9-10)
6. [Phase 5: Sphinx Integration & QA (Day 11)](#phase-5-sphinx-integration--qa-day-11)
7. [Quality Standards](#quality-standards)
8. [Acceptance Criteria](#acceptance-criteria)

---

## Module Overview

### Optimization Module Structure

```
src/optimization/
├── algorithms/                  # Algorithm implementations
│   ├── swarm/                   # PSO and variants (12 files)
│   │   ├── pso_core.py             # Core PSO algorithm
│   │   ├── advanced_pso.py         # Adaptive inertia, constriction
│   │   ├── multi_objective_pso.py  # Pareto optimization
│   │   └── memory_efficient_pso.py # Large-scale optimization
│   ├── evolutionary/            # Genetic algorithms (8 files)
│   │   ├── genetic.py              # Genetic algorithm implementation
│   │   ├── differential.py         # Differential evolution
│   │   └── evolution_strategies.py # CMA-ES, ES variants
│   ├── gradient_based/          # Gradient methods (6 files)
│   │   ├── bfgs.py                 # BFGS quasi-Newton
│   │   ├── nelder_mead.py          # Simplex method
│   │   └── adam.py                 # Adaptive gradient descent
│   ├── bayesian/                # Bayesian optimization (5 files)
│   │   ├── gaussian_process.py     # GP surrogate models
│   │   ├── acquisition.py          # EI, UCB, PI functions
│   │   └── bayesian_optimizer.py   # Main BO implementation
│   └── base.py                  # Abstract optimizer interface
├── objectives/                  # Objective function library
│   ├── control/                 # Control-specific objectives (10 files)
│   │   ├── tracking_error.py       # ISE, ITAE, RMSE
│   │   ├── stability_metrics.py    # Overshoot, settling time
│   │   ├── chattering_index.py     # Chattering quantification
│   │   └── multi_objective.py      # Weighted objectives
│   └── base.py                  # Objective interface
├── constraints/                 # Constraint handling (8 files)
│   ├── bounds.py                # Simple bounds
│   ├── penalty.py               # Penalty methods
│   ├── barrier.py               # Barrier functions
│   └── projection.py            # Projection methods
├── integration/                 # Controller integration (6 files)
│   ├── factory_adapter.py       # Controller factory integration
│   ├── gain_wrapper.py          # Gain vector handling
│   └── simulation_runner.py     # Optimization-simulation bridge
├── core/                        # Core infrastructure (5 files)
│   ├── optimizer_interface.py   # Unified optimizer protocol
│   ├── parameter_space.py       # Search space definition
│   └── convergence.py           # Convergence detection
└── benchmarks/                  # Optimization benchmarks (5 files)
    ├── test_functions.py        # Rastrigin, Rosenbrock, etc.
    └── performance_profiling.py # Benchmark suite

Total: ~60 optimization files
```

### Core/Simulation Module Structure

```
src/core/
├── dynamics.py                  # Simplified dynamics (linearized)
├── dynamics_full.py             # Full nonlinear dynamics
├── simulation_runner.py         # Main simulation orchestrator
├── simulation_context.py        # Unified simulation state
├── vector_sim.py                # Numba batch simulator
├── safety_guards.py             # Numerical stability checks
└── __init__.py

src/simulation/ (if exists)
├── integration/                 # Integration methods
│   ├── euler.py                 # Euler method
│   ├── rk4.py                   # 4th-order Runge-Kutta
│   ├── rk45.py                  # Adaptive RK45 (Dormand-Prince)
│   └── comparison.py            # Method comparison framework
├── state_management/            # State handling
│   ├── history.py               # State history tracking
│   └── checkpointing.py         # Simulation checkpoints
└── performance/                 # Performance optimization
    ├── numba_kernels.py         # Compiled simulation kernels
    └── batch_processing.py      # Parallel simulation

Total: ~42 core/simulation files
```

---

## Phase 1: Mathematical Foundations (Days 1-2)

**Duration:** 2 days | **Effort:** 6-8 hours
**Target:** 2,600 lines of mathematical theory documentation

### 1.1 PSO Algorithm Theory

**File:** `docs/mathematical_foundations/pso_algorithm_theory.md`
**Target:** 800 lines

**Content Structure:**

#### 1.1.1 Swarm Intelligence Foundations (150 lines)
- Origins: Bird flocking, fish schooling, social behavior
- Collective intelligence principles
- Emergence of optimal behavior from simple rules

#### 1.1.2 PSO Mathematical Formulation (200 lines)

**Particle Dynamics:**
```
v_{i}^{t+1} = ω·v_{i}^{t} + c₁·r₁·(p_{best,i} - x_{i}^{t}) + c₂·r₂·(g_{best} - x_{i}^{t})
x_{i}^{t+1} = x_{i}^{t} + v_{i}^{t+1}
```

Where:
- $v_i^t$: Velocity of particle i at iteration t
- $x_i^t$: Position of particle i at iteration t
- $p_{best,i}$: Personal best position of particle i
- $g_{best}$: Global best position across swarm
- $ω$: Inertia weight (exploration vs exploitation)
- $c_1, c_2$: Cognitive and social coefficients
- $r_1, r_2$: Random values in [0,1]

#### 1.1.3 Convergence Analysis (250 lines)

**Theorem (PSO Convergence):**
Under certain parameter conditions, PSO converges to stationary points:

```
Condition: χ = 2κ / |2 - φ - √(φ² - 4φ)|
where φ = c₁ + c₂ > 4, κ ∈ [0,1]

Then: lim_{t→∞} E[||x_i^t - x*||²] = 0
```

**Proof outline:**
1. Define Lyapunov function V(t) = E[||x(t) - x*||²]
2. Show V̇(t) < 0 under parameter constraints
3. Invoke LaSalle's invariance principle

#### 1.1.4 Parameter Selection Guidelines (150 lines)
- **Inertia weight ω:**
  - High (0.9): Global exploration
  - Low (0.4): Local exploitation
  - Adaptive: ω(t) = 0.9 - 0.5·(t/T_max)

- **Cognitive/Social coefficients (c₁, c₂):**
  - Balanced: c₁ = c₂ = 2.05 (common choice)
  - Social focus: c₂ > c₁ (faster convergence, premature)
  - Cognitive focus: c₁ > c₂ (slower, more robust)

#### 1.1.5 Advanced PSO Variants (50 lines)
- Adaptive PSO (time-varying parameters)
- Multi-objective PSO (Pareto fronts)
- Quantum PSO (quantum mechanics inspired)
- Comprehensive learning PSO (CLPSO)

**Code Embedding:**
```markdown
### PSO Core Implementation

\`\`\`{literalinclude} ../../../src/optimization/algorithms/swarm/pso_core.py
:language: python
:linenos:
:lines: 1-100
:emphasize-lines: 45-52
\`\`\`

**Line-by-line explanation:**
- **Lines 45-47**: Velocity update with inertia term
- **Lines 48-50**: Cognitive component (personal best attraction)
- **Lines 51-52**: Social component (global best attraction)
```

---

### 1.2 Optimization Landscape Analysis

**File:** `docs/mathematical_foundations/optimization_landscape_analysis.md`
**Target:** 500 lines

**Content Structure:**

#### 1.2.1 Gain Space Geometry (150 lines)

**Controller Gain Bounds (Classical SMC):**
```
Stability Requirements:
  k₁, k₂, λ₁, λ₂ > 0  (positive surface gains)
  K > ||d||∞          (switching gain > disturbance bound)
  k_d ≥ 0             (damping gain)

Bounded Search Space:
  Ω = {g ∈ ℝ⁶ | g_min ≤ g ≤ g_max}
  where g = [k₁, k₂, λ₁, λ₂, K, k_d]

Typical Bounds:
  k₁, k₂, λ₁, λ₂ ∈ [0.1, 50.0]
  K ∈ [1.0, 200.0]
  k_d ∈ [0.0, 50.0]
```

#### 1.2.2 Multi-Objective Formulation (150 lines)

**Fitness Function Design:**
```python
J(g) = w₁·ISE(g) + w₂·chattering(g) + w₃·control_effort(g)

where:
  ISE(g) = ∫₀ᵀ ||x(t;g)||² dt
  chattering(g) = ∫₀ᵀ |u̇(t;g)| dt
  control_effort(g) = ∫₀ᵀ u²(t;g) dt
```

**Pareto Optimization:**
- Minimize ISE (performance)
- Minimize chattering (smoothness)
- Minimize control effort (energy)
- Trade-off frontier visualization

#### 1.2.3 Landscape Characteristics (150 lines)
- **Multimodality:** Multiple local minima
- **Ruggedness:** Chattering creates rough landscape
- **Deceptiveness:** Good performance ≠ good generalization
- **Constraint violations:** Unstable regions in gain space

#### 1.2.4 Convergence Diagnostics (50 lines)
- Fitness stagnation detection
- Diversity metrics (swarm spread)
- Premature convergence indicators
- Escape strategies for local minima

---

### 1.3 Numerical Integration Theory

**File:** `docs/mathematical_foundations/numerical_integration_theory.md`
**Target:** 600 lines

**Content Structure:**

#### 1.3.1 Integration Method Fundamentals (150 lines)

**Explicit Euler (1st Order):**
```
x_{n+1} = x_n + h·f(t_n, x_n)

Local Error: O(h²)
Global Error: O(h)
Stability: Conditionally stable
```

**Runge-Kutta 4th Order (RK4):**
```
k₁ = f(t_n, x_n)
k₂ = f(t_n + h/2, x_n + h·k₁/2)
k₃ = f(t_n + h/2, x_n + h·k₂/2)
k₄ = f(t_n + h, x_n + h·k₃)

x_{n+1} = x_n + (h/6)·(k₁ + 2k₂ + 2k₃ + k₄)

Local Error: O(h⁵)
Global Error: O(h⁴)
```

**Adaptive RK45 (Dormand-Prince):**
```
Embedded 4th/5th order pair
Error estimate: e_n = ||x₅ - x₄||
Step size control: h_{n+1} = h_n·(tol/e_n)^(1/5)
```

#### 1.3.2 Stability Analysis (200 lines)

**Linear Stability:**
```
Test equation: ẋ = λx, λ < 0

Stability Region:
  Euler: |1 + hλ| < 1  ⟹  h < 2/|λ|
  RK4:   |R₄(hλ)| < 1  (larger region)

where R₄(z) = 1 + z + z²/2 + z³/6 + z⁴/24
```

**Stiffness and Chattering:**
- Sliding mode creates stiff system (fast switching)
- Explicit methods require tiny timesteps
- Adaptive methods adjust automatically

#### 1.3.3 Energy Conservation (150 lines)

**Hamiltonian Systems:**
```
H(q,p) = T(q̇) + V(q) = constant (for conservative systems)

DIP Hamiltonian:
H = ½(I₁θ̇₁² + I₂θ̇₂² + mẋ²) + mg(L₁cosθ₁ + L₂cosθ₂)
```

**Symplectic Integrators:**
- Preserve phase space volume
- Long-term energy stability
- Importance for benchmark validation

#### 1.3.4 Accuracy Metrics (100 lines)

**Convergence Order Estimation:**
```python
# example-metadata:
# runnable: false

# Richardson extrapolation
def estimate_convergence_order(method, x0, t_span, dt_values):
    errors = []
    for dt in dt_values:
        x_h = method.integrate(x0, t_span, dt)
        x_ref = method.integrate(x0, t_span, dt/10)  # Fine reference
        errors.append(norm(x_h[-1] - x_ref[-1]))

    # Fit log(error) vs log(dt)
    order = polyfit(log(dt_values), log(errors), 1)[0]
    return order
```

---

### 1.4 Dynamics Derivations

**File:** `docs/mathematical_foundations/dynamics_derivations.md`
**Target:** 700 lines

**Content Structure:**

#### 1.4.1 Lagrangian Mechanics (250 lines)

**Generalized Coordinates:**
```
q = [θ₁, θ₂, x]ᵀ
q̇ = [θ̇₁, θ̇₂, ẋ]ᵀ
```

**Kinetic Energy:**
```
T = ½m₁v₁² + ½m₂v₂² + ½mᵥvᵥ²

where:
  v₁ = (ẋ + L₁θ̇₁cosθ₁)² + (L₁θ̇₁sinθ₁)²
  v₂ = (ẋ + L₁θ̇₁cosθ₁ + L₂θ̇₂cosθ₂)² + (L₁θ̇₁sinθ₁ + L₂θ̇₂sinθ₂)²
  vᵥ = ẋ²
```

**Potential Energy:**
```
V = -m₁gL₁cosθ₁ - m₂g(L₁cosθ₁ + L₂cosθ₂)
```

**Lagrangian:**
```
L = T - V

Euler-Lagrange Equations:
  d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = Qᵢ

where Q = [0, 0, u]ᵀ (generalized forces)
```

#### 1.4.2 Equations of Motion (250 lines)

**Full Nonlinear Dynamics:**
```
M(q)q̈ + C(q,q̇)q̇ + G(q) = B·u

Mass Matrix M(q) ∈ ℝ³ˣ³:
  M₁₁ = I₁ + m₁L₁² + m₂(L₁² + L₂² + 2L₁L₂cosθ₂)
  M₁₂ = m₂(L₂² + L₁L₂cosθ₂)
  M₁₃ = (m₁ + m₂)L₁cosθ₁ + m₂L₂cosθ₂
  ...

Coriolis Matrix C(q,q̇) ∈ ℝ³ˣ³:
  C₁₂ = -m₂L₁L₂sinθ₂·θ̇₂
  C₂₁ = m₂L₁L₂sinθ₂·θ̇₁
  ...

Gravity Vector G(q) ∈ ℝ³:
  G₁ = -(m₁ + m₂)gL₁sinθ₁ - m₂gL₂sinθ₂
  G₂ = -m₂gL₂sinθ₂
  G₃ = 0
```

#### 1.4.3 Simplified vs Full Dynamics (150 lines)

**Comparison Table:**

| Feature | Simplified | Full Nonlinear |
|---------|-----------|----------------|
| State dimension | 6 | 6 |
| Nonlinear terms | Linearized | Full trigonometry |
| Coupling | Weak | Strong θ₂ coupling |
| Computational cost | O(n) | O(n²) |
| Accuracy (small angles) | 95% | 100% |
| Accuracy (large angles) | 60% | 100% |

**When to Use:**
- **Simplified:** PSO optimization (fast fitness evaluation)
- **Full:** Final validation, research publication

#### 1.4.4 State-Space Representation (50 lines)

**First-Order Form:**
```
ẋ = f(x,u)

where x = [θ₁, θ₂, x, θ̇₁, θ̇₂, ẋ]ᵀ ∈ ℝ⁶

f(x,u) = [θ̇₁, θ̇₂, ẋ, M⁻¹(q)·(B·u - C(q,q̇)q̇ - G(q))]ᵀ
```

---

## Phase 2: PSO Optimization Module (Days 3-5)

**Duration:** 3 days | **Effort:** 10-12 hours
**Target:** 3,500 lines of implementation documentation

### 2.1 PSO Core Algorithm Guide

**File:** `docs/optimization/pso_core_algorithm_guide.md`
**Target:** 900 lines

**Content Structure:**

#### 2.1.1 Algorithm Overview (100 lines)
- High-level workflow diagram
- Input/output specifications
- Integration with controller factory
- Typical optimization timeline

#### 2.1.2 Architecture (150 lines)

**Class Hierarchy:**
```python
BaseOptimizer (ABC)
  ├── SwarmOptimizer (ABC)
  │   ├── PSOCore
  │   ├── AdaptivePSO
  │   └── MultiObjectivePSO
  ├── EvolutionaryOptimizer (ABC)
  │   ├── GeneticAlgorithm
  │   └── DifferentialEvolution
  └── BayesianOptimizer
```

**Component Diagram:**
```mermaid
graph LR
    A[PSOCore] --> B[ParticleSwarm]
    A --> C[VelocityUpdater]
    A --> D[PositionUpdater]
    B --> E[FitnessEvaluator]
    E --> F[ControllerFactory]
    E --> G[SimulationRunner]
```

#### 2.1.3 Full Source Code (300 lines)

```markdown
### PSO Core Implementation

\`\`\`{literalinclude} ../../../src/optimization/algorithms/swarm/pso_core.py
:language: python
:linenos:
:emphasize-lines: 87-95, 120-135
\`\`\`

#### Key Algorithm Steps

**Lines 87-95: Velocity Update**
```python
# Inertia term
velocity = self.inertia * velocity

# Cognitive component (personal best attraction)
cognitive = self.c1 * rand(0,1) * (pbest - position)
velocity += cognitive

# Social component (global best attraction)
social = self.c2 * rand(0,1) * (gbest - position)
velocity += social
```

**Mathematical interpretation:**
- Inertia: Maintains exploration momentum
- Cognitive: Learn from personal experience
- Social: Learn from swarm's best discovery

**Lines 120-135: Fitness Evaluation**
```python
# example-metadata:
# runnable: false

def evaluate_fitness(self, gains):
    # Create controller from gains
    controller = self.factory.create(gains)

    # Run simulation
    result = self.simulator.run(controller)

    # Compute multi-objective fitness
    fitness = (
        self.w1 * result.ise +
        self.w2 * result.chattering_index +
        self.w3 * result.control_effort
    )

    return fitness
```
\`\`\`

#### 2.1.4 Parameter Configuration (150 lines)

**YAML Configuration:**
```yaml
pso:
  n_particles: 30           # Swarm size
  max_iters: 100            # Maximum iterations
  inertia: 0.7298           # Constriction coefficient
  c1: 1.49618               # Cognitive coefficient
  c2: 1.49618               # Social coefficient
  bounds:
    classical_smc:
      - [0.1, 50.0]         # k1 bounds
      - [0.1, 50.0]         # k2 bounds
      - [0.1, 50.0]         # λ1 bounds
      - [0.1, 50.0]         # λ2 bounds
      - [1.0, 200.0]        # K bounds
      - [0.0, 50.0]         # kd bounds
```

**Parameter Tuning Guidelines:**
- **Swarm size:** 20-50 particles (larger for complex landscapes)
- **Iterations:** 50-200 (diminishing returns after 150)
- **Inertia:** 0.4-0.9 (adaptive recommended)
- **c1, c2:** Sum ~4.0 (standard: 2.05 each)

#### 2.1.5 Usage Examples (100 lines)

**Basic PSO Optimization:**
```python
from src.optimization.algorithms.swarm import PSOCore
from src.controllers.factory import SMCFactory

# Define bounds
bounds = [
    (0.1, 50.0),  # k1
    (0.1, 50.0),  # k2
    (0.1, 50.0),  # λ1
    (0.1, 50.0),  # λ2
    (1.0, 200.0), # K
    (0.0, 50.0),  # kd
]

# Create optimizer
optimizer = PSOCore(
    factory=SMCFactory,
    bounds=bounds,
    n_particles=30,
    max_iters=100
)

# Run optimization
result = optimizer.optimize()

print(f"Best gains: {result.best_position}")
print(f"Best fitness: {result.best_fitness}")
print(f"Convergence iteration: {result.convergence_iter}")
```

#### 2.1.6 Performance Analysis (100 lines)

**Computational Complexity:**
- **Per iteration:** O(N·M·S)
  - N: Swarm size
  - M: Simulation timesteps
  - S: State dimension

**Typical Runtime:**
- Classical SMC (6 gains, 100 iters, 30 particles): 15-20 minutes
- Adaptive SMC (5 gains): 12-15 minutes
- Super-Twisting SMC (6 gains): 18-25 minutes

**Optimization Tips:**
1. Use simplified dynamics for PSO fitness
2. Validate final gains with full dynamics
3. Parallel fitness evaluation (multiprocessing)
4. Early stopping if convergence detected

---

### 2.2 Advanced Optimization Algorithms

**File:** `docs/optimization/advanced_algorithms_guide.md`
**Target:** 700 lines

**Coverage:**

#### 2.2.1 Genetic Algorithms (200 lines)
- Selection methods (tournament, roulette)
- Crossover operators (single-point, uniform)
- Mutation strategies
- Elitism and diversity preservation

**Code Embedding:**
```markdown
\`\`\`{literalinclude} ../../../src/optimization/algorithms/evolutionary/genetic.py
:language: python
:pyobject: GeneticAlgorithm
:linenos:
\`\`\`
```

#### 2.2.2 Differential Evolution (200 lines)
- Mutation strategy: DE/rand/1/bin
- Scaling factor F and crossover rate CR
- Convergence characteristics
- Comparison with PSO

#### 2.2.3 Bayesian Optimization (250 lines)
- Gaussian Process surrogate models
- Acquisition functions (EI, UCB, PI)
- Sequential design strategies
- Sample efficiency vs PSO

#### 2.2.4 Algorithm Comparison (50 lines)

**Performance Benchmarks:**

| Algorithm | Convergence Speed | Sample Efficiency | Robustness |
|-----------|-------------------|-------------------|------------|
| PSO | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Genetic Algorithm | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ |
| Differential Evolution | ★★★★☆ | ★★★☆☆ | ★★★★★ |
| Bayesian Optimization | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |

**Recommendations:**
- **PSO:** Default choice for SMC gain tuning
- **Differential Evolution:** When PSO stagnates
- **Genetic Algorithm:** Multi-modal landscapes
- **Bayesian:** Expensive simulations (HIL)

---

### 2.3 Fitness Function Design

**File:** `docs/optimization/fitness_function_design_guide.md`
**Target:** 800 lines

**Content Structure:**

#### 2.3.1 Control-Specific Objectives (250 lines)

**Tracking Performance:**
```python
def compute_ise(states):
    """Integral of Squared Error."""
    return np.trapz(states**2, dx=dt)

def compute_itae(time, states):
    """Integral of Time-weighted Absolute Error."""
    return np.trapz(time * np.abs(states), dx=dt)
```

**Chattering Quantification:**
```python
def compute_chattering_index(control_signal, dt):
    """Total variation of control signal."""
    control_derivative = np.diff(control_signal) / dt
    return np.sum(np.abs(control_derivative)) * dt
```

**Control Effort:**
```python
def compute_control_effort(control_signal, dt):
    """L2 norm of control signal."""
    return np.trapz(control_signal**2, dx=dt)
```

#### 2.3.2 Multi-Objective Formulation (200 lines)

**Weighted Sum Approach:**
```python
# example-metadata:
# runnable: false

class MultiObjectiveFitness:
    def __init__(self, weights):
        self.w_ise = weights['ise']
        self.w_chattering = weights['chattering']
        self.w_effort = weights['effort']
        self.w_violations = weights['violations']

    def evaluate(self, simulation_result):
        J = (
            self.w_ise * simulation_result.ise +
            self.w_chattering * simulation_result.chattering_index +
            self.w_effort * simulation_result.control_effort +
            self.w_violations * simulation_result.constraint_violations
        )
        return J
```

**Pareto Optimization:**
```python
def pareto_front(objectives):
    """Compute non-dominated solutions."""
    is_pareto = np.ones(len(objectives), dtype=bool)
    for i, obj_i in enumerate(objectives):
        for j, obj_j in enumerate(objectives):
            if i != j and dominates(obj_j, obj_i):
                is_pareto[i] = False
                break
    return objectives[is_pareto]
```

#### 2.3.3 Constraint Handling (150 lines)

**Penalty Methods:**
```python
# example-metadata:
# runnable: false

def penalized_fitness(gains, base_fitness):
    """Add penalty for constraint violations."""
    penalty = 0.0

    # Stability constraint: positive gains
    if any(g <= 0 for g in gains[:5]):
        penalty += 1e6

    # Switching gain constraint: K > disturbance
    if gains[4] < 10.0:  # Minimum K
        penalty += 1e4 * (10.0 - gains[4])

    return base_fitness + penalty
```

#### 2.3.4 Fitness Landscape Visualization (100 lines)

**2D Slices:**
```python
# example-metadata:
# runnable: false

def plot_fitness_landscape(optimizer, fixed_gains, vary_indices):
    """Visualize fitness function in 2D slice."""
    k1_range = np.linspace(0.1, 50, 50)
    k2_range = np.linspace(0.1, 50, 50)

    fitness_grid = np.zeros((len(k1_range), len(k2_range)))

    for i, k1 in enumerate(k1_range):
        for j, k2 in enumerate(k2_range):
            gains = fixed_gains.copy()
            gains[vary_indices[0]] = k1
            gains[vary_indices[1]] = k2
            fitness_grid[i, j] = optimizer.evaluate_fitness(gains)

    plt.contourf(k1_range, k2_range, fitness_grid)
    plt.xlabel(f'Gain {vary_indices[0]}')
    plt.ylabel(f'Gain {vary_indices[1]}')
    plt.colorbar(label='Fitness')
```

#### 2.3.5 Design Guidelines (100 lines)

**Best Practices:**
1. **Normalize objectives** to same scale
2. **Weight selection:** Start with equal weights, iterate
3. **Constraint violations:** Use large penalties
4. **Simulation length:** 5-10 seconds typical
5. **Initial conditions:** Test multiple scenarios

---

### 2.4 Constraint Handling Methods

**File:** `docs/optimization/constraint_handling_guide.md`
**Target:** 600 lines

**Coverage:**
- Simple bounds (box constraints)
- Penalty methods (static, dynamic, adaptive)
- Barrier functions (logarithmic, inverse)
- Projection methods (feasibility repair)
- Constraint satisfaction in PSO

**Code Examples:** Embed constraint handling implementations

---

### 2.5 Controller-Optimizer Integration

**File:** `docs/optimization/controller_integration_patterns.md`
**Target:** 500 lines

**Content:**

#### 2.5.1 Factory Adapter Pattern (150 lines)
- Unified interface for all controller types
- Gain vector to configuration mapping
- Type-safe controller creation

#### 2.5.2 Simulation Bridge (150 lines)
- Optimization loop integration
- Batch simulation for fitness evaluation
- Result caching and memoization

#### 2.5.3 Workflows (200 lines)

**End-to-End Optimization:**
```python
# example-metadata:
# runnable: false

# 1. Define optimization problem
problem = OptimizationProblem(
    controller_type='classical_smc',
    bounds=[(0.1, 50)] * 6,
    objectives=['ise', 'chattering', 'effort'],
    weights=[0.5, 0.3, 0.2]
)

# 2. Create optimizer
optimizer = PSOCore(
    problem=problem,
    n_particles=30,
    max_iters=100
)

# 3. Run optimization
result = optimizer.optimize()

# 4. Validate with full dynamics
final_controller = create_controller(
    'classical_smc',
    gains=result.best_position,
    dynamics_model='full'
)

validation_result = simulate(final_controller, duration=10.0)

# 5. Save optimized gains
save_gains(result.best_position, 'optimized_classical_smc.json')
```

---

## Phase 3: Simulation & Dynamics (Days 6-8)

**Duration:** 3 days | **Effort:** 10-12 hours
**Target:** 3,000 lines of simulation documentation

### 3.1 Simulation Engine Architecture

**File:** `docs/simulation/simulation_engine_guide.md`
**Target:** 800 lines

**Content Structure:**

#### 3.1.1 Component Overview (150 lines)

**Architecture Diagram:**
```mermaid
graph TB
    A[SimulationRunner] --> B[SimulationContext]
    A --> C[DynamicsModel]
    A --> D[Controller]
    B --> E[StateHistory]
    B --> F[PerformanceMetrics]
    C --> G[SimplifiedDynamics]
    C --> H[FullDynamics]
    I[VectorSim] --> A
```

#### 3.1.2 SimulationRunner (300 lines)

**Full Source Code:**
```markdown
\`\`\`{literalinclude} ../../../src/core/simulation_runner.py
:language: python
:linenos:
\`\`\`

**Key Components:**

**Main Simulation Loop (lines 120-180):**
```python
# example-metadata:
# runnable: false

def run(self, controller, dynamics, duration, dt):
    # Initialize state
    x = self.initial_state
    t = 0.0
    history = {'t': [], 'x': [], 'u': []}

    while t < duration:
        # Compute control
        u = controller.compute_control(x, history)

        # Integrate dynamics
        x_next = self.integrator.step(x, u, dynamics, dt)

        # Safety checks
        if self.check_divergence(x_next):
            raise SimulationDivergenceError()

        # Record history
        history['t'].append(t)
        history['x'].append(x)
        history['u'].append(u)

        # Update state
        x = x_next
        t += dt

    return SimulationResult(history)
```

**Performance Metrics:**
- Simulation speed: 1000x real-time typical
- Memory usage: O(T/dt) for history
- Numerical stability: Adaptive timestep recommended
\`\`\`

#### 3.1.3 SimulationContext (200 lines)

**Unified State Management:**
```python
# example-metadata:
# runnable: false

class SimulationContext:
    """Centralized simulation state and configuration."""

    state: np.ndarray           # Current state [6,]
    time: float                 # Current time
    controller_vars: Dict       # Controller internal state
    dynamics_params: Dict       # Physics parameters
    history: StateHistory       # Trajectory recording

    def update(self, x_next, u, dt):
        """Thread-safe state update."""
        with self._lock:
            self.state = x_next
            self.time += dt
            self.history.append(self.state, u)
```

#### 3.1.4 Integration Patterns (150 lines)

**Standard Workflow:**
```python
# example-metadata:
# runnable: false

# 1. Configure simulation
config = SimulationConfig(
    duration=5.0,
    dt=0.01,
    integrator='rk4',
    initial_state=np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
)

# 2. Create components
dynamics = FullNonlinearDynamics(physics_params)
controller = create_controller('classical_smc', gains=[...])

# 3. Run simulation
runner = SimulationRunner(config)
result = runner.run(controller, dynamics)

# 4. Analyze results
print(f"ISE: {result.ise}")
print(f"Settling time: {result.settling_time}")
```

---

### 3.2 Dynamics Models

**File:** `docs/simulation/dynamics_models_guide.md`
**Target:** 900 lines

**Content Structure:**

#### 3.2.1 Simplified Dynamics (300 lines)

**Full Source Code:**
```markdown
\`\`\`{literalinclude} ../../../src/core/dynamics.py
:language: python
:linenos:
:emphasize-lines: 45-60
\`\`\`

**Mathematical Foundation:**

Linearized around equilibrium (θ₁ = θ₂ = 0):

```python
def compute_derivative(self, x, u):
    """Simplified linearized dynamics."""
    θ1, θ2, x_pos, ω1, ω2, v = x

    # Linearized equations (small angle approximation)
    ω1_dot = (g/L1) * θ1 + (u/I1) * x_pos
    ω2_dot = (g/L2) * θ2 + coupling_term
    v_dot = u / m_total

    return np.array([ω1, ω2, v, ω1_dot, ω2_dot, v_dot])
```

**Validity Range:**
- Small angles: |θ₁|, |θ₂| < 15° (0.26 rad)
- Accuracy: 95% within validity range
- Computational cost: 50% of full dynamics
\`\`\`

#### 3.2.2 Full Nonlinear Dynamics (400 lines)

**Complete Implementation:**
```markdown
\`\`\`{literalinclude} ../../../src/core/dynamics_full.py
:language: python
:linenos:
\`\`\`

**Line-by-Line Explanation:**

**Mass Matrix Computation (lines 67-95):**
```python
# example-metadata:
# runnable: false

def compute_mass_matrix(self, q):
    """
    M(q) ∈ ℝ³ˣ³ - Configuration-dependent mass matrix

    Derivation from kinetic energy:
    T = ½q̇ᵀM(q)q̇
    """
    θ1, θ2, x = q

    m1, m2, L1, L2 = self.params

    # Diagonal terms
    M11 = self.I1 + m1*L1**2 + m2*(L1**2 + L2**2 + 2*L1*L2*np.cos(θ2))
    M22 = self.I2 + m2*L2**2
    M33 = self.m_total

    # Off-diagonal coupling terms
    M12 = m2*(L2**2 + L1*L2*np.cos(θ2))
    M13 = (m1 + m2)*L1*np.cos(θ1) + m2*L2*np.cos(θ2)
    M23 = m2*L2*np.cos(θ2)

    M = np.array([
        [M11, M12, M13],
        [M12, M22, M23],
        [M13, M23, M33]
    ])

    return M
```

**Coriolis/Centrifugal Terms (lines 97-120):**
```python
# example-metadata:
# runnable: false

def compute_coriolis(self, q, qdot):
    """
    C(q,q̇)q̇ - Velocity-dependent forces

    Christoffel symbols of second kind:
    Cᵢⱼₖ = ½(∂Mᵢⱼ/∂qₖ + ∂Mᵢₖ/∂qⱼ - ∂Mⱼₖ/∂qᵢ)
    """
    θ1, θ2, x = q
    ω1, ω2, v = qdot

    # Centrifugal force from θ2 rotation
    C12 = -m2*L1*L2*np.sin(θ2)*ω2
    C21 = m2*L1*L2*np.sin(θ2)*ω1

    # Coupling terms
    C13 = -(m1 + m2)*L1*np.sin(θ1)*ω1 - m2*L2*np.sin(θ2)*ω2

    C = np.array([
        [0, C12, C13],
        [C21, 0, 0],
        [0, 0, 0]
    ])

    return C @ qdot
```

**Gravity Vector (lines 122-135):**
```python
# example-metadata:
# runnable: false

def compute_gravity(self, q):
    """
    G(q) - Potential energy gradient

    V = -m₁gL₁cosθ₁ - m₂g(L₁cosθ₁ + L₂cosθ₂)
    Gᵢ = ∂V/∂qᵢ
    """
    θ1, θ2, x = q

    G1 = -(m1 + m2)*g*L1*np.sin(θ1) - m2*g*L2*np.sin(θ2)
    G2 = -m2*g*L2*np.sin(θ2)
    G3 = 0.0

    return np.array([G1, G2, G3])
```
\`\`\`

#### 3.2.3 Model Comparison (150 lines)

**Accuracy Benchmark:**

| Angle | Simplified Error | Full Dynamics | Relative Error |
|-------|------------------|---------------|----------------|
| 5° | 0.01% | Reference | - |
| 10° | 0.5% | Reference | - |
| 15° | 2.0% | Reference | - |
| 30° | 12.0% | Reference | - |
| 45° | 35.0% | Reference | - |

**Recommendation:**
- **Simplified:** PSO fitness evaluation (speed critical)
- **Full:** Final validation, research publication

#### 3.2.4 Low-Rank Approximations (50 lines)
- Reduced-order models
- Computational efficiency
- Accuracy trade-offs

---

### 3.3 Numerical Integration Methods

**File:** `docs/simulation/numerical_integration_guide.md`
**Target:** 700 lines

**Content Structure:**

#### 3.3.1 Method Implementations (300 lines)

**Euler Method:**
```markdown
\`\`\`{literalinclude} ../../../src/simulation/integration/euler.py
:language: python
:linenos:
\`\`\`

**RK4 Method:**
\`\`\`{literalinclude} ../../../src/simulation/integration/rk4.py
:language: python
:linenos:
\`\`\`

**Adaptive RK45:**
\`\`\`{literalinclude} ../../../src/simulation/integration/rk45.py
:language: python
:linenos:
\`\`\`
```

#### 3.3.2 Accuracy Comparison (200 lines)

**Convergence Test Results:**
```python
Method    | dt=0.01 | dt=0.005 | dt=0.001 | Order
----------|---------|----------|----------|-------
Euler     | 1e-3    | 5e-4     | 1e-4     | 1.0
RK4       | 1e-7    | 6e-9     | 1e-11    | 4.0
RK45      | 1e-9    | 1e-11    | 1e-13    | 5.0
```

**Computational Cost:**
```python
Method    | Function Evals | Relative Cost
----------|----------------|---------------
Euler     | 1 per step     | 1x
RK4       | 4 per step     | 4x
RK45      | 6 per step (avg)| 6x (adaptive)
```

#### 3.3.3 Stability Regions (150 lines)

**Visual Comparison:**
- Stability region plots in complex plane
- Stiffness handling capabilities
- Chattering impact on stability

#### 3.3.4 Method Selection Guide (50 lines)

**Decision Matrix:**

| Use Case | Recommended Method | Reason |
|----------|-------------------|---------|
| PSO fitness | Euler (dt=0.01) | Speed |
| Development | RK4 (dt=0.01) | Balance |
| Production | RK45 (tol=1e-6) | Accuracy |
| Research | RK45 (tol=1e-9) | Precision |

---

### 3.4 Batch Simulation (Numba Vectorization)

**File:** `docs/simulation/batch_simulation_guide.md`
**Target:** 600 lines

**Content Structure:**

#### 3.4.1 Vectorization Principles (150 lines)
- NumPy broadcasting
- Numba JIT compilation
- Memory layout optimization

#### 3.4.2 Batch Simulator Implementation (300 lines)

**Full Source Code:**
```markdown
\`\`\`{literalinclude} ../../../src/core/vector_sim.py
:language: python
:linenos:
:emphasize-lines: 78-95
\`\`\`

**Key Optimization (lines 78-95):**
```python
# example-metadata:
# runnable: false

@numba.jit(nopython=True, parallel=True)
def batch_integrate(x0_batch, gains_batch, duration, dt):
    """
    Vectorized simulation for PSO fitness evaluation.

    Args:
        x0_batch: Initial states (B, 6)
        gains_batch: Controller gains (B, N_gains)
        duration: Simulation time
        dt: Timestep

    Returns:
        metrics_batch: Performance metrics (B, N_metrics)
    """
    B = x0_batch.shape[0]
    N = int(duration / dt)
    metrics = np.zeros((B, 3))  # ISE, chattering, effort

    for b in numba.prange(B):  # Parallel loop
        x = x0_batch[b]
        ise = 0.0
        chattering = 0.0
        effort = 0.0

        for i in range(N):
            u = compute_control_vectorized(x, gains_batch[b])
            x_next = rk4_step_vectorized(x, u, dt)

            ise += np.sum(x**2) * dt
            if i > 0:
                chattering += np.abs(u - u_prev)
            effort += u**2 * dt

            x = x_next
            u_prev = u

        metrics[b] = [ise, chattering, effort]

    return metrics
```

**Performance Gain:**
- Serial: 30 particles × 100 iters × 0.5s = 25 minutes
- Vectorized: 100 iters × 0.05s = 5 minutes (5x speedup)
\`\`\`

#### 3.4.3 Usage Examples (100 lines)

**PSO Integration:**
```python
from src.core.vector_sim import batch_simulate

# Generate initial conditions
x0_batch = np.random.randn(30, 6) * 0.1

# Swarm positions (gains)
gains_batch = swarm.positions  # (30, 6)

# Batch fitness evaluation
metrics_batch = batch_simulate(x0_batch, gains_batch, 5.0, 0.01)

# Extract fitness values
fitness = np.sum(metrics_batch * weights, axis=1)
```

#### 3.4.4 Performance Profiling (50 lines)
- Numba compilation overhead
- Parallel scaling (CPU cores)
- Memory bandwidth limits

---

## Phase 4: Tutorials & Examples (Days 9-10)

**Duration:** 2 days | **Effort:** 8-10 hours
**Target:** 9+ tutorials, 30+ code examples

### 4.1 PSO Optimization Tutorials

**Location:** `docs/tutorials/optimization/`

#### Tutorial 1: Basic PSO Optimization (300 lines)
**File:** `basic_pso_workflow.md`

**Content:**
1. Setup: Install dependencies, configure environment
2. Define optimization problem: Controller type, bounds
3. Run PSO: Execute optimization, monitor progress
4. Analyze results: Convergence plots, gain validation
5. Deploy gains: Save and test optimized controller

**Working Example:**
```python
# example-metadata:
# runnable: false

# Complete runnable script
from src.optimization import PSOCore
from src.controllers.factory import create_controller

# ... (full implementation)

if __name__ == '__main__':
    main()
```

#### Tutorial 2: Multi-Objective PSO (350 lines)
**File:** `multi_objective_optimization.md`

**Content:**
- Pareto front visualization
- Weight selection strategies
- Trade-off analysis
- Decision-making from Pareto solutions

#### Tutorial 3: Custom Fitness Functions (300 lines)
**File:** `custom_fitness_design.md`

**Content:**
- Defining new objectives
- Constraint handling
- Normalization techniques
- Integration with PSO framework

#### Tutorial 4: Adaptive PSO Parameters (250 lines)
**File:** `adaptive_pso_tuning.md`

**Content:**
- Time-varying inertia
- Self-adaptive parameters
- Diversity-based adaptation
- Convergence acceleration

#### Tutorial 5: Optimization Debugging (300 lines)
**File:** `optimization_troubleshooting.md`

**Content:**
- Premature convergence diagnosis
- Fitness landscape exploration
- Parameter sensitivity analysis
- Common pitfalls and solutions

---

### 4.2 Simulation Workflow Tutorials

**Location:** `docs/tutorials/simulation/`

#### Tutorial 6: Custom Dynamics Models (350 lines)
**File:** `custom_dynamics_implementation.md`

**Content:**
- Defining new dynamics equations
- Integration with simulation framework
- Validation against physical models
- Performance optimization

#### Tutorial 7: Integration Method Selection (300 lines)
**File:** `integration_method_guide.md`

**Content:**
- Accuracy vs speed trade-offs
- Stiffness detection
- Adaptive timestep strategies
- Benchmarking integration methods

#### Tutorial 8: Batch Simulation (300 lines)
**File:** `batch_simulation_workflows.md`

**Content:**
- Vectorized computation patterns
- Numba optimization techniques
- Memory management
- Scaling to large parameter sweeps

#### Tutorial 9: Performance Profiling (250 lines)
**File:** `simulation_performance_optimization.md`

**Content:**
- Profiling tools (cProfile, line_profiler)
- Bottleneck identification
- Numba vs NumPy performance
- Hardware acceleration (GPU considerations)

---

### 4.3 Code Examples Library

**Location:** `docs/examples/optimization/` and `docs/examples/simulation/`

**30+ Standalone Scripts:**

**Optimization Examples (15 scripts):**
1. `basic_pso.py` - Minimal PSO example (50 lines)
2. `pso_with_logging.py` - Progress tracking (75 lines)
3. `multi_objective_pso.py` - Pareto optimization (100 lines)
4. `adaptive_pso.py` - Time-varying parameters (80 lines)
5. `genetic_algorithm.py` - GA implementation (90 lines)
6. `differential_evolution.py` - DE example (85 lines)
7. `bayesian_optimization.py` - BO workflow (120 lines)
8. `custom_fitness.py` - Custom objective (60 lines)
9. `constraint_handling.py` - Penalty methods (70 lines)
10. `parallel_pso.py` - Multiprocessing (95 lines)
11. `convergence_analysis.py` - Diagnostics (110 lines)
12. `landscape_visualization.py` - Fitness plots (130 lines)
13. `benchmark_comparison.py` - Algorithm comparison (140 lines)
14. `sensitivity_analysis.py` - Parameter tuning (100 lines)
15. `production_workflow.py` - End-to-end pipeline (150 lines)

**Simulation Examples (15 scripts):**
1. `basic_simulation.py` - Minimal example (40 lines)
2. `custom_initial_conditions.py` - IC exploration (60 lines)
3. `trajectory_visualization.py` - Plotting results (80 lines)
4. `energy_conservation.py` - Hamiltonian validation (90 lines)
5. `integration_comparison.py` - Method benchmarking (110 lines)
6. `adaptive_timestep.py` - RK45 usage (75 lines)
7. `batch_simulation.py` - Vectorized example (100 lines)
8. `monte_carlo_simulation.py` - Statistical analysis (120 lines)
9. `parameter_sweep.py` - Grid search (95 lines)
10. `sensitivity_analysis.py` - Jacobian computation (105 lines)
11. `stability_analysis.py` - Eigenvalue tracking (115 lines)
12. `phase_portraits.py` - State space visualization (130 lines)
13. `lyapunov_exponents.py` - Chaos analysis (140 lines)
14. `frequency_response.py` - Bode plots (125 lines)
15. `performance_profiling.py` - Speed benchmarking (85 lines)

**All Examples Include:**
- Complete, runnable code
- Inline comments explaining key steps
- Expected output descriptions
- Visualization of results

---

## Phase 5: Sphinx Integration & QA (Day 11)

**Duration:** 1 day | **Effort:** 4-5 hours
**Target:** Complete integration and validation

### 5.1 Module Index Pages

#### Optimization Index

**File:** `docs/optimization/index.md`
**Target:** 200 lines

**Content:**
```markdown
# Optimization Module Documentation

## Overview

Comprehensive optimization framework for automated controller tuning...

## Table of Contents

\`\`\`{toctree}
:maxdepth: 2

pso_core_algorithm_guide
advanced_algorithms_guide
fitness_function_design_guide
constraint_handling_guide
controller_integration_patterns
\`\`\`

## Mathematical Foundations

- [PSO Algorithm Theory](../../mathematical_foundations/pso_algorithm_theory.md)
- [Optimization Landscape Analysis](../../mathematical_foundations/pso_algorithm_theory.md#optimization-landscape) (see PSO theory sections)

## Tutorials

\`\`\`{toctree}
:maxdepth: 1

../tutorials/optimization/basic_pso_workflow
../tutorials/optimization/multi_objective_optimization
../tutorials/optimization/custom_fitness_design
../tutorials/optimization/adaptive_pso_tuning
../tutorials/optimization/optimization_troubleshooting
\`\`\`

## Code Examples

See code examples in:
- `src/optimization/algorithms/swarm/pso.py` - Core PSO implementation
- `tests/test_optimizer/test_pso_optimizer.py` - PSO usage examples
- [PSO Optimization Workflow Guide](../../guides/workflows/pso-optimization-workflow.md) - Complete examples

## API Reference

\`\`\`{toctree}
:maxdepth: 2

api/algorithms
api/objectives
api/constraints
api/integration
\`\`\`
```

#### Simulation Index

**File:** `docs/simulation/index.md`
**Target:** 180 lines

**Structure:** (similar to optimization index)

---

### 5.2 Cross-References

**Integration with Week 2 Controllers:**

**In PSO documentation:**
```markdown
See [Classical SMC Technical Guide](../../controllers/classical_smc_technical_guide.md)
for controller-specific gain tuning requirements.
```

**In Controllers documentation:**
```markdown
For automated gain tuning, see [PSO Core Algorithm Guide](../../optimization/pso_core_algorithm_guide.md).
```

**Mathematical Foundations Links:**
```markdown
The PSO convergence proof relies on Lyapunov theory, similar to
[SMC stability analysis](../../theory/smc_theory_complete.md#lyapunov-stability).
```

---

### 5.3 Main Index Update

**File:** `docs/index.md`

**Add Sections:**
```markdown
## Control Systems & Optimization

### Controllers
- {doc}`controllers/index` - SMC variants, factory, primitives

### Optimization ← NEW
- {doc}`optimization/index` - PSO, GA, DE, Bayesian optimization

### Simulation & Dynamics ← NEW
- {doc}`simulation/index` - Integration methods, batch simulation

### Mathematical Foundations
- {doc}`mathematical_foundations/index` - Theory, proofs, derivations
```

---

### 5.4 Quality Assurance Checklist

**Documentation Quality:**
- [ ] All documents use consistent formatting
- [ ] Mathematical notation follows standards
- [ ] Code examples are syntactically correct
- [ ] Cross-references use proper Sphinx directives
- [ ] Table of contents with appropriate depth

**Content Completeness:**
- [ ] All optimization algorithms documented
- [ ] Complete PSO workflow coverage
- [ ] Dynamics equations fully derived
- [ ] Numerical methods compared
- [ ] Tutorials cover beginner to advanced

**Sphinx Integration:**
- [ ] All new files in toctree directives
- [ ] Index files created for navigation
- [ ] Main index updated
- [ ] No broken internal references
- [ ] Proper MyST markdown usage

**Technical Accuracy:**
- [ ] PSO convergence proofs correct
- [ ] Dynamics derivations match literature
- [ ] Integration methods validated
- [ ] Code examples tested and working
- [ ] Performance benchmarks reproducible

**Build Validation:**
```bash
cd docs/
make clean
make html 2>&1 | tee week3_build.log

# Target: 0 warnings for Week 3 content
grep -i "warning" week3_build.log | wc -l
# Expected: 0
```

---

## Quality Standards

### Code Embedding Best Practices

#### 1. Full Source Code with Context
```markdown
## PSO Velocity Update

### Mathematical Foundation
The velocity update combines three components:
- Inertia: ω·v (momentum)
- Cognitive: c₁·r₁·(p_best - x) (personal experience)
- Social: c₂·r₂·(g_best - x) (swarm knowledge)

### Implementation

\`\`\`{literalinclude} ../../../src/optimization/algorithms/swarm/pso_core.py
:language: python
:pyobject: PSOCore.update_velocity
:linenos:
:emphasize-lines: 5-7
\`\`\`

### Line-by-Line Explanation

**Line 5:** Inertia term maintains exploration momentum
**Lines 6-7:** Cognitive component pulls toward personal best
**Lines 8-9:** Social component attracts to global best
```

#### 2. Emphasize Critical Lines
```markdown
\`\`\`{literalinclude} ../../../src/core/dynamics_full.py
:lines: 67-95
:emphasize-lines: 12-15
\`\`\`
```

#### 3. Extract Specific Functions
```markdown
\`\`\`{literalinclude} ../../../src/optimization/objectives/control/tracking_error.py
:pyobject: compute_ise
:linenos:
\`\`\`
```

---

### Mathematical Documentation Standards

#### 1. Equation Formatting
```markdown
**Discrete-Time Dynamics:**

$$
x_{k+1} = x_k + h \cdot f(x_k, u_k)
$$ (eq:euler)

Where:
- $x_k \in \mathbb{R}^6$: State vector at timestep k
- $u_k \in \mathbb{R}$: Control input
- $h$: Integration timestep
- $f(·,·)$: Dynamics function
```

#### 2. Theorem Structure
```markdown
**Theorem (PSO Convergence):**

*Under parameter conditions $\phi = c_1 + c_2 > 4$ and appropriate $\kappa$,
the PSO algorithm converges to stationary points.*

**Proof:**
1. Define Lyapunov function: $V(t) = \mathbb{E}[||x(t) - x^*||^2]$
2. Compute time derivative: $\dot{V}(t) = ...$
3. Show negativity: $\dot{V}(t) < 0$ when $\phi > 4$
4. Apply LaSalle's invariance principle
∎
```

#### 3. Algorithm Pseudocode
```markdown
**Algorithm: Particle Swarm Optimization**

\`\`\`
Input: f (fitness function), bounds, n_particles, max_iters
Output: x_best (optimal solution)

1. Initialize swarm: x_i ~ Uniform(bounds) for i = 1..n_particles
2. Evaluate fitness: f_i = f(x_i)
3. Set personal bests: p_i = x_i
4. Set global best: g = argmin(f_i)
5. For t = 1 to max_iters:
     a. Update velocities: v_i = ω·v_i + c₁·r₁·(p_i - x_i) + c₂·r₂·(g - x_i)
     b. Update positions: x_i = x_i + v_i
     c. Evaluate fitness: f_i = f(x_i)
     d. Update personal bests: if f_i < f(p_i), p_i = x_i
     e. Update global best: g = argmin(f(p_i))
6. Return g
\`\`\`
```

---

### Tutorial Writing Standards

#### 1. Learning Objectives (Start of Each Tutorial)
```markdown
## Learning Objectives

After completing this tutorial, you will be able to:

✅ Configure and run PSO optimization for SMC gain tuning
✅ Interpret convergence plots and fitness landscapes
✅ Validate optimized gains with full nonlinear dynamics
✅ Save and deploy optimized controllers in production
```

#### 2. Prerequisites
```markdown
## Prerequisites

**Required Knowledge:**
- Basic Python programming
- Understanding of SMC controllers (see [Controllers Module](../../controllers/index.md))
- Familiarity with optimization concepts

**Required Software:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**Estimated Time:** 30 minutes
```

#### 3. Step-by-Step Structure
```markdown
## Step 1: Define Optimization Problem

### Goal
Configure PSO to optimize Classical SMC gains for minimal tracking error.

### Implementation
\`\`\`python
from src.optimization import PSOCore

bounds = [
    (0.1, 50.0),  # k1 bounds
    ...
]
```

✅ **Checkpoint:** Verify bounds are valid
```

#### 4. Expected Output
```markdown
### Expected Output

\`\`\`
Iteration 1/100: Best Fitness = 45.23
Iteration 10/100: Best Fitness = 12.56
...
Iteration 100/100: Best Fitness = 2.34

Convergence achieved at iteration 87

Optimized Gains:
  k1 = 15.23
  k2 = 12.45
  λ1 = 18.67
  λ2 = 14.89
  K = 45.12
  kd = 8.34
\`\`\`
```

#### 5. Troubleshooting Section
```markdown
## Common Issues

### Premature Convergence

**Symptoms:** Fitness stagnates before reaching good values

**Solutions:**
1. Increase swarm size: 30 → 50 particles
2. Adjust inertia: Use adaptive ω(t)
3. Restart with different random seed
```

---

## Acceptance Criteria

### Phase Success Metrics

**Phase 1-2: Mathematical Theory & PSO ✅**
- [ ] 2,600 lines of mathematical foundations
- [ ] Complete PSO convergence proofs
- [ ] 3,500 lines of PSO implementation docs
- [ ] All optimization algorithms documented

**Phase 3: Simulation & Dynamics ✅**
- [ ] 3,000 lines of simulation documentation
- [ ] Full dynamics equations derived
- [ ] Integration methods compared
- [ ] Batch simulation patterns documented

**Phase 4: Tutorials & Examples ✅**
- [ ] 9 comprehensive tutorials
- [ ] 30+ working code examples
- [ ] Beginner to advanced coverage
- [ ] All examples tested

**Phase 5: Integration ✅**
- [ ] All files integrated with Sphinx
- [ ] Hierarchical navigation structure
- [ ] Cross-references to controllers module
- [ ] Build validation successful

**Overall Week 3 Targets ✅**
- [ ] ~8,000 lines of documentation
- [ ] 102 Python files documented
- [ ] 0 Sphinx build warnings
- [ ] Publication-ready quality

---

## Deliverables Summary

### Documentation Files Created

**Mathematical Foundations (4 files, 2,600 lines):**
- `pso_algorithm_theory.md` (800 lines)
- `optimization_landscape_analysis.md` (500 lines)
- `numerical_integration_theory.md` (600 lines)
- `dynamics_derivations.md` (700 lines)

**Optimization Module (5 files, 3,500 lines):**
- `pso_core_algorithm_guide.md` (900 lines)
- `advanced_algorithms_guide.md` (700 lines)
- `fitness_function_design_guide.md` (800 lines)
- `constraint_handling_guide.md` (600 lines)
- `controller_integration_patterns.md` (500 lines)

**Simulation Module (4 files, 3,000 lines):**
- `simulation_engine_guide.md` (800 lines)
- `dynamics_models_guide.md` (900 lines)
- `numerical_integration_guide.md` (700 lines)
- `batch_simulation_guide.md` (600 lines)

**Tutorials (9 files, ~2,500 lines):**
- 5 optimization tutorials (1,500 lines)
- 4 simulation tutorials (1,000 lines)

**Code Examples (30+ files, ~2,700 lines):**
- 15 optimization examples (1,400 lines)
- 15 simulation examples (1,300 lines)

**Infrastructure (2 files, 380 lines):**
- `optimization/index.md` (200 lines)
- `simulation/index.md` (180 lines)

**Total: ~14,680 lines across 54+ files**

---

## Timeline & Milestones

### Weekly Schedule

**Days 1-2 (Oct 14-15):** Mathematical Foundations
- ✅ PSO theory (800 lines)
- ✅ Landscape analysis (500 lines)
- ✅ Integration theory (600 lines)
- ✅ Dynamics derivations (700 lines)

**Days 3-5 (Oct 16-18):** PSO Optimization Module
- ✅ PSO core guide (900 lines)
- ✅ Advanced algorithms (700 lines)
- ✅ Fitness functions (800 lines)
- ✅ Constraints & integration (1,100 lines)

**Days 6-8 (Oct 19-21):** Simulation & Dynamics
- ✅ Simulation engine (800 lines)
- ✅ Dynamics models (900 lines)
- ✅ Integration methods (700 lines)
- ✅ Batch simulation (600 lines)

**Days 9-10 (Oct 22-23):** Tutorials & Examples
- ✅ 9 comprehensive tutorials (2,500 lines)
- ✅ 30+ code examples (2,700 lines)

**Day 11 (Oct 24):** Integration & QA
- ✅ Sphinx integration complete
- ✅ Build validation (0 warnings)
- ✅ Quality review and polish

---

## Success Criteria

### Quality Gates

**Documentation Completeness:**
- ✅ All 102 files have embedded source code
- ✅ Mathematical theory for all algorithms
- ✅ Line-by-line explanations for key functions
- ✅ Usage examples for all major features
- ✅ Architecture diagrams for workflows

**Technical Accuracy:**
- ✅ PSO convergence proofs match literature
- ✅ Dynamics equations validated against physics
- ✅ Integration methods theoretically sound
- ✅ Code examples tested and working
- ✅ Performance benchmarks reproducible

**Sphinx Integration:**
- ✅ 0 build warnings for Week 3 content
- ✅ All toctrees properly structured
- ✅ Cross-references working
- ✅ Navigation intuitive
- ✅ Search functionality complete

**Production Readiness:**
- ✅ Ready for academic publication
- ✅ Suitable for onboarding new developers
- ✅ Complete reference documentation
- ✅ Maintained consistency with Week 2

---

## Next Steps (Beyond Week 3)

### Week 4: Supporting Modules
- Plant models (27 files)
- Interfaces & protocols (46 files)
- Configuration system (6 files)

### Week 5: Analysis & Utilities
- Analysis module (30 files)
- Utils module (32 files)
- Benchmarks (11 files)

### Future Enhancements
- HIL system documentation
- Multi-objective optimization deep dive
- Advanced numerical methods
- GPU acceleration patterns

---

**Plan Version:** 1.0
**Created:** 2025-10-04
**Status:** 📋 PLANNED
**Estimated Start:** 2025-10-14
**Estimated Completion:** 2025-10-24
**Expected Output:** ~14,680 lines, 54+ files
