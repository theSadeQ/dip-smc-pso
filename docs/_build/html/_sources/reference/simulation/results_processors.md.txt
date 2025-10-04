# simulation.results.processors

**Source:** `src\simulation\results\processors.py`

## Module Overview

Result processing and analysis tools.

## Complete Source Code

```{literalinclude} ../../../src/simulation/results/processors.py
:language: python
:linenos:
```

---

## Classes

### `ResultProcessor`

Process and analyze simulation results.

#### Source Code

```{literalinclude} ../../../src/simulation/results/processors.py
:language: python
:pyobject: ResultProcessor
:linenos:
```

#### Methods (4)

##### `compute_statistics(states)`

Compute basic statistics for state trajectories.

[View full source →](#method-resultprocessor-compute_statistics)

##### `compute_energy_metrics(states)`

Compute energy-related metrics.

[View full source →](#method-resultprocessor-compute_energy_metrics)

##### `compute_control_metrics(controls)`

Compute control effort metrics.

[View full source →](#method-resultprocessor-compute_control_metrics)

##### `analyze_trajectory(self, result_container)`

Comprehensive trajectory analysis.

[View full source →](#method-resultprocessor-analyze_trajectory)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Any, Dict, List, Optional, Tuple`
- `import numpy as np`
