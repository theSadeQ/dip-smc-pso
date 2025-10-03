# simulation.orchestrators.batch

**Source:** `src\simulation\orchestrators\batch.py`

## Module Overview

Batch simulation orchestrator for vectorized execution.

## Complete Source Code

```{literalinclude} ../../../src/simulation/orchestrators/batch.py
:language: python
:linenos:
```

---

## Classes

### `BatchOrchestrator`

**Inherits from:** `BaseOrchestrator`

Batch simulation orchestrator for vectorized execution.

This orchestrator can execute multiple simulations simultaneously
using vectorized operations, providing significant performance improvements
for Monte Carlo analysis and parameter sweeps.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/batch.py
:language: python
:pyobject: BatchOrchestrator
:linenos:
```

#### Methods (2)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute batch simulation.

[View full source →](#method-batchorchestrator-execute)

##### `_normalize_control_inputs(self, control_inputs, batch_size, horizon)`

Normalize control inputs to consistent batch format.

[View full source →](#method-batchorchestrator-_normalize_control_inputs)

---

## Functions

### `simulate_batch(initial_states, control_inputs, dt, horizon)`

Vectorized batch simulation function for backward compatibility.

This function provides a simplified interface similar to the original
vector_sim.simulate function.

Parameters
----------
initial_states : np.ndarray
    Initial states - shape (batch_size, state_dim)
control_inputs : np.ndarray
    Control inputs - shape (batch_size, horizon) or (batch_size, horizon, m)
dt : float
    Time step
horizon : int, optional
    Simulation horizon (inferred from control_inputs if None)
energy_limits : float, optional
    Energy limit for safety guards
state_bounds : tuple, optional
    State bounds for safety guards
stop_fn : callable, optional
    Early stopping function
t0 : float, optional
    Initial time
**kwargs
    Additional arguments

Returns
-------
np.ndarray
    Batch state trajectories - shape (batch_size, horizon+1, state_dim)

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/batch.py
:language: python
:pyobject: simulate_batch
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import Any, Callable, Optional`
- `import numpy as np`
- `from .base import BaseOrchestrator`
- `from ..core.interfaces import ResultContainer`
- `from ..results.containers import BatchResultContainer`
