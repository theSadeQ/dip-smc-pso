# optimization.core.interfaces

**Source:** `src\optimization\core\interfaces.py`

## Module Overview

Core interfaces for professional optimization framework.

## Complete Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:linenos:
```

---

## Classes

### `OptimizationType`

**Inherits from:** `Enum`

Types of optimization problems.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: OptimizationType
:linenos:
```

---

### `ConvergenceStatus`

**Inherits from:** `Enum`

Convergence status indicators.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: ConvergenceStatus
:linenos:
```

---

### `ParameterSpace`

**Inherits from:** `ABC`

Abstract base class for parameter spaces.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: ParameterSpace
:linenos:
```

#### Methods (5)

##### `sample(self, n_samples, rng)`

Sample parameters from the space.

[View full source →](#method-parameterspace-sample)

##### `validate(self, parameters)`

Validate parameters are within the space.

[View full source →](#method-parameterspace-validate)

##### `clip(self, parameters)`

Clip parameters to valid bounds.

[View full source →](#method-parameterspace-clip)

##### `dimensions(self)`

Number of optimization dimensions.

[View full source →](#method-parameterspace-dimensions)

##### `bounds(self)`

Lower and upper bounds for each parameter.

[View full source →](#method-parameterspace-bounds)

---

### `ObjectiveFunction`

**Inherits from:** `ABC`

Abstract base class for optimization objective functions.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: ObjectiveFunction
:linenos:
```

#### Methods (7)

##### `evaluate(self, parameters)`

Evaluate objective function at given parameters.

[View full source →](#method-objectivefunction-evaluate)

##### `evaluate_batch(self, parameters)`

Evaluate objective function for batch of parameters.

[View full source →](#method-objectivefunction-evaluate_batch)

##### `is_vectorized(self)`

Whether function supports vectorized evaluation.

[View full source →](#method-objectivefunction-is_vectorized)

##### `supports_gradients(self)`

Whether function provides gradient information.

[View full source →](#method-objectivefunction-supports_gradients)

##### `gradient(self, parameters)`

Compute gradient at given parameters.

[View full source →](#method-objectivefunction-gradient)

##### `evaluation_count(self)`

Number of function evaluations performed.

[View full source →](#method-objectivefunction-evaluation_count)

##### `reset_evaluation_count(self)`

Reset evaluation counter.

[View full source →](#method-objectivefunction-reset_evaluation_count)

---

### `Constraint`

**Inherits from:** `ABC`

Abstract base class for optimization constraints.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: Constraint
:linenos:
```

#### Methods (3)

##### `evaluate(self, parameters)`

Evaluate constraint at given parameters.

[View full source →](#method-constraint-evaluate)

##### `is_satisfied(self, parameters, tolerance)`

Check if constraint is satisfied.

[View full source →](#method-constraint-is_satisfied)

##### `constraint_type(self)`

Type of constraint ('equality' or 'inequality').

[View full source →](#method-constraint-constraint_type)

---

### `OptimizationResult`

Container for optimization results.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: OptimizationResult
:linenos:
```

#### Methods (2)

##### `__init__(self, x, fun, success, status, message, nit, nfev)`

Initialize optimization result.

[View full source →](#method-optimizationresult-__init__)

##### `to_dict(self)`

Convert result to dictionary.

[View full source →](#method-optimizationresult-to_dict)

---

### `OptimizationProblem`

Complete optimization problem specification.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: OptimizationProblem
:linenos:
```

#### Methods (4)

##### `__init__(self, objective, parameter_space, optimization_type, constraints, name)`

Initialize optimization problem.

[View full source →](#method-optimizationproblem-__init__)

##### `evaluate_objective(self, parameters)`

Evaluate objective with proper sign handling.

[View full source →](#method-optimizationproblem-evaluate_objective)

##### `evaluate_objective_batch(self, parameters)`

Evaluate objective batch with proper sign handling.

[View full source →](#method-optimizationproblem-evaluate_objective_batch)

##### `check_constraints(self, parameters)`

Check all constraints.

[View full source →](#method-optimizationproblem-check_constraints)

---

### `Optimizer`

**Inherits from:** `ABC`

Abstract base class for optimization algorithms.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: Optimizer
:linenos:
```

#### Methods (8)

##### `__init__(self, parameter_space)`

Initialize optimizer.

[View full source →](#method-optimizer-__init__)

##### `optimize(self, problem)`

Perform optimization.

[View full source →](#method-optimizer-optimize)

##### `set_convergence_monitor(self, monitor)`

Set convergence monitor.

[View full source →](#method-optimizer-set_convergence_monitor)

##### `set_callback(self, callback)`

Set iteration callback function.

[View full source →](#method-optimizer-set_callback)

##### `algorithm_name(self)`

Name of the optimization algorithm.

[View full source →](#method-optimizer-algorithm_name)

##### `supports_constraints(self)`

Whether algorithm supports constraints.

[View full source →](#method-optimizer-supports_constraints)

##### `supports_bounds(self)`

Whether algorithm supports parameter bounds.

[View full source →](#method-optimizer-supports_bounds)

##### `is_population_based(self)`

Whether algorithm uses a population of candidates.

[View full source →](#method-optimizer-is_population_based)

---

### `ConvergenceMonitor`

**Inherits from:** `ABC`

Abstract base class for convergence monitoring.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: ConvergenceMonitor
:linenos:
```

#### Methods (4)

##### `update(self, iteration, best_value, parameters)`

Update convergence monitor with new iteration data.

[View full source →](#method-convergencemonitor-update)

##### `check_convergence(self)`

Check if convergence criteria are met.

[View full source →](#method-convergencemonitor-check_convergence)

##### `reset(self)`

Reset convergence monitor.

[View full source →](#method-convergencemonitor-reset)

##### `convergence_history(self)`

Get convergence history data.

[View full source →](#method-convergencemonitor-convergence_history)

---

### `PopulationBasedOptimizer`

**Inherits from:** `Optimizer`

Base class for population-based optimizers.

#### Source Code

```{literalinclude} ../../../src/optimization/core/interfaces.py
:language: python
:pyobject: PopulationBasedOptimizer
:linenos:
```

#### Methods (4)

##### `__init__(self, parameter_space, population_size)`

Initialize population-based optimizer.

[View full source →](#method-populationbasedoptimizer-__init__)

##### `is_population_based(self)`

Population-based optimizers return True.

[View full source →](#method-populationbasedoptimizer-is_population_based)

##### `initialize_population(self, rng)`

Initialize population of parameter vectors.

[View full source →](#method-populationbasedoptimizer-initialize_population)

##### `update_population(self, population, fitness)`

Update population based on fitness values.

[View full source →](#method-populationbasedoptimizer-update_population)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, List, Optional, Tuple, Union, Callable`
- `import numpy as np`
- `from enum import Enum`
