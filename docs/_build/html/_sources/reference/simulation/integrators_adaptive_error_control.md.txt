# simulation.integrators.adaptive.error_control

**Source:** `src\simulation\integrators\adaptive\error_control.py`

## Module Overview

Error control and step size adaptation for adaptive integration.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/error_control.py
:language: python
:linenos:
```

---

## Classes

### `ErrorController`

Basic error controller for adaptive step size methods.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/error_control.py
:language: python
:pyobject: ErrorController
:linenos:
```

#### Methods (2)

##### `__init__(self, safety_factor)`

Initialize error controller.

[View full source →](#method-errorcontroller-__init__)

##### `update_step_size(self, error_norm, current_dt, min_dt, max_dt, order)`

Update step size based on error estimate.

[View full source →](#method-errorcontroller-update_step_size)

---

### `PIController`

**Inherits from:** `ErrorController`

PI (Proportional-Integral) controller for step size adaptation.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/error_control.py
:language: python
:pyobject: PIController
:linenos:
```

#### Methods (3)

##### `__init__(self, safety_factor, alpha, beta)`

Initialize PI controller.

[View full source →](#method-picontroller-__init__)

##### `update_step_size(self, error_norm, current_dt, min_dt, max_dt, order)`

Update step size using PI control.

[View full source →](#method-picontroller-update_step_size)

##### `reset(self)`

Reset controller state.

[View full source →](#method-picontroller-reset)

---

### `DeadBeatController`

**Inherits from:** `ErrorController`

Dead-beat controller for aggressive step size adaptation.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/adaptive/error_control.py
:language: python
:pyobject: DeadBeatController
:linenos:
```

#### Methods (2)

##### `__init__(self, safety_factor, target_error)`

Initialize dead-beat controller.

[View full source →](#method-deadbeatcontroller-__init__)

##### `update_step_size(self, error_norm, current_dt, min_dt, max_dt, order)`

Update step size using dead-beat control.

[View full source →](#method-deadbeatcontroller-update_step_size)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Tuple`
- `import numpy as np`
