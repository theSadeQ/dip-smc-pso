# optimization.algorithms.swarm.pso

**Source:** `src\optimization\algorithms\swarm\pso.py`

## Module Overview

Enhanced Particle Swarm Optimization with framework integration.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/swarm/pso.py
:language: python
:linenos:
```

---

## Classes

### `ParticleSwarmOptimizer`

**Inherits from:** `PopulationBasedOptimizer`

Professional Particle Swarm Optimization algorithm.

This implementation provides a modern, framework-integrated PSO algorithm
with advanced features for control engineering applications.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/swarm/pso.py
:language: python
:pyobject: ParticleSwarmOptimizer
:linenos:
```

#### Methods (15)

##### `__init__(self, parameter_space, population_size, inertia_weight, cognitive_weight, social_weight, max_iterations, tolerance, adaptive_weights, velocity_clamping)`

Initialize PSO optimizer.

[View full source →](#method-particleswarmoptimizer-__init__)

##### `algorithm_name(self)`

Algorithm name.

[View full source →](#method-particleswarmoptimizer-algorithm_name)

##### `supports_constraints(self)`

PSO can handle constraints through penalty methods.

[View full source →](#method-particleswarmoptimizer-supports_constraints)

##### `supports_bounds(self)`

PSO naturally supports parameter bounds.

[View full source →](#method-particleswarmoptimizer-supports_bounds)

##### `optimize(self, problem)`

Perform PSO optimization.

[View full source →](#method-particleswarmoptimizer-optimize)

##### `initialize_population(self, rng)`

Initialize particle positions and velocities.

[View full source →](#method-particleswarmoptimizer-initialize_population)

##### `update_population(self, population, fitness)`

Update population (used by base class interface).

[View full source →](#method-particleswarmoptimizer-update_population)

##### `_update_velocities(self, rng)`

Update particle velocities.

[View full source →](#method-particleswarmoptimizer-_update_velocities)

##### `_update_positions(self)`

Update particle positions.

[View full source →](#method-particleswarmoptimizer-_update_positions)

##### `_update_personal_bests(self, fitness)`

Update personal best positions and fitness.

[View full source →](#method-particleswarmoptimizer-_update_personal_bests)

##### `_update_global_best(self)`

Update global best position and fitness.

[View full source →](#method-particleswarmoptimizer-_update_global_best)

##### `_update_adaptive_parameters(self, iteration, max_iterations)`

Update PSO parameters adaptively.

[View full source →](#method-particleswarmoptimizer-_update_adaptive_parameters)

##### `_calculate_diversity(self)`

Calculate swarm diversity.

[View full source →](#method-particleswarmoptimizer-_calculate_diversity)

##### `_apply_constraint_penalties(self, fitness, problem)`

Apply constraint penalties to fitness values.

[View full source →](#method-particleswarmoptimizer-_apply_constraint_penalties)

##### `get_swarm_statistics(self)`

Get detailed swarm statistics.

[View full source →](#method-particleswarmoptimizer-get_swarm_statistics)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import numpy as np`
- `from typing import Any, Callable, Dict, Optional, Tuple`
- `import logging`
- `from ...core.interfaces import PopulationBasedOptimizer, OptimizationProblem, OptimizationResult, ConvergenceStatus, ParameterSpace`
