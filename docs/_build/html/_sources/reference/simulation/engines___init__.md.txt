# simulation.engines.__init__

**Source:** `src\simulation\engines\__init__.py`

## Module Overview

Simulation engines and numerical integration methods.

## Complete Source Code

```{literalinclude} ../../../src/simulation/engines/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .simulation_runner import get_step_fn`
- `from .adaptive_integrator import rk45_step`
- `from .vector_sim import simulate`
