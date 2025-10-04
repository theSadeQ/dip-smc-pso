# simulation.safety.__init__

**Source:** `src\simulation\safety\__init__.py`

## Module Overview

Safety monitoring and constraint enforcement for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/safety/__init__.py
:language: python
:linenos:
```

---

## Dependencies

This module imports:

- `from .guards import apply_safety_guards, guard_no_nan, guard_energy, guard_bounds, SafetyViolationError`
- `from .constraints import StateConstraints, ControlConstraints, EnergyConstraints, ConstraintChecker`
- `from .monitors import PerformanceMonitor, SafetyMonitor, SystemHealthMonitor`
- `from .recovery import SafetyRecovery, EmergencyStop, StateLimiter`
