# utils.monitoring.latency

**Source:** `src\utils\monitoring\latency.py`

## Module Overview

Real-time latency monitoring for control loops.

Provides tools for monitoring control loop execution times and detecting
deadline violations in real-time systems.

## Complete Source Code

```{literalinclude} ../../../src/utils/monitoring/latency.py
:language: python
:linenos:
```

---

## Classes

### `LatencyMonitor`

Measure and analyse loop latency.

Parameters
----------
dt : float
    Nominal control period (seconds).
margin : float, optional
    Fraction of ``dt`` regarded as acceptable margin before
    flagging an overrun. Defaults to 0.9; a latency exceeding
    ``dt`` will always be counted as a missed deadline.

#### Source Code

```{literalinclude} ../../../src/utils/monitoring/latency.py
:language: python
:pyobject: LatencyMonitor
:linenos:
```

#### Methods (8)

##### `__init__(self, dt, margin)`

[View full source →](#method-latencymonitor-__init__)

##### `start(self)`

Record the start time and return it.

[View full source →](#method-latencymonitor-start)

##### `end(self, start_time)`

Record the end time and determine if a deadline was missed.

[View full source →](#method-latencymonitor-end)

##### `stats(self)`

Return median and 95th percentile of recorded latencies.

[View full source →](#method-latencymonitor-stats)

##### `missed_rate(self)`

Return the fraction of samples that missed the deadline.

[View full source →](#method-latencymonitor-missed_rate)

##### `enforce(self, m, k)`

Check a weakly‑hard (m,k) deadline miss constraint.

[View full source →](#method-latencymonitor-enforce)

##### `reset(self)`

Clear all recorded samples.

[View full source →](#method-latencymonitor-reset)

##### `get_recent_stats(self, n)`

Get statistics for the most recent n samples.

[View full source →](#method-latencymonitor-get_recent_stats)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import List, Tuple`
- `import numpy as np`
