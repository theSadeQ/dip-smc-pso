# optimization.algorithms.gradient_based.nelder_mead

**Source:** `src\optimization\algorithms\gradient_based\nelder_mead.py`

## Module Overview

Nelder-Mead simplex optimization algorithm.

## Complete Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/nelder_mead.py
:language: python
:linenos:
```

---

## Classes

### `NelderMeadConfig`

Configuration for Nelder-Mead algorithm.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/nelder_mead.py
:language: python
:pyobject: NelderMeadConfig
:linenos:
```

---

### `NelderMeadSimplex`

Nelder-Mead simplex data structure.

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/nelder_mead.py
:language: python
:pyobject: NelderMeadSimplex
:linenos:
```

#### Methods (12)

##### `__init__(self, vertices, function_values)`

[View full source →](#method-neldermeadsimplex-__init__)

##### `_sort_vertices(self)`

Sort vertices by function value (best first).

[View full source →](#method-neldermeadsimplex-_sort_vertices)

##### `best_vertex(self)`

Get the best vertex.

[View full source →](#method-neldermeadsimplex-best_vertex)

##### `best_value(self)`

Get the best function value.

[View full source →](#method-neldermeadsimplex-best_value)

##### `worst_vertex(self)`

Get the worst vertex.

[View full source →](#method-neldermeadsimplex-worst_vertex)

##### `worst_value(self)`

Get the worst function value.

[View full source →](#method-neldermeadsimplex-worst_value)

##### `second_worst_vertex(self)`

Get the second worst vertex.

[View full source →](#method-neldermeadsimplex-second_worst_vertex)

##### `second_worst_value(self)`

Get the second worst function value.

[View full source →](#method-neldermeadsimplex-second_worst_value)

##### `centroid(self, exclude_worst)`

Calculate centroid of simplex.

[View full source →](#method-neldermeadsimplex-centroid)

##### `replace_worst(self, new_vertex, new_value)`

Replace worst vertex with new vertex.

[View full source →](#method-neldermeadsimplex-replace_worst)

##### `shrink_simplex(self, shrinkage_coeff)`

Shrink simplex towards best vertex.

[View full source →](#method-neldermeadsimplex-shrink_simplex)

##### `volume(self)`

Calculate simplex volume.

[View full source →](#method-neldermeadsimplex-volume)

---

### `NelderMead`

**Inherits from:** `OptimizationAlgorithm`

Nelder-Mead simplex optimization algorithm.

The Nelder-Mead algorithm is a direct search method that uses a simplex
(n+1 vertices in n dimensions) to navigate the parameter space. It uses
reflection, expansion, contraction, and shrinkage operations to adapt
the simplex shape and converge to the optimum.

Features:
- Derivative-free optimization
- Adaptive simplex operations
- Boundary constraint handling
- Convergence detection
- Robust parameter adaptation

#### Source Code

```{literalinclude} ../../../src/optimization/algorithms/gradient_based/nelder_mead.py
:language: python
:pyobject: NelderMead
:linenos:
```

#### Methods (17)

##### `__init__(self, config)`

Initialize Nelder-Mead algorithm.

[View full source →](#method-neldermead-__init__)

##### `optimize(self, problem, parameter_space, initial_guess)`

Run Nelder-Mead optimization.

[View full source →](#method-neldermead-optimize)

##### `_initialize_simplex(self, initial_guess)`

Initialize the simplex.

[View full source →](#method-neldermead-_initialize_simplex)

##### `_perform_iteration(self)`

Perform one iteration of Nelder-Mead algorithm.

[View full source →](#method-neldermead-_perform_iteration)

##### `_reflect(self, centroid, worst_vertex)`

Perform reflection operation.

[View full source →](#method-neldermead-_reflect)

##### `_expand(self, centroid, reflected_point)`

Perform expansion operation.

[View full source →](#method-neldermead-_expand)

##### `_contract_outside(self, centroid, reflected_point)`

Perform outside contraction.

[View full source →](#method-neldermead-_contract_outside)

##### `_contract_inside(self, centroid, worst_vertex)`

Perform inside contraction.

[View full source →](#method-neldermead-_contract_inside)

##### `_shrink_simplex(self)`

Shrink the entire simplex.

[View full source →](#method-neldermead-_shrink_simplex)

##### `_apply_bounds(self, point)`

Apply parameter bounds to a point.

[View full source →](#method-neldermead-_apply_bounds)

##### `_safe_evaluate(self, point)`

Safely evaluate objective function.

[View full source →](#method-neldermead-_safe_evaluate)

##### `_update_adaptive_parameters(self)`

Update adaptive algorithm parameters.

[View full source →](#method-neldermead-_update_adaptive_parameters)

##### `_check_termination(self)`

Check termination conditions.

[View full source →](#method-neldermead-_check_termination)

##### `_create_result(self)`

Create optimization result.

[View full source →](#method-neldermead-_create_result)

##### `get_simplex_info(self)`

Get information about current simplex.

[View full source →](#method-neldermead-get_simplex_info)

##### `_estimate_convergence_rate(self)`

Estimate convergence rate.

[View full source →](#method-neldermead-_estimate_convergence_rate)

##### `restart_simplex(self, perturbation_factor)`

Restart simplex with perturbation.

[View full source →](#method-neldermead-restart_simplex)

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
