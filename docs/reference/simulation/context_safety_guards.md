# simulation.context.safety_guards

**Source:** `src\simulation\context\safety_guards.py`

## Module Overview

Vectorized safety guard functions for simulation.

These helpers implement pure checks on state tensors.  They operate on
scalars, vectors or batched vectors (any shape with the last axis as the state
dimension) and raise informative RuntimeError exceptions when invariants are
violated.  The error messages contain frozen substrings which are matched
exactly in the acceptance tests; do not modify the substrings.

## Complete Source Code

```{literalinclude} ../../../src/simulation/context/safety_guards.py
:language: python
:linenos:
```

---

## Functions

### `_guard_no_nan(state, step_idx)`

Raise if ``state`` contains any non‑finite values.

Parameters
----------
state : array-like
    State array of shape ``(..., D)``.  Can be scalar or batched.
step_idx : int
    Index of the current step (for reporting purposes).

Raises
------
RuntimeError
    If any element of ``state`` is NaN or infinite.  The message
    contains the frozen substring ``"NaN detected in state at step <i>"``
    followed by the actual step index.

#### Source Code

```{literalinclude} ../../../src/simulation/context/safety_guards.py
:language: python
:pyobject: _guard_no_nan
:linenos:
```

---

### `_guard_energy(state, limits)`

Check that the total energy of ``state`` does not exceed a maximum.

Energy is defined as the sum of squares of the state variables
``sum(state**2, axis=-1)``.  When any batch element exceeds the
configured maximum, a RuntimeError is raised.  The message contains
the frozen substring ``"Energy check failed: total_energy=<val> exceeds <max>"``.

Parameters
----------
state : array-like
    State array of shape ``(..., D)``.  Scalars and batches are allowed.
limits : dict or None
    Must contain the key ``"max"`` specifying the maximum allowed total
    energy.  If ``limits`` is ``None`` or missing the key, this check
    silently returns.

#### Source Code

```{literalinclude} ../../../src/simulation/context/safety_guards.py
:language: python
:pyobject: _guard_energy
:linenos:
```

---

### `_guard_bounds(state, bounds, t)`

Check that ``state`` lies within elementwise bounds.

Parameters
----------
state : array-like
    State array of shape ``(..., D)``.
bounds : tuple or None
    A pair ``(lower, upper)`` specifying inclusive bounds.  Each may be
    a scalar, an array broadcastable to ``state``, or ``None`` to
    disable that side of the bound.
t : float
    Simulation time (for error reporting).

Raises
------
RuntimeError
    If any element of ``state`` falls outside the specified bounds.
    The message contains the frozen substring ``"State bounds violated at t=<t>"``.

#### Source Code

```{literalinclude} ../../../src/simulation/context/safety_guards.py
:language: python
:pyobject: _guard_bounds
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import numpy as np`
- `from typing import Any, Tuple, Optional, Dict`
