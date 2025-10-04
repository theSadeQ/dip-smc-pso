# plant.core.state_validation

**Source:** `src\plant\core\state_validation.py`

## Module Overview

State Vector Validation for Plant Dynamics.

Provides comprehensive validation and sanitization of system states:
- State vector format validation
- Physical bounds checking
- Numerical validity verification
- Constraint enforcement

Ensures robust dynamics computation by catching invalid states early.

## Complete Source Code

```{literalinclude} ../../../src/plant/core/state_validation.py
:language: python
:linenos:
```

---

## Classes

### `StateValidationError`

**Inherits from:** `ValueError`

Raised when state vector validation fails.

#### Source Code

```{literalinclude} ../../../src/plant/core/state_validation.py
:language: python
:pyobject: StateValidationError
:linenos:
```

---

### `StateValidator`

**Inherits from:** `Protocol`

Protocol for state validation strategies.

#### Source Code

```{literalinclude} ../../../src/plant/core/state_validation.py
:language: python
:pyobject: StateValidator
:linenos:
```

#### Methods (2)

##### `validate_state(self, state)`

Validate state vector.

[View full source →](#method-statevalidator-validate_state)

##### `sanitize_state(self, state)`

Sanitize and correct state vector if possible.

[View full source →](#method-statevalidator-sanitize_state)

---

### `DIPStateValidator`

Double Inverted Pendulum state vector validation.

Validates state vectors for the DIP system ensuring:
- Correct dimensionality (6-element vectors)
- Physical bounds on positions and velocities
- Numerical validity (no NaN/inf values)
- Angular wrapping and constraint enforcement

#### Source Code

```{literalinclude} ../../../src/plant/core/state_validation.py
:language: python
:pyobject: DIPStateValidator
:linenos:
```

#### Methods (14)

##### `__init__(self, position_bounds, angle_bounds, velocity_bounds, angular_velocity_bounds, wrap_angles, strict_validation)`

Initialize DIP state validator.

[View full source →](#method-dipstatevalidator-__init__)

##### `validate_state(self, state)`

Validate complete state vector.

[View full source →](#method-dipstatevalidator-validate_state)

##### `sanitize_state(self, state)`

Sanitize state vector to ensure validity.

[View full source →](#method-dipstatevalidator-sanitize_state)

##### `get_state_info(self, state)`

Get detailed information about state vector.

[View full source →](#method-dipstatevalidator-get_state_info)

##### `reset_statistics(self)`

Reset validation statistics.

[View full source →](#method-dipstatevalidator-reset_statistics)

##### `get_statistics(self)`

Get validation statistics.

[View full source →](#method-dipstatevalidator-get_statistics)

##### `_check_state_structure(self, state)`

Check if state has correct structure.

[View full source →](#method-dipstatevalidator-_check_state_structure)

##### `_check_numerical_validity(self, state)`

Check if state contains valid numerical values.

[View full source →](#method-dipstatevalidator-_check_numerical_validity)

##### `_check_physical_bounds(self, state)`

Check if state is within physical bounds.

[View full source →](#method-dipstatevalidator-_check_physical_bounds)

##### `_fix_numerical_issues(self, state)`

Fix numerical issues in state vector.

[View full source →](#method-dipstatevalidator-_fix_numerical_issues)

##### `_apply_physical_bounds(self, state)`

Apply physical bounds to state vector.

[View full source →](#method-dipstatevalidator-_apply_physical_bounds)

##### `_wrap_angles(self, angles)`

Wrap angles to [-π, π] range.

[View full source →](#method-dipstatevalidator-_wrap_angles)

##### `_estimate_energy(self, state)`

Estimate total system energy (rough approximation).

[View full source →](#method-dipstatevalidator-_estimate_energy)

##### `_estimate_angular_momentum(self, state)`

Estimate total angular momentum (rough approximation).

[View full source →](#method-dipstatevalidator-_estimate_angular_momentum)

---

### `MinimalStateValidator`

Minimal state validator for performance-critical applications.

Provides only essential validation with minimal overhead.

#### Source Code

```{literalinclude} ../../../src/plant/core/state_validation.py
:language: python
:pyobject: MinimalStateValidator
:linenos:
```

#### Methods (2)

##### `validate_state(self, state)`

Fast basic validation.

[View full source →](#method-minimalstatevalidator-validate_state)

##### `sanitize_state(self, state)`

Minimal sanitization.

[View full source →](#method-minimalstatevalidator-sanitize_state)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple, Optional, Protocol, Dict, Any`
- `import numpy as np`
- `import warnings`
