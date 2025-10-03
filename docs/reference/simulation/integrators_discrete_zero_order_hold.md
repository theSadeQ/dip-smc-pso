# simulation.integrators.discrete.zero_order_hold

**Source:** `src\simulation\integrators\discrete\zero_order_hold.py`

## Module Overview

Zero-order hold discretization for discrete-time simulation.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/discrete/zero_order_hold.py
:language: python
:linenos:
```

---

## Classes

### `ZeroOrderHold`

**Inherits from:** `BaseIntegrator`

Zero-order hold discretization for linear and linearized systems.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/discrete/zero_order_hold.py
:language: python
:pyobject: ZeroOrderHold
:linenos:
```

#### Methods (9)

##### `__init__(self, A, B, dt)`

Initialize ZOH discretization.

[View full source →](#method-zeroorderhold-__init__)

##### `order(self)`

Integration method order (exact for linear systems).

[View full source →](#method-zeroorderhold-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-zeroorderhold-adaptive)

##### `set_linear_system(self, A, B, dt)`

Set linear system matrices and compute discrete-time equivalent.

[View full source →](#method-zeroorderhold-set_linear_system)

##### `_compute_discrete_matrices(self)`

Compute discrete-time matrices using matrix exponential.

[View full source →](#method-zeroorderhold-_compute_discrete_matrices)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using zero-order hold discretization.

[View full source →](#method-zeroorderhold-integrate)

##### `_integrate_nonlinear(self, dynamics_fn, state, control, dt, t)`

Integrate nonlinear system with ZOH control approximation.

[View full source →](#method-zeroorderhold-_integrate_nonlinear)

##### `get_discrete_matrices(self)`

Get computed discrete-time matrices.

[View full source →](#method-zeroorderhold-get_discrete_matrices)

##### `simulate_discrete_sequence(self, initial_state, control_sequence, horizon)`

Simulate discrete-time system for multiple steps.

[View full source →](#method-zeroorderhold-simulate_discrete_sequence)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable, Optional`
- `import numpy as np`
- `from scipy.linalg import expm`
- `from ..base import BaseIntegrator`
