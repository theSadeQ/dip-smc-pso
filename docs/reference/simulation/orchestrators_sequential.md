# simulation.orchestrators.sequential

**Source:** `src\simulation\orchestrators\sequential.py`

## Module Overview

Sequential simulation orchestrator for single-threaded execution.

## Complete Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:linenos:
```

---

## Classes

### `SequentialOrchestrator`

**Inherits from:** `BaseOrchestrator`

Sequential simulation orchestrator for single-threaded execution.

This orchestrator executes simulations step-by-step in a single thread,
providing compatibility with the original simulation_runner functionality.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: SequentialOrchestrator
:linenos:
```

#### Methods (1)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute sequential simulation.

[View full source →](#method-sequentialorchestrator-execute)

---

## Functions

### `get_step_fn()`

Legacy function for backward compatibility.

Returns
-------
callable
    Step function that dispatches to appropriate dynamics model

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: get_step_fn
:linenos:
```

---

### `_load_full_step()`

Load full dynamics step function.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: _load_full_step
:linenos:
```

---

### `_load_lowrank_step()`

Load low-rank dynamics step function.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: _load_lowrank_step
:linenos:
```

---

### `step(x, u, dt)`

Legacy step function for backward compatibility.

Parameters
----------
x : array-like
    Current state
u : array-like
    Control input
dt : float
    Time step

Returns
-------
array-like
    Next state

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: step
:linenos:
```

---

### `run_simulation()`

Legacy simulation runner for backward compatibility.

This function maintains the exact interface and behavior of the original
run_simulation function from simulation_runner.py.

Parameters
----------
controller : Any
    Controller object with __call__ or compute_control method
dynamics_model : Any
    Dynamics model with step method
sim_time : float
    Total simulation time
dt : float
    Time step
initial_state : array-like
    Initial state vector
u_max : float, optional
    Control saturation limit
seed : int, optional
    Random seed (deprecated, use rng)
rng : np.random.Generator, optional
    Random number generator
latency_margin : float, optional
    Unused (for future latency control)
fallback_controller : callable, optional
    Fallback controller for deadline misses
**_kwargs
    Additional arguments (ignored)

Returns
-------
tuple
    (times, states, controls) arrays

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/sequential.py
:language: python
:pyobject: run_simulation
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from typing import Any, Callable, Optional, Tuple`
- `import numpy as np`
- `from .base import BaseOrchestrator`
- `from ..core.interfaces import ResultContainer`
- `from ..results.containers import StandardResultContainer`
- `from ..safety.guards import apply_safety_guards`
