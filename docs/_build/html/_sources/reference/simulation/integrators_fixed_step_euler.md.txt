# simulation.integrators.fixed_step.euler

**Source:** `src\simulation\integrators\fixed_step\euler.py`

## Module Overview

Euler integration methods (explicit and implicit).

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/euler.py
:language: python
:linenos:
```

---

## Classes

### `ForwardEuler`

**Inherits from:** `BaseIntegrator`

Forward (explicit) Euler integration method.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/euler.py
:language: python
:pyobject: ForwardEuler
:linenos:
```

#### Methods (3)

##### `order(self)`

Integration method order.

[View full source →](#method-forwardeuler-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-forwardeuler-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using forward Euler method.

[View full source →](#method-forwardeuler-integrate)

---

### `BackwardEuler`

**Inherits from:** `BaseIntegrator`

Backward (implicit) Euler integration method.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/euler.py
:language: python
:pyobject: BackwardEuler
:linenos:
```

#### Methods (4)

##### `__init__(self, rtol, atol, max_iterations)`

Initialize backward Euler integrator.

[View full source →](#method-backwardeuler-__init__)

##### `order(self)`

Integration method order.

[View full source →](#method-backwardeuler-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-backwardeuler-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using backward Euler method.

[View full source →](#method-backwardeuler-integrate)

---

### `ModifiedEuler`

**Inherits from:** `BaseIntegrator`

Modified Euler method (Heun's method).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/euler.py
:language: python
:pyobject: ModifiedEuler
:linenos:
```

#### Methods (3)

##### `order(self)`

Integration method order.

[View full source →](#method-modifiedeuler-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-modifiedeuler-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using modified Euler (Heun's) method.

[View full source →](#method-modifiedeuler-integrate)

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable`
- `import numpy as np`
- `from scipy.optimize import fsolve`
- `from ..base import BaseIntegrator`
