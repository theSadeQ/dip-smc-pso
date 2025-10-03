# optimization.algorithms.base

**Source:** `src\optimization\algorithms\base.py`

## Module Overview

Base classes for optimization algorithms.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/base.py
:language: python
:linenos:
```

---

## Classes

### `OptimizationAlgorithm`

**Inherits from:** `ABC`

Abstract base class for optimization algorithms.

This class defines the common interface that all optimization algorithms
must implement. It provides a standard structure for algorithm initialization,
execution, and result reporting.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/base.py
:language: python
:pyobject: OptimizationAlgorithm
:linenos:
```

#### Methods (7)

##### `__init__(self)`

Initialize the optimization algorithm.

[View full source →](#method-optimizationalgorithm-__init__)

##### `optimize(self, problem, parameter_space)`

Run the optimization algorithm.

[View full source →](#method-optimizationalgorithm-optimize)

##### `get_algorithm_info(self)`

Get information about the algorithm.

[View full source →](#method-optimizationalgorithm-get_algorithm_info)

##### `reset(self)`

Reset the algorithm to initial state.

[View full source →](#method-optimizationalgorithm-reset)

##### `supports_constraints(self)`

Check if algorithm supports constraints.

[View full source →](#method-optimizationalgorithm-supports_constraints)

##### `supports_parallel_evaluation(self)`

Check if algorithm supports parallel function evaluation.

[View full source →](#method-optimizationalgorithm-supports_parallel_evaluation)

##### `get_default_parameters(self)`

Get default algorithm parameters.

[View full source →](#method-optimizationalgorithm-get_default_parameters)

---

### `PopulationBasedAlgorithm`

**Inherits from:** `OptimizationAlgorithm`

Base class for population-based optimization algorithms.

This class extends OptimizationAlgorithm with common functionality
for algorithms that maintain a population of candidate solutions.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/base.py
:language: python
:pyobject: PopulationBasedAlgorithm
:linenos:
```

#### Methods (4)

##### `__init__(self, population_size)`

Initialize population-based algorithm.

[View full source →](#method-populationbasedalgorithm-__init__)

##### `get_algorithm_info(self)`

Get algorithm information including population details.

[View full source →](#method-populationbasedalgorithm-get_algorithm_info)

##### `reset(self)`

Reset the algorithm including population.

[View full source →](#method-populationbasedalgorithm-reset)

##### `supports_parallel_evaluation(self)`

Population-based algorithms typically support parallel evaluation.

[View full source →](#method-populationbasedalgorithm-supports_parallel_evaluation)

---

### `GradientBasedAlgorithm`

**Inherits from:** `OptimizationAlgorithm`

Base class for gradient-based optimization algorithms.

This class extends OptimizationAlgorithm with common functionality
for algorithms that use gradient information.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/base.py
:language: python
:pyobject: GradientBasedAlgorithm
:linenos:
```

#### Methods (4)

##### `__init__(self, gradient_tolerance)`

Initialize gradient-based algorithm.

[View full source →](#method-gradientbasedalgorithm-__init__)

##### `get_algorithm_info(self)`

Get algorithm information including gradient details.

[View full source →](#method-gradientbasedalgorithm-get_algorithm_info)

##### `reset(self)`

Reset the algorithm including gradient information.

[View full source →](#method-gradientbasedalgorithm-reset)

##### `requires_gradients(self)`

Check if algorithm requires analytical gradients.

[View full source →](#method-gradientbasedalgorithm-requires_gradients)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, Optional`
- `from ..core.interfaces import OptimizationProblem, ParameterSpace, OptimizationResult`
