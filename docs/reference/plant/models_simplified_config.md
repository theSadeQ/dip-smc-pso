# plant.models.simplified.config

**Source:** `src\plant\models\simplified\config.py`

## Module Overview

Configuration for Simplified DIP Dynamics.

Type-safe configuration with validation for the simplified double
inverted pendulum model. Ensures physical consistency and provides
mathematical constraints based on mechanical engineering principles.

## Complete Source Code

```{literalinclude} ../../../src/plant/models/simplified/config.py
:language: python
:linenos:
```

---

## Classes

### `SimplifiedDIPConfig`

Type-safe configuration for simplified DIP dynamics.

Physical Parameters:
- All masses must be positive (physical requirement)
- All lengths must be positive (geometric requirement)
- Friction coefficients must be non-negative (energy dissipation)
- Inertias must be positive (rotational mass distribution)

Numerical Parameters:
- Regularization ensures matrix invertibility
- Condition number bounds prevent numerical instability

#### Source Code

```{literalinclude} ../../../src/plant/models/simplified/config.py
:language: python
:pyobject: SimplifiedDIPConfig
:linenos:
```

#### Methods (13)

##### `__post_init__(self)`

Validate configuration after creation.

[View full source →](#method-simplifieddipconfig-__post_init__)

##### `_validate_physical_parameters(self)`

Validate physical parameters for consistency.

[View full source →](#method-simplifieddipconfig-_validate_physical_parameters)

##### `_validate_numerical_parameters(self)`

Validate numerical parameters for stability.

[View full source →](#method-simplifieddipconfig-_validate_numerical_parameters)

##### `_validate_geometric_constraints(self)`

Validate geometric constraints between parameters.

[View full source →](#method-simplifieddipconfig-_validate_geometric_constraints)

##### `create_default(cls)`

Create configuration with sensible default parameters.

[View full source →](#method-simplifieddipconfig-create_default)

##### `create_benchmark(cls)`

Create configuration for benchmark/comparison studies.

[View full source →](#method-simplifieddipconfig-create_benchmark)

##### `create_lightweight(cls)`

Create configuration optimized for computational speed.

[View full source →](#method-simplifieddipconfig-create_lightweight)

##### `to_dict(self)`

Convert configuration to dictionary.

[View full source →](#method-simplifieddipconfig-to_dict)

##### `from_dict(cls, config_dict)`

Create configuration from dictionary.

[View full source →](#method-simplifieddipconfig-from_dict)

##### `get_total_mass(self)`

Get total system mass.

[View full source →](#method-simplifieddipconfig-get_total_mass)

##### `get_characteristic_length(self)`

Get characteristic length scale of the system.

[View full source →](#method-simplifieddipconfig-get_characteristic_length)

##### `get_characteristic_time(self)`

Get characteristic time scale for oscillations.

[View full source →](#method-simplifieddipconfig-get_characteristic_time)

##### `estimate_natural_frequency(self)`

Estimate natural frequency for small oscillations.

[View full source →](#method-simplifieddipconfig-estimate_natural_frequency)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Optional, Dict, Any`
- `from dataclasses import dataclass, field`
- `import numpy as np`
