# plant.models.simplified.__init__

**Source:** `src\plant\models\simplified\__init__.py`

## Module Overview

Simplified Double Inverted Pendulum Model.

Modular implementation of the simplified DIP dynamics with:
- Focused physics computation
- Type-safe configuration
- Numerical stability features
- Performance optimizations

Refactored from the monolithic 688-line dynamics.py file.

## Complete Source Code

```{literalinclude} ../../../src/plant/models/simplified/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .config import SimplifiedDIPConfig`
- `from .physics import SimplifiedPhysicsComputer`
- `from .dynamics import SimplifiedDIPDynamics`
