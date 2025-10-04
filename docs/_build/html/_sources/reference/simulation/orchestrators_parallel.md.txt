# simulation.orchestrators.parallel

**Source:** `src\simulation\orchestrators\parallel.py`

## Module Overview

Parallel simulation orchestrator for multi-threaded execution.

## Complete Source Code

```{literalinclude} ../../../src/simulation/orchestrators/parallel.py
:language: python
:linenos:
```

---

## Classes

### `ParallelOrchestrator`

**Inherits from:** `BaseOrchestrator`

Parallel simulation orchestrator for multi-threaded execution.

This orchestrator executes multiple simulations in parallel using
a thread pool, providing performance improvements for independent
simulation runs such as Monte Carlo analysis.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/parallel.py
:language: python
:pyobject: ParallelOrchestrator
:linenos:
```

#### Methods (4)

##### `__init__(self, context, max_workers)`

Initialize parallel orchestrator.

[View full source →](#method-parallelorchestrator-__init__)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute parallel simulation.

[View full source →](#method-parallelorchestrator-execute)

##### `_execute_parallel_batch(self, initial_states, control_inputs, dt, horizon)`

Execute batch simulations in parallel.

[View full source →](#method-parallelorchestrator-_execute_parallel_batch)

##### `_run_single_simulation(self, initial_state, control_inputs, dt, horizon, kwargs)`

Run a single simulation using sequential orchestrator.

[View full source →](#method-parallelorchestrator-_run_single_simulation)

---

### `WorkerPool`

Reusable worker pool for parallel simulations.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/parallel.py
:language: python
:pyobject: WorkerPool
:linenos:
```

#### Methods (4)

##### `__init__(self, max_workers)`

Initialize worker pool.

[View full source →](#method-workerpool-__init__)

##### `__enter__(self)`

Enter context manager.

[View full source →](#method-workerpool-__enter__)

##### `__exit__(self, exc_type, exc_val, exc_tb)`

Exit context manager.

[View full source →](#method-workerpool-__exit__)

##### `map_simulations(self, simulation_fn, parameters)`

Map simulation function over parameter list.

[View full source →](#method-workerpool-map_simulations)

---

## Functions

### `run_parallel_simulations(simulation_configs, max_workers)`

Run multiple simulations in parallel.

Parameters
----------
simulation_configs : list
    List of simulation configuration dictionaries
max_workers : int, optional
    Maximum number of worker threads

Returns
-------
list
    List of simulation results

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/parallel.py
:language: python
:pyobject: run_parallel_simulations
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `import time`
- `from concurrent.futures import ThreadPoolExecutor, as_completed`
- `from typing import Any, Callable, List, Optional`
- `import numpy as np`
- `from .base import BaseOrchestrator`
- `from .sequential import SequentialOrchestrator`
- `from ..core.interfaces import ResultContainer`
- `from ..results.containers import BatchResultContainer`
