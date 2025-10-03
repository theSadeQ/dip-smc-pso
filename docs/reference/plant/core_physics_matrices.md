# plant.core.physics_matrices

**Source:** `src\plant\core\physics_matrices.py`

## Module Overview

Physics Matrix Computation for DIP Systems.

Provides focused components for computing the fundamental physics matrices:
- Inertia Matrix (M): Mass and inertial properties
- Coriolis Matrix (C): Velocity-dependent forces
- Gravity Vector (G): Gravitational forces

Split from monolithic dynamics for clarity, testability, and reusability.

## Complete Source Code

```{literalinclude} ../../../src/plant/core/physics_matrices.py
:language: python
:linenos:
```

---

## Classes

### `PhysicsMatrixComputer`

**Inherits from:** `Protocol`

Protocol for physics matrix computation.

#### Source Code

```{literalinclude} ../../../src/plant/core/physics_matrices.py
:language: python
:pyobject: PhysicsMatrixComputer
:linenos:
```

#### Methods (3)

##### `compute_inertia_matrix(self, state)`

Compute inertia matrix M(q).

[View full source →](#method-physicsmatrixcomputer-compute_inertia_matrix)

##### `compute_coriolis_matrix(self, state)`

Compute Coriolis matrix C(q, q̇).

[View full source →](#method-physicsmatrixcomputer-compute_coriolis_matrix)

##### `compute_gravity_vector(self, state)`

Compute gravity vector G(q).

[View full source →](#method-physicsmatrixcomputer-compute_gravity_vector)

---

### `DIPPhysicsMatrices`

Double Inverted Pendulum physics matrix computation.

Encapsulates the mathematical computation of fundamental physics matrices
for the DIP system. Uses numerical optimizations (JIT compilation) for
performance while maintaining clear mathematical structure.

#### Source Code

```{literalinclude} ../../../src/plant/core/physics_matrices.py
:language: python
:pyobject: DIPPhysicsMatrices
:linenos:
```

#### Methods (8)

##### `__init__(self, parameters)`

Initialize physics matrix computer.

[View full source →](#method-dipphysicsmatrices-__init__)

##### `compute_inertia_matrix(self, state)`

Compute the inertia matrix M(q) for the DIP system.

[View full source →](#method-dipphysicsmatrices-compute_inertia_matrix)

##### `compute_coriolis_matrix(self, state)`

Compute the Coriolis matrix C(q, q̇) for the DIP system.

[View full source →](#method-dipphysicsmatrices-compute_coriolis_matrix)

##### `compute_gravity_vector(self, state)`

Compute the gravity vector G(q) for the DIP system.

[View full source →](#method-dipphysicsmatrices-compute_gravity_vector)

##### `compute_all_matrices(self, state)`

Compute all physics matrices in a single call for efficiency.

[View full source →](#method-dipphysicsmatrices-compute_all_matrices)

##### `_compute_inertia_matrix_numba(theta1, theta2, m0, m1, m2, L1, L2, Lc1, Lc2, I1, I2)`

JIT-compiled inertia matrix computation.

[View full source →](#method-dipphysicsmatrices-_compute_inertia_matrix_numba)

##### `_compute_coriolis_matrix_numba(theta1, theta2, theta1_dot, theta2_dot, m1, m2, L1, L2, Lc1, Lc2, c0, c1, c2)`

JIT-compiled Coriolis matrix computation.

[View full source →](#method-dipphysicsmatrices-_compute_coriolis_matrix_numba)

##### `_compute_gravity_vector_numba(theta1, theta2, m1, m2, L1, Lc1, Lc2, g)`

JIT-compiled gravity vector computation.

[View full source →](#method-dipphysicsmatrices-_compute_gravity_vector_numba)

---

### `SimplifiedDIPPhysicsMatrices`

**Inherits from:** `DIPPhysicsMatrices`

Simplified physics matrices for computational efficiency.

Uses approximations and simplifications suitable for control design
while maintaining essential dynamics characteristics.

#### Source Code

```{literalinclude} ../../../src/plant/core/physics_matrices.py
:language: python
:pyobject: SimplifiedDIPPhysicsMatrices
:linenos:
```

#### Methods (2)

##### `compute_inertia_matrix(self, state)`

Simplified inertia matrix with reduced coupling terms.

[View full source →](#method-simplifieddipphysicsmatrices-compute_inertia_matrix)

##### `_compute_simplified_inertia_matrix_numba(theta1, theta2, m0, m1, m2, L1, L2, Lc1, Lc2, I1, I2)`

Simplified inertia matrix computation.

[View full source →](#method-simplifieddipphysicsmatrices-_compute_simplified_inertia_matrix_numba)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple, Protocol, Any`
- `import numpy as np`
