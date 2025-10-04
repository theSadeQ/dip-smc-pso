# simulation.integrators.base

**Source:** `src\simulation\integrators\base.py`

## Module Overview

Base integrator interface and common utilities.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/base.py
:language: python
:linenos:
```

---

## Classes

### `BaseIntegrator`

**Inherits from:** `Integrator`

Base class for numerical integration methods.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/base.py
:language: python
:pyobject: BaseIntegrator
:linenos:
```

#### Methods (10)

##### `__init__(self, rtol, atol)`

Initialize base integrator.

[View full source →](#method-baseintegrator-__init__)

##### `integrate(self, dynamics_fn, state, control, dt)`

Integrate dynamics forward by one time step.

[View full source →](#method-baseintegrator-integrate)

##### `order(self)`

Integration method order.

[View full source →](#method-baseintegrator-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-baseintegrator-adaptive)

##### `reset_statistics(self)`

Reset integration statistics.

[View full source →](#method-baseintegrator-reset_statistics)

##### `get_statistics(self)`

Get integration statistics.

[View full source →](#method-baseintegrator-get_statistics)

##### `integrate_step(self, dynamics_fn, state, time, dt)`

Integrate dynamics forward by one time step (interface compatibility method).

[View full source →](#method-baseintegrator-integrate_step)

##### `_update_stats(self, accepted, func_evals)`

Update integration statistics.

[View full source →](#method-baseintegrator-_update_stats)

##### `_validate_inputs(self, dynamics_fn, state, control, dt)`

Validate integration inputs.

[View full source →](#method-baseintegrator-_validate_inputs)

##### `_compute_error_norm(self, error, state)`

Compute error norm for adaptive integration.

[View full source →](#method-baseintegrator-_compute_error_norm)

---

### `IntegrationResult`

Container for integration step results.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/base.py
:language: python
:pyobject: IntegrationResult
:linenos:
```

#### Methods (1)

##### `__init__(self, state, accepted, error_estimate, suggested_dt, function_evaluations)`

Initialize integration result.

[View full source →](#method-integrationresult-__init__)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from abc import ABC, abstractmethod`
- `from typing import Any, Callable, Dict, Optional, Tuple`
- `import numpy as np`
- `from ..core.interfaces import Integrator`
