# optimization.objectives.base

**Source:** `src\optimization\objectives\base.py`

## Module Overview

Base classes for optimization objective functions.

## Complete Source Code

```{literalinclude} ../../../src/optimization/objectives/base.py
:language: python
:linenos:
```

---

## Classes

### `SimulationBasedObjective`

**Inherits from:** `ObjectiveFunction`

Base class for objectives that require simulation.

#### Source Code

```{literalinclude} ../../../src/optimization/objectives/base.py
:language: python
:pyobject: SimulationBasedObjective
:linenos:
```

#### Methods (6)

##### `__init__(self, simulation_config, controller_factory, reference_trajectory)`

Initialize simulation-based objective.

[View full source →](#method-simulationbasedobjective-__init__)

##### `_compute_objective_from_simulation(self, times, states, controls)`

Compute objective value from simulation results.

[View full source →](#method-simulationbasedobjective-_compute_objective_from_simulation)

##### `evaluate(self, parameters)`

Evaluate objective for single parameter set.

[View full source →](#method-simulationbasedobjective-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate objective for batch of parameters.

[View full source →](#method-simulationbasedobjective-evaluate_batch)

##### `_run_simulation(self, parameters)`

Run simulation with given parameters.

[View full source →](#method-simulationbasedobjective-_run_simulation)

##### `is_vectorized(self)`

Simulation-based objectives are not inherently vectorized.

[View full source →](#method-simulationbasedobjective-is_vectorized)

---

### `AnalyticalObjective`

**Inherits from:** `ObjectiveFunction`

Base class for analytical objective functions.

#### Source Code

```{literalinclude} ../../../src/optimization/objectives/base.py
:language: python
:pyobject: AnalyticalObjective
:linenos:
```

#### Methods (5)

##### `__init__(self)`

Initialize analytical objective.

[View full source →](#method-analyticalobjective-__init__)

##### `_compute_analytical_objective(self, parameters)`

Compute objective analytically.

[View full source →](#method-analyticalobjective-_compute_analytical_objective)

##### `evaluate(self, parameters)`

Evaluate objective for single parameter set.

[View full source →](#method-analyticalobjective-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate objective for batch of parameters.

[View full source →](#method-analyticalobjective-evaluate_batch)

##### `is_vectorized(self)`

Analytical objectives can be vectorized.

[View full source →](#method-analyticalobjective-is_vectorized)

---

### `CompositeObjective`

**Inherits from:** `ObjectiveFunction`

Composite objective combining multiple objectives.

#### Source Code

```{literalinclude} ../../../src/optimization/objectives/base.py
:language: python
:pyobject: CompositeObjective
:linenos:
```

#### Methods (6)

##### `__init__(self, objectives, weights, combination_method)`

Initialize composite objective.

[View full source →](#method-compositeobjective-__init__)

##### `evaluate(self, parameters)`

Evaluate composite objective.

[View full source →](#method-compositeobjective-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate composite objective for batch.

[View full source →](#method-compositeobjective-evaluate_batch)

##### `_combine_objectives(self, values)`

Combine objective values according to method.

[View full source →](#method-compositeobjective-_combine_objectives)

##### `is_vectorized(self)`

Composite objective is vectorized if all components are.

[View full source →](#method-compositeobjective-is_vectorized)

##### `get_individual_evaluations(self, parameters)`

Get individual objective evaluations.

[View full source →](#method-compositeobjective-get_individual_evaluations)

---

### `PenaltyObjective`

**Inherits from:** `ObjectiveFunction`

Objective with constraint penalties.

#### Source Code

```{literalinclude} ../../../src/optimization/objectives/base.py
:language: python
:pyobject: PenaltyObjective
:linenos:
```

#### Methods (5)

##### `__init__(self, base_objective, constraints, penalty_factor)`

Initialize penalty objective.

[View full source →](#method-penaltyobjective-__init__)

##### `evaluate(self, parameters)`

Evaluate objective with penalties.

[View full source →](#method-penaltyobjective-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate objective with penalties for batch.

[View full source →](#method-penaltyobjective-evaluate_batch)

##### `_compute_penalty(self, parameters)`

Compute constraint penalty.

[View full source →](#method-penaltyobjective-_compute_penalty)

##### `is_vectorized(self)`

Penalty objective inherits vectorization from base.

[View full source →](#method-penaltyobjective-is_vectorized)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, List, Optional, Union, Callable`
- `import numpy as np`
- `from ..core.interfaces import ObjectiveFunction`
