# plant.core.numerical_stability

**Source:** `src\plant\core\numerical_stability.py`

## Module Overview

Numerical Stability Utilities for Plant Dynamics.

Provides robust numerical methods for:
- Matrix conditioning and regularization
- Singular value analysis
- Adaptive regularization schemes
- Numerical instability detection

Extracted from monolithic dynamics for focused responsibility and testing.

## Complete Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:linenos:
```

---

## Classes

### `NumericalInstabilityError`

**Inherits from:** `RuntimeError`

Raised when numerical computation becomes unstable.

This exception indicates that the system matrices are too ill-conditioned
for reliable numerical computation, typically due to near-singular
inertia matrices or extreme parameter values.

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: NumericalInstabilityError
:linenos:
```

---

### `MatrixRegularizer`

**Inherits from:** `Protocol`

Protocol for matrix regularization strategies.

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: MatrixRegularizer
:linenos:
```

#### Methods (2)

##### `regularize_matrix(self, matrix)`

Apply regularization to improve matrix conditioning.

[View full source →](#method-matrixregularizer-regularize_matrix)

##### `check_conditioning(self, matrix)`

Check if matrix conditioning is acceptable.

[View full source →](#method-matrixregularizer-check_conditioning)

---

### `AdaptiveRegularizer`

Adaptive matrix regularization for improved numerical stability.

Uses Tikhonov regularization with adaptive damping based on matrix
conditioning. Provides robust matrix inversion for dynamics computation.

Mathematical Background:
- Adds λI to matrix diagonal where λ is adaptive damping parameter
- λ scales with largest singular value and condition number
- Prevents numerical instability while minimizing bias

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: AdaptiveRegularizer
:linenos:
```

#### Methods (5)

##### `__init__(self, regularization_alpha, max_condition_number, min_regularization, use_fixed_regularization)`

Initialize adaptive regularizer.

[View full source →](#method-adaptiveregularizer-__init__)

##### `regularize_matrix(self, matrix)`

Apply adaptive regularization to improve matrix conditioning.

[View full source →](#method-adaptiveregularizer-regularize_matrix)

##### `check_conditioning(self, matrix)`

Check if matrix conditioning is acceptable.

[View full source →](#method-adaptiveregularizer-check_conditioning)

##### `_apply_fixed_regularization(self, matrix)`

Apply fixed regularization with minimum damping.

[View full source →](#method-adaptiveregularizer-_apply_fixed_regularization)

##### `_apply_adaptive_regularization(self, matrix)`

Apply adaptive regularization based on matrix conditioning.

[View full source →](#method-adaptiveregularizer-_apply_adaptive_regularization)

---

### `MatrixInverter`

Robust matrix inversion with numerical stability checks.

Provides multiple inversion strategies with fallback mechanisms
for reliable computation of matrix inverses in dynamics.

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: MatrixInverter
:linenos:
```

#### Methods (3)

##### `__init__(self, regularizer)`

Initialize matrix inverter.

[View full source →](#method-matrixinverter-__init__)

##### `invert_matrix(self, matrix)`

Robustly invert matrix with regularization if needed.

[View full source →](#method-matrixinverter-invert_matrix)

##### `solve_linear_system(self, A, b)`

Solve linear system Ax = b with numerical stability.

[View full source →](#method-matrixinverter-solve_linear_system)

---

### `NumericalStabilityMonitor`

Monitor numerical stability during dynamics computation.

Tracks conditioning, regularization frequency, and stability metrics
for debugging and performance optimization.

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: NumericalStabilityMonitor
:linenos:
```

#### Methods (4)

##### `__init__(self)`

Initialize stability monitor.

[View full source →](#method-numericalstabilitymonitor-__init__)

##### `reset_statistics(self)`

Reset monitoring statistics.

[View full source →](#method-numericalstabilitymonitor-reset_statistics)

##### `record_inversion(self, condition_number, was_regularized, failed)`

Record matrix inversion statistics.

[View full source →](#method-numericalstabilitymonitor-record_inversion)

##### `get_statistics(self)`

Get numerical stability statistics.

[View full source →](#method-numericalstabilitymonitor-get_statistics)

---

## Functions

### `fast_condition_estimate(matrix)`

**Decorators:** `@njit`

Fast condition number estimation using determinant ratio.

Provides a lightweight alternative to full SVD for condition checking
in performance-critical code paths.

Args:
    matrix: Matrix to analyze

Returns:
    Approximate condition number estimate

#### Source Code

```{literalinclude} ../../../src/plant/core/numerical_stability.py
:language: python
:pyobject: fast_condition_estimate
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple, Optional, Protocol`
- `import numpy as np`
- `import warnings`
