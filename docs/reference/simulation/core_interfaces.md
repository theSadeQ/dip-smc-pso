# simulation.core.interfaces

**Source:** `src\simulation\core\interfaces.py`

## Module Overview

Abstract base classes defining simulation framework interfaces.

## Complete Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:linenos:
```

---

## Classes

### `SimulationEngine`

**Inherits from:** `ABC`

Base interface for all simulation engines.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: SimulationEngine
:linenos:
```

#### Methods (1)

##### `step(self, state, control, dt)`

Execute a single simulation step.

[View full source →](#method-simulationengine-step)

---

### `Integrator`

**Inherits from:** `ABC`

Base interface for numerical integration methods.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: Integrator
:linenos:
```

#### Methods (3)

##### `integrate(self, dynamics_fn, state, control, dt)`

Integrate dynamics forward by one time step.

[View full source →](#method-integrator-integrate)

##### `order(self)`

Integration method order.

[View full source →](#method-integrator-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-integrator-adaptive)

---

### `Orchestrator`

**Inherits from:** `ABC`

Base interface for simulation execution strategies.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: Orchestrator
:linenos:
```

#### Methods (1)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute simulation with specified strategy.

[View full source →](#method-orchestrator-execute)

---

### `SimulationStrategy`

**Inherits from:** `ABC`

Base interface for simulation analysis strategies (Monte Carlo, sensitivity, etc.).

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: SimulationStrategy
:linenos:
```

#### Methods (1)

##### `analyze(self, simulation_fn, parameters)`

Perform strategy-specific analysis.

[View full source →](#method-simulationstrategy-analyze)

---

### `SafetyGuard`

**Inherits from:** `ABC`

Base interface for safety monitoring and constraints.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: SafetyGuard
:linenos:
```

#### Methods (2)

##### `check(self, state, step_idx)`

Check safety conditions.

[View full source →](#method-safetyguard-check)

##### `get_violation_message(self)`

Get description of last safety violation.

[View full source →](#method-safetyguard-get_violation_message)

---

### `ResultContainer`

**Inherits from:** `ABC`

Base interface for simulation result containers.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: ResultContainer
:linenos:
```

#### Methods (4)

##### `add_trajectory(self, states, times)`

Add a simulation trajectory to results.

[View full source →](#method-resultcontainer-add_trajectory)

##### `get_states(self)`

Get state trajectories.

[View full source →](#method-resultcontainer-get_states)

##### `get_times(self)`

Get time vectors.

[View full source →](#method-resultcontainer-get_times)

##### `export(self, format_type, filepath)`

Export results to specified format.

[View full source →](#method-resultcontainer-export)

---

### `DataLogger`

**Inherits from:** `ABC`

Base interface for simulation data logging.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: DataLogger
:linenos:
```

#### Methods (2)

##### `log_step(self, step_data)`

Log data from a simulation step.

[View full source →](#method-datalogger-log_step)

##### `finalize(self)`

Finalize logging and cleanup resources.

[View full source →](#method-datalogger-finalize)

---

### `PerformanceMonitor`

**Inherits from:** `ABC`

Base interface for performance monitoring.

#### Source Code

```{literalinclude} ../../../src/simulation/core/interfaces.py
:language: python
:pyobject: PerformanceMonitor
:linenos:
```

#### Methods (3)

##### `start_timing(self, operation)`

Start timing an operation.

[View full source →](#method-performancemonitor-start_timing)

##### `end_timing(self, operation)`

End timing and return elapsed time.

[View full source →](#method-performancemonitor-end_timing)

##### `get_statistics(self)`

Get performance statistics.

[View full source →](#method-performancemonitor-get_statistics)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, List, Optional, Tuple, Union, Callable`
- `import numpy as np`
