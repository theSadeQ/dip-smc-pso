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
