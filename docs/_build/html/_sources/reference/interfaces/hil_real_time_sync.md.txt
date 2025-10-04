# interfaces.hil.real_time_sync

**Source:** `src\interfaces\hil\real_time_sync.py`

## Module Overview

Real-time synchronization and scheduling for HIL systems.
This module provides real-time capabilities including high-priority scheduling,
deadline monitoring, and timing constraint enforcement for deterministic
control system execution.

## Complete Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:linenos:
```

---

## Classes

### `SchedulingPolicy`

**Inherits from:** `Enum`

Real-time scheduling policy enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: SchedulingPolicy
:linenos:
```

---

### `TimingViolationType`

**Inherits from:** `Enum`

Timing violation type enumeration.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: TimingViolationType
:linenos:
```

---

### `TimingConstraints`

Real-time timing constraints.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: TimingConstraints
:linenos:
```

---

### `TimingEvent`

Timing event record.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: TimingEvent
:linenos:
```

---

### `DeadlineMissHandler`

Handler for deadline miss events.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: DeadlineMissHandler
:linenos:
```

#### Methods (4)

##### `__init__(self)`

[View full source →](#method-deadlinemisshandler-__init__)

##### `add_handler(self, handler)`

Add deadline miss handler.

[View full source →](#method-deadlinemisshandler-add_handler)

##### `handle_deadline_miss(self, event)`

Handle deadline miss event.

[View full source →](#method-deadlinemisshandler-handle_deadline_miss)

##### `get_statistics(self)`

Get deadline miss statistics.

[View full source →](#method-deadlinemisshandler-get_statistics)

---

### `RealTimeScheduler`

Real-time scheduler for HIL systems.

Provides deterministic scheduling with deadline monitoring,
CPU affinity control, and real-time priority management.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: RealTimeScheduler
:linenos:
```

#### Methods (14)

##### `__init__(self, sample_time, priority, cpu_affinity)`

Initialize real-time scheduler.

[View full source →](#method-realtimescheduler-__init__)

##### `start(self)`

Start real-time scheduler.

[View full source →](#method-realtimescheduler-start)

##### `stop(self)`

Stop real-time scheduler.

[View full source →](#method-realtimescheduler-stop)

##### `wait_for_next_period(self)`

Wait for next scheduling period.

[View full source →](#method-realtimescheduler-wait_for_next_period)

##### `set_constraints(self, constraints)`

Set timing constraints.

[View full source →](#method-realtimescheduler-set_constraints)

##### `get_timing_statistics(self)`

Get timing performance statistics.

[View full source →](#method-realtimescheduler-get_timing_statistics)

##### `add_deadline_miss_handler(self, handler)`

Add deadline miss handler.

[View full source →](#method-realtimescheduler-add_deadline_miss_handler)

##### `_configure_real_time(self)`

Configure real-time scheduling properties.

[View full source →](#method-realtimescheduler-_configure_real_time)

##### `_configure_linux_rt(self)`

Configure Linux real-time scheduling.

[View full source →](#method-realtimescheduler-_configure_linux_rt)

##### `_configure_psutil_rt(self)`

Configure real-time properties using psutil.

[View full source →](#method-realtimescheduler-_configure_psutil_rt)

##### `_restore_settings(self)`

Restore original scheduling settings.

[View full source →](#method-realtimescheduler-_restore_settings)

##### `_precise_sleep(self, sleep_time)`

High-precision sleep implementation.

[View full source →](#method-realtimescheduler-_precise_sleep)

##### `_handle_deadline_miss(self, current_time, deadline)`

Handle deadline miss event.

[View full source →](#method-realtimescheduler-_handle_deadline_miss)

##### `_record_jitter(self, jitter)`

Record timing jitter.

[View full source →](#method-realtimescheduler-_record_jitter)

---

### `HighResolutionTimer`

High-resolution timer for precise timing control.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: HighResolutionTimer
:linenos:
```

#### Methods (5)

##### `__init__(self)`

[View full source →](#method-highresolutiontimer-__init__)

##### `start(self)`

Start timer.

[View full source →](#method-highresolutiontimer-start)

##### `elapsed(self)`

Get elapsed time in seconds.

[View full source →](#method-highresolutiontimer-elapsed)

##### `elapsed_ns(self)`

Get elapsed time in nanoseconds.

[View full source →](#method-highresolutiontimer-elapsed_ns)

##### `sleep_until(target_time)`

Sleep until specific time.

[View full source →](#method-highresolutiontimer-sleep_until)

---

### `RTThreadScheduler`

Real-time thread scheduler for CPU-intensive tasks.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: RTThreadScheduler
:linenos:
```

#### Methods (4)

##### `__init__(self)`

[View full source →](#method-rtthreadscheduler-__init__)

##### `create_rt_thread(self, target, priority, cpu_affinity)`

Create real-time thread.

[View full source →](#method-rtthreadscheduler-create_rt_thread)

##### `start_all_threads(self)`

Start all created threads.

[View full source →](#method-rtthreadscheduler-start_all_threads)

##### `stop_all_threads(self)`

Stop all threads.

[View full source →](#method-rtthreadscheduler-stop_all_threads)

---

### `TimingSynchronizer`

Synchronize multiple real-time processes.

#### Source Code

```{literalinclude} ../../../src/interfaces/hil/real_time_sync.py
:language: python
:pyobject: TimingSynchronizer
:linenos:
```

#### Methods (4)

##### `__init__(self, num_processes)`

[View full source →](#method-timingsynchronizer-__init__)

##### `create_sync_point(self)`

Create synchronization point.

[View full source →](#method-timingsynchronizer-create_sync_point)

##### `wait_sync_point(self, sync_id, timeout)`

Wait at synchronization point.

[View full source →](#method-timingsynchronizer-wait_sync_point)

##### `get_sync_statistics(self)`

Get synchronization statistics.

[View full source →](#method-timingsynchronizer-get_sync_statistics)

---

## Dependencies

This module imports:

- `import asyncio`
- `import time`
- `import threading`
- `import os`
- `import signal`
- `from dataclasses import dataclass, field`
- `from typing import Optional, List, Callable, Dict, Any`
- `from enum import Enum`
- `import logging`
