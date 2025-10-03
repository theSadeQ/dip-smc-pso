# simulation.safety.guards

**Source:** `src\simulation\safety\guards.py`

## Module Overview

Enhanced safety guard functions for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:linenos:
```

---

## Classes

### `SafetyViolationError`

**Inherits from:** `RuntimeError`

Exception raised when safety constraints are violated.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: SafetyViolationError
:linenos:
```

#### Methods (1)

##### `__init__(self, message, violation_type, step_idx)`

Initialize safety violation error.

[View full source →](#method-safetyviolationerror-__init__)

---

### `NaNGuard`

**Inherits from:** `SafetyGuard`

Guard against NaN and infinite values in state.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: NaNGuard
:linenos:
```

#### Methods (2)

##### `check(self, state, step_idx)`

Check for NaN/infinite values.

[View full source →](#method-nanguard-check)

##### `get_violation_message(self)`

Get violation message.

[View full source →](#method-nanguard-get_violation_message)

---

### `EnergyGuard`

**Inherits from:** `SafetyGuard`

Guard against excessive system energy.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: EnergyGuard
:linenos:
```

#### Methods (3)

##### `__init__(self, max_energy)`

Initialize energy guard.

[View full source →](#method-energyguard-__init__)

##### `check(self, state, step_idx)`

Check energy constraint.

[View full source →](#method-energyguard-check)

##### `get_violation_message(self)`

Get violation message.

[View full source →](#method-energyguard-get_violation_message)

---

### `BoundsGuard`

**Inherits from:** `SafetyGuard`

Guard against state bounds violations.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: BoundsGuard
:linenos:
```

#### Methods (3)

##### `__init__(self, lower_bounds, upper_bounds)`

Initialize bounds guard.

[View full source →](#method-boundsguard-__init__)

##### `check(self, state, step_idx)`

Check bounds constraint.

[View full source →](#method-boundsguard-check)

##### `get_violation_message(self)`

Get violation message.

[View full source →](#method-boundsguard-get_violation_message)

---

### `SafetyGuardManager`

Manager for multiple safety guards.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: SafetyGuardManager
:linenos:
```

#### Methods (4)

##### `__init__(self)`

Initialize safety guard manager.

[View full source →](#method-safetyguardmanager-__init__)

##### `add_guard(self, guard)`

Add a safety guard.

[View full source →](#method-safetyguardmanager-add_guard)

##### `check_all(self, state, step_idx)`

Check all safety guards.

[View full source →](#method-safetyguardmanager-check_all)

##### `clear_guards(self)`

Clear all safety guards.

[View full source →](#method-safetyguardmanager-clear_guards)

---

## Functions

### `guard_no_nan(state, step_idx)`

Check for NaN/infinite values (legacy interface).

Parameters
----------
state : array-like
    State array
step_idx : int
    Current step index

Raises
------
SafetyViolationError
    If NaN/infinite values detected

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: guard_no_nan
:linenos:
```

---

### `guard_energy(state, limits)`

Check energy constraint (legacy interface).

Parameters
----------
state : array-like
    State array
limits : dict or None
    Energy limits with 'max' key

Raises
------
SafetyViolationError
    If energy constraint violated

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: guard_energy
:linenos:
```

---

### `guard_bounds(state, bounds, t)`

Check bounds constraint (legacy interface).

Parameters
----------
state : array-like
    State array
bounds : tuple or None
    (lower, upper) bounds
t : float
    Current time

Raises
------
SafetyViolationError
    If bounds violated

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: guard_bounds
:linenos:
```

---

### `apply_safety_guards(state, step_idx, config)`

Apply all configured safety guards.

Parameters
----------
state : np.ndarray
    Current state vector
step_idx : int
    Current simulation step
config : Any
    Configuration object with safety settings

Raises
------
SafetyViolationError
    If any safety guard is violated

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: apply_safety_guards
:linenos:
```

---

### `create_default_guards(config)`

Create default safety guards from configuration.

Parameters
----------
config : Any
    Configuration object

Returns
-------
SafetyGuardManager
    Configured safety guard manager

#### Source Code

```{literalinclude} ../../../src/simulation/safety/guards.py
:language: python
:pyobject: create_default_guards
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import numpy as np`
- `from typing import Any, Tuple, Optional, Dict, Union`
- `from ..core.interfaces import SafetyGuard`
