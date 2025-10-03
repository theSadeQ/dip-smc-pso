# optimization.core.problem

**Source:** `src\optimization\core\problem.py`

## Module Overview

Optimization problem builders and specialized problem types.

## Complete Source Code

```{literalinclude} ../../../src/optimization/core/problem.py
:language: python
:linenos:
```

---

## Classes

### `OptimizationProblemBuilder`

Builder for constructing optimization problems.

#### Source Code

```{literalinclude} ../../../src/optimization/core/problem.py
:language: python
:pyobject: OptimizationProblemBuilder
:linenos:
```

#### Methods (9)

##### `__init__(self)`

Initialize problem builder.

[View full source →](#method-optimizationproblembuilder-__init__)

##### `with_objective(self, objective)`

Set objective function.

[View full source →](#method-optimizationproblembuilder-with_objective)

##### `with_parameter_space(self, parameter_space)`

Set parameter space.

[View full source →](#method-optimizationproblembuilder-with_parameter_space)

##### `with_bounds(self, lower, upper)`

Set parameter bounds (creates continuous parameter space).

[View full source →](#method-optimizationproblembuilder-with_bounds)

##### `minimize(self)`

Set optimization type to minimization.

[View full source →](#method-optimizationproblembuilder-minimize)

##### `maximize(self)`

Set optimization type to maximization.

[View full source →](#method-optimizationproblembuilder-maximize)

##### `with_constraint(self, constraint)`

Add constraint.

[View full source →](#method-optimizationproblembuilder-with_constraint)

##### `with_name(self, name)`

Set problem name.

[View full source →](#method-optimizationproblembuilder-with_name)

##### `build(self)`

Build optimization problem.

[View full source →](#method-optimizationproblembuilder-build)

---

### `ControlOptimizationProblem`

**Inherits from:** `OptimizationProblem`

Specialized optimization problem for control parameter tuning.

#### Source Code

```{literalinclude} ../../../src/optimization/core/problem.py
:language: python
:pyobject: ControlOptimizationProblem
:linenos:
```

#### Methods (3)

##### `__init__(self, objective, parameter_space, controller_factory, simulation_config, optimization_type, constraints, name)`

Initialize control optimization problem.

[View full source →](#method-controloptimizationproblem-__init__)

##### `create_controller(self, parameters)`

Create controller from optimization parameters.

[View full source →](#method-controloptimizationproblem-create_controller)

##### `simulate_controller(self, parameters)`

Simulate controller with given parameters.

[View full source →](#method-controloptimizationproblem-simulate_controller)

---

### `MultiObjectiveProblem`

**Inherits from:** `OptimizationProblem`

Multi-objective optimization problem.

#### Source Code

```{literalinclude} ../../../src/optimization/core/problem.py
:language: python
:pyobject: MultiObjectiveProblem
:linenos:
```

#### Methods (3)

##### `__init__(self, objectives, parameter_space, weights, optimization_type, constraints, name)`

Initialize multi-objective problem.

[View full source →](#method-multiobjectiveproblem-__init__)

##### `evaluate_objectives(self, parameters)`

Evaluate all individual objectives.

[View full source →](#method-multiobjectiveproblem-evaluate_objectives)

##### `evaluate_objectives_batch(self, parameters)`

Evaluate all objectives for batch of parameters.

[View full source →](#method-multiobjectiveproblem-evaluate_objectives_batch)

---

### `WeightedSumObjective`

**Inherits from:** `ObjectiveFunction`

Weighted sum of multiple objectives.

#### Source Code

```{literalinclude} ../../../src/optimization/core/problem.py
:language: python
:pyobject: WeightedSumObjective
:linenos:
```

#### Methods (4)

##### `__init__(self, objectives, weights)`

Initialize weighted sum objective.

[View full source →](#method-weightedsumobjective-__init__)

##### `evaluate(self, parameters)`

Evaluate weighted sum of objectives.

[View full source →](#method-weightedsumobjective-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate weighted sum for batch of parameters.

[View full source →](#method-weightedsumobjective-evaluate_batch)

##### `is_vectorized(self)`

Vectorized if all component objectives are vectorized.

[View full source →](#method-weightedsumobjective-is_vectorized)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Callable, Union`
- `import numpy as np`
- `from .interfaces import OptimizationProblem, ObjectiveFunction, ParameterSpace, Constraint, OptimizationType`
- `from .parameters import ContinuousParameterSpace`
