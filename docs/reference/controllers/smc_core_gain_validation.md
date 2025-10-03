# controllers.smc.core.gain_validation

**Source:** `src\controllers\smc\core\gain_validation.py`

## Module Overview

Gain Validation for SMC Controllers.

Provides centralized validation logic for SMC controller parameters.
Ensures gains satisfy stability requirements from sliding mode theory.

Mathematical Requirements:
- Surface gains (k1, k2, λ1, λ2) must be positive for Hurwitz stability
- Switching gains (K) must be positive to guarantee reaching condition
- Derivative gains (kd) must be non-negative for damping
- Adaptation gains must satisfy boundedness conditions

## Complete Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:linenos:
```

---

## Classes

### `SMCControllerType`

**Inherits from:** `Enum`

SMC controller types with different gain requirements.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: SMCControllerType
:linenos:
```

---

### `GainBounds`

Bounds for SMC controller gains.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: GainBounds
:linenos:
```

#### Methods (1)

##### `validate(self, value)`

Check if value is within bounds.

[View full source →](#method-gainbounds-validate)

---

### `SMCGainValidator`

Centralized gain validation for all SMC controller types.

Provides type-specific validation rules based on SMC theory requirements.

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: SMCGainValidator
:linenos:
```

#### Methods (6)

##### `__init__(self)`

Initialize gain validator with standard bounds.

[View full source →](#method-smcgainvalidator-__init__)

##### `_initialize_standard_bounds(self)`

Initialize standard gain bounds for each controller type.

[View full source →](#method-smcgainvalidator-_initialize_standard_bounds)

##### `validate_gains(self, gains, controller_type)`

Validate gains for specific SMC controller type.

[View full source →](#method-smcgainvalidator-validate_gains)

##### `validate_stability_conditions(self, gains, controller_type)`

Validate SMC-specific stability conditions.

[View full source →](#method-smcgainvalidator-validate_stability_conditions)

##### `get_recommended_ranges(self, controller_type)`

Get recommended gain ranges for controller type.

[View full source →](#method-smcgainvalidator-get_recommended_ranges)

##### `update_bounds(self, controller_type, gain_name, min_val, max_val)`

Update gain bounds for specific controller and gain.

[View full source →](#method-smcgainvalidator-update_bounds)

---

## Functions

### `validate_smc_gains(gains, controller_type)`

Quick validation of SMC gains.

Args:
    gains: Gain values
    controller_type: Type of SMC controller

Returns:
    True if gains are valid, False otherwise

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: validate_smc_gains
:linenos:
```

---

### `check_stability_conditions(gains, controller_type)`

Quick check of SMC stability conditions.

Args:
    gains: Gain values
    controller_type: Type of SMC controller

Returns:
    True if stability conditions are satisfied, False otherwise

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: check_stability_conditions
:linenos:
```

---

### `get_gain_bounds_for_controller(controller_type)`

Get gain bounds for specific controller type.

Args:
    controller_type: Type of SMC controller

Returns:
    Dictionary of gain bounds

#### Source Code

```{literalinclude} ../../../src/controllers/smc/core/gain_validation.py
:language: python
:pyobject: get_gain_bounds_for_controller
:linenos:
```

---

## Dependencies

This module imports:

- `from typing import List, Union, Dict, Optional, Sequence`
- `import numpy as np`
- `from dataclasses import dataclass`
- `from enum import Enum`
