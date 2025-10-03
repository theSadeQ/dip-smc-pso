# plant.core.dynamics

**Source:** `src\plant\core\dynamics.py`

## Module Overview

Plant core dynamics compatibility module.

This module provides backward compatibility for test modules that expect
plant dynamics components at src.plant.core.dynamics. All functionality
is re-exported from the actual implementation locations.

## Complete Source Code

```{literalinclude} ../../../src/plant/core/dynamics.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from ...core.dynamics import *`
- `from ..models.dynamics import *`
- `from ...core.dynamics import DIPDynamics, DoubleInvertedPendulum, DIPParams`
