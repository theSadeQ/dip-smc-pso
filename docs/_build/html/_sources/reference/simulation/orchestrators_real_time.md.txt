# simulation.orchestrators.real_time

**Source:** `src\simulation\orchestrators\real_time.py`

## Module Overview

Real-time simulation orchestrator with timing constraints.

## Complete Source Code

```{literalinclude} ../../../src/simulation/orchestrators/real_time.py
:language: python
:linenos:
```

---

## Classes

### `RealTimeOrchestrator`

**Inherits from:** `BaseOrchestrator`

Real-time simulation orchestrator with timing constraints.

This orchestrator executes simulations with real-time timing constraints,
useful for hardware-in-the-loop testing and real-time control verification.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/real_time.py
:language: python
:pyobject: RealTimeOrchestrator
:linenos:
```

#### Methods (5)

##### `__init__(self, context, real_time_factor, tolerance)`

Initialize real-time orchestrator.

[View full source →](#method-realtimeorchestrator-__init__)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute real-time simulation.

[View full source →](#method-realtimeorchestrator-execute)

##### `_compute_control(self, controller, t, state, step)`

Compute control input with timing measurement.

[View full source →](#method-realtimeorchestrator-_compute_control)

##### `get_real_time_statistics(self)`

Get real-time execution statistics.

[View full source →](#method-realtimeorchestrator-get_real_time_statistics)

##### `set_real_time_factor(self, factor)`

Set real-time scaling factor.

[View full source →](#method-realtimeorchestrator-set_real_time_factor)

---

### `HardwareInLoopOrchestrator`

**Inherits from:** `RealTimeOrchestrator`

Hardware-in-the-loop simulation orchestrator.

Extends real-time orchestrator with hardware interface capabilities.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/real_time.py
:language: python
:pyobject: HardwareInLoopOrchestrator
:linenos:
```

#### Methods (4)

##### `__init__(self, context, hardware_interface, real_time_factor, tolerance)`

Initialize HIL orchestrator.

[View full source →](#method-hardwareinlooporchestrator-__init__)

##### `_read_hardware_state(self)`

Read state from hardware sensors.

[View full source →](#method-hardwareinlooporchestrator-_read_hardware_state)

##### `_write_hardware_control(self, control)`

Write control to hardware actuators.

[View full source →](#method-hardwareinlooporchestrator-_write_hardware_control)

##### `execute_hil(self, controller, horizon, dt)`

Execute hardware-in-the-loop simulation.

[View full source →](#method-hardwareinlooporchestrator-execute_hil)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import Any, Callable, Optional`
- `import numpy as np`
- `from .base import BaseOrchestrator`
- `from ..core.interfaces import ResultContainer`
- `from ..core.time_domain import RealTimeScheduler`
- `from ..results.containers import StandardResultContainer`
