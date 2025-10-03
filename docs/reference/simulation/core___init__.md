# simulation.core.__init__

**Source:** `src\simulation\core\__init__.py`

## Module Overview

Core simulation framework interfaces and abstractions.

## Complete Source Code

```{literalinclude} ../../../src/simulation/core/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .interfaces import SimulationEngine, Integrator, Orchestrator, SimulationStrategy, SafetyGuard, ResultContainer`
- `from .simulation_context import SimulationContext`
- `from .state_space import StateSpaceUtilities`
- `from .time_domain import TimeManager`
