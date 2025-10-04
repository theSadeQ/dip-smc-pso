# optimization.algorithms.gradient_based.bfgs

**Source:** `src\optimization\algorithms\gradient_based\bfgs.py`

## Module Overview

BFGS quasi-Newton optimization algorithm with numerical gradients.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/bfgs.py
:language: python
:linenos:
```

---

## Classes

### `BFGSConfig`

Configuration for BFGS algorithm.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/bfgs.py
:language: python
:pyobject: BFGSConfig
:linenos:
```

---

### `BFGSOptimizer`

**Inherits from:** `OptimizationAlgorithm`

BFGS quasi-Newton optimization algorithm.

The BFGS (Broyden-Fletcher-Goldfarb-Shanno) algorithm is a quasi-Newton
method that approximates the Hessian matrix using gradient information.
It builds up curvature information iteratively to achieve superlinear
convergence near the optimum.

Features:
- Numerical gradient computation (forward, backward, central differences)
- Line search with Wolfe conditions
- Hessian approximation updates
- Boundary constraint handling
- Robust convergence criteria

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/bfgs.py
:language: python
:pyobject: BFGSOptimizer
:linenos:
```

#### Methods (16)

##### `__init__(self, config)`

Initialize BFGS algorithm.

[View full source →](#method-bfgsoptimizer-__init__)

##### `optimize(self, problem, parameter_space, initial_guess)`

Run BFGS optimization.

[View full source →](#method-bfgsoptimizer-optimize)

##### `_initialize_optimization(self, initial_guess)`

Initialize optimization state.

[View full source →](#method-bfgsoptimizer-_initialize_optimization)

##### `_perform_iteration(self)`

Perform one BFGS iteration.

[View full source →](#method-bfgsoptimizer-_perform_iteration)

##### `_compute_numerical_gradient(self, x)`

Compute numerical gradient using finite differences.

[View full source →](#method-bfgsoptimizer-_compute_numerical_gradient)

##### `_update_hessian_inverse(self, x_old, x_new, grad_old, grad_new)`

Update inverse Hessian approximation using BFGS formula.

[View full source →](#method-bfgsoptimizer-_update_hessian_inverse)

##### `_line_search(self, x, f, gradient, direction)`

Line search with Wolfe conditions.

[View full source →](#method-bfgsoptimizer-_line_search)

##### `_safe_evaluate(self, x)`

Safely evaluate objective function.

[View full source →](#method-bfgsoptimizer-_safe_evaluate)

##### `_check_termination(self)`

Check termination conditions.

[View full source →](#method-bfgsoptimizer-_check_termination)

##### `_create_result(self)`

Create optimization result.

[View full source →](#method-bfgsoptimizer-_create_result)

##### `_compute_hessian_condition_number(self)`

Compute condition number of Hessian approximation.

[View full source →](#method-bfgsoptimizer-_compute_hessian_condition_number)

##### `get_optimization_info(self)`

Get detailed optimization information.

[View full source →](#method-bfgsoptimizer-get_optimization_info)

##### `_estimate_convergence_rate(self)`

Estimate convergence rate from function value history.

[View full source →](#method-bfgsoptimizer-_estimate_convergence_rate)

##### `reset_hessian(self)`

Reset Hessian approximation to identity.

[View full source →](#method-bfgsoptimizer-reset_hessian)

##### `get_hessian_eigenvalues(self)`

Get eigenvalues of current Hessian approximation.

[View full source →](#method-bfgsoptimizer-get_hessian_eigenvalues)

##### `get_search_direction(self)`

Get current search direction.

[View full source →](#method-bfgsoptimizer-get_search_direction)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Callable, Tuple`
- `import numpy as np`
- `import warnings`
- `from dataclasses import dataclass`
- `from ..base import OptimizationAlgorithm`
- `from ...core.interfaces import OptimizationProblem, ParameterSpace, OptimizationResult`
- `from ...core.parameters import ContinuousParameterSpace`
