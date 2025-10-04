# simulation.integrators.adaptive.runge_kutta

**Source:** `src\simulation\integrators\adaptive\runge_kutta.py`

## Module Overview

Adaptive Runge-Kutta integration methods with error control.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/runge_kutta.py
:language: python
:linenos:
```

---

## Classes

### `AdaptiveRungeKutta`

**Inherits from:** `BaseIntegrator`

Base class for adaptive Runge-Kutta methods.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/runge_kutta.py
:language: python
:pyobject: AdaptiveRungeKutta
:linenos:
```

#### Methods (4)

##### `__init__(self, rtol, atol, min_step, max_step, safety_factor)`

Initialize adaptive Runge-Kutta integrator.

[View full source →](#method-adaptiverungekutta-__init__)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-adaptiverungekutta-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate dynamics with adaptive step size.

[View full source →](#method-adaptiverungekutta-integrate)

##### `_adaptive_step(self, f, t, y, dt)`

Perform one adaptive integration step.

[View full source →](#method-adaptiverungekutta-_adaptive_step)

---

### `DormandPrince45`

**Inherits from:** `AdaptiveRungeKutta`

Dormand-Prince 4(5) embedded Runge-Kutta method with adaptive step size.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/runge_kutta.py
:language: python
:pyobject: DormandPrince45
:linenos:
```

#### Methods (2)

##### `order(self)`

Integration method order.

[View full source →](#method-dormandprince45-order)

##### `_adaptive_step(self, f, t, y, dt)`

Perform single Dormand-Prince 4(5) step with error control.

[View full source →](#method-dormandprince45-_adaptive_step)

---

## Functions

### `rk45_step(f, t, y, dt, abs_tol, rel_tol)`

Legacy Dormand-Prince 4(5) step function for backward compatibility.

Parameters
----------
f : callable
    Function computing time derivative dy/dt = f(t, y)
t : float
    Current integration time
y : np.ndarray
    Current state vector
dt : float
    Proposed step size
abs_tol : float
    Absolute tolerance for error control
rel_tol : float
    Relative tolerance for error control

Returns
-------
tuple
    (y_new, dt_new) where y_new is None if step rejected

Notes
-----
This function maintains backward compatibility with the original
adaptive_integrator.py implementation.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/runge_kutta.py
:language: python
:pyobject: rk45_step
:linenos:
```

---

### `_original_rk45_step(f, t, y, dt, abs_tol, rel_tol)`

Original RK45 implementation for fallback.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/runge_kutta.py
:language: python
:pyobject: _original_rk45_step
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable, Optional, Tuple`
- `import numpy as np`
- `from ..base import BaseIntegrator, IntegrationResult`
- `from .error_control import ErrorController`
