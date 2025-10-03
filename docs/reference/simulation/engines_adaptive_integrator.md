# simulation.engines.adaptive_integrator

**Source:** `src\simulation\engines\adaptive_integrator.py`

## Module Overview

Adaptive Runge–Kutta integrators for state‑space models.

This module implements a Dormand–Prince 4(5) embedded Runge–Kutta step
with error estimation and adaptive step size control.  Embedded
Runge–Kutta pairs compute two solutions of different orders from the
same function evaluations; the difference between the 4th‑ and 5th‑order
approximations provides an estimate of the local truncation error.  By
comparing this error against user‑supplied absolute and relative
tolerances the integrator can accept or reject a proposed step and
adjust the step size accordingly【313837333132264†L58-L82】.  Adaptive
integrators avoid manual tuning of Courant–Friedrichs–Lewy (CFL)
parameters and automatically reduce the step size when the system
exhibits rapid dynamics or near‑singular mass matrices.

The implementation here focuses on a single step of the Dormand–Prince
method.  A higher‑level loop must call :func:`rk45_step` repeatedly
while updating the integration time and state.  If a step is rejected
the returned state will be ``None`` and the caller should retry the
integration with the suggested smaller ``dt``.  When a step is
accepted the integrator proposes a new step size that can be used for
the next call.

The algorithm is described in many numerical analysis textbooks; see
Section III of Shampine and Reichelt for details【313837333132264†L58-L82】.

## Complete Source Code

```{literalinclude} ../../../src/simulation/engines/adaptive_integrator.py
:language: python
:linenos:
```

---

## Functions

### `rk45_step(f, t, y, dt, abs_tol, rel_tol)`

Perform a single Dormand–Prince 4(5) integration step.

Parameters
----------
f : Callable[[float, np.ndarray], np.ndarray]
    Function computing the time derivative of the state ``y`` at time
    ``t``.  The derivative must be a one‑dimensional NumPy array.
t : float
    Current integration time.
y : np.ndarray
    Current state vector.
dt : float
    Proposed step size.
abs_tol : float
    Absolute tolerance for local error control.
rel_tol : float
    Relative tolerance for local error control.

Returns
-------
Tuple[Optional[np.ndarray], float]
    A tuple ``(y_new, dt_new)``.  If the step is accepted then
    ``y_new`` contains the 5th‑order solution at ``t + dt`` and
    ``dt_new`` is a suggested step size for the next step.  If the
    step is rejected then ``y_new`` is ``None`` and ``dt_new`` is a
    smaller step size to retry.

Notes
-----
This implementation uses the Dormand–Prince coefficients for the
classic `RK45` method.  The constants are hard‑coded for clarity
rather than generated programmatically.  See the cited reference
for the Butcher tableau【313837333132264†L58-L82】.

#### Source Code

```{literalinclude} ../../../src/simulation/engines/adaptive_integrator.py
:language: python
:pyobject: rk45_step
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable, Tuple, Optional`
- `import numpy as np`
