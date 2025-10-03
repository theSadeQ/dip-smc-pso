# optimization.objectives.multi.pareto

**Source:** `src\optimization\objectives\multi\pareto.py`

## Module Overview

Pareto-based multi-objective optimization.

## Complete Source Code

```{literalinclude} ../../../src/optimization/objectives/multi/pareto.py
:language: python
:linenos:
```

---

## Classes

### `ParetoObjective`

**Inherits from:** `SimulationBasedObjective`

Multi-objective optimization using Pareto dominance.

This objective handles true multi-objective optimization by maintaining
a Pareto frontier of non-dominated solutions. Unlike weighted sum approaches,
this can find solutions on non-convex portions of the Pareto frontier.

The objective returns a composite metric but also maintains detailed
Pareto analysis for optimization algorithms that can handle it.

#### Source Code

```{literalinclude} ../../../src/optimization/objectives/multi/pareto.py
:language: python
:pyobject: ParetoObjective
:linenos:
```

#### Methods (23)

##### `__init__(self, simulation_config, controller_factory, objectives, scalarization_method, reference_point, normalization, reference_trajectory)`

Initialize Pareto multi-objective.

[View full source →](#method-paretoobjective-__init__)

##### `_compute_objective_from_simulation(self, times, states, controls)`

Compute Pareto-based objective from simulation results.

[View full source →](#method-paretoobjective-_compute_objective_from_simulation)

##### `_update_pareto_frontier(self, parameters, objectives)`

Update the Pareto frontier with new solution.

[View full source →](#method-paretoobjective-_update_pareto_frontier)

##### `_check_dominance(self, obj1, obj2)`

Check dominance relationship between two objective vectors.

[View full source →](#method-paretoobjective-_check_dominance)

##### `_normalize_objectives(self, objective_values)`

Normalize objective values.

[View full source →](#method-paretoobjective-_normalize_objectives)

##### `_scalarize_objectives(self, objectives)`

Convert multi-objective values to scalar.

[View full source →](#method-paretoobjective-_scalarize_objectives)

##### `_compute_hypervolume_contribution(self, objectives)`

Compute hypervolume contribution (approximation).

[View full source →](#method-paretoobjective-_compute_hypervolume_contribution)

##### `_compute_crowding_distance(self, objectives)`

Compute crowding distance metric.

[View full source →](#method-paretoobjective-_compute_crowding_distance)

##### `_compute_epsilon_indicator(self, objectives)`

Compute epsilon indicator metric.

[View full source →](#method-paretoobjective-_compute_epsilon_indicator)

##### `get_pareto_frontier(self)`

Get current Pareto frontier information.

[View full source →](#method-paretoobjective-get_pareto_frontier)

##### `_compute_frontier_metrics(self)`

Compute metrics about the current Pareto frontier.

[View full source →](#method-paretoobjective-_compute_frontier_metrics)

##### `_compute_frontier_hypervolume(self)`

Compute hypervolume of current Pareto frontier.

[View full source →](#method-paretoobjective-_compute_frontier_hypervolume)

##### `_compute_frontier_spread(self, objectives_array)`

Compute spread (diversity) of Pareto frontier.

[View full source →](#method-paretoobjective-_compute_frontier_spread)

##### `_compute_frontier_extent(self, objectives_array)`

Compute extent (range) of Pareto frontier.

[View full source →](#method-paretoobjective-_compute_frontier_extent)

##### `evaluate_solution_quality(self, times, states, controls)`

Evaluate solution quality in multi-objective context.

[View full source →](#method-paretoobjective-evaluate_solution_quality)

##### `_compute_pareto_rank(self, objectives)`

Compute Pareto rank (1 = non-dominated, higher = more dominated).

[View full source →](#method-paretoobjective-_compute_pareto_rank)

##### `_count_dominated_solutions(self, objectives)`

Count how many solutions this one dominates.

[View full source →](#method-paretoobjective-_count_dominated_solutions)

##### `_count_dominating_solutions(self, objectives)`

Count how many solutions dominate this one.

[View full source →](#method-paretoobjective-_count_dominating_solutions)

##### `reset_pareto_frontier(self)`

Reset the Pareto frontier and evaluation history.

[View full source →](#method-paretoobjective-reset_pareto_frontier)

##### `get_optimization_progress(self)`

Get optimization progress information.

[View full source →](#method-paretoobjective-get_optimization_progress)

##### `_compute_convergence_metrics(self)`

Compute convergence metrics for the optimization.

[View full source →](#method-paretoobjective-_compute_convergence_metrics)

##### `_measure_recent_improvement(self, recent_objectives)`

Measure improvement in recent evaluations.

[View full source →](#method-paretoobjective-_measure_recent_improvement)

##### `_measure_frontier_stability(self)`

Measure stability of Pareto frontier.

[View full source →](#method-paretoobjective-_measure_frontier_stability)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Union, Callable, Tuple`
- `import numpy as np`
- `import warnings`
- `from ..base import SimulationBasedObjective`
- `from ...core.interfaces import ObjectiveFunction`
- `from src.utils.numerical_stability import EPSILON_DIV`
