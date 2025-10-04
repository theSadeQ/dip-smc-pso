# optimization.algorithms.multi_objective_pso

**Source:** `src\optimization\algorithms\multi_objective_pso.py`

## Module Overview

Multi-Objective Particle Swarm Optimization (MOPSO) for Controller Tuning.

This module implements a production-ready multi-objective PSO algorithm specifically
designed for control system parameter optimization. It provides Pareto front discovery,
convergence analysis, and advanced optimization features.

Features:
- NSGA-II style non-dominated sorting
- Crowding distance calculation for diversity maintenance
- Archive-based Pareto front management
- Hypervolume indicator for convergence assessment
- Real-time convergence monitoring
- Statistical validation and benchmarking

References:
- Coello, C.A.C., et al. "MOPSO: A proposal for multiple objective particle swarm optimization."
  IEEE Congress on Evolutionary Computation, 2002.
- Deb, K., et al. "A fast and elitist multiobjective genetic algorithm: NSGA-II."
  IEEE Transactions on Evolutionary Computation, 2002.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:linenos:
```

---

## Classes

### `MOPSOConfig`

Multi-Objective PSO Configuration.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:pyobject: MOPSOConfig
:linenos:
```

---

### `ParetoArchive`

Efficient Pareto archive for non-dominated solutions.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:pyobject: ParetoArchive
:linenos:
```

#### Methods (6)

##### `__init__(self, max_size)`

[View full source →](#method-paretoarchive-__init__)

##### `add_solution(self, position, objectives, metadata)`

Add a solution to the archive if it's non-dominated.

[View full source →](#method-paretoarchive-add_solution)

##### `_dominates(self, obj1, obj2)`

Check if obj1 dominates obj2 (minimization assumed).

[View full source →](#method-paretoarchive-_dominates)

##### `_truncate_archive(self)`

Remove solutions with lowest crowding distance.

[View full source →](#method-paretoarchive-_truncate_archive)

##### `_calculate_crowding_distance(self, objectives)`

Calculate crowding distance for diversity maintenance.

[View full source →](#method-paretoarchive-_calculate_crowding_distance)

##### `get_pareto_front(self)`

Get the current Pareto front.

[View full source →](#method-paretoarchive-get_pareto_front)

---

### `MultiObjectivePSO`

Multi-Objective Particle Swarm Optimization for Controller Tuning.

This implementation provides advanced multi-objective optimization capabilities
with Pareto front discovery and convergence analysis.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:pyobject: MultiObjectivePSO
:linenos:
```

#### Methods (10)

##### `__init__(self, bounds, config)`

[View full source →](#method-multiobjectivepso-__init__)

##### `optimize(self, objective_functions, constraints, reference_point)`

Execute multi-objective PSO optimization.

[View full source →](#method-multiobjectivepso-optimize)

##### `_evaluate_population(self, objective_functions, positions)`

Evaluate objective functions for all particles.

[View full source →](#method-multiobjectivepso-_evaluate_population)

##### `_update_leaders(self)`

Update leader particles from archive.

[View full source →](#method-multiobjectivepso-_update_leaders)

##### `_update_swarm(self, iteration)`

Update particle velocities and positions.

[View full source →](#method-multiobjectivepso-_update_swarm)

##### `_update_personal_bests(self, new_objectives)`

Update personal best positions and add to archive.

[View full source →](#method-multiobjectivepso-_update_personal_bests)

##### `_dominates(self, obj1, obj2)`

Check if obj1 dominates obj2.

[View full source →](#method-multiobjectivepso-_dominates)

##### `_calculate_hypervolume(self, objectives, reference_point)`

Calculate hypervolume indicator.

[View full source →](#method-multiobjectivepso-_calculate_hypervolume)

##### `_hypervolume_2d(self, objectives, reference_point)`

Calculate exact hypervolume for 2D case.

[View full source →](#method-multiobjectivepso-_hypervolume_2d)

##### `_hypervolume_monte_carlo(self, objectives, reference_point, n_samples)`

Monte Carlo approximation of hypervolume.

[View full source →](#method-multiobjectivepso-_hypervolume_monte_carlo)

---

## Functions

### `create_control_objectives(pso_tuner)`

Create multiple objective functions for control system optimization.

Parameters
----------
pso_tuner : PSOTuner
    Single-objective PSO tuner to extract fitness components

Returns
-------
List[Callable]
    List of objective functions for multi-objective optimization

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:pyobject: create_control_objectives
:linenos:
```

---

### `run_multi_objective_pso(controller_factory, config, seed)`

Run multi-objective PSO optimization for controller tuning.

Parameters
----------
controller_factory : Callable
    Factory function to create controllers with given gains
config : ConfigSchema
    Configuration object
seed : int, optional
    Random seed for reproducibility

Returns
-------
Dict[str, Any]
    Multi-objective optimization results

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/multi_objective_pso.py
:language: python
:pyobject: run_multi_objective_pso
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import logging`
- `import numpy as np`
- `from typing import Any, Callable, Dict, List, Optional, Tuple, Union`
- `from dataclasses import dataclass`
- `from concurrent.futures import ThreadPoolExecutor`
- `import threading`
- `from src.optimization.algorithms.pso_optimizer import PSOTuner`
- `from src.config import ConfigSchema`
