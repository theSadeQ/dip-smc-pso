# simulation.orchestrators.base

**Source:** `src\simulation\orchestrators\base.py`

## Module Overview

Base orchestrator interface and common functionality.

## Complete Source Code

```{literalinclude} ../../../src/simulation/orchestrators/base.py
:language: python
:linenos:
```

---

## Classes

### `BaseOrchestrator`

**Inherits from:** `Orchestrator`, `SimulationEngine`

Base class for simulation execution orchestrators.

#### Source Code

```{literalinclude} ../../../src/simulation/orchestrators/base.py
:language: python
:pyobject: BaseOrchestrator
:linenos:
```

#### Methods (11)

##### `__init__(self, context)`

Initialize base orchestrator.

[View full source →](#method-baseorchestrator-__init__)

##### `_create_integrator(self)`

Create appropriate integrator based on configuration.

[View full source →](#method-baseorchestrator-_create_integrator)

##### `step(self, state, control, dt)`

Execute a single simulation step.

[View full source →](#method-baseorchestrator-step)

##### `execute(self, initial_state, control_inputs, dt, horizon)`

Execute simulation with orchestrator-specific strategy.

[View full source →](#method-baseorchestrator-execute)

##### `_create_result_container(self)`

Create appropriate result container.

[View full source →](#method-baseorchestrator-_create_result_container)

##### `_validate_simulation_inputs(self, initial_state, control_inputs, dt, horizon)`

Validate simulation inputs.

[View full source →](#method-baseorchestrator-_validate_simulation_inputs)

##### `get_execution_statistics(self)`

Get execution performance statistics.

[View full source →](#method-baseorchestrator-get_execution_statistics)

##### `reset_statistics(self)`

Reset execution statistics.

[View full source →](#method-baseorchestrator-reset_statistics)

##### `_update_stats(self, num_steps, execution_time)`

Update execution statistics.

[View full source →](#method-baseorchestrator-_update_stats)

##### `set_integrator(self, integrator)`

Set custom integrator.

[View full source →](#method-baseorchestrator-set_integrator)

##### `get_integrator(self)`

Get current integrator.

[View full source →](#method-baseorchestrator-get_integrator)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Dict, Optional, Callable`
- `import numpy as np`
- `from ..core.interfaces import Orchestrator, ResultContainer, SimulationEngine`
- `from ..core.simulation_context import SimulationContext`
- `from ..results.containers import StandardResultContainer`
