# optimization.algorithms.pso_optimizer

**Source:** `src\optimization\algorithms\pso_optimizer.py`

## Module Overview

Particle Swarm Optimisation (PSO) tuner for sliding-mode controllers.

This module defines the high-throughput, vectorised `PSOTuner` class that wraps
a particle swarm optimisation algorithm around the vectorised simulation of a
double inverted pendulum (DIP) system.  It incorporates improvements from
design review steps, including decoupling of global state, explicit random
number generation, dynamic instability penalties and configurable cost
normalisation.  The implementation follows robust control theory practices
and is fully documented with theoretical backing.

References used throughout this module are provided in the accompanying
design-review report.



## Architecture Diagram

```{mermaid}
graph TD
    A[Parameter Bounds] --> B[Initialize Swarm]
    B --> C[Particle Population]
    C --> D{For Each Particle}
    D --> E[Create Controller]
    E --> F[Run Simulation]
    F --> G[Compute Cost]
    G --> H[Update Personal Best]
    H --> I{All Particles Done?}
    I -->|No| D
    I -->|Yes| J[Update Global Best]
    J --> K{Convergence?}
    K -->|No| L[Update Velocities]
    L --> M[Update Positions]
    M --> D
    K -->|Yes| N[Return Optimal Gains]

    style C fill:#9cf
    style G fill:#ff9
    style J fill:#f9f
    style N fill:#9f9
```

**Data Flow:**
1. Initialize swarm in parameter space
2. Evaluate fitness via closed-loop simulation
3. Update particle velocities: v = wv + c₁(p-x) + c₂(g-x)
4. Converge to optimal controller gains
5. Return best solution with performance metrics


## Mathematical Foundation

### Particle Swarm Optimization

PSO updates particle positions using:

```{math}
\begin{align}
v_i^{k+1} &= wv_i^k + c_1r_1(p_i - x_i^k) + c_2r_2(g - x_i^k) \\
x_i^{k+1} &= x_i^k + v_i^{k+1}
\end{align}
```

Where:
- $w$: Inertia weight (exploration vs exploitation)
- $c_1, c_2$: Cognitive and social coefficients
- $p_i$: Personal best position
- $g$: Global best position

### Convergence Properties

Proper parameter selection ensures:
1. **Global exploration**: $w \in [0.4, 0.9]$
2. **Local exploitation**: $c_1 + c_2 < 4$
3. **Velocity bounds**: Prevent divergence

**See:** {doc}`../../../mathematical_foundations/optimization_theory`


## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/pso_optimizer.py
:language: python
:linenos:
```

---

## Classes

### `PSOTuner`

High-throughput, vectorised tuner for sliding-mode controllers.

The tuner wraps a particle swarm optimisation algorithm around the
vectorised simulation.  It uses local PRNGs to avoid global side effects
and computes instability penalties based on normalisation constants.  Cost
aggregation between mean and worst-case performance is controlled via
``COMBINE_WEIGHTS``.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/pso_optimizer.py
:language: python
:pyobject: PSOTuner
:linenos:
```

#### Methods (7)

##### `__init__(self, controller_factory, config, seed, rng)`

Initialise the PSOTuner.

