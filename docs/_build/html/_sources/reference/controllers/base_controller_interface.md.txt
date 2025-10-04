# controllers.base.controller_interface

**Source:** `src\controllers\base\controller_interface.py`

## Module Overview

Abstract base controller interface for the double inverted pendulum system.

## Complete Source Code

```{literalinclude} ../../../src/controllers/base/controller_interface.py
:language: python
:linenos:
```

---

## Classes

### `ControllerInterface`

**Inherits from:** `ABC`

Abstract base class for all controllers in the DIP system.

This interface defines the common methods that all controllers must implement,
ensuring consistency and interoperability across different control algorithms.

#### Source Code

```{literalinclude} ../../../src/controllers/base/controller_interface.py
:language: python
:pyobject: ControllerInterface
:linenos:
```

#### Methods (7)

##### `__init__(self, max_force, dt)`

Initialize the base controller.

[View full source →](#method-controllerinterface-__init__)

##### `compute_control(self, state, reference)`

Compute the control action for the given state.

[View full source →](#method-controllerinterface-compute_control)

##### `reset(self)`

Reset the controller internal state.

[View full source →](#method-controllerinterface-reset)

##### `_reset_state(self)`

Reset internal controller state variables.

[View full source →](#method-controllerinterface-_reset_state)

##### `step(self, state, reference)`

Perform one control step.

[View full source →](#method-controllerinterface-step)

##### `parameters(self)`

Get controller parameters as a dictionary.

[View full source →](#method-controllerinterface-parameters)

##### `__repr__(self)`

String representation of the controller.

[View full source →](#method-controllerinterface-__repr__)

---

## Dependencies

This module imports:

- `from abc import ABC, abstractmethod`
- `from typing import Any, Optional, Tuple, Union`
- `import numpy as np`
