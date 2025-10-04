# simulation.integrators.fixed_step.runge_kutta

**Source:** `src\simulation\integrators\fixed_step\runge_kutta.py`

## Module Overview

Fixed step-size Runge-Kutta integration methods.

## Complete Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/runge_kutta.py
:language: python
:linenos:
```

---

## Classes

### `RungeKutta2`

**Inherits from:** `BaseIntegrator`

Second-order Runge-Kutta method (midpoint rule).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/runge_kutta.py
:language: python
:pyobject: RungeKutta2
:linenos:
```

#### Methods (3)

##### `order(self)`

Integration method order.

[View full source →](#method-rungekutta2-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-rungekutta2-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using second-order Runge-Kutta (midpoint) method.

[View full source →](#method-rungekutta2-integrate)

---

### `RungeKutta4`

**Inherits from:** `BaseIntegrator`

Fourth-order Runge-Kutta method (classic RK4).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/runge_kutta.py
:language: python
:pyobject: RungeKutta4
:linenos:
```

#### Methods (3)

##### `order(self)`

Integration method order.

[View full source →](#method-rungekutta4-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-rungekutta4-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using fourth-order Runge-Kutta method.

[View full source →](#method-rungekutta4-integrate)

---

### `RungeKutta38`

**Inherits from:** `BaseIntegrator`

Runge-Kutta 3/8 rule (alternative 4th-order method).

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/runge_kutta.py
:language: python
:pyobject: RungeKutta38
:linenos:
```

#### Methods (3)

##### `order(self)`

Integration method order.

[View full source →](#method-rungekutta38-order)

##### `adaptive(self)`

Whether integrator supports adaptive step size.

[View full source →](#method-rungekutta38-adaptive)

##### `integrate(self, dynamics_fn, state, control, dt, t)`

Integrate using Runge-Kutta 3/8 rule.

[View full source →](#method-rungekutta38-integrate)

---

### `ClassicalRungeKutta`

**Inherits from:** `RungeKutta4`

Alias for standard RK4 method for backward compatibility.

#### Source Code

```{literalinclude} ../../../src/simulation/integrators/fixed_step/runge_kutta.py
:language: python
:pyobject: ClassicalRungeKutta
:linenos:
```

---

## Dependencies

This module imports:

- `from __future__ import annotations`
- `from typing import Callable`
- `import numpy as np`
- `from ..base import BaseIntegrator`
