# simulation.safety.monitors

**Source:** `src\simulation\safety\monitors.py`

## Module Overview

Performance and safety monitoring for simulation execution.

## Complete Source Code

```{literalinclude} ../../../src/simulation/safety/monitors.py
:language: python
:linenos:
```

---

## Classes

### `SimulationPerformanceMonitor`

**Inherits from:** `PerformanceMonitor`

Monitor simulation execution performance.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/monitors.py
:language: python
:pyobject: SimulationPerformanceMonitor
:linenos:
```

#### Methods (4)

##### `__init__(self)`

Initialize performance monitor.

[View full source →](#method-simulationperformancemonitor-__init__)

##### `start_timing(self, operation)`

Start timing an operation.

[View full source →](#method-simulationperformancemonitor-start_timing)

##### `end_timing(self, operation)`

End timing and return elapsed time.

[View full source →](#method-simulationperformancemonitor-end_timing)

##### `get_statistics(self)`

Get performance statistics.

[View full source →](#method-simulationperformancemonitor-get_statistics)

---

### `SafetyMonitor`

Monitor safety violations and system health.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/monitors.py
:language: python
:pyobject: SafetyMonitor
:linenos:
```

#### Methods (5)

##### `__init__(self)`

Initialize safety monitor.

[View full source →](#method-safetymonitor-__init__)

##### `record_violation(self, violation_type, message, step)`

Record a safety violation.

[View full source →](#method-safetymonitor-record_violation)

##### `record_warning(self, warning_type, message, step)`

Record a safety warning.

[View full source →](#method-safetymonitor-record_warning)

##### `get_safety_report(self)`

Get comprehensive safety report.

[View full source →](#method-safetymonitor-get_safety_report)

##### `_compute_safety_score(self)`

Compute overall safety score (0-1, higher is better).

[View full source →](#method-safetymonitor-_compute_safety_score)

---

### `SystemHealthMonitor`

Monitor overall system health and performance.

#### Source Code

```{literalinclude} ../../../src/simulation/safety/monitors.py
:language: python
:pyobject: SystemHealthMonitor
:linenos:
```

#### Methods (5)

##### `__init__(self, history_length)`

Initialize system health monitor.

[View full source →](#method-systemhealthmonitor-__init__)

##### `update(self, state, control, metrics)`

Update system health with new data.

[View full source →](#method-systemhealthmonitor-update)

##### `get_health_status(self)`

Get current system health status.

[View full source →](#method-systemhealthmonitor-get_health_status)

##### `_analyze_stability(self, states)`

Analyze state stability (0-1, higher is more stable).

[View full source →](#method-systemhealthmonitor-_analyze_stability)

##### `_analyze_control_effort(self, controls)`

Analyze control effort (0-1, higher means more effort).

[View full source →](#method-systemhealthmonitor-_analyze_control_effort)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import Any, Dict, List, Optional`
- `import numpy as np`
- `from ..core.interfaces import PerformanceMonitor`
