# analysis.performance.control_analysis

**Source:** `src\analysis\performance\control_analysis.py`

## Module Overview

Linearisation and controllability/observability analysis utilities.

This module exposes helper functions to linearise the double inverted
pendulum dynamics at an equilibrium point and to construct the
controllability and observability matrices for a linear time‑invariant
(LTI) system.  The Kalman rank criterion states that an LTI system is
controllable if and only if its controllability matrix has full rank
equal to the number of state variables【920100172589331†L79-L84】.  An
analogous condition holds for observability.  These functions aid in
assessing whether a given linearised model is suitable for state‐space
control or estimation design.

## Complete Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:linenos:
```

---

## Classes

### `ControlAnalyzer`

Control analysis utilities for linearization and controllability assessment.

This class provides a convenient interface to control-theoretic analysis
functions including linearization, controllability, and observability analysis.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:pyobject: ControlAnalyzer
:linenos:
```

#### Methods (6)

##### `__init__(self)`

Initialize the control analyzer.

[View full source →](#method-controlanalyzer-__init__)

##### `linearize_dynamics(dyn, x_eq, u_eq)`

Linearize nonlinear dynamics around equilibrium point.

[View full source →](#method-controlanalyzer-linearize_dynamics)

##### `controllability_matrix(A, B)`

Compute controllability matrix for LTI system.

[View full source →](#method-controlanalyzer-controllability_matrix)

##### `observability_matrix(A, C)`

Compute observability matrix for LTI system.

[View full source →](#method-controlanalyzer-observability_matrix)

##### `is_controllable(self, A, B)`

Check if system is controllable using rank test.

[View full source →](#method-controlanalyzer-is_controllable)

##### `is_observable(self, A, C)`

Check if system is observable using rank test.

[View full source →](#method-controlanalyzer-is_observable)

---

## Functions

### `linearize_dip(dyn, x_eq, u_eq)`

Linearise the nonlinear dynamics around an equilibrium point.

Parameters
----------
dyn : callable
    A function implementing the continuous‑time dynamics ``f(x, u)``.
x_eq : np.ndarray
    Equilibrium state vector at which to linearise.
u_eq : float
    Equilibrium control input.

Returns
-------
(A, B) : tuple of np.ndarray
    Continuous‑time state matrix ``A`` and input matrix ``B`` obtained
    via numerical differentiation of the dynamics.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:pyobject: linearize_dip
:linenos:
```

---

### `controllability_matrix(A, B)`

Construct the controllability matrix of an LTI system.

For an ``n``‑state system described by matrices ``A`` and ``B``, the
controllability matrix is defined as ``[B, AB, A^2B, …, A^{n-1}B]``.
The system is controllable if this matrix has full row rank equal to ``n``【920100172589331†L79-L84】.

Parameters
----------
A : np.ndarray
    State transition matrix of shape ``(n, n)``.
B : np.ndarray
    Input matrix of shape ``(n, m)``.

Returns
-------
np.ndarray
    The controllability matrix of shape ``(n, n*m)``.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:pyobject: controllability_matrix
:linenos:
```

---

### `observability_matrix(A, C)`

Construct the observability matrix of an LTI system.

Given output matrix ``C`` of shape ``(p, n)``, the observability
matrix is ``[C; CA; CA^2; …; CA^{n-1}]``.  The system is observable
when this matrix has full column rank equal to ``n``【920100172589331†L79-L84】.

Parameters
----------
A : np.ndarray
    State transition matrix of shape ``(n, n)``.
C : np.ndarray
    Output matrix of shape ``(p, n)``.

Returns
-------
np.ndarray
    Observability matrix of shape ``(p*n, n)``.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:pyobject: observability_matrix
:linenos:
```

---

### `check_controllability_observability(A, B, C)`

Check controllability and observability of an LTI system.

Parameters
----------
A : np.ndarray
    State transition matrix ``(n, n)``.
B : np.ndarray
    Input matrix ``(n, m)``.
C : np.ndarray
    Output matrix ``(p, n)``.

Returns
-------
(bool, bool)
    Tuple ``(is_controllable, is_observable)``.  ``True`` when the
    corresponding rank test passes【920100172589331†L79-L84】.

#### Source Code

```{literalinclude} ../../../src/analysis/performance/control_analysis.py
:language: python
:pyobject: check_controllability_observability
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple`
- `import numpy as np`
- `from src.controllers.mpc_controller import _numeric_linearize_continuous`
