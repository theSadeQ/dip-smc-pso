# simulation.results.validators

**Source:** `src\simulation\results\validators.py`

## Module Overview

Result validation and sanity checking.

## Complete Source Code

```{literalinclude} ../../../src/simulation/results/validators.py
:language: python
:linenos:
```

---

## Classes

### `ResultValidator`

Validate simulation results for correctness and sanity.

#### Source Code

```{literalinclude} ../../../src/simulation/results/validators.py
:language: python
:pyobject: ResultValidator
:linenos:
```

#### Methods (4)

##### `validate_basic_structure(result_container)`

Validate basic result structure.

[View full source →](#method-resultvalidator-validate_basic_structure)

##### `validate_time_consistency(times, tolerance)`

Validate time vector consistency.

[View full source →](#method-resultvalidator-validate_time_consistency)

##### `validate_physical_constraints(states, bounds)`

Validate physical constraint satisfaction.

[View full source →](#method-resultvalidator-validate_physical_constraints)

##### `comprehensive_validation(self, result_container, validation_config)`

Perform comprehensive result validation.

[View full source →](#method-resultvalidator-comprehensive_validation)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Tuple`
- `import numpy as np`
