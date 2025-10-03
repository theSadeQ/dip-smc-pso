# simulation.core.time_domain

**Source:** `src\simulation\core\time_domain.py`

## Module Overview

Time domain management and scheduling utilities for simulation framework.

## Complete Source Code

```{literalinclude} ../../../src/simulation/core/time_domain.py
:language: python
:linenos:
```

---

## Classes

### `TimeManager`

Manages time-related aspects of simulation execution.

#### Source Code

```{literalinclude} ../../../src/simulation/core/time_domain.py
:language: python
:pyobject: TimeManager
:linenos:
```

#### Methods (12)

##### `__init__(self, dt, total_time, horizon)`

Initialize time manager.

[View full source →](#method-timemanager-__init__)

##### `current_time(self)`

Current simulation time.

[View full source →](#method-timemanager-current_time)

##### `current_step(self)`

Current simulation step.

[View full source →](#method-timemanager-current_step)

##### `progress(self)`

Simulation progress as fraction (0.0 to 1.0).

[View full source →](#method-timemanager-progress)

##### `start_simulation(self)`

Mark simulation start time.

[View full source →](#method-timemanager-start_simulation)

##### `advance_step(self, dt)`

Advance simulation by one time step.

[View full source →](#method-timemanager-advance_step)

##### `is_finished(self)`

Check if simulation is complete.

[View full source →](#method-timemanager-is_finished)

##### `remaining_time(self)`

Get remaining simulation time.

[View full source →](#method-timemanager-remaining_time)

##### `remaining_steps(self)`

Get remaining simulation steps.

[View full source →](#method-timemanager-remaining_steps)

##### `get_time_vector(self)`

Generate time vector for current simulation.

[View full source →](#method-timemanager-get_time_vector)

##### `wall_clock_elapsed(self)`

Get elapsed wall clock time since simulation start.

[View full source →](#method-timemanager-wall_clock_elapsed)

##### `real_time_factor(self)`

Compute real-time factor (simulation_time / wall_clock_time).

[View full source →](#method-timemanager-real_time_factor)

---

### `RealTimeScheduler`

Scheduler for real-time simulation execution.

#### Source Code

```{literalinclude} ../../../src/simulation/core/time_domain.py
:language: python
:pyobject: RealTimeScheduler
:linenos:
```

#### Methods (5)

##### `__init__(self, target_dt, tolerance)`

Initialize real-time scheduler.

[View full source →](#method-realtimescheduler-__init__)

##### `start_step(self)`

Mark start of a real-time step.

[View full source →](#method-realtimescheduler-start_step)

##### `wait_for_next_step(self)`

Wait until next step deadline.

[View full source →](#method-realtimescheduler-wait_for_next_step)

##### `get_timing_stats(self)`

Get real-time execution statistics.

[View full source →](#method-realtimescheduler-get_timing_stats)

##### `reset(self)`

Reset scheduler state.

[View full source →](#method-realtimescheduler-reset)

---

### `AdaptiveTimeStep`

Adaptive time step management for integration.

#### Source Code

```{literalinclude} ../../../src/simulation/core/time_domain.py
:language: python
:pyobject: AdaptiveTimeStep
:linenos:
```

#### Methods (3)

##### `__init__(self, initial_dt, min_dt, max_dt, safety_factor, growth_factor, shrink_factor)`

Initialize adaptive time step controller.

[View full source →](#method-adaptivetimestep-__init__)

##### `update_step_size(self, error_estimate, tolerance)`

Update time step based on error estimate.

[View full source →](#method-adaptivetimestep-update_step_size)

##### `get_statistics(self)`

Get adaptive time step statistics.

[View full source →](#method-adaptivetimestep-get_statistics)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import Any, Dict, List, Optional, Tuple, Callable`
- `import numpy as np`
