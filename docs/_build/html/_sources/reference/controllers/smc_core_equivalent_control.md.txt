# controllers.smc.core.equivalent_control

**Source:** `src\controllers\smc\core\equivalent_control.py`

## Module Overview

Equivalent Control Computation for SMC Controllers.

Implements model-based equivalent control (u_eq) that drives the system along
the sliding surface. This is the feedforward component of SMC that provides
nominal performance when the model is accurate.

Mathematical Background:
- Equivalent control: u_eq = -(LM^{-1}B)^{-1} * LM^{-1}F
- Where: M = inertia matrix, F = nonlinear forces, L = surface gradient, B = input matrix
- Requires dynamics model and assumes controllability: |LM^{-1}B| > threshold

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/core/equivalent_control.py
:language: python
:linenos:
```

---

## Classes

### `EquivalentControl`

Model-based equivalent control computation for SMC.

Computes the control input that would maintain the system exactly on the
sliding surface if the model were perfect and no disturbances were present.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/equivalent_control.py
:language: python
:pyobject: EquivalentControl
:linenos:
```

#### Methods (7)

##### `__init__(self, dynamics_model, regularization, regularization_alpha, min_regularization, max_condition_number, use_fixed_regularization, controllability_threshold)`

Initialize equivalent control computation.

[View full source →](#method-equivalentcontrol-__init__)

##### `compute(self, state, sliding_surface, surface_derivative)`

Compute equivalent control input.

[View full source →](#method-equivalentcontrol-compute)

##### `_extract_dynamics_matrices(self, state)`

Extract inertia matrix M and force vector F from dynamics model.

[View full source →](#method-equivalentcontrol-_extract_dynamics_matrices)

##### `_get_surface_gradient(self, sliding_surface)`

Get surface gradient L from sliding surface object.

[View full source →](#method-equivalentcontrol-_get_surface_gradient)

##### `check_controllability(self, state, sliding_surface)`

Analyze system controllability at current state.

[View full source →](#method-equivalentcontrol-check_controllability)

##### `set_controllability_threshold(self, threshold)`

Update controllability threshold.

[View full source →](#method-equivalentcontrol-set_controllability_threshold)

##### `get_dynamics_info(self, state)`

Get information about dynamics matrices at current state.

[View full source →](#method-equivalentcontrol-get_dynamics_info)

---

## Dependencies

This module imports:

- `from typing import Optional, Any, Tuple`
- `import numpy as np`
- `import logging`
- `from abc import ABC, abstractmethod`
- `from src.plant.core.numerical_stability import MatrixInverter, AdaptiveRegularizer`