[View full source →](#method-psotuner-__init__)

##### `_iter_perturbed_physics(self)`

Yield perturbed physics parameters for robustness evaluation.

[View full source →](#method-psotuner-_iter_perturbed_physics)

##### `_compute_cost_from_traj(self, t, x_b, u_b, sigma_b)`

Compute the cost per particle from simulated trajectories.

[View full source →](#method-psotuner-_compute_cost_from_traj)

##### `_normalise(self, val, denom)`

Safely normalise an array by a scalar denominator using the instance's threshold.

[View full source →](#method-psotuner-_normalise)

##### `_combine_costs(self, costs)`

Aggregate costs across uncertainty draws using the instance's weights.

[View full source →](#method-psotuner-_combine_costs)

##### `_fitness(self, particles)`

Vectorised fitness function for a swarm of particles.

[View full source →](#method-psotuner-_fitness)

##### `optimise(self)`

Run particle swarm optimisation with optional overrides.

[View full source →](#method-psotuner-optimise)

---

## Functions

### `_normalise(val, denom)`

Safely normalise an array by a scalar denominator.

When the denominator is very small (≤ NORMALISATION_THRESHOLD) the input
array is returned unchanged.  The division suppresses divide-by-zero
warnings.  See tests for expected behaviour.

Parameters
----------
val : np.ndarray
    Array of values to be normalised.
denom : float
    Scalar denominator.

Returns
-------
np.ndarray
    The normalised array.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/pso_optimizer.py
:language: python
:pyobject: _normalise
:linenos:
```

---

### `_seeded_global_numpy(seed)`

**Decorators:** `@contextmanager`

Context manager to temporarily seed the global NumPy RNG.

This is used only in the optimise method to ensure deterministic
behaviour of the PySwarms optimiser when a fixed seed is provided.  It
saves and restores the global RNG state.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/pso_optimizer.py
:language: python
:pyobject: _seeded_global_numpy
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import logging`
- `from contextlib import contextmanager`
- `from pathlib import Path`
- `from typing import Any, Callable, Dict, Iterable, Optional, Union`
- `import numpy as np`
- `from src.config import ConfigSchema, load_config`
- `from src.utils.seed import create_rng`
- `from ...plant.models.dynamics import DIPParams`
- `from ...simulation.engines.vector_sim import simulate_system_batch`


## Usage Examples

### Multi-Objective PSO Optimization

```python
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_smc_for_pso, SMCType

# Define multi-objective cost function
def multi_objective_cost(gains):
    controller = create_smc_for_pso(SMCType.HYBRID, gains)
    result = simulate(controller, duration=10.0)

    # Combine objectives with weights
    tracking_error = np.mean(np.abs(result.states[:, :2]))  # Angles
    control_effort = np.mean(np.abs(result.control))
    chattering = np.std(np.diff(result.control))

    return 0.6 * tracking_error + 0.3 * control_effort + 0.1 * chattering

# Configure PSO with adaptive parameters
pso = PSOTuner(
    controller_factory=lambda g: create_smc_for_pso(SMCType.HYBRID, g),
    bounds=([1.0]*4, [50.0]*4),  # Hybrid has 4 gains
    n_particles=40,
    max_iter=100,
    w=0.7,           # Inertia weight
    c1=1.5,          # Cognitive coefficient
    c2=1.5           # Social coefficient
)

best_gains, best_cost = pso.optimize()
print(f"Optimal gains: {best_gains}, Cost: {best_cost:.4f}")
```

### Convergence Monitoring & Analysis

```python
import matplotlib.pyplot as plt

# Track convergence history
convergence_history = []

def convergence_callback(iteration, global_best_cost):
    convergence_history.append(global_best_cost)
    print(f"Iteration {iteration}: Best cost = {global_best_cost:.6f}")

pso = PSOTuner(
    controller_factory=lambda g: create_smc_for_pso(SMCType.CLASSICAL, g),
    bounds=(bounds_lower, bounds_upper),
    callback=convergence_callback
)

best_gains, _ = pso.optimize()

# Plot convergence
plt.plot(convergence_history)
plt.xlabel('Iteration')
plt.ylabel('Best Cost')
plt.title('PSO Convergence Analysis')
plt.grid(True)
plt.show()
```

### Robustness-Focused Optimization

```python
# Optimize for robustness across parameter uncertainty
def robust_cost(gains):
    controller_factory = lambda: create_smc_for_pso(SMCType.ADAPTIVE, gains)

    # Test across multiple scenarios
    costs = []
    for mass_variation in [0.8, 1.0, 1.2]:  # ±20% mass uncertainty
        dynamics = SimplifiedDynamics(cart_mass=mass_variation * 1.0)
        result = simulate(controller_factory(), dynamics, duration=10.0)
        costs.append(compute_ISE(result.states))

    # Return worst-case cost (robust optimization)
    return max(costs)

pso = PSOTuner(
    controller_factory=lambda g: None,  # Not used, cost computes internally
    bounds=([0.1]*5, [100.0]*5),  # Adaptive SMC: 5 gains
    fitness_function=robust_cost,
    n_particles=50,
    max_iter=150
)

robust_gains, worst_case_cost = pso.optimize()
```

**See:** {doc}`../../../optimization_workflows/advanced_pso_strategies`

