# plant.models.simplified.physics

**Source:** `src\plant\models\simplified\physics.py`

## Module Overview

Simplified Physics Computation for DIP.

Focused physics computation module extracted from the monolithic
dynamics implementation. Provides optimized matrix computation
with numerical stability features.

## Complete Source Code

```{literalinclude} ../../../src/plant/models/simplified/physics.py
:language: python
:linenos:
```

---

## Classes

### `SimplifiedPhysicsComputer`

Simplified physics computation for DIP dynamics.

Optimized for computational efficiency while maintaining essential
dynamics characteristics. Uses adaptive regularization for numerical
stability and supports both full and simplified matrix computation.

#### Source Code

```{literalinclude} ../../../src/plant/models/simplified/physics.py
:language: python
:pyobject: SimplifiedPhysicsComputer
:linenos:
```

#### Methods (16)

##### `__init__(self, config)`

Initialize simplified physics computer.

[View full source →](#method-simplifiedphysicscomputer-__init__)

##### `compute_dynamics_rhs(self, state, control_input)`

Compute right-hand side of dynamics equation.

[View full source →](#method-simplifiedphysicscomputer-compute_dynamics_rhs)

##### `get_physics_matrices(self, state)`

Get physics matrices M, C, G for current state.

[View full source →](#method-simplifiedphysicscomputer-get_physics_matrices)

##### `compute_inertia_matrix(self, state)`

Compute inertia matrix M(q).

[View full source →](#method-simplifiedphysicscomputer-compute_inertia_matrix)

##### `compute_coriolis_matrix(self, state)`

Compute Coriolis matrix C(q, q̇).

[View full source →](#method-simplifiedphysicscomputer-compute_coriolis_matrix)

##### `compute_gravity_vector(self, state)`

Compute gravity vector G(q).

[View full source →](#method-simplifiedphysicscomputer-compute_gravity_vector)

##### `compute_total_energy(self, state)`

Compute total energy of the system.

[View full source →](#method-simplifiedphysicscomputer-compute_total_energy)

##### `compute_kinetic_energy(self, state)`

Compute kinetic energy T = (1/2) q̇ᵀ M q̇.

[View full source →](#method-simplifiedphysicscomputer-compute_kinetic_energy)

##### `compute_potential_energy(self, state)`

Compute potential energy V.

[View full source →](#method-simplifiedphysicscomputer-compute_potential_energy)

##### `_compute_kinetic_energy(self, state)`

Internal kinetic energy computation.

[View full source →](#method-simplifiedphysicscomputer-_compute_kinetic_energy)

##### `_compute_potential_energy(self, state)`

Internal potential energy computation.

[View full source →](#method-simplifiedphysicscomputer-_compute_potential_energy)

##### `enable_matrix_caching(self, enable)`

Enable/disable matrix caching for repeated calculations.

[View full source →](#method-simplifiedphysicscomputer-enable_matrix_caching)

##### `clear_matrix_cache(self)`

Clear matrix cache.

[View full source →](#method-simplifiedphysicscomputer-clear_matrix_cache)

##### `set_simplified_inertia(self, use_simplified)`

Enable/disable simplified inertia matrix computation.

[View full source →](#method-simplifiedphysicscomputer-set_simplified_inertia)

##### `get_matrix_conditioning(self, state)`

Get condition number of inertia matrix.

[View full source →](#method-simplifiedphysicscomputer-get_matrix_conditioning)

##### `check_numerical_stability(self, state)`

Check if current state leads to numerically stable computation.

[View full source →](#method-simplifiedphysicscomputer-check_numerical_stability)

---

## Functions

### `compute_simplified_dynamics_numba(state, control_force, m0, m1, m2, L1, L2, Lc1, Lc2, I1, I2, g, c0, c1, c2, reg_alpha, min_reg)`

**Decorators:** `@njit`

JIT-compiled simplified dynamics computation.

Ultra-fast dynamics computation for performance-critical applications.
Uses simplified physics with minimal overhead.

Args:
    state: System state vector
    control_force: Applied control force
    m0, m1, m2: Masses
    L1, L2, Lc1, Lc2: Lengths and COM distances
    I1, I2: Inertias
    g: Gravity
    c0, c1, c2: Friction coefficients
    reg_alpha, min_reg: Regularization parameters

Returns:
    State derivative vector

#### Source Code

```{literalinclude} ../../../src/plant/models/simplified/physics.py
:language: python
:pyobject: compute_simplified_dynamics_numba
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple, Any`
- `import numpy as np`
- `from ...core import DIPPhysicsMatrices, SimplifiedDIPPhysicsMatrices, AdaptiveRegularizer, MatrixInverter, NumericalInstabilityError`
- `from .config import SimplifiedDIPConfig`
